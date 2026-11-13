# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/belovs-k-distinctness/. The authors are listed in prov/KK9NWR.jsonl.
"""Tests of the classical parts of Belovs's learning graph for k-distinctness.

The quantum algorithm itself is not simulated: it is obtained from the dual adversary solution
through a general theorem. The tests check the exponents and the objective (12), the loading
procedure of Table 2 against a direct definition, and, for k = 2 on a small domain, that the
matrices X_j satisfy the constraint (1b) of the dual adversary bound exactly.
"""

import math
import random
from collections import Counter
from fractions import Fraction
from itertools import permutations, product

from belovs_k_distinctness import (
    STAR,
    DualK2,
    ambainis_bound,
    exponents,
    is_certificate,
    k2_objective,
    load,
    query_bound,
    sizes,
    stage_costs,
    term_exponents,
    weights,
)


def test_exponents():
    assert exponents(2) == [Fraction(2, 3)]
    assert exponents(3) == [Fraction(5, 7), Fraction(6, 7)]
    assert exponents(4)[0] == Fraction(11, 15)
    for k in range(2, 12):
        rho = exponents(k)
        assert rho[0] == Fraction(3, 4) - Fraction(1, 4 * (2**k - 1))
        # every term of (12) has the same exponent rho_1
        assert set(term_exponents(k)) == {rho[0]}
        # the sets get larger, and stay below n
        assert all(a < b < 1 for a, b in zip(rho, rho[1:]))
        # better than Ambainis for k >= 3, equal for k = 2
        if k == 2:
            assert rho[0] == Fraction(k, k + 1)
        else:
            assert rho[0] < Fraction(k, k + 1)


def test_objective():
    for k in range(2, 7):
        for e in (20, 40, 60):
            n = 2.0**e
            ratio = query_bound(n, k) / n ** float(exponents(k)[0])
            assert math.isclose(ratio, k, rel_tol=1e-9)
    assert math.isclose(ambainis_bound(2.0**30, 2), query_bound(2.0**30, 2), rel_tol=1e-9)
    # n^(5/7) against n^(3/4): at n = 2^60 the Belovs objective is less than half
    assert query_bound(2.0**60, 3) < ambainis_bound(2.0**60, 3) / 2


def test_weights_balance():
    # with the weights of Section 5.2, the negative and positive costs of each stage are equal
    n, k = 2.0**30, 4
    r = sizes(n, k)
    w = weights(n, k, r)
    for s in range(1, k + 1):
        neg = n**s * w[("II", s)] / math.prod(r[: s - 1])
        pos = 1 / w[("II", s)]
        assert math.isclose(neg, pos, rel_tol=1e-9)
    for s in range(2, k):
        w0, w1 = w[("I", s)]
        prod_s = math.prod(r[:s])
        neg = prod_s / n ** (s - 1) * w0 + r[s - 1] * w1
        pos = prod_s / (n ** (s - 1) * w1) + r[s - 1] / w0
        assert math.isclose(neg, pos, rel_tol=1e-9)
        assert math.isclose(neg / 2, stage_costs(n, k, r)[s - 1], rel_tol=1e-9)


def uncovered_direct(x, parts, t, s):
    """t in parts[s] is uncovered iff its value is in every earlier part (a chain of equal values)."""
    return all(x[t] in {x[u] for u in parts[i]} for i in range(s))


def test_loading_matches_definition():
    rng = random.Random(2026)
    for _ in range(300):
        k = rng.randint(2, 5)
        n = rng.randint(3 * k, 40)
        m = rng.randint(n // 2, 2 * n)
        x = [rng.randrange(m) for _ in range(n)]
        v = m  # a fresh value for the k-collision
        cert = sorted(rng.sample(range(n), k))
        for a in cert:
            x[a] = v
        rest = [i for i in range(n) if i not in cert]
        rng.shuffle(rest)
        parts, pos = [], 0
        for _ in range(k - 1):
            size = rng.randint(1, max(1, (len(rest) - pos) // (k - 1)))
            parts.append(rest[pos : pos + size])
            pos += size
        alpha, counts = load(x, k, cert, parts)
        for s, part in enumerate(parts):
            for t in part:
                assert (alpha[t] is not STAR) == uncovered_direct(x, parts, t, s)
            assert counts[s] == sum(uncovered_direct(x, parts, t, s) for t in part)
        # after stage II all of a_1, ..., a_k are uncovered: the final vertex holds a certificate
        assert all(alpha[a] == v for a in cert)
        assert is_certificate(alpha, k)
        # before a_k is loaded, exactly k - 1 uncovered elements hold the value v
        before = [a for t, a in alpha.items() if t != cert[-1]]
        assert before.count(v) == k - 1


def domain(n, m):
    neg = [z for z in product(range(m), repeat=n) if len(set(z)) == n]
    pos = [z for z in product(range(m), repeat=n) if sorted(Counter(z).values()) == [1] * (n - 2) + [2]]
    return neg, pos


def test_dual_adversary_k2_exact():
    neg, pos = domain(4, 4)
    assert (len(neg), len(pos)) == (24, 144)
    for r in (1, 2):
        d = DualK2(4, r)
        for x in pos:
            for y in neg:
                assert abs(d.entry(x, y) - 1) < 1e-12
        f_neg, f_pos = d.formula()
        assert all(math.isclose(d.diagonal(z), f_neg) for z in neg)
        assert all(math.isclose(d.diagonal(z), f_pos) for z in pos)
    # r = 1: objective max(6.5, 7) = r + sqrt(n) + n / sqrt(r)
    assert DualK2(4, 1).formula() == (6.5, 7.0)


def test_dual_adversary_k2_sampled():
    rng = random.Random(11)
    n, m = 6, 6
    neg = list(permutations(range(m)))
    for r in (1, 2, 3):
        d = DualK2(n, r)
        for _ in range(300):
            y = rng.choice(neg)
            x = list(rng.choice(neg))
            i, j = rng.sample(range(n), 2)
            x[j] = x[i]
            assert abs(d.entry(tuple(x), y) - 1) < 1e-12
            assert math.isclose(d.diagonal(tuple(x)), d.formula()[1])
        assert math.isclose(d.diagonal(neg[0]), d.formula()[0])


def test_dual_objective_scaling():
    # the k = 2 objective is about r + sqrt(n) + n / sqrt(r); its minimum is at r near
    # (n/2)^(2/3) with the value 3 (n/2)^(2/3) + sqrt(n) = Theta(n^(2/3))
    for n in (10**3, 10**4, 10**5):
        best_r = min(range(1, n - 2), key=lambda r: max(k2_objective(n, r)))
        best = max(k2_objective(n, best_r))
        assert 0.75 < best_r / (n / 2) ** (2 / 3) < 1.1
        assert 1.85 < best / n ** (2 / 3) < 2.35
