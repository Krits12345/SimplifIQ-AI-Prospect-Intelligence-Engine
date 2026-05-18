# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Option 1: Docker (Recommended for Local Development)

```bash
# 1. Clone repository
git clone <repository-url>
cd simplif-iq

# 2. Create .env file in backend
cd backend
cp .env.example .env

# 3. Update .env with your API keys
# Edit backend/.env with:
# OPENAI_API_KEY=your_key       # used by the insight / competitor / email agents
# TAVILY_API_KEY=your_key       # used for web research + competitor discovery
# SENDGRID_API_KEY=your_key     # optional — demo mode if absent
# (Optional) GOOGLE_SERVICE_ACCOUNT_FILE + GOOGLE_SHEETS_SPREADSHEET_ID + GOOGLE_DRIVE_FOLDER_ID
#           for the Sheets logger / Drive PDF archive

# 4. Start everything with Docker Compose
cd ..
docker-compose up

# 5. Access applications
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Database: localhost:5432 (via psql)
```

### Option 2: Manual Setup (Development)

#### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
cp .env.example .env
# Edit .env with API keys
pip install -r requirements.txt
bash run.sh
```

#### Frontend Setup (in new terminal)
```bash
cd frontend
npm install
npm run dev
```

### Option 3: Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Render backend deployment
- Vercel frontend deployment
- Managed database setup
- Custom domains
- SSL certificates

---

## 📝 Configuration

### Required API Keys

1. **OpenAI API** (LLM for insights / competitor analysis / email drafting)
   - Get at: https://platform.openai.com
   - Add to `OPENAI_API_KEY`
   - Without this, agents log a warning and leave AI fields empty
     (the report endpoint surfaces this honestly instead of fabricating data).

2. **Tavily API** (Web Research)
   - Get at: https://tavily.com
   - Add to `TAVILY_API_KEY`

3. **SendGrid** (Email) — optional
   - Get at: https://sendgrid.com
   - Add to `SENDGRID_API_KEY`
   - If absent the workflow runs in demo mode (PDF + Sheets + Drive still work).

### Optional — Bonus Google integrations

4. **Google Service Account** (for Sheets logging + Drive PDF archive)
   - Create at: https://console.cloud.google.com → IAM & Admin → Service Accounts
   - Download the JSON key and point `GOOGLE_SERVICE_ACCOUNT_FILE` at it
   - Share the target spreadsheet + Drive folder with the service-account email
   - Set `GOOGLE_SHEETS_SPREADSHEET_ID` and `GOOGLE_DRIVE_FOLDER_ID`

### Database Setup

**Local (Docker):**
```bash
# Already configured in docker-compose.yml
# Connection: postgresql://simplif_iq:simplif_iq_password@postgres:5432/simplif_iq
```

**Manual PostgreSQL:**
```bash
createdb simplif_iq
# Update DATABASE_URL in .env
```

---

## 🧪 Testing the System

### Test Lead Submission
```bash
curl -X POST http://localhost:8000/api/leads/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "company": "TechCorp",
    "website": "https://example.com",
    "industry": "SaaS"
  }'
```

### Check Status
```bash
curl http://localhost:8000/api/leads/status/1
```

### Access Admin Dashboard
- Visit: http://localhost:5173/admin

### View API Documentation
- Visit: http://localhost:8000/docs

---

## 🔧 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python3 --version  # Must be 3.10+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check database connection
psql $DATABASE_URL
```

### Frontend Build Fails
```bash
# Clear node modules
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database Connection Issues
```bash
# Verify database is running (Docker)
docker-compose ps

# Check DATABASE_URL format
# postgresql://user:password@host:port/database
```

### API Calls Not Working
- Check CORS settings in backend (already configured)
- Verify frontend API URL matches backend URL
- Check network tab in browser developer tools

---

## 📚 Project Walkthrough

### Start Fresh
1. Visit http://localhost:5173
2. Click "Analyze Company"
3. Fill form:
   - Name: Your Name
   - Email: your@email.com
   - Company: Company Name
   - Website: https://example.com
   - Industry: Tech
4. Submit → Watch status page
5. Dashboard shows metrics

### Key Files to Explore

**Frontend:**
- `frontend/src/pages/` - Main pages
- `frontend/src/services/api.js` - API integration

**Backend:**
- `backend/app/main.py` - Entry point
- `backend/app/workflows/lead_workflow.py` - Main logic
- `backend/app/agents/` - AI agents

**Database:**
- `backend/app/models/database.py` - Data models

---

## 🎯 Next Steps

1. **Customize**: Update colors, fonts, company name
2. **Add Features**: Implement Google Sheets sync
3. **Test Workflows**: Try different companies
4. **Deploy**: Follow DEPLOYMENT.md guide
5. **Monitor**: Check logs and metrics

---

## 📞 Need Help?

- Check README.md for architecture details
- See DEPLOYMENT.md for production setup
- Review error logs in backend terminal
- Check browser console for frontend errors

---

**Welcome to SimplifIQ! 🚀**
