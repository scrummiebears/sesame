import click
from flask.cli import with_appcontext
from app import db

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

@click.command("populateDb")
@with_appcontext
def populateDb():
    """Insert some data into the database
    
    """
    print("Inserting data into the db")
