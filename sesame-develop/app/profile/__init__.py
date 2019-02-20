from flask import Flask, Blueprint

profile = Blueprint("profile", __name__)

import app.auth.models