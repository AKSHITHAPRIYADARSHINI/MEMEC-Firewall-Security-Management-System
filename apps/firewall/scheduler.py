# -*- encoding: utf-8 -*-
"""
Background Task Scheduler for Firewall Dashboard
Handles automated daily report generation and notifications
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import date, datetime
import logging
from apps.firewall.analytics import DashboardAnalytics
from apps.authentication.models import Users
from apps import db

logger = logging.getLogger(__name__)

class DailyAuditScheduler:
    """Manages scheduled tasks for daily audits and reports"""

    _scheduler = None
    _initialized = False

    @staticmethod
    def init_scheduler(app):
        """Initialize the APScheduler"""
        if DailyAuditScheduler._initialized:
            return

        DailyAuditScheduler._scheduler = BackgroundScheduler()

        # Schedule daily report generation at midnight
        DailyAuditScheduler._scheduler.add_job(
            func=DailyAuditScheduler.generate_daily_report,
            trigger=CronTrigger(hour=0, minute=0),
            id='daily_audit_report',
            name='Generate Daily Audit Report',
            replace_existing=True,
            args=[app]
        )

        try:
            DailyAuditScheduler._scheduler.start()
            logger.info("Scheduler initialized successfully")
            DailyAuditScheduler._initialized = True
        except Exception as e:
            logger.error(f"Error initializing scheduler: {e}")

    @staticmethod
    def shutdown_scheduler():
        """Shutdown the scheduler"""
        if DailyAuditScheduler._scheduler:
            try:
                DailyAuditScheduler._scheduler.shutdown()
                DailyAuditScheduler._initialized = False
                logger.info("Scheduler shut down successfully")
            except Exception as e:
                logger.error(f"Error shutting down scheduler: {e}")

    @staticmethod
    def generate_daily_report(app=None):
        """Generate daily audit report"""
        try:
            if app is None:
                from apps import create_app
                from apps.config import config_dict
                app = create_app(config_dict['Debug'])

            with app.app_context():
                # Get yesterday's date (since this runs at midnight)
                yesterday = date.today()

                logger.info(f"Generating daily audit report for {yesterday}")

                # Generate the report
                report = DashboardAnalytics.generate_daily_report(yesterday)

                if report:
                    logger.info(f"Daily report generated successfully for {yesterday}")
                    # TODO: Send email notification to admins
                    DailyAuditScheduler.send_daily_report_email(report)
                else:
                    logger.warning(f"Failed to generate report for {yesterday}")

        except Exception as e:
            logger.error(f"Error generating daily report: {e}")

    @staticmethod
    def send_daily_report_email(report):
        """Send daily report email to administrators"""
        try:
            # Get all admin users
            admin_users = Users.query.filter(
                Users.role.in_(['admin', 'lower_admin'])
            ).all()

            if not admin_users:
                logger.warning("No admin users found for daily report email")
                return

            # TODO: Implement email sending
            # This would require:
            # 1. Flask-Mail extension
            # 2. Email templates
            # 3. SMTP configuration

            logger.info(f"Daily report email would be sent to {len(admin_users)} admin(s)")

        except Exception as e:
            logger.error(f"Error sending daily report email: {e}")

    @staticmethod
    def trigger_manual_report(app=None):
        """Manually trigger report generation (for testing)"""
        try:
            if app is None:
                from apps import create_app
                from apps.config import config_dict
                app = create_app(config_dict['Debug'])

            with app.app_context():
                logger.info("Manually triggering daily audit report")
                DailyAuditScheduler.generate_daily_report(app)

        except Exception as e:
            logger.error(f"Error in manual trigger: {e}")


def init_scheduler(app):
    """Initialize scheduler with Flask app"""
    DailyAuditScheduler.init_scheduler(app)


def shutdown_scheduler():
    """Shutdown scheduler"""
    DailyAuditScheduler.shutdown_scheduler()
