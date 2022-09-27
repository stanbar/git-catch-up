# git-changes-tracker

Track daily changes in a directory using git.

# Usage

1. Activate virtual env using `pipenv shell`
2. Change to the target repo directory
3. Run `python <path to git-changes-tracker>/main.py`

# Installation

1. Bundle executable. Run `pyinstaller --onefile main.py`
2. Move executable to `$PATH`. Run `mv dist/main /usr/local/bin/git-catch-up` (or other OS specific location).
