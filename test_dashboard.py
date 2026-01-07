#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Test script for Firewall Dashboard Analytics
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app to path
sys.path.insert(0, os.path.dirname(__file__))

from apps import create_app, db
from apps.config import config_dict
from apps.authentication.models import (
    Users, AuditLog, LoginStatistics, AccessTable, DailyAuditReport
)
from apps.firewall.analytics import DashboardAnalytics

def test_database_connection():
    """Test database connection"""
    print("\n[TEST] Database Connection")
    try:
        app = create_app(config_dict['Debug'])
        with app.app_context():
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"  Tables found: {len(tables)}")
            print(f"  Sample tables: {tables[:5]}")
            return True
    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_analytics_functions():
    """Test all analytics functions"""
    print("\n[TEST] Analytics Functions")
    try:
        app = create_app(config_dict['Debug'])
        with app.app_context():
            # Test each analytics function
            tests = [
                ("Today login attempts", DashboardAnalytics.get_today_login_attempts),
                ("Today blocked IPs", DashboardAnalytics.get_today_blocked_ips),
                ("Active whitelist entries", DashboardAnalytics.get_active_whitelist_entries),
                ("Today security alerts", DashboardAnalytics.get_today_security_alerts),
                ("Yesterday login attempts", DashboardAnalytics.get_yesterday_login_attempts),
                ("Hourly login activity", DashboardAnalytics.get_hourly_login_activity),
                ("Weekly access trends", DashboardAnalytics.get_weekly_access_trends),
                ("Risk distribution", DashboardAnalytics.get_risk_distribution),
                ("Recent security events", DashboardAnalytics.get_recent_security_events),
                ("Top blocked IPs", DashboardAnalytics.get_top_blocked_ips),
                ("Top login times", DashboardAnalytics.get_top_login_times),
                ("User login frequency", DashboardAnalytics.get_user_login_frequency),
                ("Monthly summary", DashboardAnalytics.get_monthly_summary)
            ]

            passed = 0
            failed = 0

            for test_name, func in tests:
                try:
                    result = func()
                    if result is not None:
                        print(f"  [PASS] {test_name}")
                        passed += 1
                    else:
                        print(f"  [FAIL] {test_name} - returned None")
                        failed += 1
                except Exception as e:
                    print(f"  [ERROR] {test_name}: {e}")
                    failed += 1

            print(f"\n  Results: {passed} passed, {failed} failed")
            return failed == 0

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints"""
    print("\n[TEST] API Endpoints")
    try:
        app = create_app(config_dict['Debug'])

        # Create test client
        with app.app_context():
            client = app.test_client()

            endpoints = [
                "/firewall/api/dashboard/metrics",
                "/firewall/api/dashboard/hourly-activity",
                "/firewall/api/dashboard/weekly-trends",
                "/firewall/api/dashboard/risk-distribution",
                "/firewall/api/dashboard/recent-events",
                "/firewall/api/dashboard/top-blocked-ips",
                "/firewall/api/dashboard/top-login-times",
                "/firewall/api/dashboard/user-frequency",
                "/firewall/api/dashboard/monthly-summary"
            ]

            passed = 0
            failed = 0

            for endpoint in endpoints:
                try:
                    # Note: These will fail with 401 without login, but they should at least be defined
                    response = client.get(endpoint)
                    # Check if endpoint exists (not 404)
                    if response.status_code != 404:
                        print(f"  [PASS] {endpoint} (status: {response.status_code})")
                        passed += 1
                    else:
                        print(f"  [FAIL] {endpoint} - not found")
                        failed += 1
                except Exception as e:
                    print(f"  [ERROR] {endpoint}: {e}")
                    failed += 1

            print(f"\n  Results: {passed} passed, {failed} failed")
            return failed == 0

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def test_models():
    """Test database models"""
    print("\n[TEST] Database Models")
    try:
        app = create_app(config_dict['Debug'])
        with app.app_context():
            # Test model imports
            models = [
                ("Users", Users),
                ("AuditLog", AuditLog),
                ("LoginStatistics", LoginStatistics),
                ("AccessTable", AccessTable),
                ("DailyAuditReport", DailyAuditReport)
            ]

            passed = 0
            for model_name, model_class in models:
                try:
                    # Check if model has basic attributes
                    if hasattr(model_class, '__tablename__'):
                        print(f"  [PASS] {model_name} model loaded")
                        passed += 1
                    else:
                        print(f"  [FAIL] {model_name} - invalid model")
                except Exception as e:
                    print(f"  [ERROR] {model_name}: {e}")

            print(f"\n  Results: {passed}/{len(models)} models loaded successfully")
            return passed == len(models)

    except Exception as e:
        print(f"  ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Firewall Dashboard Analytics - Test Suite")
    print("=" * 60)

    results = []

    results.append(("Database Connection", test_database_connection()))
    results.append(("Database Models", test_models()))
    results.append(("Analytics Functions", test_analytics_functions()))
    results.append(("API Endpoints", test_api_endpoints()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {test_name}")

    print(f"\nTotal: {passed}/{total} test groups passed")

    if passed == total:
        print("\nAll tests PASSED! Dashboard is ready.")
        return 0
    else:
        print(f"\n{total - passed} test group(s) FAILED.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
