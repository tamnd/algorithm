# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coupling-from-the-past/. The authors are listed in prov/3S0NKB.jsonl.

import random
from fractions import Fraction

from coupling_from_the_past import (
    NoCoalescence,
    coupling_from_the_past,
    forward_coupling,
    monotone_cftp,
    walk_update,
)


class Exhausted(Exception):
    pass


class ScriptedRandom:
    """A fake generator that follows a list of choices and records each call.

    After the list it returns 0, and after cap calls it raises Exhausted, so
    that a caller can walk through every sequence of choices.
    """

    def __init__(self, prefix: list[int], cap: int) -> None:
        self.prefix = prefix
        self.cap = cap
        self.trace: list[tuple[int, int]] = []

    def randrange(self, n: int) -> int:
        k = len(self.trace)
        if k >= self.cap:
            raise Exhausted
        v = self.prefix[k] if k < len(self.prefix) else 0
        self.trace.append((v, n))
        return v


def exact_law(run, cap: int):
    """Walk through each sequence of choices of run(rng), with at most cap calls.

    Returns (law, rest): law maps each output to its exact probability, and
    rest is the probability that run needed more than cap calls.
    """
    law: dict = {}
    rest = Fraction(0)
    stack: list[list[int]] = [[]]
    while stack:
        prefix = stack.pop()
        rng = ScriptedRandom(prefix, cap)
        try:
            out = run(rng)
            done = True
        except Exhausted:
            done = False
        p = Fraction(1)
        for _, n in rng.trace:
            p /= n
        if done:
            law[out] = law.get(out, Fraction(0)) + p
        else:
            rest += p
        for i in range(len(prefix), len(rng.trace)):
            v, n = rng.trace[i]
            for c in range(v + 1, n):
                stack.append([x for x, _ in rng.trace[:i]] + [c])
    return law, rest


def stationary(P):
    """Solve pi P = pi, sum pi = 1 exactly by Gauss-Jordan elimination."""
    n = len(P)
    rows = [[P[i][j] - (1 if i == j else 0) for i in range(n)] + [Fraction(0)] for j in range(n - 1)]
    rows.append([Fraction(1)] * n + [Fraction(1)])
    for c in range(n):
        p = next(r for r in range(c, n) if rows[r][c] != 0)
        rows[c], rows[p] = rows[p], rows[c]
        for r in range(n):
            if r != c and rows[r][c] != 0:
                f = rows[r][c] / rows[c][c]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[c])]
    return [rows[i][n] / rows[i][i] for i in range(n)]


UPDATE = walk_update(2, 4, 2, 1)  # down w.p. 1/2, stay w.p. 1/4, up w.p. 1/4
DRAW = lambda rng: rng.randrange(4)  # noqa: E731


def matrix_of(update, k, m):
    P = [[Fraction(0)] * (k + 1) for _ in range(k + 1)]
    for x in range(k + 1):
        for u in range(m):
            P[x][update(x, u)] += Fraction(1, m)
    return P


def test_stationary_of_the_example() -> None:
    pi = stationary(matrix_of(UPDATE, 2, 4))
    assert pi == [Fraction(4, 7), Fraction(2, 7), Fraction(1, 7)]


def test_update_is_monotone() -> None:
    for u in range(4):
        vals = [UPDATE(x, u) for x in range(3)]
        assert vals == sorted(vals)


def test_scripted_runs() -> None:
    # u_1 = 0 (down): from 2 and 0 the states are 1 and 0. Not met, T = 2.
    # u_2 = 0 (down): T = 2 runs u_2 then u_1: 2 -> 1 -> 0 and 0 -> 0 -> 0.
    assert monotone_cftp(UPDATE, 0, 2, DRAW, ScriptedRandom([0, 0], 10)) == (0, 2)
    # u_1 = 3 (up), u_2 = 3 (up): both reach 2 at T = 2.
    assert monotone_cftp(UPDATE, 0, 2, DRAW, ScriptedRandom([3, 3], 10)) == (2, 2)
    # u_1 = 2 (stay), u_2 = 3 (up): 0 -> 1 -> 1 and 2 -> 2 -> 2, not met.
    # u_3 = 0, u_4 = 0: T = 4 runs down, down, up, stay: 2 -> 1 -> 0 -> 1 -> 1.
    assert monotone_cftp(UPDATE, 0, 2, DRAW, ScriptedRandom([2, 3, 0, 0], 10)) == (1, 4)


def test_exact_law_matches_pi() -> None:
    pi = [Fraction(4, 7), Fraction(2, 7), Fraction(1, 7)]
    prev_rest = Fraction(1)
    for cap in (1, 2, 4, 8):
        law, rest = exact_law(lambda r: monotone_cftp(UPDATE, 0, 2, DRAW, r)[0], cap)
        # Each partial law is below pi, and the missing mass is exactly rest.
        assert sum(law.values()) + rest == 1
        for y in range(3):
            assert law.get(y, 0) <= pi[y] <= law.get(y, 0) + rest
        assert rest <= prev_rest
        prev_rest = rest
    # With T at most 8 the run stops with probability 1 - 2377/65536.
    assert rest == Fraction(2377, 65536)
    assert law == {0: Fraction(9105, 16384), 1: Fraction(8817, 32768), 2: Fraction(9105, 65536)}


def test_general_cftp_agrees_with_monotone() -> None:
    a, ra = exact_law(lambda r: monotone_cftp(UPDATE, 0, 2, DRAW, r)[0], 8)
    b, rb = exact_law(lambda r: coupling_from_the_past(UPDATE, [0, 1, 2], DRAW, r)[0], 8)
    assert a == b and ra == rb


def test_forward_reading_is_biased() -> None:
    # Forward, the chains from 0 and 2 can meet only at 0 or at 2.
    law, rest = exact_law(lambda r: forward_coupling(UPDATE, 0, 2, DRAW, r)[0], 8)
    assert law.get(1, 0) == 0
    assert set(law) <= {0, 2}
    # pi(1) = 2/7 is far more than the missing mass, so the bias is proved.
    assert rest < Fraction(2, 7)
    # The state 0 gets too much mass: more than pi(0) even if all the rest went elsewhere.
    assert law[0] == Fraction(3011, 4096) and law[0] > Fraction(4, 7)


def test_statistics_with_a_seed() -> None:
    rng = random.Random(20240501)
    n = 21000
    counts = [0, 0, 0]
    for _ in range(n):
        x, _ = monotone_cftp(UPDATE, 0, 2, DRAW, rng)
        counts[x] += 1
    pi = [4 / 7, 2 / 7, 1 / 7]
    chi2 = sum((c - n * p) ** 2 / (n * p) for c, p in zip(counts, pi))
    assert chi2 < 20.0  # 2 degrees of freedom; Pr[chi2 > 20] is about 4.5e-5


def test_no_coalescence_is_reported() -> None:
    # The identity update never merges two states.
    try:
        monotone_cftp(lambda x, u: x, 0, 1, DRAW, random.Random(1), max_t=8)
    except NoCoalescence:
        pass
    else:
        raise AssertionError("expected NoCoalescence")


def test_larger_monotone_chain() -> None:
    # Walk on 0..5, down 1/3, up 1/3, stay 1/3: pi is uniform.
    upd = walk_update(5, 3, 1, 1)
    rng = random.Random(7)
    n = 12000
    counts = [0] * 6
    for _ in range(n):
        x, _ = monotone_cftp(upd, 0, 5, lambda r: r.randrange(3), rng)
        counts[x] += 1
    chi2 = sum((c - n / 6) ** 2 / (n / 6) for c in counts)
    assert chi2 < 30.0  # 5 degrees of freedom; Pr[chi2 > 30] is about 1.5e-5
