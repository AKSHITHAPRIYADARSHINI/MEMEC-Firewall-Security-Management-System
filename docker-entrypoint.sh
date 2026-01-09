#!/bin/bash
set -e

echo "Starting Firewall Dashboard..."
echo "Environment: Production Mode"
echo "Database: SQLite"
echo "Port: 5000"

# Run the application
python -c "
from waitress import serve
from apps.config import config_dict
from apps import create_app
import os

os.environ['DISABLE_SCHEDULER'] = 'True'
app = create_app(config_dict['Production'])
print('=================================================')
print('Firewall Security Management System')
print('=================================================')
print('Server running on http://0.0.0.0:5000')
print('Login: http://localhost:5000/login')
print('=================================================')
serve(app, host='0.0.0.0', port=5000, threads=4)
"
