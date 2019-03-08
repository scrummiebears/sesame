from flask import Flask, render_template, flash, redirect, url_for, make_response, request, abort
from werkzeug import secure_filename
import os

# Import the extensions used here
from app import db, login_manager, mail
import app.call_system.forms
from flask_login import current_user, login_required
from flask_mail import Message

# Import call_system blueprint
from app.reviewer import reviewer

import datetime
import config


@reviewer.route("review")
def review():

@reviewer.route("accept")
def accept():

@reviewer.route("reject")
def reject():
    