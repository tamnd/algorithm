# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/solovay-kitaev-theorem/. The authors are listed in prov/ZW8FD1.jsonl.
"""Tests of the Solovay-Kitaev algorithm over the base set {H, T, T^dagger}.

Setup of the main test: the net is every word of length at most 14 (3404 distinct gates modulo
phase), the targets are 10 Haar-random elements of SU(2) from random.Random(2024), and the
recursion depth goes from 0 to 4. The depth is limited by the run time, not by the method: depth k
makes 3^k net lookups per target and gives words about 5^k times longer, so depth 4 (81 lookups,
words of up to about 7300 gates) is the last depth that keeps this file near 1 s of CPU time.
"""

import cmath
import itertools
import math
import random

from qsim import H, T, close, dagger, matmul
from solovay_kitaev_theorem import (GATES, _key, build_net, dist, group_commutator, inverse_word, qconj, qmul,
                                    random_su2, rotation, solovay_kitaev, to_matrix, word_quat)


def op_norm(a) -> float:
    """The largest singular value of a 2 x 2 matrix."""
    f = sum(abs(x) ** 2 for row in a for x in row)
    det = abs(a[0][0] * a[1][1] - a[0][1] * a[1][0])
    return math.sqrt((f + math.sqrt(max(0.0, f * f - 4 * det * det))) / 2)


def same_gate(p, q, tol: float = 1e-9) -> bool:
    """Equal quaternions up to sign, compared entry by entry. (dist takes a square root, so it
    turns a rounding error of 1e-13 into 1e-6 and is not a good equality test.)"""
    return min(max(abs(x - y) for x, y in zip(p, q)), max(abs(x + y) for x, y in zip(p, q))) < tol


def equal_up_to_phase(a, b) -> bool:
    k = max(((i, j) for i in range(2) for j in range(2)), key=lambda ij: abs(b[ij[0]][ij[1]]))
    ph = a[k[0]][k[1]] / b[k[0]][k[1]]
    return abs(abs(ph) - 1) < 1e-12 and close(a, [[ph * x for x in row] for row in b])


def test_base_gates_and_quaternion_product() -> None:
    tdg = dagger(T)
    for name, m in (("H", H), ("T", T), ("Tdg", tdg)):
        q = GATES[name]
        assert abs(sum(x * x for x in q) - 1) < 1e-15
        assert equal_up_to_phase(to_matrix(q), m)
    rng = random.Random(1)
    for _ in range(50):
        p, q = random_su2(rng), random_su2(rng)
        assert close(to_matrix(qmul(p, q)), matmul(to_matrix(p), to_matrix(q)))
        assert close(to_matrix(qconj(p)), dagger(to_matrix(p)))
    w = ["H", "T", "T", "H", "Tdg"]
    assert same_gate(qmul(word_quat(w), word_quat(inverse_word(w))), (1.0, 0.0, 0.0, 0.0))


def test_distance_is_the_phase_invariant_operator_norm() -> None:
    rng = random.Random(2)
    for _ in range(30):
        p, q = random_su2(rng), random_su2(rng)
        a, b = to_matrix(p), to_matrix(q)
        d = dist(p, q)
        # for SU(2) the best phase is +1 or -1
        best = min(op_norm([[x - y for x, y in zip(r, s)] for r, s in zip(a, b)]),
                   op_norm([[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]))
        assert abs(d - best) < 1e-7
        tr = a[0][0].conjugate() * b[0][0] + a[1][0].conjugate() * b[1][0] \
            + a[0][1].conjugate() * b[0][1] + a[1][1].conjugate() * b[1][1]
        assert abs(d - math.sqrt(max(0.0, 2 - abs(tr)))) < 1e-7
        for k in range(360):  # no other phase does better
            ph = cmath.exp(1j * math.pi * k / 180)
            assert op_norm([[x - ph * y for x, y in zip(r, s)] for r, s in zip(a, b)]) > d - 1e-7


def test_net_against_brute_force_enumeration() -> None:
    for length in range(7):
        keys = {_key(word_quat(list(w))) for k in range(length + 1) for w in itertools.product(GATES, repeat=k)}
        net = build_net(length)
        assert len(net) == len(keys) == len({_key(q) for q, _ in net})
        for q, w in net:
            assert len(w) <= length and same_gate(q, word_quat(w))
    # the gates H and T generate an infinite group, so the net keeps growing
    sizes = [len(build_net(k)) for k in range(0, 15, 2)]
    assert all(a < b for a, b in zip(sizes, sizes[1:]))


def test_balanced_group_commutator() -> None:
    rng = random.Random(3)
    for _ in range(200):
        n = [rng.gauss(0, 1) for _ in range(3)]
        s = math.sqrt(sum(x * x for x in n))
        theta = rng.uniform(1e-6, 0.5)
        u = rotation((n[0] / s, n[1] / s, n[2] / s), theta)
        v, w = group_commutator(u)
        c = qmul(qmul(v, w), qmul(qconj(v), qconj(w)))
        assert dist(c, u) < 1e-7
        one = (1.0, 0.0, 0.0, 0.0)
        # V and W are rotations by the same angle phi, about sqrt(theta), so d(V, I) is of
        # the order of d(U, I)^(1/2)
        assert abs(dist(v, one) - dist(w, one)) < 1e-12
        assert dist(v, one) <= math.sqrt(dist(u, one))


def test_error_falls_with_depth() -> None:
    net = build_net(14)
    assert len(net) == 3404
    rng = random.Random(2024)
    targets = [random_su2(rng) for _ in range(10)]
    worst = []
    for depth in range(5):
        errs = []
        for u in targets:
            approx, word = solovay_kitaev(u, depth, net)
            assert set(word) <= set(GATES)
            assert len(word) <= 14 * 5 ** depth
            assert same_gate(approx, word_quat(word))  # the word really is the claimed product
            errs.append(dist(u, approx))
        worst.append(max(errs))
    assert all(b < a for a, b in zip(worst, worst[1:]))
    assert worst[0] < 0.1 and worst[4] < 5e-4
    # each level gives at most about 8 eps^(3/2) on this run; the constant 8 is empirical
    assert all(b <= 8 * a ** 1.5 for a, b in zip(worst, worst[1:]))
