from .forms import *
from . import profile
from .models import *
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from datetime import datetime, date

@profile.route("edit/education", methods=["GET", "POST"])
@login_required
def editEducation():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = EducationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        education = Education(researcher_id=researcher.user_id, degree=form.degree.data, field_of_study=form.field_of_study.data,
                              institution=form.institution.data, location=form.location.data, degree_award_year=form.degree_award_year.data)
        db.session.add(education)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editEducation"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/employment", methods=["GET", "POST"])
def editEmployment():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = EmploymentForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        employment = Employment(researcher_id=researcher.user_id, institution=form.institution.data,
                                location=form.location.data, years=form.years.data)
        db.session.add(employment)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editEmployment"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/membership", methods=["GET", "POST"])
def editMembership():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = MembershipForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        membership = Membership(start_date=start_date, end_date=end_date,
                                society_name=form.society_name.data, membership_type=form.membership.data)
        db.session.add(employment)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editMembership"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/award", methods=["GET", "POST"])
def editAward():
    form = AwardForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/funding_diversification")
def editFundingDiversification():
    form = FundingDiversificationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/team_member", methods=["GET", "POST"])
def editTeamMember():
    form = TeamMemberForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/impact", methods=["GET", "POST"])
def editImpact():
    form = ImpactForm()
    return render_template("profile/edit.html", form=form)


@profile.route("edit/innovation", methods=["GET", "POST"])
def editInnovation():
    form = InnovationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/publication", methods=["GET", "POST"])
def editPublication():
    form = PublicationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/presentation", methods=["GET", "POST"])
def editPresentation():
    form = PresentationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/academic_collaboration", methods=["GET", "POST"])
def editAcademicCollaboration():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = AcademicCollaborationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        start_date_input = form.start_date.data.split("-")
        start_date = date(int(start_date_input[0]), int(start_date_input[1]), int(start_date_input[2]))
        end_date_input = form.end_date.data
        end_date = date(int(end_date_input[0]), int(end_date_input[1]), int(end_date_input[2]))
        academic_collaboration = AcademicCollaboration(start_date=start_date, end_date=end_date, institution=form.institution.data, location=form.location.data, collaborator_name=form.collaborator.data,
                                                              primary_goal=form.primary_goal.data, interaction_frequency=form.interaction_frequency.data, primary_attribution=form.primary_attribution.data)
        db.session.add(academic_collaboration)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editAcademicCollaboration"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/non_academic_collaboration", methods=["GET", "POST"])
def editNonAcademicCollaboration():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = NonAcademicCollaborationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        start_date_input = form.start_date.data.split("-")
        start_date = date(int(start_date_input[0]), int(start_date_input[1]), int(start_date_input[2]))
        end_date_input = form.end_date.data
        end_date = date(int(end_date_input[0]), int(end_date_input[1]), int(end_date_input[2]))
        non_academic_collaboration = NonAcademicCollaboration(start_date=start_date, end_date=end_date, institution=form.institution.data, location=form.location.data, collaborator_name=form.collaborator.data,
                                                              primary_goal=form.primary_goal.data, interaction_frequency=form.interaction_frequency.data, primary_attribution=form.primary_attribution.data)
        db.session.add(non_academic_collaboration)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editNonAcademicCollaboration"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/conference", methods=["GET", "POST"])
def editConference():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = ConferenceForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        start_date_input = form.start_date.data.split("-")
        start_date = date(int(start_date_input[0]), int(start_date_input[1]), int(start_date_input[2]))
        end_date_input = form.end_date.data
        end_date = date(int(end_date_input[0]), int(end_date_input[1]), int(end_date_input[2]))
        conference = Conference(start_date=start_date, end_date=end_date, title=form.title.data, event_type=form.event_type.data,
                                role=form.role.data, location=form.location.data, primary_attribution=form.primary_attribution.data)
        db.session.add(conference)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editConference"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/communication_overview")
def editCommunicationOverview():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = CommunicationOverviewForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher
        
        comm_overview = CommunicationOverview(year=form.year.data, num_of_public_lectures=form.num_of_public_lectures.data, num_of_visits=form)
        db.session.add(conference)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editConference"))
    return render_template("profile/edit.html", form=form)

@profile.route("edit/sfi_funding_ratio", methods=["GET", "POST"])
def editSFIFundingRatio():
    form = SFIFundingRatioForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/educaiton_and_public_engagement", methods=["GET", "POST"])
def editEducationAndPublicEngagement():
    form = EducationAndPublicEngagementForm()
    return render_template("profile/edit.html", form=form)
