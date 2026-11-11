# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zk-snark/. The authors are listed in prov/QH7EWC.jsonl.
# There are no official test vectors for the R1CS to QAP step. The tests
# cross-check the interpolation over the rationals with Fraction, and compare
# with the decimal values printed in Buterin's 2016 introduction (for example
# h = [-3.666, 17.055, -3.444]). Only the arithmetization is tested; no
# pairing-based SNARK is implemented.

import random
from fractions import Fraction

from zk_snark import (
    A_ROWS,
    B_ROWS,
    C_ROWS,
    QAP,
    R,
    VARIABLES,
    WITNESS,
    lagrange,
    pdivmod,
    peval,
    pmul,
    psub,
    r1cs_satisfied,
    vanishing,
)


def is_probable_prime(n, bases=(2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)):
    d, s = n - 1, 0
    while d % 2 == 0:
        d, s = d // 2, s + 1
    for b in bases:
        x = pow(b, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def to_field(fr):
    return fr.numerator % R * pow(fr.denominator, -1, R) % R


def lagrange_rational(ys):
    m = len(ys)
    out = [Fraction(0)] * m
    for i, yi in enumerate(ys):
        basis, den = [Fraction(1)], Fraction(1)
        for j in range(m):
            if j != i:
                nb = [Fraction(0)] * (len(basis) + 1)
                for k, a in enumerate(basis):
                    nb[k] -= a * (j + 1)
                    nb[k + 1] += a
                basis, den = nb, den * (i - j)
        for k in range(m):
            out[k] += yi * basis[k] / den
    return out


def test_bn254_scalar_field():
    assert R.bit_length() == 254
    assert is_probable_prime(R)
    assert (R - 1) % 2**28 == 0      # roots of unity of order 2^28 exist, for FFTs


def test_r1cs_accepts_the_witness_only():
    assert len(VARIABLES) == len(WITNESS) == 6
    assert r1cs_satisfied(A_ROWS, B_ROWS, C_ROWS, WITNESS)
    for i in range(1, 6):
        bad = list(WITNESS)
        bad[i] += 1
        assert not r1cs_satisfied(A_ROWS, B_ROWS, C_ROWS, bad)
    # x = 4 is consistent with the constraints only for out = 73, not 35.
    assert r1cs_satisfied(A_ROWS, B_ROWS, C_ROWS, [1, 4, 73, 16, 64, 68])


def test_interpolation_matches_rationals():
    for rows in (A_ROWS, B_ROWS, C_ROWS):
        for i in range(6):
            col = [row[i] for row in rows]
            got = lagrange(col)
            want = [to_field(c) for c in lagrange_rational(col)]
            while want and want[-1] == 0:
                want.pop()
            assert got == want
            assert [peval(got, j) for j in range(1, 5)] == [c % R for c in col]


def test_published_polynomials():
    # A_one = -5 + 55/6 X - 5 X^2 + 5/6 X^3, as in Buterin's article.
    want = [Fraction(-5), Fraction(55, 6), Fraction(-5), Fraction(5, 6)]
    assert lagrange([row[0] for row in A_ROWS]) == [to_field(c) for c in want]
    h, rem = QAP(A_ROWS, B_ROWS, C_ROWS).quotient(WITNESS)
    assert rem == []
    assert h == [to_field(c) for c in (Fraction(-11, 3), Fraction(307, 18), Fraction(-31, 9))]
    assert vanishing(4) == [24, R - 50, 35, R - 10, 1]


def test_divisibility_is_equivalent_to_satisfaction():
    qap = QAP(A_ROWS, B_ROWS, C_ROWS)
    _, rem = qap.quotient(WITNESS)
    assert rem == []
    rng = random.Random(1)
    for _ in range(20):
        bad = [1] + [rng.randrange(R) for _ in range(5)]
        assert not r1cs_satisfied(A_ROWS, B_ROWS, C_ROWS, bad)
        _, rem = qap.quotient(bad)
        assert rem != []
    # At each point j the polynomial P = A B - C takes the value of the
    # error of constraint j, which is zero exactly when the constraint holds.
    bad = [1, 3, 36, 9, 27, 30]
    *_, p = qap.polys(bad)
    assert [peval(p, j) for j in range(1, 5)] == [0, 0, 0, R - 1]


def test_random_point_check():
    qap = QAP(A_ROWS, B_ROWS, C_ROWS)
    rng = random.Random(2)
    h, _ = qap.quotient(WITNESS)
    for _ in range(20):
        assert qap.check_at(WITNESS, h, rng.randrange(R))
    # A cheater with a bad witness sends the best quotient it has; the check
    # fails at a random point except with probability deg(rem) / R < 2^-250.
    bad = [1, 3, 36, 9, 27, 30]
    h_bad, rem = qap.quotient(bad)
    assert len(rem) - 1 == 3
    for _ in range(20):
        assert not qap.check_at(bad, h_bad, rng.randrange(R))


def test_schwartz_zippel_count_in_a_small_field():
    # Over GF(97) count the points where the check passes for the bad witness:
    # they are the roots of the remainder, at most its degree 3.
    p = 97
    qap = QAP(A_ROWS, B_ROWS, C_ROWS, mod=p)
    bad = [1, 3, 36, 9, 27, 30]
    h_bad, rem = qap.quotient(bad)
    passing = [tau for tau in range(p) if qap.check_at(bad, h_bad, tau)]
    roots = [tau for tau in range(p) if peval(rem, tau, p) == 0]
    assert passing == roots and len(passing) <= 3
    # The honest witness passes at every point.
    h, _ = qap.quotient(WITNESS)
    assert all(qap.check_at(WITNESS, h, tau) for tau in range(p))


def test_polynomial_division():
    a = [5, 0, 3, 1]
    b = [R - 2, 1]
    q, r = pdivmod(a, b)
    assert psub(a, pmul(q, b)) == r and len(r) <= 1
