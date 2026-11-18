# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eager-aggregation/. The authors are listed in prov/B4N0ZP.jsonl.
"""Eager aggregation: a grouping below a join, with a final grouping above it.

The tables are R(g, k, x) and S(k, v), both bags. The query is

    SELECT G, agg_1, ..., agg_m FROM R JOIN S ON R.k = S.k GROUP BY G

where G is ["g"] or [] and each aggregate is (func, attr, out) with func one
of count_star, count, sum, min, max, avg and attr "v" (a column of S), "x" (a
column of R) or None for count_star. lazy() evaluates the query as written.
eager() groups S by its join column k first, joins the partial results with
R, and combines them with a final grouping. For an aggregate of a column of
R, each row of R stands for c joined rows, where c is the number of rows of S
in the partial group, so sums and counts of R columns are weighted by c. This
is eager group-by on S combined with eager count, in the terms of Yan and
Larson. eager_without_final() also drops the final grouping, which is right
only when g is a key of R.
"""

from fractions import Fraction
from typing import List, Sequence, Tuple

import dbrel
from dbrel import Relation

FUNCS = ("count_star", "count", "sum", "min", "max", "avg")
COUNTS = ("count_star", "count")


def _check(R: Relation, S: Relation, group: Sequence[str], aggs: Sequence[Tuple]) -> None:
    if sorted(R.schema) != ["g", "k", "x"] or sorted(S.schema) != ["k", "v"]:
        raise ValueError("R must have the attributes g, k, x and S the attributes k, v")
    if R.mode != dbrel.BAG or S.mode != dbrel.BAG:
        raise ValueError("SQL tables are bags")
    if list(group) not in (["g"], []):
        raise ValueError("the grouping is ['g'] or []")
    outs = set()
    for agg in aggs:
        if len(agg) != 3 or agg[0] not in FUNCS:
            raise ValueError("an aggregate is (func, attr, out) with func in %r" % (FUNCS,))
        func, attr, out = agg
        if (func == "count_star") != (attr is None) or attr not in (None, "v", "x"):
            raise ValueError("bad attribute %r for %s" % (attr, func))
        if out in outs or out in ("g", "k", "x", "v", "c"):
            raise ValueError("bad output name %r" % (out,))
        outs.add(out)


def lazy(R: Relation, S: Relation, group: Sequence[str], aggs: Sequence[Tuple]) -> Relation:
    """The query as written: the join first, then one grouping."""
    _check(R, S, group, aggs)
    return dbrel.aggregate(dbrel.natural_join(R, S), list(group), list(aggs))


def _partials(aggs: Sequence[Tuple]) -> List[Tuple]:
    """The partial aggregates of S, grouped by k. c counts the rows of each group."""
    out = [("count_star", None, "c")]
    for i, (func, attr, _) in enumerate(aggs):
        if attr != "v":
            continue
        if func == "avg":
            out += [("sum", "v", "p%d_s" % i), ("count", "v", "p%d_n" % i)]
        else:
            out.append((func, "v", "p%d" % i))
    return out


def _finals(aggs: Sequence[Tuple]) -> List[Tuple]:
    """The final aggregates over the join of R with the partial results."""
    out = []
    for i, (func, attr, _) in enumerate(aggs):
        if func == "count_star":
            out.append(("sum", "c", "f%d" % i))
        elif attr == "v" and func == "avg":
            out += [("sum", "p%d_s" % i, "f%d_s" % i), ("sum", "p%d_n" % i, "f%d_n" % i)]
        elif attr == "v":
            out.append(("min" if func == "min" else "max" if func == "max" else "sum", "p%d" % i, "f%d" % i))
        elif func in ("min", "max"):
            out.append((func, "x", "f%d" % i))  # copies of a row do not change MIN and MAX
        elif func == "sum":
            out.append(("sum", "xc", "f%d" % i))
        elif func == "count":
            out.append(("sum", "cx", "f%d" % i))
        else:
            out += [("sum", "xc", "f%d_s" % i), ("sum", "cx", "f%d_n" % i)]
    return out


def _weighted(J: Relation) -> Relation:
    """J with the columns xc = x * c and cx = c, both NULL where x is NULL."""
    xi, ci = J.index("x"), J.index("c")
    rows = {}
    for t, m in J.rows.items():
        x, c = t[xi], t[ci]
        u = t + ((None, None) if x is None else (x * c, c))
        rows[u] = rows.get(u, 0) + m
    return Relation(J.schema + ("xc", "cx"), rows)


def _finish(F: Relation, group: Sequence[str], aggs: Sequence[Tuple]) -> Relation:
    """Replace NULL counts by 0 and divide the sums of each AVG."""
    rows = {}
    for t, m in F.rows.items():
        r = F.as_dict(t)
        u = [r[a] for a in group]
        for i, (func, _, _) in enumerate(aggs):
            if func == "avg":
                s, n = r["f%d_s" % i], r["f%d_n" % i] or 0
                u.append(None if n == 0 else Fraction(s, 1) / n)
            elif func in COUNTS:
                u.append(r["f%d" % i] or 0)
            else:
                u.append(r["f%d" % i])
        rows[tuple(u)] = rows.get(tuple(u), 0) + m
    return Relation(tuple(group) + tuple(out for _, _, out in aggs), rows)


def eager(R: Relation, S: Relation, group: Sequence[str], aggs: Sequence[Tuple]) -> Relation:
    """The rewritten query: group S by k, join with R, then group by G."""
    _check(R, S, group, aggs)
    P = dbrel.aggregate(S, ["k"], _partials(aggs))  # @line L1
    J = dbrel.natural_join(R, P)  # @line L2
    J = _weighted(J)  # @line L3
    F = dbrel.aggregate(J, list(group), _finals(aggs))  # @line L4
    return _finish(F, group, aggs)  # @line L5


def eager_without_final(R: Relation, S: Relation, aggs: Sequence[Tuple]) -> Relation:
    """Eager aggregation with no grouping above the join, for GROUP BY g.

    Each row of the join of R with the partial results becomes one result row.
    This equals the query only when no two joined rows of R share a value of g,
    for example when g is a key of R.
    """
    _check(R, S, ["g"], aggs)
    J = _weighted(dbrel.natural_join(R, dbrel.aggregate(S, ["k"], _partials(aggs))))
    rows = {}
    for t, m in J.rows.items():
        one = Relation(J.schema, {t: 1})
        for u in _finish(dbrel.aggregate(one, ["g"], _finals(aggs)), ["g"], aggs).rows:
            rows[u] = rows.get(u, 0) + m
    return Relation(("g",) + tuple(out for _, _, out in aggs), rows)


def join_sizes(R: Relation, S: Relation) -> Tuple[int, int]:
    """The number of rows that the join reads from S, without and with the grouping below it."""
    P = dbrel.aggregate(S, ["k"], [("count_star", None, "c")])
    return len(dbrel.natural_join(R, S)), len(dbrel.natural_join(R, P))
