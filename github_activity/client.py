from sgqlc.endpoint.requests import RequestsEndpoint

from github_activity import fetch_issue_comments, fetch_issues


HOSTNAME = "https://api.github.com/graphql"


class Client:
    def __init__(self, token):
        self.endpoint = RequestsEndpoint(
            HOSTNAME, base_headers={"Authorization": f"Bearer {token}"}
        )

    def timeline(self, owner, repo):
        for issue in self._issues(owner, repo):
            yield issue
            for comment in self._issue_comments(issue.id):
                yield comment

    def _issues(self, owner, repo):
        op = fetch_issues.Operations.query.fetch_issues
        data = self.endpoint(op, {"owner": owner, "name": repo, "first": 10})
        repo = (op + data).repository

        for edge in repo.issues.edges:
            yield edge.node

    def _issue_comments(self, id):
        op = fetch_issue_comments.Operations.query.fetch_issue_comments
        data = self.endpoint(op, {"id": id, "first": 10})
        node = (op + data).node
        for edge in node.comments.edges:
            yield edge.node
