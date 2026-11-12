# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-experience-replay/. The authors are listed in prov/T8RE4E.jsonl.

import bisect
import random
from fractions import Fraction as F

import pytest

from prioritized_experience_replay import PrioritizedReplay, SumTree, rank_based_probabilities


def brute_find(values, u):
    prefix, acc = [], 0
    for v in values:
        acc += v
        prefix.append(acc)
    return bisect.bisect_right(prefix, u)


def test_page_example_tree():
    t = SumTree(5)
    for i, v in enumerate([3, 1, 4, 1, 5]):
        t.update(i, v)
    assert t.size == 8
    assert t.total() == 14
    assert t.tree[1:8] == [14, 9, 5, 4, 5, 5, 0]
    assert [t.find(u) for u in (0, 2.9, 3, 4, 7.99, 8, 8.5, 9, 13.99)] == [0, 0, 1, 2, 2, 3, 3, 4, 4]


def test_grid_inversion_gives_exact_frequencies():
    # alpha = 1/2 and priorities that are squares of rationals, so p^alpha is exact.
    alpha_roots = [F(1, 2), F(0), F(3, 2), F(1), F(1), F(2)]
    priorities = [r * r for r in alpha_roots]
    t = SumTree(len(priorities))
    for i, p in enumerate(priorities):
        root = alpha_roots[i]
        assert root * root == p
        t.update(i, root)  # the leaf holds p_i^alpha
    total = t.total()
    assert total == 6
    m = 600
    counts = [0] * len(priorities)
    for j in range(m):
        u = (j + F(1, 2)) * total / m
        counts[t.find(u)] += 1
    for i, root in enumerate(alpha_roots):
        assert counts[i] == root / total * m  # exactly m P(i)


def test_updates_against_brute_force_prefix_sums():
    rng = random.Random(3)
    for _ in range(60):
        n = rng.randint(1, 13)
        t = SumTree(n)
        values = [0] * n
        for _ in range(40):
            i = rng.randrange(n)
            v = rng.randint(0, 6)
            t.update(i, v)
            values[i] = v
            assert t.total() == sum(values)
            for u in range(t.total()):
                assert t.find(u) == brute_find(values, u)
            for u in range(2 * t.total()):
                assert t.find(F(u, 2)) == brute_find(values, F(u, 2))


def test_internal_nodes_are_sums():
    t = SumTree(6)
    rng = random.Random(8)
    for _ in range(100):
        t.update(rng.randrange(6), F(rng.randint(0, 9), rng.randint(1, 4)))
        for j in range(1, t.size):
            assert t.tree[j] == t.tree[2 * j] + t.tree[2 * j + 1]


def test_bad_arguments():
    with pytest.raises(ValueError):
        SumTree(0)
    with pytest.raises(IndexError):
        SumTree(3).update(3, 1)
    with pytest.raises(ValueError):
        PrioritizedReplay(4, 0.6).sample(2, 0.4, random.Random(0))


def test_probabilities_and_weights():
    buf = PrioritizedReplay(4, alpha=0.6, eps=0.01)
    for t in range(4):
        buf.add(t)
    deltas = [2.0, -0.5, 0.0, 1.0]
    buf.update_priorities([0, 1, 2, 3], deltas)
    p = [abs(d) + 0.01 for d in deltas]
    z = sum(x ** 0.6 for x in p)
    for i in range(4):
        assert abs(buf.probability(i) - p[i] ** 0.6 / z) < 1e-12
    idx, items, w = buf.sample(8, beta=0.4, rng=random.Random(1))
    assert items == idx
    raw = [(4 * p[i] ** 0.6 / z) ** -0.4 for i in idx]
    for a, b in zip(w, raw):
        assert abs(a - b / max(raw)) < 1e-12
    assert max(w) == 1.0


def test_stratified_sampling_hits_each_segment():
    buf = PrioritizedReplay(8, alpha=1.0)
    for t in range(8):
        buf.add(t)
    buf.update_priorities(list(range(8)), [float(k) for k in range(8)])
    total = buf.tree.total()
    idx, _, _ = buf.sample(4, 0.5, random.Random(4))
    for j, i in enumerate(idx):
        lo = sum(buf.tree.leaf(k) for k in range(i))
        hi = lo + buf.tree.leaf(i)
        # the leaf interval meets segment j
        assert lo < (j + 1) * total / 4 and hi > j * total / 4


def test_sampling_frequencies_match_p_alpha():
    buf = PrioritizedReplay(5, alpha=0.5)
    for t in range(5):
        buf.add(t)
    buf.update_priorities(list(range(5)), [0.0, 1.0, 4.0, 9.0, 16.0])
    rng = random.Random(77)
    counts = [0] * 5
    draws = 0
    for _ in range(4000):
        idx, _, _ = buf.sample(5, 1.0, rng)
        for i in idx:
            counts[i] += 1
        draws += 5
    for i in range(5):
        expected = buf.probability(i) * draws
        assert abs(counts[i] - expected) < 0.03 * draws


def test_new_transitions_get_max_priority():
    buf = PrioritizedReplay(3, alpha=1.0, eps=0.0)
    buf.add("a")
    buf.update_priorities([0], [5.0])
    buf.add("b")
    assert buf.tree.leaf(1) == 5.0
    buf.add("c")
    buf.add("d")  # overwrites slot 0
    assert buf.data == ["d", "b", "c"]
    assert buf.tree.leaf(0) == 5.0


def test_rank_based():
    p = rank_based_probabilities([0.1, -3.0, 2.0], alpha=1.0)
    z = 1 + 1 / 2 + 1 / 3
    assert abs(p[1] - 1 / z) < 1e-12
    assert abs(p[2] - (1 / 2) / z) < 1e-12
    assert abs(p[0] - (1 / 3) / z) < 1e-12
