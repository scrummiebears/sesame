# Import Flask
from flask import Flask, render_template, flash, redirect, url_for, make_response, request
from werkzeug import secure_filename
import os
# Import the extensions used here
from app import db, login_manager, mail
import app.call_system.forms
from flask_login import current_user, login_required
from flask_mail import Message
from app import programme_docs

# Import call_system blueprint
from app.call_system import call_system

# Import the Models used
from app.call_system.models import Call
from app.auth.models import User

# Import the forms
from app.call_system.forms import CallForm, ProposalForm
import datetime
import config

@call_system.route("/make_call", methods=["GET", "POST"])
@login_required
def make_call():
    if current_user.role != "ADMIN":
        return redirect(url_for("auth.login"))

    form = CallForm()
    if form.is_submitted():
        if form.validate():
            # render a new page which confirms the call??
            # two step process like asking a question on stack overflow

            # check they are admin
            # Obtain all info, make a new Call object,
            # Render a new page that is a confirmation of input
            # or simply insert the call into the database
            #
            # Publishing stuff may also be trigered? its a backgrond job?
            call = Call(published_by=current_user.id, information=form.information.data,
                        target_group=form.target_group.data, proposal_template=form.proposal_template.data,
                        deadline=form.deadline.data)
            db.session.add(call)
            db.session.commit()

            emails = db.session.query(User.email)

            for email, in emails:
                msg = Message("Call for Proposal", recipients=[email])
                msg.body = "Proposal Information:\n" + form.information.data + "\nDeadline: " + form.deadline.data.strftime('%m/%d/%Y')

                pdf = form.file.data
                filename = secure_filename(pdf.filename)

                pdf.save(os.path.join(
                    config.UPLOAD_FOLDER, filename))

                msg.attach(filename, 'application/pdf', pdf.read())
                mail.send(msg)

            flash("Call for funding has been published")
            return render_template("call_system/call_info_view_page.html", form=form)

        else:
            flash("Unable to publish call - Please enter details in all fields")
            return render_template("call_system/make_call.html", form=form)
    else:
        return render_template("call_system/make_call.html", form=form)

@call_system.route("/query")
def query():
    calls = Call.query.all()
    return str(len(calls))

@call_system.route("/user")
def user():
    u = current_user
    return str(current_user)

# @call_system.route("/upload", methods=["GET", "POST"])
# def upload():
#     # Cannot pass in 'request.form' to AddRecipeForm constructor, as this will cause 'request.files' to not be
#     # sent to the form.  This will cause AddRecipeForm to not see the file data.
#     # Flask-WTF handles passing form data to the form, so not parameters need to be included.
#     from app.call_system.forms import TextForm
#     form = TextForm()
#     if request.method == 'POST':
#         if form.validate_on_submit():
#             filename = texts.save(request.files['text'])
#             url = texts.url(filename)
#             text = File(title=form.title.data, filename=filename, url=url)
#             db.session.add(text)
#             db.session.commit()
#             flash('added, success')
#         else:
#             flash_errors(form)
#             flash('ERROR! Recipe was not added.', 'error')
#     return render_template('call_system/text_upload.html', form=form)

@call_system.route("<call_id>/apply/")
def apply(call_id):
    """The form for grant application

    The <call_id> is the call you are applying to.
    All fields are required. Bootstrap wont show the options field for some reason.
    """
    form = ProposalForm()
    if request.method == "POST":
        if form.validate_on_submit():
            filename = programme_docs.save(request.files["programme_documents"])
            url = programme_docs.url(filename)
            proposal = Proposal(title=form.title.data, duration=form.duration.data, nrp=form.nrp.data,
                                legal_remit=form.legal_remit.data, ethical_issues=form.ethical_issues.data,
                                location=form.location.data, co_applicants=form.co_applicants.data,
                                collaborators=form.collaborators.data, scientific_abstract=form.scientific_abstract.data,
                                lay_abstract=form.lay_abstract.data, programme_docs_filename=filename,
                                programme_docs_url=url)
            db.session.add(proposal)
            db.session.commit()
    return render_template("call_system/apply.html", form=form)

@call_system.route("/all_cfp")
def view_all_calls():
    calls = Call.query.order_by(Call.deadline.desc()).all()
    if len(calls) == 0:
        flash("No calls to display")
    return render_template("call_system/view_all_calls.html", calls=calls)

@call_system.route("/<int:call_id>/view")
def view_call(call_id):
    call = Call.query.filter_by(id=call_id).first()
    # flash("Reading more about call #" + str(call_id))
    return render_template("call_system/view_call.html", call=call)
