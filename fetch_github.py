import requests
from dotenv import load_dotenv
import os
import spacy
import re

load_dotenv()
personal_access_token = os.getenv("GITHUB_TOKEN")

# 100 issues per page so adjust max pages accordingly
def fetch_github_issues(owner, repo, personal_access_token=personal_access_token, max_pages=1):
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
        if max_pages is not None and page > max_pages:
            break
        params["page"] = page
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        page_issues = response.json()
        if not page_issues:
            break
        for issue in page_issues:
            issue_body = issue["body"]
            if issue_body:
                issue_body_clean = clean_text(issue_body)
                issue_bodies.append(issue_body_clean)
        page += 1

    return issue_bodies

# Load the small English model
nlp = spacy.load("en_core_web_sm")
def clean_text_spacy(text):
    doc = nlp(text)
    clean_tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space and not token.like_url and not token.like_num]
    return ' '.join(clean_tokens)

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '[URL]', text)

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Convert to lowercase
    text = text.lower()

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

if __name__ == "__main__":
    # Usage
    owner = "octocat"  # Replace with the desired username
    repo = "Hello-World"  # Replace with the desired repo name
    issue_bodies = fetch_github_issues(owner, repo, personal_access_token)

    print(issue_bodies)
    # Print the bodies of the fetched issues
    for body in issue_bodies:
        print(body)

