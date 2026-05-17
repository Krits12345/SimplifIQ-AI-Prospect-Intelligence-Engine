import React, { useEffect, useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { useParams, useNavigate, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { leadService, reportService } from '../services/api'
import { CheckCircle2, Loader, AlertCircle, Download, ChevronDown } from 'lucide-react'
import EnhancedWorkflowSteps from '../components/EnhancedWorkflowSteps'
import CompanyPreview from '../components/CompanyPreview'
import WebsiteHealthAudit from '../components/WebsiteHealthAudit'
import CompetitorIntelligence from '../components/CompetitorIntelligence'
import ResearchConfidence from '../components/ResearchConfidence'
import ReportMetadata from '../components/ReportMetadata'

const WORKFLOW_STEPS = [
  { id: 1, label: 'Lead Captured' },
  { id: 2, label: 'Validating Information' },
  { id: 3, label: 'Researching Company' },
  { id: 4, label: 'Scraping Website' },
  { id: 5, label: 'Finding Competitors' },
  { id: 6, label: 'Generating AI Insights' },
  { id: 7, label: 'Creating Personalized Report' },
  { id: 8, label: 'Generating PDF' },
  { id: 9, label: 'Sending Email' },
  { id: 10, label: 'Completed' },
]

export default function WorkflowStatusPage() {
  const { leadId } = useParams()
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [isComplete, setIsComplete] = useState(false)
  const [expandedSections, setExpandedSections] = useState({
    audit: true,
    competitor: true,
    metadata: true,
  })

  const { data: statusData, isLoading, error } = useQuery({
    queryKey: ['leadStatus', leadId],
    queryFn: () => leadService.getLeadStatus(leadId),
    refetchInterval: 2000, // Poll every 2 seconds
  })

  const location = useLocation()
  const formData = location.state?.formData

  // simple client-side progression will run independently of backend

  const { data: reportData } = useQuery({
    queryKey: ['report', leadId],
    queryFn: () => reportService.getReport(leadId),
    enabled: isComplete,
  })
  const steps = [
    'Lead Captured',
    'Validating Information',
    'Researching Company',
    'Scraping Website',
    'Finding Competitors',
    'Generating AI Insights',
    'Creating Personalized Report',
    'Generating PDF',
    'Sending Email',
    'Completed',
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev >= steps.length - 1) {
          clearInterval(interval)
          setProgress(100)
          setIsComplete(true)
          return prev
        }

        const next = prev + 1
        setProgress(Math.round((next / (steps.length - 1)) * 100))
        return next
      })
    }, 2500)

    return () => clearInterval(interval)
  }, [])

  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }))
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
        >
          <Loader className="w-12 h-12 text-primary" />
        </motion.div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center p-6 rounded-xl bg-red-900/20 border border-red-600/30"
        >
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-white mb-2">Error Loading Status</h2>
          <p className="text-slate-400 mb-4">Failed to load lead status. Please try again.</p>
          <button
            onClick={() => navigate('/')}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 transition"
          >
            Return Home
          </button>
        </motion.div>
      </div>
    )
  }

  const completedSteps = WORKFLOW_STEPS.slice(0, currentStep)

  const CollapsibleSection = ({ title, icon: Icon, isOpen, onToggle, children, delay = 0 }) => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="rounded-xl border border-slate-700 overflow-hidden shadow-lg"
    >
      {/* Section Header */}
      <button
        onClick={onToggle}
        className="w-full px-6 py-4 bg-slate-800/50 hover:bg-slate-800 transition flex items-center justify-between group"
      >
        <div className="flex items-center gap-3">
          <Icon className="w-5 h-5 text-primary group-hover:text-blue-300 transition" />
          <span className="text-white font-semibold group-hover:text-blue-100 transition">{title}</span>
        </div>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown className="w-5 h-5 text-slate-400 group-hover:text-slate-300 transition" />
        </motion.div>
      </button>

      {/* Section Content */}
      <motion.div
        initial={false}
        animate={{ height: isOpen ? 'auto' : 0 }}
        transition={{ duration: 0.3 }}
        className="overflow-hidden bg-gradient-to-b from-slate-900/50 to-slate-800/30"
      >
        <div className="p-6">{children}</div>
      </motion.div>
    </motion.div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-700/50 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-10">
        <button
          onClick={() => navigate('/')}
          className="text-primary font-semibold hover:text-blue-300 transition flex items-center gap-1"
        >
          ← Back to Home
        </button>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          {/* Company Preview */}
          <div className="mb-12">
            <CompanyPreview website={formData?.website || statusData?.website} company={formData?.company || statusData?.company} />
          </div>

          {/* Main Workflow Section */}
          <div className="mb-12">
            <EnhancedWorkflowSteps
              currentStep={currentStep}
              completedSteps={completedSteps}
              progress={progress}
            />
          </div>

          {/* Completion State with Additional Insights */}
          {isComplete && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 20 }}
              className="space-y-12"
            >
              {/* Success Banner */}
              <motion.div
                animate={{ scale: [1, 1.02, 1] }}
                transition={{ duration: 3, repeat: Infinity }}
                className="p-8 rounded-xl bg-gradient-to-r from-emerald-900/50 via-emerald-800/40 to-teal-900/50 border border-emerald-500/50 text-center shadow-xl"
              >
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                >
                  <CheckCircle2 className="w-16 h-16 mx-auto mb-4 text-emerald-400" />
                </motion.div>
                <h2 className="text-2xl font-bold text-emerald-100 mb-2">Analysis Complete! 🎉</h2>
                <p className="text-emerald-200/80 mb-6">
                  Your personalized AI report has been generated and sent to your email
                </p>

                {reportData && (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="px-8 py-3 bg-white text-emerald-600 rounded-lg font-semibold flex items-center gap-2 mx-auto hover:bg-slate-100 transition shadow-lg"
                  >
                    <Download className="w-5 h-5" />
                    Download Report
                  </motion.button>
                )}
              </motion.div>

              {/* Research Confidence */}
              <CollapsibleSection
                title="Research Confidence"
                icon={CheckCircle2}
                isOpen={expandedSections.audit}
                onToggle={() => toggleSection('audit')}
                delay={0.1}
              >
                <ResearchConfidence />
              </CollapsibleSection>

              {/* Website Health Audit */}
              <CollapsibleSection
                title="Website Health Audit"
                icon={AlertCircle}
                isOpen={expandedSections.audit}
                onToggle={() => toggleSection('audit')}
                delay={0.2}
              >
                <WebsiteHealthAudit website={formData?.website || statusData?.website} />
              </CollapsibleSection>

              {/* Competitor Intelligence */}
              <CollapsibleSection
                title="Competitor Intelligence"
                icon={AlertCircle}
                isOpen={expandedSections.competitor}
                onToggle={() => toggleSection('competitor')}
                delay={0.3}
              >
                <CompetitorIntelligence company={formData?.company || statusData?.company} />
              </CollapsibleSection>

              {/* Report Metadata */}
              <CollapsibleSection
                title="Report Analytics"
                icon={AlertCircle}
                isOpen={expandedSections.metadata}
                onToggle={() => toggleSection('metadata')}
                delay={0.4}
              >
                <ReportMetadata />
              </CollapsibleSection>
            </motion.div>
          )}

          {/* Processing State */}
          {!isComplete && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="p-6 rounded-lg bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm"
            >
              <p className="text-slate-300 flex items-center gap-2">
                <Loader className="w-4 h-4 animate-spin text-primary" />
                Currently processing: <span className="text-primary font-semibold">{statusData?.workflow?.current_step || 'Lead Analysis'}</span>
              </p>
              <p className="text-slate-400 text-sm mt-2">
                Estimated time remaining: {statusData?.workflow?.estimated_time_remaining || '~30'} seconds
              </p>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  )
}
