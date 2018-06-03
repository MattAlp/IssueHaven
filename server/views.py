from flask import render_template
from github_searcher.models import Issue, Repo
from .app import app, db
import config


@app.route("/")
def index():
    return render_template("index.jinja2", total=db.session.query(Issue).count())


@app.route("/issues/")
@app.route("/issues/<int:page>")
@app.route("/issues/<string:language>")
@app.route("/issues/<string:language>/<int:page>")
def show_issues(page=1, language=None):
    if language is not None:
        if language.lower() in config.MAPPINGS:
            language = config.MAPPINGS[language]
        issues = db.session.query(Issue).filter(Issue.category == "code").order_by(Issue.created_at.desc(), Issue.total_comments.desc()).join(Issue.repo).order_by(Repo.total_stars.desc()).filter(Repo.language.ilike(language)).paginate(page=page, per_page=15)
    else:
        issues = db.session.query(Issue).filter(Issue.category == "code").order_by(Issue.created_at.desc(), Issue.total_comments.desc()).join(Issue.repo).order_by(Repo.total_stars.desc()).paginate(page=page, per_page=15)
    return render_template("issues.jinja2", issues=issues, language=language)


@app.route("/chores/")
@app.route("/chores/<int:page>")
@app.route("/chores/<string:language>")
@app.route("/chores/<string:language>/<int:page>")
def show_chores(page=1, language=None):
    if language is not None:
        if language.lower() in config.MAPPINGS:
            language = config.MAPPINGS[language]
        chores = db.session.query(Issue).filter(Issue.category == "chore").order_by(Issue.created_at.desc(), Issue.total_comments.desc()).join(Issue.repo).order_by(Repo.total_stars.desc()).filter(Repo.language.ilike(language)).paginate(page=page, per_page=15)
    else:
        chores = db.session.query(Issue).filter(Issue.category == "chore").order_by(Issue.created_at.desc(), Issue.total_comments.desc()).join(Issue.repo).order_by(Repo.total_stars.desc()).paginate(page=page, per_page=15)
    return render_template("chores.jinja2", chores=chores, language=language)