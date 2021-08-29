import enum
import logging

from sgqlc.endpoint.http import HTTPEndpoint

from github_activity import (
    fetch_commits_for_branch,
    fetch_issue_comments,
    fetch_issues,
    fetch_pull_request_comments,
    fetch_pull_requests,
)


HOSTNAME = "https://api.github.com/graphql"
DEFAULT_PAGE_SIZE = 100


logger = logging.getLogger(__name__)


class GraphQLErrors(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__("Errors in graphql response")


class EventType(enum.Enum):
    IssueCreated = enum.auto()
    IssueComment = enum.auto()
    IssueClosed = enum.auto()
    PullRequestCreated = enum.auto()
    PullRequestComment = enum.auto()
    Commit = enum.auto()

    def to_dict(self):
        return self.name


class Event:
    def __init__(self, type, node=None, json=None):
        self.type = type
        self.node = node
        self.json = json

    def to_dict(self):
        node_data = {}
        if self.node is not None:
            node_data.update(self.node.__to_json_value__())
        if self.json is not None:
            node_data.update(self.json)

        if self.type == EventType.Commit:
            node_data["createdAt"] = node_data.pop("committedDate")

        return {"type": self.type.to_dict(), **node_data}


class Client:
    def __init__(self, token, page_size=DEFAULT_PAGE_SIZE):
        logger.debug("creating client")
        self.endpoint = HTTPEndpoint(
            HOSTNAME, base_headers={"Authorization": f"Bearer {token}"}, timeout=30
        )
        self.page_size = page_size

    def timeline(self, owner, repo, branch):
        for issue in self._issues(owner, repo):
            yield Event(type=EventType.IssueCreated, node=issue)
            if issue.closed_at is not None:
                yield Event(
                    type=EventType.IssueClosed, json={"createdAt": issue.closed_at}
                )
            for comment in self._issue_comments(issue.id):
                yield Event(type=EventType.IssueComment, node=comment)

        for pr in self._pull_requests(owner, repo):
            yield Event(type=EventType.PullRequestCreated, node=pr)
            for comment in self._pull_request_comments(pr.id):
                yield Event(type=EventType.PullRequestComment, node=comment)

        for commit in self._commits(owner, repo, branch):
            yield Event(type=EventType.Commit, node=commit)

    def _issues(self, owner, repo):
        base_data = {"owner": owner, "name": repo, "first": self.page_size}
        yield from self._paginate(
            op=fetch_issues.Operations.query.fetch_issues,
            base_data=base_data,
            base_lens_fn=lambda data: data.repository.issues,
        )

    def _issue_comments(self, id):
        base_data = {"id": id, "first": self.page_size}
        yield from self._paginate(
            op=fetch_issue_comments.Operations.query.fetch_issue_comments,
            base_data=base_data,
            base_lens_fn=lambda data: data.node.comments,
        )

    def _pull_requests(self, owner, repo):
        base_data = {"owner": owner, "name": repo, "first": self.page_size}
        yield from self._paginate(
            op=fetch_pull_requests.Operations.query.fetch_pull_requests,
            base_data=base_data,
            base_lens_fn=lambda data: data.repository.pull_requests,
        )

    def _pull_request_comments(self, id):
        base_data = {"id": id, "first": self.page_size}
        yield from self._paginate(
            op=fetch_pull_request_comments.Operations.query.fetch_pull_request_comments,
            base_data=base_data,
            base_lens_fn=lambda data: data.node.comments,
        )

    def _commits(self, owner, repo, branch):
        base_data = {
            "owner": owner,
            "name": repo,
            "branch": branch,
            "first": self.page_size,
        }
        yield from self._paginate(
            op=fetch_commits_for_branch.Operations.query.fetch_commits_for_branch,
            base_data=base_data,
            base_lens_fn=lambda data: data.repository.ref.target.history,
        )

    def _paginate(self, op, base_data, base_lens_fn):
        after = None
        while True:
            data = base_data.copy()
            data["after"] = after
            logger.debug(f"variables: {data}")
            data = self.endpoint(op, data)

            if "errors" in data:
                raise GraphQLErrors(data["errors"])

            typed_data = op + data

            base_node = base_lens_fn(typed_data)

            for edge in base_node.edges:
                yield edge.node

            page_info = base_node.page_info
            if not page_info.has_next_page:
                break

            after = page_info.end_cursor
