import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Globe, Newspaper, Building2, Award } from 'lucide-react'

export default function ResearchConfidence() {
  const [confidenceData, setConfidenceData] = useState(null)

  useEffect(() => {
    // Mock data - in production, this would come from backend
    setConfidenceData({
      overallConfidence: 87,
      sources: [
        { icon: Globe, label: 'Company Website', value: 'Complete' },
        { icon: Newspaper, label: 'Recent News', value: 'Found' },
        { icon: Building2, label: 'Public Directories', value: 'Verified' },
        { icon: Award, label: 'About Page', value: 'Analyzed' },
      ],
    })
  }, [])

  if (!confidenceData) {
    return <div className="text-slate-400">Loading confidence data...</div>
  }

  const confidenceColor = 
    confidenceData.overallConfidence >= 85
      ? 'from-emerald-500 to-teal-500'
      : confidenceData.overallConfidence >= 70
      ? 'from-amber-500 to-yellow-500'
      : 'from-red-500 to-pink-500'

  return (
    <div className="space-y-8">
      {/* Main Confidence Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="p-8 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 shadow-xl"
      >
        <div className="flex flex-col md:flex-row items-center gap-8">
          {/* Circular Progress */}
          <motion.div className="flex-shrink-0 relative w-40 h-40">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 160 160">
              {/* Background Circle */}
              <circle
                cx="80"
                cy="80"
                r="70"
                fill="none"
                stroke="#1e293b"
                strokeWidth="6"
              />

              {/* Progress Circle */}
              <motion.circle
                cx="80"
                cy="80"
                r="70"
                fill="none"
                strokeWidth="6"
                strokeLinecap="round"
                stroke="url(#confidenceGradient)"
                initial={{
                  strokeDasharray: `0 ${2 * Math.PI * 70}`,
                  strokeDashoffset: 0,
                }}
                animate={{
                  strokeDasharray: `${
                    (confidenceData.overallConfidence / 100) * (2 * Math.PI * 70)
                  } ${2 * Math.PI * 70}`,
                }}
                transition={{ duration: 2, ease: 'easeOut' }}
              />

              <defs>
                <linearGradient id="confidenceGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#0066cc" />
                  <stop offset="100%" stopColor="#00a86b" />
                </linearGradient>
              </defs>
            </svg>

            {/* Center Text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.3, type: 'spring', stiffness: 200 }}
              >
                <div className="text-4xl font-bold text-white">
                  {confidenceData.overallConfidence}%
                </div>
                <div className="text-xs text-slate-400 text-center mt-1">Confidence</div>
              </motion.div>
            </div>
          </motion.div>

          {/* Description */}
          <div className="flex-grow">
            <h3 className="text-2xl font-bold text-white mb-3">Research Confidence Score</h3>
            <p className="text-slate-400 mb-4">
              {confidenceData.overallConfidence >= 85
                ? 'High confidence in research findings. Data collected from multiple authoritative sources.'
                : confidenceData.overallConfidence >= 70
                ? 'Good confidence level. Data verified from primary sources.'
                : 'Moderate confidence. Additional sources recommended for complete picture.'}
            </p>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-emerald-500/10 border border-emerald-500/30">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span className="text-emerald-100 font-semibold text-sm">Reliable</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Sources Grid */}
      <div>
        <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Award className="w-5 h-5 text-primary" />
          Research Sources
        </h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {confidenceData.sources.map((source, idx) => {
            const Icon = source.icon
            return (
              <motion.div
                key={source.label}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                whileHover={{ y: -2 }}
                className="p-5 rounded-lg bg-slate-800/50 border border-slate-700 hover:border-primary/50 transition-all cursor-default group"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-grow">
                    <div className="p-2 rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors mt-1">
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <p className="text-white font-semibold text-sm">{source.label}</p>
                      <p className="text-slate-400 text-xs mt-1">{source.value}</p>
                    </div>
                  </div>
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: idx * 0.1 + 0.2, type: 'spring' }}
                  >
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  </motion.div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
