from flask import Flask
from app import db, bcrypt, login_manager

@auth.route("/createAdmin",methods=["GET","POST"])
def createAdmin():
    password = bcrypt.generate_password_hash("password").decode("utf-8")
            user = User("116449934@umail.ucc.ie",password, "ADMIN")
            db.session.add(user)
            db.session.commit()
            flash("Admin made")
            return redirect(url_for("auth.login"))