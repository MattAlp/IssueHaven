from github import Github
import config
import requests_cache
import time
import json
import os


def get_top_repos(language: str, limit: int = 1, update: bool = False):
    client = Github(config.TOKEN, per_page=100)
    repos = client.search_repositories("stars:>1 language:%s" % language)

    if update:
        collected_repos = []

    for repo in repos[:limit]:  # TODO add proper limiting code, this doesn't work when limit is set to 0
        t = time.time()
        overlap = list(set(label.name for label in repo.get_labels()) & set(config.CODE))
        if len(overlap) != 0:
            print(repo.full_name, language, repo.stargazers_count, overlap)
            if update:
                collected_repos.append({"name": repo.full_name, "code_labels": overlap, "chore_labels": []})
        time.sleep(max(0.0, (2 / 30.0) - (time.time() - t)))

    if update:
        file = open("repos.json", "r+")
        if os.stat("repos.json").st_size == 0:
            data = {"repos": []}
        else:
            data = json.load(file)
        data["repos"] += collected_repos
        json.dump(data, file, indent=4)
        file.close()


if __name__ == "__main__":
    requests_cache.install_cache("top_repos_cache", backend="sqlite", expire_after=3600)

    languages = config.LANGUAGES  # Want to run through some other languages? Just change this to a custom list!

    for language in config.LANGUAGES:
        get_top_repos(language, limit=200, update=True)