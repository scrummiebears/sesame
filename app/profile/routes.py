from .forms import *
from . import profile
from .models import *
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
    return render_template("profile/edit.html", form=form, title="Education")

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
    return render_template("profile/edit.html", form=form, title="Employment")

@profile.route("edit/membership", methods=["GET", "POST"])
def editMembership():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = MembershipForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        membership = Membership(researcher_id=researcher.user_id, start_date=form.start_date.data,
                                end_date=form.end_date.data, society_name=form.society_name.data,
                                membership_type=form.membership_type.data)
        db.session.add(membership)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editMembership"))
    return render_template("profile/edit.html", form=form, title="Membership")

@profile.route("edit/award", methods=["GET", "POST"])
def editAward():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = AwardForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        award = Award(researcher_id=researcher.user_id, year=form.year.data,
                      awarding_body=form.awarding_body.data, details=form.details.data,
                      team_member_name=form.team_member_name.data)
        db.session.add(award)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editAward"))
    return render_template("profile/edit.html", form=form, title="Award")

@profile.route("edit/funding_diversification")
def editFundingDiversification():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = FundingDiversificationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        funding_diversification = FundingDiversification(researcher_id=researcher.user_id,
                                                         start_date=form.start_date.data,
                                                         end_date=form.end_date.data,
                                                         amount=form.amount.data,
                                                         funding_body=form.funding_body.data,
                                                         funding_programme=form.funding_programme.data,
                                                         primary_attribution=form.primary_attribution.data)
        db.session.add(funding_diversification)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editFundingDiversification"))
    return render_template("profile/edit.html", form=form, title="Funding Diversification")

@profile.route("edit/team_member", methods=["GET", "POST"])
def editTeamMember():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = TeamMemberForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        team_member = TeamMember(researcher_id=researcher.user_id, start_date=form.start_date.data,
                                 departure_date=form.departure_date.data, name=form.name.data,
                                 position=form.position.data, primary_attribution=form.primary_attribution.data)
        db.session.add(team_member)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editTeamMember"))
    return render_template("profile/edit.html", form=form, title="Team Members")

@profile.route("edit/impact", methods=["GET", "POST"])
def editImpact():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = ImpactForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        impact = Impact(researcher_id=researcher.user_id, title=form.title.data,
                        category=form.category.data, primary_beneficiary=form.primary_beneficiary.data,
                        primary_attribution=form.primary_attribution.data)
        db.session.add(impact)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editImpact"))
    return render_template("profile/edit.html", form=form, title="Impact")

@profile.route("edit/innovation", methods=["GET", "POST"])
def editInnovation():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = InnovationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        innovation = Innovation(researcher_id=researcher.user_id, year=form.year.data,
                                innovation_type=form.innovation_type.data, title=form.title.data,
                                primary_attribution=form.primary_attribution.data)
        db.session.add(innovation)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editInnovation"))
    return render_template("profile/edit.html", form=form, title="Innovation")

@profile.route("edit/publication", methods=["GET", "POST"])
def editPublication():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = PublicationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        publication = Publication(researcher_id=researcher.user_id, year=form.year.data,
                                  original_article=form.original_article.data, review_article=form.review_article.data,
                                  conference_paper=form.conference_paper.data,
                                  book=form.book.data, technical_report=form.technical_report.data,
                                  title=form.title.data, journal_name=form.journal_name.data,
                                  is_published=form.is_published.data, in_press=form.in_press.data,
                                  DOI=form.DOI.data, primary_attribution=form.primary_attribution.data)
        db.session.add(publication)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editPublication"))
    return render_template("profile/edit.html", form=form, title="Publication")

@profile.route("edit/presentation", methods=["GET", "POST"])
def editPresentation():
    if current_user.role != "RESEARCHER":
        abort(403)
    form = PresentationForm()
    if request.method == "POST" and form.validate():
        researcher = current_user.researcher

        presentation = Presentation(researcher_id=researcher.user_id, year=form.year.data,
                                    title=form.title.data, conference=form.conference.data,
                                    invited_seminar=form.invited_seminar.data,
                                    keynote=form.keynote.data,
                                    organising_body=form.invited_seminar.data,
                                    location=form.location.data,
                                    primary_attribution=form.primary_attribution.data)
        db.session.add(presentation)
        db.session.commit()
        flash("Your profile has been updated")
        return redirect(url_for("profile.editPresentation"))
    return render_template("profile/edit.html", form=form, title="Presentation")

@profile.route("edit/academic_collaboration", methods=["GET", "POST"])
def editAcademicCollaboration():
    form = AcademicCollaborationForm()
    return render_template("profile/edit.html", form=form, title="Academic Collaboration")

@profile.route("edit/non_academic_collaboration", methods=["GET", "POST"])
def editNonAcademicCollaboration():
    form = NonAcademicCollaborationForm()
    return render_template("profile/edit.html", form=form, title="Non Academic Collaboration")

@profile.route("edit/conference", methods=["GET", "POST"])
def editConference():
    form = ConferenceForm()
    return render_template("profile/edit.html", form=form, title="Conference")

@profile.route("edit/communication_overview")
def editCommunicationOverview():
    form = CommunicationOverviewForm()
    return render_template("profile/edit.html", form=form, title="Communication Overview")

@profile.route("edit/sfi_funding_ratio", methods=["GET", "POST"])
def editSFIFundingRatio():
    form = SFIFundingRatioForm()
    return render_template("profile/edit.html", form=form, title="SFI Funding Ratio")

@profile.route("edit/educaiton_and_public_engagement", methods=["GET", "POST"])
def editEducationAndPublicEngagement():
    form = EducationAndPublicEngagementForm()
    return render_template("profile/edit.html", form=form, title="Education and Public Engagement")
