from .forms import *
from . import profile
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

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
    form = EmploymentForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/membership", methods=["GET", "POST"])
def editMembership():
    form = MembershipForm()
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
    form = AcademicCollaborationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/non_academic_collaboration", methods=["GET", "POST"])
def editNonAcademicCollaboration():
    form = NonAcademicCollaborationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/conference", methods=["GET", "POST"])
def editConference():
    form = ConferenceForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/communication_overview")
def editCommunicationOverview():
    form = CommunicationOverviewForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/sfi_funding_ratio", methods=["GET", "POST"])
def editSFIFundingRatio():
    form = SFIFundingRatioForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/educaiton_and_public_engagement", methods=["GET", "POST"])
def editEducationAndPublicEngagement():
    form = EducationAndPublicEngagementForm()
    return render_template("profile/edit.html", form=form)
