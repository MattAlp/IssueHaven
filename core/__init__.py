from core.config import Config
import requests
MAX_RESULTS = 1020
SECONDS_PER_REQUEST = 2
RESULTS_PER_PAGE = 30


def generate_searches():
    searches = []
    for language in Config.languages:
        for label in Config.labels:
            searches.append("""label:"%s" language:%s state:open""" % (label, language))
    return searches
