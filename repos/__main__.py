#!/usr/bin/env python3

import os
from pathlib import Path
import typer
import requests

app = typer.Typer()

ignored_folders = [
    '.git',
    '.DS_Store',
    '.obsidian',
]


def getReposFromPage(github_token: str, organization: str, page: int):
    # Get all repos from a specific page for an organization from GitHub.
    # https://docs.github.com/en/rest/reference/repos#list-organization-repositories
    try:
        url = f"https://api.github.com/orgs/{organization}/repos"
        payload = {}
        headers = {
            'Authorization': f'token {github_token}'
        }
        params = {
            'per_page': '100',
            'page': page,
            'sort': 'full_name'
        }

        response = requests.request("GET", url, headers=headers, data=payload, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"status code {response.status_code}")
    except Exception as e:
        print(f"error: {e}")
        return None


def getRepos(github_token: str, organization: str):
    # Get all repos for an organization from GitHub by iterating over all pages.
    # https://docs.github.com/en/rest/reference/repos#list-organization-repositories
    try:
        repos = []
        page = 1
        while True:
            repos_page = getReposFromPage(github_token, organization, page)
            if repos_page is not None:
                repos.extend(repos_page)
                if len(repos_page) < 100:
                    break
                else:
                    page += 1
            else:
                raise Exception("repos_page is None")
        return repos
    except Exception as e:
        print(f"error: {e}")
        return None


@app.command()
def list(github_token: str = typer.Argument("--token", envvar="GITHUB_TOKEN")):
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


@app.command()
def check(github_token: str = typer.Argument("--token", envvar="GITHUB_TOKEN"), list_orphaned: bool = False):
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
                            print(f" {repo['name']} - {repo['description']}")
                            repos_need_changes.append(repo)
                        else:
                            print(f" {repo['name']} - {repo['description']}")

                    except Exception as e:
                        print(f"error: {e}")
                else:
                    print(f"  {repo['name']} - {repo['description']}")
                    repos_not_cloned.append(repo)

        # Check orphaned repos
        repos_orphaned = []

        # read all folders in projects folder
        for item in os.listdir(f'{ Path.home() }/projects/clcreative'):
            # check if item is in repos list, and if item is not in ignored folders
            if item not in [repo['name'] for repo in repos] and item not in ignored_folders:
                repos_orphaned.append(item)

        # List all orphaned repos
        if list_orphaned:
            print("---\nOrphaned:")
            for repo in repos_orphaned:
                print(f"  {repo}")

        # Get Information about all Repos
        print(f"---\nTotal: {len(repos)}, Need changes: {len(repos_need_changes)}, Not cloned: {len(repos_not_cloned)}, Orphaned: {len(repos_orphaned)}")

    except Exception as e:
        print(f"error: {e}")


@app.command()
def clone(github_token: str = typer.Argument("--token", envvar="GITHUB_TOKEN")):
    # Clone all missing repos for an organization from GitHub

    try:
        repos = getRepos(github_token, 'clcreative')
        if repos is not None:
            for repo in repos:
                # set repo path on local workstation
                repo_path = f'{ Path.home() }/projects/{repo["owner"]["login"]}/{repo["name"]}'

                # when repo is not existing
                if not os.path.exists(repo_path):
                    print(f"  {repo['name']} - {repo['description']}")
                    os.system(f'git clone git@github.com:{repo["owner"]["login"]}/{repo["name"]}.git {repo_path}')

    except Exception as e:
        print(f"error: {e}")


@app.command()
def clear(github_token: str = typer.Argument("--token", envvar="GITHUB_TOKEN")):
    # Clear all orphaned repos from workstation

    repos_orphaned = []

    try:
        repos = getRepos(github_token, 'clcreative')
        if repos is not None:
            # read all folders in projects folder
            for item in os.listdir(f'{ Path.home() }/projects/clcreative'):
                # check if item is in repos list, and if item is not in ignored folders
                if item not in [repo['name'] for repo in repos] and item not in ignored_folders:
                    repos_orphaned.append(item)

            # ask for confirmation
            if len(repos_orphaned) > 0:
                print("---\nOrphaned:")
                for repo in repos_orphaned:
                    print(f"  {repo}")
                print(f"---\nTotal: {len(repos_orphaned)}")
                if typer.confirm("Do you want to delete all orphaned repos?"):
                    for repo in repos_orphaned:
                        # delete folder using rm
                        os.system(f'rm -rf { Path.home() }/projects/clcreative/{repo}')

    except Exception as e:
        print(f"error: {e}")


if __name__ == "__main__":
    app()
