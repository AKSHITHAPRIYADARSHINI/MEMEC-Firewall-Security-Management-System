# -*- encoding: utf-8 -*-
"""
Firewall utility functions
"""

import re
import json
from ipaddress import ip_address, ip_network, AddressValueError
from apps.authentication.models import AuditLog
from apps import db
from datetime import datetime


def validate_ip_address(ip_str):
    """Validate if string is a valid IP address"""
    try:
        ip_address(ip_str)
        return True
    except ValueError:
        return False


def validate_cidr_range(cidr_str):
    """Validate if string is a valid CIDR range"""
    try:
        ip_network(cidr_str, strict=False)
        return True
    except ValueError:
        return False


def validate_port_range(port_str):
    """Validate port range string (e.g., '80' or '80-443' or '1024:65535')"""
    if not port_str:
        return False

    parts = re.split(r'[-:]', port_str.strip())

    if len(parts) == 1:
        # Single port
        try:
            port = int(parts[0])
            return 0 <= port <= 65535
        except ValueError:
            return False
    elif len(parts) == 2:
        # Port range
        try:
            start, end = int(parts[0]), int(parts[1])
            return 0 <= start <= end <= 65535
        except ValueError:
            return False

    return False


def validate_network_ranges(ranges_text):
    """Validate multiple network ranges in CIDR format"""
    ranges = ranges_text.strip().split('\n')
    valid_ranges = []
    invalid_ranges = []

    for cidr in ranges:
        cidr = cidr.strip()
        if not cidr:
            continue
        if validate_cidr_range(cidr):
            valid_ranges.append(cidr)
        else:
            invalid_ranges.append(cidr)

    return valid_ranges, invalid_ranges


def validate_json_config(config_text):
    """Validate if text is valid JSON"""
    if not config_text or not config_text.strip():
        return True, {}
    try:
        config = json.loads(config_text)
        return True, config
    except json.JSONDecodeError as e:
        return False, str(e)


def log_audit_event(event_type, event_description, user_id, ip_address=None,
                    risk_level='low', geo_location=None, device_info=None):
    """Log an event to audit trail"""
    audit_log = AuditLog(
        event_type=event_type,
        event_description=event_description,
        user_id=user_id,
        ip_address=ip_address,
        risk_level=risk_level,
        geo_location=geo_location,
        device_info=device_info,
        timestamp=datetime.utcnow()
    )
    db.session.add(audit_log)
    db.session.commit()
    return audit_log


def get_request_ip(request):
    """Get client IP address from request"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0].strip()
    return request.environ.get('REMOTE_ADDR')


def get_device_info(request):
    """Extract device information from request"""
    user_agent = request.environ.get('HTTP_USER_AGENT', 'Unknown')

    # Parse User-Agent for device type
    device_type = 'Unknown'
    if 'Mobile' in user_agent or 'Android' in user_agent:
        device_type = 'Mobile'
    elif 'Tablet' in user_agent or 'iPad' in user_agent:
        device_type = 'Tablet'
    else:
        device_type = 'Desktop'

    return {
        'user_agent': user_agent,
        'device_type': device_type
    }


def is_ip_in_ranges(ip_str, ranges_list):
    """Check if IP address is within any of the specified ranges"""
    try:
        ip = ip_address(ip_str)
        for range_str in ranges_list:
            if ip in ip_network(range_str, strict=False):
                return True
        return False
    except (ValueError, AddressValueError):
        return False


def sort_policies_by_priority(policies):
    """Sort policies by priority (lower number = higher priority)"""
    return sorted(policies, key=lambda p: p.priority)


def check_policy_conflicts(new_policy, existing_policies):
    """Check for conflicting policies"""
    conflicts = []

    for policy in existing_policies:
        if (policy.rule_type == new_policy.rule_type and
            policy.protocol == new_policy.protocol and
            policy.port_range == new_policy.port_range and
            policy.action != new_policy.action):

            conflicts.append({
                'policy': policy,
                'conflict_type': 'Action conflict (Allow vs Block)'
            })

    return conflicts
