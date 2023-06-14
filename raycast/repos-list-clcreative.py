#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title List Repos for clcreative
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon https://avatars.githubusercontent.com/u/97734037?s=200&v=4

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

from dotenv import load_dotenv
import os
from github import Github


load_dotenv()

g = Github(os.getenv("GITHUB_TOKEN"))

ignored_folders = [
    '.git',
    '.DS_Store',
    '.obsidian',
]

if __name__ == "__main__":
    try:
        repos = g.get_organization('clcreative').get_repos()

        for repo in repos:
            print(repo.name)

        print(f"Total repos: {repos.totalCount}")

    except Exception as e:
        print(f"error: {e}")
