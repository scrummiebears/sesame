import click
from flask.cli import with_appcontext, AppGroup
from app import db, bcrypt
from sqlalchemy import text
from app.auth.models import *
from app.profile.models import *
from app.admin.models import *
from app.call_system import *

db_cli = AppGroup("db")

@db_cli.command("drop", help="Drop all tables")
@click.option("--only", help="Only drop this table")
@with_appcontext
def drop(only):
    """Drop all tables from the database.
    
    If the --only <table> option is used, only that table is dropped
    """
    meta = db.metadata
    if only:
        for table in reversed(meta.sorted_tables):
            if str(table) == only:
                print("Dropped table %s" % table)
                table.drop(db.engine)
                meta.remove(table)
                return
    else:
        for table in reversed(meta.sorted_tables):
            print("Dropped table %s" % table)
            table.drop(db.engine)
            meta.remove(table)
        meta.drop_all(db.engine)

@db_cli.command("clear", help="Clear all tables")
@click.option("--only", help="Only clear this table")
@with_appcontext
def clear(only):
    """Clear the contents of all tables
    
    If the --only <table> option is used, only that table is cleared
    """
    meta = db.metadata
    if only:
        for table in reversed(meta.sorted_tables):
            if str(table) == only:
                print("Cleared table %s" % table)
                db.session.execute(table.delete())
            db.session.commit()
    else:
        for table in reversed(meta.sorted_tables):
            print("Cleared table %s" % table)
            db.session.execute(table.delete())
        db.session.commit()

@db_cli.command("init")
@with_appcontext
def init():
    """Initiate all tables

    """
    db.create_all()
    print("Done")

@db_cli.command("list")
@with_appcontext
def list():
    """List all tables (BROKEN)
    """
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print(table)

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
@user_cli.command("init", help="Initiate an Admin account on the system with the specfied details")
def user_init():
    """Makes an initial admin account with specified details so the system can be used.
    """
    if len(User.query.all()) != 0:
        print("FAILED: initial account already created")
        return
    print("Please enter the account details as prompted")
    email = input("Email: ")
    password = input("Password: ")

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    a_user = User(email, password_hash, "ADMIN")
    db.session.add(a_user)

    a = Admin(user_id=1,first_name=first_name ,last_name=last_name)
    db.session.add(a)
    db.session.commit()

    print("""Admin account created - 
    Email: %s
    Password: %s
    Name %s %s""" % (email, password, first_name, last_name))
    
    # Researchers
    # r_user = User("researcher@sesame.com", password, "RESEARCHER")
    # db.session.add(r_user)
    # db.session.commit()

    # r = Researcher(user_id=2, first_name="Peter", last_name="Adams", job_title="Operator", prefix="Mr", suffix="Jr", phone="086111111", phone_ext="+353", orcid="0193FG")
    # db.session.add(r)
    # db.session.commit()

    # r_user = User("maygreen@sesame.com", password, "RESEARCHER")
    # db.session.add(r_user)
    # db.session.commit()

    # r = Researcher(user_id=3, first_name="May", last_name="Green", job_title="Biologist", prefix="Ms", suffix="Jr", phone="037493829", phone_ext="+353", orcid="0193FG")
    # db.session.add(r)
    # db.session.commit()

    # r_user = User("jackb@sesame.com", password, "RESEARCHER")
    # db.session.add(r_user)
    # db.session.commit()

    # r = Researcher(user_id=4, first_name="Jack", last_name="Blue", job_title="Operator", prefix="Mr", suffix="Jr", phone="086111111", phone_ext="+353", orcid="0193FG")
    # db.session.add(r)
    # db.session.commit()

    # db.engine.execute("insert into calls (id, date_published, admin_id, information, target_group, proposal_template, deadline, eligibility_criteria, duration_of_award, reporting_guidelines, expected_start_date, status) values (1, '2019-01-05 05:52:11', 1, 'Donec dapibus. Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante.', 'Ut tellus. Nulla ut erat id mauris vulputate elementum.', 'Vestibulum sed magna at nunc commodo placerat. Praesent blandit. Nam nulla. Integer pede justo, lacinia eget, tincidunt eget, tempus vel, pede. Morbi porttitor lorem id ligula. Suspendisse ornare consequat lectus. In est risus, auctor sed, tristique in, tempus sit amet, sem. Fusce consequat.', '2018-09-13 06:33:55', 'Aenean fermentum. Donec ut mauris eget massa tempor convallis. Nulla neque libero, convallis eget, eleifend luctus, ultricies eu, nibh. Quisque id justo sit amet sapien dignissim vestibulum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nulla dapibus dolor vel est.', '2018-04-21 16:48:33', 'Duis at velit eu est congue elementum. In hac habitasse platea dictumst. Morbi vestibulum, velit id pretium iaculis, diam erat fermentum justo, nec condimentum neque sapien placerat ante. Nulla justo. Aliquam quis turpis eget elit sodales scelerisque. Mauris sit amet eros. Suspendisse accumsan tortor quis turpis. Sed ante. Vivamus tortor. Duis mattis egestas metus.', '2020-11-29 16:58:26', 'PUBLISHED');")
    # db.engine.execute("insert into calls (id, date_published, admin_id, information, target_group, proposal_template, deadline, eligibility_criteria, duration_of_award, reporting_guidelines, expected_start_date, status) values (2, '2018-11-13 01:33:56', 1, 'Duis aliquam convallis nunc. Proin at turpis a pede posuere nonummy. Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum.', 'Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum.', 'Sed vel enim sit amet nunc viverra dapibus. Nulla suscipit ligula in lacus. Curabitur at ipsum ac tellus semper interdum. Mauris ullamcorper purus sit amet nulla. Quisque arcu libero, rutrum ac, lobortis vel, dapibus at, diam.', '2019-02-09 22:30:40', 'Sed accumsan felis. Ut at dolor quis odio consequat varius. Integer ac leo. Pellentesque ultrices mattis odio.', '2019-02-04 13:18:31', 'In hac habitasse platea dictumst. Aliquam augue quam, sollicitudin vitae, consectetuer eget, rutrum at, lorem. Integer tincidunt ante vel ipsum. Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat. Praesent blandit.', '2020-10-11 07:43:18', 'PUBLISHED');")
    # db.engine.execute("insert into calls (id, date_published, admin_id, information, target_group, proposal_template, deadline, eligibility_criteria, duration_of_award, reporting_guidelines, expected_start_date, status) values (3, '2018-09-28 23:50:31', 1, 'Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus. Duis at velit eu est congue elementum.', 'Phasellus in felis.', 'Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus. In sagittis dui vel nisl. Duis ac nibh.', '2019-01-03 13:17:22', 'Sed sagittis. Nam congue, risus semper porta volutpat, quam pede lobortis ligula, sit amet eleifend pede libero quis orci. Nullam molestie nibh in lectus. Pellentesque at nulla. Suspendisse potenti. Cras in purus eu magna vulputate luctus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vivamus vestibulum sagittis sapien.', '2018-11-19 18:50:30', 'Morbi a ipsum. Integer a nibh. In quis justo. Maecenas rhoncus aliquam lacus. Morbi quis tortor id nulla ultrices aliquet. Maecenas leo odio, condimentum id, luctus nec, molestie sed, justo. Pellentesque viverra pede ac diam. Cras pellentesque volutpat dui. Maecenas tristique, est et tempus semper, est quam pharetra magna, ac consequat metus sapien ut nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Mauris viverra diam vitae quam.', '2020-10-09 09:17:36', 'PUBLISHED');")
    # db.engine.execute("insert into calls (id, date_published, admin_id, information, target_group, proposal_template, deadline, eligibility_criteria, duration_of_award, reporting_guidelines, expected_start_date, status) values (4, '2018-03-26 10:31:14', 1, 'Praesent lectus. Vestibulum quam sapien, varius ut, blandit non, interdum in, ante. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Duis faucibus accumsan odio. Curabitur convallis. Duis consequat dui nec nisi volutpat eleifend. Donec ut dolor.', 'Nulla nisl. Nunc nisl. Duis bibendum, felis sed interdum venenatis, turpis enim blandit mi, in porttitor pede justo eu massa. Donec dapibus.', 'Praesent blandit lacinia erat. Vestibulum sed magna at nunc commodo placerat.', '2018-08-10 06:05:06', 'Etiam justo. Etiam pretium iaculis justo.', '2018-04-10 18:55:09', 'Integer non velit. Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec pharetra, magna vestibulum aliquet ultrices, erat tortor sollicitudin mi, sit amet lobortis sapien sapien non mi. Integer ac neque. Duis bibendum. Morbi non quam nec dui luctus rutrum. Nulla tellus.', '2020-08-01 01:02:26', 'PUBLISHED');")
