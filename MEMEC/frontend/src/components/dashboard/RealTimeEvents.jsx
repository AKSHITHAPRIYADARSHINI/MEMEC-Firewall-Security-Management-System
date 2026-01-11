import { useState } from 'react'
import { useWebSocket } from '../../context/WebSocketContext'
import { Search, Filter } from 'lucide-react'

export default function RealTimeEvents() {
  const { events, stats } = useWebSocket()
  const [searchTerm, setSearchTerm] = useState('')
  const [filterSeverity, setFilterSeverity] = useState('all')

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.sourceIP.includes(searchTerm) ||
                          event.destIP.includes(searchTerm) ||
                          event.ruleName.includes(searchTerm)
    const matchesSeverity = filterSeverity === 'all' || event.severity === filterSeverity
    return matchesSearch && matchesSeverity
  })

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Critical':
        return 'bg-red-900 text-red-200 border-red-700'
      case 'High':
        return 'bg-orange-900 text-orange-200 border-orange-700'
      case 'Medium':
        return 'bg-yellow-900 text-yellow-200 border-yellow-700'
      default:
        return 'bg-blue-900 text-blue-200 border-blue-700'
    }
  }

  const getActionColor = (action) => {
    switch (action) {
      case 'ALLOW':
        return 'text-green-400'
      case 'BLOCK':
      case 'DROP':
      case 'REJECT':
        return 'text-red-400'
      default:
        return 'text-slate-400'
    }
  }

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Total Events (24h)</p>
          <p className="text-3xl font-bold text-white mt-2">{stats?.totalEvents24h || 0}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Blocked Connections</p>
          <p className="text-3xl font-bold text-red-400 mt-2">{stats?.blockedConnections || 0}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Allowed Connections</p>
          <p className="text-3xl font-bold text-green-400 mt-2">{stats?.allowedConnections || 0}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Active Rules</p>
          <p className="text-3xl font-bold text-blue-400 mt-2">{stats?.activeRules || 0}</p>
        </div>
      </div>

      {/* Events Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
        <div className="p-6 border-b border-slate-700 space-y-4">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white">Real-time Firewall Events</h2>
            <span className="text-sm text-slate-400">({filteredEvents.length} events)</span>
          </div>

          {/* Filters */}
          <div className="flex gap-4 flex-wrap">
            <div className="flex-1 min-w-64">
              <div className="relative">
                <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
                <input
                  type="text"
                  placeholder="Search by IP or rule..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-slate-400" />
              <select
                value={filterSeverity}
                onChange={(e) => setFilterSeverity(e.target.value)}
                className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
              >
                <option value="all">All Severities</option>
                <option value="Critical">Critical</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-700 border-b border-slate-600">
              <tr>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Timestamp</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Source IP</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Dest IP</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Port</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Protocol</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Action</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Severity</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Rule</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.length > 0 ? (
                filteredEvents.map((event) => (
                  <tr key={event.id} className="border-b border-slate-700 hover:bg-slate-700 transition-colors">
                    <td className="px-6 py-3 text-slate-300">
                      {new Date(event.timestamp).toLocaleTimeString()}
                    </td>
                    <td className="px-6 py-3 text-slate-300 font-mono text-xs">{event.sourceIP}</td>
                    <td className="px-6 py-3 text-slate-300 font-mono text-xs">{event.destIP}</td>
                    <td className="px-6 py-3 text-slate-300">{event.destPort}</td>
                    <td className="px-6 py-3 text-slate-300">{event.protocol}</td>
                    <td className={`px-6 py-3 font-semibold ${getActionColor(event.action)}`}>
                      {event.action}
                    </td>
                    <td className="px-6 py-3">
                      <span className={`px-2 py-1 rounded text-xs border ${getSeverityColor(event.severity)}`}>
                        {event.severity}
                      </span>
                    </td>
                    <td className="px-6 py-3 text-slate-300 text-xs">{event.ruleName}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="px-6 py-8 text-center text-slate-400">
                    No events found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
