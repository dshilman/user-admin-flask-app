from datetime import datetime

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
from . import routes_bp


@routes_bp.route('/')
def index():
    return redirect('auth/login')