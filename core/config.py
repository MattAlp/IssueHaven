from os import environ


class Config:
    labels = ["first-timers-only", "low-hanging-fruit", "easy", "beginner", "good first issue", "easy-pick",
              "starter bug", "good-first-issue", "jump in", "newcomer", "beginner friendly"]
    languages = ["python", "javascript", "ruby", "php", "c++", "go", "c#", "ruby", "java"]
    # labels = ["first-timers-only"]
    # languages = ["python"]
    user = environ.get("USERNAME")
    password = environ.get("PASSWORD")
