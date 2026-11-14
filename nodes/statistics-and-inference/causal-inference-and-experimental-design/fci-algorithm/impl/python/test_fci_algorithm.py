# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fci-algorithm/. The authors are listed in prov/HH185A.jsonl.

import itertools
import random

from fci_algorithm import (
    dag_marks, fci, latent_oracle, m_oracle, m_separated, mag_of_dag, pag_edges,
)


def ancestor_sets(mark, nodes):
    parents = {v: {u for u in nodes if mark.get((u, v)) == '>' and mark.get((v, u)) == '-'} for v in nodes}
    anc = {}
    for v in nodes:
        seen, stack = set(), [v]
        while stack:
            x = stack.pop()
            for p in parents[x]:
                if p not in seen:
                    seen.add(p)
                    stack.append(p)
        anc[v] = seen
    return anc


def signature(oracle, nodes):
    sig = []
    for a, b in itertools.combinations(nodes, 2):
        rest = [v for v in nodes if v not in (a, b)]
        for k in range(len(rest) + 1):
            for s in itertools.combinations(rest, k):
                sig.append(oracle(a, b, set(s)))
    return tuple(sig)


def all_mags(n):
    """All maximal ancestral graphs with directed and bidirected edges on n nodes."""
    nodes = list(range(n))
    pairs = list(itertools.combinations(nodes, 2))
    out = []
    for choice in itertools.product(range(4), repeat=len(pairs)):
        mark = {}
        for (u, v), c in zip(pairs, choice):
            if c == 1:
                mark[(u, v)], mark[(v, u)] = '>', '-'
            elif c == 2:
                mark[(u, v)], mark[(v, u)] = '-', '>'
            elif c == 3:
                mark[(u, v)], mark[(v, u)] = '>', '>'
        anc = ancestor_sets(mark, nodes)
        if any(v in anc[v] for v in nodes):
            continue  # directed cycle
        if any(mark[(u, v)] == '>' and mark[(v, u)] == '>' and (u in anc[v] or v in anc[u]) for (u, v) in pairs if (u, v) in mark):
            continue  # almost directed cycle
        ok = True
        for u, v in pairs:
            if (u, v) in mark:
                continue
            rest = [w for w in nodes if w not in (u, v)]
            if not any(m_separated(mark, nodes, {u}, {v}, set(s)) for k in range(len(rest) + 1) for s in itertools.combinations(rest, k)):
                ok = False  # not maximal
                break
        if ok:
            out.append(mark)
    return out


def pag_of_class(members):
    """Marks shared by all MAGs of a class; other marks are circles."""
    pag = {}
    for e in members[0]:
        ms = {m[e] for m in members}
        pag[e] = ms.pop() if len(ms) == 1 else 'o'
    return pag


def mag_classes(n):
    nodes = list(range(n))
    classes = {}
    for m in all_mags(n):
        classes.setdefault(signature(m_oracle(m, nodes), nodes), []).append(m)
    return {sig: pag_of_class(ms) for sig, ms in classes.items()}, classes


CLASSES = {n: mag_classes(n) for n in (3, 4)}


def test_worked_example_with_latent():
    g = {"A": set(), "L": set(), "D": set(), "B": {"A", "L"}, "C": {"L", "D"}}
    obs = ["A", "B", "C", "D"]
    res = fci(obs, latent_oracle(g, obs))
    assert pag_edges(res.mark) == ["A o-> B", "B <-> C", "C <-o D"]


PDS_EXAMPLE = {"A": {"B", "L1"}, "B": {"C"}, "C": {"L2"}, "D": {"A", "L3"}, "E": {"L2", "L3"},
               "F": {"E", "L1"}, "L1": set(), "L2": set(), "L3": set()}


def test_possible_d_sep_phase_removes_an_edge():
    obs = list("ABCDEF")
    res = fci(obs, latent_oracle(PDS_EXAMPLE, obs))
    assert res.pds_removed == [("D", "F")]
    assert res.sepset[frozenset(("D", "F"))] == {"A", "B", "E"}
    assert pag_edges(res.mark) == ["A --> D", "A <-> F", "A <-o B", "B o-o C", "C o-> E", "D <-> E", "E --> F"]
    mag = mag_of_dag(PDS_EXAMPLE, obs)
    assert pag_edges(mag) == ["A --> D", "A <-- B", "A <-> F", "B <-- C", "C <-> E", "D <-> E", "E --> F"]
    for e, m in res.mark.items():
        assert m == 'o' or m == mag[e]


def test_m_separation_matches_dag_d_separation():
    # On DAGs, m-separation is d-separation; compare with the moral-graph method.
    rng = random.Random(5)
    for _ in range(50):
        n = 5
        parents = {v: {u for u in range(v) if rng.random() < 0.4} for v in range(n)}
        mark = dag_marks(parents)
        for a, b in itertools.combinations(range(n), 2):
            rest = [v for v in range(n) if v not in (a, b)]
            for k in range(3):
                for s in itertools.combinations(rest, k):
                    assert m_separated(mark, list(range(n)), {a}, {b}, set(s)) == moral_dsep(parents, a, b, set(s))


def moral_dsep(parents, a, b, s):
    keep, stack = {a, b} | s, [a, b, *s]
    while stack:
        v = stack.pop()
        for p in parents[v]:
            if p not in keep:
                keep.add(p)
                stack.append(p)
    nb = {v: set() for v in keep}
    for v in keep:
        ps = list(parents[v])
        for p in ps:
            nb[v].add(p)
            nb[p].add(v)
        for p, q in itertools.combinations(ps, 2):
            nb[p].add(q)
            nb[q].add(p)
    seen, stack = {a}, [a]
    while stack:
        v = stack.pop()
        if v == b:
            return False
        for w in nb[v]:
            if w not in seen and w not in s:
                seen.add(w)
                stack.append(w)
    return True


def test_number_of_mags_and_classes():
    pags3, classes3 = CLASSES[3]
    pags4, classes4 = CLASSES[4]
    # Counts found by this enumeration (MAGs without undirected edges).
    assert sum(len(c) for c in classes3.values()) == 56
    assert len(classes3) == 11  # on three nodes, the same independence models as DAGs
    assert sum(len(c) for c in classes4.values()) == 2492
    assert len(classes4) == 248  # 185 of them are DAG models


def check_every_mag(n):
    nodes = list(range(n))
    pags, classes = CLASSES[n]
    for sig, members in classes.items():
        want = pag_edges(pags[sig])
        for m in members:
            res = fci(nodes, m_oracle(m, nodes))
            assert pag_edges(res.mark) == want


def test_every_mag_on_three_nodes():
    check_every_mag(3)


def test_every_mag_on_four_nodes():
    check_every_mag(4)


def test_dags_without_latents_four_nodes():
    pags, _ = CLASSES[4]
    nodes = list(range(4))
    pairs = list(itertools.combinations(nodes, 2))
    count = 0
    for choice in itertools.product((0, 1, 2), repeat=6):
        parents = {v: set() for v in nodes}
        for (u, v), c in zip(pairs, choice):
            if c == 1:
                parents[v].add(u)
            elif c == 2:
                parents[u].add(v)
        mark = dag_marks(parents)
        if any(v in s for v, s in ancestor_sets(mark, nodes).items()):
            continue
        count += 1
        oracle = latent_oracle(parents, nodes)
        res = fci(nodes, oracle)
        assert pag_edges(res.mark) == pag_edges(pags[signature(oracle, nodes)])
    assert count == 543


def random_latent_dag(rng, n_obs, n_lat, p):
    names = list(range(n_obs)) + [f"L{i}" for i in range(n_lat)]
    order = names[:]
    rng.shuffle(order)
    parents = {v: set() for v in names}
    for i, j in itertools.combinations(range(len(order)), 2):
        if rng.random() < p:
            parents[order[j]].add(order[i])
    for lat in names[n_obs:]:
        # make each latent a source with at least two observed children
        parents[lat] = set()
    for v in names:
        parents[v] = {u for u in parents[v] if u in names}
    for lat in names[n_obs:]:
        kids = rng.sample(range(n_obs), 2)
        for k in kids:
            parents[k].add(lat)
    return parents


def test_latent_dags_four_observed_against_mag_classes():
    pags, _ = CLASSES[4]
    rng = random.Random(20261114)
    nodes = list(range(4))
    for _ in range(300):
        g = random_latent_dag(rng, 4, rng.choice((1, 2)), 0.35)
        if any(v in s for v, s in ancestor_sets(dag_marks(g), list(g)).items()):
            continue
        oracle = latent_oracle(g, nodes)
        res = fci(nodes, oracle)
        assert pag_edges(res.mark) == pag_edges(pags[signature(oracle, nodes)])


def test_soundness_on_larger_latent_dags():
    # Every non-circle mark of the output must agree with the MAG of the DAG,
    # and the skeleton must be the MAG skeleton. (Soundness check, not completeness.)
    rng = random.Random(99)
    checked = 0
    while checked < 40:
        g = random_latent_dag(rng, rng.choice((5, 6)), rng.choice((1, 2)), 0.3)
        if any(v in s for v, s in ancestor_sets(dag_marks(g), list(g)).items()):
            continue
        obs = [v for v in g if not str(v).startswith("L")]
        mag = mag_of_dag(g, obs)
        res = fci(obs, latent_oracle(g, obs))
        assert set(res.mark) == set(mag)
        for e, m in res.mark.items():
            assert m == 'o' or m == mag[e]
        checked += 1
