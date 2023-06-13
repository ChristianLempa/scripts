#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Check Repos for clcreative
# @raycast.mode inline

# Optional parameters:
# @raycast.icon https://avatars.githubusercontent.com/u/97734037?s=200&v=4

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

from dotenv import load_dotenv
import os
from pathlib import Path
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
        # Get all repos for an organization from GitHub
        # https://docs.github.com/en/rest/reference/repos#list-organization-repositories

        repos = getRepos(github_token, 'clcreative')
        repos_need_changes = []
        repos_not_cloned = []

        if repos is not None:
            for repo in repos:
                # set repo path on local workstation
                repo_path = f'{ Path.home() }/projects/{repo["owner"]["login"]}/{repo["name"]}'

                # when repo is existing
                if os.path.exists(repo_path):
                    try:
                        os.chdir(repo_path)

                        # check if there are any changes
                        # changes = os.system('git diff --exit-code --quiet')

                        # check if there are any changes to the repo, and if something needs to be pulled or committed
                        changes = os.system('git diff --exit-code --quiet')

                        if changes != 0:
                            # print(f" {repo['name']} - {repo['description']}")
                            repos_need_changes.append(repo)
                        else:
                            pass
                            # print(f" {repo['name']} - {repo['description']}")

                    except Exception as e:
                        print(f"error: {e}")
                else:
                    # print(f"  {repo['name']} - {repo['description']}")
                    repos_not_cloned.append(repo)

        # Check orphaned repos
        repos_orphaned = []

        # read all folders in projects folder
        for item in os.listdir(f'{ Path.home() }/projects/clcreative'):
            # check if item is in repos list, and if item is not in ignored folders
            if item not in [repo['name'] for repo in repos] and item not in ignored_folders:
                repos_orphaned.append(item)

        # Get Information about all Repos
        print(f"Repos: {len(repos)} \033[31m(u: {len(repos_need_changes)}, m: {len(repos_not_cloned)}, o: {len(repos_orphaned)})\033[0m")

    except Exception as e:
        print(f"error: {e}")
