import json, os
from github import Github

class GitHubApiClient():
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_API_KEY"))

    def save_json(self, data, filename):
        """Save data to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def fetch_repo_events(self, repo_name):
        """Fetch and return GitHub repository events."""
        repo = self.github.get_repo(repo_name)
        return list(map(lambda e: e.raw_data, repo.get_events()))
