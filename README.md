# git-catch-up

Catch up uncommited files keeping modification date.

# Environment

1. Set virtual environment `pipenv shell`.

# Installation

1. Bundle executable. Run `pyinstaller --onefile main.py`.
2. Move executable to `$PATH`. Run `mv dist/main /usr/local/bin/git-catch-up` (or other OS specific location).

# Usage

Execute `git-catch-up` within the target repository's directory.
