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
        nav.Item('Calls For Proposals', 'call_system.view_all_calls'),
        nav.Item('Register', 'auth.register'),
        nav.Item('Login', 'auth.login')
    ])

    # Navbar for logged in users (researchers)
    nav.Bar('user', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Profile', 'profile.view'),
        nav.Item('Calls For Proposals', 'call_system.view_all_calls'),
        nav.Item('Logout', 'auth.logout')
    ])

    # Navbar for logged in admins
    nav.Bar('admin', [
        nav.Item('Home', 'admin.dashboard'),
        nav.Item('Calls For Proposals', 'admin.allCalls'),
        nav.Item('Make CFP', 'call_system.make_call'),
        nav.Item('Logout', 'auth.logout')
    ])

    # Navbar for logged in reviewers
    nav.Bar('reviewer', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Calls For Proposals', 'call_system.view_all_calls'),
        #nav.Item('Proposal Submissions', 'call_system.view_proposal_submissions'),
        nav.Item('Logout', 'auth.logout')
    ])
    nav.Bar('researcher', [
        nav.Item('Home', 'auth.home'),
        nav.Item('Calls For Proposals', 'call_system.view_all_calls'),
        nav.Item('Proposal Submissions', 'call_system.researcher_view_initial_pending_submissions'),
        nav.Item('Logout', 'auth.logout')
    ])

    from app.auth import auth
    app.register_blueprint(auth, url_prefix="/auth/")
    from app.profile import profile
    app.register_blueprint(profile, url_prefix="/profile/")
    from app.call_system import call_system
    app.register_blueprint(call_system, url_prefix="/calls/")
    from app.admin import admin
    app.register_blueprint(admin, url_prefix="/admin/")
    from app.reviewer import reviewer
    app.register_blueprint(reviewer, url_prefix="/review/")

    with app.app_context():
        db.create_all()

    configure_uploads(app, programme_docs)

    from app import commands
    app.cli.add_command(commands.db_cli)
    app.cli.add_command(commands.user_cli)



    return app
