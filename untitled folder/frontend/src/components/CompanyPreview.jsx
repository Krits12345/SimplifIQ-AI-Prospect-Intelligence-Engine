import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Globe, Briefcase, Building2, Loader } from 'lucide-react'

export default function CompanyPreview({ website, company }) {
  const [companyData, setCompanyData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    // Simulate API delay
    const timeout = setTimeout(() => {
      // Try to get logo from Clearbit API
      const domain = website?.replace('https://', '').replace('http://', '').split('/')[0]
      const logoUrl = domain ? `https://logo.clearbit.com/${domain}` : null

      setCompanyData({
        name: company || 'Company',
        website: website || '',
        logo: logoUrl,
        industry: 'Technology',
        founded: 2020,
      })
      setLoading(false)
    }, 500)

    return () => clearTimeout(timeout)
  }, [website, company])

  // Get initials for fallback
  const getInitials = (name) => {
    return name
      .split(' ')
      .map((n) => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2)
  }

  if (loading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex items-center justify-center p-8"
      >
        <Loader className="w-6 h-6 text-primary animate-spin" />
      </motion.div>
    )
  }

  if (!companyData) {
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="p-6 rounded-xl bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700 shadow-xl"
    >
      <div className="flex items-start gap-6">
        {/* Logo Container */}
        <motion.div
          className="flex-shrink-0"
          whileHover={{ scale: 1.05 }}
        >
          <div className="w-24 h-24 rounded-xl bg-gradient-to-br from-slate-700 to-slate-800 border border-slate-600 flex items-center justify-center shadow-lg overflow-hidden">
            {companyData.logo ? (
              <motion.img
                src={companyData.logo}
                alt={companyData.name}
                className="w-full h-full object-cover"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                onError={(e) => {
                  e.target.style.display = 'none'
                }}
              />
            ) : (
              <div className="text-center">
                <div className="text-3xl font-bold text-primary mb-1">
                  {getInitials(companyData.name)}
                </div>
              </div>
            )}

            {/* Fallback if image fails */}
            <div
              className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-primary/30 to-primary/10 hidden"
              id={`fallback-${companyData.name}`}
            >
              <div className="text-2xl font-bold text-primary">
                {getInitials(companyData.name)}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Company Info */}
        <motion.div
          className="flex-grow space-y-3"
          initial={{ opacity: 0, x: 10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
        >
          {/* Name */}
          <div>
            <p className="text-slate-400 text-xs font-semibold uppercase tracking-wide mb-1">
              Company Name
            </p>
            <h3 className="text-2xl font-bold text-white">{companyData.name}</h3>
          </div>

          {/* Website */}
          {companyData.website && (
            <div className="flex items-center gap-2">
              <Globe className="w-4 h-4 text-primary" />
              <a
                href={`https://${companyData.website.replace('https://', '').replace('http://', '')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:text-blue-300 transition text-sm font-medium"
              >
                {companyData.website.replace('https://', '').replace('http://', '')}
              </a>
            </div>
          )}

          {/* Details Grid */}
          <div className="grid grid-cols-2 gap-4 pt-2">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.2 }}
              className="p-3 rounded-lg bg-slate-800/50 border border-slate-700"
            >
              <p className="text-slate-400 text-xs font-semibold uppercase mb-1">Industry</p>
              <div className="flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-primary" />
                <p className="text-white font-medium text-sm">{companyData.industry}</p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="p-3 rounded-lg bg-slate-800/50 border border-slate-700"
            >
              <p className="text-slate-400 text-xs font-semibold uppercase mb-1">Status</p>
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4 text-emerald-400" />
                <p className="text-white font-medium text-sm">Active</p>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}
