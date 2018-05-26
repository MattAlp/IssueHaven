import os


# "Help wanted" is intentionally not included, far too vague
# Same applies for the "Bug" label
CODE = ["first-timers-only", "low-hanging-fruit", "easy", "beginner", "good first issue", "easy-pick",
        "starter bug", "good-first-issue", "jump in", "newcomer", "beginner friendly", "e-easy", "starter",
        "newbie", "easy fix", "easy-fix", "good for new contributors", "contribution-starter", "good for beginner",
        "good-for-beginner", "first timers only", "first time contributor"]

DOCS = ["translation", "documentation", "docs", "chore", "localization"]

LANGUAGES = ["python", "typescript", "javascript", "ruby", "php", "c++", "go", "c#", "java"]

TOKEN = os.getenv("TOKEN")

SEARCH_PER_PAGE = 100

DEFAULT_RESULTS_PER_PAGE = 30

PROJECT_ROOT = os.path.dirname(__file__)

DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")

DATABASE_URL = "sqlite:///" + os.path.join(DATA_FOLDER, "github_data.db")
