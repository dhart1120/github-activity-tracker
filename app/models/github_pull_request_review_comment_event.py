from app.models.github_event import GitHubEvent
from app.utils.date_utils import convert_to_local

class GitHubPullRequestReviewCommentEvent(GitHubEvent):
    def __init__(self, event):
        super().__init__(event)
        self.action = event.get("payload").get("action")
        self.pull_request = event.get("payload").get("pull_request")
        self.comment = event.get("payload").get("comment")

    def summary(self):
        """
        Example:
        username created comment on PR 1615720019 at 2024-01-01T00:00:00Z for repo username/reponame
        """
        
        actor_name = self.actor.get("login")
        pr_number = self.pull_request["number"]
        pr_title = self.pull_request["title"]
        jira_tickets = f"related to ({', '.join(self.related_jira_keys)})" if self.related_jira_keys else ""

        return f"""
        {convert_to_local(self.created_at)} {actor_name} {self.action} review comment on PR #{pr_number} '{pr_title}' for repo {self.repo} {jira_tickets}
        """.strip()
        

    def __str__(self):
        return f'<PullRequestReviewCommentEvent {self.action} {self.number}>'

    def to_json(self):
        payload = self.raw_event.get('payload')

        # Base properties
        ret = {
            **(super().to_json()),
            "action": self.action, 
        }
        
        comment = payload.get('comment')
        if comment:
            ret["comment"] = {
                "id": comment.get('id'),
                "body": comment.get('body'),
                "user": comment.get('user'),
                "created_at": comment.get('created_at'),
                "updated_at": comment.get('updated_at'),
                "html_url": comment.get('html_url'),
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
        
        pr = payload.get('pull_request')
        if pr:
            ret["pull_request"] = {
                "id": pr.get('id'),
                "url": pr.get('_links').get("html").get("href"),
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