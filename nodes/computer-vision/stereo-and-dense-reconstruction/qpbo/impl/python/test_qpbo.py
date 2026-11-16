# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/qpbo/. The authors are listed in prov/W42VES.jsonl.

import itertools
import random

from qpbo import doubled_energy, energy, qpbo


def all_minimizers(unary, terms):
    n = len(unary)
    vals = {x: energy(unary, terms, x) for x in itertools.product((0, 1), repeat=n)}
    best = min(vals.values())
    return best, [x for x, e in vals.items() if e == best]


def random_energy(rng, n, submodular_only=False):
    unary = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(n)]
    terms = []
    for (p, q) in itertools.combinations(range(n), 2):
        if rng.random() < 0.5:
            A, B, C, D = (rng.randint(-5, 5) for _ in range(4))
            if submodular_only and A + D > B + C:
                A, B = B, A  # swap a pair of values to fix the sign
                if A + D > B + C:
                    D = B + C - A
            terms.append((p, q, A, B, C, D))
    return unary, terms


def test_doubled_energy_on_the_diagonal():
    rng = random.Random(1)
    for _ in range(50):
        n = rng.randint(1, 6)
        unary, terms = random_energy(rng, n)
        for x in itertools.product((0, 1), repeat=n):
            xbar = [1 - v for v in x]
            assert doubled_energy(unary, terms, x, xbar) == 2 * energy(unary, terms, x)


def test_persistency_and_bound():
    rng = random.Random(2)
    labeled_total = 0
    for _ in range(300):
        n = rng.randint(1, 9)
        unary, terms = random_energy(rng, n)
        labels, bound = qpbo(unary, terms)
        best, mins = all_minimizers(unary, terms)
        assert bound <= best
        labeled_total += sum(v is not None for v in labels)
        # Every minimizer stays a minimizer when the labeled values are imposed.
        for z in mins:
            z2 = tuple(labels[p] if labels[p] is not None else z[p] for p in range(n))
            assert energy(unary, terms, z2) == best
    assert labeled_total > 0


def test_doubled_minimum_is_found():
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(1, 5)
        unary, terms = random_energy(rng, n)
        labels, bound = qpbo(unary, terms)
        brute = min(doubled_energy(unary, terms, x, xb)
                    for x in itertools.product((0, 1), repeat=n)
                    for xb in itertools.product((0, 1), repeat=n))
        assert 2 * bound == brute


def test_submodular_with_unique_minimum_is_fully_labeled():
    rng = random.Random(4)
    checked = 0
    for _ in range(300):
        n = rng.randint(1, 8)
        unary, terms = random_energy(rng, n, submodular_only=True)
        best, mins = all_minimizers(unary, terms)
        labels, bound = qpbo(unary, terms)
        assert bound == best
        if len(mins) == 1:
            checked += 1
            assert tuple(labels) == mins[0]
    assert checked > 50


def test_frustrated_triangle():
    # Each pair pays 1 when the two values agree; at least one pair agrees.
    terms = [(p, q, 1, 0, 0, 1) for (p, q) in ((0, 1), (1, 2), (0, 2))]
    unary = [(0, 0)] * 3
    labels, bound = qpbo(unary, terms)
    assert labels == [None, None, None]
    assert bound == 0
    assert all_minimizers(unary, terms)[0] == 1


def test_worked_example():
    # A path of three variables: one nonsubmodular pair and a strong unary.
    unary = [(0, 4), (0, 0), (0, 0)]
    terms = [(0, 1, 2, 0, 0, 2), (1, 2, 0, 3, 3, 0)]
    labels, bound = qpbo(unary, terms)
    assert labels == [0, 1, 1]
    assert bound == 0 and energy(unary, terms, (0, 1, 1)) == 0


def test_partial_example():
    # The frustrated triangle with a fourth variable tied to variable 0.
    terms = [(p, q, 1, 0, 0, 1) for (p, q) in ((0, 1), (1, 2), (0, 2))]
    terms.append((0, 3, 0, 1, 1, 0))
    unary = [(0, 0)] * 3 + [(0, 3)]
    labels, bound = qpbo(unary, terms)
    assert labels == [None, None, None, 0]
    assert bound == 0.5
    best, mins = all_minimizers(unary, terms)
    assert best == 1 and all(z[3] == 0 for z in mins)
