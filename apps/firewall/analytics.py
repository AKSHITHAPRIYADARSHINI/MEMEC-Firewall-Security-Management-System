# -*- encoding: utf-8 -*-
"""
Firewall Dashboard Analytics Module
Provides real-time data aggregation for security metrics and visualizations
"""

from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_
import json
from apps.authentication.models import AuditLog, AccessTable, LoginStatistics, Users, DailyAuditReport
from apps import db


class DashboardAnalytics:
    """Core analytics engine for firewall dashboard"""

    @staticmethod
    def get_today_login_attempts():
        """Get total login attempts for today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        count = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= today_start,
                LoginStatistics.login_time < today_end
            )
        ).count()
        return count

    @staticmethod
    def get_today_blocked_ips():
        """Get count of blocked IPs today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        count = AuditLog.query.filter(
            and_(
                AuditLog.timestamp >= today_start,
                AuditLog.timestamp < today_end,
                AuditLog.risk_level.in_(['high', 'critical']),
                AuditLog.event_type == 'unauthorized_access'
            )
        ).count()
        return count

    @staticmethod
    def get_active_whitelist_entries():
        """Get count of active whitelisted IPs"""
        count = AccessTable.query.filter(
            and_(
                AccessTable.is_active == True,
                AccessTable.access_level == 'allow'
            )
        ).count()
        return count

    @staticmethod
    def get_today_security_alerts():
        """Get high and critical risk events today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        count = AuditLog.query.filter(
            and_(
                AuditLog.timestamp >= today_start,
                AuditLog.timestamp < today_end,
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).count()
        return count

    @staticmethod
    def get_yesterday_login_attempts():
        """Get total login attempts for yesterday (for comparison)"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday_start = today_start - timedelta(days=1)

        count = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= yesterday_start,
                LoginStatistics.login_time < today_start
            )
        ).count()
        return count

    @staticmethod
    def get_hourly_login_activity(days_back=0):
        """Get hourly login activity for specified day (default: today)"""
        target_date = datetime.utcnow() - timedelta(days=days_back)
        day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        # Initialize all 24 hours with zeros
        hourly_data = {i: {'successful': 0, 'suspicious': 0, 'blocked': 0} for i in range(24)}

        # Get successful logins
        successful = db.session.query(
            func.strftime('%H', LoginStatistics.login_time).label('hour'),
            func.count(LoginStatistics.id).label('count')
        ).filter(
            and_(
                LoginStatistics.login_time >= day_start,
                LoginStatistics.login_time < day_end,
                LoginStatistics.success_status == True
            )
        ).group_by('hour').all()

        for hour, count in successful:
            hourly_data[int(hour)]['successful'] = count

        # Get suspicious/failed logins
        suspicious = db.session.query(
            func.strftime('%H', LoginStatistics.login_time).label('hour'),
            func.count(LoginStatistics.id).label('count')
        ).filter(
            and_(
                LoginStatistics.login_time >= day_start,
                LoginStatistics.login_time < day_end,
                LoginStatistics.success_status == False
            )
        ).group_by('hour').all()

        for hour, count in suspicious:
            hourly_data[int(hour)]['suspicious'] = count

        # Get blocked attempts
        blocked = db.session.query(
            func.strftime('%H', AuditLog.timestamp).label('hour'),
            func.count(AuditLog.id).label('count')
        ).filter(
            and_(
                AuditLog.timestamp >= day_start,
                AuditLog.timestamp < day_end,
                AuditLog.event_type == 'unauthorized_access',
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).group_by('hour').all()

        for hour, count in blocked:
            hourly_data[int(hour)]['blocked'] = count

        return hourly_data

    @staticmethod
    def get_weekly_access_trends():
        """Get access trends for last 7 days"""
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=6)

        daily_data = []

        for i in range(7):
            current_date = week_ago + timedelta(days=i)
            day_start = current_date
            day_end = day_start + timedelta(days=1)

            total = LoginStatistics.query.filter(
                and_(
                    LoginStatistics.login_time >= day_start,
                    LoginStatistics.login_time < day_end
                )
            ).count()

            successful = LoginStatistics.query.filter(
                and_(
                    LoginStatistics.login_time >= day_start,
                    LoginStatistics.login_time < day_end,
                    LoginStatistics.success_status == True
                )
            ).count()

            blocked = AuditLog.query.filter(
                and_(
                    AuditLog.timestamp >= day_start,
                    AuditLog.timestamp < day_end,
                    AuditLog.event_type == 'unauthorized_access',
                    AuditLog.risk_level.in_(['high', 'critical'])
                )
            ).count()

            daily_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day': current_date.strftime('%a'),
                'total': total,
                'successful': successful,
                'blocked': blocked
            })

        return daily_data

    @staticmethod
    def get_risk_distribution():
        """Get distribution of risk levels for today"""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        risks = {
            'low': AuditLog.query.filter(
                and_(
                    AuditLog.timestamp >= today_start,
                    AuditLog.timestamp < today_end,
                    AuditLog.risk_level == 'low'
                )
            ).count(),
            'medium': AuditLog.query.filter(
                and_(
                    AuditLog.timestamp >= today_start,
                    AuditLog.timestamp < today_end,
                    AuditLog.risk_level == 'medium'
                )
            ).count(),
            'high': AuditLog.query.filter(
                and_(
                    AuditLog.timestamp >= today_start,
                    AuditLog.timestamp < today_end,
                    AuditLog.risk_level == 'high'
                )
            ).count(),
            'critical': AuditLog.query.filter(
                and_(
                    AuditLog.timestamp >= today_start,
                    AuditLog.timestamp < today_end,
                    AuditLog.risk_level == 'critical'
                )
            ).count()
        }

        return risks

    @staticmethod
    def get_recent_security_events(limit=20, risk_level=None):
        """Get recent security events"""
        query = AuditLog.query.order_by(AuditLog.timestamp.desc())

        if risk_level and risk_level != 'all':
            query = query.filter(AuditLog.risk_level == risk_level)

        events = query.limit(limit).all()

        return [{
            'id': event.id,
            'timestamp': event.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': event.ip_address,
            'event_type': event.event_type,
            'risk_level': event.risk_level,
            'description': event.event_description,
            'geo_location': event.geo_location
        } for event in events]

    @staticmethod
    def get_top_blocked_ips(limit=10):
        """Get most frequently blocked IPs"""
        blocked_ips = db.session.query(
            AuditLog.ip_address,
            func.count(AuditLog.id).label('block_count')
        ).filter(
            and_(
                AuditLog.event_type == 'unauthorized_access',
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).group_by(AuditLog.ip_address).order_by(
            func.count(AuditLog.id).desc()
        ).limit(limit).all()

        return [{
            'ip': ip,
            'count': count
        } for ip, count in blocked_ips]

    @staticmethod
    def get_top_login_times():
        """Get most active hours of the day"""
        data = db.session.query(
            func.strftime('%H', LoginStatistics.login_time).label('hour'),
            func.count(LoginStatistics.id).label('count')
        ).filter(
            LoginStatistics.login_time >= (datetime.utcnow() - timedelta(days=7))
        ).group_by('hour').order_by(
            func.count(LoginStatistics.id).desc()
        ).all()

        return [{
            'hour': f"{int(hour):02d}:00",
            'count': count
        } for hour, count in data]

    @staticmethod
    def get_user_login_frequency(limit=10):
        """Get users with most login attempts"""
        users_data = db.session.query(
            Users.username,
            func.count(LoginStatistics.id).label('login_count')
        ).join(
            LoginStatistics, Users.id == LoginStatistics.user_id
        ).filter(
            LoginStatistics.login_time >= (datetime.utcnow() - timedelta(days=7))
        ).group_by(Users.username).order_by(
            func.count(LoginStatistics.id).desc()
        ).limit(limit).all()

        return [{
            'username': username,
            'count': count
        } for username, count in users_data]

    @staticmethod
    def get_monthly_summary(month_offset=0):
        """Get summary for current or past month"""
        now = datetime.utcnow()
        if month_offset > 0:
            first_day = (now - timedelta(days=now.day-1)).replace(hour=0, minute=0, second=0, microsecond=0)
            first_day = first_day.replace(month=first_day.month - month_offset if first_day.month > month_offset else 12)
        else:
            first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        if now.month == 12:
            last_day = first_day.replace(year=first_day.year + 1, month=1) - timedelta(days=1)
        else:
            last_day = first_day.replace(month=first_day.month + 1) - timedelta(days=1)

        last_day = last_day.replace(hour=23, minute=59, second=59)

        total_logins = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= first_day,
                LoginStatistics.login_time <= last_day
            )
        ).count()

        successful_logins = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= first_day,
                LoginStatistics.login_time <= last_day,
                LoginStatistics.success_status == True
            )
        ).count()

        blocked = AuditLog.query.filter(
            and_(
                AuditLog.timestamp >= first_day,
                AuditLog.timestamp <= last_day,
                AuditLog.event_type == 'unauthorized_access',
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).count()

        # Find peak hour
        peak_hour_result = db.session.query(
            func.strftime('%H', LoginStatistics.login_time).label('hour'),
            func.count(LoginStatistics.id).label('count')
        ).filter(
            and_(
                LoginStatistics.login_time >= first_day,
                LoginStatistics.login_time <= last_day
            )
        ).group_by('hour').order_by(
            func.count(LoginStatistics.id).desc()
        ).first()

        peak_hour = int(peak_hour_result[0]) if peak_hour_result else 0

        # Find most active user
        most_active_result = db.session.query(
            Users.username,
            func.count(LoginStatistics.id).label('count')
        ).join(
            LoginStatistics, Users.id == LoginStatistics.user_id
        ).filter(
            and_(
                LoginStatistics.login_time >= first_day,
                LoginStatistics.login_time <= last_day
            )
        ).group_by(Users.username).order_by(
            func.count(LoginStatistics.id).desc()
        ).first()

        most_active_user = most_active_result[0] if most_active_result else 'N/A'

        return {
            'month': first_day.strftime('%B %Y'),
            'total_logins': total_logins,
            'successful_logins': successful_logins,
            'blocked_attempts': blocked,
            'peak_hour': f"{peak_hour:02d}:00",
            'most_active_user': most_active_user
        }

    @staticmethod
    def generate_daily_report(report_date=None):
        """Generate daily audit report for specified date or today"""
        if report_date is None:
            report_date = date.today()

        day_start = datetime.combine(report_date, datetime.min.time())
        day_end = datetime.combine(report_date, datetime.max.time())

        # Get all metrics for the day
        total_attempts = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= day_start,
                LoginStatistics.login_time <= day_end
            )
        ).count()

        successful = LoginStatistics.query.filter(
            and_(
                LoginStatistics.login_time >= day_start,
                LoginStatistics.login_time <= day_end,
                LoginStatistics.success_status == True
            )
        ).count()

        blocked = AuditLog.query.filter(
            and_(
                AuditLog.timestamp >= day_start,
                AuditLog.timestamp <= day_end,
                AuditLog.event_type == 'unauthorized_access',
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).count()

        # Count unique blocked IPs
        unique_blocked_ips = db.session.query(
            func.count(func.distinct(AuditLog.ip_address))
        ).filter(
            and_(
                AuditLog.timestamp >= day_start,
                AuditLog.timestamp <= day_end,
                AuditLog.event_type == 'unauthorized_access',
                AuditLog.risk_level.in_(['high', 'critical'])
            )
        ).scalar() or 0

        # Risk distribution
        risk_dist = DashboardAnalytics.get_risk_distribution()

        # Peak hour
        peak_hour_result = db.session.query(
            func.strftime('%H', LoginStatistics.login_time).label('hour'),
            func.count(LoginStatistics.id).label('count')
        ).filter(
            and_(
                LoginStatistics.login_time >= day_start,
                LoginStatistics.login_time <= day_end
            )
        ).group_by('hour').order_by(
            func.count(LoginStatistics.id).desc()
        ).first()

        peak_hour = int(peak_hour_result[0]) if peak_hour_result else None

        # Check for existing report
        existing_report = DailyAuditReport.query.filter_by(report_date=report_date).first()

        if existing_report:
            # Update existing report
            existing_report.total_login_attempts = total_attempts
            existing_report.successful_logins = successful
            existing_report.blocked_attempts = blocked
            existing_report.total_ips_blocked_today = unique_blocked_ips
            existing_report.low_risk_events = risk_dist['low']
            existing_report.medium_risk_events = risk_dist['medium']
            existing_report.high_risk_events = risk_dist['high']
            existing_report.critical_risk_events = risk_dist['critical']
            existing_report.peak_activity_hour = peak_hour
            db.session.commit()
            return existing_report
        else:
            # Create new report
            new_report = DailyAuditReport(
                report_date=report_date,
                total_login_attempts=total_attempts,
                successful_logins=successful,
                blocked_attempts=blocked,
                total_ips_blocked_today=unique_blocked_ips,
                low_risk_events=risk_dist['low'],
                medium_risk_events=risk_dist['medium'],
                high_risk_events=risk_dist['high'],
                critical_risk_events=risk_dist['critical'],
                peak_activity_hour=peak_hour
            )
            db.session.add(new_report)
            db.session.commit()
            return new_report

    @staticmethod
    def get_all_dashboard_data(days_back=0):
        """Get all dashboard data at once for efficiency"""
        return {
            'today_logins': DashboardAnalytics.get_today_login_attempts(),
            'yesterday_logins': DashboardAnalytics.get_yesterday_login_attempts(),
            'today_blocked_ips': DashboardAnalytics.get_today_blocked_ips(),
            'active_whitelist': DashboardAnalytics.get_active_whitelist_entries(),
            'today_alerts': DashboardAnalytics.get_today_security_alerts(),
            'hourly_activity': DashboardAnalytics.get_hourly_login_activity(days_back),
            'weekly_trends': DashboardAnalytics.get_weekly_access_trends(),
            'risk_distribution': DashboardAnalytics.get_risk_distribution(),
            'recent_events': DashboardAnalytics.get_recent_security_events(),
            'top_blocked_ips': DashboardAnalytics.get_top_blocked_ips(),
            'top_login_times': DashboardAnalytics.get_top_login_times(),
            'user_frequency': DashboardAnalytics.get_user_login_frequency(),
            'monthly_summary': DashboardAnalytics.get_monthly_summary()
        }
