@admin.route("dashboard")
def dashboard():
    return render_template("admin/dashboard.html", user=admin)

@admin.route("new_admin")
def newAdmin():
    return render_template("admin/new_admin.html", user=admin)

@admin.route("<call>/proposals")
def proposals(call):
    return render_template("admin/proposals.html")

@admin.route("<proposal>/review")
def review(proposal)

@admin.route("<proposal>/deny")
def rejectProposal(propsoal):
    return redirect(url_for(""))

@admin.route("<proposal>/assign_reviewers")
def assignReviewers(proposal):
    return render_template("admin/assign_reviewers")

@admin.route("<proposal>/approve")
def approveProposal(proposal):
    return redirect(url_for(""))



