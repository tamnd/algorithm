# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dalal-revision/. The authors are listed in prov/WXMFTE.jsonl.

import itertools
import random

import pytest

from dalal_revision import dalal_distance, dalal_revision, dalal_revision_with_stats, hamming


def worlds(n):
    return range(1 << n)


def random_set(rng, n, prob):
    return frozenset(w for w in worlds(n) if rng.random() < prob)


def brute_force(k, p, n):
    """Models of p at minimum Hamming distance from some model of k, by all pairs."""
    k, p = frozenset(k), frozenset(p)
    if not p:
        return frozenset()
    if not k:
        return p
    dist = {w: min(hamming(w, v) for v in k) for w in p}
    best = min(dist.values())
    return frozenset(w for w in p if dist[w] == best)


def all_subsets(n):
    ws = list(worlds(n))
    for mask in range(1 << len(ws)):
        yield frozenset(w for j, w in enumerate(ws) if mask >> j & 1)


# The six KM postulates, with formulas given by their sets of models.
def km_violations(op, k, p, q, n):
    bad = []
    r = op(k, p, n)
    if not r <= p:
        bad.append("R1")
    if k & p and r != k & p:
        bad.append("R2")
    if p and not r:
        bad.append("R3")
    if op(list(k)[::-1], sorted(p, reverse=True), n) != r:
        bad.append("R4")
    rpq = op(k, p & q, n)
    if not (r & q) <= rpq:
        bad.append("R5")
    if r & q and not rpq <= r & q:
        bad.append("R6")
    return bad


# Atoms a, b, c, d are bits 0, 1, 2, 3. The example of the page is Example 3.3 of
# Eiter and Gottlob (1992): K = a and b and c, p = (not a and d) or (a and not b and not c and not d).
A, B, C, D = 1, 2, 4, 8


def page_example():
    n = 4
    k = frozenset(w for w in worlds(n) if w & A and w & B and w & C)
    p = frozenset(w for w in worlds(n) if (not w & A and w & D) or w == A)
    return k, p, n


def test_page_example():
    k, p, n = page_example()
    assert k == {A | B | C, A | B | C | D}
    assert p == {D, B | D, C | D, B | C | D, A}
    result, d, visited, flips = dalal_revision_with_stats(k, p, n)
    assert d == 1
    assert result == {B | C | D}
    # Layer 0 has 2 worlds, layer 1 adds 6 new worlds, after 2 * 4 flips.
    assert visited == 8 and flips == 8
    # Distances of the five models of p to Mod(K).
    assert {w: min(hamming(w, v) for v in k) for w in p} == {D: 3, B | D: 2, C | D: 2, B | C | D: 1, A: 2}


def test_dalal_small_example():
    # K = a and not b, p = b, over two atoms (Dalal 1988, Section 3): the result is a and b.
    assert dalal_revision({A}, {B, A | B}, 2) == {A | B}
    assert dalal_distance({A}, {B, A | B}, 2) == 1


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5])
def test_matches_brute_force(n):
    rng = random.Random(1000 + n)
    for _ in range(300):
        k = random_set(rng, n, rng.choice([0.05, 0.2, 0.5]))
        p = random_set(rng, n, rng.choice([0.05, 0.2, 0.5]))
        r = dalal_revision(k, p, n)
        assert r == brute_force(k, p, n)
        d = dalal_distance(k, p, n)
        if k and p:
            assert d == min(hamming(u, v) for u in k for v in p)
        else:
            assert d is None


def test_exhaustive_two_atoms():
    for k in all_subsets(2):
        for p in all_subsets(2):
            assert dalal_revision(k, p, 2) == brute_force(k, p, 2)


def test_empty_cases():
    assert dalal_revision(set(), {1, 2}, 2) == {1, 2}
    assert dalal_revision({1}, set(), 2) == set()
    assert dalal_revision(set(), set(), 3) == set()
    assert dalal_revision({0}, {0}, 0) == {0}


def test_bad_world_rejected():
    with pytest.raises(ValueError):
        dalal_revision({4}, {1}, 2)
    with pytest.raises(ValueError):
        dalal_revision({1}, {-1}, 2)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_km_postulates_dalal(n):
    rng = random.Random(2000 + n)
    for _ in range(200):
        k = random_set(rng, n, rng.choice([0.0, 0.1, 0.3, 0.6]))
        p = random_set(rng, n, rng.choice([0.1, 0.3, 0.6]))
        q = random_set(rng, n, rng.choice([0.2, 0.5, 0.8]))
        assert km_violations(dalal_revision, k, p, q, n) == []


def test_km_postulates_dalal_exhaustive_two_atoms():
    subsets = list(all_subsets(2))
    for k in subsets:
        for p in subsets:
            for q in subsets:
                assert km_violations(dalal_revision, k, p, q, 2) == []


def test_cost_counts():
    rng = random.Random(7)
    for n in range(1, 6):
        for _ in range(100):
            k = random_set(rng, n, 0.1)
            p = random_set(rng, n, 0.1)
            _, d, visited, flips = dalal_revision_with_stats(k, p, n)
            assert visited <= 1 << n
            assert flips <= n * visited
            if d is not None:
                assert d <= n
    # Antipodal worlds: the layers cover the whole cube, d = n.
    _, d, visited, flips = dalal_revision_with_stats({0}, {31}, 5)
    assert (d, visited) == (5, 32)
    assert flips == 5 * (1 + 5 + 10 + 10 + 5)


# Faithful assignments of total preorders (Katsuno and Mendelzon 1991). A total
# preorder on worlds is given by a rank function: w <= v iff rank[w] <= rank[v].
def ranked_operator(rank_of):
    def op(k, p, n):
        k, p = frozenset(k), frozenset(p)
        if not p:
            return frozenset()
        rank = rank_of(k, n)
        best = min(rank[w] for w in p)
        return frozenset(w for w in p if rank[w] == best)

    return op


def faithful_random_ranks(seed):
    """A faithful assignment: rank 0 on Mod(K), a rank from 1 to 3 elsewhere.

    The ranks depend only on the set Mod(K), so equal bases get equal preorders.
    If Mod(K) is empty, the ranks are free.
    """

    def rank_of(k, n):
        key = sum(1 << w for w in k)
        rng = random.Random(seed * 1000003 + key * 7 + n)
        if not k:
            return {w: rng.randrange(3) for w in worlds(n)}
        return {w: 0 if w in k else 1 + rng.randrange(3) for w in worlds(n)}

    return rank_of


def dalal_ranks(k, n):
    if not k:
        return {w: 0 for w in worlds(n)}
    return {w: min(hamming(w, v) for v in k) for w in worlds(n)}


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_faithful_total_preorders_satisfy_r1_to_r6(seed):
    op = ranked_operator(faithful_random_ranks(seed))
    rng = random.Random(3000 + seed)
    for _ in range(300):
        n = rng.randrange(1, 5)
        k = random_set(rng, n, rng.choice([0.0, 0.2, 0.5]))
        p = random_set(rng, n, rng.choice([0.2, 0.5]))
        q = random_set(rng, n, rng.choice([0.3, 0.6]))
        assert km_violations(op, k, p, q, n) == []


def test_dalal_is_the_hamming_ranking():
    op = ranked_operator(dalal_ranks)
    rng = random.Random(4000)
    for _ in range(300):
        n = rng.randrange(1, 6)
        k = random_set(rng, n, 0.2)
        p = random_set(rng, n, 0.3)
        assert op(k, p, n) == dalal_revision(k, p, n)


def test_unfaithful_assignment_breaks_r2():
    # The world 3 (a and b) is outside Mod(K) = {1} but gets rank 0, the same rank as the model of K.
    def rank_of(k, n):
        return {w: 0 if w in k or w == 3 else 1 for w in worlds(n)}

    op = ranked_operator(rank_of)
    k, p, q = frozenset({1}), frozenset({1, 3}), frozenset(worlds(2))
    assert op(k, p, 2) == {1, 3}
    assert "R2" in km_violations(op, k, p, q, 2)


def satoh_revision(k, p, n):
    """Keep the models of p whose difference to some model of K is minimal under set inclusion."""
    k, p = frozenset(k), frozenset(p)
    if not k or not p:
        return p
    diffs = {u ^ v for u in p for v in k}
    minimal = {x for x in diffs if not any(y != x and y & x == y for y in diffs)}
    return frozenset(u for u in p if any(u ^ v in minimal for v in k))


def test_random_search_finds_r6_failures_of_satoh_only():
    # Satoh's operator compares differences by set inclusion, which is not a total preorder.
    rng = random.Random(5)
    failures = 0
    for _ in range(3000):
        k = random_set(rng, 3, 0.25)
        p = random_set(rng, 3, 0.5)
        q = random_set(rng, 3, 0.5)
        bad = km_violations(satoh_revision, k, p, q, 3)
        assert all(x == "R6" for x in bad)
        if bad:
            failures += 1
            assert km_violations(dalal_revision, k, p, q, 3) == []
    assert failures > 0


def test_satoh_r6_counterexample_of_the_page():
    # K = not a and not b and not c, p = (a and not b and not c) or (not a and b),
    # q = (a and not b and not c) or (not a and b and c).
    k = frozenset({0})
    p = frozenset({A, B, B | C})
    q = frozenset({A, B | C})
    assert satoh_revision(k, p, 3) == {A, B}
    assert satoh_revision(k, p & q, 3) == {A, B | C}
    assert km_violations(satoh_revision, k, p, q, 3) == ["R6"]
    assert dalal_revision(k, p, 3) == {A, B}
    assert dalal_revision(k, p & q, 3) == {A}
    assert km_violations(dalal_revision, k, p, q, 3) == []


def preorder_from_operator(op, k, n):
    """KM's construction: w <= v iff w is in Mod(K o form(w, v))."""
    return {(w, v) for w in worlds(n) for v in worlds(n) if w in op(k, {w, v}, n)}


@pytest.mark.parametrize("n", [1, 2, 3])
def test_km_construction_recovers_operator(n):
    rng = random.Random(6000 + n)
    bases = list(all_subsets(n)) if n <= 2 else [random_set(rng, n, 0.3) for _ in range(12)]
    preds = list(all_subsets(n)) if n <= 2 else [random_set(rng, n, 0.5) for _ in range(60)]
    for k in bases:
        le = preorder_from_operator(dalal_revision, k, n)
        ws = list(worlds(n))
        for w, v in itertools.product(ws, ws):
            assert (w, v) in le or (v, w) in le  # total
        for w, v, u in itertools.product(ws, ws, ws):
            if (w, v) in le and (v, u) in le:
                assert (w, u) in le  # transitive
        for w in k:
            for v in ws:
                if v not in k:
                    assert (w, v) in le and (v, w) not in le  # faithful, condition 2
            for v in k:
                assert (w, v) in le  # faithful, condition 1
        for p in preds:
            mins = frozenset(w for w in p if all((w, v) in le for v in p))
            assert mins == dalal_revision(k, p, n)
