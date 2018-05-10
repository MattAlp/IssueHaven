from os import environ

class Config:
    CODE = ["first-timers-only", "low-hanging-fruit", "easy", "beginner", "good first issue", "easy-pick",
            "starter bug", "good-first-issue", "jump in", "newcomer", "beginner friendly", "e-easy", "starter",
            "newbie", "easy fix", "easy-fix", "good for new contributors", "contribution-starter", "good for beginner",
            "good-for-beginner", "first timers only", "first time contributor", "help wanted"]

    DOCS = ["localization", "documentation", "docs", "chore"]  # TODO revise all these tags

    GFX = ["graphics", "design", "ux", "ui", "ui/ux"]  # "copy" tag?

    LANGUAGES = ["python", "javascript", "ruby", "php", "c++", "go", "c#", "ruby", "java"]

    # TODO are the labels caps-sensitive on GitHub -> Nope

    CATEGORIES = {"newbie": CODE, "docs": DOCS, "graphics": GFX}

    USER = environ.get("USERNAME")
    PASSWORD = environ.get("PASSWORD")

    MAX_RESULTS = 1020
    RESULTS_PER_PAGE = 30
    MAX_PAGES = MAX_RESULTS / RESULTS_PER_PAGE
    SECONDS_PER_REQUEST = 2.1  # Just a little over 2

    ISSUES_URL = "https://api.github.com/search/issues"


