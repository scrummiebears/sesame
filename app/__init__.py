# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlcheny
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_navigation import Navigation
from flask_uploads import UploadSet, ALL, configure_uploads

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

programme_docs = UploadSet("programmeDocs", ALL)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    nav = Navigation(app)

    # Navbar visible to all
    nav.Bar('top', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Register', 'auth.register'),
        nav.Item('Login', 'auth.login')
    ])

    # Navbar for logged in users (researchers)
    nav.Bar('user', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Profile', 'auth.home'),
        nav.Item('Logout', 'auth.logout')
    ])

    # Navbar for logged in admins
    nav.Bar('admin', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Make CFP', 'call_system.make_call'),
        nav.Item('Logout', 'auth.logout')
    ])

    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth/")
    from app.profile import profile
    app.register_blueprint(profile)
    from app.call_system import call_system
    app.register_blueprint(call_system, url_prefix="/calls/")

    with app.app_context():
        db.create_all()

    configure_uploads(app, programme_docs)

    from app import commands
    app.cli.add_command(commands.flushDb)
    app.cli.add_command(commands.populateDb)
    

    return app