# -*- encoding: utf-8 -*-
"""
Firewall Management Routes
"""

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user

from apps import db
from apps.firewall import blueprint
from apps.firewall.forms import FirewallConfigForm
from apps.firewall.utils import (
    validate_network_ranges, validate_json_config,
    log_audit_event, get_request_ip, get_device_info
)
from apps.authentication.decorators import admin_required, lower_admin_required
from apps.authentication.models import Users
from apps.authentication.models import FirewallConfig, AccessTable, Policies, AuditLog, LoginStatistics


@blueprint.route('/dashboard')
@lower_admin_required
def dashboard():
    """Main firewall analytics dashboard with real-time security metrics"""
    return render_template('firewall/dashboard_analytics.html')


@blueprint.route('/config', methods=['GET', 'POST'])
@admin_required
def config():
    """Firewall configuration page"""
    form = FirewallConfigForm(request.form)
    fw_config = FirewallConfig.query.first()

    if form.validate_on_submit() or (request.method == 'POST' and 'submit' in request.form):
        # Validate network ranges
        valid_ranges, invalid_ranges = validate_network_ranges(form.network_ranges.data)

        if invalid_ranges:
            flash(f'Invalid CIDR ranges: {", ".join(invalid_ranges)}', 'danger')
            return render_template('firewall/config.html', form=form, fw_config=fw_config)

        # Validate JSON if provided
        if form.system_configs.data:
            is_valid_json, json_result = validate_json_config(form.system_configs.data)
            if not is_valid_json:
                flash(f'Invalid JSON in system configs: {json_result}', 'danger')
                return render_template('firewall/config.html', form=form, fw_config=fw_config)

        # Update or create firewall config
        if fw_config:
            # Store old values for audit
            old_type = fw_config.firewall_type
            fw_config.firewall_type = form.firewall_type.data
            fw_config.network_ranges = '\n'.join(valid_ranges)
            fw_config.system_configs = form.system_configs.data or None
            fw_config.modified_by = current_user.id
        else:
            fw_config = FirewallConfig(
                firewall_type=form.firewall_type.data,
                network_ranges='\n'.join(valid_ranges),
                system_configs=form.system_configs.data or None,
                modified_by=current_user.id,
                is_active=True
            )
            db.session.add(fw_config)

        db.session.commit()

        # Log audit event
        log_audit_event(
            event_type='config_change',
            event_description=f'Firewall configuration updated to {form.firewall_type.data}',
            user_id=current_user.id,
            ip_address=get_request_ip(request),
            device_info=str(get_device_info(request)),
            risk_level='low'
        )

        flash('Firewall configuration saved successfully!', 'success')
        return redirect(url_for('firewall_blueprint.config'))

    if fw_config:
        form.firewall_type.data = fw_config.firewall_type
        form.network_ranges.data = fw_config.network_ranges
        form.system_configs.data = fw_config.system_configs

    return render_template('firewall/config.html', form=form, fw_config=fw_config)


@blueprint.route('/access-control', methods=['GET', 'POST'])
@admin_required
def access_control():
    """IP Access Control page with CRUD operations"""
    from apps.firewall.forms import AccessTableForm

    page = request.args.get('page', 1, type=int)
    access_list = AccessTable.query.paginate(page=page, per_page=10)
    form = AccessTableForm(request.form)

    if form.validate_on_submit() or (request.method == 'POST' and 'submit' in request.form):
        ip = form.ip_address.data.strip()

        # Check if IP already exists
        existing_ip = AccessTable.query.filter_by(ip_address=ip).first()
        if existing_ip:
            flash(f'IP address {ip} already exists in access control list', 'warning')
            return redirect(url_for('firewall_blueprint.access_control'))

        # Create new access entry
        access_entry = AccessTable(
            ip_address=ip,
            device_id=form.device_id.data.strip() or None,
            access_level=form.access_level.data,
            added_by=current_user.id,
            notes=form.notes.data or None,
            is_active=True
        )

        db.session.add(access_entry)
        db.session.commit()

        # Log audit event
        log_audit_event(
            event_type='access_change',
            event_description=f'IP address {ip} added to {form.access_level.data.upper()} list',
            user_id=current_user.id,
            ip_address=get_request_ip(request),
            device_info=str(get_device_info(request)),
            risk_level='low'
        )

        flash(f'IP address {ip} added to {form.access_level.data} list successfully!', 'success')
        return redirect(url_for('firewall_blueprint.access_control'))

    return render_template('firewall/access_control.html', access_list=access_list, form=form)


@blueprint.route('/access-control/<int:entry_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_access_control(entry_id):
    """Edit access control entry"""
    from apps.firewall.forms import AccessTableForm

    entry = AccessTable.query.get_or_404(entry_id)
    form = AccessTableForm(request.form)

    if form.validate_on_submit() or (request.method == 'POST' and 'submit' in request.form):
        # Check if IP is being changed and already exists
        if form.ip_address.data.strip() != entry.ip_address:
            existing = AccessTable.query.filter_by(ip_address=form.ip_address.data.strip()).first()
            if existing:
                flash(f'IP address {form.ip_address.data} already exists', 'warning')
                return render_template('firewall/edit_access_control.html', form=form, entry=entry)

        old_ip = entry.ip_address
        old_level = entry.access_level

        entry.ip_address = form.ip_address.data.strip()
        entry.device_id = form.device_id.data.strip() or None
        entry.access_level = form.access_level.data
        entry.notes = form.notes.data or None

        db.session.commit()

        # Log audit event
        changes = []
        if old_ip != entry.ip_address:
            changes.append(f'IP changed from {old_ip} to {entry.ip_address}')
        if old_level != entry.access_level:
            changes.append(f'Level changed from {old_level} to {entry.access_level}')

        log_audit_event(
            event_type='access_change',
            event_description=f'IP entry updated: {", ".join(changes)}',
            user_id=current_user.id,
            ip_address=get_request_ip(request),
            device_info=str(get_device_info(request)),
            risk_level='low'
        )

        flash(f'IP address {entry.ip_address} updated successfully!', 'success')
        return redirect(url_for('firewall_blueprint.access_control'))

    if request.method == 'GET':
        form.ip_address.data = entry.ip_address
        form.device_id.data = entry.device_id
        form.access_level.data = entry.access_level
        form.notes.data = entry.notes

    return render_template('firewall/edit_access_control.html', form=form, entry=entry)


@blueprint.route('/access-control/<int:entry_id>/delete', methods=['POST'])
@admin_required
def delete_access_control(entry_id):
    """Delete access control entry"""
    entry = AccessTable.query.get_or_404(entry_id)
    ip_address = entry.ip_address
    access_level = entry.access_level

    db.session.delete(entry)
    db.session.commit()

    # Log audit event
    log_audit_event(
        event_type='access_change',
        event_description=f'IP address {ip_address} removed from {access_level} list',
        user_id=current_user.id,
        ip_address=get_request_ip(request),
        device_info=str(get_device_info(request)),
        risk_level='low'
    )

    flash(f'IP address {ip_address} deleted successfully!', 'success')
    return redirect(url_for('firewall_blueprint.access_control'))


@blueprint.route('/policies')
@admin_required
def policies():
    """Firewall Policies page with pagination"""
    page = request.args.get('page', 1, type=int)
    policies_list = Policies.query.order_by(Policies.priority).paginate(page=page, per_page=15)
    return render_template('firewall/policies.html', policies=policies_list)


@blueprint.route('/policies/create', methods=['GET', 'POST'])
@admin_required
def create_policy():
    """Create new firewall policy"""
    from apps.firewall.forms import PolicyForm

    form = PolicyForm(request.form)

    if form.validate_on_submit() or (request.method == 'POST' and 'submit' in request.form):
        # Check if policy name already exists
        existing_policy = Policies.query.filter_by(policy_name=form.policy_name.data.strip()).first()
        if existing_policy:
            flash(f'Policy "{form.policy_name.data}" already exists', 'warning')
            return render_template('firewall/create_policy.html', form=form)

        # Validate priority is numeric
        try:
            priority = int(form.priority.data)
        except ValueError:
            flash('Priority must be a numeric value', 'danger')
            return render_template('firewall/create_policy.html', form=form)

        # Create new policy
        policy = Policies(
            policy_name=form.policy_name.data.strip(),
            rule_type=form.rule_type.data,
            protocol=form.protocol.data,
            port_range=form.port_range.data.strip(),
            source_ip=form.source_ip.data.strip() or None,
            destination_ip=form.destination_ip.data.strip() or None,
            action=form.action.data,
            priority=priority,
            created_by=current_user.id,
            is_active=True
        )

        db.session.add(policy)
        db.session.commit()

        # Log audit event
        log_audit_event(
            event_type='policy_change',
            event_description=f'Policy created: {form.policy_name.data} ({form.rule_type.data.upper()}/{form.protocol.data}/{form.port_range.data})',
            user_id=current_user.id,
            ip_address=get_request_ip(request),
            device_info=str(get_device_info(request)),
            risk_level='medium'
        )

        flash(f'Policy "{form.policy_name.data}" created successfully!', 'success')
        return redirect(url_for('firewall_blueprint.policies'))

    return render_template('firewall/create_policy.html', form=form)


@blueprint.route('/policies/<int:policy_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_policy(policy_id):
    """Edit firewall policy"""
    from apps.firewall.forms import PolicyForm

    policy = Policies.query.get_or_404(policy_id)
    form = PolicyForm(request.form)

    if form.validate_on_submit() or (request.method == 'POST' and 'submit' in request.form):
        # Check if new policy name already exists (excluding current policy)
        if form.policy_name.data.strip() != policy.policy_name:
            existing_policy = Policies.query.filter_by(policy_name=form.policy_name.data.strip()).first()
            if existing_policy:
                flash(f'Policy "{form.policy_name.data}" already exists', 'warning')
                return render_template('firewall/edit_policy.html', form=form, policy=policy)

        # Validate priority is numeric
        try:
            priority = int(form.priority.data)
        except ValueError:
            flash('Priority must be a numeric value', 'danger')
            return render_template('firewall/edit_policy.html', form=form, policy=policy)

        # Track changes for audit log
        changes = []
        if form.policy_name.data.strip() != policy.policy_name:
            changes.append(f'Name changed from "{policy.policy_name}" to "{form.policy_name.data.strip()}"')
        if form.rule_type.data != policy.rule_type:
            changes.append(f'Rule type changed from {policy.rule_type} to {form.rule_type.data}')
        if form.protocol.data != policy.protocol:
            changes.append(f'Protocol changed from {policy.protocol} to {form.protocol.data}')
        if form.port_range.data.strip() != policy.port_range:
            changes.append(f'Port range changed from {policy.port_range} to {form.port_range.data.strip()}')
        if form.action.data != policy.action:
            changes.append(f'Action changed from {policy.action} to {form.action.data}')
        if priority != policy.priority:
            changes.append(f'Priority changed from {policy.priority} to {priority}')

        # Update policy
        policy.policy_name = form.policy_name.data.strip()
        policy.rule_type = form.rule_type.data
        policy.protocol = form.protocol.data
        policy.port_range = form.port_range.data.strip()
        policy.source_ip = form.source_ip.data.strip() or None
        policy.destination_ip = form.destination_ip.data.strip() or None
        policy.action = form.action.data
        policy.priority = priority

        db.session.commit()

        # Log audit event if changes were made
        if changes:
            log_audit_event(
                event_type='policy_change',
                event_description=f'Policy "{policy.policy_name}" updated: {", ".join(changes)}',
                user_id=current_user.id,
                ip_address=get_request_ip(request),
                device_info=str(get_device_info(request)),
                risk_level='medium'
            )

        flash(f'Policy "{policy.policy_name}" updated successfully!', 'success')
        return redirect(url_for('firewall_blueprint.policies'))

    if request.method == 'GET':
        form.policy_name.data = policy.policy_name
        form.rule_type.data = policy.rule_type
        form.protocol.data = policy.protocol
        form.port_range.data = policy.port_range
        form.source_ip.data = policy.source_ip
        form.destination_ip.data = policy.destination_ip
        form.action.data = policy.action
        form.priority.data = str(policy.priority)

    return render_template('firewall/edit_policy.html', form=form, policy=policy)


@blueprint.route('/policies/<int:policy_id>/delete', methods=['POST'])
@admin_required
def delete_policy(policy_id):
    """Delete firewall policy"""
    policy = Policies.query.get_or_404(policy_id)
    policy_name = policy.policy_name

    db.session.delete(policy)
    db.session.commit()

    # Log audit event
    log_audit_event(
        event_type='policy_change',
        event_description=f'Policy deleted: {policy_name}',
        user_id=current_user.id,
        ip_address=get_request_ip(request),
        device_info=str(get_device_info(request)),
        risk_level='high'
    )

    flash(f'Policy "{policy_name}" deleted successfully!', 'success')
    return redirect(url_for('firewall_blueprint.policies'))


@blueprint.route('/audit-logs')
@lower_admin_required
def audit_logs():
    """Audit Logs page"""
    page = request.args.get('page', 1, type=int)
    event_type = request.args.get('event_type', '')

    query = AuditLog.query

    # Filter by event type if provided
    if event_type:
        query = query.filter_by(event_type=event_type)

    logs = query.order_by(AuditLog.timestamp.desc()).paginate(page=page, per_page=20)

    return render_template('firewall/audit_logs.html', logs=logs, event_type=event_type)


@blueprint.route('/statistics')
@lower_admin_required
def statistics():
    """Statistics and reports page"""
    return render_template('firewall/statistics.html')


@blueprint.route('/risk-dashboard')
@lower_admin_required
def risk_dashboard():
    """Risk monitoring dashboard for lower-level admins"""
    return render_template('firewall/risk_dashboard.html')


# ============================================================================
# FIREWALL DASHBOARD API ENDPOINTS - For Real-Time Data
# ============================================================================

@blueprint.route('/api/dashboard/metrics', methods=['GET'])
@lower_admin_required
def api_dashboard_metrics():
    """API endpoint for real-time dashboard metrics"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        data = {
            'today_logins': DashboardAnalytics.get_today_login_attempts(),
            'yesterday_logins': DashboardAnalytics.get_yesterday_login_attempts(),
            'today_blocked_ips': DashboardAnalytics.get_today_blocked_ips(),
            'active_whitelist': DashboardAnalytics.get_active_whitelist_entries(),
            'today_alerts': DashboardAnalytics.get_today_security_alerts()
        }
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/hourly-activity', methods=['GET'])
@lower_admin_required
def api_hourly_activity():
    """API endpoint for hourly login activity data"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        days_back = request.args.get('days_back', 0, type=int)
        data = DashboardAnalytics.get_hourly_login_activity(days_back)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/weekly-trends', methods=['GET'])
@lower_admin_required
def api_weekly_trends():
    """API endpoint for weekly access trends"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        data = DashboardAnalytics.get_weekly_access_trends()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/risk-distribution', methods=['GET'])
@lower_admin_required
def api_risk_distribution():
    """API endpoint for risk level distribution"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        data = DashboardAnalytics.get_risk_distribution()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/recent-events', methods=['GET'])
@lower_admin_required
def api_recent_events():
    """API endpoint for recent security events"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        limit = request.args.get('limit', 20, type=int)
        risk_level = request.args.get('risk_level', None)
        data = DashboardAnalytics.get_recent_security_events(limit, risk_level)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/top-blocked-ips', methods=['GET'])
@lower_admin_required
def api_top_blocked_ips():
    """API endpoint for top blocked IPs"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        limit = request.args.get('limit', 10, type=int)
        data = DashboardAnalytics.get_top_blocked_ips(limit)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/top-login-times', methods=['GET'])
@lower_admin_required
def api_top_login_times():
    """API endpoint for top login times"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        data = DashboardAnalytics.get_top_login_times()
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/user-frequency', methods=['GET'])
@lower_admin_required
def api_user_frequency():
    """API endpoint for user login frequency"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        limit = request.args.get('limit', 10, type=int)
        data = DashboardAnalytics.get_user_login_frequency(limit)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/monthly-summary', methods=['GET'])
@lower_admin_required
def api_monthly_summary():
    """API endpoint for monthly summary"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        month_offset = request.args.get('month_offset', 0, type=int)
        data = DashboardAnalytics.get_monthly_summary(month_offset)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@blueprint.route('/api/dashboard/all', methods=['GET'])
@lower_admin_required
def api_all_dashboard_data():
    """API endpoint for all dashboard data at once"""
    from apps.firewall.analytics import DashboardAnalytics

    try:
        days_back = request.args.get('days_back', 0, type=int)
        data = DashboardAnalytics.get_all_dashboard_data(days_back)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
