from app import db

class Admin(db.Model):
    
    __tablename__ = "admins"

    user = db.relationship("User", backref=db.backref("admin", uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
