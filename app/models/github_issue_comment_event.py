from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubIssueCommentEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        self.action = event.get("payload").get("action")
        self.comment = event.get("payload").get("comment")
        self.issue = event.get("payload").get("issue")

    def summary(self):
        """
        Example:
        username created comment on PR #123 at 2024-01-01T00:00:00Z for repo username/reponame
        """
        
        actor_name = self.actor.get("login")
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""
    
        pr_number = self.issue["number"]

        return f"""
        {convert_to_local(self.created_at)} {actor_name} {self.action} comment on PR #{pr_number} for repo {self.repo} {jira_tickets}
        """.strip()
        

    def __str__(self):
        return f'<IssueCommentEvent>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "action": self.action, 
        }
        
        pull_request = self.issue.get("pull_request")
        if pull_request:
            ret["pull_request"] = {
                "html_url": pull_request.get("html_url"),
                "number": self.issue["number"],
            }
        
        comment = payload.get('comment')
        if comment:
            ret["comment"] = {
                "comment_id": comment.get('id'),
                "issue_id": comment.get('issue_id'),
                "url": comment.get('url'),
                "body": comment.get('body'),
                "user": comment.get('user'),
                "created_at": comment.get('created_at'),
                "updated_at": comment.get('updated_at'),
                # "html_url": comment.get('html_url'),
            }
            
            commenter = comment.get('user')
            if commenter:
                ret["comment"]["user"] = {
                    "id": commenter.get('id'),
                    "login": commenter.get('login'),
                    "type": commenter.get('type'),
                    "author_association": comment.get('author_association'),
                    "avatar_url": commenter.get('avatar_url'),
                    "url": commenter.get('url'),
                }
            
        org = self.raw_event.get('org')
        if org:
            ret["org"] = {
                "id": org.get('id'),
                "login": org.get('login'),
                "avatar_url": org.get('avatar_url'),
                "url": org.get('url'),
            }

        return ret