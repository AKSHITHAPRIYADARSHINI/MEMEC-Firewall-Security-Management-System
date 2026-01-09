import os
import sys

# Disable scheduler to speed up startup
os.environ['DISABLE_SCHEDULER'] = 'True'

from apps.config import config_dict
from apps import create_app, db
from flask_migrate import Migrate

DEBUG = True
app_config = config_dict['Debug']
app = create_app(app_config)
Migrate(app, db)

if __name__ == "__main__":
    print("\n✅ Starting Firewall Dashboard")
    print("🌐 URL: http://localhost:5000")
    print("📝 Login: http://localhost:5000/login\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
