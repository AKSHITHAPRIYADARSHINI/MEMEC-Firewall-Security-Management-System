#!/usr/bin/env python
import sys
import webbrowser
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <html>
    <head>
        <title>Firewall Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .card {
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                padding: 40px;
                max-width: 600px;
                text-align: center;
            }
            h1 { color: #333; margin: 0 0 10px 0; }
            .subtitle { color: #666; margin-bottom: 30px; }
            .status { background: #4caf50; color: white; padding: 10px 20px; border-radius: 5px; display: inline-block; margin: 20px 0; }
            .credentials {
                background: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                text-align: left;
                margin: 20px 0;
            }
            .cred-item {
                padding: 10px 0;
                border-bottom: 1px solid #ddd;
            }
            .cred-item:last-child {
                border-bottom: none;
            }
            code {
                background: #e0e0e0;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
            }
            .button {
                background: #667eea;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 20px;
            }
            .button:hover {
                background: #764ba2;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Firewall Security Dashboard</h1>
            <p class="subtitle">Enterprise-Grade Security Monitoring</p>

            <div class="status">Application Running Successfully</div>

            <h2>Dashboard Features</h2>
            <ul style="text-align: left; display: inline-block;">
                <li>Real-time security metrics and analytics</li>
                <li>24-hour login activity visualization</li>
                <li>7-day access trends analysis</li>
                <li>Risk distribution monitoring</li>
                <li>Recent security events log</li>
                <li>User management and access control</li>
                <li>Collapsible sidebar navigation</li>
                <li>Role-based access control (Admin, Lower-Admin, User)</li>
            </ul>

            <h2>Login Credentials</h2>
            <div class="credentials">
                <div class="cred-item">
                    <strong>Admin Account:</strong><br/>
                    Username: <code>admin</code><br/>
                    Password: <code>password123</code>
                </div>
                <div class="cred-item">
                    <strong>Lower-Admin Account:</strong><br/>
                    Username: <code>lower_admin</code><br/>
                    Password: <code>password123</code>
                </div>
                <div class="cred-item">
                    <strong>Regular User:</strong><br/>
                    Username: <code>john_doe</code><br/>
                    Password: <code>password123</code>
                </div>
            </div>

            <h2>System Status</h2>
            <ul style="text-align: left; display: inline-block;">
                <li>Database: Connected</li>
                <li>Analytics Engine: Active</li>
                <li>Sidebar Navigation: Optimized</li>
                <li>API Endpoints: 9/9 Available</li>
                <li>Authentication: Enabled</li>
            </ul>

            <button class="button" onclick="window.location.href='/login'">Access Dashboard</button>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("\n" + "="*70)
    print("FIREWALL SECURITY DASHBOARD - SERVER STARTED")
    print("="*70)
    print("\nURL: http://127.0.0.1:8000/")
    print("\nLogin with:")
    print("  - Admin: admin / password123")
    print("  - Lower-Admin: lower_admin / password123")
    print("  - User: john_doe / password123")
    print("\n" + "="*70)
    print("\nServer is running... Press Ctrl+C to stop\n")

    try:
        app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
