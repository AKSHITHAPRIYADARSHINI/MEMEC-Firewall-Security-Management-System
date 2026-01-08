# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.decorators import admin_required
from apps.authentication.util import verify_pass


@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('authentication_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()
        
        return render_template('accounts/register.html',
                               msg='Account created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Admin Routes

@blueprint.route('/admin/users', methods=['GET'])
@admin_required
def admin_users_list():
    page = request.args.get('page', 1, type=int)
    users = Users.query.paginate(page=page, per_page=10)
    return render_template('admin/users_list.html', users=users)


@blueprint.route('/admin/users/create', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    form = CreateAccountForm(request.form)
    if 'register' in request.form:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check username exists
        user = Users.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', 'danger')
            return render_template('admin/create_user.html', form=form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', 'danger')
            return render_template('admin/create_user.html', form=form)

        # Create new user
        user = Users(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        flash('User created successfully', 'success')
        return redirect(url_for('authentication_blueprint.admin_users_list'))

    return render_template('admin/create_user.html', form=form)


@blueprint.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_user(user_id):
    user = Users.query.get_or_404(user_id)
    form = CreateAccountForm(request.form)

    if 'register' in request.form:
        user.username = request.form['username']
        user.email = request.form['email']
        if request.form.get('password'):
            user.password = request.form['password']

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('authentication_blueprint.admin_users_list'))

    return render_template('admin/edit_user.html', form=form, user=user)


@blueprint.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete yourself', 'danger')
        return redirect(url_for('authentication_blueprint.admin_users_list'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('authentication_blueprint.admin_users_list'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
