Issue Haven
===========
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![HitCount](http://hits.dwyl.io/MattAlp/IssueHaven.svg)](http://hits.dwyl.io/MattAlp/IssueHaven)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/MattAlp)


About
-----

Contributing to Open Source projects shouldn't be difficult for first-timers, but finding projects that provide contributors with a learning experience is often a daunting and difficult task.

**Issue Haven** addresses these problems by giving users an automatically curated and categorized catalog of available issues from popular repositories on Github, sorted by language and type.

In doing so, it aims to greatly lower the barriers to OSS contributions by connecting motivated contributors with welcoming projects that could use their help.

How is this different from other approaches to the problem?
-----------------------------------------------------------

Currently, there are multiple other projects that attempt to address this issue:
1. [Code Triage](https://www.codetriage.com/)
   * Code Triage maintains a list of recently opened issues in popular repositories and sends out emails to developers who have expressed interest in the project.

2. [First Timers Only](https://www.firsttimersonly.com/)
   * First Timers Only is a campaign that encourages projects to use the label "first-timers-only" to signify to new contributors that the issue is of an appropriate skill level and reserved for them.

3. [Up for Grabs](https://up-for-grabs.net/)
   * Up for Grabs is a maintained list of repositories that have curated tasks specifically for new contributors.
   
**Issue Haven** is set apart from existing solutions in several ways:

1. Unlike the aforementioned services, Issue Haven automatically compiles a list of suitable repositories, and requires no maintenance; repositories must have at least 500 stars and use any of the predefined labels to be automatically recorded into Issue Haven

2. **Issue Haven** maintains an extensive list of issue labels deemed beginner-friendly (see the [configuration](config.py)), capturing a variety of projects without forcing them to adhere to a new set of conventions (i.e. the Hacktoberfest or First-Timers-Only tag)

3. **Issue Haven** sorts issues into several categories (i.e. programming-related & documentation-related tasks) to differentiate issues for contributors with different skill sets; whether one's skilled in programming, writing up swathes of documentation, or graphics design, **Issue Haven** makes it easy to quickly find a suitable issue.

How does it work?
------ 
Issue Haven consists of two main components:

1. An issue aggregation script named [Monolith](project_tools/monolith.py), which queries the Github API to find open issues appropriate for beginners, and sorts them into various categories 
2. A [Flask server](server) responsible for serving up the front end, which allows users to browse through the aggregated issues

#### On Monolith 
Monolith functions by going through a list of predefined issue labels and querying the Github API for repositories with *500 or more stars* that use any of the labels; this attempts to ensure that issues are pulled from projects with relatively healthy codebases, and that issues are geared towards beginners.

After obtaining a list of repositories that fit the criteria, the script iterates through the labeled issues in the repository and categorizes them (i.e. programming vs documentation), and stores them in a database.

#### Stack Information
The public instance of Issue Haven runs on a Flask / Gunicorn / NGINX stack.

Other Information
-----------------

If you're interested in contributing, please open an issue with the appropriate labels prior to working on any changes.

This project uses the [black](https://github.com/ambv/black) code formatter; run ```black``` in the project directory before submitting a PR.

If you want to support this project, consider donating via [PayPal](https://paypal/me/MattAlp).