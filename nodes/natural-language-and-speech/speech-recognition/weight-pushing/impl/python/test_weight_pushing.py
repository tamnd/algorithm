# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weight-pushing/. The authors are listed in prov/GPP9K3.jsonl.

import itertools
import math
import random

import pytest

from nlslog import LOG_COST, TROPICAL, Semiring, log_sum
from weight_pushing import Machine, push, shortest_distance_to_final, string_weight

LABELS = ["a", "b"]


def all_strings(max_len: int):
    for k in range(max_len + 1):
        yield from itertools.product(LABELS, repeat=k)


def close(u: float, v: float, tol: float = 1e-9) -> bool:
    if math.isinf(u) or math.isinf(v):
        return u == v
    return abs(u - v) <= tol


def random_tropical(rng: random.Random, n: int, m: int) -> Machine:
    t = Machine()
    for _ in range(n):
        t.add_state()
    for _ in range(m):
        c = rng.choice(LABELS)
        t.add_arc(rng.randrange(n), c, c, rng.randint(0, 8) * 0.5, rng.randrange(n))
    for q in rng.sample(range(n), rng.randint(1, n)):
        t.set_final(q, rng.randint(0, 4) * 0.5)
    t.initial = rng.randint(0, 2) * 0.5
    return t


def random_probabilistic(rng: random.Random, n: int, k: int) -> Machine:
    """Each state gives total probability 0.9 to its k arcs and its final weight, so all sums converge."""
    t = Machine()
    for _ in range(n):
        t.add_state()
    for q in range(n):
        parts = [rng.random() + 0.05 for _ in range(k + 1)]
        s = sum(parts)
        for j in range(k):
            c = rng.choice(LABELS)
            t.add_arc(q, c, c, -math.log(0.9 * parts[j] / s), rng.randrange(n))
        if rng.random() < 0.6 or q == n - 1:
            t.set_final(q, -math.log(0.9 * parts[k] / s))
    return t


def bellman_ford_to_final(t: Machine) -> list:
    n = t.num_states()
    d = [math.inf] * n
    for q, rho in t.final.items():
        d[q] = min(d[q], rho)
    for _ in range(n):
        for p in range(n):
            for _, _, w, q in t.arcs[p]:
                d[p] = min(d[p], w + d[q])
    return d


def linear_solve_to_final(t: Machine) -> list:
    """Solve x = P x + f in probabilities by Gaussian elimination, and return the costs -log x."""
    n = t.num_states()
    a = [[0.0] * (n + 1) for _ in range(n)]
    for p in range(n):
        a[p][p] += 1.0
        for _, _, w, q in t.arcs[p]:
            a[p][q] -= math.exp(-w)
        a[p][n] = math.exp(-t.final[p]) if p in t.final else 0.0
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(a[r][col]))
        a[col], a[piv] = a[piv], a[col]
        for r in range(n):
            if r != col and a[r][col] != 0.0:
                f = a[r][col] / a[col][col]
                a[r] = [x - f * y for x, y in zip(a[r], a[col])]
    return [-math.log(a[i][n] / a[i][i]) if a[i][n] / a[i][i] > 0 else math.inf for i in range(n)]


def out_sum(t: Machine, q: int, sr: Semiring) -> float:
    total = t.final.get(q, sr.zero)
    for _, _, w, _ in t.arcs[q]:
        total = sr.plus(total, w)
    return total


def test_page_example():
    t = Machine()
    for _ in range(4):
        t.add_state()
    t.add_arc(0, "a", "a", 0.0, 1)
    t.add_arc(0, "b", "b", 1.0, 2)
    t.add_arc(1, "c", "c", 3.0, 3)
    t.add_arc(2, "c", "c", 1.0, 3)
    t.add_arc(2, "d", "d", 4.0, 3)
    t.set_final(3, 0.0)
    assert shortest_distance_to_final(t, TROPICAL) == [2.0, 3.0, 1.0, 0.0]
    p = push(t, TROPICAL)
    assert p.initial == 2.0
    assert p.arcs == [[("a", "a", 1.0, 1), ("b", "b", 0.0, 2)], [("c", "c", 0.0, 3)], [("c", "c", 0.0, 3), ("d", "d", 3.0, 3)], []]
    d = shortest_distance_to_final(t, LOG_COST)
    assert close(d[2], -math.log(math.exp(-1) + math.exp(-4)))
    p = push(t, LOG_COST)
    for q in range(3):
        assert close(out_sum(p, q, LOG_COST), 0.0)
    assert close(math.exp(-p.arcs[0][0][2]), math.exp(-3) / (math.exp(-3) + math.exp(-2) + math.exp(-5)))


def test_tropical_distances_and_push():
    rng = random.Random(4)
    for _ in range(60):
        t = random_tropical(rng, rng.randint(1, 5), rng.randint(1, 9))
        d = shortest_distance_to_final(t, TROPICAL)
        assert d == bellman_ford_to_final(t)
        if math.isinf(d[t.start]):
            with pytest.raises(ValueError):
                push(t, TROPICAL)
            continue
        p = push(t, TROPICAL)
        assert p.initial == t.initial + d[t.start]
        for q in range(p.num_states()):
            assert close(out_sum(p, q, TROPICAL), 0.0)
            assert all(w >= -1e-12 for _, _, w, _ in p.arcs[q])
        for x in all_strings(4):
            assert close(string_weight(t, x, TROPICAL), string_weight(p, x, TROPICAL))


def test_log_distances_and_stochastic():
    rng = random.Random(5)
    for _ in range(40):
        t = random_probabilistic(rng, rng.randint(1, 5), rng.randint(1, 3))
        d = shortest_distance_to_final(t, LOG_COST)
        ref = linear_solve_to_final(t)
        assert all(close(u, v, 1e-8) for u, v in zip(d, ref))
        if math.isinf(d[t.start]):
            with pytest.raises(ValueError):
                push(t, LOG_COST)
            continue
        p = push(t, LOG_COST)
        for q in range(p.num_states()):
            probs = [math.exp(-w) for _, _, w, _ in p.arcs[q]]
            if q in p.final:
                probs.append(math.exp(-p.final[q]))
            assert abs(sum(probs) - 1.0) < 1e-8
        for x in all_strings(4):
            assert close(string_weight(t, x, LOG_COST), string_weight(p, x, LOG_COST), 1e-8)


def test_pushing_makes_equivalent_machines_equal():
    def chain(w1: float, w2: float, w3: float) -> Machine:
        t = Machine()
        for _ in range(3):
            t.add_state()
        t.add_arc(0, "a", "a", w1, 1)
        t.add_arc(1, "b", "b", w2, 2)
        t.add_arc(1, "c", "c", w3, 2)
        t.set_final(2, 0.0)
        return t

    one = push(chain(1.0, 2.0, 5.0), TROPICAL)
    two = push(chain(3.0, 0.0, 3.0), TROPICAL)
    assert one.arcs == two.arcs and one.initial == two.initial and one.final == two.final


def test_dead_states_are_removed():
    t = Machine()
    for _ in range(3):
        t.add_state()
    t.add_arc(0, "a", "a", 1.0, 1)
    t.add_arc(0, "b", "b", 1.0, 2)
    t.set_final(1, 0.5)
    p = push(t, TROPICAL)
    assert p.num_states() == 2
    assert p.initial == 1.5


def test_no_path_raises():
    t = Machine()
    t.add_state()
    t.add_state()
    t.add_arc(0, "a", "a", 1.0, 0)
    t.set_final(1, 0.0)
    with pytest.raises(ValueError):
        push(t, TROPICAL)


def test_log_sum_of_pushed_start_is_total_weight():
    rng = random.Random(6)
    t = random_probabilistic(rng, 4, 2)
    p = push(t, LOG_COST)
    # In a stochastic machine the total of all strings is 1, so the start weight carries the total.
    total = -log_sum([-string_weight(t, x, LOG_COST) for x in all_strings(8)])
    assert p.initial <= total + 1e-12
    assert abs(p.initial - total) < 0.05
