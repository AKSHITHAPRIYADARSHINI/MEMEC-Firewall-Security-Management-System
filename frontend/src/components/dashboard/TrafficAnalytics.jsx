import { useWebSocket } from '../../context/WebSocketContext'
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts'

export default function TrafficAnalytics() {
  const { metrics } = useWebSocket()

  if (!metrics) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-slate-400">Loading analytics data...</p>
      </div>
    )
  }

  const protocolColors = {
    tcp: '#3b82f6',
    udp: '#10b981',
    icmp: '#f59e0b',
    other: '#8b5cf6'
  }

  const pieData = [
    { name: 'TCP', value: metrics.protocolDistribution.tcp, color: protocolColors.tcp },
    { name: 'UDP', value: metrics.protocolDistribution.udp, color: protocolColors.udp },
    { name: 'ICMP', value: metrics.protocolDistribution.icmp, color: protocolColors.icmp },
    { name: 'Other', value: metrics.protocolDistribution.other, color: protocolColors.other }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Traffic Analytics</h1>
        <p className="text-slate-400 mt-1">Real-time network traffic visualization and metrics</p>
      </div>

      {/* Traffic Over Time */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-lg font-bold text-white mb-4">Traffic Over Time (24h)</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={metrics.hours}>
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis dataKey="time" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
              labelStyle={{ color: '#e2e8f0' }}
            />
            <Legend />
            <Line type="monotone" dataKey="inbound" stroke="#3b82f6" strokeWidth={2} name="Inbound" />
            <Line type="monotone" dataKey="outbound" stroke="#10b981" strokeWidth={2} name="Outbound" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Protocol Distribution */}
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
          <h2 className="text-lg font-bold text-white mb-4">Protocol Distribution</h2>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Top Destination Ports */}
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
          <h2 className="text-lg font-bold text-white mb-4">Top Destination Ports</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={metrics.topPorts.slice(0, 8)}>
              <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
              <XAxis dataKey="port" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
                labelStyle={{ color: '#e2e8f0' }}
              />
              <Bar dataKey="traffic" fill="#f59e0b" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Source IPs */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
        <h2 className="text-lg font-bold text-white mb-4">Top Source IPs by Traffic</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart
            data={metrics.topSourceIPs.slice(0, 10)}
            layout="vertical"
            margin={{ left: 150 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
            <XAxis type="number" stroke="#94a3b8" />
            <YAxis dataKey="ip" type="category" stroke="#94a3b8" width={140} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #475569' }}
              labelStyle={{ color: '#e2e8f0' }}
            />
            <Bar dataKey="traffic" fill="#10b981" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Avg Inbound (Mbps)</p>
          <p className="text-2xl font-bold text-blue-400 mt-2">
            {(metrics.hours.reduce((sum, h) => sum + h.inbound, 0) / metrics.hours.length).toFixed(1)}
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Avg Outbound (Mbps)</p>
          <p className="text-2xl font-bold text-green-400 mt-2">
            {(metrics.hours.reduce((sum, h) => sum + h.outbound, 0) / metrics.hours.length).toFixed(1)}
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Peak Traffic</p>
          <p className="text-2xl font-bold text-orange-400 mt-2">
            {Math.max(...metrics.hours.map(h => h.inbound + h.outbound))}
          </p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <p className="text-slate-400 text-sm">Dominant Protocol</p>
          <p className="text-2xl font-bold text-purple-400 mt-2">
            {pieData.reduce((max, p) => p.value > max.value ? p : max).name}
          </p>
        </div>
      </div>
    </div>
  )
}
