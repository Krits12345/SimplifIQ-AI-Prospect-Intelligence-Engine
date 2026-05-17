import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import LandingPage from './pages/LandingPage'
import LeadSubmissionPage from './pages/LeadSubmissionPage'
import WorkflowStatusPage from './pages/WorkflowStatusPage'
import AdminDashboard from './pages/AdminDashboard'
import './index.css'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/submit" element={<LeadSubmissionPage />} />
          <Route path="/status/:leadId" element={<WorkflowStatusPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
