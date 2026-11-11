# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exhaustive-key-search/. The authors are listed in prov/BSXCZ6.jsonl.

import random

from exhaustive_key_search import first_key, key_search, toy_encrypt

K = 16  # key length of the toy cipher
X0 = 0x1234  # the fixed chosen plaintext of the time-memory trade-offs


def test_finds_the_key_with_two_pairs() -> None:
    rng = random.Random(1)
    for _ in range(2):
        key = rng.randrange(1 << K)
        xs = rng.sample(range(1 << 16), 2)
        pairs = [(x, toy_encrypt(key, x)) for x in xs]
        assert key_search(toy_encrypt, pairs, K) == [key]


def test_false_positives_with_one_pair() -> None:
    # With one pair, each wrong key passes with probability about 2^-16, so about 1 false key is expected.
    rng = random.Random(2)
    total = 0
    for _ in range(3):
        key = rng.randrange(1 << K)
        x = rng.randrange(1 << 16)
        found = key_search(toy_encrypt, [(x, toy_encrypt(key, x))], K)
        assert key in found
        total += len(found) - 1
    assert total <= 10


def test_average_work_is_about_half() -> None:
    # The key is uniform, so its position in the search order is uniform: about 2^(k-1) tries on average.
    rng = random.Random(3)
    tries = []
    for _ in range(8):
        key = rng.randrange(1 << K)
        xs = rng.sample(range(1 << 16), 2)
        pairs = [(x, toy_encrypt(key, x)) for x in xs]
        found, tried = first_key(toy_encrypt, pairs, K)
        assert found == key
        assert tried == key + 1
        tries.append(tried)
    assert 0.2 < sum(tries) / len(tries) / (1 << K) < 0.8


def test_multi_target() -> None:
    # T = 64 targets under the same plaintext: a scan hits a first target after about 2^k / (T + 1) tries.
    rng = random.Random(4)
    keys = set(rng.sample(range(1 << K), 64))
    targets = {toy_encrypt(key, X0): key for key in keys}
    tried = 0
    for key in range(1 << K):
        tried += 1
        y = toy_encrypt(key, X0)
        if y in targets:
            break
    assert toy_encrypt(targets[y], X0) == y
    assert tried < (1 << K) // 8


def _f(key: int, col: int) -> int:
    """The step function of a chain: encrypt X0 under the key, then reduce with the column index."""
    return toy_encrypt(key, X0) ^ col


def hellman_tables(tables: int, m: int, t: int, rng: random.Random) -> list[dict[int, int]]:
    """Hellman (1980): each table i uses its own reduction (XOR with i) and keeps only (end, start)."""
    out = []
    for i in range(tables):
        table = {}
        for _ in range(m):
            start = rng.randrange(1 << K)
            key = start
            for _ in range(t):
                key = _f(key, i)
            table[key] = start
        out.append(table)
    return out


def hellman_lookup(tabs: list[dict[int, int]], t: int, y0: int) -> int | None:
    for i, table in enumerate(tabs):
        key = y0 ^ i
        for j in range(t):
            if key in table:
                cand = table[key]
                for _ in range(t - 1 - j):
                    cand = _f(cand, i)
                if toy_encrypt(cand, X0) == y0:
                    return cand
            key = _f(key, i)
    return None


def rainbow_table(m: int, t: int, rng: random.Random) -> dict[int, int]:
    """Oechslin (2003): one table, with the reduction of column j (XOR with j) in each chain."""
    table = {}
    for _ in range(m):
        start = rng.randrange(1 << K)
        key = start
        for j in range(t):
            key = _f(key, j)
        table[key] = start
    return table


def rainbow_lookup(table: dict[int, int], t: int, y0: int) -> int | None:
    for col in range(t - 1, -1, -1):
        key = y0 ^ col
        for j in range(col + 1, t):
            key = _f(key, j)
        if key in table:
            cand = table[key]
            for j in range(col):
                cand = _f(cand, j)
            if toy_encrypt(cand, X0) == y0:
                return cand
    return None


def test_hellman_tmto() -> None:
    rng = random.Random(1980)
    tabs = hellman_tables(4, 256, 64, rng)
    wins = 0
    for _ in range(20):
        key = rng.randrange(1 << K)
        got = hellman_lookup(tabs, 64, toy_encrypt(key, X0))
        if got is not None:
            assert toy_encrypt(got, X0) == toy_encrypt(key, X0)
            wins += 1
    assert wins >= 5


def test_rainbow_table() -> None:
    rng = random.Random(2003)
    table = rainbow_table(1024, 64, rng)
    wins = 0
    for _ in range(20):
        key = rng.randrange(1 << K)
        got = rainbow_lookup(table, 64, toy_encrypt(key, X0))
        if got is not None:
            assert toy_encrypt(got, X0) == toy_encrypt(key, X0)
            wins += 1
    assert wins >= 5
