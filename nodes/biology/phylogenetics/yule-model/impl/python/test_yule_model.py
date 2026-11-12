# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yule-model/. The authors are listed in prov/CV9KCF.jsonl.

import itertools
import math
import random
from collections import defaultdict
from fractions import Fraction

from yule_model import (
    cherries,
    clusters,
    grow,
    labeled_history_count,
    labeled_tree,
    number_of_rankings,
    ranked_shape,
    ranked_shape_probability,
    simulate,
    topology_probability,
)


def all_choice_sequences(n):
    """Every split sequence of the Yule process; each has probability 1/(n-1)!."""
    return itertools.product(*(range(k) for k in range(1, n)))


def exact_distributions(n):
    """Brute force: run the process along every split sequence and every
    labeling, with exact weights, and collect the induced distributions."""
    w = Fraction(1, math.factorial(n - 1) * math.factorial(n))
    topo, shapes, histories = defaultdict(Fraction), defaultdict(Fraction), defaultdict(Fraction)
    for choices in all_choice_sequences(n):
        children, rank, tips = grow(list(choices))
        shapes[ranked_shape(children, rank)] += w * math.factorial(n)
        for labels in itertools.permutations(range(n)):
            tree = labeled_tree(children, tips, list(labels))
            topo[clusters(tree)] += w
            name = dict(zip(tips, labels))
            hist = []
            for x, r in rank.items():
                below, stack = [], [x]
                while stack:
                    y = stack.pop()
                    if y in children:
                        stack.extend(children[y])
                    else:
                        below.append(name[y])
                hist.append((frozenset(below), r))
            histories[frozenset(hist)] += w
    return topo, shapes, histories


def tree_from_clusters(cl, labels):
    """Rebuild a nested-pair tree from its cluster set."""
    def build(s):
        if len(s) == 1:
            return next(iter(s))
        kids = [c for c in cl if c < s and not any(c < d < s for d in cl)]
        singles = [frozenset([x]) for x in s if not any(x in c for c in kids)]
        parts = kids + singles
        assert len(parts) == 2
        return (build(parts[0]), build(parts[1]))
    return build(frozenset(labels))


def double_factorial(m):
    return math.prod(range(m, 0, -2)) if m > 0 else 1


def test_topology_probabilities_by_enumeration() -> None:
    for n in (2, 3, 4, 5):
        topo, _, _ = exact_distributions(n)
        assert len(topo) == double_factorial(2 * n - 3)
        assert sum(topo.values()) == 1
        for cl, p in topo.items():
            tree = tree_from_clusters(cl, range(n))
            assert topology_probability(tree) == p


def test_four_taxa_values() -> None:
    assert topology_probability((((0, 1), 2), 3)) == Fraction(1, 18)
    assert topology_probability(((0, 1), (2, 3))) == Fraction(1, 9)
    assert number_of_rankings(((0, 1), (2, 3))) == 2
    assert number_of_rankings((((0, 1), 2), 3)) == 1


def test_ranked_shapes_and_histories() -> None:
    for n in (2, 3, 4, 5):
        _, shapes, histories = exact_distributions(n)
        assert sum(shapes.values()) == 1
        for shape, p in shapes.items():
            assert ranked_shape_probability(shape) == p
        assert len(histories) == labeled_history_count(n)
        assert set(histories.values()) == {Fraction(1, labeled_history_count(n))}


def test_rankings_times_history_probability() -> None:
    for n in (3, 4, 5):
        topo, _, _ = exact_distributions(n)
        for cl, p in topo.items():
            tree = tree_from_clusters(cl, range(n))
            assert p == Fraction(number_of_rankings(tree), labeled_history_count(n))


def test_expected_cherries_is_n_over_3() -> None:
    for n in range(3, 8):
        total = Fraction(0)
        for choices in all_choice_sequences(n):
            children, _, tips = grow(list(choices))
            total += cherries(labeled_tree(children, tips, list(range(n))))
        assert total / math.factorial(n - 1) == Fraction(n, 3)


def test_simulation_matches() -> None:
    rng = random.Random(11)
    n, rate, reps = 4, 2.0, 30000
    count_cat, total_time = 0, 0.0
    for _ in range(reps):
        tree, _, times = simulate(n, rate, rng)
        total_time += sum(times)
        sizes = sorted(len(c) for c in clusters(tree))
        count_cat += sizes == [2, 3, 4]
    p = 2 / 3
    assert abs(count_cat / reps - p) < 4 * math.sqrt(p * (1 - p) / reps)
    mean = sum(1 / (k * rate) for k in range(1, n))
    var = sum(1 / (k * rate) ** 2 for k in range(1, n))
    assert abs(total_time / reps - mean) < 4 * math.sqrt(var / reps)
