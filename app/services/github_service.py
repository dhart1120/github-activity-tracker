import json
from datetime import datetime
from app.external.github_api_client import GitHubApiClient

from app.models.github_event import GitHubEvent
from app.models.github_pull_request_event import GitHubPullRequestEvent
from app.models.github_pull_request_review_event import GitHubPullRequestReviewEvent
from app.models.github_pull_request_review_comment_event import GitHubPullRequestReviewCommentEvent
from app.models.github_issue_comment_event import GitHubIssueCommentEvent
from app.models.github_create_event import GitHubCreateEvent
from app.models.github_delete_event import GitHubDeleteEvent
from app.models.github_push_event import GitHubPushEvent
from app.models.github_release_event import GitHubReleaseEvent

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def get_event(repo_owner, repo_name, event_id: int):
    id_as_str = str(event_id)
    for event in list_repo_events(repo_owner, repo_name):
        if event.id == id_as_str:
            return event
    
    return None

def list_all_repo_events(repos, resultsFilter = {
    "event_type": None,
    "start_date": None,
    "end_date": None,
}):
    ret = []
    for repo_name in repos:      
        try:
            ret.extend(list_repo_events(repo_name, resultsFilter))
        except Exception as e:
            print(f"An error occurred for {repo_name}: {e}")
    return ret

def list_repo_events(repo_name, resultsFilter = {
    "event_type": None,
    "start_date": None,
    "end_date": None,
}):
    '''
    Reads the repo.json file and returns the list of events.
    This is basically a mock until the API is used.
    '''
    print(f"Fetching events for {repo_name}")
    json_data = GitHubApiClient().fetch_repo_events(repo_name)
    
    # Filter by date range if it is provided
    start_date, end_date = resultsFilter.get('start_date'), resultsFilter.get('end_date')
    ret = [
        event for event in json_data
        if (start_date is None or datetime.strptime(event['created_at'].split('T')[0], '%Y-%m-%d') >= start_date) and
           (end_date is None or datetime.strptime(event['created_at'].split('T')[0], '%Y-%m-%d') <= end_date)
    ]
    
    def mapper(event):
        match event:
            case {'type': 'PullRequestEvent'}:
                return GitHubPullRequestEvent(event)
            case {'type': 'PullRequestReviewEvent'}:
                return GitHubPullRequestReviewEvent(event)
            case {'type': 'PullRequestReviewCommentEvent'}:
                return GitHubPullRequestReviewCommentEvent(event)
            case {'type': 'IssueCommentEvent'}:
                return GitHubIssueCommentEvent(event)
            case {'type': 'CreateEvent'}:
                return GitHubCreateEvent(event)
            case {'type': 'DeleteEvent'}:
                return GitHubDeleteEvent(event)
            case {'type': 'PushEvent'}:
                return GitHubPushEvent(event)
            case {'type': 'ReleaseEvent'}:
                return GitHubReleaseEvent(event)
            case _:
                return GitHubEvent(event)

    # Filter results if event_type is provided 
    if resultsFilter.get('event_type'):
        ret = list(filter(lambda evt: evt.get('type') == resultsFilter.get('event_type'), ret))
        
    # Sort by created_at in descending order
    ret = sorted(ret, key = lambda evt: evt.get('created_at'))
    
    return list(map(mapper, ret))
    