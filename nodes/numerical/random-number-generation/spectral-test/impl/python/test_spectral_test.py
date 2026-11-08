# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-test/. The authors are listed in prov/81HMHG.jsonl.

from itertools import product
from math import isqrt

from spectral_test import dual_basis, gauss_reduce_nu2, lll_reduce, shortest_vector, spectral_test


def _brute_nu2(a: int, m: int, t: int) -> int:
    # A shortest dual vector has squared length <= gamma_t m^(2/t) <= 2m (Hermite),
    # so its coordinates lie in [-isqrt(2m), isqrt(2m)].
    k = isqrt(2 * m)
    best = m * m
    for s in product(range(-k, k + 1), repeat=t):
        if any(s):
            if sum(si * pow(a, i, m) for i, si in enumerate(s)) % m == 0:
                best = min(best, sum(si * si for si in s))
    return best


def test_matches_brute_force_small_moduli() -> None:
    for m in (31, 64, 101):
        for a in range(2, m):
            r = spectral_test(a, m, 3)
            assert r[2][0] == _brute_nu2(a, m, 2) == gauss_reduce_nu2(a, m)
    for m, a in ((101, 12), (101, 37), (128, 5), (128, 77), (97, 23)):
        assert spectral_test(a, m, 3)[3][0] == _brute_nu2(a, m, 3)


def test_returned_vector_is_in_the_dual_lattice() -> None:
    a, m = 48271, 2**31 - 1
    for t, (nu2, s, _) in spectral_test(a, m, 6).items():
        assert len(s) == t and sum(x * x for x in s) == nu2
        assert sum(si * pow(a, i, m) for i, si in enumerate(s)) % m == 0


def test_randu() -> None:
    # RANDU: a = 65539 = 2^16 + 3, m = 2^31. Since a^2 = 6a - 9 mod 2^31, the vector
    # (9, -6, 1) is in L*_3: nu_3^2 = 118, so the triples lie on planes 1/sqrt(118) apart.
    r = spectral_test(65539, 2**31, 3)
    assert r[3][0] == 118
    assert sorted(abs(x) for x in r[3][1]) == [1, 6, 9]
    assert r[3][2] < 0.0001  # mu_3: far below Knuth's threshold 0.1


def test_hermite_bound() -> None:
    # nu_t^2 <= gamma_t m^(2/t) with gamma_t^t = 4/3, 2, 4, 8, 64/3 for t = 2..6.
    gamma_t = {2: (4 / 3) ** (1 / 2), 3: 2 ** (1 / 3), 4: 4 ** (1 / 4), 5: 8 ** (1 / 5), 6: (64 / 3) ** (1 / 6)}
    for a, m in ((16807, 2**31 - 1), (48271, 2**31 - 1), (69069, 2**32), (1103515245, 2**31)):
        for t, (nu2, _, mu) in spectral_test(a, m, 6).items():
            assert nu2 <= gamma_t[t] * m ** (2 / t) * (1 + 1e-12)
            assert mu > 0


def test_minimal_standard_multipliers() -> None:
    # Both pass Knuth's criterion mu_t >= 0.1 for t = 2..6; 48271 is the better in t = 2.
    r1, r2 = spectral_test(16807, 2**31 - 1), spectral_test(48271, 2**31 - 1)
    assert all(r1[t][2] >= 0.1 and r2[t][2] >= 0.1 for t in range(2, 7))
    assert r2[2][0] > r1[2][0]


def test_lll_keeps_the_lattice() -> None:
    b = dual_basis(16807, 2**31 - 1, 4)
    r = lll_reduce(b)
    # Same lattice: both bases have the same determinant m, and every reduced row is a dual vector.
    for row in r:
        assert sum(si * pow(16807, i, 2**31 - 1) for i, si in enumerate(row)) % (2**31 - 1) == 0

    def det(mat):
        if len(mat) == 1:
            return mat[0][0]
        return sum((-1) ** j * mat[0][j] * det([row[:j] + row[j + 1 :] for row in mat[1:]]) for j in range(len(mat)))

    assert abs(det(r)) == abs(det(b)) == 2**31 - 1


def test_shortest_vector_small_lattice() -> None:
    assert shortest_vector([[1, 0], [0, 1]])[0] == 1
    assert shortest_vector([[3, 1], [1, 3]])[0] == 8
