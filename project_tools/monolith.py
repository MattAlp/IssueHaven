import json
import time
import config
import requests
from typing import List


class PyJSON(object):

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
        nameWithOwner
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
        title
        bodyText
        url
        assignees{
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


if __name__ == "__main__":
    print("Config Token: %s" % config.TOKEN)
    for language in config.LANGUAGES:
        print("\nLanguage: " + language)
        more_repos = True
        next_repo_page = None
        while more_repos:
            repo_search = get_repos(
                language, labels=config.LABELS, after=next_repo_page
            )
            for repo in repo_search.search.nodes:
                if repo["issues"]["totalCount"] > 0:
                    more_issues = True
                    next_issues_page = None
                    while more_issues:
                        issues = get_issues(
                            repo["nameWithOwner"],
                            labels=config.LABELS,
                            after=next_issues_page,
                        )
                        for issue in issues.repository.issues.nodes:
                            print(repo["nameWithOwner"], issue["title"])
                        more_issues = issues.repository.issues.pageInfo.hasNextPage
                        if more_issues:
                            next_issues_page = (
                                issues.repository.issues.pageInfo.endCursor
                            )
            more_repos = repo_search.search.pageInfo.hasNextPage
            if more_repos:
                next_repo_page = repo_search.search.pageInfo.endCursor
