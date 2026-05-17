import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { leadService } from '../services/api'
import { AlertCircle, CheckCircle2 } from 'lucide-react'

export default function LeadSubmissionPage() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    website: '',
    industry: '',
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const mutation = useMutation({
    mutationFn: (data) => leadService.submitLead(data),
    onSuccess: (response) => {
      setSuccess('Lead submitted successfully!')
      setTimeout(() => {
        // pass form data to the status page so UI can render immediately
        navigate(`/status/${response.data.id}`, { state: { formData } })
      }, 1500)
    },
    onError: (error) => {
      setError(error.response?.data?.detail || 'Failed to submit lead')
    },
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    // Validation
    if (!formData.name || !formData.email || !formData.company || !formData.website) {
      setError('Please fill in all required fields')
      return
    }

    mutation.mutate(formData)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-700">
        <button
          onClick={() => navigate('/')}
          className="text-primary font-semibold hover:text-blue-400 transition"
        >
          ← Back to Home
        </button>
      </div>

      {/* Form Container */}
      <div className="max-w-2xl mx-auto px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl font-bold text-white mb-2">Analyze Your Lead</h1>
          <p className="text-slate-400 mb-8">Submit company information for instant AI-powered analysis</p>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name Field */}
            <div>
              <label className="block text-white font-medium mb-2">Your Name *</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="John Doe"
                className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
              />
            </div>

            {/* Email Field */}
            <div>
              <label className="block text-white font-medium mb-2">Email Address *</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="john@example.com"
                className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
              />
            </div>

            {/* Company Field */}
            <div>
              <label className="block text-white font-medium mb-2">Company Name *</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="TechCorp Inc"
                className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
              />
            </div>

            {/* Website Field */}
            <div>
              <label className="block text-white font-medium mb-2">Website URL *</label>
              <input
                type="text"
                name="website"
                value={formData.website}
                onChange={handleChange}
                placeholder="https://techcorp.com"
                className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
              />
            </div>

            {/* Industry Field */}
            <div>
              <label className="block text-white font-medium mb-2">Industry (Optional)</label>
              <input
                type="text"
                name="industry"
                value={formData.industry}
                onChange={handleChange}
                placeholder="SaaS, E-commerce, etc."
                className="w-full px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white placeholder-slate-500 focus:border-primary focus:outline-none transition"
              />
            </div>

            {/* Error Alert */}
            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="p-4 rounded-lg bg-red-900/20 border border-red-600/30 text-red-300 flex items-start gap-3"
              >
                <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <span>{error}</span>
              </motion.div>
            )}

            {/* Success Alert */}
            {success && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="p-4 rounded-lg bg-green-900/20 border border-green-600/30 text-green-300 flex items-start gap-3"
              >
                <CheckCircle2 className="w-5 h-5 mt-0.5 flex-shrink-0" />
                <span>{success}</span>
              </motion.div>
            )}

            {/* Submit Button */}
            <motion.button
              type="submit"
              disabled={mutation.isPending}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full py-3 bg-gradient-primary text-white rounded-lg font-semibold hover:shadow-lg hover:shadow-primary/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {mutation.isPending ? 'Submitting...' : 'Submit for Analysis'}
            </motion.button>
          </form>

          {/* Info Box */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-8 p-6 rounded-lg bg-slate-800 border border-slate-700"
          >
            <h3 className="text-white font-semibold mb-4">What Happens Next?</h3>
            <ul className="space-y-2 text-slate-300">
              <li>✓ We'll research your company across multiple sources</li>
              <li>✓ Our AI will analyze strengths, opportunities, and competitors</li>
              <li>✓ A professional report will be generated automatically</li>
              <li>✓ You'll receive a personalized email with insights</li>
            </ul>
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}
