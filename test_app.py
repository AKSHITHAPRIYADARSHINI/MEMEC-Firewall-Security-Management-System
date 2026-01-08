#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Minimal test app to verify Flask works
"""

from flask import Flask, render_template_string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Firewall Dashboard - Test</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .info { background: #e3f2fd; padding: 15px; border-radius: 4px; margin: 15px 0; border-left: 4px solid #2196F3; }
            .button { background: #66bb6a; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
            .button:hover { background: #58a85c; }
            code { background: #f0f0f0; padding: 2px 6px; border-radius: 3px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Firewall Security Dashboard</h1>
            <div class="info">
                <strong>Status:</strong> Application is running correctly!
            </div>

            <h2>Login Information</h2>
            <p>Use these credentials to access the full dashboard:</p>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f9f9f9;">
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Role</th>
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Username</th>
                    <th style="padding: 10px; border: 1px solid #ddd; text-align: left;">Password</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">Admin</td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>admin</code></td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>password123</code></td>
                </tr>
                <tr style="background: #f9f9f9;">
                    <td style="padding: 10px; border: 1px solid #ddd;">Lower Admin</td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>lower_admin</code></td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>password123</code></td>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">User</td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>john_doe</code></td>
                    <td style="padding: 10px; border: 1px solid #ddd;"><code>password123</code></td>
                </tr>
            </table>

            <h2>Features</h2>
            <ul>
                <li>Real-time Firewall Analytics Dashboard</li>
                <li>24-Hour Login Activity Chart</li>
                <li>7-Day Access Trends</li>
                <li>Risk Distribution Visualization</li>
                <li>Recent Security Events Log</li>
                <li>User Management & Access Control</li>
                <li>Audit Logs & Statistics</li>
                <li>Collapsible Sidebar Navigation</li>
            </ul>

            <h2>Sidebar Features</h2>
            <ul>
                <li>Collapse/Expand toggle button with smooth animations</li>
                <li>Icons-only view when collapsed (70px width)</li>
                <li>Tooltips on hover in collapsed state</li>
                <li>localStorage persistence across sessions</li>
                <li>Responsive design for all devices</li>
                <li>Role-based menu visibility</li>
            </ul>

            <div style="margin-top: 30px; padding: 20px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px;">
                <strong>Next Steps:</strong>
                <ol>
                    <li>Click the button below to access the full dashboard</li>
                    <li>Login with admin account</li>
                    <li>Explore the firewall analytics and management tools</li>
                    <li>Test the sidebar collapse/expand feature</li>
                </ol>
            </div>

            <p style="margin-top: 20px;">
                <a href="/login" class="button">Go to Dashboard</a>
            </p>
        </div>
    </body>
    </html>
    '''

@app.route('/status')
def status():
    return {
        'status': 'running',
        'message': 'Firewall Dashboard is operational',
        'version': '2.0',
        'features': [
            'Firewall Analytics',
            'User Management',
            'Access Control',
            'Real-time Metrics',
            'Security Events Tracking'
        ]
    }

if __name__ == '__main__':
    print("\n" + "="*70)
    print("FIREWALL SECURITY DASHBOARD")
    print("="*70)
    print("\nURL: http://127.0.0.1:5000/")
    print("Status: http://127.0.0.1:5000/status")
    print("\nLogin Credentials:")
    print("  Admin: admin / password123")
    print("  Lower-Admin: lower_admin / password123")
    print("  User: john_doe / password123")
    print("\n" + "="*70 + "\n")

    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
