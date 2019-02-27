# Import Flask
from flask import Flask, render_template, flash, redirect, url_for

# Import the extensions used here
from app import db, bcrypt, login_manager, mail
from app.auth.forms import LoginForm, RegistrationForm, TeamForm
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from flask_mail import Message

# Import auth blueprint
from app.auth import auth
from app.call_system import call_system

# Import the Models used

from app.profile.models import *
from app.call_system.models import *



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
        flash("Registration unsuccesfull")
        return render_template("auth/register.html", form=form)
    return render_template("auth/register.html", form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # return "you are logged in"
        redirect(url_for('auth.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Checks email instead of username
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.pwd_hash,form.password.data):
            #If we decide to implement a remember me function
            login_user(user)#, remember=form.remember.data)
            flash("You are now logged in")
            return redirect(url_for('auth.home'))
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

@auth.route("/CreateNewAdmin")
@login_required
def CreateNewAdmin():
    if current_user.role == "ADMIN":
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if not user:

                password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                user = User(form.email.data, password, "ADMIN")
                db.session.add(user)
                db.session.commit()

                user = User.query.filter_by(email=form.email.data).first()
                admin = Admin(user_id=user.id, first_name=form.first_name.data, last_name=form.last_name.data,
                                        job_title=form.job_title.data, prefix=form.prefix.data, suffix=form.suffix.data,
                                        phone=form.phone.data, phone_ext=form.phone_ext.data, orcid=form.orcid.data)
                db.session.add(admin)
                # education = Education(user_id=user.id, degree=None, field_of_study=None, institution=None,
                #                         location=None,degree_award_year=None)
                # db.session.add(education)
                db.session.commit()

                flash("Admin account has been created. You can now login")
                return redirect(url_for("auth.login"))
            else:
                flash("An account already exists with this email address. Please login.")
        return render_template("auth/register.html", form=form)

@auth.route("/teams", methods=['GET','POST'])

def team_form():
    if current_user.is_authenticated:
        form = TeamForm()
        researcher_id = current_user.id
        if form.validate_on_submit():
            teamMem = TeamMembers(start_date = form.start_date.data, end_date = form.end_date.data, name = form.name.data,position = form.position.data, primary_attribute = form.grant_number.data,researcher_id = researcher_id)
            db.session.add(teamMem)
            db.session.commit()
            flash("Your team member has been added!") 
        members = TeamMembers.query.filter_by(researcher_id = researcher_id).all()
        for member in members:
            print(member.name)
        return render_template('auth/team_form.html',title="Enter Team", form=form, members=members)
    else:
        return redirect(url_for("auth.login"))


@auth.route("/profile",methods=['GET'])
@login_required
def profile(): 
    user = Researcher.query.filter_by(user_id=current_user.id).first()
    user_education = Education.query.filter_by(researcher_id=current_user.id).first()
    user_employment = Employment.query.filter_by(researcher_id=current_user.id).first()
    user_membership = Membership.query.filter_by(researcher_id=current_user.id).first()
    user_award = Award.query.filter_by(researcher_id=current_user.id).first()
    user_funding = FundingDiversification.query.filter_by(researcher_id=current_user.id).first()
    user_team = TeamMember.query.filter_by(researcher_id=current_user.id).first()
    user_impact = Impact.query.filter_by(researcher_id=current_user.id).first()
    user_innovation = Innovation.query.filter_by(researcher_id=current_user.id).first()
    user_publication = Publication.query.filter_by(researcher_id=current_user.id).first()
    user_presentation = Presentation.query.filter_by(researcher_id=current_user.id).first()
    user_academicCollabaration = AcademicCollabaration.query.filter_by(researcher_id=current_user.id).first()
    user_nonAcademicCollabaration = NonAcademicCollabaration.query.filter_by(researcher_id=current_user.id).first()
    user_confrence = Confrence.query.filter_by(researcher_id=current_user.id).first()
    user_communicationOverview = CommunicationOverview.query.filter_by(researcher_id=current_user.id).first()
    user_sfiFunding = SFIFundingRatio.query.filter_by(researcher_id=current_user.id).first()
    user_educationAndPublicEngagement = EducaionAndPublicEngagement.query.filter_by(researcher_id=current_user.id).first()
    return render_template('auth/account.html', title ="Profile",user=user,user_education=user_education,user_employment=user_employment,user_membership=user_membership,user_award=user_award,user_funding=user_funding,user_team=user_team,user_impact=user_impact,user_innovation=user_innovation,user_publication=user_publication,user_presentation=user_presentation,user_academicCollabaration=user_academicCollabaration,user_nonAcademicCollabaration=user_nonAcademicCollabaration,user_confrence=user_confrence,user_communicationOverview=user_communicationOverview,user_sfiFundingq=user_sfiFunding,user_educationAndPublicEngagement=user_educationAndPublicEngagement)


@auth.route("/stats",methods=['GET'])
@login_required
def proposals():
    #creates an array of all proposals from this reasearcher
    user_proposals = Proposal.query.filter_by(researcher_id=current_user.id).all()
    approved = []
    rejected = []
    pending_admin = []
    pending_review = []
    edit=[]

    approvedNum=0
    rejectedNum=0
    pending_adminNum=0
    pending_reviewNum=0
    editNum=0
    for prop in user_proposals:
        if prop.approved == "APPROVED":
            approved.append(prop)
            approvedNum += 1
        elif prop.approved == "REJECTED":
            rejected.append(prop)
            rejectedNum += 1
        elif prop.approved == "EDIT":
            rejected.append(prop)
            rejectedNum += 1
        elif prop.approved == "PENDING ADMIN":
            rejected.append(prop)
            rejectedNum += 1
        elif prop.approved == "PENDING REVIEW":
            rejected.append(prop)
            rejectedNum += 1
    return render_template('auth/home.html',title="Statistics",approved=approved,pending_reviewNum=pending_reviewNum,editNum=editNum,pending_adminNum=pending_adminNum,edit=edit,rejected=rejected,pending_review=pending_review,pending_admin=pending_admin,approvedNum=approvedNum,rejectedNum=rejectedNum)




@auth.route("/createAdmin",methods=["GET","POST"])
def createAdmin():
    password = bcrypt.generate_password_hash("password").decode("utf-8")
    user = User("admin",password, "ADMIN")
    db.session.add(user)
    db.session.commit()
    flash("Admin made")
    return redirect(url_for("auth.login"))