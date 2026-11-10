# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nisan-wigderson-generator/. The authors are listed in prov/TFPG45.jsonl.

import random
from fractions import Fraction
from itertools import product

from nisan_wigderson_generator import (
    max_intersection,
    nw,
    polynomial_design,
    predictor_from_fixing,
    restrict,
)


def random_function(rng, n):
    table = {z: rng.randrange(2) for z in product((0, 1), repeat=n)}
    return lambda z: table[tuple(z)]


def hybrid_probs(design, f, test, d):
    """p_i = Pr[test(NW(y)_1..i, uniform rest) = 1], exactly, for i = 0..m."""
    m = len(design)
    accept = {z for z in product((0, 1), repeat=m) if test(z)}
    probs = []
    for i in range(m + 1):
        counts = {}
        for z in accept:
            counts[z[:i]] = counts.get(z[:i], 0) + 1
        total = 0
        for y in product((0, 1), repeat=d):
            total += counts.get(nw(y, design, f)[:i], 0)
        probs.append(Fraction(total, 2**d * 2 ** (m - i)))
    return probs


def test_design_parameters() -> None:
    for q in (2, 3, 5, 7):
        for r in range(1, min(q, 3) + 1):
            design = polynomial_design(q, r)
            assert len(design) == q**r
            assert all(len(set(s)) == q and all(0 <= p < q * q for p in s) for s in design)
            assert len(set(design)) == q**r
            if q**r <= 400:
                assert max_intersection(design) <= r - 1


def test_example_design_on_page() -> None:
    design = polynomial_design(3, 2)
    assert design[0] == (0, 3, 6)
    assert design[1] == (0, 4, 8)
    assert design[3] == (1, 4, 7)
    assert max_intersection(design) == 1
    maj = lambda z: 1 if sum(z) >= 2 else 0  # noqa: E731
    y = (1, 0, 1, 1, 0, 0, 1, 1, 0)
    assert nw(y, design, maj) == (1, 0, 1, 0, 0, 0, 0, 1, 1)


def test_output_matches_oracle() -> None:
    rng = random.Random(1)
    for _ in range(500):
        q = rng.choice((2, 3, 5))
        r = rng.randrange(1, 3)
        design = polynomial_design(q, r)
        f = random_function(rng, q)
        y = tuple(rng.randrange(2) for _ in range(q * q))
        out = nw(y, design, f)
        assert len(out) == q**r
        for i, s in enumerate(design):
            assert out[i] == f(tuple(y[p] for p in sorted(s)))


def check_reconstruction(design, d, f, test, i):
    m = len(design)
    s_i = design[i - 1]
    outside = [p for p in range(d) if p not in s_i]
    probs = hybrid_probs(design, f, test, d)
    right = 0
    best = 0
    count_fix = 0
    for w in product((0, 1), repeat=len(outside)):
        fixed = [0] * d
        for pos, bit in zip(outside, w):
            fixed[pos] = bit
        for j in range(i - 1):
            shared = sorted(set(s_i) & set(design[j]))
            seen = {}
            for z in product((0, 1), repeat=len(s_i)):
                y = list(fixed)
                for pos, bit in zip(s_i, z):
                    y[pos] = bit
                key = tuple(y[p] for p in shared)
                val = f(restrict(y, design[j]))
                assert seen.setdefault(key, val) == val
        for r in product((0, 1), repeat=m - i + 1):
            c = predictor_from_fixing(design, f, test, i, fixed, r)
            hits = sum(c(z) == f(z) for z in product((0, 1), repeat=len(s_i)))
            right += hits
            best = max(best, hits)
            count_fix += 1
    success = Fraction(right, count_fix * 2 ** len(s_i))
    assert success == Fraction(1, 2) + probs[i] - probs[i - 1]
    assert Fraction(best, 2 ** len(s_i)) >= success


def test_reconstruction_exact_small() -> None:
    rng = random.Random(2)
    design = polynomial_design(2, 2)
    for _ in range(40):
        f = random_function(rng, 2)
        test = random_function(rng, 4)
        for i in range(1, 5):
            check_reconstruction(design, 4, f, test, i)


def test_reconstruction_exact_q3() -> None:
    rng = random.Random(3)
    design = polynomial_design(3, 2)
    f = random_function(rng, 3)
    test = random_function(rng, 9)
    for i in (7, 8, 9):
        check_reconstruction(design, 9, f, test, i)


def test_telescoping() -> None:
    rng = random.Random(4)
    design = polynomial_design(2, 2)
    for _ in range(100):
        f = random_function(rng, 2)
        test = random_function(rng, 4)
        probs = hybrid_probs(design, f, test, 4)
        gaps = [probs[i] - probs[i - 1] for i in range(1, 5)]
        assert sum(gaps) == probs[-1] - probs[0]
        assert 4 * max(abs(g) for g in gaps) >= abs(probs[-1] - probs[0])


def test_parity_function_is_broken() -> None:
    design = polynomial_design(3, 3)
    d, m = 9, 27
    vectors = [sum(1 << p for p in s) for s in design]
    basis = []
    dep = 0
    for idx, v in enumerate(vectors):
        mask = 1 << idx
        for b, bm in basis:
            if v ^ b < v:
                v, mask = v ^ b, mask ^ bm
        if v == 0:
            dep = mask
            break
        basis.append((v, mask))
        basis.sort(reverse=True)
    assert dep != 0
    parity = lambda z: sum(z) & 1  # noqa: E731
    members = [k for k in range(m) if (dep >> k) & 1]
    for y in product((0, 1), repeat=d):
        out = nw(y, design, parity)
        assert sum(out[k] for k in members) % 2 == 0
