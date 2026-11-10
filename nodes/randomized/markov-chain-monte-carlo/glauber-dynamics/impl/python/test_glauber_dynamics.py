# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/glauber-dynamics/. The authors are listed in prov/G0ENPS.jsonl.

import itertools
import math
import random
from fractions import Fraction

from glauber_dynamics import (
    allowed_colors,
    glauber_coloring,
    glauber_coloring_step,
    glauber_step,
    greedy_coloring,
    heat_bath_law,
    is_proper,
)


class ScriptedRandom:
    """A fake generator that follows a list of choices and records each call."""

    def __init__(self, prefix: list[int]) -> None:
        self.prefix = prefix
        self.trace: list[tuple[int, int]] = []

    def randrange(self, n: int) -> int:
        k = len(self.trace)
        v = self.prefix[k] if k < len(self.prefix) else 0
        self.trace.append((v, n))
        return v


def step_law(adj, q, x):
    """The exact law of one step from x, by walking through every choice."""
    law: dict[tuple, Fraction] = {}
    stack: list[list[int]] = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptedRandom(prefix)
        y = tuple(glauber_coloring_step(adj, q, list(x), rng))
        p = Fraction(1)
        for _, n in rng.trace:
            p /= n
        law[y] = law.get(y, Fraction(0)) + p
        for i in range(len(prefix), len(rng.trace)):
            v, n = rng.trace[i]
            for c in range(v + 1, n):
                stack.append([a for a, _ in rng.trace[:i]] + [c])
    return law


def proper_colorings(adj, q):
    n = len(adj)
    return [x for x in itertools.product(range(q), repeat=n) if is_proper(adj, x)]


def chain(adj, q):
    states = proper_colorings(adj, q)
    return states, {x: step_law(adj, q, x) for x in states}


PATH3 = [[1], [0, 2], [1]]  # n = 3, max degree 2
EDGE = [[1], [0]]  # n = 2, max degree 1
TRIANGLE = [[1, 2], [0, 2], [0, 1]]


def tv_to_uniform(mu, m):
    return sum(abs(p - Fraction(1, m)) for p in mu.values()) / 2 + Fraction(m - len(mu), 2 * m)


def test_allowed_colors_and_example() -> None:
    x = [0, 1, 0]
    assert allowed_colors(PATH3, 5, x, 1) == [1, 2, 3, 4]
    assert allowed_colors(PATH3, 5, x, 0) == [0, 2, 3, 4]
    # Trace of the page: v = 1, then index 2 of [1, 2, 3, 4], so color 3.
    assert glauber_coloring_step(PATH3, 5, [0, 1, 0], ScriptedRandom([1, 2])) == [0, 3, 0]
    # v = 0: its neighbor has color 3, so the list is [0, 1, 2, 4]; index 3 gives 4.
    assert glauber_coloring_step(PATH3, 5, [0, 3, 0], ScriptedRandom([0, 3])) == [4, 3, 0]


def test_counts_of_proper_colorings() -> None:
    assert len(proper_colorings(PATH3, 5)) == 5 * 4 * 4
    assert len(proper_colorings(EDGE, 3)) == 6
    assert len(proper_colorings(TRIANGLE, 4)) == 24


def test_uniform_is_stationary_and_reversible() -> None:
    for adj, q in ((PATH3, 5), (EDGE, 3), (TRIANGLE, 4), (PATH3, 3)):
        states, P = chain(adj, q)
        m = len(states)
        for x in states:
            assert sum(P[x].values()) == 1
            assert set(P[x]) <= set(states)  # proper colorings stay proper
            for y, p in P[x].items():
                assert P[y].get(x, 0) == p  # symmetric, so detailed balance for uniform
        for y in states:
            assert sum(P[x].get(y, 0) for x in states) * Fraction(1, m) == Fraction(1, m)


def distances(adj, q, tmax):
    states, P = chain(adj, q)
    m = len(states)
    rows = {x: {x: Fraction(1)} for x in states}
    out = []
    for _ in range(tmax + 1):
        out.append(max(tv_to_uniform(rows[x], m) for x in states))
        new = {}
        for x in states:
            r: dict = {}
            for z, p in rows[x].items():
                for y, pp in P[z].items():
                    r[y] = r.get(y, 0) + p * pp
            new[x] = r
        rows = new
    return out


def test_exact_mixing_time_against_path_coupling_bound() -> None:
    for adj, q, delta, want in ((EDGE, 3, 1, 4), (PATH3, 5, 2, 6)):
        n = len(adj)
        bound = math.ceil((q - delta) / (q - 2 * delta) * n * math.log(4 * n))
        d = distances(adj, q, bound)
        assert all(a >= b for a, b in zip(d, d[1:]))  # d(t) does not increase
        tmix = next(t for t, v in enumerate(d) if v <= Fraction(1, 4))
        assert tmix == want
        assert tmix <= bound
        # the path coupling bound holds at each t: d(t) <= n (1 - (q-2D)/(n(q-D)))^t
        c = 1 - Fraction(q - 2 * delta, n * (q - delta))
        assert all(v <= n * c**t for t, v in enumerate(d))


def test_path_coupling_contraction() -> None:
    """For colorings (proper or not) that differ at one vertex, the coupling of the proof contracts."""
    for adj, q in ((PATH3, 5), (EDGE, 3), ([[1, 2, 3], [0], [0], [0]], 7)):
        n = len(adj)
        delta = max(len(a) for a in adj)
        bound = 1 - Fraction(q - 2 * delta, n * (q - delta))
        for x in itertools.product(range(q), repeat=n):
            for w in range(n):
                for b in range(q):
                    if b == x[w]:
                        continue
                    y = list(x)
                    y[w] = b
                    e = Fraction(0)
                    for v in range(n):
                        ax = allowed_colors(adj, q, x, v)
                        ay = allowed_colors(adj, q, y, v)
                        # optimal coupling of two uniform laws: disagree w.p. TV
                        common = len(set(ax) & set(ay))
                        p_dis = 1 - Fraction(common, max(len(ax), len(ay)))
                        if v == w:
                            assert ax == ay
                            e += Fraction(1, n) * 0
                        else:
                            e += Fraction(1, n) * (1 + p_dis)
                    assert e <= bound


def test_improper_start_becomes_proper() -> None:
    rng = random.Random(3)
    for _ in range(200):
        x = [0, 0, 0]
        glauber_coloring(PATH3, 5, x, 60, rng)
        assert is_proper(PATH3, x)


def test_statistics_with_a_seed() -> None:
    rng = random.Random(12345)
    n = 5000
    counts: dict = {}
    for _ in range(n):
        x = glauber_coloring(PATH3, 5, greedy_coloring(PATH3, 5), 30, rng)
        key = (x[0], x[1])
        counts[key] = counts.get(key, 0) + 1
    # (x0, x1) is uniform on the 20 ordered pairs of distinct colors.
    assert len(counts) == 20
    chi2 = sum((c - n / 20) ** 2 / (n / 20) for c in counts.values())
    assert chi2 < 60.0  # 19 degrees of freedom; Pr[chi2 > 60] is below 1e-5


def test_heat_bath_hard_core_exact() -> None:
    """General Glauber for the hard-core model with fugacity 2 on a path of 3 sites."""
    lam = Fraction(2)
    edges = [(0, 1), (1, 2)]

    def weight(y):
        if any(y[a] and y[b] for a, b in edges):
            return Fraction(0)
        return lam ** sum(y)

    states = [y for y in itertools.product((0, 1), repeat=3) if weight(y) > 0]
    z = sum(weight(y) for y in states)
    pi = {y: weight(y) / z for y in states}
    P = {x: {} for x in states}
    for x in states:
        for v in range(3):
            for s, p in heat_bath_law(x, v, (0, 1), weight):
                if p:
                    y = list(x)
                    y[v] = s
                    P[x][tuple(y)] = P[x].get(tuple(y), 0) + Fraction(1, 3) * p
    for x in states:
        assert sum(P[x].values()) == 1
        for y, p in P[x].items():
            assert pi[x] * p == pi[y] * P[y][x]
    rng = random.Random(9)
    x = [0, 0, 0]
    counts: dict = {}
    for _ in range(30000):
        glauber_step(x, (0, 1), weight, rng)
        counts[tuple(x)] = counts.get(tuple(x), 0) + 1
    for y in states:
        assert abs(counts.get(y, 0) / 30000 - float(pi[y])) < 0.03
