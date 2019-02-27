import click
from flask.cli import with_appcontext, AppGroup
from app import db, bcrypt
from sqlalchemy import text
from app.auth.models import *
from app.profile.models import *

db_cli = AppGroup("db")

@click.command("flushDb")
@with_appcontext
def flushDb():
    """Clear all tables from the database
    
    After this is complete, the db.create_all function needs to run to
    create all the tables again
    """
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print("Clear table %s" % table)
        db.session.execute(table.delete())
    db.session.commit()
    
@db_cli.command("stats", help="List number of rows for each table")
@with_appcontext
def stats():
    meta = db.metadata
    for table in meta.sorted_tables:
        print("""Table: %s\n===================""" % table.name)
        query = "SELECT COUNT(*) FROM " + table.name
        result = db.session.execute(query).first()
        print("Number of rows: " + str(result[0]))
        print("\n")

@db_cli.command("exec", help="Execute an SQL File")
@click.argument("file")
@with_appcontext
def exec(file):
    f = open(file, "r")
    for line in f:
        db.engine.execute(text(line))
    f.close()


user_cli = AppGroup("user")
@user_cli.command("init")
def user_init():
    password = bcrypt.generate_password_hash("1234").decode("utf-8")
    user = User("root", password, "RESEARCHER")
    db.session.add(user)
    db.session.commit()

    r = Researcher(user_id=1, first_name="root", last_name="", job_title="", prefix="")
    db.session.add(r)
    db.session.commit()
