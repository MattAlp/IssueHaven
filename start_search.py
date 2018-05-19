from core.models import engine, Base, Issue
from core import search_issues, Config
from sqlalchemy.orm import sessionmaker
import requests_cache

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    requests_cache.install_cache("testing_cache", backend=None, expire_after=360000)

    code = ["good first issue", "beginner", "e-easy", "beginner friendly", "starter",
            "first-timers only", "starter", "newbie", "jump in", "low-hanging fruit"]

    for language in Config.LANGUAGES:
        for label in code:
            search_issues(label, language, "code", session)
    #
    # for label in Config.DOCS:
    #     search_issues(label, "any", "documentation", session)
    #
    # for label in Config.GFX:
    #     search_issues(label, "any", "graphics", session)

    # for i, issue in enumerate(session.query(Issue).order_by(Issue.score.desc())):
    #     print(issue.category, issue.html_url, issue.score)

    session.close()
    exit()
