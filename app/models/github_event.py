import re
from app.utils.date_utils import convert_to_local

class GitHubEvent():
    def __init__(self, event):
        self.id = event.get("id")
        self.type = event.get("type")
        self.created_at = event.get("created_at")
        self.repo = event.get("repo").get("name")
        self.raw_event = event
        self.actor = event.get('actor')
        self.related_jira_keys = self.__get_jira_keys()
    
    def summary(self):
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""
        
        return f"""
        {convert_to_local(self.created_at)} An Event of type {self.type} was created for repo {self.repo} {jira_tickets}
        """.strip()    

    def __str__(self):
        return f'<GitHubEvent {self.event_id} {self.type} {self.created_at}>'
    
    def to_raw(self):
        return self.raw_event
    
    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "created_at": self.created_at,
            "related_jira_keys": self.related_jira_keys
        }
        
    def __get_jira_keys(self):
        """
        Looks for anything that looks like JIRA keys in the raw event.

        Returns:
            _type_: list<string>: A list of JIRA keys as strings
        """
        pattern = r'(?<![A-Z0-9])[A-Z]{2,4}-\d+(?!\d)'
        matches = re.findall(pattern, str(self.raw_event))
        return sorted(list(set(matches)))