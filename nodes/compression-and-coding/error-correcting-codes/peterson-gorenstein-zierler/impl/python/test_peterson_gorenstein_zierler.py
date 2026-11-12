# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-gorenstein-zierler/. The authors are listed in prov/7Z5YDC.jsonl.

import itertools
import random

from gf import GF2m
from peterson_gorenstein_zierler import hankel, pgz_decode, pgz_locator, rank, solve, syndromes

F8 = GF2m(3, 0b1011)  # x^3 + x + 1
F16 = GF2m(4, 0b10011)  # x^4 + x + 1
F256 = GF2m(8, 0x11D)  # x^8 + x^4 + x^3 + x^2 + 1
CCSDS = GF2m(8, 0x187)  # x^8 + x^7 + x^2 + x + 1


def berlekamp_massey(f: GF2m, s: list[int]) -> list[int]:
    """Oracle: the shortest LFSR connection polynomial of s (Massey 1969), trimmed."""
    return bm_with_length(f, s)[1]


def bm_with_length(f: GF2m, s: list[int]) -> tuple[int, list[int]]:
    """The LFSR length L and the trimmed connection polynomial (its degree can be below L)."""
    c, bpoly, L, m, bval = [1], [1], 0, 1, 1
    for r in range(len(s)):
        d = 0
        for j in range(min(L, len(c) - 1) + 1):
            d ^= f.mul(c[j], s[r - j])
        if d == 0:
            m += 1
            continue
        coef = f.div(d, bval)
        new = c + [0] * max(0, m + len(bpoly) - len(c))
        for j, v in enumerate(bpoly):
            new[m + j] ^= f.mul(coef, v)
        if 2 * L <= r:
            bpoly, bval, L, m = c, d, r + 1 - L, 1
        else:
            m += 1
        c = new
    return L, f.trim(c)


def rs_codeword(f: GF2m, msg: list[int], nsym: int, b: int = 1, step: int = 1) -> list[int]:
    """Systematic Reed-Solomon codeword: the remainder in positions 0 .. nsym - 1."""
    g = [1]
    for j in range(b, b + nsym):
        g = f.pmul(g, [f.alpha(step * j), 1])
    _, rem = f.pdivmod([0] * nsym + list(msg), g)
    return rem + [0] * (nsym - len(rem)) + list(msg)


def add_errors(c: list[int], pos: tuple[int, ...] | list[int], vals: tuple[int, ...] | list[int]) -> list[int]:
    r = list(c)
    for i, v in zip(pos, vals):
        r[i] ^= v
    return r


def test_worked_example() -> None:
    a = F16.alpha
    c = rs_codeword(F16, [a(i) for i in range(11)], 4)
    r = add_errors(c, [2, 7], [a(5), a(11)])
    syn = syndromes(F16, r, 4)
    assert syn == [a(4), a(13), a(9), a(10)]
    assert pgz_locator(F16, syn) == [1, a(12), a(9)]
    assert pgz_decode(F16, r, 4) == (c, [2, 7], [a(5), a(11)])
    # one error: M_2 is singular, M_1 = [S_1] is not
    r1 = add_errors(c, [4], [a(3)])
    syn1 = syndromes(F16, r1, 4)
    assert solve(F16, hankel(syn1, 2), syn1[2:4]) is None
    assert pgz_decode(F16, r1, 4) == (c, [4], [a(3)])


def test_exhaustive_rs_7_3() -> None:
    # every pattern of at most t = 2 errors on RS(7, 3) over GF(8), for b = 1 and b = 0
    for b in (0, 1):
        c = rs_codeword(F8, [5, 1, 6], 4, b=b)
        for nu in range(0, 3):
            for pos in itertools.combinations(range(7), nu):
                for vals in itertools.product(range(1, 8), repeat=nu):
                    r = add_errors(c, pos, vals)
                    assert pgz_decode(F8, r, 4, b=b) == (c, list(pos), list(vals))


def test_exhaustive_rs_15_9_and_bm() -> None:
    # every pattern of at most 2 errors and a sample of 3 errors on RS(15, 9), t = 3,
    # with the locator compared to Berlekamp-Massey
    rng = random.Random(9)
    c = rs_codeword(F16, [rng.randrange(16) for _ in range(9)], 6)
    patterns = [(p, v) for nu in range(3) for p in itertools.combinations(range(15), nu)
                for v in itertools.product(range(1, 16), repeat=nu)]
    for _ in range(600):
        p = tuple(sorted(rng.sample(range(15), 3)))
        patterns.append((p, tuple(rng.randrange(1, 16) for _ in range(3))))
    for pos, vals in patterns:
        r = add_errors(c, pos, vals)
        syn = syndromes(F16, r, 6)
        assert pgz_locator(F16, syn) == berlekamp_massey(F16, syn)
        assert pgz_decode(F16, r, 6) == (c, list(pos), list(vals))


def test_number_of_errors_is_the_rank() -> None:
    # M_t = V D V^T, so its rank is the number of errors when it is at most t
    rng = random.Random(1960)
    for _ in range(300):
        nsym = rng.choice((4, 6, 8, 10))
        nu = rng.randrange(0, nsym // 2 + 1)
        w = add_errors([0] * 15, rng.sample(range(15), nu), [rng.randrange(1, 16) for _ in range(nu)])
        syn = syndromes(F16, w, nsym)
        assert rank(F16, hankel(syn, nsym // 2)) == nu
        for mu in range(nu + 1, nsym // 2 + 1):
            assert solve(F16, hankel(syn, mu), syn[mu: 2 * mu]) is None


def test_random_against_bm_gf256() -> None:
    # 600 random syndrome sequences of error patterns within t: the PGZ locator is the BM locator
    rng = random.Random(1961)
    for _ in range(600):
        nsym = rng.choice((2, 4, 6, 8, 10, 12, 16))
        nu = rng.randrange(0, nsym // 2 + 1)
        w = add_errors([0] * 255, rng.sample(range(255), nu), [rng.randrange(1, 256) for _ in range(nu)])
        syn = syndromes(F256, w, nsym, b=0)
        assert pgz_locator(F256, syn) == berlekamp_massey(F256, syn)


def test_beyond_t_when_bm_is_short() -> None:
    # random syndromes (most words are beyond t): when the BM length L is at most t,
    # M_L is nonsingular and every larger M_mu is singular, so PGZ finds the same LFSR.
    # Its polynomial can have degree below L; then the root count check of line L6 fails.
    rng = random.Random(3)
    agree = short = 0
    for _ in range(600):
        nsym = rng.choice((4, 6))
        syn = [rng.randrange(8) for _ in range(nsym)]
        L, lam = bm_with_length(F8, syn)
        if L <= nsym // 2:
            got = pgz_locator(F8, syn)
            assert len(got) == L + 1 and F8.trim(got) == lam
            agree += 1
            short += len(lam) - 1 < L
    assert agree > 100 and short > 0


def test_binary_bch_15_7_and_15_5() -> None:
    # binary BCH codes: the same decoder with error values 1, every pattern up to t
    for g, t in ((0b111010001, 2), (0b10100110111, 3)):  # x^8+x^7+x^6+x^4+1 and x^10+x^8+x^5+x^4+x^2+x+1
        gl = [(g >> i) & 1 for i in range(g.bit_length())]
        c = gl + [0] * (15 - len(gl))  # g(x) itself is a codeword
        c = [c[(i - 3) % 15] for i in range(15)]  # and so is x^3 g(x) mod x^15 - 1
        assert not any(syndromes(F16, c, 2 * t))
        for nu in range(t + 1):
            for pos in itertools.combinations(range(15), nu):
                r = add_errors(c, pos, [1] * nu)
                assert pgz_decode(F16, r, 2 * t) == (c, list(pos), [1] * nu)


def test_ccsds_convention() -> None:
    # RS(255, 223) zeros beta^112 .. beta^143, beta = alpha^11, t = 16
    rng = random.Random(131)
    for _ in range(4):
        c = rs_codeword(CCSDS, [rng.randrange(256) for _ in range(223)], 32, b=112, step=11)
        nu = rng.randrange(0, 17)
        pos = sorted(rng.sample(range(255), nu))
        vals = [rng.randrange(1, 256) for _ in range(nu)]
        assert pgz_decode(CCSDS, add_errors(c, pos, vals), 32, b=112, step=11) == (c, pos, vals)


def test_failure_is_detected_or_close() -> None:
    # 3 errors on RS(7, 3): a failure, or a codeword within distance 2 of the received word
    c = rs_codeword(F8, [1, 2, 3], 4)
    failures = 0
    for pos in itertools.combinations(range(7), 3):
        for vals in itertools.product(range(1, 8), repeat=3):
            r = add_errors(c, pos, vals)
            out = pgz_decode(F8, r, 4)
            if out is None:
                failures += 1
            else:
                assert not any(syndromes(F8, out[0], 4))
                assert sum(x != y for x, y in zip(out[0], r)) <= 2
    assert failures > 0


def test_edges() -> None:
    assert pgz_decode(F16, [0] * 15, 4) == ([0] * 15, [], [])
    assert pgz_locator(F16, [0, 0, 0, 0]) == [1]
    assert rank(F16, [[0, 0], [0, 0]]) == 0
    r = [0] * 15
    r[14] = 7
    assert pgz_decode(F16, r, 2) == ([0] * 15, [14], [7])
