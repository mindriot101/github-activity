import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ('Operations',)


def query_fetch_commits_for_branch():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='FetchCommitsForBranch', variables=dict(name=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), owner=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), branch=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)), after=sgqlc.types.Arg(_schema.String)))
    _op_repository = _op.repository(owner=sgqlc.types.Variable('owner'), name=sgqlc.types.Variable('name'))
    _op_repository_ref = _op_repository.ref(qualified_name=sgqlc.types.Variable('branch'))
    _op_repository_ref.name()
    _op_repository_ref.prefix()
    _op_repository_ref_target = _op_repository_ref.target()
    _op_repository_ref_target__as__Commit = _op_repository_ref_target.__as__(_schema.Commit)
    _op_repository_ref_target__as__Commit_history = _op_repository_ref_target__as__Commit.history(first=sgqlc.types.Variable('first'), after=sgqlc.types.Variable('after'))
    _op_repository_ref_target__as__Commit_history_page_info = _op_repository_ref_target__as__Commit_history.page_info()
    _op_repository_ref_target__as__Commit_history_page_info.has_next_page()
    _op_repository_ref_target__as__Commit_history_page_info.end_cursor()
    _op_repository_ref_target__as__Commit_history_edges = _op_repository_ref_target__as__Commit_history.edges()
    _op_repository_ref_target__as__Commit_history_edges_node = _op_repository_ref_target__as__Commit_history_edges.node()
    _op_repository_ref_target__as__Commit_history_edges_node.oid()
    _op_repository_ref_target__as__Commit_history_edges_node.committed_date(__alias__='created_at')
    return _op


class Query:
    fetch_commits_for_branch = query_fetch_commits_for_branch()


class Operations:
    query = Query
