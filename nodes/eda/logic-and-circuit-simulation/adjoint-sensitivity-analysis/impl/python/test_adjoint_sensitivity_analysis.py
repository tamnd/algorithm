# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adjoint-sensitivity-analysis/. The authors are listed in prov/XP8WTV.jsonl.

import random
from fractions import Fraction as F

import pytest

from adjoint_sensitivity_analysis import (
    SingularMatrixError,
    node_output,
    sensitivities,
    source_current_output,
    stamp,
)
from densela import lu_factor, lu_solve, matvec, solve


def output_value(netlist, n, c):
    a, z, _ = stamp(netlist, n)
    x = solve(a, z)
    return sum(ci * xi for ci, xi in zip(c, x))


def with_parameter(netlist, k, value):
    el = list(netlist[k])
    el[-1] = value
    return netlist[:k] + [tuple(el)] + netlist[k + 1 :]


def direct_sensitivity(netlist, n, k):
    """The direct method: solve M dx = dz - dM x for one parameter, exactly."""
    if netlist[k][0] == "R":
        # dx/dR = dx/dG * dG/dR with G = 1/R, so work with a conductance.
        el = netlist[k]
        r = el[-1]
        g_net = netlist[:k] + [("G", el[1], el[2], 1 / r)] + netlist[k + 1 :]
        return [d * (-1 / (r * r)) for d in direct_sensitivity(g_net, n, k)]
    a, z, _ = stamp(netlist, n)
    x = solve(a, z)
    a1, z1, _ = stamp(with_parameter(netlist, k, netlist[k][-1] + 1), n)
    # M and z are affine in a conductance, a gain or a source value, so a unit step gives dM and dz exactly.
    da = [[u - v for u, v in zip(r1, r)] for r1, r in zip(a1, a)]
    dz = [u - v for u, v in zip(z1, z)]
    rhs = [d - m for d, m in zip(dz, matvec(da, x))]
    return solve(a, rhs)


# The circuit of the page: 6 V at node 1, 2 ohm from 1 to 2, 3 ohm from 2 to 0, 1 A into node 2.
PAGE = [("V", 1, 0, F(6)), ("R", 1, 2, F(2)), ("R", 2, 0, F(3)), ("I", 0, 2, F(1))]


def test_page_example():
    stats = {}
    [(phi, grad)] = sensitivities(PAGE, 2, [node_output(PAGE, 2, 2)], stats)
    assert phi == F(24, 5)
    # e2 = R2 (E + R1 I) / (R1 + R2); its partial derivatives by hand are
    # R2 / (R1 + R2), R2 (I R2 - E) / (R1 + R2)^2, R1 (E + R1 I) / (R1 + R2)^2 and R1 R2 / (R1 + R2).
    assert grad == [F(3, 5), F(-9, 25), F(16, 25), F(6, 5)]
    assert stats == {"factorizations": 1, "solves": 1, "transposed_solves": 1}


def test_divider_formula():
    e, r1, r2 = F(10), F(2), F(8)
    net = [("V", 1, 0, e), ("R", 1, 2, r1), ("R", 2, 0, r2)]
    [(phi, grad)] = sensitivities(net, 2, [node_output(net, 2, 2)])
    assert phi == e * r2 / (r1 + r2)
    assert grad[0] == r2 / (r1 + r2)
    assert grad[1] == -e * r2 / (r1 + r2) ** 2
    assert grad[2] == e * r1 / (r1 + r2) ** 2


def random_circuit(rng, n, exact):
    def val(lo, hi):
        if exact:
            return F(rng.randint(lo * 4, hi * 4), 4)
        return rng.uniform(lo, hi)

    net = []
    for k in range(1, n + 1):  # a spanning tree keeps every node connected to ground
        net.append(("R", k, rng.randint(0, k - 1), val(1, 5)))
    for _ in range(n):
        p, q = rng.sample(range(n + 1), 2)
        net.append(("G", p, q, val(1, 3)))
    for _ in range(2):
        p, q = rng.sample(range(n + 1), 2)
        net.append(("I", p, q, val(-2, 2)))
    net.append(("V", rng.randint(1, n), 0, val(1, 5)))
    p, q, c, d = (rng.randint(0, n) for _ in range(4))
    if p != q and c != d:
        net.append(("VCCS", p, q, c, d, val(-1, 1)))
    return net


def nonsingular_circuits(seed, count, exact):
    rng = random.Random(seed)
    out = []
    while len(out) < count:
        n = rng.randint(2, 5)
        net = random_circuit(rng, n, exact)
        try:
            lu_factor(stamp(net, n)[0])
        except SingularMatrixError:
            continue
        out.append((net, n))
    return out


def test_adjoint_equals_exact_direct_sensitivities():
    for net, n in nonsingular_circuits(7, 12, exact=True):
        outputs = [node_output(net, n, k) for k in range(1, n + 1)]
        outputs.append(source_current_output(net, n, next(k for k, el in enumerate(net) if el[0] == "V")))
        results = sensitivities(net, n, outputs)
        for k in range(len(net)):
            dx = direct_sensitivity(net, n, k)
            for c, (_, grad) in zip(outputs, results):
                assert grad[k] == sum(ci * di for ci, di in zip(c, dx))


def test_adjoint_equals_exact_difference_quotient_limit():
    # phi is a rational function of each parameter; the central difference with exact
    # fractions differs from the derivative by O(t^2), checked over three values of t.
    curved = 0
    for net, n in nonsingular_circuits(11, 4, exact=True):
        # The current of the voltage source depends on every element of these circuits.
        c = source_current_output(net, n, next(k for k, el in enumerate(net) if el[0] == "V"))
        [(_, grad)] = sensitivities(net, n, [c])
        for k in range(len(net)):
            p = net[k][-1]
            errs = []
            for t in (F(1, 10**4), F(1, 10**5), F(1, 10**6)):
                hi = output_value(with_parameter(net, k, p + t), n, c)
                lo = output_value(with_parameter(net, k, p - t), n, c)
                errs.append(abs((hi - lo) / (2 * t) - grad[k]))
            if errs[0] == 0:
                assert errs == [0, 0, 0]  # phi is affine in this parameter
            else:
                curved += 1
                assert all(90 < a / b < 110 for a, b in zip(errs, errs[1:])), errs
    assert curved >= 20


def test_adjoint_against_float_central_differences():
    for net, n in nonsingular_circuits(2024, 20, exact=False):
        outputs = [node_output(net, n, n), source_current_output(net, n, next(k for k, el in enumerate(net) if el[0] == "V"))]
        for c, (phi, grad) in zip(outputs, sensitivities(net, n, outputs)):
            check_against_differences(net, n, c, phi, grad)


def check_against_differences(net, n, c, phi, grad):
    assert abs(phi - output_value(net, n, c)) < 1e-12 * max(1.0, abs(phi))
    for k in range(len(net)):
        p = net[k][-1]
        t = 1e-6 * max(1.0, abs(p))
        hi = output_value(with_parameter(net, k, p + t), n, c)
        lo = output_value(with_parameter(net, k, p - t), n, c)
        assert abs((hi - lo) / (2 * t) - grad[k]) < 1e-6 * max(1.0, abs(grad[k]))


def test_one_factorization_and_one_adjoint_solve_per_output():
    net, n = nonsingular_circuits(5, 1, exact=True)[0]
    outputs = [node_output(net, n, k) for k in range(1, n + 1)]
    stats = {}
    results = sensitivities(net, n, outputs, stats)
    assert stats == {"factorizations": 1, "solves": 1, "transposed_solves": n}
    assert all(len(grad) == len(net) for _, grad in results)


def test_reciprocal_circuit_has_adjoint_equal_to_a_forward_solve():
    # Without controlled sources M is symmetric, so the adjoint circuit is the circuit itself.
    net = [("V", 1, 0, F(6)), ("R", 1, 2, F(2)), ("R", 2, 3, F(3)), ("R", 3, 0, F(1)), ("R", 2, 0, F(4))]
    a, _, _ = stamp(net, 3)
    assert all(a[i][j] == a[j][i] for i in range(4) for j in range(4))
    c = node_output(net, 3, 3)
    lam = lu_solve(lu_factor(a), c)
    [(_, grad)] = sensitivities(net, 3, [c])
    assert grad[0] == lam[3]  # d e3 / dE is the adjoint value at the source row


def test_singular_circuit_is_reported():
    net = [("V", 1, 0, F(1)), ("V", 1, 0, F(1)), ("R", 1, 0, F(1))]  # a loop of voltage sources
    with pytest.raises(SingularMatrixError):
        sensitivities(net, 1, [[1, 0, 0]])
