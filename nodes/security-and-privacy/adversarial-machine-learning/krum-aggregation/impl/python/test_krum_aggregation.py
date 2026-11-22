# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/krum-aggregation/. The authors are listed in prov/NQC1A8.jsonl.

"""Tests of Krum on updates built from fixed seeds: brute force over subsets, the distance bound, and a small training run."""

import itertools
import math
import random

import mlkit as m
from krum_aggregation import (
    average,
    check_sizes,
    krum,
    krum_index,
    krum_scores,
    multi_krum,
    multi_krum_indices,
    squared_distance,
)


def brute_scores(updates: list[list[float]], f: int) -> list[float]:
    """s(i) from the definition: the minimum, over all sets S of n - f - 2 other updates, of the sum over S."""
    n = len(updates)
    k = n - f - 2
    out = []
    for i in range(n):
        dist = {j: squared_distance(updates[i], updates[j]) for j in range(n) if j != i}
        out.append(min(math.fsum(dist[j] for j in s) for s in itertools.combinations(sorted(dist), k)))
    return out


def brute_index(updates: list[list[float]], f: int) -> int:
    s = brute_scores(updates, f)
    return min(range(len(s)), key=lambda i: (s[i], i))


def random_instance(rng: random.Random) -> tuple[list[list[float]], int]:
    f = rng.randint(0, 2)
    n = rng.randint(2 * f + 3, 8)
    d = rng.randint(1, 4)
    if rng.random() < 0.5:
        # small integers, so that equal scores (ties) are common
        updates = [[float(rng.randint(-2, 2)) for _ in range(d)] for _ in range(n)]
    else:
        updates = [[rng.gauss(0.0, 1.0) * rng.choice([1.0, 10.0]) for _ in range(d)] for _ in range(n)]
    return updates, f


def test_example_of_the_page() -> None:
    v = [[0.0], [1.0], [2.0], [4.0], [10.0]]
    assert krum_scores(v, 1) == [5.0, 2.0, 5.0, 13.0, 100.0]
    assert krum_index(v, 1) == 1
    assert krum(v, 1) == [1.0]
    assert average(v) == [3.4]


def test_matches_brute_force_over_subsets() -> None:
    rng = random.Random(3101)
    for _ in range(600):
        updates, f = random_instance(rng)
        assert krum_scores(updates, f) == brute_scores(updates, f)
        assert krum_index(updates, f) == brute_index(updates, f)


def test_ties_go_to_the_smallest_index() -> None:
    v = [[1.0], [0.0], [2.0], [1.0], [1.0]]
    # V_0, V_3 and V_4 all have score 0 with f = 1; the first one wins
    assert krum_index(v, 1) == 0
    assert krum_index([[0.0]] * 5, 1) == 0


def test_rejects_too_few_updates() -> None:
    for f in range(0, 4):
        for n in range(1, 2 * f + 3):
            try:
                krum_index([[0.0]] * n, f)
            except ValueError:
                pass
            else:
                raise AssertionError((n, f))
            try:
                check_sizes(n, f)
            except ValueError:
                pass
            else:
                raise AssertionError((n, f))
        krum_index([[0.0]] * (2 * f + 3), f)


def test_multi_krum_matches_repeated_brute_force() -> None:
    rng = random.Random(3102)
    for _ in range(300):
        updates, f = random_instance(rng)
        n = len(updates)
        mm = rng.randint(1, n - 2 * f - 2)
        left = list(range(n))
        expect = []
        for _ in range(mm):
            k = brute_index([updates[i] for i in left], f)
            expect.append(left.pop(k))
        assert multi_krum_indices(updates, f, mm) == expect
        mean = multi_krum(updates, f, mm)
        for j in range(len(updates[0])):
            assert abs(mean[j] - sum(updates[i][j] for i in expect) / mm) < 1e-9
        assert multi_krum_indices(updates, f, 1) == [krum_index(updates, f)]


def byzantine_updates(rng: random.Random, honest: list[list[float]], b: int, d: int) -> list[list[float]]:
    """Abstract Byzantine strategies on synthetic vectors, chosen at random."""
    kind = rng.randrange(4)
    center = average(honest)
    if kind == 0:  # far away
        return [[rng.gauss(0.0, 100.0) for _ in range(d)] for _ in range(b)]
    if kind == 1:  # the collusion of Figure 3: b - 1 far points, one at the barycenter of all
        far = [[100.0 + rng.random() for _ in range(d)] for _ in range(b - 1)]
        bary = average(honest + far) if far else center
        return far + [bary]
    if kind == 2:  # close to the honest mean, shifted by a random multiple of the honest spread
        spread = max(math.sqrt(squared_distance(h, center)) for h in honest)
        direction = [rng.gauss(0.0, 1.0) for _ in range(d)]
        r = m.norm2(direction) or 1.0
        c = rng.uniform(0.0, 3.0) * spread / r
        return [m.add(center, m.scale(c, direction)) for _ in range(b)]
    # copies of one honest update with a small shift
    base = rng.choice(honest)
    return [[a + rng.gauss(0.0, 0.5) for a in base] for _ in range(b)]


def test_choice_is_close_to_some_honest_update() -> None:
    """The theorem of the page: min_j ||V* - V_j||^2 <= (n - f - 2) / (n - 2 f - 1) rho^2."""
    rng = random.Random(3103)
    for _ in range(600):
        f = rng.randint(1, 2)
        n = rng.randint(2 * f + 3, 9)
        d = rng.randint(1, 4)
        b = rng.randint(0, f)
        honest = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n - b)]
        updates = honest + byzantine_updates(rng, honest, b, d)
        rng.shuffle(updates)
        chosen = krum(updates, f)
        rho2 = min(max(squared_distance(h, g) for g in honest) for h in honest)
        delta2 = min(squared_distance(chosen, h) for h in honest)
        assert delta2 <= (n - f - 2) / (n - 2 * f - 1) * rho2 * (1 + 1e-12) + 1e-12


def test_one_byzantine_update_moves_the_average_anywhere() -> None:
    """Lemma 1 of Blanchard et al.: a linear rule is moved to any target U by one update."""
    rng = random.Random(3104)
    for _ in range(100):
        n, d = rng.randint(4, 8), rng.randint(1, 4)
        honest = [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(n - 1)]
        target = [rng.uniform(-50, 50) for _ in range(d)]
        bad = [n * target[j] - math.fsum(h[j] for h in honest) for j in range(d)]
        got = average(honest + [bad])
        assert all(abs(a - t) < 1e-9 for a, t in zip(got, target))


def test_training_run_with_two_byzantine_clients() -> None:
    """Seeded logistic regression with 9 clients, 2 of them Byzantine, on synthetic blobs."""
    rng = random.Random(3105)
    n, f, d = 9, 2, 2
    centers = [[-1.0, -1.0], [1.0, 1.0]]
    clients = [m.make_blobs(rng, 10, d, centers, 0.7) for _ in range(n - f)]
    test = m.make_blobs(rng, 200, d, centers, 0.7)

    def honest_update(w: list[float], b: float, data: m.Data) -> list[float]:
        gw, gb = [0.0] * d, 0.0
        for x, y in data:
            g, g0 = m.grad_w_logistic(w, b, x, y)
            gw = m.add(gw, g)
            gb += g0
        return [a / len(data) for a in gw] + [gb / len(data)]

    def run(rule) -> float:
        w, b = [0.0] * d, 0.0
        for _ in range(40):
            ups = [honest_update(w, b, c) for c in clients]
            mean = average(ups)
            ups += [m.scale(-10.0, mean) for _ in range(f)]
            step = rule(ups)
            w = [w[j] - 0.5 * step[j] for j in range(d)]
            b -= 0.5 * step[d]
        return m.accuracy(lambda x: 1 if m.dot(w, x) + b > 0 else 0, test)

    assert run(lambda u: krum(u, f)) >= 0.9
    assert run(lambda u: multi_krum(u, f, 3)) >= 0.9
    assert run(average) <= 0.5
