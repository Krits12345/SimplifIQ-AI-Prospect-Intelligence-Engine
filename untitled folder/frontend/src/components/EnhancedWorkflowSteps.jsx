import React from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Loader } from 'lucide-react'

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

export default function EnhancedWorkflowSteps({ currentStep, completedSteps, progress }) {
  return (
    <div className="space-y-4">
      {/* Progress Bar with Label */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-3">
          <span className="text-white font-semibold text-lg">Analysis Progress</span>
          <motion.span
            className="text-primary font-bold text-2xl"
            key={Math.round(progress)}
            initial={{ scale: 1.2, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {Math.round(progress)}%
          </motion.span>
        </div>
        <div className="w-full h-3 bg-gradient-to-r from-slate-700 to-slate-600 rounded-full overflow-hidden shadow-inner">
          <motion.div
            className="h-full gradient-primary relative overflow-hidden"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          >
            {/* Shimmer effect on progress bar */}
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
              animate={{ x: ['0%', '100%'] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: 'linear' }}
            />
          </motion.div>
        </div>
      </div>

      {/* Workflow Steps - ChatGPT Style */}
      <div className="space-y-3">
        {WORKFLOW_STEPS.map((step, index) => {
          const isCompleted = index < completedSteps.length
          const isCurrent = index === currentStep

          return (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className={`flex items-center gap-4 p-5 rounded-xl transition-all duration-300 backdrop-blur-sm ${
                isCompleted
                  ? 'bg-gradient-to-r from-emerald-900/40 to-emerald-800/20 border border-emerald-500/40 shadow-lg shadow-emerald-500/10'
                  : isCurrent
                  ? 'bg-gradient-to-r from-blue-900/40 to-cyan-900/20 border border-primary/40 shadow-lg shadow-primary/20'
                  : 'bg-slate-800/50 border border-slate-700/50 hover:bg-slate-800/70 hover:border-slate-600/50'
              }`}
            >
              {/* Icon Container */}
              <div className="flex-shrink-0 relative">
                {isCompleted ? (
                  <motion.div
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                    className="w-10 h-10 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-500/50"
                  >
                    <CheckCircle2 className="w-6 h-6 text-white" />
                  </motion.div>
                ) : isCurrent ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    className="w-10 h-10 rounded-full border-3 border-primary border-t-transparent shadow-lg shadow-primary/50"
                  >
                    <motion.div
                      className="w-full h-full rounded-full flex items-center justify-center"
                      animate={{ boxShadow: ['0 0 10px rgba(0, 102, 204, 0.5)', '0 0 20px rgba(0, 102, 204, 0.8)', '0 0 10px rgba(0, 102, 204, 0.5)'] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  </motion.div>
                ) : (
                  <div className="w-10 h-10 rounded-full bg-slate-700/60 border border-slate-600 flex items-center justify-center">
                    <span className="text-slate-400 text-sm font-semibold">{index + 1}</span>
                  </div>
                )}
              </div>

              {/* Label */}
              <div className="flex-grow">
                <motion.p
                  className={`font-medium ${
                    isCompleted
                      ? 'text-emerald-100'
                      : isCurrent
                      ? 'text-blue-100'
                      : 'text-slate-300'
                  }`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.08 }}
                >
                  {step.label}
                </motion.p>
              </div>

              {/* Status Indicator */}
              {isCurrent && (
                <motion.span
                  initial={{ opacity: 0, x: 10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="text-xs font-bold text-primary bg-primary/10 px-3 py-1 rounded-full border border-primary/30"
                >
                  Processing
                </motion.span>
              )}
            </motion.div>
          )
        })}
      </div>

      {/* Completion Message */}
      {progress === 100 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 20 }}
          className="mt-8 p-6 rounded-xl bg-gradient-to-r from-emerald-900/50 to-teal-900/50 border border-emerald-500/50 text-center shadow-xl"
        >
          <motion.p
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="text-emerald-100 font-semibold text-lg"
          >
            ✓ Analysis Complete
          </motion.p>
          <p className="text-emerald-200/70 text-sm mt-2">Your report is ready to view</p>
        </motion.div>
      )}
    </div>
  )
}
