from core import search_issues, Config
from core.models import engine, Base
from sqlalchemy.orm import sessionmaker
import requests_cache

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()
    requests_cache.install_cache("testing_cache", backend=None, expire_after=3600)

    for language in Config.LANGUAGES:
        for label in Config.CODE:
            search_issues(label, language, "code", session)

    for label in Config.DOCS:
        search_issues(label, "any", "documentation", session)

    for label in Config.GFX:
        search_issues(label, "any", "graphics", session)
    session.close()
    exit()
