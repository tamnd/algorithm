# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parareal-algorithm/. The authors are listed in prov/GD4NTE.jsonl.

import math
from fractions import Fraction as F

import pytest

from parareal_algorithm import parareal, rk_propagator, sequential_fine


def _err(values, ref):
    def d(u, v):
        if isinstance(u, list):
            return max(abs(a - b) for a, b in zip(u, v))
        return abs(u - v)
    return max(d(u, v) for u, v in zip(values, ref))


def test_exact_after_k_iterations_with_fractions():
    f = lambda t, y: -y + t
    G = rk_propagator(f, 1, "euler")
    Fp = rk_propagator(f, 4, "euler")
    N = 6
    ref = sequential_fine(Fp, F(0), F(1), F(3), N)
    r = parareal(G, Fp, F(0), F(1), F(3), N, keep_history=True)
    for k, U in enumerate(r.history):
        assert U[:k + 1] == ref[:k + 1]           # the first k + 1 values are exact
        if k < N - 1:
            assert U[k + 2:] != ref[k + 2:]
    assert r.values == ref and r.iterations == N and r.converged


def test_linear_error_bound():
    lam, T, N = -1.0, 10.0, 20
    dT = T / N
    G = lambda ta, tb, y: y / (1 - lam * (tb - ta))           # backward Euler
    Fx = lambda ta, tb, y: y * math.exp(lam * (tb - ta))      # exact
    ref = sequential_fine(Fx, 0.0, 1.0, T, N)
    r = parareal(G, Fx, 0.0, 1.0, T, N, max_iter=8, keep_history=True)
    alpha = abs(math.exp(lam * dT) - 1 / (1 - lam * dT))
    M = max(abs(u - v) for u, v in zip(r.history[0], ref))
    for k, U in enumerate(r.history):
        for n in range(N + 1):
            assert abs(U[n] - ref[n]) <= M * alpha ** k * math.comb(n, k) + 1e-15


def test_fast_convergence_on_decay():
    f = lambda t, y: -y
    G = lambda ta, tb, y: y / (1 + (tb - ta))
    Fp = rk_propagator(f, 50)
    ref = sequential_fine(Fp, 0.0, 1.0, 10.0, 20)
    r = parareal(G, Fp, 0.0, 1.0, 10.0, 20, max_iter=8, keep_history=True)
    errs = [_err(U, ref) for U in r.history]
    assert abs(errs[0] - 7.66e-2) < 1e-4
    assert all(errs[i + 1] < errs[i] / 5 for i in range(8))
    assert r.fine_calls == 8 * 20 and r.coarse_calls == 9 * 20


def test_nonlinear_vector_and_tolerance_stop():
    br = lambda t, y: [1 + y[0] * y[0] * y[1] - 4 * y[0], 3 * y[0] - y[0] * y[0] * y[1]]
    G = rk_propagator(br, 4)
    Fp = rk_propagator(br, 100)
    ref = sequential_fine(Fp, 0.0, [1.5, 3.0], 20.0, 20)
    r = parareal(G, Fp, 0.0, [1.5, 3.0], 20.0, 20, tol=1e-10)
    assert r.converged and r.iterations <= 8
    assert _err(r.values, ref) < 1e-9


def test_stiff_needs_stable_coarse_propagator():
    fs = lambda t, y: -1000 * (y - math.cos(t))
    be = lambda ta, tb, y: (y + (tb - ta) * 1000 * math.cos(tb)) / (1 + 1000 * (tb - ta))
    Fp = rk_propagator(fs, 1000)
    ref = sequential_fine(Fp, 0.0, 0.0, 1.0, 10)
    r = parareal(be, Fp, 0.0, 0.0, 1.0, 10, max_iter=5)
    assert _err(r.values, ref) < 1e-10
    eu = rk_propagator(fs, 1, "euler")                        # factor 1 - 100 per slice
    r = parareal(eu, Fp, 0.0, 0.0, 1.0, 10, max_iter=3)
    assert _err(r.values, ref) > 1e10


def test_oscillator_over_long_time_converges_slowly():
    osc = lambda t, y: [y[1], -y[0]]
    G = rk_propagator(osc, 1)
    Fp = rk_propagator(osc, 100)
    ref = sequential_fine(Fp, 0.0, [1.0, 0.0], 100.0, 50)
    r = parareal(G, Fp, 0.0, [1.0, 0.0], 100.0, 50, max_iter=5)
    assert _err(r.values, ref) > 0.5


def test_edge_cases():
    f = lambda t, y: y
    G = rk_propagator(f, 1, "euler")
    Fp = rk_propagator(f, 8, "euler")
    r = parareal(G, Fp, 0.0, 1.0, 0.0, 4)
    assert r.values == [1.0] and r.iterations == 0 and r.fine_calls == 0
    r = parareal(G, Fp, F(0), F(1), F(1), 1)
    assert r.values[-1] == F(9, 8) ** 8 and r.iterations == 1
    with pytest.raises(ValueError):
        parareal(G, Fp, 0.0, 1.0, 1.0, 0)
    with pytest.raises(ValueError):
        parareal(G, Fp, 1.0, 1.0, 0.0, 2)
    with pytest.raises(ValueError):
        rk_propagator(f, 0)
    with pytest.raises(ValueError):
        rk_propagator(f, 1, "rk2")
