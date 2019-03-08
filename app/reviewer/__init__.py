from flask import Blueprint

reviewer = Blueprint("reviewer", __name__)

import app.reviewer.models
import app.reviewer.routes