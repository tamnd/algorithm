# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pate/. The authors are listed in prov/7WDT5Q.jsonl.

import math
import random

import pytest

import dpkit
from pate import (
    basic_epsilon,
    noisy_max,
    noisy_max_pmf,
    pate,
    predict,
    split,
    train_centroids,
    vote_counts,
)

CLASS_0 = [(-1.0, 0.2), (-0.8, -0.1), (-1.2, 0.0), (-0.9, 0.3), (-1.1, -0.2),
           (-0.7, 0.1), (-1.3, 0.1), (-1.0, -0.3), (-0.6, 0.0), (-1.2, 0.2)]
CLASS_1 = [(1.0, 0.1), (0.9, -0.2), (1.1, 0.0), (0.8, 0.2), (1.2, -0.1),
           (0.7, 0.0), (1.3, 0.2), (1.0, -0.3), (0.6, 0.1), (1.1, 0.3)]
PRIVATE = [e for a, b in zip(CLASS_0, CLASS_1) for e in ((a, 0), (b, 1))]
PUBLIC = [(-0.5, 0.0), (0.02, 0.0), (0.9, 0.0)]


def test_check_values():
    teachers = [train_centroids(p, 2) for p in split(PRIVATE, 5)]
    assert [vote_counts(teachers, x, 2) for x in PUBLIC] == [[5, 0], [3, 2], [0, 5]]
    p = noisy_max_pmf([5, 0], 0.5)
    assert p[0] == pytest.approx(0.907654, abs=1e-6)
    assert noisy_max_pmf([3, 2], 0.5)[0] == pytest.approx(0.620918, abs=1e-6)
    student, labels = pate(PRIVATE, PUBLIC, 5, 2, 0.5, random.Random(2))
    assert labels == [0, 0, 1]
    assert student[0] == pytest.approx([-0.24, 0.0]) and student[1] == pytest.approx([0.9, 0.0])
    assert basic_epsilon(0.5, 3) == 3.0
    assert basic_epsilon(0.05, 100) == pytest.approx(10.0)


def test_bad_input():
    with pytest.raises(ValueError):
        pate(PRIVATE, PUBLIC, 0, 2, 0.5, random.Random(0))
    with pytest.raises(ValueError):
        pate([((0.0,), 3)], PUBLIC, 1, 2, 0.5, random.Random(0))


def random_data(n, d, classes, rng):
    return [(tuple(rng.uniform(-1, 1) for _ in range(d)), rng.randrange(classes)) for _ in range(n)]


def oracle_votes(data, k, x, classes):
    """Independent oracle: rebuild each teacher from the indices and rank (distance, class) pairs."""
    votes = [0] * classes
    for j in range(k):
        mine = [data[i] for i in range(j, len(data), k)]
        options = []
        for c in range(classes):
            pts = [p for p, y in mine if y == c]
            if pts:
                centre = [sum(col) / len(pts) for col in zip(*pts)]
                options.append((sum((a - b) ** 2 for a, b in zip(x, centre)), c))
        votes[min(options)[1] if options else 0] += 1
    return votes


def test_votes_against_oracle():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 20)
        d = rng.randint(1, 3)
        classes = rng.randint(2, 3)
        k = rng.randint(1, 5)
        data = random_data(n, d, classes, rng)
        x = tuple(rng.uniform(-1, 1) for _ in range(d))
        teachers = [train_centroids(p, classes) for p in split(data, k)]
        assert vote_counts(teachers, x, classes) == oracle_votes(data, k, x, classes)


def two_class_win(n0, n1, gamma):
    """Closed form: class 0 wins when L1 - L0 < n0 - n1, and L1 - L0 has P(> t) = e^(-gamma t)(1 + gamma t / 2) / 2."""
    t = n0 - n1
    if t >= 0:
        return 1 - 0.5 * math.exp(-gamma * t) * (1 + gamma * t / 2)
    return 0.5 * math.exp(gamma * t) * (1 - gamma * t / 2)


def test_pmf_against_closed_form():
    rng = random.Random(2)
    for _ in range(500):
        n0, n1 = rng.randint(0, 8), rng.randint(0, 8)
        gamma = rng.uniform(0.05, 2.0)
        p = noisy_max_pmf([n0, n1], gamma)
        assert p[0] == pytest.approx(two_class_win(n0, n1, gamma), abs=1e-6)
        assert p[0] + p[1] == pytest.approx(1.0, abs=1e-6)


def test_sampler_against_pmf():
    rng = random.Random(3)
    m = 2000
    margin = dpkit.hoeffding_margin(m, 1e-6)
    for counts, gamma in (([4, 3, 1], 0.5), ([2, 2, 4], 1.0)):
        p = noisy_max_pmf(counts, gamma)
        assert sum(p) == pytest.approx(1.0, abs=1e-6)
        emp = dpkit.empirical_pmf(noisy_max(counts, gamma, rng) for _ in range(m))
        for c in range(3):
            assert abs(emp.get(c, 0.0) - p[c]) <= margin


def test_one_moved_vote_costs_at_most_two_gamma():
    rng = random.Random(4)
    worst = 0.0
    for _ in range(40):
        k = rng.randint(1, 6)
        gamma = rng.uniform(0.1, 1.0)
        counts = [0, 0, 0]
        for _ in range(k):
            counts[rng.randrange(3)] += 1
        a = rng.choice([c for c in range(3) if counts[c] > 0])
        b = rng.choice([c for c in range(3) if c != a])
        moved = list(counts)
        moved[a] -= 1
        moved[b] += 1
        p = dict(enumerate(noisy_max_pmf(counts, gamma)))
        q = dict(enumerate(noisy_max_pmf(moved, gamma)))
        loss = max(dpkit.max_privacy_loss(p, q), dpkit.max_privacy_loss(q, p))
        assert loss <= 2 * gamma + 1e-5
        worst = max(worst, loss / (2 * gamma))
    assert worst > 0.5
    # With two classes and a large lead the bound 2 gamma is nearly reached.
    p = two_class_win(0, 30, 0.5)
    q = two_class_win(1, 29, 0.5)
    assert 0.9 * 2 * 0.5 < math.log(q / p) <= 2 * 0.5


def test_replacing_one_example_changes_one_teacher():
    rng = random.Random(5)
    for _ in range(200):
        n = rng.randint(1, 20)
        k = rng.randint(1, 5)
        data = random_data(n, 2, 3, rng)
        other = list(data)
        i = rng.randrange(n)
        other[i] = (tuple(rng.uniform(-1, 1) for _ in range(2)), rng.randrange(3))
        t1 = [train_centroids(p, 3) for p in split(data, k)]
        t2 = [train_centroids(p, 3) for p in split(other, k)]
        assert all(t1[j] == t2[j] for j in range(k) if j != i % k)
        x = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        v1, v2 = vote_counts(t1, x, 3), vote_counts(t2, x, 3)
        assert sum(abs(a - b) for a, b in zip(v1, v2)) <= 2


def test_predict_tie_and_empty():
    assert predict([None, None], (0.0,)) == 0
    assert predict([[1.0], [-1.0]], (0.0,)) == 0
    assert predict([None, [0.5]], (0.0,)) == 1
