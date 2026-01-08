#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Fast startup version - minimal dependencies
"""

import os
from sys import exit

# Disable debug mode for faster startup
os.environ['DEBUG'] = 'False'

from apps.config import config_dict
from apps import create_app, db

try:
    app_config = config_dict['Debug']
except KeyError:
    exit('Error: Invalid config')

# Create app without scheduler
app = create_app(app_config)

# Disable Flask-Minify for faster response
app.config['MINIFY_HTML'] = False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Firewall Security Dashboard - Fast Startup")
    print("="*60)
    print("\nURL: http://127.0.0.1:5000/")
    print("\nLogin Credentials:")
    print("  Admin: admin / password123")
    print("  Lower-Admin: lower_admin / password123")
    print("\n" + "="*60 + "\n")

    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=True)
