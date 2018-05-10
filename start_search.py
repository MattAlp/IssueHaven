from core import search_issues, Config
from core.models import engine, Base
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    for language in Config.LANGUAGES:
        for label in Config.CODE:
            search_issues(label, language, session)
    # for label in Config.DOCS:
    #     search_issues(label, "any")
    session.close()
    exit()
