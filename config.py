import os

DEV_MODE = False  # TODO add custom configs based on DEV_MODE variable


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

TOKEN = os.getenv("TOKEN")

HEADER = {"Authorization": "token %s" % TOKEN}

SEARCH_PER_PAGE = 100

DEFAULT_RESULTS_PER_PAGE = 30

PROJECT_ROOT = os.path.dirname(__file__)

DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")

DATABASE_URL = "sqlite:///" + os.path.join(DATA_FOLDER, "github_data.db")

GRAPHQL_API_URL = "https://api.github.com/graphql"
