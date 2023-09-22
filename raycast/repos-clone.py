#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Clone all my GitHub Repos
# @raycast.mode compact

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
    # Clone Repositories for christianlempa
    # https://docs.github.com/en/rest/reference/repos#list-organization-repositories
    # --
    try:
        repos = g.get_user('christianlempa').get_repos()
        cloned_repos = []

        if repos is not None:
            for repo in repos:
                # set repo path on local workstation
                repo_path = f'{ Path.home() }/projects/{repo.owner.login}/{repo.name}'

                # when repo is not existing
                if not os.path.exists(repo_path):
                    # print(f"  {repo['name']} - {repo['description']}")
                    Repo.clone_from(repo.ssh_url, repo_path)
                    cloned_repos.append(repo.name)

            if len(cloned_repos) > 0:
                print(f"cloned {len(cloned_repos)} repos.")
            else:
                print("all repos are already cloned.")
        else:
            print("error: no repos found in organization")
            exit(1)

    except Exception:
        traceback.format_exc()
        exit(1)
