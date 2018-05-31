from flask import render_template
from github_searcher.models import Issue
from .app import app, db

# TODO create actual templates instead of placeholders


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.jinja2")


@app.route("/issues/<int:page>")
def show_issues(page):

    issues = db.session.query(Issue).paginate(page=page, per_page=15)

    # return render_template("issues.jinja2", issues=db.session.query(Issue).all())
    return render_template("issues.jinja2", issues=issues.items)
