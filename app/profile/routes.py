from .forms import *
from . import profile
from flask import render_template

@profile.route("edit/education")
def editEducation():
    form = EducationForm()
    return render_template("profile/editeducation.html", form=form)

@profile.route("edit/employment")
def editEmployment():
    form = EmploymentForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/membership")
def editMembership():
    form = MembershipForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/award")
def editAward():
    form = AwardForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/funding_diversification")
def editFundingDiversification():
    form = FundingDiversificationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/team_member")
def editTeamMember():
    form = TeamMemberForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/impact")
def editImpact():
    form = ImpactForm()
    return render_template("profile/edit.html", form=form)


@profile.route("edit/innovation")
def editInnovation():
    form = InnovationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/publication")
def editPublication():
    form = PublicationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/presentation")
def editPresentation():
    form = PresentationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/academic_collaboration")
def editAcademicCollaboration():
    form = AcademicCollaborationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/non_academic_collaboration")
def editNonAcademicCollaboration():
    form = NonAcademicCollaborationForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/conference")
def editConference():
    form = ConferenceForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/communication_overview")
def editCommunicationOverview():
    form = CommunicationOverviewForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/sfi_funding_ratio")
def editSFIFundingRatio():
    form = SFIFundingRatioForm()
    return render_template("profile/edit.html", form=form)

@profile.route("edit/educaiton_and_public_engagement")
def editEducationAndPublicEngagement():
    form = EducationAndPublicEngagementForm()
    return render_template("profile/edit.html", form=form)
