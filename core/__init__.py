from core.config import Config
import time
import requests

#  TODO fix the organization of my modules and files, they're not structured or organized properly at all

MAX_RESULTS = 1020
RESULTS_PER_PAGE = 30

MAX_PAGES = MAX_RESULTS / RESULTS_PER_PAGE
SECONDS_PER_REQUEST = 2.1

ISSUES_URL = "https://api.github.com/search/issues"


def generate_search_string():
    searches = []
    for language in Config.languages:
        for label in Config.labels:
            searches.append("""label:"%s" language:%s state:open""" % (label, language))
    return searches


def search_issues(label: str, language: str):
    page_count = 1
    i = 1
    while i <= page_count:
        payload = {"q": """label:"%s" language:%s state:open""" % (label, language), "page": i}
        t = time.time()
        current_page = requests.get(ISSUES_URL, auth=(Config.user, Config.password), params=payload).json()
        data = current_page["items"]
        total_issues = current_page["total_count"]

        print("Total issue count is %d, of which %d are shown" % (total_issues, min(MAX_RESULTS, int(total_issues))))
        if i == 1:
            page_count = int(min(MAX_PAGES, int(total_issues / RESULTS_PER_PAGE)))
        #  Repository has language related things, issue knows nothing of the related language
        #  Score is 1 for all items unless a search string is issued
        for issue in data:
            print("Issue ID [%i], titled %s" %(issue['id'], issue['title']))
        print("Sleeping for %f" %(SECONDS_PER_REQUEST - (time.time() - t)))

        print("Total results printed thus far: %d" % (i * RESULTS_PER_PAGE))
        i += 1

        try:
            time.sleep(SECONDS_PER_REQUEST - (time.time() - t))
        except ValueError:
            print("Request took longer than 2 seconds")
