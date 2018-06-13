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
    }}
  }}
}}
"""


def get_issues(name: str, owner: str, labels: List[str], next: str = False):
    headers = {'Authorization': 'token %s' % config.TOKEN}
    generated_guery = query.format_map(locals()).replace("'", "\"")
    # print({"query": query.format_map(kwargs)})
    print(requests.post(GRAPHQL_URL, json={"query": generated_guery}, headers=headers).json())


if __name__ == "__main__":
    with open(os.path.join(config.PROJECT_ROOT, "repos.json"), "r") as f:
        data = json.load(f)
        for json_repo in data["repos"]:
            owner, name = json_repo["name"].split("/")
            get_issues(owner=owner, name=name, labels=str(json_repo["code_labels"]))