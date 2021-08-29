import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ("Operations",)


def query_fetch_issues():
    _op = sgqlc.operation.Operation(
        _schema_root.query_type,
        name="FetchIssues",
        variables=dict(
            name=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)),
            owner=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)),
            first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)),
            after=sgqlc.types.Arg(_schema.String),
        ),
    )
    _op_repository = _op.repository(
        name=sgqlc.types.Variable("name"), owner=sgqlc.types.Variable("owner")
    )
    _op_repository_issues = _op_repository.issues(
        first=sgqlc.types.Variable("first"), after=sgqlc.types.Variable("after")
    )
    _op_repository_issues_page_info = _op_repository_issues.page_info()
    _op_repository_issues_page_info.has_next_page()
    _op_repository_issues_page_info.end_cursor()
    _op_repository_issues_edges = _op_repository_issues.edges()
    _op_repository_issues_edges_node = _op_repository_issues_edges.node()
    _op_repository_issues_edges_node.id()
    _op_repository_issues_edges_node.title()
    _op_repository_issues_edges_node.created_at()
    _op_repository_issues_edges_node.closed_at()
    return _op


class Query:
    fetch_issues = query_fetch_issues()


class Operations:
    query = Query
