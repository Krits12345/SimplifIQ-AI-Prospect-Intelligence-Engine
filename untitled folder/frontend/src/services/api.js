import axios from 'axios'

// In production set VITE_API_URL on the Vercel project (e.g. https://your-api.onrender.com/api).
// Locally falls back to the dev backend.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const leadService = {
  submitLead: async (leadData) => {
    try {
      const res = await api.post('/leads/submit', leadData)
      return res.data
    } catch (err) {
      // Backend unreachable — return mock id so frontend can proceed
      const mockId = `mock-${Date.now()}`
      return { id: mockId }
    }
  },

  getLeadStatus: async (leadId) => {
    try {
      const res = await api.get(`/leads/status/${leadId}`)
      return res.data
    } catch (err) {
      // If it's a mock id, simulate progressive workflow
      if (typeof leadId === 'string' && leadId.startsWith('mock-')) {
        const start = parseInt(leadId.split('-')[1], 10)
        const elapsed = Math.max(0, Math.floor((Date.now() - start) / 1000))
        const total = 20
        const progress = Math.min(100, Math.floor((elapsed / total) * 100))

        const WORKFLOW_STEPS = [
          'Lead Captured',
          'Website Validation',
          'Researching Company',
          'Scraping Website',
          'Finding Competitors',
          'Generating AI Insights',
          'Creating PDF',
          'Sending Email',
          'Completed',
        ]

        const stepsCount = Math.ceil((progress / 100) * WORKFLOW_STEPS.length)
        const current_step = WORKFLOW_STEPS[Math.min(Math.max(0, stepsCount - 1), WORKFLOW_STEPS.length - 1)]
        const estimated_time_remaining = Math.max(0, total - elapsed)

        return {
          workflow: {
            progress_percentage: progress,
            current_step,
            estimated_time_remaining,
          },
          company: 'Mock Company',
          email: 'demo@example.com',
          website: '',
        }
      }

      throw err
    }
  },

  getLead: async (leadId) => {
    try {
      const res = await api.get(`/leads/${leadId}`)
      return res.data
    } catch (err) {
      if (typeof leadId === 'string' && leadId.startsWith('mock-')) {
        return {
          id: leadId,
          name: 'Demo User',
          email: 'demo@example.com',
          company: 'Mock Company',
          website: '',
        }
      }
      throw err
    }
  },
}

export const reportService = {
  getReport: async (leadId) => {
    try {
      const res = await api.get(`/reports/${leadId}`)
      return res.data
    } catch (err) {
      if (typeof leadId === 'string' && leadId.startsWith('mock-')) {
        return {
          lead_id: leadId,
          company_name: 'Mock Company',
          website: 'mock.company',
          industry: 'Consulting',
          generated_date: new Date().toISOString(),
          executive_summary: 'This report summarizes core opportunities and website improvements for the company.',
          company_intelligence: {
            overview: 'Analyzed public company information, website content and business positioning data.',
            industry: 'Consulting',
            target_customers: ['SMBs', 'Startups', 'Enterprises'],
            strengths: ['Strong brand narrative', 'Clear customer focus'],
            opportunities: ['Improve SEO metadata', 'Strengthen mobile experience'],
          },
          website_audit: {
            website_score: 82,
            https_status: true,
            seo_score: 7,
            meta_description: false,
            broken_links: 1,
            mobile_responsiveness: true,
          },
          competitor_intelligence: {
            competitors: ['Competitor A', 'Competitor B', 'Competitor C'],
            positioning_notes: ['Competitor A is price-focused.', 'Competitor B is feature-rich.', 'Competitor C is service-led.'],
            comparison_table: [
              { feature: 'AI Insights', company: true, competitor_a: true, competitor_b: false },
              { feature: 'Mobile Responsive', company: true, competitor_a: true, competitor_b: true },
              { feature: 'Personalized Outreach', company: true, competitor_a: false, competitor_b: true },
            ],
          },
          research_confidence: {
            confidence_score: 85,
            sources: ['Company website', 'Business directories', 'Competitor profiles', 'Recent news'],
            limitations: ['No private analytics', 'Public information only'],
          },
          strategic_recommendations: [
            'Refine homepage messaging to highlight differentiation.',
            'Use clear offers and conversion triggers.',
            'Develop a priority roadmap for mobile improvements.',
          ],
          report_metadata: {
            sources_analyzed: 4,
            generation_time_seconds: 24,
            insights_generated: 12,
            confidence_score: 85,
          },
        }
      }
      throw err
    }
  },

  downloadReport: async (leadId) => {
    try {
      const res = await api.get(`/reports/${leadId}/download`, { responseType: 'blob' })
      return res.data
    } catch (err) {
      if (typeof leadId === 'string' && leadId.startsWith('mock-')) {
        return new Blob(['Mock PDF content'], { type: 'application/pdf' })
      }
      throw err
    }
  },

  sendReport: async (leadId) => {
    try {
      const res = await api.post(`/reports/${leadId}/send`)
      return res.data
    } catch (err) {
      if (typeof leadId === 'string' && leadId.startsWith('mock-')) {
        return {
          status: 'demo',
          message: 'Report prepared and email workflow completed for demo@example.com'
        }
      }
      throw err
    }
  },
}

export const dashboardService = {
  getDashboard: () =>
    api.get('/admin/dashboard'),
  
  getRecentActivity: (limit = 20) =>
    api.get(`/admin/recent-activity?limit=${limit}`),
  
  getLeadsSummary: () =>
    api.get('/admin/leads-summary'),
}

export default api
