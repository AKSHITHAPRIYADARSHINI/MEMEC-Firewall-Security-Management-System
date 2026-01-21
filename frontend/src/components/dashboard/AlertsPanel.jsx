import { useState } from 'react'
import { useWebSocket } from '../../context/WebSocketContext'
import { CheckCircle, AlertTriangle, Filter, Trash2 } from 'lucide-react'

export default function AlertsPanel() {
  const { alerts, acknowledgeAlert, resolveAlert } = useWebSocket()
  const [filterSeverity, setFilterSeverity] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')

  const filteredAlerts = alerts.filter(alert => {
    const matchesSeverity = filterSeverity === 'all' || alert.severity === filterSeverity
    const matchesStatus = filterStatus === 'all' || alert.status === filterStatus
    return matchesSeverity && matchesStatus
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

  const getStatusColor = (status) => {
    switch (status) {
      case 'New':
        return 'bg-red-900 text-red-200'
      case 'Acknowledged':
        return 'bg-yellow-900 text-yellow-200'
      case 'Resolved':
        return 'bg-green-900 text-green-200'
      default:
        return 'bg-slate-700 text-slate-300'
    }
  }

  const alertStats = {
    total: alerts.length,
    critical: alerts.filter(a => a.severity === 'Critical').length,
    high: alerts.filter(a => a.severity === 'High').length,
    unresolved: alerts.filter(a => a.status !== 'Resolved').length
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Security Alerts & Incidents</h1>
        <p className="text-slate-400 mt-1">Monitor and respond to security threats in real-time</p>
      </div>

      {/* Alert Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Total Alerts</p>
          <p className="text-3xl font-bold text-blue-400 mt-2">{alertStats.total}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-red-700">
          <p className="text-slate-400 text-sm">Critical Alerts</p>
          <p className="text-3xl font-bold text-red-400 mt-2">{alertStats.critical}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-orange-700">
          <p className="text-slate-400 text-sm">High Priority</p>
          <p className="text-3xl font-bold text-orange-400 mt-2">{alertStats.high}</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-yellow-700">
          <p className="text-slate-400 text-sm">Unresolved</p>
          <p className="text-3xl font-bold text-yellow-400 mt-2">{alertStats.unresolved}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <span className="text-slate-300 font-semibold">Filter:</span>
          </div>

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

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500"
          >
            <option value="all">All Statuses</option>
            <option value="New">New</option>
            <option value="Acknowledged">Acknowledged</option>
            <option value="Resolved">Resolved</option>
          </select>
        </div>
      </div>

      {/* Alerts List */}
      <div className="space-y-3">
        {filteredAlerts.length > 0 ? (
          filteredAlerts.map((alert) => (
            <div
              key={alert.id}
              className="bg-slate-800 border border-slate-700 rounded-lg p-4 hover:border-slate-600 transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 flex-wrap">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getSeverityColor(alert.severity)}`}>
                      {alert.severity}
                    </span>
                    <h3 className="text-white font-semibold">{alert.type}</h3>
                    <span className={`px-2 py-1 rounded text-xs ${getStatusColor(alert.status)}`}>
                      {alert.status}
                    </span>
                  </div>

                  <p className="text-slate-300 mt-2">{alert.message}</p>

                  <div className="flex items-center gap-6 text-sm text-slate-400 mt-3 flex-wrap">
                    <div>
                      <span className="text-slate-500">Source IP:</span>
                      <span className="text-slate-200 ml-2 font-mono">{alert.sourceIP}</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Dest IP:</span>
                      <span className="text-slate-200 ml-2 font-mono">{alert.destIP}</span>
                    </div>
                    <div>
                      <span className="text-slate-500">Time:</span>
                      <span className="text-slate-200 ml-2">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-2 flex-shrink-0">
                  {alert.status === 'New' && (
                    <button
                      onClick={() => acknowledgeAlert(alert.id)}
                      className="px-3 py-1 bg-yellow-600 hover:bg-yellow-700 text-white rounded text-sm transition-colors"
                      title="Acknowledge Alert"
                    >
                      Acknowledge
                    </button>
                  )}

                  {alert.status !== 'Resolved' && (
                    <button
                      onClick={() => resolveAlert(alert.id)}
                      className="px-3 py-1 bg-green-600 hover:bg-green-700 text-white rounded text-sm flex items-center gap-1 transition-colors"
                      title="Resolve Alert"
                    >
                      <CheckCircle className="w-3 h-3" />
                      Resolve
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="bg-slate-800 rounded-lg border border-slate-700 p-8 text-center">
            <AlertTriangle className="w-12 h-12 text-slate-500 mx-auto mb-4" />
            <p className="text-slate-400">No alerts found with current filters</p>
          </div>
        )}
      </div>

      {/* Alert Summary */}
      {filteredAlerts.length > 0 && (
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-4">
          <p className="text-slate-300">
            Showing <span className="font-bold text-white">{filteredAlerts.length}</span> of <span className="font-bold text-white">{alerts.length}</span> alerts
          </p>
        </div>
      )}
    </div>
  )
}
