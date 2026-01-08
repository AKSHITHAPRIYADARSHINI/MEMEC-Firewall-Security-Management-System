# -*- encoding: utf-8 -*-
"""
Firewall Forms for configuration and management
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Optional, Length, IPAddress, ValidationError
import re


class FirewallConfigForm(FlaskForm):
    """Form for firewall configuration"""
    firewall_type = SelectField(
        'Firewall Type',
        choices=[
            ('host_based', 'Host-Based Firewall (Protects individual systems)'),
            ('network_based', 'Network-Based Firewall (Protects network perimeter)'),
            ('hybrid', 'Hybrid Mode (Both host and network)')
        ],
        validators=[DataRequired()]
    )

    network_ranges = TextAreaField(
        'Network Ranges',
        validators=[DataRequired(), Length(min=5)],
        render_kw={
            "placeholder": "Enter network ranges in CIDR notation (one per line)\n192.168.0.0/24\n10.0.0.0/8"
        }
    )

    system_configs = TextAreaField(
        'System-Specific Rules (JSON)',
        validators=[Optional()],
        render_kw={
            "placeholder": 'Optional: {"server1": {"rules": []}, "workstation1": {"rules": []}}'
        }
    )

    submit = SubmitField('Save Configuration')


class AccessTableForm(FlaskForm):
    """Form for adding/editing IP access control entries"""
    ip_address = StringField(
        'IP Address',
        validators=[DataRequired()],
        render_kw={"placeholder": "192.168.1.100 or 2001:db8::1"}
    )

    device_id = StringField(
        'Device Identifier',
        validators=[Optional(), Length(max=128)],
        render_kw={"placeholder": "Optional: device-name or MAC address"}
    )

    access_level = SelectField(
        'Access Level',
        choices=[
            ('allow', 'Allow - Whitelist'),
            ('block', 'Block - Blacklist')
        ],
        validators=[DataRequired()]
    )

    notes = TextAreaField(
        'Notes',
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Optional: reason for allowing/blocking this IP"}
    )

    submit = SubmitField('Add/Update IP Address')


class PolicyForm(FlaskForm):
    """Form for creating/editing firewall policies"""
    policy_name = StringField(
        'Policy Name',
        validators=[DataRequired(), Length(min=3, max=128)],
        render_kw={"placeholder": "e.g., Allow Web Traffic"}
    )

    rule_type = SelectField(
        'Rule Type',
        choices=[
            ('inbound', 'Inbound (Incoming traffic)'),
            ('outbound', 'Outbound (Outgoing traffic)')
        ],
        validators=[DataRequired()]
    )

    protocol = SelectField(
        'Protocol',
        choices=[
            ('TCP', 'TCP'),
            ('UDP', 'UDP'),
            ('ICMP', 'ICMP'),
            ('ALL', 'All Protocols')
        ],
        validators=[DataRequired()]
    )

    port_range = StringField(
        'Port Range',
        validators=[DataRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "e.g., 80 or 80-443 or 1024:65535"}
    )

    source_ip = StringField(
        'Source IP (Optional)',
        validators=[Optional()],
        render_kw={"placeholder": "192.168.1.0/24 or specific IP"}
    )

    destination_ip = StringField(
        'Destination IP (Optional)',
        validators=[Optional()],
        render_kw={"placeholder": "10.0.0.0/8 or specific IP"}
    )

    action = SelectField(
        'Action',
        choices=[
            ('allow', 'Allow'),
            ('deny', 'Deny/Block')
        ],
        validators=[DataRequired()]
    )

    priority = StringField(
        'Priority',
        default='100',
        validators=[DataRequired()],
        render_kw={"placeholder": "Lower number = higher priority"}
    )

    submit = SubmitField('Create/Update Policy')


class AuditLogFilterForm(FlaskForm):
    """Form for filtering audit logs"""
    event_type = SelectField(
        'Event Type',
        choices=[
            ('', 'All Events'),
            ('config_change', 'Configuration Changes'),
            ('policy_change', 'Policy Changes'),
            ('access_change', 'Access Table Changes'),
            ('unauthorized_access', 'Unauthorized Access'),
            ('system_event', 'System Events')
        ],
        validators=[Optional()]
    )

    risk_level = SelectField(
        'Risk Level',
        choices=[
            ('', 'All Levels'),
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        validators=[Optional()]
    )

    submit = SubmitField('Filter')


class ExportAuditForm(FlaskForm):
    """Form for exporting audit logs"""
    export_format = SelectField(
        'Export Format',
        choices=[
            ('csv', 'CSV'),
            ('pdf', 'PDF'),
            ('json', 'JSON')
        ],
        validators=[DataRequired()]
    )

    admin_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Re-enter your password to confirm export"}
    )

    submit = SubmitField('Export Audit Logs')
