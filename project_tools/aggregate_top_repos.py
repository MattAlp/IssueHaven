from github import Github
import config
import time
import json
import os


def get_top_repos(language: str, limit: int = 1, update: bool = False):
    client = Github(config.TOKEN, per_page=100)
    repos = client.search_repositories("stars:>1 language:%s" % language)

    if update:
        collected_repos = []

    for repo in repos[:limit]:  # TODO add proper limiting code, this doesn't work when limit is set to 0
        last_time = time.time()
        labels = repo.get_labels()
        code_overlap = list(set(label.name for label in labels) & set(config.CODE))
        chore_overlap = list(set(label.name for label in labels) & set(config.CHORE))

        if len(code_overlap) != 0 or len(chore_overlap) != 0:
            info = "Repo:%s, Stars:%s, Code Labels:%s, Chore Labels:%s"
            print(info % (repo.full_name, repo.stargazers_count, code_overlap, chore_overlap))
            if update:
                collected_repos.append({"name": repo.full_name, "code_labels": code_overlap,
                                        "chore_labels": chore_overlap})
        time.sleep(max(0.0, (2 / 30.0) - (time.time() - last_time)))

    # This code doesn't work completely and requires that a repos.json file is made with {"repos":[]} as the content
    # TODO fix this
    if update:
        file = open("repos.json", "r+")
        if os.stat("repos.json").st_size == 0:
            data = {"repos": []}
        else:
            data = json.load(file)
        data["repos"] += collected_repos
        file.seek(0)
        json.dump(data, file, indent=4)
        file.close()


if __name__ == "__main__":
    languages = config.LANGUAGES  # Want to run through some other languages? Just change this to a custom list!
    for language in languages:
        get_top_repos(language, limit=200, update=True)
