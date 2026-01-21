import { useState, useEffect } from 'react'
import { AuthProvider } from './context/AuthContext'
import { WebSocketProvider } from './context/WebSocketContext'
import LoginPage from './components/auth/LoginPage'
import DashboardLayout from './components/layout/DashboardLayout'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if token exists in localStorage
    const token = localStorage.getItem('token')
    if (token) {
      // Validate token with backend
      fetch('http://localhost:3001/api/validate', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(data => {
          if (data.valid) {
            setIsAuthenticated(true)
          } else {
            localStorage.removeItem('token')
          }
        })
        .catch(err => {
          console.error('Token validation failed:', err)
          localStorage.removeItem('token')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    localStorage.removeItem('token')
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          <p className="mt-4 text-slate-400">Loading Dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <AuthProvider>
      {isAuthenticated ? (
        <WebSocketProvider>
          <DashboardLayout onLogout={handleLogout} />
        </WebSocketProvider>
      ) : (
        <LoginPage onLogin={handleLogin} />
      )}
    </AuthProvider>
  )
}

export default App
