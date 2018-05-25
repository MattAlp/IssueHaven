from github import Github, enable_console_debug_logging
import config
import json


if __name__ == "__main__":
    enable_console_debug_logging()
    client = Github(config.TOKEN, per_page=100)
    with open('repos.json', "r") as f:
        data = json.load(f)
        for json_repo in data["repos"]:
            repo = client.get_repo(json_repo["name"])

            labels = [label for label in repo.get_labels() if label.name in json_repo["code_labels"]]
            # print(labels)
            for label in labels:
                for issue in repo.get_issues(labels=[label], state="open", assignee="none")[:30]:
                    print(issue.title, label.name, issue.comments)