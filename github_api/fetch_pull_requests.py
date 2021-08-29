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
            cursor=sgqlc.types.Arg(_schema.String),
            pageSize=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)),
        ),
    )
    _op_repository = _op.repository(
        name=sgqlc.types.Variable("name"), owner=sgqlc.types.Variable("owner")
    )
    _op_repository_pull_requests = _op_repository.pull_requests(
        first=sgqlc.types.Variable("pageSize"), after=sgqlc.types.Variable("cursor")
    )
    _op_repository_pull_requests_page_info = _op_repository_pull_requests.page_info()
    _op_repository_pull_requests_page_info.has_next_page()
    _op_repository_pull_requests_page_info.end_cursor()
    _op_repository_pull_requests_nodes = _op_repository_pull_requests.nodes()
    _op_repository_pull_requests_nodes.id()
    return _op


class Query:
    fetch_pull_requests = query_fetch_pull_requests()


class Operations:
    query = Query
