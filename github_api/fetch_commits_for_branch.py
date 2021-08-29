import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ("Operations",)


def query_fetch_commits_for_branch():
    _op = sgqlc.operation.Operation(
        _schema_root.query_type,
        name="FetchCommitsForBranch",
        variables=dict(
            id=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ID)),
            first=sgqlc.types.Arg(_schema.Int),
            after=sgqlc.types.Arg(_schema.String),
        ),
    )
    _op_node = _op.node(id=sgqlc.types.Variable("id"))
    _op_node__as__Ref = _op_node.__as__(_schema.Ref)
    _op_node__as__Ref.name()
    _op_node__as__Ref_target = _op_node__as__Ref.target()
    _op_node__as__Ref_target__as__Commit = _op_node__as__Ref_target.__as__(
        _schema.Commit
    )
    _op_node__as__Ref_target__as__Commit_history = (
        _op_node__as__Ref_target__as__Commit.history(
            first=sgqlc.types.Variable("first"), after=sgqlc.types.Variable("after")
        )
    )
    _op_node__as__Ref_target__as__Commit_history_page_info = (
        _op_node__as__Ref_target__as__Commit_history.page_info()
    )
    _op_node__as__Ref_target__as__Commit_history_page_info.has_next_page()
    _op_node__as__Ref_target__as__Commit_history_edges = (
        _op_node__as__Ref_target__as__Commit_history.edges()
    )
    _op_node__as__Ref_target__as__Commit_history_edges_node = (
        _op_node__as__Ref_target__as__Commit_history_edges.node()
    )
    _op_node__as__Ref_target__as__Commit_history_edges_node.committed_date()
    _op_node__as__Ref_target__as__Commit_history_edges_node.oid()
    return _op


class Query:
    fetch_commits_for_branch = query_fetch_commits_for_branch()


class Operations:
    query = Query
