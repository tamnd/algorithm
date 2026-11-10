# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rejection-sampling/. The authors are listed in prov/TF4M5C.jsonl.

import math
import random
from fractions import Fraction

import pytest

from rejection_sampling import (
    SQRT_2E_OVER_PI,
    acceptance_probability,
    beta22,
    normal_from_exponential,
    rejection_discrete,
    rejection_sample_counted,
)


class Branch(Exception):
    def __init__(self, n):
        self.n = n


class Cut(Exception):
    pass


class Script:
    """Replays a prefix of choices, then asks for a new one; cuts long runs."""

    def __init__(self, prefix, limit):
        self.prefix = prefix
        self.pos = 0
        self.limit = limit

    def randrange(self, n):
        if self.pos == self.limit:
            raise Cut()
        if self.pos < len(self.prefix):
            k = self.prefix[self.pos]
            self.pos += 1
            return k
        raise Branch(n)


def enumerate_law(sampler, limit):
    """Exact law of the output over all choice sequences of length <= limit.

    Returns ({output: probability}, probability of the cut runs).
    """
    law, cut = {}, Fraction(0)
    stack = [((), Fraction(1))]
    while stack:
        prefix, p = stack.pop()
        try:
            out = sampler(Script(list(prefix), limit))
        except Branch as b:
            for k in range(b.n):
                stack.append((prefix + (k,), p / b.n))
            continue
        except Cut:
            cut += p
            continue
        law[out] = law.get(out, Fraction(0)) + p
    return law, cut


def test_example() -> None:
    # Weights (1, 3, 2): wmax = 3, acceptance 6 / 9 = 2 / 3.
    assert acceptance_probability([1, 3, 2]) == (6, 9)

    class Fixed:
        def __init__(self, vals):
            self.vals = list(vals)

        def randrange(self, n):
            return self.vals.pop(0)

    # Try (i = 0, t = 2): 2 < 1 fails. Try (i = 2, t = 1): 1 < 2, accept index 2.
    assert rejection_discrete([1, 3, 2], Fixed([0, 2, 2, 1])) == 2


def test_exact_law_and_geometric_tries() -> None:
    for w in [[1, 3, 2], [2, 0, 1], [1, 1], [0, 5], [3, 1, 1, 2]]:
        n, W, wmax = len(w), sum(w), max(w)
        p = Fraction(W, n * wmax)
        for k in range(1, 4):
            law, cut = enumerate_law(lambda r: rejection_discrete(w, r), 2 * k)
            # Runs that finish within k tries: Pr[i, N <= k] = (w_i / W)(1 - (1 - p)^k).
            done = 1 - (1 - p) ** k
            assert cut == (1 - p) ** k
            for i in range(n):
                assert law.get(i, Fraction(0)) == Fraction(w[i], W) * done


def test_wrong_envelope_fails() -> None:
    # An envelope below the maximum weight caps the large weights.
    def wrong(r, w=(1, 3, 2)):
        while True:
            i = r.randrange(3)
            t = r.randrange(2)
            if t < w[i]:
                return i

    law, cut = enumerate_law(wrong, 4)
    total = sum(law.values())
    assert law[1] / total != Fraction(3, 6)


def ks_statistic(xs, cdf) -> float:
    xs = sorted(xs)
    m = len(xs)
    d = 0.0
    for i, x in enumerate(xs):
        c = cdf(x)
        d = max(d, (i + 1) / m - c, c - i / m)
    return d


def ks_threshold(m: int, alpha: float = 1e-9) -> float:
    # Dvoretzky-Kiefer-Wolfowitz with Massart's constant: Pr[D > t] <= 2 exp(-2 m t^2).
    return math.sqrt(math.log(2.0 / alpha) / (2.0 * m))


def phi(x: float) -> float:
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def beta22_cdf(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 3 * x * x - 2 * x ** 3


def test_continuous_ks_and_tries() -> None:
    rng = random.Random(1951)
    m = 40000
    xs = [normal_from_exponential(rng) for _ in range(m)]
    assert ks_statistic(xs, phi) < ks_threshold(m)
    ys = [beta22(rng) for _ in range(m)]
    assert ks_statistic(ys, beta22_cdf) < ks_threshold(m)
    # Mean number of tries is M for a normalized f.
    total = 0
    for _ in range(m):
        _, t = rejection_sample_counted(
            lambda x: 6.0 * x * (1.0 - x), lambda r: r.random(), lambda x: 1.0, 1.5, rng
        )
        total += t
    sd = math.sqrt((1 - 1 / 1.5) * 1.5 ** 2 / m)
    assert abs(total / m - 1.5) < 6 * sd
    assert abs(SQRT_2E_OVER_PI - 1.3155) < 1e-4


def test_continuous_wrong_envelope_fails() -> None:
    # M = 1 is below sup f / g = 3 / 2: the density becomes min(f, 1), flat in the middle.
    rng = random.Random(3)
    m = 40000
    xs = []
    for _ in range(m):
        y, _ = rejection_sample_counted(
            lambda x: 6.0 * x * (1.0 - x), lambda r: r.random(), lambda x: 1.0, 1.0, rng
        )
        xs.append(y)
    assert ks_statistic(xs, beta22_cdf) > ks_threshold(m)


def test_errors() -> None:
    with pytest.raises(ValueError):
        rejection_discrete([0, 0], random.Random(0))
