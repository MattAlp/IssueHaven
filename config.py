import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=True), override=True)

DEV_MODE = os.getenv("DEV_MODE") == "True"  # dotenv values are strings

PROJECT_ROOT = os.path.dirname(__file__)

if DEV_MODE:
    DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
    DATABASE_URL = "sqlite:///" + os.path.join(
        DATA_FOLDER, "github_data.db"
    )  # there might be a better way to do this
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

TOKEN = os.getenv("TOKEN")

CONTRIBUTE_LINK = os.getenv("CONTRIBUTE_LINK")

DONATE_LINK = os.getenv("DONATE_LINK")

REFER_LINK = os.getenv("REFER_LINK")

LEARN_LINK = os.getenv("LEARN_LINK")

HEADER = {"Authorization": "token %s" % TOKEN}

# "Help wanted" is intentionally not included, far too vague
# Same applies for the "Bug" label
CODE = [
    "first-timers-only",
    "low-hanging-fruit",
    "easy",
    "beginner",
    "good first issue",
    "easy-pick",
    "starter bug",
    "good-first-issue",
    "jump in",
    "newcomer",
    "beginner friendly",
    "e-easy",
    "starter",
    "newbie",
    "easy fix",
    "easy-fix",
    "good for new contributors",
    "contribution-starter",
    "good for beginner",
    "good-for-beginner",
    "first timers only",
    "first time contributor",
    "exp/beginner",
    "jump-in",
    "good-beginner-issue",
    "stat:contributions welcome",
    "level:starter",
    "good first bug",
    "difficulty/low",
    "difficulty/newcomer",
    "for beginners",
]

CHORE = ["translation", "documentation", "docs", "chore", "localization"]

SPECIAL = []  # i.e. Hacktoberfest and other code-sprint-like events

CATEGORIES = {
    "chore": CHORE,
    "code": CODE,
    "special": SPECIAL,
}  # Categories are iterated over first to last (highest to lowest priority)

LABELS = sorted({x for v in CATEGORIES.values() for x in v})  # From Stack Overflow

LANGUAGES = [
    "javascript",
    "python",
    "java",
    "ruby",
    "php",
    "cpp",
    "csharp",
    "go",
    "typescript",
    "swift",
    "scala",
    "objc",
]

MAPPINGS = {
    "csharp": "C#",
    "cpp": "C++",
    "cplusplus": "C++",
    "objectivec": "Objective-C",
    "objc": "Objective-C",
    "py": "Python",
    "python": "Python",
    "java": "Java",
    "ruby": "Ruby",
    "go": "Go",
    "swift": "Swift",
    "scala": "Scala",
    "rb": "Ruby",
    "js": "JavaScript",
    "ts": "TypeScript",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "php": "PHP",
}

# TODO add custom colour support via CSS to issue pages

COLOUR_MAPPINGS = {
    "JavaScript": "F0DB4F",
    "Python": "#306998",
    "Java": "#FF8C00",
    "Ruby": "#CC342D",
    "PHP": "#8892BE",
    "C++": "#ffffff",
    "C#": "#ffffff",
    "Go": "#34A853",
    "TypeScript": "#007ACC",
    "Swift": "#FC3F27",
    "Scala": "#371777",
    "Objective-C": "#8E43E7",
}

SEARCH_PER_PAGE = 100

DEFAULT_RESULTS_PER_PAGE = 30

GRAPHQL_API_URL = "https://api.github.com/graphql"
