from flask import Blueprint, render_template
from app import render
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    days_data = render.get_timeline_data()
    return render_template('timeline.html', days_data=days_data, title="Dashboard")