from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from .context_processors import format_date


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.context_processor
def processors():
    return {
        "format_date": format_date
    }


from app import models
from app import views
