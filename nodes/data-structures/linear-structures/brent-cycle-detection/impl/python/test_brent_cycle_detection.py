# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brent-cycle-detection/. The authors are listed in prov/AW3RN4.jsonl.

import random

from brent_cycle_detection import brent, count_evaluations


def rho(f, x0):
    seen = {}
    x, i = x0, 0
    while x not in seen:
        seen[x] = i
        x, i = f(x), i + 1
    return i - seen[x], seen[x]


def test_page_examples() -> None:
    nxt = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 3}
    assert brent(nxt.__getitem__, 0) == (5, 3)
    assert count_evaluations(nxt.__getitem__, 0) == (5, 3, 23)
    f = lambda x: (x * x + 1) % 255
    assert brent(f, 3) == (6, 2)


def test_edges() -> None:
    assert brent(lambda x: x, 7) == (1, 0)
    assert brent(lambda x: 0, 5) == (1, 1)
    assert brent(lambda x: (x + 1) % 10, 0) == (10, 0)
    assert brent(lambda x: 1 - x, 0) == (2, 0)


def test_random_functions_against_hashing() -> None:
    rng = random.Random(1980)
    for _ in range(1000):
        n = rng.randrange(1, 60)
        table = [rng.randrange(n) for _ in range(n)]
        x0 = rng.randrange(n)
        lam, mu = rho(table.__getitem__, x0)
        got_lam, got_mu, calls = count_evaluations(table.__getitem__, x0)
        assert (got_lam, got_mu) == (lam, mu)
        assert calls < 2 * max(mu + 1, lam) + 2 * lam + 2 * mu
