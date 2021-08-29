import sgqlc.types
import sgqlc.operation
from . import github_schema

_schema = github_schema
_schema_root = _schema.github_schema

__all__ = ('Operations',)


def query_fetch_branches():
    _op = sgqlc.operation.Operation(_schema_root.query_type, name='FetchBranches', variables=dict(name=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), owner=sgqlc.types.Arg(sgqlc.types.non_null(_schema.String)), first=sgqlc.types.Arg(sgqlc.types.non_null(_schema.Int)), after=sgqlc.types.Arg(_schema.String)))
    _op_repository = _op.repository(name=sgqlc.types.Variable('name'), owner=sgqlc.types.Variable('owner'))
    _op_repository_refs = _op_repository.refs(ref_prefix='refs/heads/', first=sgqlc.types.Variable('first'), after=sgqlc.types.Variable('after'))
    _op_repository_refs_page_info = _op_repository_refs.page_info()
    _op_repository_refs_page_info.has_next_page()
    _op_repository_refs_page_info.end_cursor()
    _op_repository_refs_edges = _op_repository_refs.edges()
    _op_repository_refs_edges_node = _op_repository_refs_edges.node()
    _op_repository_refs_edges_node.id()
    return _op


class Query:
    fetch_branches = query_fetch_branches()


class Operations:
    query = Query
