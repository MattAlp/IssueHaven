from flask import render_template, redirect
from github_searcher.models import Issue, Repo
from .app import app, db
import config


@app.route("/")
def index():
    return render_template(
        "index.jinja2",
        total_issues=db.session.query(Issue).count(),
        total_repos=db.session.query(Repo).count(),
        languages=config.LANGUAGES,
        mappings=config.MAPPINGS,
    )


@app.route("/about")
def about():
    return render_template(
        "about.jinja2", languages=config.LANGUAGES, mappings=config.MAPPINGS
    )


@app.route("/donate")
def donate():
    redirect(config.DONATE_LINK, code=302)


@app.route("/contribute")
def contribute():
    redirect(config.CONTRIBUTE_LINK, code=302)


@app.route("/issues/")
@app.route("/issues/<int:page>")
@app.route("/issues/<string:language>")
@app.route("/issues/<string:language>/<int:page>")
def show_issues(page=1, language: str = None):
    if language is not None:
        language = config.MAPPINGS[language.lower()]
        issues = (
            db.session.query(Issue)
            .filter(Issue.category == "code")
            .order_by(Issue.created_at.desc(), Issue.total_comments.desc())
            .join(Issue.repo)
            .order_by(Repo.total_stars.desc())
            .filter(Repo.language.ilike(language))
            .paginate(page=page, per_page=15)
        )
    else:
        issues = (
            db.session.query(Issue)
            .filter(Issue.category == "code")
            .order_by(Issue.created_at.desc(), Issue.total_comments.desc())
            .join(Issue.repo)
            .order_by(Repo.total_stars.desc())
            .paginate(page=page, per_page=15)
        )
    return render_template(
        "issues.jinja2",
        issues=issues,
        language=language,
        languages=config.LANGUAGES,
        mappings=config.MAPPINGS,
    )


@app.route("/chores/")
@app.route("/chores/<int:page>")
@app.route("/chores/<string:language>")
@app.route("/chores/<string:language>/<int:page>")
def show_chores(page=1, language=None):
    if language is not None:
        language = config.MAPPINGS[language.lower()]
        chores = (
            db.session.query(Issue)
            .filter(Issue.category == "chore")
            .order_by(Issue.created_at.desc(), Issue.total_comments.desc())
            .join(Issue.repo)
            .order_by(Repo.total_stars.desc())
            .filter(Repo.language.ilike(language))
            .paginate(page=page, per_page=15)
        )
    else:
        chores = (
            db.session.query(Issue)
            .filter(Issue.category == "chore")
            .order_by(Issue.created_at.desc(), Issue.total_comments.desc())
            .join(Issue.repo)
            .order_by(Repo.total_stars.desc())
            .paginate(page=page, per_page=15)
        )
    return render_template(
        "chores.jinja2",
        chores=chores,
        language=language,
        languages=config.LANGUAGES,
        mappings=config.MAPPINGS,
    )
