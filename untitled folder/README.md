# 🚀 SimplifIQ AI Prospect Intelligence Engine

<div align="center">

### Transform raw leads into AI-powered company intelligence reports instantly

An AI-powered prospect intelligence platform that automatically researches companies, analyzes websites, identifies competitors, generates consulting-style insights, creates professional reports, and drafts personalized outreach emails.

![React](https://img.shields.io/badge/React-18-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38BDF8)
![Status](https://img.shields.io/badge/Status-Production--Ready-success)

</div>

---

# ✨ Why SimplifIQ?

Traditional lead systems stop at collecting information:

```text
Lead Form → CRM Entry
```

SimplifIQ goes further:

```text
Lead Form
     ↓
AI Research
     ↓
Website Analysis
     ↓
Competitor Intelligence
     ↓
Confidence Scoring
     ↓
Report Generation
     ↓
Personalized Outreach
```

Instead of behaving like a form collector, SimplifIQ acts like an AI-powered research assistant.

---

# 🌟 What Makes This Project Stand Out

Unlike generic lead systems, SimplifIQ includes:

✅ ChatGPT-style AI workflow visualization  
✅ Real-time animated AI processing pipeline  
✅ Website Health Audit & scoring  
✅ Competitor Intelligence engine  
✅ Research Confidence scoring  
✅ Smart company logo detection  
✅ AI-generated recommendations  
✅ Personalized outreach generation  
✅ Consulting-style report generation  
✅ Premium AI SaaS user experience  

---

# 🎥 Demo Workflow

```text
Landing Page
    ↓
Lead Submission
    ↓
AI Workflow Animation
    ↓
Research Company
    ↓
Website Health Audit
    ↓
Competitor Intelligence
    ↓
Confidence Analysis
    ↓
Generate Report
    ↓
Generate PDF
    ↓
Personalized Email
```

### Frontend

http://localhost:5173

### Backend API Docs

http://localhost:8000/docs

### Live Demo

Coming Soon

### Video Walkthrough

Coming Soon

---

# 📸 Screenshots

## Landing Page

Add screenshot:

```text
assets/home.png
```

## Lead Submission

Add screenshot:

```text
assets/form.png
```

## AI Workflow Visualization

Add screenshot:

```text
assets/workflow.png
```

## Website Audit + Competitor Intelligence

Add screenshot:

```text
assets/report.png
```

---

# 🏗️ System Architecture

```text
Frontend (React + Vite)
          ↓
      REST APIs
          ↓
Backend (FastAPI)
          ↓
Workflow Orchestrator
          ↓
AI Agent Layer

 ├── Research Agent
 ├── Insight Agent
 ├── Competitor Agent
 ├── Audit Agent
 ├── Report Agent
 └── Email Agent

          ↓

External Services

 ├── Gemini API
 ├── Tavily Search
 ├── SendGrid
 └── PostgreSQL
```

---

# 🔄 End-to-End Workflow

```text
User submits lead form
            ↓
Validate inputs
            ↓
Store lead data
            ↓
Trigger workflow
            ↓

Research Agent

- Search company
- Scrape website
- Collect public data
- Gather company context

            ↓

Insight Agent

- Analyze strengths
- Identify opportunities
- Detect pain points
- Generate recommendations

            ↓

Competitor Agent

- Identify competitors
- Compare positioning
- Analyze similarities

            ↓

Audit Agent

- HTTPS checks
- SEO checks
- Meta tag analysis
- Broken link detection

            ↓

Generate Confidence Score

            ↓

Generate Report

            ↓

Generate PDF

            ↓

Draft Personalized Email

            ↓

Send Email

            ↓

Update Dashboard
```

---

# 🤖 AI Multi-Agent Workflow

SimplifIQ uses a modular AI workflow architecture.

### Research Agent

Responsible for:

- Company research
- Website scraping
- Business overview
- News collection

### Insight Agent

Responsible for:

- Opportunity generation
- Pain point detection
- Strength analysis
- AI recommendations

### Competitor Agent

Responsible for:

- Competitor identification
- Feature comparison
- Market positioning

### Audit Agent

Responsible for:

- Website scoring
- SEO checks
- HTTPS validation
- Website analysis

### Report Agent

Responsible for:

- HTML report creation
- PDF generation

### Email Agent

Responsible for:

- Personalized outreach
- Email drafting
- Email delivery

---

# 🛠️ Tech Stack

## Frontend

- React
- Vite
- Tailwind CSS
- Framer Motion
- React Query
- Axios
- React Router
- Lucide React

## Backend

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

## AI & Research

- Gemini API
- LangGraph
- LangChain
- Tavily Search
- BeautifulSoup

## Services

- SendGrid
- WeasyPrint

## Deployment

Frontend → Vercel  
Backend → Render  
Database → PostgreSQL  

---

# ✨ Core Features

## Intelligent Lead Capture

- Real-time validation
- Email verification
- Website verification
- Error handling

## AI Workflow Visualization

Displays:

```text
✓ Lead Captured
✓ Validating Information
✓ Researching Company
✓ Scraping Website
✓ Finding Competitors
✓ Generating AI Insights
✓ Creating Report
✓ Generating PDF
✓ Sending Email
```

## Website Health Audit

Provides:

- HTTPS validation
- SEO score
- Meta description analysis
- Broken links detection
- Mobile responsiveness
- Website health score

## Competitor Intelligence

Provides:

- Competitor discovery
- Feature comparisons
- Market positioning
- Strategic insights

## Research Confidence Engine

Provides:

- Confidence score
- Source verification
- Reliability metrics

## Report Analytics

Displays:

- Sources analyzed
- Insights generated
- Confidence score
- Generation time

---

# 📁 Project Structure

```text
simplif-iq/

frontend/
├── src/
│   ├── pages/
│   │   ├── LandingPage.jsx
│   │   ├── LeadSubmissionPage.jsx
│   │   ├── WorkflowStatusPage.jsx
│   │   └── AdminDashboard.jsx
│   │
│   ├── components/
│   │   ├── EnhancedWorkflowSteps.jsx
│   │   ├── CompanyPreview.jsx
│   │   ├── WebsiteHealthAudit.jsx
│   │   ├── CompetitorIntelligence.jsx
│   │   ├── ResearchConfidence.jsx
│   │   └── ReportMetadata.jsx
│   │
│   └── services/

backend/
├── app/
│   ├── routes/
│   ├── agents/
│   ├── workflows/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── main.py
├── config.py
└── database.py

README.md
```

---

# 🧠 Engineering Challenges & Solutions

### Problem

AI workflows often feel slow and users assume the system froze.

### Solution

Built an animated workflow engine that visualizes AI thinking and progression.

---

### Problem

Company information can be incomplete.

### Solution

Added confidence scoring and fallback logic.

---

### Problem

Traditional lead systems provide very little business intelligence.

### Solution

Added website audits and competitor intelligence.

---

# 🚀 Installation Guide

## Clone Repository

```bash
git clone <your-repository-url>

cd simplif-iq
```

## Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```bash
.env
```

Add:

```env
DATABASE_URL=your_database_url

GEMINI_API_KEY=your_api_key

TAVILY_API_KEY=your_api_key

SENDGRID_API_KEY=your_api_key
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

Backend:

```bash
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend:

```bash
http://localhost:5173
```

---

# 🔮 Future Improvements

- AI voice summaries
- CRM integrations
- Google Drive support
- Live web crawling
- Multi-tenant architecture
- Advanced analytics dashboard

---

# 👩‍💻 Author

### Kriti Saraf

Built with ❤️ using AI + Full Stack Engineering