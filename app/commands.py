import click
from flask.cli import with_appcontext, AppGroup
from app import db
from sqlalchemy import text
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