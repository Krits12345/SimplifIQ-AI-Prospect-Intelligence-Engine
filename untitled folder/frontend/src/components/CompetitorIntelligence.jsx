import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, CheckCircle2, X } from 'lucide-react'

export default function CompetitorIntelligence({ company }) {
  const [comparisonData, setComparisonData] = useState(null)

  useEffect(() => {
    // Mock data - in production, this would call an API
    setComparisonData({
      yourCompany: company || 'Notion',
      competitors: ['Confluence', 'ClickUp', 'Monday.com'],
      features: [
        { name: 'AI Support', your: true, competitors: [true, true, false] },
        { name: 'Blog Presence', your: true, competitors: [true, true, true] },
        { name: 'Knowledge Base', your: true, competitors: [true, false, true] },
        { name: 'Customer Reviews', your: true, competitors: [true, true, true] },
        { name: 'Mobile App', your: true, competitors: [true, true, true] },
        { name: 'API Available', your: true, competitors: [true, true, false] },
      ],
    })
  }, [company])

  if (!comparisonData) {
    return <div className="text-slate-400">Loading competitor data...</div>
  }

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 },
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-2xl font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-primary" />
            Competitor Intelligence
          </h3>
          <p className="text-slate-400 text-sm mt-1">Feature comparison across top competitors</p>
        </div>
      </div>

      {/* Comparison Table */}
      <motion.div
        className="rounded-xl overflow-hidden border border-slate-700 shadow-xl"
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <div className="grid grid-cols-4 bg-slate-800/80 border-b border-slate-700 backdrop-blur-sm sticky top-0">
          <div className="p-5 col-span-1">
            <p className="text-white font-bold text-sm">Features</p>
          </div>
          {[comparisonData.yourCompany, ...comparisonData.competitors].map((name, idx) => (
            <motion.div
              key={name}
              variants={itemVariants}
              className={`p-5 text-center border-l border-slate-700 ${
                idx === 0 ? 'bg-primary/10' : ''
              }`}
            >
              <p className={`font-bold text-sm ${idx === 0 ? 'text-primary' : 'text-white'}`}>
                {name}
              </p>
              {idx === 0 && (
                <span className="inline-block mt-1 px-2 py-0.5 bg-primary/20 border border-primary/30 rounded text-xs text-primary font-semibold">
                  Your Company
                </span>
              )}
            </motion.div>
          ))}
        </div>

        {/* Rows */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {comparisonData.features.map((feature, rowIdx) => (
            <motion.div
              key={feature.name}
              variants={itemVariants}
              className="grid grid-cols-4 border-b border-slate-700/50 hover:bg-slate-800/30 transition-colors last:border-b-0"
            >
              <div className="p-5 col-span-1 flex items-center">
                <p className="text-white font-medium text-sm">{feature.name}</p>
              </div>

              {/* Your Company */}
              <div className="p-5 text-center border-l border-slate-700/30 flex items-center justify-center bg-primary/5">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{
                    type: 'spring',
                    stiffness: 200,
                    damping: 15,
                    delay: rowIdx * 0.05 + 0.1,
                  }}
                >
                  {feature.your ? (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  ) : (
                    <X className="w-5 h-5 text-slate-500" />
                  )}
                </motion.div>
              </div>

              {/* Competitors */}
              {feature.competitors.map((has, compIdx) => (
                <div
                  key={compIdx}
                  className="p-5 text-center border-l border-slate-700/30 flex items-center justify-center"
                >
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{
                      type: 'spring',
                      stiffness: 200,
                      damping: 15,
                      delay: rowIdx * 0.05 + (compIdx + 1) * 0.05 + 0.1,
                    }}
                  >
                    {has ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                    ) : (
                      <X className="w-5 h-5 text-slate-500" />
                    )}
                  </motion.div>
                </div>
              ))}
            </motion.div>
          ))}
        </motion.div>
      </motion.div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span className="text-slate-300">Feature Available</span>
        </div>
        <div className="flex items-center gap-2">
          <X className="w-4 h-4 text-slate-500" />
          <span className="text-slate-300">Feature Not Available</span>
        </div>
      </div>
    </div>
  )
}
