# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/relational-algebra/. The authors are listed in prov/NEME20.jsonl.

"""An interpreter for the relational algebra, named perspective, set semantics.

A relation is a schema (a frozenset of attribute names) and a set of tuples.
A tuple is stored as a sorted tuple of (attribute, value) pairs, so that it is
hashable, and is shown to the user as a dict.

The six basic operators are selection, projection, renaming, union,
difference and Cartesian product. Natural join, intersection and division
are derived from them, as in Codd (1972).

An expression is a nested tuple:
  ("rel", name)                  a relation of the database
  ("select", cond, e)            cond as below
  ("project", attrs, e)
  ("rename", {old: new}, e)
  ("union", e1, e2), ("diff", e1, e2), ("product", e1, e2)
  ("join", e1, e2), ("intersect", e1, e2), ("divide", e1, e2)
A condition is ("eq", a, b) or ("lt", a, b), where a and b are attribute
names or ("const", v), or ("and", c1, c2), ("or", c1, c2), ("not", c).
"""

from collections.abc import Hashable, Iterable, Mapping

Tup = tuple[tuple[Hashable, Hashable], ...]


class Relation:
    __slots__ = ("schema", "rows")

    def __init__(self, schema: Iterable[Hashable], rows: Iterable[Mapping[Hashable, Hashable]] = ()):
        self.schema = frozenset(schema)
        out = set()
        for r in rows:
            if set(r) != self.schema:
                raise ValueError(f"tuple {dict(r)} does not match schema {sorted(self.schema)}")
            out.add(tuple(sorted(r.items(), key=lambda kv: repr(kv[0]))))
        self.rows: frozenset[Tup] = frozenset(out)

    def tuples(self) -> list[dict]:
        return sorted((dict(t) for t in self.rows), key=lambda d: sorted(map(repr, d.items())))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Relation) and self.schema == other.schema and self.rows == other.rows

    def __hash__(self) -> int:
        return hash((self.schema, self.rows))

    def __len__(self) -> int:
        return len(self.rows)

    def __repr__(self) -> str:
        return f"Relation({sorted(self.schema, key=repr)}, {self.tuples()})"


def _value(t: Mapping, term: object) -> object:
    if isinstance(term, tuple) and len(term) == 2 and term[0] == "const":
        return term[1]
    return t[term]


def holds(cond: tuple, t: Mapping) -> bool:
    op = cond[0]
    if op == "eq":
        return _value(t, cond[1]) == _value(t, cond[2])
    if op == "lt":
        return _value(t, cond[1]) < _value(t, cond[2])
    if op == "and":
        return holds(cond[1], t) and holds(cond[2], t)
    if op == "or":
        return holds(cond[1], t) or holds(cond[2], t)
    if op == "not":
        return not holds(cond[1], t)
    raise ValueError(f"unknown condition {op!r}")


# The six basic operators.


def select(r: Relation, cond: tuple) -> Relation:
    return Relation(r.schema, (t for t in map(dict, r.rows) if holds(cond, t)))


def project(r: Relation, attrs: Iterable[Hashable]) -> Relation:
    xs = frozenset(attrs)
    if not xs <= r.schema:
        raise ValueError("projection on attributes outside the schema")
    return Relation(xs, ({a: v for a, v in t if a in xs} for t in r.rows))


def rename(r: Relation, mapping: Mapping[Hashable, Hashable]) -> Relation:
    new = [mapping.get(a, a) for a in r.schema]
    if len(set(new)) != len(new):
        raise ValueError("renaming makes two attributes equal")
    return Relation(new, ({mapping.get(a, a): v for a, v in t} for t in r.rows))


def union(r: Relation, s: Relation) -> Relation:
    if r.schema != s.schema:
        raise ValueError("union needs equal schemas")
    return Relation(r.schema, map(dict, r.rows | s.rows))


def difference(r: Relation, s: Relation) -> Relation:
    if r.schema != s.schema:
        raise ValueError("difference needs equal schemas")
    return Relation(r.schema, map(dict, r.rows - s.rows))


def product(r: Relation, s: Relation) -> Relation:
    if r.schema & s.schema:
        raise ValueError("product needs disjoint schemas; rename first")
    return Relation(r.schema | s.schema, ({**dict(t), **dict(u)} for t in r.rows for u in s.rows))


# Derived operators, written only with the six above.


def natural_join(r: Relation, s: Relation) -> Relation:
    common = sorted(r.schema & s.schema, key=repr)
    fresh = {a: ("join-copy", a) for a in common}
    p = product(r, rename(s, fresh))
    cond: tuple = ("eq", ("const", 0), ("const", 0))
    for a in common:
        cond = ("and", cond, ("eq", a, fresh[a]))
    return project(select(p, cond), r.schema | s.schema)


def intersection(r: Relation, s: Relation) -> Relation:
    return difference(r, difference(r, s))


def division(r: Relation, s: Relation) -> Relation:
    """The X-values of r that occur with every tuple of s, where X = schema(r) - schema(s)."""
    x = r.schema - s.schema
    px = project(r, x)
    return difference(px, project(difference(product(px, s), r), x))


def natural_join_direct(r: Relation, s: Relation) -> Relation:
    """The join by its definition, with a hash table on the common attributes (a reference)."""
    common = sorted(r.schema & s.schema, key=repr)
    index: dict[tuple, list[dict]] = {}
    for u in map(dict, s.rows):
        index.setdefault(tuple(u[a] for a in common), []).append(u)
    out = []
    for t in map(dict, r.rows):
        for u in index.get(tuple(t[a] for a in common), ()):
            out.append({**t, **u})
    return Relation(r.schema | s.schema, out)


def evaluate(expr: tuple, db: Mapping[str, Relation]) -> Relation:
    """Evaluate an expression tree against a database (a dict of named relations)."""
    op = expr[0]
    if op == "rel":
        return db[expr[1]]
    if op == "select":
        return select(evaluate(expr[2], db), expr[1])
    if op == "project":
        return project(evaluate(expr[2], db), expr[1])
    if op == "rename":
        return rename(evaluate(expr[2], db), expr[1])
    binary = {
        "union": union,
        "diff": difference,
        "product": product,
        "join": natural_join,
        "intersect": intersection,
        "divide": division,
    }
    if op in binary:
        return binary[op](evaluate(expr[1], db), evaluate(expr[2], db))
    raise ValueError(f"unknown operator {op!r}")
