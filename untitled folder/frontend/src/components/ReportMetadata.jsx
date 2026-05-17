import React from 'react'
import { motion } from 'framer-motion'
import { Database, Clock, Zap, TrendingUp } from 'lucide-react'

export default function ReportMetadata() {
  const metadata = [
    {
      icon: Database,
      label: 'Sources Used',
      value: '12',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-900/30',
      borderColor: 'border-blue-600/40',
    },
    {
      icon: Clock,
      label: 'Generation Time',
      value: '21s',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'bg-purple-900/30',
      borderColor: 'border-purple-600/40',
    },
    {
      icon: Zap,
      label: 'Insights Generated',
      value: '24',
      color: 'from-amber-500 to-orange-500',
      bgColor: 'bg-amber-900/30',
      borderColor: 'border-amber-600/40',
    },
    {
      icon: TrendingUp,
      label: 'Confidence Score',
      value: '87%',
      color: 'from-emerald-500 to-teal-500',
      bgColor: 'bg-emerald-900/30',
      borderColor: 'border-emerald-600/40',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { opacity: 1, scale: 1 },
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-white mb-6">Report Analytics</h3>

      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {metadata.map((item, idx) => {
          const Icon = item.icon
          return (
            <motion.div
              key={item.label}
              variants={itemVariants}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
              className={`p-6 rounded-lg border transition-all cursor-default ${item.bgColor} ${item.borderColor} hover:shadow-lg hover:${item.borderColor}`}
            >
              {/* Icon and Label */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <p className="text-slate-300 text-sm font-medium">{item.label}</p>
                </div>
                <motion.div
                  className={`p-3 rounded-lg bg-gradient-to-br ${item.color} shadow-lg`}
                  animate={{ rotate: [0, 5, -5, 0] }}
                  transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                >
                  <Icon className="w-5 h-5 text-white" />
                </motion.div>
              </div>

              {/* Value */}
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="text-3xl font-bold text-white">{item.value}</div>
              </motion.div>

              {/* Accent Line */}
              <div className="mt-4 h-1 w-12 rounded-full bg-gradient-to-r from-slate-700 to-transparent" />
            </motion.div>
          )
        })}
      </motion.div>

      {/* Info Box */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="mt-6 p-4 rounded-lg bg-slate-800/50 border border-slate-700 text-slate-300 text-sm"
      >
        <p>
          <span className="font-semibold text-white">Pro Tip:</span> This report was generated using
          advanced AI analysis and multiple data sources for accuracy and comprehensiveness.
        </p>
      </motion.div>
    </div>
  )
}
