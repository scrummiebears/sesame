from app.admin import admin
from flask import render_template, url_for, redirect, request, abort
from app.call_system.models import Call, Proposal
from .forms import *
from flask_login import current_user, login_required
from app.profile.models import Researcher
import json

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
    form = NewAdminForm
    if request.method == "POST" and form.validate:

        password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(form.email.data, password, "ADMIN")
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email=form.email.data).first()

        new_admin = Admin(user_id=user.id, first_name=form.fisrt_name.data, last_name=form.last_name.data)
        db.session.add(new_admin)
        db.session.commit()
        flash("New admin created - %s %s" % (form.first_name.data, form.last_name.data))
        return redirect(url_for(admin.newAdmin))
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

@admin.route("proposal/<proposal_id>/deny")
@login_required
def rejectProposal(propsoal_id):
    if current_user.role != "ADMIN":
        abort(403)
    proposal = Proposal.query.get(proposal_id)
    proposal.query.update({"status": "REJECTED"})
    flash("Proposal has been rejected")
    return redirect(url_for("admin.dashboard"))

@admin.route("proposal/<proposal_id>/assign_reviewers", methods=["GET", "POST"])
@login_required
def assignReviewers(proposal_id):
    if current_user.role != "ADMIN":
        abort(403)
    form = AssignReviewersForm()
    proposal = Proposal.query.get(proposal_id) or abort(404)
    if request.method == "POST" and form.validate:
        reviewer_emails = emails.replace(" ","")
        review_emails = emails.split(",")
        
        # create new reviewers
        for email in reviewer_emails:
            researcher = Researcher.query.filter_by(email=email)
            db.session.add(reviewer(researcher_id=researcher.user_id, proposal_id=proposal_id))
            

        proposal.status = "PENDING REVIEWER"
        db.session.commit()
        flash("Proposal has been sent out for review")
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