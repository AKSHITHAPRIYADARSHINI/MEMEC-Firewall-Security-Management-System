import { createContext, useContext, useEffect, useState } from 'react'
import io from 'socket.io-client'
import { useAuth } from './AuthContext'

const WebSocketContext = createContext()

export const WebSocketProvider = ({ children }) => {
  const { token } = useAuth()
  const [socket, setSocket] = useState(null)
  const [connected, setConnected] = useState(false)
  const [events, setEvents] = useState([])
  const [alerts, setAlerts] = useState([])
  const [rules, setRules] = useState([])
  const [metrics, setMetrics] = useState(null)
  const [stats, setStats] = useState(null)

  useEffect(() => {
    if (!token) return

    const newSocket = io('http://localhost:3001', {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    })

    newSocket.on('connect', () => {
      console.log('WebSocket connected')
      setConnected(true)
      newSocket.emit('authenticate', { token })
      newSocket.emit('request-initial-data')
    })

    newSocket.on('authenticated', (data) => {
      if (data.success) {
        console.log('WebSocket authenticated')
      } else {
        console.error('WebSocket authentication failed')
      }
    })

    newSocket.on('new-event', (event) => {
      setEvents(prev => [event, ...prev.slice(0, 99)])
    })

    newSocket.on('initial-events', (initialEvents) => {
      setEvents(initialEvents)
    })

    newSocket.on('new-alert', (alert) => {
      setAlerts(prev => [alert, ...prev.slice(0, 49)])
    })

    newSocket.on('initial-alerts', (initialAlerts) => {
      setAlerts(initialAlerts)
    })

    newSocket.on('rules-list', (rulesList) => {
      setRules(rulesList)
    })

    newSocket.on('initial-rules', (initialRules) => {
      setRules(initialRules)
    })

    newSocket.on('rules-updated', (updatedRules) => {
      setRules(updatedRules)
    })

    newSocket.on('traffic-metrics', (metricsData) => {
      setMetrics(metricsData)
    })

    newSocket.on('statistics', (statsData) => {
      setStats(statsData)
    })

    newSocket.on('alert-acknowledged', (alertId) => {
      setAlerts(prev => prev.map(a => a.id === alertId ? { ...a, status: 'Acknowledged' } : a))
    })

    newSocket.on('alert-resolved', (alertId) => {
      setAlerts(prev => prev.map(a => a.id === alertId ? { ...a, status: 'Resolved' } : a))
    })

    newSocket.on('disconnect', () => {
      console.log('WebSocket disconnected')
      setConnected(false)
    })

    setSocket(newSocket)

    return () => {
      newSocket.disconnect()
    }
  }, [token])

  const addRule = (ruleData) => {
    if (socket) {
      socket.emit('add-rule', ruleData)
    }
  }

  const updateRule = (ruleData) => {
    if (socket) {
      socket.emit('update-rule', ruleData)
    }
  }

  const deleteRule = (ruleId) => {
    if (socket) {
      socket.emit('delete-rule', ruleId)
    }
  }

  const toggleRule = (ruleId) => {
    if (socket) {
      socket.emit('toggle-rule', ruleId)
    }
  }

  const acknowledgeAlert = (alertId) => {
    if (socket) {
      socket.emit('acknowledge-alert', alertId)
    }
  }

  const resolveAlert = (alertId) => {
    if (socket) {
      socket.emit('resolve-alert', alertId)
    }
  }

  return (
    <WebSocketContext.Provider value={{
      socket,
      connected,
      events,
      alerts,
      rules,
      metrics,
      stats,
      addRule,
      updateRule,
      deleteRule,
      toggleRule,
      acknowledgeAlert,
      resolveAlert
    }}>
      {children}
    </WebSocketContext.Provider>
  )
}

export const useWebSocket = () => {
  const context = useContext(WebSocketContext)
  if (!context) {
    throw new Error('useWebSocket must be used within WebSocketProvider')
  }
  return context
}
