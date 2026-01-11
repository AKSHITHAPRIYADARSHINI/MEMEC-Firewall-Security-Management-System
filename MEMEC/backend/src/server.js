import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import dotenv from 'dotenv';
import { verifyToken, generateToken } from './auth.js';
import { setupWebSocket } from './websocket.js';

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.CORS_ORIGIN || 'http://localhost:5173',
    methods: ['GET', 'POST']
  }
});

const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Firewall Dashboard Backend is running' });
});

app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // Hardcoded credentials for demo
  if (username === 'admin@soc.local' && password === 'firewall123') {
    const token = generateToken({ username, role: 'admin' });
    return res.json({
      success: true,
      token,
      user: { username, role: 'admin' }
    });
  }

  res.status(401).json({
    success: false,
    message: 'Invalid credentials'
  });
});

app.post('/api/validate', (req, res) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) {
    return res.status(401).json({ valid: false });
  }

  const decoded = verifyToken(token);
  if (decoded) {
    return res.json({ valid: true, user: decoded });
  }

  res.status(401).json({ valid: false });
});

// WebSocket Connection
io.on('connection', (socket) => {
  console.log('New client connected:', socket.id);

  socket.on('authenticate', (data) => {
    const decoded = verifyToken(data.token);
    if (decoded) {
      socket.userId = decoded.username;
      socket.emit('authenticated', { success: true });
      console.log(`${socket.userId} authenticated`);
    } else {
      socket.emit('authenticated', { success: false });
      socket.disconnect();
    }
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
});

// Setup WebSocket handlers
setupWebSocket(io);

httpServer.listen(PORT, () => {
  console.log(`Firewall Dashboard Backend running on port ${PORT}`);
  console.log(`Test credentials: admin@soc.local / firewall123`);
});
