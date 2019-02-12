# Import Flask
from flask import Flask, render_template, flash, redirect, url_for

# Import the extensions used here
from app import db, bcrypt, login_manager, mail
from app.auth.forms import LoginForm, RegistrationForm, TeamForm
from flask_login import UserMixin, current_user, login_user, logout_user
from flask_mail import Message

# Import auth blueprint
from app.auth import auth

# Import the Models used
from app.profile.models import Researcher, Teams, TeamMembers
from app.profile.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route("/")
@auth.route("/home")
def home():
    if current_user.is_authenticated:
        navs = ["Teams", "Query", "Log Out",]
    else:
        navs = ["Login", "Register"]
    return render_template("auth/home.html", navs=navs)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:

            password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(form.email.data, password, "RESEARCHER")
            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(email=form.email.data).first()
            researcher = Researcher(user_id=user.id, first_name=form.first_name.data, last_name=form.last_name.data,
                                     job_title=form.job_title.data, prefix=form.prefix.data, suffix=form.suffix.data,
                                     phone=form.phone.data, phone_ext=form.phone_ext.data, orcid=form.orcid.data)
            db.session.add(researcher)
            # education = Education(user_id=user.id, degree=None, field_of_study=None, institution=None,
            #                         location=None,degree_award_year=None)
            # db.session.add(education)
            db.session.commit()

            flash("Your account has been created. You can now login")
            return redirect(url_for("auth.login"))
        else:
            flash("An account already exists with this email address. Please login.")
    return render_template("auth/register.html", form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return "you are logged in"#redirect(url_for(''))
    form = LoginForm()
    if form.validate_on_submit():
        #Checks email instead of username
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.pwd_hash,form.password.data):
            #If we decide to implement a remember me function
            login_user(user)#, remember=form.remember.data)
            flash("You are now logged in")
            return redirect(url_for('auth.login'))
        else:
            flash('Login Unsuccessful. Please check e-mail and password')
    return render_template('auth/login.html',title='Login', form=form)

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/query")
def query():
    users = User.query.all()
    return str(len(users))

@auth.route("/call-for-proposals", methods=['GET', 'POST'])
def call_for_proposals():
    form = CallForProposalsForm()
    if form.validate_on_submit():
        emails = db.session.query(User.email)
        for email, in emails:
            msg = Message(form.proposal_name.data + " - Call for Proposal", recipients=[email])
            msg.body = "testing"
            msg.html = "<b>testing</b>"
            mail.send(msg)

    return render_template("auth/proposals.html", title="Call For Proposals", form=form)

@auth.route("/teams")
def team_form():
    form = TeamForm()
    if form.validate_on_submit():
        teamMem = TeamMembers(form.start_date.data,form.end_date.data,form.name.data,form.position.data,form.grant_number.data)
        db.session.add(teamMem)
        db.session.commit()
        flash("Your team member has been added!")
    members = TeamMembers.query.all()
    #teams = Teams.query.all()
    #for team in teams:
        #if team[1] == researcher's primary attribute
    return render_template('auth/team_form.html',title="Enter Team", form=form, members=members) #
