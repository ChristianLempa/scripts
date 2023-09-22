#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Clean all my orphaned GitHub Repos
# @raycast.mode compact

# Optional parameters:
# @raycast.icon https://avatars.githubusercontent.com/u/28359525?v=4
# @raycast.needsConfirmation true

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

from dotenv import load_dotenv
import os
from pathlib import Path
from github import Github
import traceback


load_dotenv()

g = Github(os.getenv("GITHUB_TOKEN"))

ignored_folders = [
    '.git',
    '.DS_Store',
    '.obsidian',
]


if __name__ == "__main__":
    try:
        repos = g.get_user('christianlempa').get_repos()
        orphaned_repos = []

        if repos is not None:

            # check all repos on local workstation
            # get all repos in projects folder
            for repo in os.listdir(f'{ Path.home() }/projects/christianlempa'):
                # check if repo is not in ignored folders
                if repo not in ignored_folders:
                    # check if repo is not in github
                    if repo not in [r.name for r in repos]:
                        orphaned_repos.append(repo)

            if len(orphaned_repos) > 0:
                # delete oraphned repos
                for repo in orphaned_repos:
                    os.system(f'rm -rf { Path.home() }/projects/christianlempa/{repo}')
                print(f"Deleted {len(orphaned_repos)} orphaned repos.")
                exit(0)
            else:
                print("No orphaned repos found.")
                exit(0)
        else:
            print("Error: No repos found in organization")
            exit(1)

    except Exception:
        traceback.format_exc()
        exit(1)
