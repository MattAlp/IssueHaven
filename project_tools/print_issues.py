from github_searcher.models import Base, engine, Issue, Repo
from sqlalchemy.orm import sessionmaker

if __name__ == "__main__":

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    for repo in session.query(Repo).all():
        print("%s - %d stars, lang:%s" % (repo.name, repo.total_stars, repo.language))
        for issue in repo.issues:
            print(
                "\t[%s]\t%s with %d comments, created at %s"
                % (issue.category, issue.title, issue.total_comments, issue.created_at)
            )
        print()
