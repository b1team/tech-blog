from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from .context_processors import format_date


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.context_processor
def processors():
    return {
        "format_date": format_date
    }


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error/404.html'), 404


@app.errorhandler(403)
def page_not_found(e):
    # note that we set the 403 status explicitly
    return render_template('error/403.html'), 403


@app.errorhandler(401)
def page_not_found(e):
    # note that we set the 403 status explicitly
    return redirect(url_for('login_bp.login'))


from app import models
from app import views
