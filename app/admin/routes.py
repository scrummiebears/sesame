from app.admin import admin
from flask import render_template, url_for, redirect, request, abort
from app.call_system.models import *
from .forms import *
from flask_login import current_user

@admin.route("dashboard")
def dashboard():
    if current_user.admin is None:
        abort(403)
    admin = None#current_user.admin
    p_pending_admin_1 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 1").all())
    p_pending_review = len(Proposal.query.filter(Proposal.status == "PENDING REVIEWER").all())
    p_pending_admin_2 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 2").all())
    p_approved = len(Proposal.query.filter(Proposal.status == "APPROVED").all())
    p_stats = {"PENDING ADMIN 1": p_pending_admin_1, "PENDING ADMIN 2": p_pending_admin_2, "PENDING REVIEW": p_pending_review, "APPROVED":p_approved}
    return render_template("admin/dashboard.html", user=admin, proposal_stats=p_stats)

@admin.route("new_admin", methods=["GET", "POST"])
def newAdmin():
    if current_user.admin is None:
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

@admin.route("<call>/proposals")
def proposals(call):
    if current_user.admin is None:
        abort(403)
    proposals = Proposal.query.filter(Proposal.call_id == call).all()
    admin = current_user.admin
    return render_template("admin/proposals.html", user=admin, proposals=proposals)

@admin.route("<proposal_id>/review")
def review(proposal):
    if current_user.admin is None:
        abort(403)
    proposal = Proposal.query.get(proposal_id) or abort(404)
    admin = current_user.admin
    return render_template("admin/review.html", user=admin, proposal=proposal)

@admin.route("<proposal_id>/deny")
def rejectProposal(propsoal_id):
    if current_user.admin is None:
        abort(403)
    proposal = Proposal.query.get(proposal_id)
    proposal.query.update({"status": "REJECTED"})
    flash("Proposal has been rejected")
    return redirect(url_for(""))

@admin.route("<proposal_id>/assign_reviewers", method=["GET", "POST"])
def assignReviewers(proposal_id):
    if current_user.admin is None:
        abort(403)
    form = AssignReviewersForm()
    proposal = Proposal.query.get(proposal_id) or abort(404)
    if method == "POST" and form.validate:
        reviewer_emails = emails.replace(" ","")
        review_emails = emails.split(",")
        
        # create new reviewers

        proposal.status = "PENDING REVIEWER"
        db.session.commit()
        flash("Proposal has been sent out for review")
        return redirect(url_for("admin.dashboard")) 
    
    return render_template("admin/assign_reviewers", form=form, proposal=proposal)

@admin.route("<proposal_id>/approve")
def approveProposal(proposal_id):
    if current_user.admin is None:
        abort(403)
    proposal = Proposal.query.get(proposal_id) or abort(404)
    proposal.status = "APPROVED"
    db.session.commit()
    admin = current_user.admin
    flash("Proposal has been approved")
    return redirect(url_for("admin.dashboard"))



