# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-timing-analysis/. The authors are listed in prov/8PGXDW.jsonl.

import random

import pytest

from iterated_timing_analysis import (
    Circuit,
    NonConvergence,
    backward_euler_newton,
    ita,
    jacobian_rho,
    mos_current,
    node_row,
    one_sweep_simulation,
    relax_time_point,
    sweep,
)

# Level-1 parameters. K (transconductance), VT (threshold) and LAM (channel-length
# modulation) are fitted model parameters; these are typical teaching values.
VDD, K, VT, LAM = 1.8, 200e-6, 0.5, 0.05


def ramp(t0, t1):
    return lambda t: 0.0 if t <= t0 else (VDD if t >= t1 else VDD * (t - t0) / (t1 - t0))


def chain(stages, cl=10e-15, cm=2e-15):
    """Inverter chain: node 0 ground, 1 supply, 2 input ramp, 3.. outputs.

    Each output has a load cl to ground and a gate-drain (Miller) capacitance cm
    to its input, which couples neighbouring nodes in both directions.
    """
    n = 3 + stages
    ckt = Circuit(n, {0: lambda t: 0.0, 1: lambda t: VDD, 2: ramp(0.1e-9, 0.15e-9)})
    prev = 2
    for s in range(stages):
        out = 3 + s
        ckt.mos("n", out, prev, 0, K, VT, LAM)
        ckt.mos("p", out, prev, 1, K, VT, LAM)
        ckt.cap(out, 0, cl)
        ckt.cap(out, prev, cm)
        prev = out
    v0 = [0.0] * n
    for s in range(stages):
        v0[3 + s] = VDD if s % 2 == 0 else 0.0
    return ckt, v0


def maxdiff(a, b, nodes):
    return max(abs(x[i] - y[i]) for (_, x), (_, y) in zip(a, b) for i in nodes)


def crossing(w, i, level=0.9):
    for (ta, xa), (tb, xb) in zip(w, w[1:]):
        if (xa[i] - level) * (xb[i] - level) <= 0 and xa[i] != xb[i]:
            return ta + (level - xa[i]) / (xb[i] - xa[i]) * (tb - ta)
    return None


def test_mos_model_values_and_partials():
    # saturation by hand: vgs = 1.8, vds = 1.8
    i, gd, gg, gs = mos_current("n", K, VT, LAM, 1.8, 1.8, 0.0)
    assert abs(i - K / 2 * 1.3**2 * (1 + LAM * 1.8)) < 1e-18
    # linear region by hand: vgs = 1.8, vds = 0.3
    i, _, _, _ = mos_current("n", K, VT, LAM, 0.3, 1.8, 0.0)
    assert abs(i - K * (1.3 * 0.3 - 0.045) * (1 + LAM * 0.3)) < 1e-18
    # p device: source at VDD, gate at 0, drain at 0: current flows from s to d
    i, _, _, _ = mos_current("p", K, VT, LAM, 0.0, 0.0, 1.8)
    assert abs(i + K / 2 * 1.3**2 * (1 + LAM * 1.8)) < 1e-18
    rng = random.Random(61)
    eps = 1e-7
    for _ in range(300):
        kind = rng.choice("np")
        vd, vg, vs = (rng.uniform(-0.2, 2.0) for _ in range(3))
        i, gd, gg, gs = mos_current(kind, K, VT, LAM, vd, vg, vs)
        for k, g in enumerate((gd, gg, gs)):
            up = [vd, vg, vs]
            dn = [vd, vg, vs]
            up[k] += eps
            dn[k] -= eps
            fd = (mos_current(kind, K, VT, LAM, *up)[0] - mos_current(kind, K, VT, LAM, *dn)[0]) / (2 * eps)
            assert abs(fd - g) < 1e-6 * K + 1e-3 * abs(g)


def random_rc(rng, n):
    ckt = Circuit(n + 1, {0: lambda t: 0.0})
    for i in range(1, n + 1):
        ckt.cap(i, 0, rng.uniform(0.5, 1.5))
        ckt.res(i, 0, rng.uniform(0.1, 1.0))
    for _ in range(2 * n):
        a, b = rng.sample(range(1, n + 1), 2)
        ckt.res(a, b, rng.uniform(0.5, 3.0))
        ckt.cap(a, b, rng.uniform(0.1, 1.0))
    return ckt.build()


def test_hand_example_of_the_page():
    ckt = Circuit(3, {0: lambda t: 0.0})
    ckt.cap(1, 0, 1.0)
    ckt.cap(2, 0, 1.0)
    ckt.res(1, 0, 1.0)
    ckt.res(2, 0, 1.0)
    ckt.res(1, 2, 1.0)
    ckt.build()
    vn = [0.0, 1.0, 0.0]
    v = list(vn)
    evals = relax_time_point(ckt, v, vn, 1.0, {1, 2}, 0.01, 100)
    assert evals == 6
    assert abs(v[1] - 91 / 243) < 1e-15 and abs(v[2] - 91 / 729) < 1e-15


def test_linear_node_update_is_exact():
    rng = random.Random(62)
    ckt = random_rc(rng, 5)
    vn = [0.0] + [rng.uniform(-1, 1) for _ in range(5)]
    v = list(vn)
    for i in ckt.unknown:
        f, dv = node_row(ckt, i, v, vn, 0.3)
        v[i] -= f / dv[i]
        assert abs(node_row(ckt, i, v, vn, 0.3)[0]) < 1e-12


def test_gauss_seidel_contraction_and_stopping_bound():
    rng = random.Random(63)
    for _ in range(20):
        n = rng.randint(3, 8)
        ckt = random_rc(rng, n)
        h = rng.uniform(0.1, 2.0)
        vn = [0.0] + [rng.uniform(-1, 1) for _ in range(n)]
        exact = backward_euler_newton(ckt, vn, h, 1)[1][1]
        rho = jacobian_rho(ckt, vn, vn, h)
        assert rho < 1  # C/h + G is strictly diagonally dominant for these networks
        v = list(vn)
        err = max(abs(v[i] - exact[i]) for i in ckt.unknown)
        for _ in range(12):
            step = sweep(ckt, v, vn, h)
            new = max(abs(v[i] - exact[i]) for i in ckt.unknown)
            assert new <= rho * err + 1e-14
            assert new <= rho / (1 - rho) * step + 1e-14
            err = new


def test_ita_matches_full_newton_backward_euler():
    ckt, v0 = chain(4)
    ref = backward_euler_newton(ckt, v0, 1e-12, 600)
    out6, ev6 = ita(ckt, v0, 1e-12, 600, 1e-6)
    out8, ev8 = ita(ckt, v0, 1e-12, 600, 1e-8)
    assert maxdiff(out6, ref, ckt.unknown) < 2e-5
    assert maxdiff(out8, ref, ckt.unknown) < 2e-7
    assert ev6 < ev8
    for i in (3, 4, 5):
        assert abs(crossing(out6, i) - crossing(ref, i)) < 1e-14
    # one sweep per time point (no iteration) is visibly different
    one, _ = one_sweep_simulation(ckt, v0, 1e-12, 600)
    assert maxdiff(one, ref, ckt.unknown) > 0.05
    assert abs(crossing(one, 5) - crossing(ref, 5)) > 5e-12


def test_crosstalk_two_way_coupling():
    ckt, v0 = chain(2)
    ckt.n += 2
    vin, vic = ckt.n - 2, ckt.n - 1
    ckt.fixed[vin] = lambda t: 0.0
    ckt.mos("n", vic, vin, 0, K / 4, VT, LAM)
    ckt.mos("p", vic, vin, 1, K / 4, VT, LAM)
    ckt.cap(vic, 0, 5e-15)
    ckt.cap(vic, 3, 20e-15)  # strong coupling to the first output
    v0 = v0 + [0.0, VDD]
    ref = backward_euler_newton(ckt, v0, 1e-12, 500)
    out, _ = ita(ckt, v0, 1e-12, 500, 1e-6)
    one, _ = one_sweep_simulation(ckt, v0, 1e-12, 500)
    assert maxdiff(out, ref, ckt.unknown) < 5e-4
    dip_ref = min(x[vic] for _, x in ref)
    dip_ita = min(x[vic] for _, x in out)
    dip_one = min(x[vic] for _, x in one)
    assert abs(dip_ita - dip_ref) < 1e-4
    assert abs(dip_one - dip_ref) > 0.05


def test_latency_skips_quiet_nodes():
    ckt, v0 = chain(8)
    _, e1 = ita(ckt, v0, 1e-12, 1000, 1e-6)
    _, e2 = ita(ckt, v0, 1e-12, 2000, 1e-6)
    _, e3 = ita(ckt, v0, 1e-12, 3000, 1e-6)
    assert e1 > 0 and e2 > e1  # the edge travels down the chain in the first 2 ns
    assert e2 == e3  # after 2 ns no node moves by more than tau: no evaluation at all


def gyrator(h):
    c = Circuit(3, {0: lambda t: 0.0})
    c.cap(1, 0, 1.0)
    c.cap(2, 0, 1.0)
    c.res(1, 0, 1.0)
    c.res(2, 0, 1.0)
    c.vccs(1, 0, 2, 0, 2.0)
    c.vccs(2, 0, 1, 0, -2.0)
    return c


def test_relaxation_needs_dominance_full_newton_does_not():
    # node Jacobian [[1/h + 1, 2], [-2, 1/h + 1]]: Gauss-Seidel rate 4 / (1/h + 1)^2
    for h in (0.25, 0.5):
        out, _ = ita(gyrator(h), [0.0, 1.0, 0.0], h, 3, 1e-10, max_evals=2000)
        ref = backward_euler_newton(gyrator(h), [0.0, 1.0, 0.0], h, 3)
        assert maxdiff(out, ref, [1, 2]) < 1e-9
    for h in (1.0, 2.0):
        backward_euler_newton(gyrator(h), [0.0, 1.0, 0.0], h, 3)
        with pytest.raises(NonConvergence):
            ita(gyrator(h), [0.0, 1.0, 0.0], h, 3, 1e-10, max_evals=2000)


def test_small_steps_make_the_chain_dominant():
    ckt, v0 = chain(4)
    ref = backward_euler_newton(ckt, v0, 1e-12, 600)
    rho = max(jacobian_rho(ckt, x, x, 1e-12) for _, x in ref)
    # limit as h -> 0: coupling capacitance over total capacitance, 4 fF / 14 fF
    assert rho < 4 / 14 + 0.01
    assert max(jacobian_rho(ckt, x, x, 1e-10) for _, x in ref) > 1
