# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reed-muller-code/. The authors are listed in prov/CWKBQ3.jsonl.

import random

from reed_muller_code import (
    anf, code, degree, dimension, encode, generator, inner, min_weight_count, monomials, uuv,
    weight_distribution,
)


def test_parameters_small() -> None:
    # n = 2^m, k = sum_{i <= r} C(m, i), d = 2^(m - r), checked on every word
    for m in range(1, 5):
        for r in range(m + 1):
            c = code(r, m)
            assert len(c) == 2 ** dimension(r, m)
            wd = weight_distribution(c, 1 << m)
            assert min(w for w in range(1, (1 << m) + 1) if wd[w]) == 1 << (m - r)
            assert wd[1 << (m - r)] == min_weight_count(r, m)


def test_parameters_m5() -> None:
    for r in range(3):
        c = code(r, 5)
        wd = weight_distribution(c, 32)
        assert len(c) == 2 ** dimension(r, 5)
        assert min(w for w in range(1, 33) if wd[w]) == 1 << (5 - r)
        assert wd[1 << (5 - r)] == min_weight_count(r, 5)
    # RM(2, 5) is the self-dual [32, 16, 8] code; its weights are all multiples of 4
    wd = weight_distribution(code(2, 5), 32)
    assert {w: a for w, a in enumerate(wd) if a} == {0: 1, 8: 620, 12: 13888, 16: 36518,
                                                     20: 13888, 24: 620, 32: 1}


def test_uuv_recursion() -> None:
    for m in range(1, 5):
        for r in range(m + 1):
            assert uuv(r, m) == code(r, m)


def test_duality() -> None:
    # RM(r, m)^perp = RM(m - r - 1, m)
    for m in range(1, 6):
        for r in range(m):
            g, h = generator(r, m), generator(m - r - 1, m)
            assert all(inner(a, b) == 0 for a in g for b in h)
            assert dimension(r, m) + dimension(m - r - 1, m) == 1 << m


def test_special_cases() -> None:
    m = 4
    n = 1 << m
    assert code(0, m) == {0, (1 << n) - 1}                                   # repetition code
    assert code(m - 1, m) == {w for w in range(1 << n) if w.bit_count() % 2 == 0}  # even weight
    # RM(m - 2, m) is the extended Hamming code [16, 11, 4]: its dual is RM(1, m)
    assert len(code(m - 2, m)) == 2 ** 11
    # RM(1, m) is the augmented Hadamard code: x -> a . x + b
    had = {sum((((a & x).bit_count() + b) & 1) << x for x in range(n)) for a in range(n) for b in (0, 1)}
    assert had == code(1, m)


def test_degree_characterization() -> None:
    rng = random.Random(1954)
    for m in range(2, 7):
        for r in range(m + 1):
            for _ in range(20):
                msg = rng.randrange(1 << dimension(r, m))
                w = encode(msg, r, m)
                assert degree(w, m) <= r
                # the Moebius transform returns the message coefficients
                mons = monomials(r, m)
                assert set(anf(w, m)) == {mons[j] for j in range(len(mons)) if (msg >> j) & 1}
