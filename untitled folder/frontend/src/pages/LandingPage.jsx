import React from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Brain, BarChart3, Globe, Zap, Users } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function LandingPage() {
  const navigate = useNavigate()

  const features = [
    {
      icon: Brain,
      title: 'AI Research Agent',
      description: 'Autonomous AI agents research companies 24/7'
    },
    {
      icon: BarChart3,
      title: 'Company Intelligence',
      description: 'Deep insights into business model and market position'
    },
    {
      icon: Users,
      title: 'Competitor Analysis',
      description: 'Identify and analyze key competitors automatically'
    },
    {
      icon: Globe,
      title: 'Website Health Audit',
      description: 'Comprehensive website analysis and recommendations'
    },
    {
      icon: Zap,
      title: 'Personalized Outreach',
      description: 'AI-generated insights and personalized communication'
    },
    {
      icon: CheckCircle2,
      title: 'Automated Reports',
      description: 'Professional consulting-style reports generated instantly'
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Navigation */}
      <nav className="px-6 py-4 flex justify-between items-center backdrop-blur-sm border-b border-slate-700">
        <div className="text-2xl font-bold text-primary">SimplifIQ</div>
        <button
          onClick={() => navigate('/admin')}
          className="px-4 py-2 text-slate-300 hover:text-white transition"
        >
          Admin
        </button>
      </nav>

      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="px-6 py-20 text-center"
      >
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight"
        >
          AI-Powered Prospect Intelligence
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.8 }}
          className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto"
        >
          Turn raw leads into personalized company intelligence reports instantly.
          Experience enterprise-grade AI research and analysis.
        </motion.p>

        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          onClick={() => navigate('/submit')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="px-8 py-4 bg-primary text-white rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
        >
          Analyze Company Now
        </motion.button>
      </motion.section>

      {/* Features Section */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-white mb-4">Powerful Features</h2>
          <p className="text-slate-300">Enterprise intelligence powered by cutting-edge AI</p>
        </motion.div>

        <motion.div
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid md:grid-cols-3 gap-8"
        >
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <motion.div
                key={index}
                variants={itemVariants}
                className="p-6 rounded-xl bg-slate-800 border border-slate-700 hover:border-primary transition-all duration-300 hover:shadow-lg hover:shadow-primary/20"
              >
                <Icon className="w-12 h-12 text-primary mb-4" />
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-slate-400">{feature.description}</p>
              </motion.div>
            )
          })}
        </motion.div>
      </section>

      {/* How It Works */}
      <section className="px-6 py-20 max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-white mb-4">How It Works</h2>
        </motion.div>

        <div className="grid md:grid-cols-4 gap-6">
          {[
            { num: '1', title: 'Submit', desc: 'Enter lead info' },
            { num: '2', title: 'Research', desc: 'AI analyzes company' },
            { num: '3', title: 'Generate', desc: 'Create insights' },
            { num: '4', title: 'Deliver', desc: 'Send report' },
          ].map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-primary flex items-center justify-center">
                <span className="text-2xl font-bold text-white">{step.num}</span>
              </div>
              <h3 className="font-semibold text-white mb-2">{step.title}</h3>
              <p className="text-slate-400 text-sm">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        className="px-6 py-20 max-w-4xl mx-auto text-center mb-20"
      >
        <div className="p-12 rounded-2xl gradient-primary">
          <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
          <p className="text-blue-100 mb-8">Transform your lead pipeline with AI-powered intelligence</p>
          <motion.button
            onClick={() => navigate('/submit')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-8 py-4 bg-white text-primary rounded-lg font-semibold hover:bg-slate-100 transition-all"
          >
            Start Analyzing →
          </motion.button>
        </div>
      </motion.section>

      {/* Footer */}
      <footer className="border-t border-slate-700 px-6 py-12 text-center text-slate-400">
        <p>&copy; 2024 SimplifIQ AI Prospect Intelligence. All rights reserved.</p>
      </footer>
    </div>
  )
}
