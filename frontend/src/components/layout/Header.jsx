import { LogOut, Menu, Wifi, WifiOff } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { useWebSocket } from '../../context/WebSocketContext'

export default function Header({ onLogout, onMenuClick }) {
  const { user } = useAuth()
  const { connected } = useWebSocket()

  const handleLogout = () => {
    localStorage.removeItem('token')
    onLogout()
  }

  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-400 hover:text-white"
        >
          <Menu className="w-6 h-6" />
        </button>

        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-slate-400 text-sm">Real-time Firewall Security Monitoring</p>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Connection Status */}
        <div className="flex items-center gap-2 px-4 py-2 bg-slate-700 rounded-lg">
          {connected ? (
            <>
              <Wifi className="w-4 h-4 text-green-400" />
              <span className="text-sm text-green-400">Connected</span>
            </>
          ) : (
            <>
              <WifiOff className="w-4 h-4 text-red-400" />
              <span className="text-sm text-red-400">Disconnected</span>
            </>
          )}
        </div>

        {/* User Info */}
        <div className="flex items-center gap-4 pl-4 border-l border-slate-700">
          {user && (
            <div className="text-right">
              <p className="text-white font-semibold text-sm">{user.username}</p>
              <p className="text-slate-400 text-xs">{user.role}</p>
            </div>
          )}

          <button
            onClick={handleLogout}
            className="p-2 hover:bg-red-600 rounded-lg transition-colors text-slate-400 hover:text-white"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  )
}
