"""
Google Sheets logging service

Appends each lead to a configured spreadsheet and updates the row as the
workflow progresses (report generated / emailed / Drive archived).

Auth: Google service account JSON. If credentials or spreadsheet ID are not
configured, every method is a no-op so the rest of the workflow continues
unaffected — matching the SendGrid demo-mode fallback pattern.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Column order written to the sheet. Keep this aligned with `_row_for_lead`
# and the index lookups in `update_lead_status`.
HEADER_ROW = [
    "Lead ID",
    "Name",
    "Email",
    "Company",
    "Website",
    "Industry",
    "Submitted At",
    "Status",
    "Report Status",
    "Drive URL",
]


class SheetsService:
    """Append + update lead rows on a Google Sheet."""

    def __init__(self):
        self.spreadsheet_id: Optional[str] = settings.google_sheets_spreadsheet_id
        self.sheet_name: str = settings.google_sheets_sheet_name
        self._service = None
        self._service_init_failed = False

    def _client(self):
        """Lazily build the Sheets API client. Returns None if unavailable."""
        if self._service is not None or self._service_init_failed:
            return self._service

        if not self.spreadsheet_id:
            logger.info("Google Sheets logging disabled: GOOGLE_SHEETS_SPREADSHEET_ID not set")
            self._service_init_failed = True
            return None

        creds_path = settings.google_service_account_file
        if not creds_path or not Path(creds_path).exists():
            logger.warning(
                "Google Sheets logging disabled: service account file missing at %s",
                creds_path,
            )
            self._service_init_failed = True
            return None

        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=SHEETS_SCOPES
            )
            self._service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
            return self._service
        except Exception as e:
            logger.error("Failed to initialize Google Sheets client: %s", e)
            self._service_init_failed = True
            return None

    def _row_for_lead(self, lead, status: str = "processing", report_status: str = "pending", drive_url: str = "") -> list:
        return [
            str(lead.id),
            lead.name or "",
            lead.email or "",
            lead.company or "",
            lead.website or "",
            lead.industry or "",
            (lead.created_at or datetime.utcnow()).isoformat(),
            status,
            report_status,
            drive_url,
        ]

    def ensure_header(self) -> None:
        """Write the header row if the sheet looks empty. Best-effort."""
        service = self._client()
        if not service:
            return
        try:
            resp = service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A1:J1",
            ).execute()
            if resp.get("values"):
                return
            service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A1:J1",
                valueInputOption="RAW",
                body={"values": [HEADER_ROW]},
            ).execute()
            logger.info("Initialized Google Sheets header row")
        except Exception as e:
            logger.error("Failed to ensure Sheets header: %s", e)

    def append_lead(self, lead) -> bool:
        """Append a new lead row. Returns True on success."""
        service = self._client()
        if not service:
            return False
        try:
            self.ensure_header()
            row = self._row_for_lead(lead)
            service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:J",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [row]},
            ).execute()
            logger.info("Logged lead %s to Google Sheets", lead.id)
            return True
        except Exception as e:
            logger.error("Failed to append lead %s to Sheets: %s", getattr(lead, "id", "?"), e)
            return False

    def update_lead_status(
        self,
        lead_id: int,
        status: Optional[str] = None,
        report_status: Optional[str] = None,
        drive_url: Optional[str] = None,
    ) -> bool:
        """Find the row for `lead_id` and update its status columns."""
        service = self._client()
        if not service:
            return False
        try:
            resp = service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A:A",
            ).execute()
            values = resp.get("values", [])
            target_row = None
            for idx, row in enumerate(values):
                if row and str(row[0]) == str(lead_id):
                    target_row = idx + 1  # Sheets is 1-indexed
                    break

            if target_row is None:
                logger.warning("Lead %s not found in Sheets — cannot update status", lead_id)
                return False

            updates = []
            if status is not None:
                updates.append({
                    "range": f"{self.sheet_name}!H{target_row}",
                    "values": [[status]],
                })
            if report_status is not None:
                updates.append({
                    "range": f"{self.sheet_name}!I{target_row}",
                    "values": [[report_status]],
                })
            if drive_url is not None:
                updates.append({
                    "range": f"{self.sheet_name}!J{target_row}",
                    "values": [[drive_url]],
                })

            if not updates:
                return True

            service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={"valueInputOption": "RAW", "data": updates},
            ).execute()
            logger.info("Updated Sheets row for lead %s", lead_id)
            return True
        except Exception as e:
            logger.error("Failed to update Sheets row for lead %s: %s", lead_id, e)
            return False

    @property
    def enabled(self) -> bool:
        return self._client() is not None
