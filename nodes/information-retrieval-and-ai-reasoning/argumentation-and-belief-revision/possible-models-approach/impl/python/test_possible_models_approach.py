# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/possible-models-approach/. The authors are listed in prov/J9PKJ2.jsonl.

import random

import pytest

from possible_models_approach import closest_models, pma_update, pma_update_per_model


def worlds(n):
    return range(1 << n)


def random_set(rng, n, prob):
    return frozenset(w for w in worlds(n) if rng.random() < prob)


def all_subsets(n):
    ws = list(worlds(n))
    for mask in range(1 << len(ws)):
        yield frozenset(w for j, w in enumerate(ws) if mask >> j & 1)


def subset_of(x, y):
    return x & y == x


def brute_force(k, p, n):
    """Union over the models w of k of the models of p whose change set from w is inclusion-minimal."""
    out = set()
    for w in k:
        for v in p:
            x = w ^ v
            if not any(subset_of(w ^ u, x) and w ^ u != x for u in p):
                out.add(v)
    return frozenset(out)


def dalal(k, p, n):
    """Dalal's revision by brute force: the models of p at least Hamming distance from the set k."""
    k, p = frozenset(k), frozenset(p)
    if not p:
        return frozenset()
    if not k:
        return p
    dist = {v: min(bin(v ^ w).count("1") for w in k) for v in p}
    best = min(dist.values())
    return frozenset(v for v in p if dist[v] == best)


def forbus(k, p, n):
    """Forbus's update by brute force: for each model of k, the models of p at least Hamming distance from it."""
    out = set()
    for w in k:
        dist = {v: bin(v ^ w).count("1") for v in p}
        if dist:
            best = min(dist.values())
            out |= {v for v in p if dist[v] == best}
    return frozenset(out)


# The KM update postulates U1 to U8, with formulas given by their sets of models.
def update_violations(op, k, k2, p, p2, q, n):
    bad = []
    r = op(k, p, n)
    if not r <= p:
        bad.append("U1")
    if k <= p and r != k:
        bad.append("U2")
    if k and p and not r:
        bad.append("U3")
    if op(sorted(k, reverse=True), sorted(p, reverse=True), n) != r:
        bad.append("U4")
    if not (r & q) <= op(k, p & q, n):
        bad.append("U5")
    r2 = op(k, p2, n)
    if r <= p2 and r2 <= p and r != r2:
        bad.append("U6")
    if len(k) == 1 and not (r & r2) <= op(k, p | p2, n):
        bad.append("U7")
    if op(k | k2, p, n) != r | op(k2, p, n):
        bad.append("U8")
    return bad


# The KM revision postulates R1 to R6, used to show that the PMA is not a revision.
def revision_violations(op, k, p, q, n):
    bad = []
    r = op(k, p, n)
    if not r <= p:
        bad.append("R1")
    if k & p and r != k & p:
        bad.append("R2")
    if p and not r:
        bad.append("R3")
    if op(sorted(k, reverse=True), sorted(p, reverse=True), n) != r:
        bad.append("R4")
    rpq = op(k, p & q, n)
    if not (r & q) <= rpq:
        bad.append("R5")
    if r & q and not rpq <= r & q:
        bad.append("R6")
    return bad


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5])
def test_matches_brute_force(n):
    rng = random.Random(100 + n)
    for _ in range(300):
        k = random_set(rng, n, rng.choice([0.0, 0.1, 0.3, 0.6]))
        p = random_set(rng, n, rng.choice([0.0, 0.1, 0.3, 0.6]))
        assert pma_update(k, p, n) == brute_force(k, p, n)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_model_by_model(n):
    # For each single model w, the closest models are the inclusion-minimal change sets.
    rng = random.Random(200 + n)
    for _ in range(200):
        k = random_set(rng, n, 0.3)
        p = random_set(rng, n, rng.choice([0.1, 0.3, 0.6]))
        per = pma_update_per_model(k, p, n)
        assert set(per) == set(k)
        for w in k:
            assert per[w] == brute_force({w}, p, n)
            assert closest_models(w, p, n) == per[w]
        union = frozenset().union(*per.values()) if per else frozenset()
        assert union == pma_update(k, p, n)


def test_exhaustive_two_atoms():
    for k in all_subsets(2):
        for p in all_subsets(2):
            assert pma_update(k, p, 2) == brute_force(k, p, 2)


@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_update_postulates_u1_to_u8(n):
    rng = random.Random(300 + n)
    for _ in range(250):
        k = random_set(rng, n, rng.choice([0.0, 0.1, 0.3, 0.6]))
        if rng.random() < 0.3:
            k = frozenset([rng.randrange(1 << n)])  # complete bases for U7
        k2 = random_set(rng, n, rng.choice([0.1, 0.3]))
        p = random_set(rng, n, rng.choice([0.1, 0.3, 0.6]))
        p2 = random_set(rng, n, rng.choice([0.1, 0.3, 0.6]))
        if rng.random() < 0.2:
            p2 = p | random_set(rng, n, 0.2)
        q = random_set(rng, n, rng.choice([0.2, 0.5, 0.8]))
        assert update_violations(pma_update, k, k2, p, p2, q, n) == []


def test_update_postulates_exhaustive_two_atoms():
    subsets = list(all_subsets(2))
    rng = random.Random(400)
    for k in subsets:
        for p in subsets:
            for p2 in subsets:
                k2 = rng.choice(subsets)
                q = rng.choice(subsets)
                assert update_violations(pma_update, k, k2, p, p2, q, 2) == []


# Atoms: b (the book is on the table) is bit 0, m (the magazine is on the table) is bit 1.
B, M = 1, 2


def test_book_and_magazine_update_differs_from_revision():
    # K: exactly one of the book and the magazine is on the table. p: the book is on the table.
    k = frozenset({B, M})
    p = frozenset({B, B | M})
    assert pma_update(k, p, 2) == {B, B | M}  # update: b, and nothing is known about m
    assert dalal(k, p, 2) == {B}  # revision: b and not m
    assert pma_update_per_model(k, p, 2) == {B: {B}, M: {B | M}}
    # The update breaks R2: K and p are consistent, but the result is not K and p.
    assert "R2" in revision_violations(pma_update, k, p, frozenset(worlds(2)), 2)
    # The revision breaks U8: the models of K are not updated one by one.
    assert "U8" in update_violations(dalal, k, frozenset({M}), p, p, p, 2)
    assert dalal({B}, p, 2) | dalal({M}, p, 2) == {B, B | M}


# Atoms a, b, c are bits 0, 1, 2. The example of the page.
A, Bb, C = 1, 2, 4


def test_page_example():
    k = frozenset({0, Bb | C})  # not a, and b if and only if c
    p = frozenset({A, Bb | C})  # (a and not b and not c) or (not a and b and c)
    assert pma_update_per_model(k, p, 3) == {0: {A, Bb | C}, Bb | C: {Bb | C}}
    assert pma_update(k, p, 3) == {A, Bb | C}
    # Forbus counts the changed atoms and drops the world two atoms away from 000.
    assert forbus(k, p, 3) == {A, Bb | C}
    assert forbus({0}, p, 3) == {A}
    assert pma_update({0}, p, 3) == {A, Bb | C}
    # Dalal's revision keeps only the common model.
    assert dalal(k, p, 3) == {Bb | C}


def test_dalal_breaks_update_postulates_and_pma_breaks_r2():
    rng = random.Random(500)
    dalal_bad = pma_bad = 0
    for _ in range(2000):
        n = 3
        k = random_set(rng, n, 0.3)
        k2 = random_set(rng, n, 0.3)
        p = random_set(rng, n, 0.4)
        p2 = random_set(rng, n, 0.4)
        q = random_set(rng, n, 0.5)
        if update_violations(dalal, k, k2, p, p2, q, n):
            dalal_bad += 1
        bad = revision_violations(pma_update, k, p, q, n)
        assert "R1" not in bad and "R4" not in bad and "R5" not in bad
        # R3 fails only for an inconsistent base, which an update keeps inconsistent.
        assert "R3" not in bad or not k
        if "R2" in bad:
            pma_bad += 1
    assert dalal_bad > 0 and pma_bad > 0


def test_inconsistent_inputs():
    # An inconsistent base stays inconsistent, and an inconsistent formula gives no model.
    assert pma_update(set(), {1, 2}, 2) == set()
    assert pma_update({1}, set(), 2) == set()
    assert pma_update({0}, {0}, 0) == {0}


def test_bad_world_rejected():
    with pytest.raises(ValueError):
        pma_update({4}, {1}, 2)
    with pytest.raises(ValueError):
        pma_update({1}, {-1}, 2)
    with pytest.raises(ValueError):
        pma_update({1}, {1}, -1)
