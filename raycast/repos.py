import requests


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
