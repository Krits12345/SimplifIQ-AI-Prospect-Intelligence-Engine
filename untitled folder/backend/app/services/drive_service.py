"""
Google Drive archiving service

Uploads the generated PDF report to a configured Google Drive folder and
returns a shareable link that gets persisted on the Report record.

Auth: Google service account JSON. If credentials or folder ID are not
configured the upload is skipped — the rest of the workflow continues
without interruption.
"""

import logging
from pathlib import Path
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.file"]


class DriveService:
    """Upload PDF reports to a Google Drive folder."""

    def __init__(self):
        self.folder_id: Optional[str] = settings.google_drive_folder_id
        self._service = None
        self._service_init_failed = False

    def _client(self):
        if self._service is not None or self._service_init_failed:
            return self._service

        if not self.folder_id:
            logger.info("Google Drive archiving disabled: GOOGLE_DRIVE_FOLDER_ID not set")
            self._service_init_failed = True
            return None

        creds_path = settings.google_service_account_file
        if not creds_path or not Path(creds_path).exists():
            logger.warning(
                "Google Drive archiving disabled: service account file missing at %s",
                creds_path,
            )
            self._service_init_failed = True
            return None

        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                creds_path, scopes=DRIVE_SCOPES
            )
            self._service = build("drive", "v3", credentials=credentials, cache_discovery=False)
            return self._service
        except Exception as e:
            logger.error("Failed to initialize Google Drive client: %s", e)
            self._service_init_failed = True
            return None

    def upload_pdf(self, pdf_path: str, lead_id: int, company_name: str) -> Optional[str]:
        """
        Upload `pdf_path` to the configured Drive folder.

        Returns the webViewLink on success, or None if Drive is disabled or
        the upload failed.
        """
        service = self._client()
        if not service:
            return None

        local = Path(pdf_path)
        if not local.exists():
            logger.error("Cannot archive to Drive: file missing at %s", pdf_path)
            return None

        try:
            from googleapiclient.http import MediaFileUpload

            safe_company = "".join(c for c in company_name if c.isalnum() or c in (" ", "_", "-")).strip() or "company"
            drive_name = f"{safe_company} - Lead {lead_id} - Intelligence Report.pdf"

            file_metadata = {
                "name": drive_name,
                "parents": [self.folder_id],
            }
            media = MediaFileUpload(str(local), mimetype="application/pdf", resumable=False)

            uploaded = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, webViewLink",
            ).execute()

            try:
                service.permissions().create(
                    fileId=uploaded["id"],
                    body={"role": "reader", "type": "anyone"},
                    fields="id",
                ).execute()
            except Exception as perm_err:
                # Public sharing may be blocked by org policy — link still works
                # for anyone with folder access.
                logger.warning("Could not set public read on Drive file: %s", perm_err)

            link = uploaded.get("webViewLink")
            logger.info("Archived report for lead %s to Drive: %s", lead_id, link)
            return link
        except Exception as e:
            logger.error("Failed to archive PDF for lead %s to Drive: %s", lead_id, e)
            return None

    @property
    def enabled(self) -> bool:
        return self._client() is not None
