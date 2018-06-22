import json
import time
import config
import requests
from typing import List
from github_searcher.models import Base, engine, Issue, Repo
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class PyJSON(object):
    """
    Modified PyJSON class with _repr_ added, based on a StackOverflow answer
    """

    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)
        self.convert_json(d)

    def convert_json(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = PyJSON(value)
            self.__dict__[key] = value

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return str(self.__dict__)


def rate_limit_gql(func):
    query = """{
  rateLimit{
    remaining
    resetAt
  }
}
"""

    def wrapper(*args, **kwargs):
        limit = PyJSON(
            requests.post(
                config.GRAPHQL_API_URL, json={"query": query}, headers=config.HEADER
            ).json()["data"]["rateLimit"]
        )
        if limit.remaining == 0:
            print("Sleeping due to rate limit")
            time.sleep(limit.resetAt - time.time() + 1)
        return func(*args, **kwargs)

    return wrapper


def fill_query(query: str, **kwargs):
    return (query % kwargs).replace("'", '"')


@rate_limit_gql
def get_repos(language: str, after: str = None, labels=List[str]):
    query = """{
  search(query: "language:%(language)s stars:>500", type: REPOSITORY, first: 100, after: %(endCursor)s) {
    repositoryCount
    nodes {
      ... on Repository {
        databaseId
        nameWithOwner
        description
        url
        primaryLanguage{
          name
        }
        createdAt
        stargazers{
          totalCount
        }
        isArchived
        issues(states: OPEN, labels: %(labels)s){
          totalCount
        }
      }
    }
    pageInfo{
      hasNextPage
      endCursor
    }
  }
}"""
    if after is not None:
        after = '"' + after + '"'
    else:
        after = "null"
    built_query = fill_query(
        query, language=language, endCursor=after, labels=str(labels)
    )
    data = requests.post(
        config.GRAPHQL_API_URL, json={"query": built_query}, headers=config.HEADER
    ).json()["data"]
    return PyJSON(data)


@rate_limit_gql
def get_issues(fullname: str, after: str = None, labels=List[str]):
    query = """{
  repository(owner: "%(owner)s", name:"%(name)s"){
    issues(states:OPEN, first:100, labels:%(labels)s, after:%(endCursor)s){
      nodes{
        assignees{
          totalCount
        }
        labels(first:100 after:null){
          nodes{
            name
          }
        }
        databaseId
        title
        bodyText
        url
        createdAt
        comments{
          totalCount
        }
      }
      pageInfo{
        hasNextPage
        endCursor
      }
    }
  }
}"""
    if after is not None:
        after = '"' + after + '"'
    else:
        after = "null"
    owner, name = fullname.split("/")
    built_query = fill_query(
        query, owner=owner, name=name, endCursor=after, labels=str(labels)
    )
    data = requests.post(
        config.GRAPHQL_API_URL, json={"query": built_query}, headers=config.HEADER
    ).json()["data"]
    return PyJSON(data)


def get_issue_category(issue_labels: List[str]):
    for category, category_labels in config.CATEGORIES.items():
        if any(i in issue_labels for i in category_labels):
            return category
    raise ValueError(
        "None of the issue labels fell under %s" % str(config.CATEGORIES.keys())
    )


if __name__ == "__main__":
    print("Config Token: %s" % config.TOKEN)
    print("Database URL: " + config.DATABASE_URL)

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session = session_factory()

    for language in config.LANGUAGES:
        print("\nLanguage: " + language)

        if language.lower() in config.MAPPINGS:
            mapped_language = config.MAPPINGS[language]
        else:
            mapped_language = language

        old_issues = (
            session.query(Issue)
            .join(Issue.repo)
            .filter(Repo.language.ilike(mapped_language))
            .all()
        )
        print("Deleting %d issues in %s" % (len(old_issues), language))
        for issue in old_issues:
            session.delete(issue)
        print("Deleted issues!")

        old_repos = (
            session.query(Repo).filter(Repo.language.ilike(mapped_language)).all()
        )
        print("Deleting %d repos in %s" % (len(old_repos), language))
        for repo in old_repos:
            session.delete(repo)
        print("Deleted repos!")

        print("Starting search!\n")
        more_repos = True
        next_repo_page = None
        while more_repos:
            repo_search = get_repos(
                language, labels=config.LABELS, after=next_repo_page
            )
            for repo in repo_search.search.nodes:
                if not repo["isArchived"] and repo["issues"]["totalCount"] > 0:
                    session.add(
                        Repo(
                            repo_id=repo["databaseId"],
                            name=repo["nameWithOwner"],
                            description=repo["description"],
                            url=repo["url"],
                            language=repo["primaryLanguage"]["name"],
                            created_at=datetime.strptime(
                                repo["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
                            ),
                            total_stars=repo["stargazers"]["totalCount"],
                        )
                    )
                    more_issues = True
                    next_issues_page = None
                    while more_issues:
                        issues = get_issues(
                            repo["nameWithOwner"],
                            labels=config.LABELS,
                            after=next_issues_page,
                        )
                        for issue in issues.repository.issues.nodes:
                            if issue["assignees"]["totalCount"] == 0:
                                print(repo["nameWithOwner"], issue["title"])
                                issue_labels = [
                                    label["name"] for label in issue["labels"]["nodes"]
                                ]
                                session.add(
                                    Issue(
                                        issue_id=issue["databaseId"],
                                        repo_id=repo["databaseId"],
                                        title=issue["title"],
                                        description=issue["bodyText"],
                                        url=issue["url"],
                                        category=get_issue_category(issue_labels),
                                        created_at=datetime.strptime(
                                            issue["createdAt"], "%Y-%m-%dT%H:%M:%SZ"
                                        ),
                                        total_comments=issue["comments"]["totalCount"],
                                    )
                                )
                        more_issues = issues.repository.issues.pageInfo.hasNextPage
                        if more_issues:
                            next_issues_page = (
                                issues.repository.issues.pageInfo.endCursor
                            )
            more_repos = repo_search.search.pageInfo.hasNextPage
            if more_repos:
                next_repo_page = repo_search.search.pageInfo.endCursor
        print("Updating repository for %s" % language)
        session.commit()

    session.close()
