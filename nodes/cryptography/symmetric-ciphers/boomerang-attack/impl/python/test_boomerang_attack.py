# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boomerang-attack/. The authors are listed in prov/008RPY.jsonl.

import random

from boomerang_attack import (
    ALPHA,
    DELTA,
    best_long_differential,
    boomerang_count,
    boomerang_rate,
    estimates,
    quartet_returns,
    tables,
)
from heys_spn import decrypt, encrypt


def _keys(seed: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.getrandbits(16) for _ in range(5)]


def test_tables_match_the_cipher() -> None:
    keys = _keys(1)
    _, _, e, d = tables(keys)
    for p in range(0, 1 << 16, 997):
        assert e[p] == encrypt(p, keys)
        assert d[e[p]] == p


def test_quartet_check_with_oracles() -> None:
    keys = _keys(2)
    _, _, e, d = tables(keys)
    enc = lambda p: encrypt(p, keys)  # noqa: E731
    dec = lambda c: decrypt(c, keys)  # noqa: E731
    for p in range(0, 1 << 16, 101):
        assert quartet_returns(enc, dec, p) == (d[e[p] ^ DELTA] ^ d[e[p ^ ALPHA] ^ DELTA] == ALPHA)


def test_boomerang_beats_the_long_differential() -> None:
    # The best 4-round differential from alpha holds with probability about
    # 2^-9; quartets return about ten times as often.
    for seed in range(3, 8):
        e0, e1, e, d = tables(_keys(seed))
        rate = boomerang_rate(e, d)
        long = best_long_differential(e)
        assert long < 0.004
        assert rate > 5 * long
        est = estimates(e0, e1)
        # Wagner's estimates, from exact half-cipher profiles, are lower than
        # the measured rate on this toy: the two halves are not independent.
        assert est["p2q2"] <= est["phat2qhat2"] <= rate


def test_sampled_rate_matches_exact_rate() -> None:
    keys = _keys(9)
    _, _, e, d = tables(keys)
    exact = boomerang_rate(e, d)
    rng = random.Random(10)
    n = 20000
    hits = sum(quartet_returns(e.__getitem__, d.__getitem__, rng.getrandbits(16)) for _ in range(n))
    sigma = (exact * (1 - exact) / n) ** 0.5
    assert abs(hits / n - exact) < 5 * sigma
    # The loop of the distinguisher gives the same fraction on the same texts.
    texts = [rng.getrandbits(16) for _ in range(2000)]
    same = sum(quartet_returns(e.__getitem__, d.__getitem__, p) for p in texts) / len(texts)
    assert boomerang_count(e.__getitem__, d.__getitem__, texts) == same


def test_wrong_alpha_does_not_return() -> None:
    # A random permutation returns a quartet with probability about 2^-16.
    e0, e1, e, d = tables(_keys(11))
    rng = random.Random(12)
    perm = list(range(1 << 16))
    rng.shuffle(perm)
    inv = [0] * (1 << 16)
    for x, y in enumerate(perm):
        inv[y] = x
    assert boomerang_rate(perm, inv) < 0.001 < boomerang_rate(e, d)
