# Import Flask
from flask import Flask, render_template, flash, redirect, url_for, make_response, request, abort
from werkzeug import secure_filename
import os
# Import the extensions used here
from app import db, login_manager, mail
import app.call_system.forms
from flask_login import current_user, login_required
from flask_mail import Message
from app import programme_docs, proposal_templates

# Import call_system blueprint
from app.call_system import call_system

# Import the Models used
from app.call_system.models import Call, Proposal
from app.auth.models import User

# Import the forms
from app.call_system.forms import CallForm, ProposalForm
import datetime
import config

from smtplib import SMTPRecipientsRefused

@call_system.route("/make_call", methods=["GET", "POST"])
@login_required
def make_call():
    if current_user.role != "ADMIN":
        abort(403)

    form = CallForm()
    if form.is_submitted():
        if form.validate():

            filename = proposal_templates.save(request.files["proposal_template"])
            url = proposal_templates.url(filename)
            expected_start_date = datetime.strptime(form.deadline.data, "%Y-%m-%d")
            deadline = datetime.strptime(form.deadline.data, "%Y-%m-%d")
            call = Call(admin_id=current_user.id, information=form.information.data,
                        target_group=form.target_group.data, proposal_template_filename=filename, proposal_template_url=url,
                        deadline=deadline, eligibility_criteria=form.eligibility_criteria.data, duration_of_award=form.duration_of_award.data, reporting_guidelines=form.reporting_guidelines.data, expected_start_date=expected_start_date, status="PUBLISHED")
            db.session.add(call)
            db.session.commit()

            emails = db.session.query(User.email)
            for email, in emails:
                try:
                    msg = Message("Call for Proposal", recipients=[email])
                    msg.body = """<h3>Call for Proposal</h3><br>
                    Dear Researcher,<br>
                    This is a notification of a new call for proposal issued by the SFI.<br>
                    <b>Information:</b><br>%s<br>
                    <b>Target Group:</b><br>%s<br>
                    <b>Deadline:</b><br>%s<br>
                    <b>Eligibility Crteria:</b><br>%s<br>
                    """ % (form.information.data, form.target_group.data,
                    form.deadline.data, form.eligibility_criteria.data)
                    msg.html = msg.body
                    pdf = form.proposal_template.data 
                    filename = secure_filename(pdf.filename)
                    
                    pdf.save(os.path.join(
                        config.UPLOAD_FOLDER, filename))
                    
                    msg.attach(filename, 'application/pdf', pdf.read())
                    mail.send(msg)
                except (SMTPRecipientsRefused):
                    pass

            flash("Call for funding has been published")
            return redirect(url_for("admin.allCalls"))

        else:
            flash("Unable to publish call - Please enter details in all fields")
            return render_template("call_system/make_call.html", form=form)
    else:
        return render_template("call_system/make_call.html", form=form)



@call_system.route("/apply/<call_id>", methods=["GET", "POST"])
@login_required
def apply(call_id):
    """The form for grant application

    The <call_id> is the call you are applying to.
    All fields are required. Bootstrap wont show the options field for some reason.
    """
    if current_user.role != "RESEARCHER":
        abort(403)
    call = Call.query.get(call_id) or abort(404)
    form = ProposalForm()
    if request.method == "POST" and form.validate:
        filename = programme_docs.save(request.files["programme_documents"])
        url = programme_docs.url(filename)
        proposal = Proposal(call_id=call_id, researcher_id=current_user.id, title=form.title.data, duration=form.duration.data, nrp=form.nrp.data,
                            legal_remit=form.legal_remit.data, ethical_issues=form.ethical_issues.data,
                            location=form.location.data, co_applicants=form.co_applicants.data,
                            collaborators=form.collaborators.data, scientific_abstract=form.scientific_abstract.data,
                            lay_abstract=form.lay_abstract.data, programme_docs_filename=filename,
                            programme_docs_url=url)
        db.session.add(proposal)
        db.session.commit()
        flash("Your proposal has been submitted")

        user = current_user

        email = user.email
        try:
            msg = Message("Submission of Proposal ID " + proposal.id + " STEP 1 OF 3", recipients=[email])
            msg.body = """Dear %s,<br>
            This is a confirmation of your submission of your proposal entitled <i>%s</i> on SFI's <i>Sesame</i> portal.<br>
            Here is a summary of the information of your submitted proposal:<br>
            Title: <b>%s</b><br>
            Duration: <b>%s</b><br>
            National Research Priority: <b>%s</b><br>
            Legal Remit: <b>%s</b><br>
            Location: <b>%s</b><br>
            Programme Docs Filename: <b>%s</b><br>
            You will be notified of any change of status to your submission.""" % (user.first_name, proposal.title,
            proposal.title, proposal.duration, proposal.nrp, proposal.legal_remit,
            proposal.location, proposal.programme_docs_filename)
            msg.html = msg.body
            mail.send(msg)
        except (SMTPRecipientsRefused):
            pass
        return redirect(url_for(".apply", call_id=call.id))
    return render_template("call_system/apply.html", form=form, call=call)

@call_system.route("/<int:call_id>/view")
def view_call(call_id):
    call = Call.query.filter_by(id=call_id).first()
    # flash("Reading more about call #" + str(call_id))
    return render_template("call_system/view_call.html", call=call)

from datetime import datetime
@call_system.route("/all_cfp")
def view_all_calls():
    calls = Call.query.order_by(Call.deadline.desc()).all();
    if len(calls) == 0:
        flash("No calls to display")
    return render_template("call_system/view_all_calls.html", calls=calls)

@call_system.route("/researcher_view_all_submissions/<section>")
@login_required
def viewSection(section):
    """Handles viewing specific proposal statuses"""
    pendingSubmissions = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.status.contains("PENDING")).all()
    approvedSubmissions = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.status=="APPROVED").all()
    editSubmissions = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.status=="EDIT").all()
    rejectedSubmissions = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.status=="REJECTED").all()

    sections = {"pendingSubmissions":pendingSubmissions, "approvedSubmissions":approvedSubmissions, "rejectedSubmissions":rejectedSubmissions, "editSubmissions":editSubmissions}
    headings = {"pendingSubmissions":"Pending Proposals", "approvedSubmissions":"Approved Proposals","rejectedSubmissions":"Rejected Proposals", "editSubmissions":"Edit Proposals"}

    if section not in sections:
        abort(404)

    data = sections[section]
    heading = headings[section]
    return render_template("call_system/researcher_view_all_submissions.html", section=section, data=data, heading=heading)

@call_system.route("/researcher_view_initial_pending_submissions")
@login_required
def researcher_view_initial_pending_submissions():
    """Generates the initial view of proposal submissions with the pending proposals"""
    if current_user.role != "RESEARCHER":
        abort(403)
    pendingSubmissions = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.status.contains("PENDING")).all()
    return render_template("call_system/researcher_view_initial_pending_submissions.html",data=pendingSubmissions)

@call_system.route("/researcher_view_submission/<submission_id>")
@login_required
def researcher_view_submission(submission_id):
    """Views a specific proposal submission made by a researcher"""
    if current_user.role != "RESEARCHER":
        abort(403)

    submission = Proposal.query.filter_by(researcher_id=current_user.id).filter(Proposal.id).first()
    return render_template("call_system/researcher_view_submission.html", submission=submission)
