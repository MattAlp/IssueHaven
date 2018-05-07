from github import Github
import time
import core
from core.models import Base, engine, Issue
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    # core.hello()
    g = Github("user", "password")

    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    for search in core.generate_searches():

        t = time.time()
        issues = g.search_issues(search)

        for index in range(min(core.MAX_RESULTS, issues.totalCount)):
            issue = issues[index]
            session.add(Issue(id=issue.id, html_url=issue.html_url, language=issue.repository.language))
            try:
                time.sleep((core.SECONDS_PER_REQUEST - (time.time() - t)) / core.RESULTS_PER_PAGE)
            except ValueError as e:
                pass
            t = time.time()
        session.commit()
        time.sleep(core.SECONDS_PER_REQUEST)
    session.close()
    exit(0)
