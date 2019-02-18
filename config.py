# Statement for enabling the development envoiroment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "uploads")
# Define the database - sqlLite for now
SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(BASE_DIR, "app.db")
#DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

SQLALCHEMY_TRACK_MODIFICATIONS = False

MAIL_SERVER = "smtp.gmail.com"

MAIL_PORT = 465

MAIL_USE_SSL = True

MAIL_USERNAME = "sesamenotifications@gmail.com"

MAIL_PASSWORD = "123sesamestreet^}-!"

MAIL_DEFAULT_SENDER = "sesamenotifications@gmail.com"


#flask upload
UPLOADS_DEFAULT_DEST = "uploads"
UPLOADS_DEFAULT_URL = "uploads"