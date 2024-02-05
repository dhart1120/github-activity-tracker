from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubReleaseEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        payload = event.get("payload")
        self.action =  payload.get("action")
        self.release = payload.get("release")
        self.short_description_html = self.release.get("short_description_html")
        self.release_id = self.release.get("id")
        
    def summary(self):
        """
        Example:
        username published release 123456 at 2024-01-01T00:00:00Z for repo username/reponame
        """
        
        actor_name = self.actor.get("login")
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""
        
        return f"""
        {convert_to_local(self.created_at)} {actor_name} {self.action} release {self.release_id} for repo {self.repo} {jira_tickets}
        """.strip()    

    def __str__(self):
        return f'<GitHubPushEvent {self.action} {self.number}>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "action": self.action,
            "release": self.release,
            "changes_html": self.short_description_html,
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