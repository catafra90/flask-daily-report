from flask import Flask

# Import blueprints
from app.clients.routes import clients_bp
from app.daily_report.routes import daily_report_bp
from app.charts.routes import charts_bp
from app.home.routes import home_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'Figurella2025'

    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(daily_report_bp, url_prefix='/daily_report')
    app.register_blueprint(charts_bp)

    # ✅ Debug route list at startup
    print("\n📦 Registered Routes:")
    with app.app_context():
        for rule in app.url_map.iter_rules():
            print(f"🔗 {rule.endpoint} --> {rule.rule}")
    print()

    return app
