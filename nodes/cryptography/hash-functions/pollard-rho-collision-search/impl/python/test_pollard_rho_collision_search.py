# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pollard-rho-collision-search/. The authors are listed in prov/YJ25N1.jsonl.

import hashlib
import math
import random

from pollard_rho_collision_search import (
    distinguished_point_search,
    find_collision,
    rho_collision,
    tail_and_cycle,
)


def trunc_sha256(n: int):
    """f(x) = the first n bits of SHA-256 of the 4-byte encoding of x."""

    def f(x: int) -> int:
        return int.from_bytes(hashlib.sha256(x.to_bytes(4, "big")).digest()[:4], "big") >> (32 - n)

    return f


class Counted:
    def __init__(self, f):
        self.f, self.calls = f, 0

    def __call__(self, x: int) -> int:
        self.calls += 1
        return self.f(x)


def lazy_random_function(rng: random.Random, n_values: int):
    table: dict[int, int] = {}

    def f(x: int) -> int:
        if x not in table:
            table[x] = rng.randrange(n_values)
        return table[x]

    return f


def test_real_collision_on_truncated_sha256() -> None:
    for n in (24, 28, 32):
        f = Counted(trunc_sha256(n))
        a, b = find_collision(f, 1 << n, random.Random(n))
        assert a != b
        da = hashlib.sha256(a.to_bytes(4, "big")).digest()
        db = hashlib.sha256(b.to_bytes(4, "big")).digest()
        assert da != db and (int.from_bytes(da[:4], "big") >> (32 - n)) == (int.from_bytes(db[:4], "big") >> (32 - n))
        assert f.calls < 40 * math.isqrt(1 << n)


def test_agrees_with_tail_and_cycle_on_small_maps() -> None:
    rng = random.Random(7)
    for _ in range(500):
        size = rng.randrange(1, 60)
        table = [rng.randrange(size) for _ in range(size)]
        f = table.__getitem__
        x0 = rng.randrange(size)
        mu, lam = tail_and_cycle(f, x0)
        # brute force path
        path, pos = [], {}
        x = x0
        while x not in pos:
            pos[x] = len(path)
            path.append(x)
            x = f(x)
        assert (mu, lam) == (pos[x], len(path) - pos[x])
        res = rho_collision(f, x0)
        if mu == 0:
            assert res is None
        else:
            a, b = res
            assert a == path[mu - 1] and b == path[mu + lam - 1] and f(a) == f(b) and a != b


def test_expected_rho_length() -> None:
    # E[mu + lam] = Q(N) = sum_k N!/((N-k)! N^k) ~ sqrt(pi N / 2), and E[lam] = (Q(N) + 1) / 2.
    big_n = 1 << 12
    q, term = 0.0, 1.0
    for k in range(1, big_n + 1):
        term *= (big_n - k + 1) / big_n
        q += term
    assert abs(q - math.sqrt(math.pi * big_n / 2)) < 0.5
    rng = random.Random(99)
    trials = 3000
    rho_sum = lam_sum = 0
    for _ in range(trials):
        f = lazy_random_function(rng, big_n)
        mu, lam = tail_and_cycle(f, rng.randrange(big_n))
        rho_sum += mu + lam
        lam_sum += lam
    assert abs(rho_sum / trials - q) / q < 0.05
    assert abs(lam_sum / trials - (q + 1) / 2) / q < 0.05


def test_distinguished_points() -> None:
    n = 28
    f = Counted(trunc_sha256(n))
    (a, b), stored = distinguished_point_search(f, 1 << n, 6, random.Random(5))
    assert a != b and f(a) == f(b)
    # memory is the number of distinguished points, far below the 2^14 of a table
    assert stored < 2000
