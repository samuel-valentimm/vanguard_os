from flask import Blueprint, render_template
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    metrics = DashboardService.get_dashboard_metrics()
    return render_template('dashboard/dashboard.html', metrics=metrics)