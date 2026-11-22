# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/syn-cookies/. The authors are listed in prov/Z3NQ59.jsonl.

import random

from syn_cookies import (
    MOD32,
    MSS_TABLE,
    check_cookie,
    keyed_hash,
    make_cookie,
    mss_index,
    split_cookie,
)

KEY = bytes(range(16))
C = ("203.0.113.7", 49152, "192.0.2.10", 443)


def test_example() -> None:
    m = mss_index(1460)
    assert m == 5
    y = make_cookie(KEY, C, 1000, m)
    assert y == 0x45D79C4E
    assert split_cookie(y) == (1000 % 32, 5, keyed_hash(KEY, C, 1000))
    a = (y + 1) % MOD32
    assert check_cookie(KEY, C, a, 1000, 2) == 1460
    assert check_cookie(KEY, C, a, 1001, 2) == 1460
    assert check_cookie(KEY, C, a, 1002, 2) == 1460
    assert check_cookie(KEY, C, a, 1003, 2) is None
    assert check_cookie(KEY, C, (a + 1) % MOD32, 1000, 2) is None
    other = ("203.0.113.7", 49153, "192.0.2.10", 443)
    assert check_cookie(KEY, other, a, 1000, 2) is None
    assert check_cookie(bytes(16), C, a, 1000, 2) is None


def test_edges() -> None:
    assert split_cookie(0xFFFFFFFF) == (31, 7, 0xFFFFFF)
    assert split_cookie(0) == (0, 0, 0)
    assert mss_index(100) == 0
    assert mss_index(9000) == 7
    # The counter crosses a multiple of 32 between the SYN and the ACK.
    for t in (30, 31, 63, 64, 1023):
        for m in range(8):
            y = make_cookie(KEY, C, t, m)
            for age in range(3):
                assert check_cookie(KEY, C, y + 1, t + age, 2) == MSS_TABLE[m]
            assert check_cookie(KEY, C, y + 1, t + 3, 2) is None
            assert check_cookie(KEY, C, y + 1, t + 32, 31) is None
    # A counter before 0 is never rebuilt.
    y = make_cookie(KEY, C, 0, 0)
    assert check_cookie(KEY, C, y + 1, 0, 0) == MSS_TABLE[0]
    # An ACK of 0 means y = 2^32 - 1, which no cookie for C at t = 0 equals.
    assert check_cookie(KEY, C, 0, 0, 5) is None
    # IPv6 documentation addresses work the same way.
    c6 = ("2001:db8::7", 50000, "2001:db8::10", 443)
    y6 = make_cookie(KEY, c6, 77, 3)
    assert check_cookie(KEY, c6, y6 + 1, 78, 1) == MSS_TABLE[3]


def _random_tuple(rng: random.Random) -> tuple[str, int, str, int]:
    return (f"198.51.100.{rng.randrange(1, 4)}", rng.choice((49152, 49153)), "192.0.2.10", 443)


def test_against_syn_cache() -> None:
    """Compare with a server that stores every SYN-ACK it sends (a SYN cache)."""
    rng = random.Random(4987)
    for _ in range(600):
        key = rng.randbytes(16)
        max_age = rng.randrange(0, 4)
        now = rng.randrange(0, 200)
        issued: list[tuple[tuple[str, int, str, int], int, int, int]] = []
        for _ in range(rng.randrange(1, 6)):
            c = _random_tuple(rng)
            t = now - rng.randrange(0, 40)
            if t < 0:
                continue
            m = rng.randrange(8)
            issued.append((c, t, m, make_cookie(key, c, t, m)))
        queries = [(c, (y + 1) % MOD32) for c, _, _, y in issued]
        queries += [(_random_tuple(rng), rng.randrange(MOD32)) for _ in range(3)]
        queries += [(_random_tuple(rng), (y + 1) % MOD32) for _, _, _, y in issued]
        for c, a in queries:
            want = None
            for c2, t2, m2, y2 in issued:
                if c2 == c and (y2 + 1) % MOD32 == a and 0 <= now - t2 <= max_age:
                    want = MSS_TABLE[m2]
            assert check_cookie(key, c, a, now, max_age) == want


def test_forged_acks_rejected() -> None:
    """An off-path guess passes with probability 2^-24; 20000 guesses expect 0.0012 hits."""
    rng = random.Random(8)
    hits = 0
    for _ in range(20000):
        if check_cookie(KEY, C, rng.randrange(MOD32), 500, 3) is not None:
            hits += 1
    assert hits == 0
