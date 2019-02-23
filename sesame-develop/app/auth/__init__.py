from flask import Flask, Blueprint
from app import login_manager

auth = Blueprint("auth", __name__)

import app.auth.routes
import app.auth.models
import app.auth.forms