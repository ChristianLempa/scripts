#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title List all my GitHub Repos
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon https://avatars.githubusercontent.com/u/28359525?v=4

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

from dotenv import load_dotenv
import os
from pathlib import Path
from github import Github
from git import Repo
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
        missing_repos = []

        if repos is not None:
            for repo in repos:
                # set repo path on local workstation
                repo_path = f'{ Path.home() }/projects/{repo.owner.login}/{repo.name}'

                # when repo is not existing
                if not os.path.exists(repo_path):
                    missing_repos.append(repo.name)
                    print(f"\033[0;31m●\033[0m {repo.name} (missing)")
                else:
                    current_repo = Repo(f"{ Path.home() }/projects/{repo.owner.login}/{repo.name}")

                    # check if repo has untracked files
                    if current_repo.untracked_files:
                        print(f"\033[0;33m●\033[0m {repo.name} (untracked files)")
                    elif current_repo.is_dirty():
                        print(f"\033[0;33m●\033[0m {repo.name} (dirty))")
                    else:
                        print(f"\033[0;32m●\033[0m {repo.name}")

    except Exception:
        traceback.format_exc()
