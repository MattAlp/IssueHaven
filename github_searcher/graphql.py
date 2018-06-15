import requests
import config


from typing import List


GRAPHQL_URL = "https://api.github.com/graphql"
REPO_ISSUES_QUERY = """
{{
  repository(owner: "{owner}", name: "{name}") {{
    databaseId
    primaryLanguage {{
      name
    }}
    issues(first: 100, labels: {labels}, after: {endCursor}, states:OPEN){{
      nodes{{
        title
        url
      }}
      pageInfo{{
        hasNextPage
        endCursor
      }}
    }}
  }}
}}
"""


class GraphQLQuery(object):
    query_base = ""
    json = ""
    headers = {'Authorization': 'token %s' % config.TOKEN}

    def __init__(self, **kwargs):
        self.json = requests.post(GRAPHQL_URL, json={"query": self.query_base.format_map(kwargs).replace("'", "\"")},
                                  headers=self.headers).json()["data"]


class RepoIssuesQuery(GraphQLQuery):
    query_base = REPO_ISSUES_QUERY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.issues = type('', (), {})()  # https://stackoverflow.com/questions/2280334/shortest-way-of-creating-an-object-with-arbitrary-attributes-in-python
        self.issues.nodes = self.json["repository"]["issues"]["nodes"]
        self.issues.pageInfo = self.json["repository"]["issues"]["pageInfo"]
        self.repo = type('', (), {})()
        self.repo.id = self.json["repository"]["databaseId"]
        self.repo.language = self.json["repository"]["primaryLanguage"]["name"]


def get_issues(name: str, owner: str, labels: List[str], endCursor: str = None):
    if endCursor is not None:
        endCursor = "\"" + endCursor + "\""
    else:
        endCursor = "null"
    headers = {'Authorization': 'token %s' % config.TOKEN}
    generated_query = REPO_ISSUES_QUERY.format_map(locals()).replace("'", "\"")
    query_results = requests.post(GRAPHQL_URL, json={"query": generated_query}, headers=headers).json()["data"]
    return query_results


if __name__ == "__main__":
    r = RepoIssuesQuery(name="ansible", owner="ansible", labels=["docs"], endCursor="null")
    print(r.repo.language)