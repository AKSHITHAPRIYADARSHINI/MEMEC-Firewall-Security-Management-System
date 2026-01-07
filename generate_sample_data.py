#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Generate Sample Security Data for Firewall Dashboard Testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

sys.path.insert(0, os.path.dirname(__file__))

from apps import create_app, db
from apps.config import config_dict
from apps.authentication.models import (
    Users, AuditLog, LoginStatistics, AccessTable, FirewallConfig
)

def create_sample_users(app):
    """Create sample users"""
    print("\n[SETUP] Creating sample users...")
    with app.app_context():
        try:
            # Check if users already exist
            if Users.query.count() > 0:
                print("  Users already exist, skipping creation")
                return

            users = [
                Users(username='admin', email='admin@example.com', role='admin'),
                Users(username='lower_admin', email='loweradmin@example.com', role='lower_admin'),
                Users(username='john_doe', email='john@example.com', role='user'),
                Users(username='jane_smith', email='jane@example.com', role='user'),
                Users(username='bob_wilson', email='bob@example.com', role='user')
            ]

            for user in users:
                user.password = 'password123'  # This will be hashed
                db.session.add(user)

            db.session.commit()
            print(f"  Created {len(users)} sample users")

        except Exception as e:
            print(f"  Error: {e}")
            db.session.rollback()

def create_sample_access_table(app):
    """Create sample access control entries"""
    print("\n[SETUP] Creating sample access control entries...")
    with app.app_context():
        try:
            if AccessTable.query.count() > 0:
                print("  Access entries already exist, skipping creation")
                return

            admin_user = Users.query.filter_by(username='admin').first()

            # Whitelisted IPs
            whitelist_ips = [
                '192.168.1.100', '192.168.1.101', '192.168.1.102',
                '10.0.0.50', '10.0.0.51', '203.0.113.10'
            ]

            for ip in whitelist_ips:
                entry = AccessTable(
                    ip_address=ip,
                    access_level='allow',
                    added_by=admin_user.id,
                    notes=f'Approved access from {ip}'
                )
                db.session.add(entry)

            # Blacklisted IPs
            blacklist_ips = [
                '192.0.2.1', '192.0.2.2', '192.0.2.3',
                '198.51.100.1', '198.51.100.2'
            ]

            for ip in blacklist_ips:
                entry = AccessTable(
                    ip_address=ip,
                    access_level='block',
                    added_by=admin_user.id,
                    notes=f'Malicious IP - {ip}'
                )
                db.session.add(entry)

            db.session.commit()
            print(f"  Created {len(whitelist_ips) + len(blacklist_ips)} access control entries")

        except Exception as e:
            print(f"  Error: {e}")
            db.session.rollback()

def create_sample_login_statistics(app):
    """Create sample login statistics"""
    print("\n[SETUP] Creating sample login statistics...")
    with app.app_context():
        try:
            if LoginStatistics.query.count() > 0:
                print("  Login statistics already exist, skipping creation")
                return

            users = Users.query.filter(Users.role == 'user').all()

            # Generate login statistics for the last 7 days
            now = datetime.utcnow()
            ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '10.0.0.50', '203.0.113.10']

            for day_offset in range(7):
                day_start = now - timedelta(days=day_offset)

                for hour in range(24):
                    timestamp = day_start.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))

                    # Create 2-8 login attempts per hour
                    for _ in range(random.randint(2, 8)):
                        user = random.choice(users)
                        ip = random.choice(ips)
                        success = random.random() > 0.15  # 85% success rate

                        login = LoginStatistics(
                            user_id=user.id,
                            ip_address=ip,
                            login_time=timestamp,
                            success_status=success,
                            device_info='Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                            session_duration=random.randint(300, 3600) if success else 0
                        )
                        db.session.add(login)

            db.session.commit()
            count = LoginStatistics.query.count()
            print(f"  Created {count} login statistics entries")

        except Exception as e:
            print(f"  Error: {e}")
            db.session.rollback()

def create_sample_audit_logs(app):
    """Create sample audit logs"""
    print("\n[SETUP] Creating sample audit logs...")
    with app.app_context():
        try:
            if AuditLog.query.count() > 0:
                print("  Audit logs already exist, skipping creation")
                return

            users = Users.query.all()
            risk_levels = ['low', 'low', 'low', 'medium', 'medium', 'high', 'critical']
            event_types = ['config_change', 'policy_change', 'access_change', 'unauthorized_access', 'system_event']
            malicious_ips = ['192.0.2.1', '192.0.2.2', '198.51.100.1', '198.51.100.2']

            now = datetime.utcnow()

            # Generate audit logs for last 7 days
            for day_offset in range(7):
                day_start = now - timedelta(days=day_offset)

                # Create 10-30 events per day
                for _ in range(random.randint(10, 30)):
                    timestamp = day_start.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))
                    user = random.choice(users)
                    event_type = random.choice(event_types)
                    risk_level = random.choice(risk_levels)

                    # Use malicious IPs for high-risk events
                    if risk_level in ['high', 'critical']:
                        ip = random.choice(malicious_ips)
                        event_type = 'unauthorized_access'
                    else:
                        ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"

                    descriptions = {
                        'config_change': f'Configuration updated by {user.username}',
                        'policy_change': f'Firewall policy modified by {user.username}',
                        'access_change': f'Access control entry changed',
                        'unauthorized_access': f'Unauthorized access attempt from {ip}',
                        'system_event': f'System event occurred'
                    }

                    log = AuditLog(
                        event_type=event_type,
                        event_description=descriptions[event_type],
                        ip_address=ip,
                        geo_location='USA' if random.random() > 0.3 else 'Unknown',
                        device_info=f'User-Agent: Mozilla/5.0',
                        risk_level=risk_level,
                        user_id=user.id,
                        timestamp=timestamp,
                        is_resolved=random.random() > 0.3
                    )
                    db.session.add(log)

            db.session.commit()
            count = AuditLog.query.count()
            print(f"  Created {count} audit log entries")

        except Exception as e:
            print(f"  Error: {e}")
            db.session.rollback()

def create_sample_firewall_config(app):
    """Create sample firewall configuration"""
    print("\n[SETUP] Creating sample firewall configuration...")
    with app.app_context():
        try:
            if FirewallConfig.query.count() > 0:
                print("  Firewall config already exists, skipping creation")
                return

            admin_user = Users.query.filter_by(username='admin').first()

            config = FirewallConfig(
                firewall_type='hybrid',
                network_ranges='192.168.1.0/24\n10.0.0.0/8\n203.0.113.0/24',
                system_configs='{"mode": "active", "logging": "enabled"}',
                modified_by=admin_user.id,
                is_active=True
            )
            db.session.add(config)
            db.session.commit()
            print("  Created firewall configuration")

        except Exception as e:
            print(f"  Error: {e}")
            db.session.rollback()

def main():
    """Main function"""
    print("=" * 60)
    print("Generate Sample Data for Firewall Dashboard")
    print("=" * 60)

    try:
        app = create_app(config_dict['Debug'])

        with app.app_context():
            # Create tables
            print("\n[SETUP] Creating database tables...")
            db.create_all()
            print("  Database tables created/verified")

            # Create sample data
            create_sample_users(app)
            create_sample_access_table(app)
            create_sample_login_statistics(app)
            create_sample_audit_logs(app)
            create_sample_firewall_config(app)

            print("\n" + "=" * 60)
            print("Sample data generation completed successfully!")
            print("=" * 60)
            print("\nYou can now log in with:")
            print("  Username: admin")
            print("  Password: password123")
            print("\nOr use the lower_admin account:")
            print("  Username: lower_admin")
            print("  Password: password123")
            return 0

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
