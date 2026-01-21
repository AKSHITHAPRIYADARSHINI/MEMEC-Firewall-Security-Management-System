import { useState } from 'react'
import { useWebSocket } from '../../context/WebSocketContext'
import { Plus, Trash2, Edit, Toggle2 } from 'lucide-react'

export default function FirewallRules() {
  const { rules, addRule, updateRule, deleteRule, toggleRule } = useWebSocket()
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    sourceIP: '',
    destIP: '',
    port: '',
    protocol: 'TCP',
    action: 'ALLOW'
  })

  const handleSubmit = (e) => {
    e.preventDefault()

    if (editingId) {
      updateRule({ id: editingId, ...formData })
      setEditingId(null)
    } else {
      addRule(formData)
    }

    setFormData({
      name: '',
      sourceIP: '',
      destIP: '',
      port: '',
      protocol: 'TCP',
      action: 'ALLOW'
    })
    setShowAddForm(false)
  }

  const handleEdit = (rule) => {
    setFormData({
      name: rule.name,
      sourceIP: rule.sourceIP,
      destIP: rule.destIP,
      port: rule.port,
      protocol: rule.protocol,
      action: rule.action
    })
    setEditingId(rule.id)
    setShowAddForm(true)
  }

  const handleCancel = () => {
    setFormData({
      name: '',
      sourceIP: '',
      destIP: '',
      port: '',
      protocol: 'TCP',
      action: 'ALLOW'
    })
    setEditingId(null)
    setShowAddForm(false)
  }

  const getActionColor = (action) => {
    switch (action) {
      case 'ALLOW':
        return 'text-green-400 bg-green-900'
      case 'BLOCK':
      case 'DROP':
        return 'text-red-400 bg-red-900'
      case 'LOG':
        return 'text-yellow-400 bg-yellow-900'
      default:
        return 'text-slate-400 bg-slate-900'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header with Add Button */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Firewall Rules</h1>
          <p className="text-slate-400 mt-1">Manage firewall security policies ({rules.length} total)</p>
        </div>

        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg flex items-center gap-2 transition-colors"
        >
          <Plus className="w-4 h-4" />
          Add Rule
        </button>
      </div>

      {/* Add/Edit Form */}
      {showAddForm && (
        <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
          <h2 className="text-lg font-bold text-white mb-4">
            {editingId ? 'Edit Rule' : 'Add New Rule'}
          </h2>

          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Rule Name</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Source IP</label>
              <input
                type="text"
                value={formData.sourceIP}
                onChange={(e) => setFormData({ ...formData, sourceIP: e.target.value })}
                placeholder="192.168.1.0/24"
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Destination IP</label>
              <input
                type="text"
                value={formData.destIP}
                onChange={(e) => setFormData({ ...formData, destIP: e.target.value })}
                placeholder="10.0.0.0/8"
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Port</label>
              <input
                type="text"
                value={formData.port}
                onChange={(e) => setFormData({ ...formData, port: e.target.value })}
                placeholder="443, 80, 22-25"
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Protocol</label>
              <select
                value={formData.protocol}
                onChange={(e) => setFormData({ ...formData, protocol: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
              >
                <option>TCP</option>
                <option>UDP</option>
                <option>ICMP</option>
                <option>ANY</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-200 mb-2">Action</label>
              <select
                value={formData.action}
                onChange={(e) => setFormData({ ...formData, action: e.target.value })}
                className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
              >
                <option>ALLOW</option>
                <option>BLOCK</option>
                <option>LOG</option>
              </select>
            </div>

            <div className="md:col-span-2 flex gap-2">
              <button
                type="submit"
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg"
              >
                {editingId ? 'Update Rule' : 'Add Rule'}
              </button>
              <button
                type="button"
                onClick={handleCancel}
                className="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Rules Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-700 border-b border-slate-600">
              <tr>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Priority</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Rule Name</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Source IP</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Dest IP</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Port</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Protocol</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Action</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Hits</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Status</th>
                <th className="px-6 py-3 text-left font-semibold text-slate-200">Actions</th>
              </tr>
            </thead>
            <tbody>
              {rules.map((rule) => (
                <tr key={rule.id} className="border-b border-slate-700 hover:bg-slate-700 transition-colors">
                  <td className="px-6 py-3 text-slate-300">{rule.priority}</td>
                  <td className="px-6 py-3 text-white font-semibold">{rule.name}</td>
                  <td className="px-6 py-3 text-slate-300 font-mono text-xs">{rule.sourceIP}</td>
                  <td className="px-6 py-3 text-slate-300 font-mono text-xs">{rule.destIP}</td>
                  <td className="px-6 py-3 text-slate-300">{rule.port}</td>
                  <td className="px-6 py-3 text-slate-300">{rule.protocol}</td>
                  <td className="px-6 py-3">
                    <span className={`px-2 py-1 rounded text-xs font-semibold ${getActionColor(rule.action)}`}>
                      {rule.action}
                    </span>
                  </td>
                  <td className="px-6 py-3 text-slate-300">{rule.hits}</td>
                  <td className="px-6 py-3">
                    <span className={`px-2 py-1 rounded text-xs ${
                      rule.enabled ? 'bg-green-900 text-green-200' : 'bg-slate-700 text-slate-400'
                    }`}>
                      {rule.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </td>
                  <td className="px-6 py-3 flex gap-2">
                    <button
                      onClick={() => toggleRule(rule.id)}
                      className="p-2 hover:bg-slate-600 rounded transition-colors text-slate-400 hover:text-white"
                      title={rule.enabled ? 'Disable' : 'Enable'}
                    >
                      <Toggle2 className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleEdit(rule)}
                      className="p-2 hover:bg-blue-600 rounded transition-colors text-blue-400 hover:text-white"
                      title="Edit"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => deleteRule(rule.id)}
                      className="p-2 hover:bg-red-600 rounded transition-colors text-red-400 hover:text-white"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
