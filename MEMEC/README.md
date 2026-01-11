# MEMEC Firewall Management Dashboard

A comprehensive SOC (Security Operations Center) Firewall Management Dashboard built with React, Tailwind CSS, and WebSocket real-time connectivity.

## Features

✅ **Real-time Event Monitoring** - Live feed of firewall events with color-coded severity levels
✅ **Firewall Rule Management** - CRUD operations for creating and managing firewall rules
✅ **Traffic Analytics** - Visual charts and metrics for network traffic analysis
✅ **Security Alerts** - Real-time security alerts and incident tracking
✅ **Authentication** - Basic JWT-based login system
✅ **WebSocket Communication** - Real-time data streaming from backend
✅ **Responsive Design** - Works on desktop and tablet devices
✅ **Dark Mode UI** - Professional dark theme with Tailwind CSS

## Technology Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Socket.io Client** - WebSocket communication
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend
- **Node.js** - Runtime
- **Express.js** - Web framework
- **Socket.io** - WebSocket server
- **JWT** - Authentication
- **CORS** - Cross-origin requests

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
MEMEC/
├── docker-compose.yml          # Docker orchestration
├── README.md                    # This file
│
├── frontend/                    # React frontend
│   ├── Dockerfile              # Frontend container
│   ├── package.json            # Dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js       # Tailwind configuration
│   ├── postcss.config.js        # PostCSS configuration
│   ├── index.html               # HTML entry point
│   └── src/
│       ├── main.jsx            # React entry point
│       ├── App.jsx              # Main app component
│       ├── index.css            # Global styles
│       ├── context/
│       │   ├── AuthContext.jsx  # Authentication state
│       │   └── WebSocketContext.jsx # WebSocket state
│       ├── components/
│       │   ├── auth/
│       │   │   └── LoginPage.jsx
│       │   ├── layout/
│       │   │   ├── DashboardLayout.jsx
│       │   │   ├── Sidebar.jsx
│       │   │   └── Header.jsx
│       │   └── dashboard/
│       │       ├── RealTimeEvents.jsx
│       │       ├── FirewallRules.jsx
│       │       ├── TrafficAnalytics.jsx
│       │       └── AlertsPanel.jsx
│       └── utils/
│
└── backend/                     # Node.js backend
    ├── Dockerfile              # Backend container
    ├── package.json            # Dependencies
    └── src/
        ├── server.js           # Express server setup
        ├── auth.js             # JWT authentication
        ├── websocket.js        # WebSocket handlers
        └── mockData.js         # Mock data generation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Installation & Running

1. **Clone the repository** (if not already done)
   ```bash
   cd MEMEC
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the frontend and backend images
   - Start both services
   - Make the frontend accessible at http://localhost:5173
   - Make the backend accessible at http://localhost:3001

3. **Access the Dashboard**
   - Open your browser and go to: **http://localhost:5173**
   - Login with credentials:
     - **Username:** `admin@soc.local`
     - **Password:** `firewall123`

4. **Stop the services**
   ```bash
   docker-compose down
   ```

## Usage Guide

### Real-time Events
- View all incoming firewall events in real-time
- Filter by severity (Critical, High, Medium, Low)
- Search by IP addresses or rule names
- View event details including source/destination IPs, ports, and protocols

### Firewall Rules
- **View Rules** - See all configured firewall rules
- **Add Rule** - Create new rules with source/destination IPs, ports, and actions
- **Edit Rule** - Modify existing rules
- **Delete Rule** - Remove unwanted rules
- **Toggle Rule** - Enable/disable rules without deleting them
- **Monitor Hits** - See how many times each rule has been triggered

### Traffic Analytics
- **Traffic Over Time** - Line chart showing inbound/outbound traffic trends
- **Protocol Distribution** - Pie chart of TCP/UDP/ICMP traffic
- **Top Source IPs** - Bar chart of most active source IPs
- **Top Ports** - Bar chart of most accessed ports
- **Key Metrics** - Summary statistics for quick insights

### Alerts & Incidents
- **Alert Feed** - Real-time security alerts with severity levels
- **Alert Types** - Brute force, port scans, DDoS, malicious IPs, etc.
- **Status Management** - Mark alerts as Acknowledged or Resolved
- **Filtering** - Filter by severity or status
- **Quick Actions** - Acknowledge or resolve alerts directly from the feed

## API Endpoints

### Authentication
- `POST /api/login` - Login with credentials
- `POST /api/validate` - Validate JWT token

### Health Check
- `GET /health` - Check backend status

## WebSocket Events

### Client → Server
- `authenticate` - Authenticate WebSocket connection
- `request-initial-data` - Get initial dashboard data
- `add-rule` - Add new firewall rule
- `update-rule` - Update existing rule
- `delete-rule` - Delete a rule
- `toggle-rule` - Enable/disable a rule
- `acknowledge-alert` - Acknowledge an alert
- `resolve-alert` - Mark alert as resolved

### Server → Client
- `authenticated` - Authentication result
- `new-event` - Real-time firewall event
- `new-alert` - Real-time security alert
- `rules-updated` - Rules list updated
- `statistics` - Updated stats
- `traffic-metrics` - Updated traffic data

## Demo Credentials

The dashboard comes with pre-configured demo credentials for testing:

```
Username: admin@soc.local
Password: firewall123
```

Note: This is for demonstration purposes only. In production, implement proper authentication mechanisms.

## Mock Data

The backend generates realistic mock data including:

- **Firewall Events** - Generated every 2-3 seconds
  - Connection attempts (allowed/blocked)
  - Port scans
  - DDoS attempts
  - Policy violations

- **Alerts** - Generated with 15% probability on new events
  - Brute force detection
  - Port scan detection
  - DDoS attack alerts
  - Malicious IP blocks

- **Firewall Rules** - Pre-populated with 25 realistic rules
  - Varying priorities
  - Different actions (ALLOW/BLOCK/LOG)
  - Real-world port combinations

- **Traffic Metrics** - Updated every 10 seconds
  - 24-hour traffic pattern
  - Protocol distribution
  - Top source IPs and ports

## Environment Variables

### Frontend (.env in frontend/)
```
VITE_API_URL=http://localhost:3001
VITE_WS_URL=ws://localhost:3001
```

### Backend (.env in backend/)
```
PORT=3001
JWT_SECRET=firewall_soc_secret_key_2026
NODE_ENV=development
CORS_ORIGIN=http://localhost:5173
```

## Features Breakdown

### Phase 1: ✅ Complete
- Project setup with Docker configuration
- Frontend scaffolding with Vite + React + Tailwind
- Backend scaffolding with Express + Socket.io
- Basic authentication system

### Phase 2: ✅ Complete
- Login page with JWT tokens
- AuthContext for state management
- Protected routes

### Phase 3: ✅ Complete
- WebSocket infrastructure
- Real-time event streaming
- Mock data generation

### Phase 4: ✅ Complete
- Dashboard layout and navigation
- Responsive sidebar
- Header with connection status

### Phase 5: ✅ Complete
- Real-time event monitor
- Event filtering and search
- Color-coded severity levels

### Phase 6: ✅ Complete
- Firewall rule management
- CRUD operations
- Rule enable/disable toggle
- Hit statistics

### Phase 7: ✅ Complete
- Traffic analytics dashboard
- Multiple chart types (Line, Bar, Pie)
- Key metrics cards
- Protocol distribution

### Phase 8: ✅ Complete
- Alerts and incidents panel
- Alert status management
- Severity filtering
- Real-time alert updates

### Phase 9: ✅ Complete
- Dark mode UI with Tailwind
- Responsive design
- Smooth animations
- Professional styling

### Phase 10: ✅ Complete
- Documentation
- Testing checklist
- End-to-end verification

## Testing Checklist

- [ ] Docker containers build successfully
- [ ] Frontend loads at http://localhost:5173
- [ ] Backend is running at http://localhost:3001
- [ ] Login with test credentials works
- [ ] WebSocket connection established (green indicator in header)
- [ ] Real-time events appearing in Events tab
- [ ] Firewall rules display correctly
- [ ] Can add/edit/delete rules
- [ ] Traffic analytics charts render with data
- [ ] Alerts appear in real-time
- [ ] Can acknowledge and resolve alerts
- [ ] Dashboard is responsive on mobile/tablet
- [ ] Logout functionality works

## Troubleshooting

### Port Already in Use
If port 3001 or 5173 is already in use, modify `docker-compose.yml`:
```yaml
ports:
  - "YOUR_PORT:3001"  # for backend
  - "YOUR_PORT:5173"  # for frontend
```

### WebSocket Connection Failed
- Ensure backend is running and accessible
- Check CORS settings in backend
- Verify VITE_WS_URL environment variable

### Docker Build Fails
- Ensure Docker is running
- Clear Docker cache: `docker-compose down -v`
- Rebuild: `docker-compose up --build`

### No Data Appearing
- Check browser console for errors
- Verify WebSocket connection is established
- Ensure backend is generating mock data

## Future Enhancements

1. **Real Firewall Integration**
   - Connect to Palo Alto Networks API
   - Integrate Cisco ASA
   - Support Fortinet FortiGate

2. **Advanced Features**
   - User management system
   - Role-based access control (RBAC)
   - Audit logging
   - Export reports (CSV/PDF)
   - Email/Slack notifications
   - Advanced filtering with regex

3. **Security Improvements**
   - OAuth2 integration
   - Two-factor authentication
   - SSL/TLS encryption
   - Rate limiting
   - Input validation

4. **Performance**
   - Data persistence (database)
   - Caching layer (Redis)
   - Search optimization
   - Query performance tuning

5. **Monitoring**
   - Prometheus metrics
   - ELK Stack integration
   - Health checks
   - Performance monitoring

## Security Notes

This is a **demonstration project**. For production use:

1. Replace hardcoded credentials with a proper user database
2. Implement OAuth2 or similar for authentication
3. Use environment variables for all secrets
4. Enable HTTPS/TLS
5. Add input validation and sanitization
6. Implement rate limiting
7. Set up proper logging and monitoring
8. Use a real database instead of in-memory data
9. Add CSRF protection
10. Implement proper error handling and logging

## License

This project is created for educational purposes.

## Support

For issues, questions, or feedback:
- Check the troubleshooting section
- Review the terminal output for errors
- Ensure all prerequisites are installed
- Verify Docker is running properly

## Contributors

Created with React, Tailwind CSS, and Node.js for the MEMEC Firewall Security Dashboard project.

---

**Status:** Production Ready for Demo/Learning
**Last Updated:** January 2026
**Version:** 1.0.0
