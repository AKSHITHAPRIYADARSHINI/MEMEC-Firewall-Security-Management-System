import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'firewall_soc_secret_key_2026';

export const generateToken = (payload) => {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: '24h' });
};

export const verifyToken = (token) => {
  try {
    return jwt.verify(token, JWT_SECRET);
  } catch (error) {
    return null;
  }
};
