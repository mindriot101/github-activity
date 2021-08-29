import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ("Operations",)


def query_fetch_pull_request_comments():
    _op = sgqlc.operation.Operation(
        _schema_root.query_type,
        name="FetchPullRequestComments",
        variables=dict(
            id=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ID)),
            first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)),
            cursor=sgqlc.types.Arg(_schema.String),
        ),
    )
    _op_node = _op.node(id=sgqlc.types.Variable("id"))
    _op_node__as__PullRequest = _op_node.__as__(_schema.PullRequest)
    _op_node__as__PullRequest_comments = _op_node__as__PullRequest.comments(
        first=sgqlc.types.Variable("first"), after=sgqlc.types.Variable("cursor")
    )
    _op_node__as__PullRequest_comments_nodes = (
        _op_node__as__PullRequest_comments.nodes()
    )
    _op_node__as__PullRequest_comments_nodes.created_at()
    return _op


class Query:
    fetch_pull_request_comments = query_fetch_pull_request_comments()


class Operations:
    query = Query
