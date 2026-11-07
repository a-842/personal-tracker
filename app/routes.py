from flask import Blueprint, render_template
from app import render
import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    date = datetime.date(2026, 11, 6)
    day_data = render.get_timeline_data_date(date)
    return render_template('timeline.html', date=date, day_data=day_data, title="Dashboard")