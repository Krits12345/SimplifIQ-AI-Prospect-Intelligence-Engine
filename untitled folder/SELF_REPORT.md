# SELF_REPORT

## Project Overview

This project delivers a lead intelligence workflow for business lead generation and analysis. The app collects company data, performs research and competitor benchmarking, audits website health, and generates a professional report with actionable recommendations.

## Architecture

- `frontend/`: React + Vite application with Tailwind CSS and React Query.
- `backend/`: FastAPI service with SQLAlchemy and SQLite.
- `backend/app/workflows/lead_workflow.py`: orchestrates research, audit, report generation, PDF creation, and email delivery.
- `backend/app/routes/reports.py`: exposes report retrieval, PDF download, and email send endpoints.
- `backend/app/services/pdf_service.py`: generates PDF if environment supports WeasyPrint.
- `backend/app/services/email_service.py`: sends email via SendGrid or falls back to demo mode.

## Implemented Features

- Professional generated report preview on the workflow status page.
- Downloadable PDF report from the backend endpoint.
- Email report delivery using SendGrid configuration.
- Graceful fallback when SendGrid API key is absent: demo send flow and logged fallback behavior.
- Frontend PDF export fallback with `html2canvas` and `jspdf` for browser-only usage.
- Persistent lead and report metadata in SQLite.

## Assumptions

- The app is intended as a demo/proof-of-concept workflow engine, not a production CRM.
- Sensitive production email delivery uses SendGrid, but demo mode is acceptable for local development.
- Full authentication and user management are intentionally excluded.
- Some report generation relies on structured text and HTML templates rather than fully polished design.

## Limitations

- PDF generation depends on WeasyPrint availability in the backend environment.
- The report preview is built from structured report data, but may need richer styling for production.
- Email delivery status updates are stored only after a successful send attempt.
- There is no retry logic for failed email or PDF generation.

## Future Improvements

- Add a dedicated `reports` database model to store full content and version history.
- Improve report styling and export fidelity with a full CSS/HTML report builder.
- Add login/signup and secure lead ownership.
- Add more robust fallback handling with retry queues, toast notifications, and offline mode.
- Build a report history page listing past exported and emailed reports.
