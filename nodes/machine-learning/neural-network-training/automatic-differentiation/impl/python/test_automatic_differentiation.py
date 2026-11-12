# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/automatic-differentiation/. The authors are listed in prov/9QSEWQ.jsonl.

import math
import random

from automatic_differentiation import (Dual, Tape, Var, cos, exp, grad, grad_forward, jacobian_forward,
                                       jacobian_reverse, jvp, log, reverse_sweep, sin, tanh, vjp)


def baydin(x):
    return log(x[0]) + x[0] * x[1] - sin(x[1])


def program_a(x):
    return exp(x[0] * x[1]) / (1 + x[2] * x[2]) + tanh(x[0] - x[2]) * cos(x[1])


def program_b(x):
    s = x[0]
    for i in range(1, len(x)):
        s = sin(s * x[i]) + x[i] / (2 + cos(s))
    return s * s


def vector_program(x):
    return [x[0] * x[1] * x[2], sin(x[0]) + exp(x[2]), x[1] / (1 + x[0] * x[0])]


def central(f, x, h=1e-5):
    g = []
    for i in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[i] += h
        xm[i] -= h
        g.append((f(xp) - f(xm)) / (2 * h))
    return g


def close(a, b, rel=1e-7, abs_=1e-9):
    return all(math.isclose(p, q, rel_tol=rel, abs_tol=abs_) for p, q in zip(a, b))


def test_worked_example():
    val, g, n = vjp(baydin, [2.0, 5.0], [1.0])
    assert math.isclose(val[0], math.log(2) + 10 - math.sin(5))
    assert math.isclose(g[0], 5.5)
    assert math.isclose(g[1], 2 - math.cos(5))
    # two inputs and five operations: log, *, sin, +, -
    assert n == 7


def test_dual_rule():
    z = Dual(3.0, 2.0) * Dual(5.0, 7.0)
    assert (z.val, z.dot) == (15.0, 3.0 * 7.0 + 2.0 * 5.0)
    q = Dual(1.0, 1.0) / Dual(2.0, 0.0)
    assert (q.val, q.dot) == (0.5, 0.5)


def test_forward_reverse_and_differences_agree():
    rng = random.Random(1)
    for _ in range(300):
        x = [rng.uniform(-1.5, 1.5) for _ in range(3)]
        for f in (program_a, program_b):
            gr = grad(f, x)
            gf = grad_forward(f, x)
            assert close(gr, gf, rel=1e-12, abs_=1e-12)
            assert close(gr, central(f, x), rel=1e-6, abs_=1e-7)


def test_longer_input():
    rng = random.Random(2)
    for _ in range(200):
        x = [rng.uniform(-1, 1) for _ in range(6)]
        assert close(grad(program_b, x), grad_forward(program_b, x), rel=1e-12, abs_=1e-12)


def test_jacobians_agree():
    rng = random.Random(3)
    for _ in range(200):
        x = [rng.uniform(-1, 1) for _ in range(3)]
        jf = jacobian_forward(vector_program, x)
        jr = jacobian_reverse(vector_program, x, 3)
        for rf, rr in zip(jf, jr):
            assert close(rf, rr, rel=1e-12, abs_=1e-12)


def test_jvp_and_vjp_are_adjoint():
    # u^T (J v) = (u^T J) v for any u and v
    rng = random.Random(4)
    for _ in range(200):
        x = [rng.uniform(-1, 1) for _ in range(3)]
        v = [rng.uniform(-1, 1) for _ in range(3)]
        u = [rng.uniform(-1, 1) for _ in range(3)]
        _, jv = jvp(vector_program, x, v)
        _, ut_j, _ = vjp(vector_program, x, u)
        lhs = sum(a * b for a, b in zip(u, jv))
        rhs = sum(a * b for a, b in zip(ut_j, v))
        assert math.isclose(lhs, rhs, rel_tol=1e-12, abs_tol=1e-12)


def test_reverse_sweep_cost_is_linear_in_tape():
    # each entry has at most two parents, so the sweep does at most 2 multiply-adds per entry
    tape = Tape()
    xs = [Var(tape, 0.1 * (i + 1)) for i in range(50)]
    program_b(xs)
    madds = sum(len(p) for p in tape.parents)
    assert madds <= 2 * len(tape)
    adj = reverse_sweep(tape, {len(tape) - 1: 1.0})
    assert len(adj) == len(tape)


def test_shared_subexpression():
    # y = x * x uses x twice; the adjoints of both uses add up
    assert grad(lambda x: x[0] * x[0], [3.0]) == [6.0]
    assert grad(lambda x: x[0] - x[0], [3.0]) == [0.0]
