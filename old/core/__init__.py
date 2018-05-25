from core.config import Config
from core.models import Issue
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from math import ceil, log10, sqrt
import time
import requests
import datetime


#  TODO get proper logging going ASAP

def search_issues(label: str, language: str, category: str, session: Session):
    print("[DEBUG] Searching for all issues with label %s written in %s" % (label, language))

    search_string = """label:"%s" language:%s state:open no:assignee""" % (label, language)
    page_count = 1
    page_index = 1
    issue_count = 0

    while page_index <= page_count:
        payload = {"q": search_string, "page": page_index}
        t = time.time()
        current_page = requests.get(Config.ISSUES_URL, auth=(Config.USER, Config.PASSWORD), params=payload).json()
        data = current_page["items"]
        total_issues = current_page["total_count"]

        if page_index == 1:
            page_count = int(min(Config.MAX_PAGES, ceil(total_issues / Config.RESULTS_PER_PAGE)))
            print("[INFO] Total issue count is %d, of which %d are shown" % (total_issues,
                                                                             min(Config.MAX_RESULTS, total_issues)))

        for issue in data:

            issue_count += 1
            id = issue['id']
            html_url = issue['html_url']
            title = issue['title']
            comments = issue['comments']
            timestamp = datetime.datetime.strptime(issue['updated_at'], '%Y-%m-%dT%H:%M:%SZ')

            print("[INFO] Issue %i, titled '%s'" % (id, title))

            if not session.query(exists().where(Issue.id == id)).scalar():
                session.add(Issue(language=language, id=id, title=title, html_url=html_url,
                                  category=category, timestamp=timestamp,
                                  score=(max(1.0, ceil(log10(total_issues - issue_count + 1.0)))) * sqrt(comments + 1.0)
                                  ))

        print("[INFO] Total results printed thus far: %d" % issue_count)
        page_index += 1
        print("[INFO] Committing to DB")
        session.commit()

        print("[INFO] Sleeping for %f" % (Config.SECONDS_PER_REQUEST - (time.time() - t)))
        try:
            time.sleep(Config.SECONDS_PER_REQUEST - (time.time() - t))
        except ValueError:
            print("[DEBUG] Request + commit took longer than 2 seconds")
            time.sleep(Config.SECONDS_PER_REQUEST)
