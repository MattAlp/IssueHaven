from github import Github
from github.GithubException import UnknownObjectException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from github_searcher.models import Base, engine, Issue, Repo
from github_searcher.util import rate_limit_github
import config
import json
import os


if __name__ == "__main__":
    print("[INFO] Token: " + config.TOKEN)
    print("[INFO] Database URL: " + config.DATABASE_URL)
    client = Github(config.TOKEN, per_page=config.SEARCH_PER_PAGE)

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    with open(os.path.join(config.PROJECT_ROOT, "repos.json"), "r") as f:
        data = json.load(f)
        for json_repo in data["repos"]:
            # PyGithub doesn't have internal waits for rate limiting so patching is the way to go for the time being
            client.get_repo = rate_limit_github(client.get_repo, client)
            repo = client.get_repo(json_repo["name"])
            repo.get_issues = rate_limit_github(repo.get_issues, client)
            repo.get_label = rate_limit_github(repo.get_label, client)
            # end patch
            if repo.has_issues and not repo.archived:
                if not session.query(exists().where(Repo.repo_id == repo.id)).scalar():
                    session.add(Repo(repo_id=repo.id, name=repo.name, description=repo.description, url=repo.html_url,
                                     language=repo.language, created_at=repo.created_at,
                                     total_stars=repo.stargazers_count))

                print("[INFO] Scanning repo %s" % repo.html_url)
                for label in json_repo["code_labels"]:
                    try:
                        issues = repo.get_issues(labels=[repo.get_label(label)], state="open", assignee="none")
                        for issue in issues:
                            info = "[INFO] Repo ID:%s, Issue ID:%s, Issue Title:%s, URL:%s"
                            print(info % (repo.id, issue.id, issue.title, issue.html_url))

                            if not session.query(exists().where(Issue.issue_id == issue.id)).scalar():
                                session.add(Issue(issue_id=issue.id, repo_id=repo.id, title=issue.title,
                                                  description=issue.body, url=issue.html_url, category="code",
                                                  created_at=issue.created_at, total_comments=issue.comments))
                            else:
                                # In case the issue already exists
                                # existing_issue = session.query(Issue).filter_by(issue_id=issue.id).first()
                                # existing_issue.total_comments = issue.comments
                                pass
                                # TODO add update/cleanup code
                    except UnknownObjectException:
                        print("[ERROR] Label %s wasn't found in repo %s" % (label, repo))
                for label in json_repo["chore_labels"]:
                    try:
                        issues = repo.get_issues(labels=[repo.get_label(label)], state="open", assignee="none")
                        for issue in issues:
                            info = "[INFO] Repo ID:%s, Issue ID:%s, Issue Title:%s, URL:%s"
                            print(info % (repo.id, issue.id, issue.title, issue.html_url))
                            if not session.query(exists().where(Issue.issue_id == issue.id)).scalar():
                                session.add(Issue(issue_id=issue.id, repo_id=repo.id, title=issue.title,
                                                  description=issue.body, url=issue.html_url, category="chore",
                                                  created_at=issue.created_at, total_comments=issue.comments))
                            else:
                                # In case the issue was already recorded by the code_labels loop, change the category to
                                # reflect that the issue is actually a chore (i.e. documentation) and not related to
                                # programming.
                                session.query(Issue).filter_by(issue_id=issue.id).first().category = "chore"
                    except UnknownObjectException:
                        print("[ERROR] Label %s wasn't found in repo %s" % (label, repo))
                session.commit()

    session.close()
