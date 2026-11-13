# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quantum-elliptic-curve-discrete-log/. The authors are listed in prov/RB6N46.jsonl.

import itertools
import math
import random

from qsim import basis_state, get_reg, registers, set_reg
from quantum_elliptic_curve_discrete_log import (
    O,
    Curve,
    circuit_distribution,
    closed_form_distribution,
    controlled_add,
    group_operation,
    merge,
    power_of_two_success,
    quantum_ecdlp,
    rounding_candidate,
    solve_congruence,
    width,
)

TOL = 1e-9

# (p, A, B, generator, order): cyclic groups E(F_p) of 6, 7, 9 and 11 points; every circuit has at most 12 qubits
CURVES = [(7, 1, 6, (1, 1), 11), (5, 2, 1, (0, 1), 7), (7, 1, 3, (4, 1), 6), (5, 1, 1, (0, 1), 9)]


def brute_log(E, P, Q, r):
    R = O
    for x in range(r):
        if R == Q:
            return x
        R = E.add(R, P)
    return None


def bsgs(E, P, Q, r):
    """Baby-step giant-step on the curve, the classical reference method."""
    m = math.isqrt(r - 1) + 1
    table, R = {}, O
    for j in range(m):
        table.setdefault(R, j)
        R = E.add(R, P)
    step = E.neg(E.mul(m, P))
    R = Q
    for i in range(m + 1):
        if R in table:
            return (i * m + table[R]) % r
        R = E.add(R, step)
    return None


def test_group_law():
    for p, A, B, P, r in CURVES:
        E = Curve(p, A, B)
        pts = E.points()
        assert len(pts) == r and abs(r - (p + 1)) <= 2 * math.isqrt(p) + 1  # the Hasse bound
        for U, V, W in itertools.product(pts, repeat=3):
            assert E.add(E.add(U, V), W) == E.add(U, E.add(V, W))
        for U in pts:
            assert E.add(U, E.neg(U)) is O
        assert E.order(P) == r and len({E.mul(k, P) for k in range(r)}) == r


def test_encoding_is_unique_and_fits():
    for p, A, B, _, _ in CURVES:
        E = Curve(p, A, B)
        codes = [E.encode(U) for U in E.points()]
        assert len(set(codes)) == len(codes) and max(codes) < 1 << E.code_bits()
        for U in E.points():
            assert E.decode(E.encode(U)) == U


def test_controlled_add_is_point_addition():
    E = Curve(7, 1, 6)
    ctrl, acc = registers(1, E.code_bits())
    for C in E.points():
        for U in E.points():
            for c in (0, 1):
                x = set_reg(set_reg(0, ctrl, c), acc, E.encode(U))
                out = controlled_add(basis_state(5, x), E, ctrl[0], acc, C)
                y = max(range(32), key=lambda i: abs(out[i]))
                assert abs(out[y] - 1) < TOL
                assert E.decode(get_reg(y, acc)) == (E.add(U, C) if c else U)


def test_group_operation_on_basis_states():
    # |a>|b>|O> -> |a>|b>|aP + bQ> for every a and b, with Q = 3P on the curve with 7 points
    E, P, r = Curve(5, 2, 1), (0, 1), 7
    Q = E.mul(3, P)
    k = width(r)
    ra, rb, acc = registers(k, k, E.code_bits())
    n = 2 * k + len(acc)
    for a in range(1 << k):
        for b in range(1 << k):
            x = set_reg(set_reg(set_reg(0, ra, a), rb, b), acc, E.encode(O))
            out = group_operation(basis_state(n, x), E, P, Q, ra, rb, acc)
            y = max(range(1 << n), key=lambda i: abs(out[i]))
            assert get_reg(y, ra) == a and get_reg(y, rb) == b
            assert E.decode(get_reg(y, acc)) == E.add(E.mul(a, P), E.mul(b, Q))


def test_distribution_matches_closed_form():
    for p, A, B, P, r in CURVES:
        E = Curve(p, A, B)
        for x in range(r):
            got = circuit_distribution(E, P, E.mul(x, P), r)
            want = closed_form_distribution(r, x)
            for key in set(got) | set(want):
                assert abs(got.get(key, 0.0) - want.get(key, 0.0)) < TOL


def test_post_processing_against_brute_force():
    for r in range(1, 31):
        for c in range(r):
            for d in range(r):
                want = {x for x in range(r) if (c * x - d) % r == 0}
                sol = solve_congruence(c, d, r)
                if not want:
                    assert sol is None
                    continue
                x0, m = sol
                assert {x for x in range(r) if x % m == x0} == want
    for m1, m2 in itertools.product(range(1, 10), repeat=2):
        for x1, x2 in itertools.product(range(m1), range(m2)):
            l = m1 * m2 // math.gcd(m1, m2)
            want = [x for x in range(l) if x % m1 == x1 and x % m2 == x2]
            assert merge(x1, m1, x2, m2) == ((want[0], l) if want else None)


def test_quantum_ecdlp_matches_brute_force_and_bsgs():
    rng = random.Random(7)
    for p, A, B, P, r in CURVES:
        E = Curve(p, A, B)
        for x in range(r):
            Q = E.mul(x, P)
            got, runs = quantum_ecdlp(E, P, Q, r, rng)
            assert got == x == brute_log(E, P, Q, r) == bsgs(E, P, Q, r)
            assert runs <= 20


def test_one_run_success_for_prime_order():
    # with the exact transform and prime r, one run fixes x unless c = 0
    E, P, r = Curve(7, 1, 6), (1, 1), 11
    for x in range(r):
        dist = circuit_distribution(E, P, E.mul(x, P), r)
        ok = sum(pr for (c, d), pr in dist.items() if solve_congruence(c, d, r) == (x, r))
        assert abs(ok - (r - 1) / r) < TOL


def test_power_of_two_form():
    # 4-qubit registers with the transform of Z_16: the rounding candidate is right with probability above 0.6
    for (p, A, B, P, r), m in [((7, 1, 6, (1, 1), 11), 4), ((5, 2, 1, (0, 1), 7), 4)]:
        E = Curve(p, A, B)
        for x in range(r):
            Q = E.mul(x, P)
            dist = circuit_distribution(E, P, Q, r, fourier_size=1 << m)
            assert abs(sum(dist.values()) - 1) < TOL
            pr = power_of_two_success(E, P, Q, r, x, m)
            checked = sum(v for (c, d), v in dist.items() if rounding_candidate(c, d, r, 1 << m) is not None and E.mul(rounding_candidate(c, d, r, 1 << m), P) == Q)
            assert abs(pr - checked) < TOL
            assert 0.6 < pr < 0.91
