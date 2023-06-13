#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Clone Repos for clcreative
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
    # Clone Repositories for clcreative
    # https://docs.github.com/en/rest/reference/repos#list-organization-repositories
    # --
    try:
        repos = getRepos(github_token, 'clcreative')

        cloned_repos = []

        if repos is not None:
            for repo in repos:
                # set repo path on local workstation
                repo_path = f'{ Path.home() }/projects/{repo["owner"]["login"]}/{repo["name"]}'

                # when repo is not existing
                if not os.path.exists(repo_path):
                    # print(f"  {repo['name']} - {repo['description']}")
                    os.system(f'git clone git@github.com:{repo["owner"]["login"]}/{repo["name"]}.git {repo_path}')
                    cloned_repos.append(repo)

            # Show how many repos are cloned
            print(f"\033[32mcloned: {len(cloned_repos)}\033[0m")

    except Exception as e:
        print(f"error: {e}")
