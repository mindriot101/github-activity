import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ("Operations",)


def query_fetch_pull_requests():
    _op = sgqlc.operation.Operation(
        _schema_root.query_type,
        name="FetchPullRequests",
        variables=dict(
            name=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)),
            owner=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)),
            after=sgqlc.types.Arg(_schema.String),
            first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)),
        ),
    )
    _op_repository = _op.repository(
        name=sgqlc.types.Variable("name"), owner=sgqlc.types.Variable("owner")
    )
    _op_repository_pull_requests = _op_repository.pull_requests(
        first=sgqlc.types.Variable("first"), after=sgqlc.types.Variable("after")
    )
    _op_repository_pull_requests_page_info = _op_repository_pull_requests.page_info()
    _op_repository_pull_requests_page_info.has_next_page()
    _op_repository_pull_requests_page_info.end_cursor()
    _op_repository_pull_requests_edges = _op_repository_pull_requests.edges()
    _op_repository_pull_requests_edges_node = _op_repository_pull_requests_edges.node()
    _op_repository_pull_requests_edges_node.id()
    _op_repository_pull_requests_edges_node.title()
    _op_repository_pull_requests_edges_node.created_at()
    _op_repository_pull_requests_edges_node.closed_at()
    _op_repository_pull_requests_edges_node.merged_at()
    return _op


class Query:
    fetch_pull_requests = query_fetch_pull_requests()


class Operations:
    query = Query
