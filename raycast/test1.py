#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title test1
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon https://avatars.githubusercontent.com/u/97734037?s=200&v=4

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

from dotenv import load_dotenv
import os
from repos import getRepos


load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

ignored_folders = [
    '.git',
    '.DS_Store',
    '.obsidian',
]


if __name__ == "__main__":
    try:
        # List all repos for an organization from GitHub
        # https://docs.github.com/en/rest/reference/repos#list-organization-repositories

        repos = getRepos(github_token, 'clcreative')
        if repos is not None:
            for repo in repos:
                print(f"{repo['name']}, {repo['owner']['login']}, {repo['description']}")
        else:
            raise Exception("repos is None")

        # Sum all repos
        print(f"---\nTotal: {len(repos)}")

    except Exception as e:
        print(f"error: {e}")
