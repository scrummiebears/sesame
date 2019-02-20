from flask import Blueprint

call_system = Blueprint("call_system", __name__)

import app.call_system.models
import app.call_system.forms
import app.call_system.routes