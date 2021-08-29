import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ('Operations',)


def query_fetch_issue_comments():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='FetchIssueComments', variables=dict(id=sgqlc.types.Arg(sgqlc.types.non_null(_schema.ID)), first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)), after=sgqlc.types.Arg(_schema.String)))
    _op_node = _op.node(id=sgqlc.types.Variable('id'))
    _op_node__as__Issue = _op_node.__as__(_schema.Issue)
    _op_node__as__Issue_comments = _op_node__as__Issue.comments(first=sgqlc.types.Variable('first'), after=sgqlc.types.Variable('after'))
    _op_node__as__Issue_comments_page_info = _op_node__as__Issue_comments.page_info()
    _op_node__as__Issue_comments_page_info.has_next_page()
    _op_node__as__Issue_comments_page_info.end_cursor()
    _op_node__as__Issue_comments_edges = _op_node__as__Issue_comments.edges()
    _op_node__as__Issue_comments_edges_node = _op_node__as__Issue_comments_edges.node()
    _op_node__as__Issue_comments_edges_node.created_at()
    return _op


class Query:
    fetch_issue_comments = query_fetch_issue_comments()


class Operations:
    query = Query
