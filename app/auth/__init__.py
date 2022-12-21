from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder="/app/templates", url_prefix='/auth')