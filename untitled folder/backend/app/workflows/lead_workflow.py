"""
Main workflow orchestrator.

Coordinates the multi-agent pipeline that turns a submitted lead into an
emailed intelligence report, plus optional Sheets logging and Drive
archiving. Every external side-effect (DB writes, Sheets, Drive, email)
is best-effort and isolated so a single failure cannot abort the run.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Callable, Dict

from app.agents.state import WorkflowState
from app.agents.research_agent import ResearchAgent
from app.agents.insight_agent import InsightAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.audit_agent import AuditAgent
from app.agents.report_agent import ReportAgent
from app.agents.email_agent import EmailAgent
from app.services.pdf_service import PDFService
from app.services.email_service import EmailService
from app.services.database_service import DatabaseService
from app.services.sheets_service import SheetsService
from app.services.drive_service import DriveService
from app.database import SessionLocal

logger = logging.getLogger(__name__)


async def _safe(name: str, fn: Callable[[], Any]) -> Any:
    """Run a best-effort side effect (sync or async). Log + swallow failures."""
    try:
        result = fn()
        if asyncio.iscoroutine(result):
            result = await result
        return result
    except Exception as e:
        logger.error(f"{name} failed: {e}")
        return None


class LeadWorkflow:
    """Sequential multi-agent pipeline for a single lead."""

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.insight_agent = InsightAgent()
        self.competitor_agent = CompetitorAgent()
        self.audit_agent = AuditAgent()
        self.report_agent = ReportAgent()
        self.email_agent = EmailAgent()
        self.pdf_service = PDFService()
        self.email_service = EmailService()
        self.sheets_service = SheetsService()
        self.drive_service = DriveService()

    async def execute_workflow(self, state: WorkflowState) -> WorkflowState:
        logger.info(f"Starting workflow for lead: {state.lead_id}")
        db = SessionLocal()
        prev_step_count = len(state.steps_completed)
        try:
            for agent in (
                self.research_agent,
                self.insight_agent,
                self.competitor_agent,
                self.audit_agent,
                self.report_agent,
            ):
                state = await agent.execute(state)
                prev_step_count = await self._persist_new_steps(db, state, prev_step_count)

            await _safe("save_company_data", lambda: DatabaseService.save_company_data(db, state))

            await self._generate_and_archive_pdf(db, state)
            prev_step_count = await self._persist_new_steps(db, state, prev_step_count)

            state = await self.email_agent.execute(state)
            prev_step_count = await self._persist_new_steps(db, state, prev_step_count)

            await self._send_email_and_update(db, state)
            prev_step_count = await self._persist_new_steps(db, state, prev_step_count)

            state.add_step("workflow_completed")
            await self._persist_new_steps(db, state, prev_step_count)
            logger.info(f"Workflow completed for lead: {state.lead_id}")
        except Exception as e:
            logger.error(f"Workflow failed: {e}", exc_info=True)
            state.add_error("workflow", str(e))
        finally:
            db.close()
        return state

    @staticmethod
    async def _persist_new_steps(db, state: WorkflowState, prev_count: int) -> int:
        """Persist any newly-completed steps as LogEntry rows. Returns new count."""
        for step in state.steps_completed[prev_count:]:
            await _safe(
                f"log_event:{step}",
                lambda s=step: DatabaseService.log_event(db, state.lead_id, s, "success"),
            )
        return len(state.steps_completed)

    async def _generate_and_archive_pdf(self, db, state: WorkflowState) -> None:
        try:
            pdf_path = self.pdf_service.generate_pdf(
                state.report_html,
                state.company_name,
                state.lead_id,
                state=state,
            )
        except Exception as e:
            logger.error(f"PDF generation failed: {e}", exc_info=True)
            state.add_error("pdf_generation", str(e))
            return

        state.pdf_path = pdf_path
        state.add_step("pdf_generated")
        await _safe("save_report", lambda: DatabaseService.save_report(db, state.lead_id, pdf_path))

        # Bonus: Google Drive archive
        drive_url = await _safe(
            "drive_upload",
            lambda: self.drive_service.upload_pdf(pdf_path, state.lead_id, state.company_name),
        )
        if drive_url:
            DatabaseService.update_report_fields(db, state.lead_id, google_drive_url=drive_url)
            await _safe(
                "sheets_update_drive",
                lambda: self.sheets_service.update_lead_status(
                    state.lead_id, report_status="generated", drive_url=drive_url
                ),
            )
        else:
            await _safe(
                "sheets_update_generated",
                lambda: self.sheets_service.update_lead_status(
                    state.lead_id, report_status="generated"
                ),
            )

    async def _send_email_and_update(self, db, state: WorkflowState) -> None:
        try:
            email_sent = await self.email_service.send_report_email(
                to_email=state.lead_email,
                to_name=state.lead_name,
                company_name=state.company_name,
                email_content=state.email_content,
                pdf_path=state.pdf_path,
            )
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            state.add_error("email_sending", str(e))
            return

        if email_sent:
            state.add_step("email_sent")
            DatabaseService.update_report_fields(
                db,
                state.lead_id,
                email_sent=True,
                status="emailed",
                email_sent_at=datetime.utcnow(),
            )
            await _safe(
                "sheets_update_emailed",
                lambda: self.sheets_service.update_lead_status(
                    state.lead_id, status="completed", report_status="emailed"
                ),
            )
        else:
            state.add_error("email_sending", "Failed to send email")
            await _safe(
                "sheets_update_email_failed",
                lambda: self.sheets_service.update_lead_status(
                    state.lead_id, status="email_failed"
                ),
            )

    # Ordered list of LogEntry.event values produced as the pipeline runs.
    # Used by `get_workflow_status` to translate persisted events into a
    # progress percentage rather than returning a hardcoded value.
    _PIPELINE_STEPS = (
        ("lead_captured", "Lead captured"),
        ("research_complete", "Researching company"),
        ("insight_complete", "Generating AI insights"),
        ("competitor_analysis_complete", "Analyzing competitors"),
        ("audit_complete", "Running website audit"),
        ("report_generated", "Generating report"),
        ("pdf_generated", "Creating PDF"),
        ("email_generated", "Drafting outreach email"),
        ("email_sent", "Sending email"),
        ("workflow_completed", "Done"),
    )

    async def get_workflow_status(self, lead_id: int) -> Dict[str, Any]:
        """Read real progress from the LogEntry / Report tables."""
        from app.models.database import LogEntry, Report  # local import to avoid cycle

        db = SessionLocal()
        try:
            events = {
                row.event
                for row in db.query(LogEntry.event)
                .filter(LogEntry.lead_id == lead_id, LogEntry.status != "failure")
                .all()
            }
            # Belt and braces: cross-check terminal stages against Report so
            # the status endpoint still reflects reality if a LogEntry write
            # failed mid-run.
            report = db.query(Report).filter(Report.lead_id == lead_id).first()
            if report:
                if report.pdf_path:
                    events.add("pdf_generated")
                if report.email_sent:
                    events.add("email_sent")
                if report.status == "emailed":
                    events.add("workflow_completed")

            completed = [label for key, label in self._PIPELINE_STEPS if key in events]
            current_index = len(completed)
            total = len(self._PIPELINE_STEPS)
            next_label = (
                self._PIPELINE_STEPS[current_index][1]
                if current_index < total
                else "Done"
            )
            overall_status = (
                "completed" if "workflow_completed" in events else "processing"
            )
            return {
                "lead_id": lead_id,
                "status": overall_status,
                "current_step": next_label if overall_status == "processing" else "Done",
                "completed_steps": completed,
                "progress_percentage": int((current_index / total) * 100),
            }
        finally:
            db.close()
