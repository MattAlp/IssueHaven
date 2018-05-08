from github import Github
import time
import core
from core.models import Base, engine, Issue
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    # core.hello()
    for language in core.Config.languages:
        for label in core.Config.labels:
            core.search_issues(label, language)
    # g = Github(core.Config.user, core.Config.password)
    #
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # Base.metadata.create_all(engine)
    #
    # for search in core.generate_search_string():
    #
    #     t = time.time()
    #     issues = g.search_issues(search)
    #
    #     for index in range(min(core.MAX_RESULTS, issues.totalCount)):
    #         issue = issues[index]
    #         session.add(Issue(id=issue.id, html_url=issue.html_url, language=issue.repository.language))
    #         try:
    #             time.sleep((core.SECONDS_PER_REQUEST - (time.time() - t)) / core.RESULTS_PER_PAGE)
    #         except ValueError as e:
    #             pass
    #         t = time.time()
    #     session.commit()
    #     time.sleep(core.SECONDS_PER_REQUEST)
    # session.close()
    exit(0)
