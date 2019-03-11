from flask import Flask, render_template, flash, redirect, url_for, make_response, request, abort

# Import the extensions used here
from app import db, login_manager, bcrypt
from flask_login import current_user, login_required, logout_user

# Import call_system blueprint
from app.reviewer import reviewer
from app.reviewer.forms import ReviewerForm, ReviewerLoginForm
from app.reviewer.models import Reviewer

import datetime
import config
import string
import random


@reviewer.route("review/<reviewer_id>", methods=["POST", "GET"])
def review(reviewer_id):
    # if there not a reviewer or already submitted a review, render an 403 unauthorised
    reviewer = Reviewer.query.get(reviewer_id) or  abort(404)
    if reviewer.completed == False:
        return "Sorry this review has already been submitted"
    # Get the proposal they are reviewing
    proposal = reviewer.proposal
    form = ReviewerForm()
    # If they have submitted the review form, depending on what button they picked, we update the reviewer object
    if request.method == "POST":
        comments = form.comments.data
        reviewer.comments = comments
        db.session.commit()
        if form.action.data == "Approve":
            return "Accepted, thanks for reviewing"
        elif form.action.data == "Reject":
            return "Rejectd, thanks for reviewing"
        elif form.action.data == "Save":
            return "Saved for later"
    
    return render_template("reviewer/review.html", form=form, reviewer=reviewer, proposal=proposal)

@reviewer.route("accept/<reviewer_id>")
def accept(reviewer_id):
    r = Reviewer.query.get(reviewer_id)
    r.decision = "ACCEPTED"
    r.completed = True
    db.session.commit()
    return redirect("reviewer.login")

@reviewer.route("reject/<reviewe_idr>")
def reject(reviewer_id):
    r = Reviewer.query.get(reviewer_id)
    r.decision = "REJECTED"
    r.completed = True
    db.session.commit()
    return redirect("reviewer.login")
    

@reviewer.route("save/<reviewer_id>")
def save(reviewer_id):
    r = Reviewer.query.get(reviewer_id)
    return redirect("reviewer.login")

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
