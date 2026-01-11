import { useState } from 'react'
import Sidebar from './Sidebar'
import Header from './Header'
import RealTimeEvents from '../dashboard/RealTimeEvents'
import TrafficAnalytics from '../dashboard/TrafficAnalytics'
import FirewallRules from '../dashboard/FirewallRules'
import AlertsPanel from '../dashboard/AlertsPanel'

export default function DashboardLayout({ onLogout }) {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <RealTimeEvents />
      case 'rules':
        return <FirewallRules />
      case 'analytics':
        return <TrafficAnalytics />
      case 'alerts':
        return <AlertsPanel />
      default:
        return <RealTimeEvents />
    }
  }

  return (
    <div className="flex h-screen bg-slate-900">
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        open={sidebarOpen}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        <Header
          onLogout={onLogout}
          onMenuClick={() => setSidebarOpen(!sidebarOpen)}
        />

        <main className="flex-1 overflow-auto bg-slate-900">
          <div className="p-6">
            {renderPage()}
          </div>
        </main>
      </div>
    </div>
  )
}
