import os


# "Help wanted" is intentionally not included, far too vague
# Same applies for the "Bug" label
CODE = ["first-timers-only", "low-hanging-fruit", "easy", "beginner", "good first issue", "easy-pick",
        "starter bug", "good-first-issue", "jump in", "newcomer", "beginner friendly", "e-easy", "starter",
        "newbie", "easy fix", "easy-fix", "good for new contributors", "contribution-starter", "good for beginner",
        "good-for-beginner", "first timers only", "first time contributor"]

LANGUAGES = ["python", "typescript", "javascript", "ruby", "php", "c++", "go", "c#", "java"]

TOKEN = os.getenv("TOKEN")
