# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-mutual-information/. The authors are listed in prov/3MRTH1.jsonl.

import itertools
import random
from collections import Counter
from fractions import Fraction
from math import comb, isclose

from normalized_mutual_information import (
    adjusted_mutual_information,
    entropy_of_labels,
    expected_mutual_information,
    mutual_information,
    normalized_mutual_information,
)

IIR_CLUSTERS = [1] * 6 + [2] * 6 + [3] * 5
IIR_CLASSES = list("xxxxxo") + list("xooood") + list("xxddd")
METHODS = ["sqrt", "arithmetic", "max", "min"]


def test_identical_partitions_give_one() -> None:
    rng = random.Random(5)
    for _ in range(50):
        u = [rng.randrange(4) for _ in range(rng.randrange(2, 20))]
        if len(set(u)) < 2:
            continue
        for m in METHODS:
            assert isclose(normalized_mutual_information(u, u, m), 1.0, abs_tol=1e-12)
            assert isclose(adjusted_mutual_information(u, u, m), 1.0, abs_tol=1e-12)


def test_invariance_under_label_permutation() -> None:
    rng = random.Random(9)
    for _ in range(100):
        n = rng.randrange(2, 25)
        u = [rng.randrange(4) for _ in range(n)]
        v = [rng.randrange(5) for _ in range(n)]
        perm = list(range(5))
        rng.shuffle(perm)
        v2 = [perm[x] for x in v]
        for m in METHODS:
            a = normalized_mutual_information(u, v, m)
            assert isclose(a, normalized_mutual_information(u, v2, m), abs_tol=1e-12)
            assert isclose(a, normalized_mutual_information(v, u, m), abs_tol=1e-12)
            assert -1e-12 <= a <= 1 + 1e-12


def test_order_of_normalizations() -> None:
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randrange(2, 25)
        u = [rng.randrange(3) for _ in range(n)]
        v = [rng.randrange(4) for _ in range(n)]
        if len(set(u)) < 2 or len(set(v)) < 2:
            continue
        vals = [normalized_mutual_information(u, v, m) for m in ["max", "arithmetic", "sqrt", "min"]]
        assert all(x <= y + 1e-12 for x, y in zip(vals, vals[1:]))


def test_iir_example() -> None:
    assert isclose(mutual_information(IIR_CLUSTERS, IIR_CLASSES), 0.39194, abs_tol=5e-6)
    assert isclose(normalized_mutual_information(IIR_CLUSTERS, IIR_CLASSES, "arithmetic"), 0.3646, abs_tol=5e-5)
    assert isclose(normalized_mutual_information(IIR_CLUSTERS, IIR_CLASSES, "sqrt"), 0.3646, abs_tol=5e-4)


def test_independent_partitions() -> None:
    assert isclose(normalized_mutual_information([0, 0, 1, 1], [0, 1, 0, 1]), 0.0, abs_tol=1e-15)


def test_degenerate_cases() -> None:
    assert normalized_mutual_information([0, 0, 0], [1, 1, 1]) == 1.0
    assert normalized_mutual_information([0, 0, 0], [0, 1, 2]) == 0.0
    assert adjusted_mutual_information([0, 1, 2], [2, 1, 0]) == 1.0
    assert adjusted_mutual_information([], []) == 1.0


def arrangements(v):
    return set(itertools.permutations(v))


def test_hypergeometric_cell_law() -> None:
    u = [0, 0, 0, 1, 1, 2, 2]
    v = [0, 0, 1, 1, 1, 1, 2]
    arr = arrangements(v)
    n = len(u)
    for x, a in Counter(u).items():
        for y, b in Counter(v).items():
            counts = Counter(sum(1 for i in range(n) if u[i] == x and p[i] == y) for p in arr)
            for t in range(0, min(a, b) + 1):
                want = Fraction(comb(b, t) * comb(n - b, a - t), comb(n, a))
                assert Fraction(counts[t], len(arr)) == want


def test_expected_mi_against_brute_force() -> None:
    rng = random.Random(4)
    for _ in range(25):
        n = rng.randrange(2, 8)
        u = [rng.randrange(3) for _ in range(n)]
        v = [rng.randrange(3) for _ in range(n)]
        arr = arrangements(v)
        brute = sum(mutual_information(u, p) for p in arr) / len(arr)
        assert isclose(expected_mutual_information(u, v), brute, abs_tol=1e-12)


def test_nmi_is_not_adjusted_but_ami_is() -> None:
    u = [0, 0, 1, 1, 2, 2, 3]
    v = [0, 1, 1, 2, 2, 3, 3]
    arr = arrangements(v)
    mean_nmi = sum(normalized_mutual_information(u, p) for p in arr) / len(arr)
    mean_ami = sum(adjusted_mutual_information(u, p) for p in arr) / len(arr)
    assert mean_nmi > 0.5
    assert isclose(mean_ami, 0.0, abs_tol=1e-12)
