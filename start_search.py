from core import search_issues, Config
from core.models import Issue, engine, Base

if __name__ == "__main__":
    for language in Config.LANGUAGES:
        for label in Config.CODE:
            search_issues(label, language)
    # for label in Config.DOCS:
    #     search_issues(label, "any")
    exit()
