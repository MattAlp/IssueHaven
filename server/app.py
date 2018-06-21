from flask import Flask
import flask_bootstrap
from github_searcher.models import Base
from flask_sqlalchemy import SQLAlchemy
import config

# Monkey-patch of flask_bootstrap to change bootstrap/jquery/html versions, may lead to problems
flask_bootstrap.BOOTSTRAP_VERSION = "4.1.0"
flask_bootstrap.JQUERY_VERSION = "3.3.1"
# This only works because these values are string-formatted into the URL when not serving the files locally
# Also probably adds some compatibility issues but if they get in the way I'll write custom BS4 templates
# End monkey-patch
app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = config.DATABASE_URL  # TODO add proper config file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

flask_bootstrap.Bootstrap(app)
db = SQLAlchemy(app, metadata=Base.metadata)

import server.views
