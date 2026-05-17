import React from 'react'
import { motion } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { dashboardService } from '../services/api'
import { BarChart3, TrendingUp, AlertCircle, CheckCircle2 } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AdminDashboard() {
  const { data: metrics, isLoading: metricsLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => dashboardService.getDashboard(),
    refetchInterval: 5000,
  })

  const { data: summary, isLoading: summaryLoading } = useQuery({
    queryKey: ['summary'],
    queryFn: () => dashboardService.getLeadsSummary(),
    refetchInterval: 5000,
  })

  const { data: activities } = useQuery({
    queryKey: ['activities'],
    queryFn: () => dashboardService.getRecentActivity(10),
    refetchInterval: 5000,
  })

  const chartData = summary ? [
    { name: 'Total', value: summary.total },
    { name: 'Processing', value: summary.processing },
    { name: 'Completed', value: summary.completed },
    { name: 'Failed', value: summary.failed },
  ] : []

  const StatCard = ({ icon: Icon, label, value, trend }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="p-6 rounded-lg bg-slate-800 border border-slate-700 hover:border-primary transition-all"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm mb-1">{label}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {trend && <p className="text-green-400 text-sm mt-2">{trend}</p>}
        </div>
        <Icon className="w-8 h-8 text-primary opacity-50" />
      </div>
    </motion.div>
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-700">
        <h1 className="text-2xl font-bold text-white">Admin Dashboard</h1>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Metrics Grid */}
        <div className="grid md:grid-cols-4 gap-6 mb-12">
          <StatCard
            icon={CheckCircle2}
            label="Total Leads"
            value={metrics?.metrics?.total_leads || 0}
          />
          <StatCard
            icon={BarChart3}
            label="Reports Generated"
            value={metrics?.metrics?.reports_generated || 0}
          />
          <StatCard
            icon={TrendingUp}
            label="Emails Sent"
            value={metrics?.metrics?.emails_sent || 0}
          />
          <StatCard
            icon={AlertCircle}
            label="Failures"
            value={metrics?.metrics?.failures || 0}
          />
        </div>

        {/* Summary Stats */}
        {summary && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-6 rounded-lg bg-slate-800 border border-slate-700 mb-12"
          >
            <h2 className="text-xl font-bold text-white mb-4">Lead Status Summary</h2>
            <div className="grid grid-cols-4 gap-4">
              <div>
                <p className="text-slate-400 text-sm">Total Leads</p>
                <p className="text-2xl font-bold text-white">{summary.total}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">Processing</p>
                <p className="text-2xl font-bold text-blue-400">{summary.processing}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">Completed</p>
                <p className="text-2xl font-bold text-green-400">{summary.completed}</p>
              </div>
              <div>
                <p className="text-slate-400 text-sm">Completion Rate</p>
                <p className="text-2xl font-bold text-purple-400">{summary.completion_rate.toFixed(1)}%</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Chart */}
        {chartData.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="p-6 rounded-lg bg-slate-800 border border-slate-700 mb-12"
          >
            <h2 className="text-xl font-bold text-white mb-6">Lead Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1e293b',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="value" fill="#0066cc" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </motion.div>
        )}

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="p-6 rounded-lg bg-slate-800 border border-slate-700"
        >
          <h2 className="text-xl font-bold text-white mb-6">Recent Activity</h2>
          <div className="space-y-4">
            {activities?.activities?.map((activity, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center justify-between p-4 rounded-lg bg-slate-700/50 border border-slate-600"
              >
                <div>
                  <p className="text-white font-medium">{activity.company}</p>
                  <p className="text-slate-400 text-sm">{activity.name} • {activity.email}</p>
                </div>
                <div className="text-right">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    activity.status === 'completed' ? 'bg-green-900/30 text-green-300' :
                    activity.status === 'processing' ? 'bg-blue-900/30 text-blue-300' :
                    'bg-red-900/30 text-red-300'
                  }`}>
                    {activity.status}
                  </span>
                  <p className="text-slate-400 text-xs mt-1">
                    {new Date(activity.created_at).toLocaleDateString()}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
