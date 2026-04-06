from flask import Flask
import os
from extensions import db, bcrypt, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexus.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register user_loader directly here
    @login_manager.user_loader
    def load_user(user_id):
        from models.models import User
        return User.query.get(int(user_id))

    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.chat import chat_bp
    from routes.upload import upload_bp
    from routes.history import history_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(history_bp)

    with app.app_context():
        # Ensure models are imported so db.create_all() works
        import models.models
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

