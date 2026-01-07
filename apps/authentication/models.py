# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from datetime import datetime

from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    role = db.Column(db.String(20), default='user')  # admin, lower_admin, user

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def is_admin(self):
        return self.role == 'admin'

    def is_lower_admin(self):
        return self.role == 'lower_admin'


class FirewallConfig(db.Model):
    """Firewall configuration settings"""
    __tablename__ = 'FirewallConfig'

    id = db.Column(db.Integer, primary_key=True)
    firewall_type = db.Column(db.String(50))  # host_based, network_based, hybrid
    network_ranges = db.Column(db.Text)  # JSON formatted network ranges
    system_configs = db.Column(db.Text)  # JSON formatted system-specific rules
    is_active = db.Column(db.Boolean, default=True)
    modified_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    modified_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FirewallConfig {self.firewall_type}>'


class AccessTable(db.Model):
    """IP Access Control List"""
    __tablename__ = 'AccessTable'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), unique=True)  # IPv4 or IPv6
    device_id = db.Column(db.String(128))  # Device identifier
    access_level = db.Column(db.String(20))  # allow, block
    added_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    added_by_user = db.relationship('Users', foreign_keys=[added_by])

    def __repr__(self):
        return f'<AccessTable {self.ip_address} - {self.access_level}>'


class Policies(db.Model):
    """Firewall Policies"""
    __tablename__ = 'Policies'

    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(128), unique=True)
    rule_type = db.Column(db.String(20))  # inbound, outbound
    protocol = db.Column(db.String(20))  # TCP, UDP, ICMP
    port_range = db.Column(db.String(50))  # e.g., "80-443" or "22"
    source_ip = db.Column(db.String(45))  # Optional source IP
    destination_ip = db.Column(db.String(45))  # Optional destination IP
    action = db.Column(db.String(20))  # allow, deny
    priority = db.Column(db.Integer, default=100)  # Lower number = higher priority
    created_by = db.Column(db.Integer, db.ForeignKey('Users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Policies {self.policy_name}>'


class AuditLog(db.Model):
    """Comprehensive audit trail for firewall activities"""
    __tablename__ = 'AuditLog'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(50))  # config_change, policy_change, access_change, unauthorized_access, system_event
    event_description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    geo_location = db.Column(db.String(128))  # Country/Region
    device_info = db.Column(db.Text)  # User-Agent, OS, browser info
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text)

    # Relationships
    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f'<AuditLog {self.event_type} at {self.timestamp}>'


class LoginStatistics(db.Model):
    """Login statistics and session tracking"""
    __tablename__ = 'LoginStatistics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    ip_address = db.Column(db.String(45))
    login_time = db.Column(db.DateTime, default=datetime.utcnow)
    logout_time = db.Column(db.DateTime)
    session_duration = db.Column(db.Integer)  # In seconds
    device_info = db.Column(db.Text)  # User-Agent and device type info
    success_status = db.Column(db.Boolean, default=True)
    login_method = db.Column(db.String(50), default='form')  # form, api, etc.

    def __repr__(self):
        return f'<LoginStatistics user_id={self.user_id} at {self.login_time}>'


class DailyAuditReport(db.Model):
    """Daily security audit summaries"""
    __tablename__ = 'DailyAuditReport'

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, unique=True)
    total_login_attempts = db.Column(db.Integer, default=0)
    successful_logins = db.Column(db.Integer, default=0)
    blocked_attempts = db.Column(db.Integer, default=0)
    total_ips_blocked_today = db.Column(db.Integer, default=0)
    low_risk_events = db.Column(db.Integer, default=0)
    medium_risk_events = db.Column(db.Integer, default=0)
    high_risk_events = db.Column(db.Integer, default=0)
    critical_risk_events = db.Column(db.Integer, default=0)
    peak_activity_hour = db.Column(db.Integer)  # Hour of day (0-23)
    most_active_user = db.Column(db.String(64))
    notable_patterns = db.Column(db.Text)  # JSON with pattern details
    recommendations = db.Column(db.Text)  # Security recommendations
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    generated_by = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return f'<DailyAuditReport {self.report_date}>'


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
