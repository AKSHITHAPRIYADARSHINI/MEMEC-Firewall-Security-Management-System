import { BarChart3, Shield, AlertCircle, Network, Zap } from 'lucide-react'

const menuItems = [
  {
    id: 'dashboard',
    label: 'Real-time Events',
    icon: Zap,
    color: 'text-blue-400'
  },
  {
    id: 'rules',
    label: 'Firewall Rules',
    icon: Shield,
    color: 'text-green-400'
  },
  {
    id: 'analytics',
    label: 'Traffic Analytics',
    icon: BarChart3,
    color: 'text-purple-400'
  },
  {
    id: 'alerts',
    label: 'Alerts & Incidents',
    icon: AlertCircle,
    color: 'text-red-400'
  }
]

export default function Sidebar({ currentPage, onPageChange, open }) {
  return (
    <aside className={`${open ? 'w-64' : 'w-20'} bg-slate-800 border-r border-slate-700 flex flex-col transition-all duration-300 overflow-hidden`}>
      {/* Logo */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
            <Shield className="w-6 h-6 text-white" />
          </div>
          {open && (
            <div>
              <h2 className="text-white font-bold text-lg">MEMEC</h2>
              <p className="text-slate-400 text-xs">Firewall SOC</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.id

          return (
            <button
              key={item.id}
              onClick={() => onPageChange(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:bg-slate-700'
              }`}
              title={item.label}
            >
              <Icon className={`w-5 h-5 flex-shrink-0 ${isActive ? 'text-white' : item.color}`} />
              {open && <span className="text-sm font-medium">{item.label}</span>}
            </button>
          )
        })}
      </nav>

      {/* Status Indicator */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          {open && (
            <div className="text-xs">
              <p className="text-green-400 font-semibold">System Online</p>
              <p className="text-slate-400">All systems normal</p>
            </div>
          )}
        </div>
      </div>
    </aside>
  )
}
