# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trevisan-extractor/. The authors are listed in prov/ENJAWZ.jsonl.

import random
from fractions import Fraction
from itertools import combinations, product

from trevisan_extractor import (
    IRREDUCIBLE,
    agreement,
    codeword,
    gf_mul,
    hadamard_bit,
    hybrid_probs,
    list_decode,
    max_intersection,
    polynomial_design,
    reconstruct,
    restrict,
    rs_value,
    rsh_bit,
    strong_distance,
    trevisan,
)


def bits_of(s: str):
    return tuple(int(c) for c in s)


def test_field_is_a_field() -> None:
    for t in range(1, 5):
        size = 1 << t
        for a in range(1, size):
            assert sum(1 for b in range(1, size) if gf_mul(a, b, t) == 1) == 1
        for a, b, c in product(range(size), repeat=3):
            assert gf_mul(a, b ^ c, t) == gf_mul(a, b, t) ^ gf_mul(a, c, t)
            assert gf_mul(gf_mul(a, b, t), c, t) == gf_mul(a, gf_mul(b, c, t), t)
    assert set(IRREDUCIBLE) == set(range(1, 9))


def test_design_property() -> None:
    for q, r, ell in [(3, 2, 3), (5, 2, 4), (5, 3, 4), (7, 2, 6)]:
        design = polynomial_design(q, r, ell)
        assert len(design) == q**r
        assert len(set(design)) == q**r
        assert all(len(s) == ell and max(s) < ell * q for s in design)
        assert max_intersection(design) == r - 1


def test_worked_example() -> None:
    design = polynomial_design(3, 2, 3)
    y = bits_of("101100110")
    assert [restrict(y, s) for s in design][:3] == [bits_of("111"), bits_of("100"), bits_of("101")]
    out = trevisan(bits_of("101"), y, design, hadamard_bit)
    assert out == bits_of("010110100")


def test_rs_example() -> None:
    # t = 2, x = (x_0, x_1) = (1, 2) in GF(4): p(alpha) = 1 + 2 alpha.
    x = (1, 0, 0, 1)
    assert [rs_value(x, a, 2) for a in range(4)] == [1, 3, 2, 0]


def test_hadamard_list_bound() -> None:
    # At most 1 / (4 delta^2) codewords agree with any word on 1/2 + delta of the positions.
    n = 4
    rng = random.Random(1)
    for _ in range(300):
        table = {z: rng.randrange(2) for z in product((0, 1), repeat=n)}
        word = lambda z, table=table: table[z]
        corr = [2 * agreement(word, x, hadamard_bit, n) - 1 for x in product((0, 1), repeat=n)]
        assert sum(c * c for c in corr) == 1  # Parseval
        for delta in (Fraction(1, 8), Fraction(1, 4), Fraction(3, 8)):
            count = sum(1 for c in corr if c >= 2 * delta)
            assert count * 4 * delta * delta <= 1


def test_rs_hadamard_distance() -> None:
    for t, n in [(2, 4), (3, 6), (2, 8)]:
        words = [codeword(x, lambda x, z, t=t: rsh_bit(x, z, t), 2 * t) for x in product((0, 1), repeat=n)]
        k = n // t
        bound = (2**t - k + 1) * 2 ** (t - 1)
        worst = min(sum(a != b for a, b in zip(u, v)) for u, v in combinations(words, 2))
        assert worst >= bound
        assert worst == bound


def test_johnson_bound_for_rs_hadamard() -> None:
    t, n = 3, 6
    gamma = Fraction(n // t - 1, 2 ** (t + 1))
    delta = Fraction(1, 4)
    limit = 1 / (4 * delta * delta - 2 * gamma)
    rng = random.Random(2)
    code = lambda x, z: rsh_bit(x, z, t)
    words = {x: codeword(x, code, 2 * t) for x in product((0, 1), repeat=n)}
    zs = list(product((0, 1), repeat=2 * t))
    for trial in range(200):
        if trial % 2:
            base = words[tuple(rng.randrange(2) for _ in range(n))]
            w = [b ^ (rng.random() < 0.2) for b in base]
        else:
            w = [rng.randrange(2) for _ in zs]
        count = sum(1 for cw in words.values() if Fraction(sum(a == b for a, b in zip(cw, w)), len(zs)) >= Fraction(1, 2) + delta)
        assert count <= limit


def test_one_output_bit_obeys_leftover_hash_lemma() -> None:
    design = polynomial_design(3, 2, 3)[:1]
    d = 9
    for k in range(0, 4):
        for support in combinations(list(product((0, 1), repeat=3)), 1 << k):
            source = {x: Fraction(1, 1 << k) for x in support}
            sd = strong_distance(source, design, hadamard_bit, d)
            assert 4 * sd * sd <= Fraction(2, 1 << k)


def test_reconstruction_is_exact() -> None:
    n, d = 3, 9
    design = polynomial_design(3, 2, 3)[:4]
    m = len(design)
    rng = random.Random(3)
    for _ in range(4):
        accept = {o for o in product((0, 1), repeat=m) if rng.randrange(2)}
        test = lambda o, accept=accept: int(o in accept)
        for x in product((0, 1), repeat=n):
            p = hybrid_probs(x, design, hadamard_bit, d, test)
            for i in range(1, m + 1):
                s_i = set(design[i - 1])
                others = [pos for pos in range(d) if pos not in s_i]
                total = Fraction(0)
                best = Fraction(0)
                count = 0
                for wbits in product((0, 1), repeat=len(others)):
                    w = [0] * d
                    for pos, b in zip(others, wbits):
                        w[pos] = b
                    for r in product((0, 1), repeat=m - i + 1):
                        word, tables = reconstruct(x, design, hadamard_bit, test, i, w, r)
                        assert all(len(tb) <= 2 for tb in tables)  # a = 1: at most 2^a entries
                        agr = agreement(word, x, hadamard_bit, n)
                        total += agr
                        best = max(best, agr)
                        count += 1
                # The average success over all fixings is exactly 1/2 + p_i - p_(i-1).
                assert total / count == Fraction(1, 2) + p[i] - p[i - 1]
                assert best >= Fraction(1, 2) + p[i] - p[i - 1]


def test_bad_source_is_in_the_list() -> None:
    n, d = 3, 9
    design = polynomial_design(3, 2, 3)[:3]
    m = len(design)
    # x = 000 has the zero codeword, so every output is 0. The test accepts only 000.
    test = lambda o: int(sum(o) == 0)
    x = bits_of("000")
    p = hybrid_probs(x, design, hadamard_bit, d, test)
    gap = p[m] - p[0]
    assert gap > 0
    i = max(range(1, m + 1), key=lambda j: p[j] - p[j - 1])
    assert p[i] - p[i - 1] >= gap / m
    s_i = set(design[i - 1])
    others = [pos for pos in range(d) if pos not in s_i]
    found = False
    for wbits in product((0, 1), repeat=len(others)):
        w = [0] * d
        for pos, b in zip(others, wbits):
            w[pos] = b
        for r in product((0, 1), repeat=m - i + 1):
            word, _ = reconstruct(x, design, hadamard_bit, test, i, w, r)
            if agreement(word, x, hadamard_bit, n) >= Fraction(1, 2) + gap / m:
                found = True
                # Agreements are multiples of 1/8, so this keeps exactly those >= 1/2 + gap/m.
                decoded = list_decode(word, n, hadamard_bit, n, Fraction(1, 2) + gap / m - Fraction(1, 1000))
                assert x in decoded
                assert len(decoded) * 4 * (gap / m) ** 2 <= 1
    assert found
