import logging

from sgqlc.endpoint.http import HTTPEndpoint

from github_activity import (
    fetch_issue_comments,
    fetch_issues,
    fetch_pull_request_comments,
    fetch_pull_requests,
)


HOSTNAME = "https://api.github.com/graphql"
DEFAULT_PAGE_SIZE = 100


logger = logging.getLogger(__name__)


class Client:
    def __init__(self, token, page_size=DEFAULT_PAGE_SIZE):
        logger.debug("creating client")
        self.endpoint = HTTPEndpoint(
            HOSTNAME, base_headers={"Authorization": f"Bearer {token}"}, timeout=5
        )
        self.page_size = page_size

    def timeline(self, owner, repo):
        for issue in self._issues(owner, repo):
            yield issue
            for comment in self._issue_comments(issue.id):
                yield comment

        for pr in self._pull_requests(owner, repo):
            yield pr
            for comment in self._pull_request_comments(pr.id):
                yield comment

    def _issues(self, owner, repo):
        base_data = {"owner": owner, "name": repo, "first": self.page_size}
        yield from self._paginate(
            op=fetch_issues.Operations.query.fetch_issues,
            base_data=base_data,
            edges_lens_fn=lambda data: data.repository.issues.edges,
            page_info_lens_fn=lambda data: data.repository.issues.page_info,
        )

    def _issue_comments(self, id):
        base_data = {"id": id, "first": self.page_size}
        yield from self._paginate(
            op=fetch_issue_comments.Operations.query.fetch_issue_comments,
            base_data=base_data,
            edges_lens_fn=lambda data: data.node.comments.edges,
            page_info_lens_fn=lambda data: data.node.comments.page_info,
        )

    def _pull_requests(self, owner, repo):
        base_data = {"owner": owner, "name": repo, "first": self.page_size}
        yield from self._paginate(
            op=fetch_pull_requests.Operations.query.fetch_pull_requests,
            base_data=base_data,
            edges_lens_fn=lambda data: data.repository.pull_requests.edges,
            page_info_lens_fn=lambda data: data.repository.pull_requests.page_info,
        )

    def _pull_request_comments(self, id):
        base_data = {"id": id, "first": self.page_size}
        yield from self._paginate(
            op=fetch_pull_request_comments.Operations.query.fetch_pull_request_comments,
            base_data=base_data,
            edges_lens_fn=lambda data: data.node.comments.edges,
            page_info_lens_fn=lambda data: data.node.comments.page_info,
        )

    def _paginate(self, op, base_data, edges_lens_fn, page_info_lens_fn):
        after = None
        while True:
            data = base_data.copy()
            data["after"] = after
            logger.debug(f"variables: {data}")
            data = self.endpoint(op, data)
            typed_data = op + data

            for edge in edges_lens_fn(typed_data):
                yield edge.node

            page_info = page_info_lens_fn(typed_data)
            if not page_info.has_next_page:
                break
            after = page_info.end_cursor
