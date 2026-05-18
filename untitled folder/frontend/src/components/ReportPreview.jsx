import React from 'react'
import { motion } from 'framer-motion'
import {
  Briefcase,
  ShieldCheck,
  BarChart3,
  Sparkles,
  FileText,
  Star,
  ClipboardList,
  AlertCircle,
} from 'lucide-react'

// All arrays/scalars come from the backend "as known" — empty when the
// workflow couldn't surface them. The component renders sections defensively
// and shows an empty-state instead of crashing.
const arr = (v) => (Array.isArray(v) ? v : [])
const txt = (v, fallback = '—') => (v ?? '') === '' ? fallback : v

const EmptyState = ({ message }) => (
  <div className="rounded-2xl bg-slate-950 p-4 border border-dashed border-slate-700 text-slate-400 text-sm flex items-center gap-2">
    <AlertCircle className="w-4 h-4 text-slate-500" />
    <span>{message}</span>
  </div>
)

const ReportPreview = React.forwardRef(({ reportData }, ref) => {
  if (!reportData) return null

  const ci = reportData.company_intelligence || {}
  const audit = reportData.website_audit || {}
  const comp = reportData.competitor_intelligence || {}
  const conf = reportData.research_confidence || {}
  const meta = reportData.report_metadata || {}

  const strengths = arr(ci.strengths)
  const opportunities = arr(ci.opportunities)
  const painPoints = arr(ci.pain_points)
  const techStack = arr(ci.tech_stack)
  const competitors = arr(comp.competitors)
  const positioning = arr(comp.positioning_notes)
  const sources = arr(conf.sources)
  const limitations = arr(conf.limitations)
  const recommendations = arr(reportData.strategic_recommendations)

  return (
    <div ref={ref} className="space-y-8">
      <div className="rounded-3xl overflow-hidden shadow-2xl border border-slate-700 bg-slate-950 text-slate-100">
        <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 p-10 text-center">
          <p className="text-sm uppercase tracking-[0.25em] text-slate-400 mb-4">
            AI Prospect Intelligence Report
          </p>
          <h1 className="text-4xl font-bold tracking-tight text-white">
            {txt(reportData.company_name)}
          </h1>
          <p className="mt-4 text-slate-300 max-w-2xl mx-auto">
            A data-driven intelligence overview tailored for {txt(reportData.company_name)}{' '}
            in the {txt(reportData.industry, 'unspecified')} industry.
          </p>
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-4 text-left">
            <div className="rounded-2xl bg-slate-900/90 p-5 border border-slate-700">
              <p className="text-slate-400 text-xs uppercase tracking-[0.2em] mb-2">Company</p>
              <p className="font-semibold text-lg text-white">{txt(reportData.company_name)}</p>
            </div>
            <div className="rounded-2xl bg-slate-900/90 p-5 border border-slate-700">
              <p className="text-slate-400 text-xs uppercase tracking-[0.2em] mb-2">Website</p>
              <p className="font-semibold text-lg text-white break-words">{txt(reportData.website)}</p>
            </div>
            <div className="rounded-2xl bg-slate-900/90 p-5 border border-slate-700">
              <p className="text-slate-400 text-xs uppercase tracking-[0.2em] mb-2">Generated</p>
              <p className="font-semibold text-lg text-white">
                {reportData.generated_date
                  ? new Date(reportData.generated_date).toLocaleDateString()
                  : '—'}
              </p>
            </div>
          </div>
        </div>

        <div className="p-8 space-y-8 bg-slate-950">
          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8"
          >
            <div className="flex items-center gap-3 mb-4">
              <FileText className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold text-white">Executive Summary</h2>
            </div>
            {reportData.executive_summary ? (
              <p className="text-slate-300 leading-7">{reportData.executive_summary}</p>
            ) : (
              <EmptyState message="No summary surfaced from public sources." />
            )}
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="grid gap-6 lg:grid-cols-2"
          >
            <div className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8">
              <div className="flex items-center gap-3 mb-4">
                <Briefcase className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold text-white">Company Intelligence</h3>
              </div>
              {ci.overview ? (
                <p className="text-slate-300 mb-4">{ci.overview}</p>
              ) : (
                <EmptyState message="Overview unavailable." />
              )}
              <div className="grid gap-3 mt-4">
                <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                  <p className="text-slate-400 text-xs uppercase mb-2">Industry</p>
                  <p className="font-semibold text-white">{txt(ci.industry)}</p>
                </div>
                <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                  <p className="text-slate-400 text-xs uppercase mb-2">Tech Stack</p>
                  {techStack.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {techStack.map((t, i) => (
                        <span
                          key={`tech-${i}`}
                          className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-200"
                        >
                          {t}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-slate-500 text-sm">No technologies detected.</p>
                  )}
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                    <p className="text-slate-400 text-xs uppercase mb-2">Strengths</p>
                    {strengths.length > 0 ? (
                      <ul className="list-disc list-inside text-slate-300 space-y-2">
                        {strengths.map((item, i) => (
                          <li key={`strength-${i}`}>{item}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-slate-500 text-sm">Not surfaced.</p>
                    )}
                  </div>
                  <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                    <p className="text-slate-400 text-xs uppercase mb-2">Opportunities</p>
                    {opportunities.length > 0 ? (
                      <ul className="list-disc list-inside text-slate-300 space-y-2">
                        {opportunities.map((item, i) => (
                          <li key={`opp-${i}`}>{item}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-slate-500 text-sm">Not surfaced.</p>
                    )}
                  </div>
                </div>
                {painPoints.length > 0 && (
                  <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                    <p className="text-slate-400 text-xs uppercase mb-2">Pain Points</p>
                    <ul className="list-disc list-inside text-slate-300 space-y-2">
                      {painPoints.map((item, i) => (
                        <li key={`pain-${i}`}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8">
              <div className="flex items-center gap-3 mb-4">
                <ShieldCheck className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold text-white">Website Health Audit</h3>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl bg-slate-950 p-5 border border-slate-800">
                  <p className="text-slate-400 text-xs uppercase mb-2">Health Score</p>
                  <p className="text-3xl font-semibold text-white">
                    {audit.website_score != null ? `${Math.round(audit.website_score)}/100` : '—'}
                  </p>
                </div>
                <div className="rounded-2xl bg-slate-950 p-5 border border-slate-800">
                  <p className="text-slate-400 text-xs uppercase mb-2">Website Content</p>
                  <p className="font-semibold text-white">
                    {audit.has_website_content ? 'Retrieved' : 'Could not retrieve'}
                  </p>
                </div>
              </div>
            </div>
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8"
          >
            <div className="flex items-center gap-3 mb-4">
              <BarChart3 className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold text-white">Competitor Intelligence</h2>
            </div>
            {competitors.length > 0 ? (
              <>
                <p className="text-slate-300 mb-4">
                  Key competitors identified for benchmarking and strategic differentiation.
                </p>
                <div className="rounded-3xl bg-slate-950 p-6 border border-slate-800">
                  <div className="grid gap-4 sm:grid-cols-3">
                    {competitors.map((c, i) => (
                      <div key={`competitor-${i}`} className="rounded-2xl bg-slate-900 p-4">
                        <p className="text-slate-400 text-xs uppercase mb-2">Competitor</p>
                        <p className="font-semibold text-white">{c}</p>
                      </div>
                    ))}
                  </div>
                </div>
                {positioning.length > 0 && (
                  <div className="mt-6 space-y-3">
                    {positioning.map((note, i) => (
                      <div
                        key={`positioning-${i}`}
                        className="rounded-2xl bg-slate-950 p-4 border border-slate-800"
                      >
                        <p className="text-slate-300">{note}</p>
                      </div>
                    ))}
                  </div>
                )}
              </>
            ) : (
              <EmptyState message="No competitors identified from public sources." />
            )}
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="grid gap-6 lg:grid-cols-2"
          >
            <div className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8">
              <div className="flex items-center gap-3 mb-4">
                <Sparkles className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold text-white">Strategic Recommendations</h3>
              </div>
              {recommendations.length > 0 ? (
                <div className="space-y-4">
                  {recommendations.map((item, i) => (
                    <div
                      key={`rec-${i}`}
                      className="rounded-2xl bg-slate-950 p-4 border border-slate-800"
                    >
                      <p className="text-slate-200">{item}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState message="AI recommendations not available." />
              )}
            </div>

            <div className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8">
              <div className="flex items-center gap-3 mb-4">
                <ClipboardList className="w-5 h-5 text-primary" />
                <h3 className="text-lg font-semibold text-white">Research Confidence</h3>
              </div>
              <div className="rounded-2xl bg-slate-950 p-6 border border-slate-800">
                <p className="text-slate-400 text-sm uppercase tracking-[0.2em] mb-3">
                  Confidence Score
                </p>
                <p className="text-4xl font-semibold text-white">
                  {conf.confidence_score != null ? `${Math.round(conf.confidence_score)}%` : '—'}
                </p>
                {sources.length > 0 && (
                  <div className="mt-5 space-y-3 text-slate-300">
                    {sources.map((source, i) => (
                      <div key={`source-${i}`} className="flex items-center gap-3">
                        <span className="inline-flex h-2.5 w-2.5 rounded-full bg-primary" />
                        <span>{source}</span>
                      </div>
                    ))}
                  </div>
                )}
                {limitations.length > 0 && (
                  <div className="mt-6 text-slate-400 text-sm space-y-2">
                    {limitations.map((item, i) => (
                      <p key={`limit-${i}`}>• {item}</p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </motion.section>

          <motion.section
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="rounded-3xl bg-slate-900/80 border border-slate-800 p-8"
          >
            <div className="flex items-center gap-3 mb-4">
              <Star className="w-5 h-5 text-primary" />
              <h2 className="text-xl font-semibold text-white">Report Metadata</h2>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                <p className="text-slate-400 text-xs uppercase mb-2">Sources Analyzed</p>
                <p className="font-semibold text-white">{meta.sources_analyzed ?? '—'}</p>
              </div>
              <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                <p className="text-slate-400 text-xs uppercase mb-2">Insights Generated</p>
                <p className="font-semibold text-white">{meta.insights_generated ?? 0}</p>
              </div>
              <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                <p className="text-slate-400 text-xs uppercase mb-2">Confidence Score</p>
                <p className="font-semibold text-white">
                  {meta.confidence_score != null ? `${Math.round(meta.confidence_score)}%` : '—'}
                </p>
              </div>
              <div className="rounded-2xl bg-slate-950 p-4 border border-slate-800">
                <p className="text-slate-400 text-xs uppercase mb-2">PDF</p>
                <p className="font-semibold text-white">
                  {meta.pdf_available ? 'Available' : 'Not generated'}
                </p>
              </div>
            </div>
            {meta.drive_url && (
              <p className="mt-4 text-sm text-slate-400">
                Archived to Drive:{' '}
                <a
                  href={meta.drive_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-primary underline"
                >
                  open
                </a>
              </p>
            )}
          </motion.section>
        </div>
      </div>
    </div>
  )
})

ReportPreview.displayName = 'ReportPreview'

export default ReportPreview
