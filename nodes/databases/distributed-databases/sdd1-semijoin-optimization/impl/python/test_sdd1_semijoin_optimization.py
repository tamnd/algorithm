# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdd1-semijoin-optimization/. The authors are listed in prov/ER70WT.jsonl.

import random
from collections import Counter
from fractions import Fraction as F

import pytest

import dbrel
from sdd1_semijoin_optimization import (Estimate, Profile, Table, candidates, execute, full_reducer, opt,
                                        reduce_by, replay, semijoin_values, yao_approx)


def paper_profile():
    """Section 4.3 of Bernstein et al. (1981), with 10,000 values in the domains of s# and p#."""
    domains = {"s#": (10000, 1), "p#": (10000, 1), "location": (50, 1), "type": (5, 1),
               "sname": (None, 1), "pname": (None, 1)}
    return Profile(
        domains=domains,
        sites={"S": 1, "Y": 2, "P": 3},
        card={"S": 10000, "Y": 100000, "P": 10000},
        distinct={"S": {"s#": 10000, "location": 50}, "Y": {"s#": 1000, "p#": 1000},
                  "P": {"p#": 10000, "type": 5}},
        schema={"S": ("s#", "sname", "location"), "Y": ("s#", "p#"), "P": ("p#", "pname", "type")},
    )


PAPER_SELECTIONS = [("S", "location", F(1, 50)), ("P", "type", F(1, 5))]


def test_paper_first_table():
    est = Estimate.start(paper_profile())
    for r, a, f in PAPER_SELECTIONS:
        est.select(r, a, f)
    assert est.card == {"S": 200, "Y": 100000, "P": 2000}
    table = {sj: (est.cost(*sj), est.benefit(*sj)) for sj in candidates(est.profile)}
    assert table == {
        ("S", "Y", "s#"): (1000, 180 * 3),
        ("P", "Y", "p#"): (1000, 1800 * 3),
        ("Y", "S", "s#"): (200, 98000 * 2),
        ("Y", "P", "p#"): (2000, 80000 * 2),
    }


def test_paper_example():
    plan = opt(paper_profile(), PAPER_SELECTIONS, prune=False)
    assert [(sj, c) for sj, c, _ in plan.trace] == [
        (("Y", "S", "s#"), 200), (("P", "Y", "p#"), 1000), (("Y", "P", "p#"), 200), (("S", "Y", "s#"), 20)]
    assert [b for _, _, b in plan.trace] == [196000, 5400, 3200, 540]
    assert plan.assembly == 2
    sj_cost, move, site, est = replay(paper_profile(), plan.program)
    assert (sj_cost, move, site) == (1420, 660, 2)
    assert est.card == {"S": 20, "Y": 400, "P": 200}
    assert plan.cost == 2080


def test_paper_example_pruned():
    plan = opt(paper_profile(), PAPER_SELECTIONS)
    assert plan.cost_before_pruning == 2080 and plan.cost == 1880
    assert plan.pruned == [("semijoin", "Y", "P", "p#")]
    assert [op[1:] for op in plan.program if op[0] == "semijoin"] == [
        ("Y", "S", "s#"), ("P", "Y", "p#"), ("S", "Y", "s#")]


def test_yao_approx_pieces():
    assert yao_approx(10, 100) == 10
    assert yao_approx(50, 100) == 50
    assert yao_approx(200, 100) == 100
    assert yao_approx(F(140), 100) == 80
    for b in (3, 10, 40):
        for n in range(0, 5 * b):
            v = yao_approx(n, b)
            assert v <= b and v <= max(n, F(b + n) / 3)


def random_query(rng):
    """A chain, a star or a triangle of 3 or 4 relations at random sites, with random rows."""
    shape = rng.choice(["chain", "star", "triangle"])
    if shape == "chain":
        n = rng.randint(2, 4)
        schemas = {f"R{i}": (f"A{i}", f"A{i + 1}") for i in range(n)}
    elif shape == "star":
        schemas = {"R0": ("A0", "A1", "A2"), "R1": ("A0", "B1"), "R2": ("A1", "B2"), "R3": ("A2", "B3")}
    else:
        schemas = {"R0": ("A", "B"), "R1": ("B", "C"), "R2": ("C", "A")}
    rels = {r: dbrel.random_relation(rng, s, rng.randint(0, 8), domain=3, null_rate=0.1) for r, s in schemas.items()}
    sites = {r: rng.randint(0, 2) for r in schemas}
    return schemas, rels, sites


def to_table(rel):
    return Table(rel.schema, Counter(rel.rows))


def to_rel(t):
    return dbrel.Relation(t.schema, t.rows)


def join_all(rels):
    names = sorted(rels)
    out = rels[names[0]]
    for r in names[1:]:
        out = dbrel.natural_join(out, rels[r])
    return out


def profile_of(rels, sites, widths):
    attrs = sorted({a for r in rels.values() for a in r.schema})
    domains = {a: (3, widths[a]) for a in attrs}
    distinct = {}
    for name, r in rels.items():
        distinct[name] = {a: max(1, len({t[r.index(a)] for t in r.rows if t[r.index(a)] is not None}))
                          for a in r.schema}
    return Profile(domains, dict(sites), {n: max(1, len(r)) for n, r in rels.items()}, distinct,
                   {n: r.schema for n, r in rels.items()})


@pytest.mark.parametrize("seed", range(60))
def test_opt_program_gives_the_join(seed):
    rng = random.Random(seed)
    schemas, rels, sites = random_query(rng)
    widths = {a: rng.randint(1, 3) for s in schemas.values() for a in s}
    plan = opt(profile_of(rels, sites, widths))
    run = execute({r: to_table(v) for r, v in rels.items()}, sites, widths, plan.program, plan.assembly)
    assert to_rel(run.result) == join_all(rels)


@pytest.mark.parametrize("seed", range(60))
def test_any_semijoin_program_keeps_the_join_and_counts_bytes(seed):
    rng = random.Random(1000 + seed)
    schemas, rels, sites = random_query(rng)
    widths = {a: rng.randint(1, 3) for s in schemas.values() for a in s}
    names = sorted(schemas)
    program = []
    for _ in range(rng.randint(0, 6)):
        i, j = rng.sample(names, 2)
        common = sorted(set(schemas[i]) & set(schemas[j]))
        if common:
            program.append(("semijoin", i, j, rng.choice(common)))
    run = execute({r: to_table(v) for r, v in rels.items()}, sites, widths, program, assembly=0)
    assert to_rel(run.result) == join_all(rels)
    # The same program by the reference operators, with its cost counted from the definition.
    cur = dict(rels)
    sj = 0
    for _, i, j, a in program:
        proj = dbrel.distinct(dbrel.select(dbrel.project(cur[j], [a]), lambda row: row[a] is not None))
        if sites[i] != sites[j]:
            sj += len(proj) * widths[a]
        cur[i] = dbrel.semijoin(cur[i], proj)
    assert run.semijoin_bytes == sj
    assert {r: to_rel(t) for r, t in run.reduced.items()} == cur
    assert run.move_bytes == sum(len(cur[r]) * sum(widths[a] for a in schemas[r]) for r in names if sites[r] != 0)


@pytest.mark.parametrize("seed", range(40))
def test_greedy_choice_and_stop(seed):
    rng = random.Random(2000 + seed)
    schemas, rels, sites = random_query(rng)
    widths = {a: rng.randint(1, 3) for s in schemas.values() for a in s}
    p = profile_of(rels, sites, widths)
    plan = opt(p, prune=False)
    est = Estimate.start(p)
    used = set()
    assert len(plan.trace) <= len(candidates(p))
    for sj, cost, benefit in plan.trace:
        profits = [est.benefit(*c) - est.cost(*c) for c in candidates(p) if c not in used]
        assert benefit - cost == max(profits) > 0
        assert (cost, benefit) == (est.cost(*sj), est.benefit(*sj))
        est.semijoin(*sj)
        used.add(sj)
    assert all(est.benefit(*c) <= est.cost(*c) for c in candidates(p) if c not in used)
    pruned = opt(p)
    assert pruned.cost <= plan.cost
    assert all(p.sites[op[1]] == pruned.assembly for op in pruned.pruned)


def fully_reduced(rels, reduced):
    """Each relation keeps exactly its rows that take part in the join: the rows that meet
    the full join on the attributes the relation shares with the others (a null in an
    attribute of its own does not stop a row from joining)."""
    full = join_all(rels)
    for r in rels:
        shared = [a for a in rels[r].schema if any(a in rels[s].schema for s in rels if s != r)]
        if reduced[r] != dbrel.semijoin(rels[r], dbrel.project(full, shared)):
            return False
    return True


@pytest.mark.parametrize("seed", range(40))
def test_full_reducer_for_tree_queries(seed):
    rng = random.Random(3000 + seed)
    if seed % 2:
        schemas = {"R0": ("A", "B"), "R1": ("B", "C"), "R2": ("C", "D"), "R3": ("C", "E")}
        parent = {"R0": None, "R1": "R0", "R2": "R1", "R3": "R1"}
    else:
        schemas = {"R0": ("A", "B", "C"), "R1": ("B", "C", "D"), "R2": ("D", "E")}
        parent = {"R1": None, "R0": "R1", "R2": "R1"}
    rels = {r: dbrel.random_relation(rng, s, rng.randint(1, 9), domain=3, null_rate=0.05) for r, s in schemas.items()}
    program = full_reducer(parent, schemas)
    assert len(program) == 2 * (len(schemas) - 1)
    run = execute({r: to_table(v) for r, v in rels.items()}, {r: r for r in rels}, {a: 1 for s in schemas.values() for a in s},
                  program, assembly="R0")
    assert fully_reduced(rels, {r: to_rel(t) for r, t in run.reduced.items()})


def test_cyclic_query_has_no_full_reducer_here():
    rels = {"R": dbrel.Relation(("A", "B"), [(0, 0), (1, 1)]),
            "S": dbrel.Relation(("B", "C"), [(0, 0), (1, 1)]),
            "T": dbrel.Relation(("C", "A"), [(0, 1), (1, 0)])}
    assert len(join_all(rels)) == 0
    tables = {r: to_table(v) for r, v in rels.items()}
    for i in rels:
        for j in rels:
            for a in set(rels[i].schema) & set(rels[j].schema):
                if i != j:
                    assert reduce_by(tables[i], a, semijoin_values(tables[j], a)).rows == tables[i].rows
    assert not fully_reduced(rels, rels)


def test_local_selection_and_same_site():
    p = Profile({"A": (10, 1), "B": (10, 2)}, {"R": 0, "S": 0}, {"R": 10, "S": 10},
                {"R": {"A": 10, "B": 10}, "S": {"B": 5}}, {"R": ("A", "B"), "S": ("B",)})
    assert candidates(p) == []  # both relations at one site: no nonlocal semijoin
    plan = opt(p, [("R", "A", F(1, 2))])
    assert plan.program == [("select", "R", "A", F(1, 2))] and plan.cost == 0
    rel = Table(("A", "B"), Counter({(1, 1): 2, (2, None): 1}))
    run = execute({"R": rel}, {"R": 0}, {"A": 1, "B": 1}, [("select", "R")], 0, {"R": lambda row: row["A"] == 1})
    assert run.result.rows == Counter({(1, 1): 2})
