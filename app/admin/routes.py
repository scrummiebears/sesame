from app.admin import admin
from flask import render_template, url_for, redirect
from app.call_system.models import *

@admin.route("dashboard")
def dashboard():
    admin = None#current_user.admin
    p_pending_admin_1 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 1").all()) or 0
    p_pending_review = len(Proposal.query.filter(Proposal.status == "PENDING REVIEWER").all())
    p_pending_admin_2 = len(Proposal.query.filter(Proposal.status == "PENDING ADMIN 2").all())
    p_approved = len(Proposal.query.filter(Proposal.status == "APPROVED").all())
    p_stats = {"PENDING ADMIN 1": p_pending_admin_1, "PENDING ADMIN 2": p_pending_admin_2, "PENDING REVIEW": p_pending_review, "APPROVED":p_approved}
    return render_template("admin/dashboard.html", user=admin, proposal_stats=p_stats)

@admin.route("new_admin", methods=["GET", "POST"])
def newAdmin():
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
    return render_template("admin/proposals.html")

@admin.route("<proposal>/review")
def review(proposal):
    return render_template("admin/review.html")

@admin.route("<proposal>/deny")
def rejectProposal(propsoal):
    return redirect(url_for(""))

@admin.route("<proposal>/assign_reviewers")
def assignReviewers(proposal):
    return render_template("admin/assign_reviewers")

@admin.route("<proposal>/approve")
def approveProposal(proposal):
    return redirect(url_for(""))



