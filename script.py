from app.services.github_service import list_all_repo_events
from datetime import datetime

def convert_date(datetime_str):
    return datetime.strptime(datetime_str.split('T')[0], '%Y-%m-%d')    
    
if __name__ == "__main__":
    result_filters = {
        "event_type": None,
        "start_date": convert_date("2024-01-01"),
        "end_date": None,
        #"users": ["octocat"], # TODO implement filters for githuhub login name
    }

    repos = ["octocat/Hello-World", "atlassian-api/atlassian-python-api"]

    ret = list_all_repo_events(repos, result_filters)
    for event in ret:
        print(event.summary())