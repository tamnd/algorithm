# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peeling-decoding/. The authors are listed in prov/W86NJM.jsonl.

import itertools
import random
import time

from peeling_decoding import (bp_bec, checks_from_parity_check, is_stopping_set, max_stopping_set,
                              peel, peel_word)

# Hamming [7, 4, 3]: column j of H is the binary form of j + 1, least significant bit in row 0.
H7 = [[((j + 1) >> r) & 1 for j in range(7)] for r in range(3)]


def codewords(h, n):
    return [c for c in itertools.product((0, 1), repeat=n)
            if all(sum(a * b for a, b in zip(row, c)) % 2 == 0 for row in h)]


def ge_unique(h, erased):
    """Maximum likelihood (Gaussian elimination) succeeds iff the erased columns are independent."""
    vecs = [sum(h[r][j] << r for r in range(len(h))) for j in erased]
    basis = []
    for v in vecs:
        for b in basis:
            v = min(v, v ^ b)
        if v == 0:
            return False
        basis.append(v)
    return True


def check_code(h, n, book):
    stats = {"peel_ok": 0, "ml_only": 0, "both_fail": 0}
    for mask in range(1 << n):
        erased = {j for j in range(n) if mask >> j & 1}
        stop = max_stopping_set(h, erased)
        ml = ge_unique(h, sorted(erased))
        for c in book:
            y = [None if j in erased else c[j] for j in range(n)]
            out = peel_word(h, y)
            left = {j for j in range(n) if out[j] is None}
            assert left == stop  # peeling stops exactly at the largest stopping set
            assert all(out[j] == c[j] for j in range(n) if out[j] is not None)
            assert out == bp_bec(h, y)  # peeling is BP on the BEC
        if not stop:
            assert ml  # peeling success implies ML success
            stats["peel_ok"] += 1
        elif ml:
            stats["ml_only"] += 1
        else:
            stats["both_fail"] += 1
    return stats


def test_hamming_exhaustive():
    book = codewords(H7, 7)
    stats = check_code(H7, 7, book[:4])
    # 57 patterns are ML decodable; peeling gets 54 of them
    assert stats == {"peel_ok": 54, "ml_only": 3, "both_fail": 71}
    assert is_stopping_set(H7, {4, 5, 6}) and ge_unique(H7, [4, 5, 6])


def test_random_sparse_codes_exhaustive():
    rng = random.Random(1)
    for _ in range(3):
        n, m = 8, 5
        h = [[0] * n for _ in range(m)]
        for j in range(n):
            for r in rng.sample(range(m), 2):
                h[r][j] = 1
        book = codewords(h, n)
        check_code(h, n, [book[rng.randrange(len(book))]])


def test_worked_example():
    y = [None, 1, 1, None, 0, None, 0]
    checks, values = checks_from_parity_check(H7, y)
    assert checks == [[0], [5], [3, 5]] and values == [1, 0, 0]
    assert peel_word(H7, y) == [1, 1, 1, 0, 0, 0, 0]
    assert peel_word(H7, [1, 1, 1, 0, None, None, None]) == [1, 1, 1, 0, None, None, None]


def test_order_does_not_matter_and_packets_work():
    rng = random.Random(2)
    n = 60
    data = [rng.getrandbits(64) for _ in range(n)]
    checks = []
    for _ in range(80):
        vs = rng.sample(range(n), rng.choice((1, 2, 2, 3)))
        checks.append(vs)
    values = [0] * len(checks)
    for i, vs in enumerate(checks):
        for v in vs:
            values[i] ^= data[v]
    base = peel(n, checks, values)
    assert all(b is None or b == d for b, d in zip(base, data))
    for _ in range(10):
        order = list(range(len(checks)))
        rng.shuffle(order)
        again = peel(n, [checks[i] for i in order], [values[i] for i in order])
        assert [b is None for b in again] == [b is None for b in base]
        assert again == base


def test_linear_time():
    rng = random.Random(3)
    times = []
    for n in (20000, 80000):
        # a chain: check i links i - 1 and i, check 0 has only variable 0
        checks = [[0]] + [[i - 1, i] for i in range(1, n)]
        rng.shuffle(checks)
        values = [0] * n
        start = time.perf_counter()
        x = peel(n, checks, values)
        times.append(time.perf_counter() - start)
        assert x == [0] * n
    assert times[1] < 12 * times[0] + 0.05
