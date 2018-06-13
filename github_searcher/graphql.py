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
    issues(first: 100, labels: {labels}, after: {after}, states:OPEN){{
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


def get_issues(name: str, owner: str, labels: List[str], after: str = None):
    if after is not None:
        after = "\"" + after + "\""
    else:
        after = "null"
    headers = {'Authorization': 'token %s' % config.TOKEN}
    generated_query = query.format_map(locals()).replace("'", "\"")
    query_results = requests.post(GRAPHQL_URL, json={"query": generated_query}, headers=headers).json()
    return query_results


if __name__ == "__main__":
    data = get_issues(name="ansible", owner="ansible", labels=["docs"])
    for issue in data["data"]["repository"]["issues"]["nodes"]:
        print(issue["title"])
    print("-----------------------")
    if data["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]:
        data = get_issues(name="ansible", owner="ansible", after=data["data"]["repository"]["issues"]["pageInfo"]["endCursor"], labels=["docs"])
    for issue in data["data"]["repository"]["issues"]["nodes"]:
        print(issue["title"])