from app.admin import admin
from app.admin.models import Admin
from flask import render_template, url_for, redirect, request, abort, flash
from app.call_system.models import Call, Proposal
from .forms import *
from flask_login import current_user, login_required
from app.profile.models import Researcher
from app.auth.models import User
from app.reviewer.models import Reviewer
from app import db, bcrypt, mail
import json
import string
import random
from smtplib import SMTPAuthenticationError, SMTPRecipientsRefused
from flask_mail import Message

@admin.route("dashboard")
@login_required
def dashboard():
    if current_user.role != "ADMIN":
        abort(403)
    admin = current_user.admin
    p_pending_admin_1 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 1").all())
    p_pending_review = len(Proposal.query.filter(Proposal.status == "PENDING REVIEWER").all())
    p_pending_admin_2 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 2").all())
    p_approved = len(Proposal.query.filter(Proposal.status == "APPROVED").all())
    p_stats = {"PENDING ADMIN 1": p_pending_admin_1, "PENDING ADMIN 2": p_pending_admin_2, "PENDING REVIEW": p_pending_review, "APPROVED":p_approved}
    return render_template("admin/dashboard.html", user=admin, proposal_stats=p_stats)

@admin.route("new_admin", methods=["GET", "POST"])
@login_required
def newAdmin():
    if current_user.role != "ADMIN":
        abort(403)
    form = NewAdminForm()
    if request.method == "POST" and form.validate:

        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(form.email.data, password, "ADMIN")
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()

        new_admin = Admin(user_id=user.id, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(new_admin)
        db.session.commit()
        flash("New admin created - %s %s" % (form.first_name.data, form.last_name.data))
        return redirect(url_for("admin.newAdmin"))
    admin = current_user.admin
    return render_template("admin/new_admin.html", user=admin, form=form)

@admin.route("call/<call>/proposals")
@login_required
def proposals(call):
    if current_user.role != "ADMIN":
        abort(403)
    proposals = Proposal.query.filter(Proposal.call_id == call).all()

    admin = current_user.admin
    return render_template("admin/proposals.html", user=admin, proposals=proposals)

@admin.route("proposal/<proposal_id>/review")
@login_required
def review(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    proposal = Proposal.query.get(proposal_id) or abort(404)
    admin = current_user.admin
    return render_template("admin/review.html", user=admin, proposal=proposal)

@admin.route("proposal/<proposal_id>/review_final")
@login_required
def reviewFinal(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    admin = current_user.admin
    proposal = Proposal.query.get(proposal_id) or abort(404)

    user = proposal.researcher.user
    email = user.email

    return render_template("admin/review_final.html", proposal=proposal,user=admin)

@admin.route("proposal/<proposal_id>/deny")
@login_required
def rejectProposal(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    proposal = Proposal.query.get(proposal_id)
    proposal.query.update({"status": "REJECTED"})
    flash("Proposal has been rejected")

    user = proposal.researcher.user
    email = user.email
    try:
        msg = Message("Proposal ID: " + proposal.id + " Stage 1 of 3 REJECTED", recipients=[email])
        msg.body = """Dear %s,<br>
        We regret to inform you that your proposal entitled <i>%s</i> has been rejected for funding by the SFI.<br>
        """ % (user.first_name, proposal.title)
        msg.html = msg.body
        mail.send(msg)
    except (SMTPAuthenticationError):
        flash("There seems to be something wrong with our mail service right now")
    return redirect(url_for("admin.dashboard"))

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@admin.route("proposal/<proposal_id>/assign_reviewers", methods=["GET", "POST"])
@login_required
def assignReviewers(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    form = AssignReviewersForm()
    proposal = Proposal.query.get(proposal_id) or abort(404)
    if request.method == "POST" and form.validate:
        emails = form.emails.data
        reviewer_emails = emails.replace(" ","")
        review_emails = emails.split(",")

        # create new reviewers
        for email in review_emails:
            reviewer = Reviewer(email=email, proposal_id=proposal_id)
            db.session.add(reviewer)
            db.session.commit()

            r_id = Reviewer.query.filter(Reviewer.email == email).first().id
            print("**** " + url_for("reviewer.review", reviewer_id=r_id) +"*****")
            try:
                msg = Message("Proposal Review Request", recipients=[email])
                msg.body = """You have been selected to review a proposal.<br>
                Please follow this link to view it - %s""" % (url_for("reviewer.review", reviewer_id=r_id))
                msg.html = msg.body
                mail.send(msg)
            except (SMTPAuthenticationError, SMTPRecipientsRefused):
                flash("There seems to be an issue with our email services. No emails were sent.")

        proposal.status = "PENDING REVIEWER"
        db.session.commit()
        flash("Proposal has been sent out for review")

        user = proposal.researcher.user
        email = user.email
        try:
            msg = Message("Proposal ID: " + str(proposal.id) + " Stage 2 of 3 PENDING REVIEWER APPROVAL", recipients=[email])
            msg.body = """Dear %s,<br>
            This email is to inform you that your proposal entitled <i>%s</i>
            has been passed onto a reviewer to adjudicate.<br>
            If approved by this reviewer, it will be passed to the 3rd and final step of adjudication.
            """ % (user.researcher.first_name, proposal.title)
            msg.html = msg.body
            mail.send(msg)
        except (SMTPAuthenticationError):
            flash("There seems to be something wron with our mail services.")
        except (SMTPRecipientsRefused):
            pass
        return redirect(url_for("admin.dashboard"))

    researchers = Researcher.query.all()
    data = []
    for r in researchers:
        data.append(r.user.email)
    return render_template("admin/assign_reviewers.html", form=form, proposal=proposal, r_emails=json.dumps(data))

@admin.route("proposal/<proposal_id>/approve")
@login_required
def approveProposal(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    proposal = Proposal.query.get(proposal_id) or abort(404)
    proposal.status = "APPROVED"
    db.session.commit()
    admin = current_user.admin
    flash("Proposal has been approved")

    try:
        msg = Message("Proposal ID: " + proposal.id + " Stage 3 of 3 APPROVED", recipients=[email])
        msg.body = """Dear %s,<br>
        Congratulations, your proposal entitled <i>%s</i> has been fully approved for funding by the SFI!<br>
        """ % (user.first_name, proposal.title)
        msg.html = msg.body
        mail.send(msg)
    except (SMTPAuthenticationError):
        flash("There seems to be something wron with our mail services.")
    except (SMTPRecipientsRefused):
        pass
    return redirect(url_for("admin.dashboard"))

@admin.route("calls/all_calls")
@login_required
def allCalls():
    if current_user.role != "ADMIN":
        abort(403)
    user = current_user.admin
    calls = {}
    calls["PUBLISHED"] = Call.query.filter(Call.status=="PUBLISHED").order_by(Call.date_published).all()
    calls["FINISHED"] = Call.query.filter(Call.status=="FINISHED").order_by(Call.date_published).all()
    return render_template("admin/all_calls.html", user=admin, calls=calls)
