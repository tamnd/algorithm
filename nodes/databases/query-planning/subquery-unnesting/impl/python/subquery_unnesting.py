# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subquery-unnesting/. The authors are listed in prov/0C9G7B.jsonl.
"""Unnesting of subqueries in WHERE, with SQL nulls, on top of the dbrel helper.

The outer table is R(k, x) and the inner table is S(k, v), both bags. The
query keeps the rows of R that pass one of these WHERE conditions:

    ("exists",)            EXISTS (SELECT * FROM S WHERE S.k = R.k)
    ("not_exists",)        NOT EXISTS (SELECT * FROM S WHERE S.k = R.k)
    ("in",)                R.k IN (SELECT S.k FROM S)
    ("not_in",)            R.k NOT IN (SELECT S.k FROM S)
    ("scalar", op, agg)    R.x op (SELECT agg(S.v) FROM S WHERE S.k = R.k)

where op is one of =, <>, <, <=, >, >= and agg is count_star, count, sum,
min or max. nested() evaluates the query by its definition, once per row of
R. unnest() returns the rewritten query evaluated with joins, semijoins,
antijoins and one grouping. kim_unnest() is the rewrite with an inner join
that has the COUNT bug, and general_unnest() is the rewrite through the set of
distinct outer values, in the style of Neumann and Kemper.
"""

from collections import Counter
from typing import Tuple

import dbrel
from dbrel import Relation, cmp3, tv_not, tv_or

OPS = ("=", "<>", "<", "<=", ">", ">=")
AGGS = ("count_star", "count", "sum", "min", "max")


def _check(R: Relation, S: Relation, cond: Tuple) -> None:
    if sorted(R.schema) != ["k", "x"] or sorted(S.schema) != ["k", "v"]:
        raise ValueError("R must have the attributes k, x and S the attributes k, v")
    if R.mode != dbrel.BAG or S.mode != dbrel.BAG:
        raise ValueError("SQL tables are bags")
    if not cond or cond[0] not in ("exists", "not_exists", "in", "not_in", "scalar"):
        raise ValueError("unknown condition %r" % (cond,))
    if cond[0] == "scalar" and (len(cond) != 3 or cond[1] not in OPS or cond[2] not in AGGS):
        raise ValueError("a scalar condition is ('scalar', op, agg)")


def empty_value(agg: str):
    """The value of the aggregate on an empty input: 0 for the counts, NULL for the others."""
    return dbrel.agg_value(agg, [])


def nested(R: Relation, S: Relation, cond: Tuple) -> Relation:
    """The original query: for each row of R, evaluate the subquery and the condition."""
    _check(R, S, cond)
    out = {}
    for t, c in R.rows.items():
        r = R.as_dict(t)
        inner = dbrel.select(S, lambda s: cmp3("=", s["k"], r["k"]))
        if cond[0] == "exists":
            ok = len(inner) > 0
        elif cond[0] == "not_exists":
            ok = len(inner) == 0
        elif cond[0] in ("in", "not_in"):
            found = False
            for u in S.rows:
                found = tv_or(found, cmp3("=", r["k"], S.as_dict(u)["k"]))
            ok = found if cond[0] == "in" else tv_not(found)
        else:
            _, op, agg = cond
            (row,) = dbrel.aggregate(inner, [], [(agg, "v", "a")]).rows
            ok = cmp3(op, r["x"], row[0])
        if ok is True:
            out[t] = c
    return Relation(R.schema, out)


def left_outer_join_on_k(R: Relation, G: Relation) -> Relation:
    """R left outer join G on R.k = G.k; G has k and other attributes, and its k is renamed gk."""
    G2 = dbrel.rename(G, {"k": "gk"})
    matched = dbrel.theta_join(R, G2, lambda row: cmp3("=", row["k"], row["gk"]))
    pad = Relation(G2.schema, [tuple(None for _ in G2.schema)])
    unmatched = dbrel.product(dbrel.antijoin(R, G), pad)
    return dbrel.union(matched, unmatched)


def null_aware_antijoin(R: Relation, S: Relation) -> Relation:
    """R.k NOT IN (SELECT S.k FROM S) as an antijoin that keeps the SQL result with nulls."""
    if len(S) == 0:
        return R
    if any(S.as_dict(u)["k"] is None for u in S.rows):
        return Relation(R.schema, [])
    return dbrel.antijoin(dbrel.select(R, lambda r: r["k"] is not None), S)


def unnest(R: Relation, S: Relation, cond: Tuple) -> Relation:
    """The rewritten query, with no evaluation of the subquery per row."""
    _check(R, S, cond)
    kind = cond[0]
    if kind in ("exists", "in"):  # @line L1
        return dbrel.semijoin(R, dbrel.project(S, ["k"]))
    if kind == "not_exists":  # @line L2
        return dbrel.antijoin(R, dbrel.project(S, ["k"]))
    if kind == "not_in":  # @line L3
        return null_aware_antijoin(R, dbrel.project(S, ["k"]))
    _, op, agg = cond
    G = dbrel.aggregate(S, ["k"], [(agg, "v", "a")])  # @line L4
    if empty_value(agg) is not None:  # @line L5
        T = left_outer_join_on_k(R, G)
        gi, ai, rows = T.index("gk"), T.index("a"), Counter()
        for row, c in T.rows.items():
            row = list(row)
            if row[gi] is None:  # a padded row: the group of R.k is empty
                row[ai] = empty_value(agg)
            rows[tuple(row)] += c
        T = Relation(T.schema, rows)
    else:
        T = dbrel.theta_join(R, dbrel.rename(G, {"k": "gk"}), lambda row: cmp3("=", row["k"], row["gk"]))  # @line L6
    return dbrel.project(dbrel.select(T, lambda row: cmp3(op, row["x"], row["a"])), R.schema)  # @line L7


def kim_unnest(R: Relation, S: Relation, cond: Tuple) -> Relation:
    """Kim's rewrite of a scalar aggregate: group S by k and join with an inner join."""
    _check(R, S, cond)
    if cond[0] != "scalar":
        raise ValueError("Kim's rewrite here is for scalar aggregates")
    _, op, agg = cond
    G = dbrel.rename(dbrel.aggregate(S, ["k"], [(agg, "v", "a")]), {"k": "gk"})
    T = dbrel.theta_join(R, G, lambda row: cmp3("=", row["k"], row["gk"]))
    return dbrel.project(dbrel.select(T, lambda row: cmp3(op, row["x"], row["a"])), R.schema)


def general_unnest(R: Relation, S: Relation, cond: Tuple, null_safe: bool = True) -> Relation:
    """Unnesting through the distinct outer values D, then a join back to R.

    D = DISTINCT R.k. The subquery is computed once for each value of D by an
    outer join of D with S and a grouping by D.k, so every value of D gets a
    result, also the empty one. The join back to R must treat two nulls as
    equal (IS NOT DISTINCT FROM); with null_safe=False it uses =, which loses
    the rows of R whose k is NULL.
    """
    _check(R, S, cond)
    if cond[0] != "scalar":
        raise ValueError("general_unnest here is for scalar aggregates")
    _, op, agg = cond
    D = dbrel.rename(dbrel.distinct(dbrel.project(R, ["k"])), {"k": "d"})
    S2 = dbrel.rename(S, {"k": "sk"})
    DS = dbrel.union(dbrel.theta_join(D, S2, lambda row: cmp3("=", row["d"], row["sk"])),
                     dbrel.product(dbrel.select(D, lambda row: not any(cmp3("=", row["d"], S2.as_dict(u)["sk"])
                                                                         for u in S2.rows)),
                                   Relation(S2.schema, [(None, None)])))
    inner_agg = (agg, "v", "a") if agg != "count_star" else ("count", "sk", "a")
    T = dbrel.aggregate(DS, ["d"], [inner_agg])

    def same(row):
        if null_safe and row["k"] is None and row["d"] is None:
            return True
        return cmp3("=", row["k"], row["d"])

    J = dbrel.theta_join(R, T, same)
    return dbrel.project(dbrel.select(J, lambda row: cmp3(op, row["x"], row["a"])), R.schema)
