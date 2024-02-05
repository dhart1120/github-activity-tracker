from enum import Enum

class GithubEventTypes(Enum):
    CREATE = "CreateEvent"
    DELETE = "DeleteEvent"
    COMMENT = "IssueCommentEvent" 
    PR = "PullRequestEvent" 
    PR_COMMENT = "PullRequestReviewCommentEvent" 
    PR_REVIEW = "PullRequestReviewEvent" 
    PUSH = "PushEvent"
    RELEASE = "ReleaseEvent" 
    FORK = "ForkEvent"
    WATCH = "WatchEvent"
    ISSUES = "IssuesEvent"