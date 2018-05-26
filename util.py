from github import Github, enable_console_debug_logging
from github.GithubException import UnknownObjectException
import config
import json


if __name__ == "__main__":
    print("[INFO] Token: " + config.TOKEN)
    # enable_console_debug_logging()
    client = Github(config.TOKEN, per_page=100)
    with open('repos.json', "r") as f:
        data = json.load(f)
        for json_repo in data["repos"]:
            repo = client.get_repo(json_repo["name"])
            print("[INFO] Scanning repo %s" % repo.html_url)
            # print(labels)
            for label in json_repo["code_labels"]:
                try:
                    issues = repo.get_issues(labels=[repo.get_label(label)], state="open", assignee="none")
                    for index, issue in enumerate(issues):
                        print(issue.title, label, issue.comments)
                        # if index + 1 == 30:
                        #     break
                except UnknownObjectException:
                    print("[ERROR] Label %s wasn't found in repo %s" % (label, repo))
