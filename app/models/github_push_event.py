from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubPushEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        payload = event.get("payload")
        self.ref =  payload.get("ref")
        self.ref_type = payload.get("ref_type")
        self.commits = event.get("payload").get("commits")
        
    def summary(self):
        """
        Example:
        username pushed 3 commits to main branch at 2024-01-01T00:00:00Z for repo username/reponame
        """
        commits = self.commits
        commit_count = len(commits)
        msg = f"{commit_count} commit{'s' if commit_count > 1 else ''}"
        
        actor_name = self.actor.get("login")
        branch_name = self.ref.split('/')[-1]
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""
        
        return f"""
        {convert_to_local(self.created_at)} {actor_name} pushed {msg} to {branch_name} for repo {self.repo} {jira_tickets}
        """.strip()    

    def __str__(self):
        return f'<GitHubPushEvent {self.action} {self.number}>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "ref": payload.get('ref'), 
            "description": payload.get('description'),
            "commits": self.commits,
        }
        
        actor = payload.get('actor')
        if actor:
            ret["user"] = {
                "id": actor.get('id'),
                "login": actor.get('login'),
                "type": actor.get('type'),
                "avatar_url": actor.get('avatar_url'),
                "url": actor.get('url'),
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