import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
# from flask_socketio import SocketIO 

from pkg.models import db 
from pkg.routes import register_blueprints

csrf = CSRFProtect()
migrate = Migrate()
mail = Mail()
# socketio = SocketIO()

def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder='static', template_folder='templates')
    
    app.config.from_pyfile("config.py")

    app.config['UPLOAD_FOLDER_VIDEO'] = os.path.join(app.root_path, 'static/uploads/video')
    app.config['UPLOAD_FOLDER_IMAGE'] = os.path.join(app.root_path, 'static/uploads/image')

    os.makedirs(app.config['UPLOAD_FOLDER_VIDEO'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_IMAGE'], exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # TEMPORARY ROUTE TO RUN MIGRATIONS (DELETE AFTER USE)
    @app.route('/run-migrations')
    def run_migrations():
        from flask_migrate import upgrade
        try:
            upgrade()
            return "✅ Database migrated successfully!"
        except Exception as e:
            return f"❌ Migration failed: {str(e)}"

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app

