# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tabled-asymmetric-numeral-systems/. The authors are listed in prov/8ATQ56.jsonl.

import math
import random

import pytest

from tabled_asymmetric_numeral_systems import (
    LL_DEFAULT_ACCURACY_LOG, LL_DEFAULT_NORM, build_tables, decode, encode, model_cost, normalize,
)

# RFC 8878 Appendix A.1, the decoding table of the predefined literals length
# distribution: state -> (symbol, Number_of_Bits, Baseline). Copied by hand.
RFC8878_LL_TABLE = {
    0: (0, 4, 0), 1: (0, 4, 16), 2: (1, 5, 32), 3: (3, 5, 0), 4: (4, 5, 0), 5: (6, 5, 0),
    6: (7, 5, 0), 7: (9, 5, 0), 8: (10, 5, 0), 9: (12, 5, 0), 10: (14, 6, 0), 11: (16, 5, 0),
    12: (18, 5, 0), 13: (19, 5, 0), 14: (21, 5, 0), 15: (22, 5, 0), 16: (24, 5, 0), 17: (25, 5, 32),
    18: (26, 5, 0), 19: (27, 6, 0), 20: (29, 6, 0), 21: (31, 6, 0), 22: (0, 4, 32), 23: (1, 4, 0),
    24: (2, 5, 0), 25: (4, 5, 32), 26: (5, 5, 0), 27: (7, 5, 32), 28: (8, 5, 0), 29: (10, 5, 32),
    30: (11, 5, 0), 31: (13, 6, 0), 32: (16, 5, 32), 33: (17, 5, 0), 34: (19, 5, 32), 35: (20, 5, 0),
    36: (22, 5, 32), 37: (23, 5, 0), 38: (25, 4, 0), 39: (25, 4, 16), 40: (26, 5, 32), 41: (28, 6, 0),
    42: (30, 6, 0), 43: (0, 4, 48), 44: (1, 4, 16), 45: (2, 5, 32), 46: (3, 5, 32), 47: (5, 5, 32),
    48: (6, 5, 32), 49: (8, 5, 32), 50: (9, 5, 32), 51: (11, 5, 32), 52: (12, 5, 32), 53: (15, 6, 0),
    54: (17, 5, 32), 55: (18, 5, 32), 56: (20, 5, 32), 57: (21, 5, 32), 58: (23, 5, 32), 59: (24, 5, 32),
    60: (35, 6, 0), 61: (34, 6, 0), 62: (33, 6, 0), 63: (32, 6, 0),
}


def test_rfc8878_literals_length_default_table() -> None:
    dtable, _ = build_tables(LL_DEFAULT_NORM, LL_DEFAULT_ACCURACY_LOG)
    assert len(dtable) == 64
    for u, row in RFC8878_LL_TABLE.items():
        assert dtable[u] == row, u


def test_rfc8878_baseline_example() -> None:
    # RFC 8878 Table 21: a symbol with probability 5 at accuracy log 7.
    dtable, states = build_tables([5, 123], 7)
    rows = [dtable[u] for u in states[0]]
    assert [nb for _, nb, _ in rows] == [5, 5, 5, 4, 4]
    assert [base for _, _, base in rows] == [32, 64, 96, 0, 16]


def test_example() -> None:
    # The worked example of the page: L = 16, counts a:8, b:5, c:3.
    norm = [8, 5, 3]
    dtable, states = build_tables(norm, 4)
    assert "".join("abc"[s] for s, _, _ in dtable) == "aabcabcabcaabaab"
    assert states == [[0, 1, 4, 7, 10, 11, 13, 14], [2, 5, 8, 12, 15], [3, 6, 9]]
    assert [dtable[u] for u in states[2]] == [(2, 3, 8), (2, 2, 0), (2, 2, 4)]
    msg = [0, 1, 0, 2, 0, 0]  # a b a c a a
    code = encode(msg, norm, 4)
    assert code.hex() == "b008"
    assert decode(code, len(msg), norm, 4) == msg


def test_tables_are_consistent() -> None:
    rng = random.Random(13)
    for _ in range(100):
        r = rng.randint(5, 10)
        k = rng.randint(2, min(40, 1 << r))
        counts = [rng.randint(0, 100) for _ in range(k)]
        counts[0] += 1
        counts[1] += 1
        norm = normalize(counts, r)
        dtable, states = build_tables(norm, r)
        size = 1 << r
        for s, cells in enumerate(states):
            assert len(cells) == max(norm[s], 0)
            # From the cells of s, the next states cover [0, L) once each.
            covered = sorted(v for u in cells for v in range(dtable[u][2], dtable[u][2] + (1 << dtable[u][1])))
            assert covered == (list(range(size)) if cells else [])


def test_edges() -> None:
    norm = [12, 4]
    for msg in ([], [0], [1], [0] * 500, [1] * 500):
        code = encode(msg, norm, 4)
        assert decode(code, len(msg), norm, 4) == msg
    with pytest.raises(ValueError):
        build_tables([3, 3], 4)
    with pytest.raises(ValueError):
        decode(b"\x00", 1, norm, 4)


def test_roundtrip_with_less_than_one_symbols() -> None:
    rng = random.Random(8878)
    weights = [max(c, 0) or 0.05 for c in LL_DEFAULT_NORM]
    for _ in range(50):
        msg = rng.choices(range(len(LL_DEFAULT_NORM)), weights=weights, k=rng.randint(1, 300))
        code = encode(msg, LL_DEFAULT_NORM, LL_DEFAULT_ACCURACY_LOG)
        assert decode(code, len(msg), LL_DEFAULT_NORM, LL_DEFAULT_ACCURACY_LOG) == msg


def test_random_roundtrip_and_size() -> None:
    rng = random.Random(2013)
    for _ in range(100):
        k = rng.randint(2, 64)
        weights = [rng.random() ** 3 for _ in range(k)]
        msg = rng.choices(range(k), weights=weights, k=rng.randint(1, 500))
        counts = [msg.count(s) for s in range(k)]
        if sum(1 for c in counts if c) < 2:
            continue
        norm = normalize(counts, 11)
        code = encode(msg, norm, 11)
        assert decode(code, len(msg), norm, 11) == msg
    # Large inputs: the output is close to the ideal length under the table.
    for weights in ([8, 4, 2, 1, 1], [30, 1], [1] * 200):
        msg = rng.choices(range(len(weights)), weights=weights, k=20000)
        counts = [msg.count(s) for s in range(len(weights))]
        n = len(msg)
        h0 = -sum(c / n * math.log2(c / n) for c in counts if c)
        norm = normalize(counts, 11)
        size = 8 * len(encode(msg, norm, 11))
        ideal = model_cost(msg, norm, 11)
        assert ideal <= n * h0 + 0.01 * n
        assert ideal - 11 <= size <= ideal + 0.01 * n + 20
