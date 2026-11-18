# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delta-rules/. The authors are listed in prov/Q8ZX00.jsonl.

"""Delta rules for the bag relational algebra, applied by structural recursion.

A change is a signed Counter from tuples to nonzero integers: a positive
weight is an insertion of that many copies and a negative weight a deletion.
A bag is a change with only positive weights, and a set is a bag with weights
1. For a database D (dbrel Relations) and a change dD (a dict from relation
names to signed Counters, such that D + dD has no negative counts),
delta(expr, D, dD) returns (schema, dE) with

    E(D + dD) = E(D) + dE.

The rules use the old values E_i(D) of the subexpressions, which the code
computes with dbrel.evaluate. Expressions are the nested tuples of dbrel:
scan, select, project, rename, union (UNION ALL), difference (monus),
intersection (min), distinct, product, join, and aggregate with count_star,
count and sum.
"""

from collections import Counter
from collections.abc import Mapping

import dbrel


def _clean(c: Counter) -> Counter:
    return Counter({t: w for t, w in c.items() if w != 0})


def _reorder(schema_from, schema_to, c: Counter) -> Counter:
    pos = [schema_from.index(a) for a in schema_to]
    out: Counter = Counter()
    for t, w in c.items():
        out[tuple(t[i] for i in pos)] += w
    return out


def zjoin(sr, r: Mapping, ss, s: Mapping):
    """The natural join of two signed Counters: weights multiply. NULL never matches."""
    common = [a for a in sr if a in ss]
    rest = [a for a in ss if a not in common]
    pr = [sr.index(a) for a in common]
    ps = [ss.index(a) for a in common]
    prest = [ss.index(a) for a in rest]
    out: Counter = Counter()
    for t, w in r.items():
        k = tuple(t[i] for i in pr)
        if any(v is None for v in k):
            continue
        for u, x in s.items():
            if tuple(u[i] for i in ps) == k:
                out[t + tuple(u[i] for i in prest)] += w * x
    return tuple(sr) + tuple(rest), _clean(out)


def apply_change(rel: dbrel.Relation, d: Mapping) -> dbrel.Relation:
    """rel + d; raises an error if a count becomes negative."""
    c = Counter(rel.rows)
    for t, w in d.items():
        c[t] += w
    return dbrel.Relation(rel.schema, {t: w for t, w in c.items() if w != 0})


def new_db(db: Mapping, dd: Mapping) -> dict:
    return {name: apply_change(rel, dd.get(name, {})) for name, rel in db.items()}


AGGS = ("count_star", "count", "sum")


def delta(expr: tuple, db: Mapping, dd: Mapping):
    """Return (schema, dE) such that E(db + dd) = E(db) + dE."""
    op = expr[0]
    old = lambda e: dbrel.evaluate(e, db)
    if op == "scan":  # @line L1
        rel = db[expr[1]]
        return rel.schema, _clean(Counter(dd.get(expr[1], {})))
    if op == "select":  # @line L2
        sch, d = delta(expr[2], db, dd)
        return sch, Counter({t: w for t, w in d.items() if expr[1](dict(zip(sch, t))) is True})
    if op == "project":  # @line L3
        sch, d = delta(expr[2], db, dd)
        attrs = tuple(expr[1])
        return attrs, _clean(_reorder(sch, attrs, d))
    if op == "rename":
        sch, d = delta(expr[2], db, dd)
        return tuple(expr[1].get(a, a) for a in sch), d
    if op == "union":  # @line L4
        s1, d1 = delta(expr[1], db, dd)
        s2, d2 = delta(expr[2], db, dd)
        out = Counter(d1)
        out.update(_reorder(s2, s1, d2))
        return s1, _clean(out)
    if op in ("join", "product"):  # @line L5
        e1, e2 = old(expr[1]), old(expr[2])
        s1, d1 = delta(expr[1], db, dd)
        s2, d2 = delta(expr[2], db, dd)
        out: Counter = Counter()
        for a, b in ((d1, e2.reorder(s2).rows), (e1.reorder(s1).rows, d2), (d1, d2)):
            sch, part = zjoin(s1, a, s2, b)
            out.update(part)
        return sch, _clean(out)
    if op in ("difference", "intersection"):  # @line L6
        e1, e2 = old(expr[1]), old(expr[2])
        s1, d1 = delta(expr[1], db, dd)
        s2, d2 = delta(expr[2], db, dd)
        d2 = _reorder(s2, s1, d2)
        o1, o2 = e1.reorder(s1).rows, e2.reorder(s1).rows
        f = (lambda m, n: max(0, m - n)) if op == "difference" else min
        out = Counter()
        for t in set(d1) | set(d2):
            out[t] = f(o1[t] + d1[t], o2[t] + d2[t]) - f(o1[t], o2[t])
        return s1, _clean(out)
    if op == "distinct":  # @line L7
        e1 = old(expr[1])
        s1, d1 = delta(expr[1], db, dd)
        o1 = e1.reorder(s1).rows
        out = Counter({t: int(o1[t] + w > 0) - int(o1[t] > 0) for t, w in d1.items()})
        return s1, _clean(out)
    if op == "aggregate":  # @line L8
        group, aggs, sub = tuple(expr[1]), expr[2], expr[3]
        if any(f not in AGGS for f, _, _ in aggs):
            raise ValueError("only count_star, count and sum have delta rules here")
        e1 = old(sub)
        s1, d1 = delta(sub, db, dd)
        gpos = [s1.index(a) for a in group]
        o1 = e1.reorder(s1).rows
        touched = sorted({tuple(t[i] for i in gpos) for t in d1}, key=dbrel.row_key)
        schema = group + tuple(o for _, _, o in aggs)
        out: Counter = Counter()

        def summary(rows: Mapping, g: tuple):
            """For each aggregate: (count of rows, count of non-null values, sum)."""
            res = []
            for f, attr, _ in aggs:
                n = k = s = 0
                for t, w in rows.items():
                    if tuple(t[i] for i in gpos) != g:
                        continue
                    n += w
                    if f != "count_star" and t[s1.index(attr)] is not None:
                        k += w
                        s += w * t[s1.index(attr)]
                res.append((n, k, s))
            return res

        def row(g: tuple, stats) -> tuple:
            vals = []
            for (f, _, _), (n, k, s) in zip(aggs, stats):
                vals.append(n if f == "count_star" else k if f == "count" else (s if k > 0 else None))
            return g + tuple(vals)

        for g in touched:  # @line L9
            before = summary(o1, g)
            change = summary(d1, g)
            after = [tuple(x + y for x, y in zip(b, c)) for b, c in zip(before, change)]
            n_before, n_after = before[0][0], after[0][0]
            # With no grouping attributes the single result row always exists.
            if n_before > 0 or not group:
                out[row(g, before)] -= 1
            if n_after > 0 or not group:
                out[row(g, after)] += 1
        return schema, _clean(out)
    raise ValueError("no delta rule for %r" % (op,))


def maintain(view: dbrel.Relation, expr: tuple, db: Mapping, dd: Mapping) -> dbrel.Relation:
    """Apply the delta of expr to a materialized view of expr over db."""
    sch, d = delta(expr, db, dd)
    return apply_change(view, _reorder(sch, view.schema, d))
