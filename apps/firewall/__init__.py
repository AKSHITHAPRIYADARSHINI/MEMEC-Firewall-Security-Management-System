# -*- encoding: utf-8 -*-
"""
Firewall Management Module
"""

from flask import Blueprint

blueprint = Blueprint(
    'firewall_blueprint',
    __name__,
    url_prefix='/firewall',
    template_folder='templates',
    static_folder='static'
)

from apps.firewall import routes
