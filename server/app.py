from flask import Flask
from flask_bootstrap import Bootstrap
from github_searcher.models import Base
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL # TODO add proper config file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app, metadata=Base.metadata)

import server.views