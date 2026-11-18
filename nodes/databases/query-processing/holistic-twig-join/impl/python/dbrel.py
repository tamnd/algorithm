# SPDX-License-Identifier: MIT
# Shared helper of the databases pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Naive relations, operators by definition, SQL three-valued logic and a page-counting disk.

This is the reference that the tests of the databases pages compare against.
Every operator here follows its definition directly, with nested loops and no
index, hash table or sort of the input. Do not use it as a fast engine.

Relations
    Relation(schema, rows, mode) holds a tuple of distinct attribute names and
    a collections.Counter from tuples to positive counts. mode is "bag" (the
    default, SQL semantics) or "set" (relational theory); in set mode every
    count is 1. rows may be an iterable of tuples (duplicates add up) or a
    mapping from tuples to counts. Two relations are equal when they have the
    same attributes (in any column order) and the same count for each tuple.
    The mode is not compared.

Operators (each returns a new Relation in the mode of its input)
    select(rel, pred)            keeps a row only when pred(row) is True
    where(rel, pred)             the same as select (the SQL WHERE filter)
    project(rel, attrs)          bag: counts add up; set: duplicates removed
    rename(rel, mapping)         mapping is {old: new}
    union(r, s)                  bag: UNION ALL (counts add); set: union
    difference(r, s)             bag: monus max(0, m - n); set: r - s
    intersection(r, s)           bag: min(m, n); set: intersection
    product(r, s)                attributes must be disjoint; counts multiply
    natural_join(r, s)           nested loops on the common attributes
    theta_join(r, s, pred)       select(product(r, s), pred)
    semijoin(r, s), antijoin(r, s)
    distinct(rel)                every count becomes 1
    aggregate(rel, group_attrs, aggs)
                                 aggs is a list of (func, attr, out) with func in
                                 count_star, count, count_distinct, sum, avg, min, max

A predicate receives the row as a dict from attribute name to value. It may
return True, False or None (UNKNOWN). Only True keeps the row.

Nulls
    NULL is None. Joins follow SQL: a common attribute that is None in either
    row never matches. aggregate follows SQL: GROUP BY puts all nulls of a
    column in one group, every aggregate except count_star skips nulls, and
    sum, avg, min and max of no non-null value give None while count gives 0.
    With no grouping attributes, aggregate returns one row even for an empty
    input, as SQL does.

Expressions
    evaluate(expr, db, mode) evaluates a tree of nested tuples:
        ("scan", name)
        ("select", pred, e)          ("project", attrs, e)
        ("rename", mapping, e)       ("distinct", e)
        ("union", e1, e2)            ("difference", e1, e2)
        ("intersection", e1, e2)     ("product", e1, e2)
        ("join", e1, e2)             ("theta_join", pred, e1, e2)
        ("semijoin", e1, e2)         ("antijoin", e1, e2)
        ("aggregate", group_attrs, aggs, e)
    db maps a name to a Relation. Each scanned relation is first put in mode.

Three-valued logic
    tv_and, tv_or and tv_not are the strong Kleene connectives on True, False
    and None. cmp3(op, x, y) compares with op in =, <>, !=, <, <=, >, >= and
    returns None when x or y is None.

Disk
    Disk counts page reads and writes. load(rows, per_page) puts an existing
    input on the disk without counting it. paginate(rows, per_page) splits a
    list of rows into pages.

Random data
    random_relation(rng, schema, n, domain, mode, null_rate) draws n rows.
"""

from collections import Counter
from collections.abc import Callable, Hashable, Iterable, Mapping, Sequence
from fractions import Fraction
from numbers import Number
import random

BAG = "bag"
SET = "set"
MODES = (BAG, SET)


# ---------------------------------------------------------------- ordering

def value_key(v: object) -> tuple:
    """A total order on the values of one column: None first, then numbers, then strings."""
    if v is None:
        return (0, 0)
    if isinstance(v, Number):
        return (1, v)
    if isinstance(v, str):
        return (2, v)
    if isinstance(v, tuple):
        return (3, tuple(value_key(x) for x in v))
    return (4, repr(v))


def row_key(t: Sequence) -> tuple:
    """A total order on tuples that tolerates None. Use it to sort rows in tests."""
    return tuple(value_key(v) for v in t)


# ---------------------------------------------------------------- relations

class Relation:
    """A relation: a schema (tuple of names), a Counter of tuples and a mode."""

    __slots__ = ("schema", "rows", "mode")

    def __init__(self, schema: Sequence[str], rows: Iterable | Mapping = (), mode: str = BAG) -> None:
        if mode not in MODES:
            raise ValueError("mode must be 'bag' or 'set'")
        schema = tuple(schema)
        if len(set(schema)) != len(schema):
            raise ValueError("duplicate attribute in schema %r" % (schema,))
        counts: Counter = Counter()
        items = rows.items() if isinstance(rows, Mapping) else ((t, 1) for t in rows)
        for t, c in items:
            t = tuple(t)
            if len(t) != len(schema):
                raise ValueError("tuple %r does not fit schema %r" % (t, schema))
            if c < 0:
                raise ValueError("negative count for %r" % (t,))
            if c:
                counts[t] += c
        if mode == SET:
            counts = Counter({t: 1 for t in counts})
        self.schema = schema
        self.rows = counts
        self.mode = mode

    def index(self, attr: str) -> int:
        return self.schema.index(attr)

    def reorder(self, schema: Sequence[str]) -> "Relation":
        """The same relation with its columns in the order of schema."""
        schema = tuple(schema)
        if sorted(schema) != sorted(self.schema):
            raise ValueError("schemas %r and %r differ" % (self.schema, schema))
        pos = [self.schema.index(a) for a in schema]
        return Relation(schema, {tuple(t[i] for i in pos): c for t, c in self.rows.items()}, self.mode)

    def with_mode(self, mode: str) -> "Relation":
        return Relation(self.schema, self.rows, mode)

    def as_dict(self, t: Sequence) -> dict:
        return dict(zip(self.schema, t))

    def sorted_rows(self) -> list:
        """Every tuple, repeated by its count, in row_key order."""
        out = []
        for t in sorted(self.rows, key=row_key):
            out.extend([t] * self.rows[t])
        return out

    def __iter__(self):
        return iter(self.sorted_rows())

    def __len__(self) -> int:
        return sum(self.rows.values())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Relation):
            return NotImplemented
        if sorted(self.schema) != sorted(other.schema):
            return False
        return self.rows == other.reorder(self.schema).rows

    def __repr__(self) -> str:
        body = ", ".join("%r: %d" % (t, self.rows[t]) for t in sorted(self.rows, key=row_key))
        return "Relation(%r, {%s}, %r)" % (self.schema, body, self.mode)


def _mode2(r: Relation, s: Relation) -> str:
    if r.mode != s.mode:
        raise ValueError("operands have modes %r and %r" % (r.mode, s.mode))
    return r.mode


def _same_schema(r: Relation, s: Relation) -> Relation:
    """s with its columns in the order of r; the attribute sets must be equal."""
    if sorted(r.schema) != sorted(s.schema):
        raise ValueError("union-incompatible schemas %r and %r" % (r.schema, s.schema))
    return s.reorder(r.schema)


# ---------------------------------------------------------------- three-valued logic

def tv_and(a: bool | None, b: bool | None) -> bool | None:
    if a is False or b is False:
        return False
    if a is None or b is None:
        return None
    return True


def tv_or(a: bool | None, b: bool | None) -> bool | None:
    if a is True or b is True:
        return True
    if a is None or b is None:
        return None
    return False


def tv_not(a: bool | None) -> bool | None:
    return None if a is None else not a


_CMP = {
    "=": lambda x, y: x == y,
    "<>": lambda x, y: x != y,
    "!=": lambda x, y: x != y,
    "<": lambda x, y: x < y,
    "<=": lambda x, y: x <= y,
    ">": lambda x, y: x > y,
    ">=": lambda x, y: x >= y,
}


def cmp3(op: str, x: object, y: object) -> bool | None:
    """SQL comparison: None (UNKNOWN) if either side is NULL."""
    if op not in _CMP:
        raise ValueError("unknown comparison %r" % (op,))
    if x is None or y is None:
        return None
    return bool(_CMP[op](x, y))


def is_true(v: bool | None) -> bool:
    """The WHERE test: only True passes; False and None (UNKNOWN) do not."""
    return v is True


# ---------------------------------------------------------------- operators

def select(rel: Relation, pred: Callable[[dict], bool | None]) -> Relation:
    out = {t: c for t, c in rel.rows.items() if pred(rel.as_dict(t)) is True}
    return Relation(rel.schema, out, rel.mode)


where = select


def project(rel: Relation, attrs: Sequence[str]) -> Relation:
    attrs = tuple(attrs)
    pos = [rel.index(a) for a in attrs]
    out: Counter = Counter()
    for t, c in rel.rows.items():
        out[tuple(t[i] for i in pos)] += c
    return Relation(attrs, out, rel.mode)


def rename(rel: Relation, mapping: Mapping[str, str]) -> Relation:
    for a in mapping:
        if a not in rel.schema:
            raise ValueError("no attribute %r to rename" % (a,))
    return Relation(tuple(mapping.get(a, a) for a in rel.schema), rel.rows, rel.mode)


def union(r: Relation, s: Relation) -> Relation:
    mode = _mode2(r, s)
    s = _same_schema(r, s)
    out = Counter(r.rows)
    out.update(s.rows)
    return Relation(r.schema, out, mode)


def difference(r: Relation, s: Relation) -> Relation:
    mode = _mode2(r, s)
    s = _same_schema(r, s)
    out = {t: max(0, c - s.rows.get(t, 0)) for t, c in r.rows.items()}
    return Relation(r.schema, out, mode)


def intersection(r: Relation, s: Relation) -> Relation:
    mode = _mode2(r, s)
    s = _same_schema(r, s)
    out = {t: min(c, s.rows.get(t, 0)) for t, c in r.rows.items()}
    return Relation(r.schema, out, mode)


def product(r: Relation, s: Relation) -> Relation:
    mode = _mode2(r, s)
    common = [a for a in r.schema if a in s.schema]
    if common:
        raise ValueError("product needs disjoint schemas; common: %r" % (common,))
    out: Counter = Counter()
    for t, c in r.rows.items():
        for u, d in s.rows.items():
            out[t + u] += c * d
    return Relation(r.schema + s.schema, out, mode)


def _matches(r: Relation, s: Relation, t: tuple, u: tuple, common: Sequence[str]) -> bool:
    for a in common:
        x, y = t[r.index(a)], u[s.index(a)]
        if x is None or y is None or x != y:
            return False
    return True


def natural_join(r: Relation, s: Relation) -> Relation:
    """Nested loops over both inputs. With no common attribute it is the product."""
    mode = _mode2(r, s)
    common = [a for a in r.schema if a in s.schema]
    rest = [a for a in s.schema if a not in common]
    rest_pos = [s.index(a) for a in rest]
    out: Counter = Counter()
    for t, c in r.rows.items():
        for u, d in s.rows.items():
            if _matches(r, s, t, u, common):
                out[t + tuple(u[i] for i in rest_pos)] += c * d
    return Relation(r.schema + tuple(rest), out, mode)


def theta_join(r: Relation, s: Relation, pred: Callable[[dict], bool | None]) -> Relation:
    return select(product(r, s), pred)


def semijoin(r: Relation, s: Relation) -> Relation:
    """Rows of r (with their counts) that join with at least one row of s."""
    _mode2(r, s)
    common = [a for a in r.schema if a in s.schema]
    out = {t: c for t, c in r.rows.items() if any(_matches(r, s, t, u, common) for u in s.rows)}
    return Relation(r.schema, out, r.mode)


def antijoin(r: Relation, s: Relation) -> Relation:
    """Rows of r (with their counts) that join with no row of s."""
    _mode2(r, s)
    common = [a for a in r.schema if a in s.schema]
    out = {t: c for t, c in r.rows.items() if not any(_matches(r, s, t, u, common) for u in s.rows)}
    return Relation(r.schema, out, r.mode)


def distinct(rel: Relation) -> Relation:
    return Relation(rel.schema, {t: 1 for t in rel.rows}, rel.mode)


AGG_FUNCS = ("count_star", "count", "count_distinct", "sum", "avg", "min", "max")


def _avg(vals: list) -> object:
    total = sum(vals)
    if all(isinstance(v, (int, Fraction)) for v in vals):
        return Fraction(total, 1) / len(vals)
    return total / len(vals)


def agg_value(func: str, vals: list) -> object:
    """One SQL aggregate over a list of column values (with repeats). count_star counts all."""
    if func == "count_star":
        return len(vals)
    nn = [v for v in vals if v is not None]
    if func == "count":
        return len(nn)
    if func == "count_distinct":
        seen: list = []
        for v in nn:
            if v not in seen:
                seen.append(v)
        return len(seen)
    if not nn:
        return None
    if func == "sum":
        return sum(nn)
    if func == "avg":
        return _avg(nn)
    if func == "min":
        return min(nn)
    if func == "max":
        return max(nn)
    raise ValueError("unknown aggregate %r" % (func,))


def aggregate(rel: Relation, group_attrs: Sequence[str], aggs: Sequence[tuple]) -> Relation:
    """gamma_{G; f(A) -> B}(rel) by definition.

    aggs is a list of (func, attr, out); attr is ignored for count_star and may
    be None. For each distinct group key, in row_key order, the whole input is
    scanned. Each result row has count 1 in either mode.
    """
    group_attrs = tuple(group_attrs)
    gpos = [rel.index(a) for a in group_attrs]
    for func, attr, _ in aggs:
        if func not in AGG_FUNCS:
            raise ValueError("unknown aggregate %r" % (func,))
        if func != "count_star":
            rel.index(attr)
    keys: list = []
    for t in rel.rows:
        k = tuple(t[i] for i in gpos)
        if k not in keys:
            keys.append(k)
    if not group_attrs and not keys:
        keys = [()]
    out: Counter = Counter()
    for k in sorted(keys, key=row_key):
        row = list(k)
        for func, attr, _ in aggs:
            vals: list = []
            for t, c in rel.rows.items():
                if tuple(t[i] for i in gpos) == k:
                    vals.extend([None if func == "count_star" else t[rel.index(attr)]] * c)
            row.append(agg_value(func, vals))
        out[tuple(row)] = 1
    schema = group_attrs + tuple(o for _, _, o in aggs)
    return Relation(schema, out, rel.mode)


# ---------------------------------------------------------------- evaluation

def evaluate(expr: tuple, db: Mapping[str, Relation], mode: str = BAG) -> Relation:
    """Evaluate an expression tree of nested tuples over db, in mode."""
    if mode not in MODES:
        raise ValueError("mode must be 'bag' or 'set'")
    op = expr[0]
    ev = lambda e: evaluate(e, db, mode)
    if op == "scan":
        return db[expr[1]].with_mode(mode)
    if op == "select":
        return select(ev(expr[2]), expr[1])
    if op == "project":
        return project(ev(expr[2]), expr[1])
    if op == "rename":
        return rename(ev(expr[2]), expr[1])
    if op == "distinct":
        return distinct(ev(expr[1]))
    if op == "aggregate":
        return aggregate(ev(expr[3]), expr[1], expr[2])
    if op == "theta_join":
        return theta_join(ev(expr[2]), ev(expr[3]), expr[1])
    binary = {
        "union": union, "difference": difference, "intersection": intersection,
        "product": product, "join": natural_join, "semijoin": semijoin, "antijoin": antijoin,
    }
    if op in binary:
        return binary[op](ev(expr[1]), ev(expr[2]))
    raise ValueError("unknown operator %r" % (op,))


# ---------------------------------------------------------------- disk

def paginate(rows: Sequence, per_page: int) -> list:
    """Split rows into pages of per_page rows; the last page may be shorter."""
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    rows = list(rows)
    return [rows[i:i + per_page] for i in range(0, len(rows), per_page)]


class Disk:
    """Pages on a simulated disk. Each read_page and write_page call costs one I/O."""

    def __init__(self) -> None:
        self.pages: dict = {}
        self.reads = 0
        self.writes = 0
        self._next = 0

    def alloc(self) -> int:
        pid = self._next
        self._next += 1
        self.pages[pid] = ()
        return pid

    def write_page(self, pid: int, rows: Iterable) -> None:
        if pid not in self.pages:
            raise KeyError("page %r was not allocated" % (pid,))
        self.pages[pid] = tuple(rows)
        self.writes += 1

    def read_page(self, pid: int) -> list:
        self.reads += 1
        return list(self.pages[pid])

    def free(self, pid: int) -> None:
        del self.pages[pid]

    def load(self, rows: Sequence, per_page: int) -> list:
        """Store an input file without counting I/O; return its page ids in order."""
        ids = []
        for page in paginate(rows, per_page):
            pid = self.alloc()
            self.pages[pid] = tuple(page)
            ids.append(pid)
        return ids

    def io(self) -> int:
        return self.reads + self.writes

    def reset_counters(self) -> None:
        self.reads = 0
        self.writes = 0


# ---------------------------------------------------------------- random data

def random_relation(rng: random.Random, schema: Sequence[str], n: int,
                    domain: int | Sequence | Mapping = 4, mode: str = BAG,
                    null_rate: float = 0.0) -> Relation:
    """n rows drawn with rng. domain is a size k (values 0 to k - 1), a list of
    values, or a dict from attribute to either. Each value is None with
    probability null_rate. In set mode duplicates collapse, so there may be
    fewer than n rows."""
    schema = tuple(schema)

    def values(a: str) -> list:
        d = domain[a] if isinstance(domain, Mapping) else domain
        return list(range(d)) if isinstance(d, int) else list(d)

    doms = [values(a) for a in schema]
    rows = []
    for _ in range(n):
        t = []
        for d in doms:
            if null_rate and rng.random() < null_rate:
                t.append(None)
            else:
                t.append(rng.choice(d))
        rows.append(tuple(t))
    return Relation(schema, rows, mode)
