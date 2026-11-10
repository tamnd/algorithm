# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyperloglog-plus-plus/. The authors are listed in prov/417CHM.jsonl.

import hashlib
import math
import random

from hyperloglog_plus_plus import (
    BiasTable,
    HyperLogLogPlusPlus,
    dense_update_of,
    sparse_to_dense,
    sparse_update_of,
)


def keyed_hash(seed: int):
    key = seed.to_bytes(8, "little")

    def h(x: object) -> int:
        d = hashlib.blake2b(repr(x).encode(), digest_size=8, key=key).digest()
        return int.from_bytes(d, "little")

    return h


def test_sparse_pair_decodes_to_dense_pair() -> None:
    rng = random.Random(1)
    cases = [0, 1, (1 << 64) - 1, 1 << 39, 1 << 38, 1 << 63]
    cases += [rng.getrandbits(64) for _ in range(3000)]
    # Hashes whose bits between p and p' are all 0 exercise the second branch.
    cases += [rng.getrandbits(4) << 60 | rng.getrandbits(39) for _ in range(500)]
    for y in cases:
        for p in (4, 6, 10, 14, 18):
            i, r = sparse_update_of(y)
            assert sparse_to_dense(i, r, p) == dense_update_of(y, p)


def dense_sketch(p: int, h, items) -> HyperLogLogPlusPlus:
    s = HyperLogLogPlusPlus(p, h)
    s.to_dense()
    s.add_all(items)
    return s


def test_sparse_then_dense_equals_dense_from_start() -> None:
    h = keyed_hash(2)
    rng = random.Random(3)
    p = 6  # m = 64: the sparse map holds at most 6 * 64 / 32 = 12 entries
    for _ in range(40):
        items = [rng.randrange(10**6) for _ in range(rng.randrange(60))]
        s = HyperLogLogPlusPlus(p, h)
        s.add_all(items)
        d = dense_sketch(p, h, items)
        assert s.dense_registers() == d.registers
        distinct_idx = len({sparse_update_of(h(x))[0] for x in items})
        assert s.is_sparse() == (distinct_idx <= 12)


def test_merge_equals_sketch_of_union_in_all_modes() -> None:
    h = keyed_hash(4)
    rng = random.Random(5)
    p = 6
    for _ in range(40):
        xs = [rng.randrange(10**6) for _ in range(rng.choice([5, 10, 40, 200]))]
        ys = [rng.randrange(10**6) for _ in range(rng.choice([5, 10, 40, 200]))]
        a, b, u = HyperLogLogPlusPlus(p, h), HyperLogLogPlusPlus(p, h), HyperLogLogPlusPlus(p, h)
        a.add_all(xs)
        b.add_all(ys)
        u.add_all(xs + ys + xs)
        mg = a.merge(b)
        assert mg.dense_registers() == u.dense_registers()
        if mg.is_sparse() and u.is_sparse():
            assert mg.sparse == u.sparse
            assert mg.estimate() == u.estimate()


def test_sparse_mode_is_nearly_exact_for_small_counts() -> None:
    # p = 14: the map stays sparse up to 3072 entries; linear counting over m' = 2^25 positions.
    rng = random.Random(6)
    for n in (1, 10, 100, 1000, 3000):
        s = HyperLogLogPlusPlus(14, lambda x: rng.getrandbits(64))
        s.add_all(range(n))
        assert s.is_sparse()
        assert abs(s.estimate() / n - 1) < 0.002
    assert HyperLogLogPlusPlus(14, keyed_hash(0)).threshold == 11500


def test_empirical_bias_correction_removes_small_range_bias() -> None:
    # Build a small table for p = 6 by seeded simulation, as the paper does for p = 4 .. 18.
    rng = random.Random(7)
    p, m = 6, 64
    raw, bias = [], []
    for n in range(10, 5 * m + 1, 10):
        es = [dense_sketch(p, lambda x: rng.getrandbits(64), range(n)).raw_estimate() for _ in range(50)]
        raw.append(sum(es) / len(es))
        bias.append(raw[-1] - n)
    table = BiasTable(raw, bias, k=6)
    for n in (60, 120):
        er, ec = [], []
        for _ in range(250):
            e = dense_sketch(p, lambda x: rng.getrandbits(64), range(n)).raw_estimate()
            er.append(e / n - 1)
            ec.append((e - table(e)) / n - 1)
        raw_mean, cor_mean = sum(er) / len(er), sum(ec) / len(ec)
        # Tolerance: the corrected mean error is below 5 percent and well below the raw one.
        assert abs(cor_mean) < 0.05
        assert raw_mean > abs(cor_mean) + 0.02


def test_dense_standard_error() -> None:
    rng = random.Random(8)
    p, n, trials = 6, 3000, 200
    errs = [dense_sketch(p, lambda x: rng.getrandbits(64), range(n)).estimate() / n - 1 for _ in range(trials)]
    se = 1.054 / math.sqrt(1 << p)
    rms = math.sqrt(sum(e * e for e in errs) / trials)
    # Tolerance: RMS within 25 percent of beta_64 / sqrt(64).
    assert 0.75 * se <= rms <= 1.25 * se
