import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, AlertCircle, Lock, Smartphone, Share2, Search } from 'lucide-react'

export default function WebsiteHealthAudit({ website }) {
  const [auditData, setAuditData] = useState(null)

  useEffect(() => {
    // Mock data - in production, this would call an API
    setAuditData({
      score: 84,
      httpsEnabled: true,
      seoScore: 7,
      metaDescription: false,
      brokenLinks: 1,
      mobileResponsive: true,
      socialLinks: true,
    })
  }, [website])

  if (!auditData) {
    return <div className="text-slate-400">Loading audit...</div>
  }

  const AuditMetric = ({ icon: Icon, label, value, status, isScore }) => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2 }}
      className={`p-4 rounded-lg border transition-all cursor-default ${
        status === 'good'
          ? 'bg-emerald-900/30 border-emerald-600/40 hover:border-emerald-500/60'
          : status === 'warning'
          ? 'bg-amber-900/30 border-amber-600/40 hover:border-amber-500/60'
          : 'bg-slate-800/50 border-slate-700/50 hover:border-slate-600/50'
      }`}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg ${
            status === 'good'
              ? 'bg-emerald-500/20 text-emerald-400'
              : status === 'warning'
              ? 'bg-amber-500/20 text-amber-400'
              : 'bg-slate-700 text-slate-400'
          }`}>
            <Icon className="w-5 h-5" />
          </div>
          <div>
            <p className="text-sm text-slate-300 font-medium">{label}</p>
            {isScore ? (
              <div className="flex items-center gap-2 mt-1">
                <div className="w-24 h-2 bg-slate-700 rounded-full overflow-hidden">
                  <motion.div
                    className={`h-full ${
                      value >= 7
                        ? 'bg-gradient-to-r from-emerald-400 to-emerald-500'
                        : 'bg-gradient-to-r from-amber-400 to-amber-500'
                    }`}
                    initial={{ width: 0 }}
                    animate={{ width: `${(value / 10) * 100}%` }}
                    transition={{ duration: 1, delay: 0.2 }}
                  />
                </div>
                <span className="text-white font-bold text-sm">{value}/10</span>
              </div>
            ) : (
              <p className="text-white font-bold text-lg">{value}</p>
            )}
          </div>
        </div>
        {status === 'good' && (
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
        )}
        {status === 'warning' && (
          <AlertCircle className="w-5 h-5 text-amber-400" />
        )}
      </div>
    </motion.div>
  )

  return (
    <div className="space-y-8">
      {/* Main Score Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="p-8 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 shadow-xl"
      >
        <div className="flex items-center gap-8">
          {/* Circular Score */}
          <motion.div
            className="flex-shrink-0"
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
          >
            <svg className="w-32 h-32 transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="56"
                fill="none"
                stroke="#1e293b"
                strokeWidth="4"
              />
              <motion.circle
                cx="64"
                cy="64"
                r="56"
                fill="none"
                strokeWidth="4"
                stroke="url(#gradient)"
                strokeLinecap="round"
                initial={{ strokeDasharray: '0 352', strokeDashoffset: 0 }}
                animate={{ strokeDasharray: '264 352', strokeDashoffset: 0 }}
                transition={{ duration: 2, ease: 'easeOut' }}
                style={{
                  strokeDasharray: `${(auditData.score / 100) * 352} 352`,
                }}
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#0066cc" />
                  <stop offset="100%" stopColor="#0052a3" />
                </linearGradient>
              </defs>
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-4xl font-bold text-white">{auditData.score}</div>
                <div className="text-sm text-slate-400">/100</div>
              </div>
            </div>
          </motion.div>

          {/* Score Description */}
          <div className="flex-grow">
            <h3 className="text-2xl font-bold text-white mb-2">Website Health Score</h3>
            <p className="text-slate-400 mb-4">
              {auditData.score >= 85
                ? 'Excellent website health. Your site is optimized and performing well.'
                : auditData.score >= 70
                ? 'Good health. Some improvements recommended.'
                : 'Fair health. Consider addressing critical issues.'}
            </p>
            <div className="inline-block px-4 py-2 rounded-full bg-primary/10 border border-primary/30">
              <span className="text-primary font-semibold text-sm">
                {auditData.score >= 85
                  ? '✓ Excellent'
                  : auditData.score >= 70
                  ? '⚠ Good'
                  : '✗ Needs Work'}
              </span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Audit Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AuditMetric
          icon={Lock}
          label="HTTPS Enabled"
          value={auditData.httpsEnabled ? 'Secure' : 'Not Secure'}
          status={auditData.httpsEnabled ? 'good' : 'warning'}
        />
        <AuditMetric
          icon={Search}
          label="SEO Score"
          value={auditData.seoScore}
          status={auditData.seoScore >= 7 ? 'good' : 'warning'}
          isScore={true}
        />
        <AuditMetric
          icon={AlertCircle}
          label="Meta Description"
          value={auditData.metaDescription ? 'Present' : 'Missing'}
          status={auditData.metaDescription ? 'good' : 'warning'}
        />
        <AuditMetric
          icon={AlertCircle}
          label="Broken Links"
          value={auditData.brokenLinks}
          status={auditData.brokenLinks === 0 ? 'good' : 'warning'}
        />
        <AuditMetric
          icon={Smartphone}
          label="Mobile Responsive"
          value={auditData.mobileResponsive ? 'Yes' : 'No'}
          status={auditData.mobileResponsive ? 'good' : 'warning'}
        />
        <AuditMetric
          icon={Share2}
          label="Social Links"
          value={auditData.socialLinks ? 'Detected' : 'Missing'}
          status={auditData.socialLinks ? 'good' : 'warning'}
        />
      </div>
    </div>
  )
}
