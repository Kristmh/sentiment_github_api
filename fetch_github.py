import requests
from dotenv import load_dotenv
import os

load_dotenv()
personal_access_token = os.getenv("GITHUB_TOKEN")

def fetch_github_issue_bodies(owner, repo, personal_access_token=None, max_issues=10):
    base_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if personal_access_token:
        headers["Authorization"] = f"token {personal_access_token}"

    params = {
        "per_page": 100,
        "state": "all"  # Get all issues (open and closed). Remove this if you only want open issues.
    }

    issue_bodies = []
    page = 1

    while True:
        if max_issues is not None and len(issue_bodies) >= max_issues:
            break
        params["page"] = page
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        page_issues = response.json()
        if not page_issues:
            break
        for issue in page_issues:
            issue_bodies.append(issue["body"])
        page += 1

    return issue_bodies

# Usage
owner = "octocat"  # Replace with the desired username
repo = "Hello-World"  # Replace with the desired repo name
issue_bodies = fetch_github_issue_bodies(owner, repo, personal_access_token)

print(issue_bodies)
# Print the bodies of the fetched issues
for body in issue_bodies:
    print(body)

