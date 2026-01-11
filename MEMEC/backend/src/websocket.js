import {
  generateFirewallEvent,
  generateAlert,
  generateTrafficMetrics,
  generateFirewallRules,
  getStatistics
} from './mockData.js';

const clients = new Map();
let currentRules = generateFirewallRules();
let eventHistory = [];
let alertHistory = [];

export const setupWebSocket = (io) => {
  io.on('connection', (socket) => {
    console.log('Socket connected:', socket.id);

    // Send initial data when client connects
    socket.on('request-initial-data', () => {
      console.log('Client requesting initial data');
      socket.emit('initial-rules', currentRules);
      socket.emit('initial-events', eventHistory.slice(-50)); // Send last 50 events
      socket.emit('initial-alerts', alertHistory.slice(-20)); // Send last 20 alerts
      socket.emit('statistics', getStatistics());
      socket.emit('traffic-metrics', generateTrafficMetrics());
    });

    // Real-time events stream
    socket.on('subscribe-events', () => {
      console.log('Client subscribed to events');
      clients.set(socket.id, { socket, subscribed: 'events' });
    });

    // Rule management
    socket.on('request-rules', () => {
      socket.emit('rules-list', currentRules);
    });

    socket.on('add-rule', (ruleData) => {
      const newRule = {
        id: Math.max(...currentRules.map(r => r.id)) + 1,
        ...ruleData,
        priority: currentRules.length + 1,
        enabled: true,
        hits: 0,
        lastModified: new Date().toISOString()
      };
      currentRules.push(newRule);
      io.emit('rules-updated', currentRules);
      socket.emit('rule-added', newRule);
    });

    socket.on('update-rule', (ruleData) => {
      const index = currentRules.findIndex(r => r.id === ruleData.id);
      if (index !== -1) {
        currentRules[index] = {
          ...currentRules[index],
          ...ruleData,
          lastModified: new Date().toISOString()
        };
        io.emit('rules-updated', currentRules);
        socket.emit('rule-updated', currentRules[index]);
      }
    });

    socket.on('delete-rule', (ruleId) => {
      currentRules = currentRules.filter(r => r.id !== ruleId);
      io.emit('rules-updated', currentRules);
      socket.emit('rule-deleted', ruleId);
    });

    socket.on('toggle-rule', (ruleId) => {
      const rule = currentRules.find(r => r.id === ruleId);
      if (rule) {
        rule.enabled = !rule.enabled;
        rule.lastModified = new Date().toISOString();
        io.emit('rules-updated', currentRules);
      }
    });

    // Alert management
    socket.on('acknowledge-alert', (alertId) => {
      const alert = alertHistory.find(a => a.id === alertId);
      if (alert) {
        alert.status = 'Acknowledged';
        io.emit('alert-acknowledged', alertId);
      }
    });

    socket.on('resolve-alert', (alertId) => {
      const alert = alertHistory.find(a => a.id === alertId);
      if (alert) {
        alert.status = 'Resolved';
        io.emit('alert-resolved', alertId);
      }
    });

    socket.on('disconnect', () => {
      console.log('Socket disconnected:', socket.id);
      clients.delete(socket.id);
    });
  });

  // Emit real-time events every 2-3 seconds
  setInterval(() => {
    const event = generateFirewallEvent();
    eventHistory.push(event);

    // Keep only last 500 events
    if (eventHistory.length > 500) {
      eventHistory = eventHistory.slice(-500);
    }

    io.emit('new-event', event);

    // Randomly generate alerts based on suspicious activity
    if (Math.random() < 0.15) {
      const alert = generateAlert();
      alertHistory.push(alert);

      // Keep only last 100 alerts
      if (alertHistory.length > 100) {
        alertHistory = alertHistory.slice(-100);
      }

      io.emit('new-alert', alert);
    }
  }, 2000);

  // Update traffic metrics every 10 seconds
  setInterval(() => {
    io.emit('traffic-metrics', generateTrafficMetrics());
  }, 10000);

  // Update statistics every 5 seconds
  setInterval(() => {
    io.emit('statistics', getStatistics());
  }, 5000);
};
