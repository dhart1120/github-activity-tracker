from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubCreateEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        payload = event.get("payload")
        self.ref =  payload.get("ref")
        self.ref_type = payload.get("ref_type")

    def summary(self):
        actor_name = self.actor.get("login")
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""
        
        return f"""
        {convert_to_local(self.created_at)} {actor_name} created {self.ref_type} {self.ref} for repo {self.repo} {jira_tickets}
        """.strip()    

    def __str__(self):
        return f'<GitHubCreateEvent>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "ref": self.ref, 
            "ref_type": self.ref_type,
            "description": payload.get('description'),
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