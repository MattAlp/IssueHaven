import requests
import config
import json
import os

from typing import List


GRAPHQL_URL = "https://api.github.com/graphql"
query = """
{{
  repository(owner: "{owner}", name: "{name}") {{
    databaseId
    primaryLanguage {{
      name
    }}
    issues(first: 100, labels: {labels}, states:OPEN){{
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


def get_issues(name: str, owner: str, labels: List[str], next: str = None):
    headers = {'Authorization': 'token %s' % config.TOKEN}
    generated_query = query.format_map(locals()).replace("'", "\"")
    query_results = requests.post(GRAPHQL_URL, json={"query": generated_query}, headers=headers).json()
    print(query_results)


if __name__ == "__main__":
    get_issues(name="ansible", owner="ansible", labels=["doc"])
    # with open(os.path.join(config.PROJECT_ROOT, "repos.json"), "r") as f:
    #     data = json.load(f)
    #     for json_repo in data["repos"]:
    #         owner, name = json_repo["name"].split("/")
    #         get_issues(owner=owner, name=name, labels=str(json_repo["code_labels"]))