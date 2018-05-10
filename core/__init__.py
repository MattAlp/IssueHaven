from core.config import Config
from core.models import Issue
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
import time
import requests

#  TODO get proper logging going ASAP


def generate_search_string():
    searches = []
    for language in Config.LANGUAGES:
        for label in Config.CODE:
            searches.append("""label:"%s" language:%s state:open""" % (label, language))
    return searches


def search_issues(label: str, language: str, session: Session):
    print("[INFO] Searching for all issues with label %s written in %s" % (label, language))
    search_string = """label:"%s" language:%s state:open""" % (label, language)
    page_count = 1
    i = 1

    while i <= page_count:
        payload = {"q": search_string, "page": i}
        t = time.time()
        current_page = requests.get(Config.ISSUES_URL, auth=(Config.USER, Config.PASSWORD), params=payload).json()
        data = current_page["items"]
        total_issues = current_page["total_count"]

        print("[INFO] Total issue count is %d, of which %d are shown" % (total_issues, min(Config.MAX_RESULTS, total_issues)))
        if i == 1:
            page_count = int(min(Config.MAX_PAGES, int(total_issues / Config.RESULTS_PER_PAGE)))

        #  Repository has language related things, issue knows nothing of the related language
        #  Score is 1 for all items unless a search string is issued

        for issue in data:
            print("[INFO] Issue %i, titled %s" % (issue['id'], issue['title']))

            if not session.query(exists().where(Issue.id == issue['id'])).scalar():
                session.add(Issue(language=language, id=issue['id'], html_url=issue['html_url'], category="CODE"))
            #  TODO category needs to be restructured and automatically derived
            # session.commit()
        print("[INFO] Sleeping for %f" % (Config.SECONDS_PER_REQUEST - (time.time() - t)))
        print("[INFO] Total results printed thus far: %d" % (i * Config.RESULTS_PER_PAGE))
        i += 1

        try:
            time.sleep(Config.SECONDS_PER_REQUEST - (time.time() - t))
        except ValueError:
            print("[DEBUG] Request took longer than 2 seconds")
            time.sleep(Config.SECONDS_PER_REQUEST)
        print("[INFO] Committing to DB")
        session.commit()