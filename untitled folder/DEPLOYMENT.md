# Deployment Guide for SimplifIQ

## Quick Deployment Checklist

### Pre-Deployment
- [ ] All environment variables configured
- [ ] Database migrations completed
- [ ] API keys verified (OpenAI, Tavily, SendGrid)
- [ ] Frontend build passes without errors
- [ ] Backend tests passing
- [ ] .env files not committed to git

### Backend Deployment (Render)

#### Step 1: Prepare Repository
```bash
# Remove .env from git history if accidentally committed
git rm --cached .env
git commit -m "Remove env file"

# Add .env to .gitignore
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Update gitignore"
```

#### Step 2: Create Render Service
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Configure service:
   - **Name**: simplif-iq-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

#### Step 3: Configure Environment Variables
In Render dashboard, add:
```
DATABASE_URL=postgresql://user:password@host:5432/simplif_iq
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
SENDGRID_API_KEY=SG....
FROM_EMAIL=noreply@simplif-iq.com
ENVIRONMENT=production

# Optional — Google bonus integrations
GOOGLE_SERVICE_ACCOUNT_FILE=/etc/secrets/service_account.json
GOOGLE_SHEETS_SPREADSHEET_ID=...
GOOGLE_DRIVE_FOLDER_ID=...
```

#### Step 4: Deploy
- Push to GitHub
- Render auto-deploys
- Check deployment logs
- Verify health endpoint: `https://api.simplif-iq.onrender.com/health`

### Database Setup (Render PostgreSQL)

#### Option 1: Render PostgreSQL
1. In Render, create new PostgreSQL database
2. Copy connection string
3. Set as DATABASE_URL

#### Option 2: Managed Database (Railway/Supabase)
1. Create PostgreSQL instance
2. Get connection string
3. Update DATABASE_URL

### Frontend Deployment (Vercel)

#### Step 1: Build Optimization
```bash
cd frontend
npm run build
# Check build size is reasonable
```

#### Step 2: Create Vercel Project
1. Go to [vercel.com](https://vercel.com)
2. Import GitHub repository
3. Select `frontend` as root directory

#### Step 3: Configure Environment
```
VITE_API_BASE_URL=https://api.simplif-iq.onrender.com
```

#### Step 4: Deploy
- Vercel auto-deploys on git push
- Verify deployment
- Check frontend connects to backend

### Post-Deployment Verification

```bash
# Test backend health
curl https://api.simplif-iq.onrender.com/health

# Test frontend loads
# Visit https://simplif-iq.vercel.app

# Test lead submission
curl -X POST https://api.simplif-iq.onrender.com/api/leads/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "company": "Test Company",
    "website": "https://example.com",
    "industry": "Tech"
  }'
```

### Monitoring & Maintenance

#### Logs
- **Backend**: View in Render dashboard
- **Frontend**: Check Vercel analytics

#### Performance
- Monitor database connections
- Check API response times
- Track PDF generation times

#### Scaling
- If high volume: upgrade Render plan
- Add caching layer (Redis)
- Implement rate limiting

### Troubleshooting

#### Database Connection Issues
```bash
# Check connection string format
# postgresql://user:password@host:port/database

# Test connection locally first
psql postgresql://user:password@host:port/database
```

#### API Timeouts
- Increase Render web service timeout
- Optimize database queries
- Add request caching

#### Email Not Sending
- Verify SendGrid API key
- Check email formatting
- Monitor SendGrid dashboard
- Test with SendGrid API directly

#### PDF Generation Issues
- Check WeasyPrint dependencies
- Verify HTML template formatting
- Monitor file size
- Check disk space on server

### SSL/TLS Certificate

Both Render and Vercel provide free SSL certificates automatically.

### Custom Domain

#### Frontend (Vercel)
1. Buy domain from registrar
2. Add domain in Vercel project settings
3. Update nameservers

#### Backend (Render)
1. Add custom domain in Render
2. Update CORS settings for new domain

### Backup & Recovery

#### Database Backups
```bash
# Manual backup
pg_dump $DATABASE_URL > backup.sql

# Automated backups
# Enable in PostgreSQL provider dashboard
```

#### Report Recovery
- Store PDFs in S3 or Google Drive (bonus feature)
- Keep local backup of PDFs
- Database stores references

### Cost Estimation

**Monthly Costs (Approximate)**
- Render Web Service (Starter): $7/month
- PostgreSQL (Standard): $15/month
- Vercel (Hobby): $0/month
- SendGrid (Free tier): $0/month (up to 100 emails)
- OpenAI API: Pay-as-you-go (~$0.50-5/month at light volume on gpt-3.5-turbo)
- Tavily API: Pay-as-you-go (~$0.50-5/month)

**Total: ~$22-30/month for startup**

---

## Development to Production Workflow

1. **Development**
   - Local: `npm run dev` & `uvicorn app.main:app --reload`
   - Test features locally
   - Commit to feature branch

2. **Staging**
   - Push to staging branch
   - Deploy to staging environment
   - Full testing

3. **Production**
   - Merge to main
   - Auto-deploy to Vercel & Render
   - Monitor logs
   - Rollback if needed (git revert)

---

**Deployment Guide v1.0**
Last Updated: January 2024
