import requests
import requests_cache
import config
import json
import os

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
    requests_cache.install_cache("GraphQL_Cache", backend="sqlite", expire_after=3600)
    with open(os.path.join(config.PROJECT_ROOT, "repos.json"), "r") as f:
        repos = json.load(f)
        for json_repo in repos["repos"]:
            owner, name = json_repo["name"].split("/")
            print(name)
            data = get_issues(name=name, owner=owner, labels=json_repo["code_labels"] + json_repo["chore_labels"])
            while True:
                for issue in data["repository"]["issues"]["nodes"]:
                    print("\t" + issue["title"])
                if not data["repository"]["issues"]["pageInfo"]["hasNextPage"]:
                    break
                else:
                    data = get_issues(name=name, owner=owner, labels=json_repo["code_labels"], endCursor=data["repository"]["issues"]["pageInfo"]["endCursor"])