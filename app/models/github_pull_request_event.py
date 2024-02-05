from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubPullRequestEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        payload = event.get("payload")
        self.action = payload.get("action")
        self.number = payload.get("number")
        self.pull_request = payload.get("pull_request")
        
    def summary(self):
        """
        Example:
        username opened PR #123 at 2024-01-01T00:00:00Z for repo username/reponame
        """
        
        actor_name = self.actor.get("login")
        pr_number = self.pull_request["number"]
        pr_title = self.pull_request["title"]
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""

        return f"""
        {convert_to_local(self.created_at)} {actor_name} {self.action} PR #{pr_number} '{pr_title}' for repo {self.repo} {jira_tickets}
        """.strip()

    def __str__(self):
        return f'<GitHubPullRequestEvent {self.action} {self.number}>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "action": payload.get('action'), 
            "number": payload.get('number'),
        }
        
        pr = payload.get('pull_request')
        if pr:
            ret["pull_request"] = {
                "id": pr.get('id'),
                "title": pr.get('title'),
                "commits": pr.get('commits'),
                "target_branch": pr.get('base').get('ref'),  
                "created_at": pr.get('created_at'),
                "closed_at": pr.get('closed_at'),
                "merged_at": pr.get('merged_at'),
                "draft": pr.get('draft'),
                }
        
        user = pr.get('user')
        if user:
            ret["user"] = {
                "id": user.get('id'),
                "login": user.get('login'),
                "type": user.get('type'),
                "avatar_url": user.get('avatar_url'),
                "url": user.get('url'),
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