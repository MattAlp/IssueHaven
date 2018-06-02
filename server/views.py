from flask import render_template
from github_searcher.models import Issue, Repo
from .app import app, db

# TODO create actual templates instead of placeholders


@app.route("/")
def index():
    return render_template("index.jinja2")


@app.route("/issues")
@app.route("/issues/<int:page>")
@app.route("/issues/<string:language>")
@app.route("/issues/<string:language>/<int:page>")
def show_issues(page=1, language=None):
    if language is not None:
        if language.lower() == "csharp":
            language = "c#"
        issues = db.session.query(Issue).order_by(Issue.created_at.desc(), Issue.total_comments.desc()).join(Issue.repo).order_by(Repo.total_stars.desc()).filter(Repo.language.ilike(language)).paginate(page=page, per_page=15)
    else:
        issues = db.session.query(Issue).paginate(page=page, per_page=15)
    return render_template("issues.jinja2", issues=issues, language=language)
