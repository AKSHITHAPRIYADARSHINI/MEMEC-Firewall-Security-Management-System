// Mock Data Generator for Firewall Dashboard

const sourceIPs = [
  '192.168.1.1', '192.168.1.5', '192.168.1.10', '10.0.0.5', '10.0.0.15',
  '172.16.0.1', '8.8.8.8', '1.1.1.1', '203.0.113.45', '198.51.100.20',
  '192.0.2.1', '203.0.113.100', '198.51.100.50', '192.168.2.1', '10.20.0.1'
];

const destIPs = [
  '8.8.8.8', '1.1.1.1', '208.67.222.222', '208.67.220.220', '9.9.9.9',
  '203.0.113.45', '198.51.100.20', '192.0.2.1', '203.0.113.100', '198.51.100.50'
];

const ports = [80, 443, 22, 23, 25, 53, 110, 143, 389, 445, 465, 587, 993, 995, 3306, 3389, 5432, 8080, 8443];
const protocols = ['TCP', 'UDP', 'ICMP', 'DNS', 'TLS', 'SSH'];
const actions = ['ALLOW', 'BLOCK', 'DROP', 'REJECT'];
const severities = ['Low', 'Medium', 'High', 'Critical'];

const alertTypes = [
  'Connection Attempt',
  'Port Scan Detected',
  'DDoS Attack',
  'Malicious IP Blocked',
  'Policy Violation',
  'Brute Force Attempt',
  'Unusual Traffic',
  'Failed Authentication'
];

const countries = ['US', 'CN', 'RU', 'KP', 'IR', 'SY', 'GB', 'DE', 'FR', 'IN'];

export const generateFirewallEvent = () => {
  const timestamp = new Date();
  const action = actions[Math.floor(Math.random() * actions.length)];
  const severity = severities[Math.floor(Math.random() * severities.length)];

  return {
    id: Math.random().toString(36).substr(2, 9),
    timestamp: timestamp.toISOString(),
    sourceIP: sourceIPs[Math.floor(Math.random() * sourceIPs.length)],
    destIP: destIPs[Math.floor(Math.random() * destIPs.length)],
    sourcePort: Math.floor(Math.random() * 65535),
    destPort: ports[Math.floor(Math.random() * ports.length)],
    protocol: protocols[Math.floor(Math.random() * protocols.length)],
    action: action,
    severity: action === 'BLOCK' || action === 'DROP' ? 'High' : severity,
    bytes: Math.floor(Math.random() * 1000000),
    packets: Math.floor(Math.random() * 5000),
    country: countries[Math.floor(Math.random() * countries.length)],
    ruleName: `Rule-${Math.floor(Math.random() * 100)}`
  };
};

export const generateAlert = () => {
  const timestamp = new Date();
  return {
    id: Math.random().toString(36).substr(2, 9),
    timestamp: timestamp.toISOString(),
    type: alertTypes[Math.floor(Math.random() * alertTypes.length)],
    severity: severities[Math.floor(Math.random() * severities.length)],
    sourceIP: sourceIPs[Math.floor(Math.random() * sourceIPs.length)],
    destIP: destIPs[Math.floor(Math.random() * destIPs.length)],
    message: `Security alert detected: Suspicious activity from ${sourceIPs[Math.floor(Math.random() * sourceIPs.length)]}`,
    status: 'New'
  };
};

export const generateTrafficMetrics = () => {
  const hours = Array.from({ length: 24 }, (_, i) => {
    return {
      time: `${String(i).padStart(2, '0')}:00`,
      inbound: Math.floor(Math.random() * 100) + 20,
      outbound: Math.floor(Math.random() * 80) + 10
    };
  });

  const protocolDistribution = {
    tcp: Math.floor(Math.random() * 40) + 30,
    udp: Math.floor(Math.random() * 30) + 20,
    icmp: Math.floor(Math.random() * 20) + 5,
    other: Math.floor(Math.random() * 15) + 5
  };

  const topSourceIPs = sourceIPs.slice(0, 10).map(ip => ({
    ip,
    traffic: Math.floor(Math.random() * 5000) + 1000
  })).sort((a, b) => b.traffic - a.traffic);

  const topPorts = ports.slice(0, 10).map(port => ({
    port,
    traffic: Math.floor(Math.random() * 3000) + 500
  })).sort((a, b) => b.traffic - a.traffic);

  return {
    hours,
    protocolDistribution,
    topSourceIPs,
    topPorts
  };
};

export const generateFirewallRules = () => {
  const rules = [];
  const protocolsList = ['TCP', 'UDP', 'ICMP', 'ANY'];
  const actionsList = ['ALLOW', 'BLOCK', 'LOG'];

  for (let i = 1; i <= 25; i++) {
    rules.push({
      id: i,
      name: `Rule-${String(i).padStart(3, '0')}`,
      sourceIP: `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.0.0/16`,
      destIP: `${Math.floor(Math.random() * 256)}.${Math.floor(Math.random() * 256)}.0.0/16`,
      port: ports[Math.floor(Math.random() * ports.length)],
      protocol: protocolsList[Math.floor(Math.random() * protocolsList.length)],
      action: actionsList[Math.floor(Math.random() * actionsList.length)],
      priority: i,
      enabled: Math.random() > 0.2,
      hits: Math.floor(Math.random() * 10000),
      lastModified: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString()
    });
  }

  return rules;
};

export const getStatistics = () => {
  return {
    totalEvents24h: Math.floor(Math.random() * 5000) + 1000,
    blockedConnections: Math.floor(Math.random() * 500) + 100,
    allowedConnections: Math.floor(Math.random() * 2000) + 500,
    activeRules: 25,
    criticalAlerts: Math.floor(Math.random() * 10) + 2,
    highAlerts: Math.floor(Math.random() * 20) + 5
  };
};
