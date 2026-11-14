# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/timing-simulation/. The authors are listed in prov/F3Y8TC.jsonl.
"""Tests for MOTIS-style timing simulation against a fine-step RK4 reference and a full
backward Euler Newton solve."""

import random

from timing_simulation import Circuit, crossing, mos, motis, node_current, ramp

VDD = 1.8
T_END = 1.0       # ns
H = 0.001         # ns, 1 ps
H_REF = 0.00005   # ns, 0.05 ps for the RK4 reference


def chain(stages=4, cap=10.0, k=200.0):
    c = Circuit(vdd=VDD)
    c.add_input("in", ramp(0.1, 0.15, 0.0, VDD))
    prev = "in"
    init = {}
    for s in range(stages):
        y = f"y{s + 1}"
        c.add_node(y, cap)
        c.add_transistor("p", prev, "vdd", y, k)
        c.add_transistor("n", prev, y, "gnd", k)
        init[y] = VDD if s % 2 == 0 else 0.0
        prev = y
    return c, init


def nand_stack():
    """A NAND gate with the internal node m of its n stack, driving an inverter."""
    c = Circuit(vdd=VDD)
    c.add_input("a", ramp(0.1, 0.15, 0.0, VDD))
    c.add_input("b", lambda t: VDD)
    c.add_node("out", 10.0)
    c.add_node("m", 3.0)
    c.add_node("z", 10.0)
    c.add_transistor("p", "a", "vdd", "out", 200.0)
    c.add_transistor("p", "b", "vdd", "out", 200.0)
    c.add_transistor("n", "a", "out", "m", 200.0)
    c.add_transistor("n", "b", "m", "gnd", 200.0)
    c.add_transistor("p", "out", "vdd", "z", 200.0)
    c.add_transistor("n", "out", "z", "gnd", 200.0)
    return c, {"out": VDD, "m": 0.0, "z": 0.0}


# ---------------------------------------------------------------- references

def rk4(c, init, t_end, h):
    """Classical Runge-Kutta on C dv/dt = I(v) with a fine step: the reference."""
    at = c.at_node()
    v = dict(init)

    def f(t, vals):
        full = {n: w(t) for n, w in c.fixed.items()}
        full.update(vals)
        return {n: node_current(c, at[n], n, full)[0] / c.cap[n] for n in c.order}

    times, waves = [0.0], {n: [v[n]] for n in c.order}
    for s in range(int(round(t_end / h))):
        t = s * h
        k1 = f(t, v)
        k2 = f(t + h / 2, {n: v[n] + h / 2 * k1[n] for n in v})
        k3 = f(t + h / 2, {n: v[n] + h / 2 * k2[n] for n in v})
        k4 = f(t + h, {n: v[n] + h * k3[n] for n in v})
        v = {n: v[n] + h / 6 * (k1[n] + 2 * k2[n] + 2 * k3[n] + k4[n]) for n in v}
        times.append(t + h)
        for n in c.order:
            waves[n].append(v[n])
    return times, waves


def solve_linear(a, b):
    """Gaussian elimination with partial pivoting."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        p = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[p] = m[p], m[col]
        for r in range(col + 1, n):
            f = m[r][col] / m[col][col]
            for j in range(col, n + 1):
                m[r][j] -= f * m[col][j]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (m[r][n] - sum(m[r][j] * x[j] for j in range(r + 1, n))) / m[r][r]
    return x


def backward_euler_newton(c, init, t_end, h):
    """Backward Euler with the full nonlinear system solved by Newton's method to 1e-13."""
    at = c.at_node()
    names = c.order
    v = {n: w(0.0) for n, w in c.fixed.items()}
    v.update(init)
    times, waves = [0.0], {n: [v[n]] for n in names}
    for s in range(1, int(round(t_end / h)) + 1):
        t = s * h
        for n, w in c.fixed.items():
            v[n] = w(t)
        old = {n: v[n] for n in names}
        for _ in range(100):
            res, jac = [], []
            for n in names:
                cur, _ = node_current(c, at[n], n, v)
                res.append(c.cap[n] * (v[n] - old[n]) / h - cur)
                row = []
                for m in names:   # derivative of the residual of n in v[m], by central differences
                    e = 1e-7
                    keep = v[m]
                    v[m] = keep + e
                    cp, _ = node_current(c, at[n], n, v)
                    v[m] = keep - e
                    cm, _ = node_current(c, at[n], n, v)
                    v[m] = keep
                    row.append((c.cap[n] / h if m == n else 0.0) - (cp - cm) / (2 * e))
                jac.append(row)
            dx = solve_linear(jac, [-r for r in res])
            for n, d in zip(names, dx):
                v[n] += d
            if max(abs(d) for d in dx) < 1e-13:
                break
        times.append(t)
        for n in names:
            waves[n].append(v[n])
    return times, waves


def max_error(a, b, stride=1):
    """Largest difference between waveforms a (coarse) and b (fine, stride points per coarse step)."""
    return max(abs(x - b[i * stride]) for i, x in enumerate(a))


# ---------------------------------------------------------------- the device model

def test_mos_regions_and_symmetry():
    k, vt = 200.0, 0.5
    assert mos("n", k, vt, 0.4, 1.0, 0.0)[0] == 0.0                     # cutoff
    assert abs(mos("n", k, vt, 1.8, 1.8, 0.0)[0] - 0.5 * k * 1.3 ** 2) < 1e-9   # saturation
    assert abs(mos("n", k, vt, 1.8, 0.2, 0.0)[0] - k * (1.3 * 0.2 - 0.02)) < 1e-9  # linear
    assert abs(mos("p", k, vt, 0.0, 1.8, 0.0)[0] - 0.5 * k * 1.3 ** 2) < 1e-9
    rng = random.Random(7)
    for _ in range(500):
        kind = rng.choice("np")
        vg, va, vb = (rng.uniform(-0.2, 2.0) for _ in range(3))
        assert abs(mos(kind, k, vt, vg, va, vb)[0] + mos(kind, k, vt, vg, vb, va)[0]) < 1e-12


def test_mos_derivatives():
    rng = random.Random(8)
    e = 1e-6
    for _ in range(500):
        kind = rng.choice("np")
        vg, va, vb = (rng.uniform(-0.2, 2.0) for _ in range(3))
        cur, da, db, dg = mos(kind, 200.0, 0.5, vg, va, vb)
        for idx, d in ((1, da), (2, db), (0, dg)):
            p = [vg, va, vb]
            q = [vg, va, vb]
            p[idx] += e
            q[idx] -= e
            num = (mos(kind, 200.0, 0.5, *p)[0] - mos(kind, 200.0, 0.5, *q)[0]) / (2 * e)
            assert abs(num - d) < 1e-3 * (1 + abs(d))


# ---------------------------------------------------------------- the solver

def test_exact_node_solves_equal_full_newton_on_feed_forward_chain():
    c, init = chain(4)
    h = 0.002
    _, w_exact, _ = motis(c, init, T_END, h, exact=True)
    _, w_full = backward_euler_newton(c, init, T_END, h)
    for n in c.order:
        assert max_error(w_exact[n], w_full[n]) < 1e-9


def test_one_newton_step_stays_near_full_backward_euler():
    c, init = chain(4)
    h = 0.002
    _, w_one, _ = motis(c, init, T_END, h)
    _, w_full = backward_euler_newton(c, init, T_END, h)
    assert max(max_error(w_one[n], w_full[n]) for n in c.order) < 0.005


def test_chain_against_fine_rk4_reference():
    c, init = chain(4)
    _, w_ref = rk4(c, init, T_END, H_REF)
    stride = int(round(H / H_REF))
    times, w, _ = motis(c, init, T_END, H)
    ref_times = [i * H_REF for i in range(len(w_ref["y1"]))]
    for n in c.order:
        assert max_error(w[n], w_ref[n], stride) < 0.02                # volts, stated tolerance
        t_sim = crossing(times, w[n], VDD / 2)
        t_ref = crossing(ref_times, w_ref[n], VDD / 2)
        assert abs(t_sim - t_ref) < 0.0015                               # 1.5 ps, stated tolerance
    assert w["y4"][-1] > VDD - 1e-3                                      # the edge went through


def test_first_order_error_ratio():
    c, init = chain(2)
    _, w_ref = rk4(c, init, 0.6, H_REF)
    errors = []
    for h in (0.004, 0.002, 0.001):
        _, w, _ = motis(c, init, 0.6, h)
        stride = int(round(h / H_REF))
        errors.append(max(max_error(w[n], w_ref[n], stride) for n in c.order))
    for e1, e2 in zip(errors, errors[1:]):
        assert 1.6 < e1 / e2 < 2.5


def test_event_skipping_saves_work():
    c, init = chain(8)
    _, w_full, n_full = motis(c, init, T_END, H)
    _, w_skip, n_skip = motis(c, init, T_END, H, eps=1e-4)
    assert n_skip < 0.5 * n_full
    assert max(max_error(w_skip[n], w_full[n]) for n in c.order) < 0.01


def test_bidirectional_stack_against_reference():
    c, init = nand_stack()
    _, w_ref = rk4(c, init, T_END, H_REF)
    stride = int(round(H / H_REF))
    _, w, _ = motis(c, init, T_END, H)
    for n in c.order:
        assert max_error(w[n], w_ref[n], stride) < 0.02
    assert w["out"][-1] < 1e-3 and w["z"][-1] > VDD - 1e-3


def test_too_large_skip_threshold_loses_the_edge():
    # Once the input ramp ends, nothing wakes y1 again. When its change per step falls
    # below 0.01 V, it is put to sleep for good and freezes between the rails.
    c, init = chain(8)
    _, w, _ = motis(c, init, T_END, H, eps=1e-2)
    assert 0.3 < w["y1"][-1] < 0.6
    _, good, _ = motis(c, init, T_END, H)
    assert good["y1"][-1] < 1e-3


def test_quiet_circuit_is_skipped():
    c, init = chain(4)
    c.fixed["in"] = lambda t: 0.0
    _, w, evals = motis(c, init, T_END, H, eps=1e-6)
    assert evals <= 4 * 2                                                # settles at once
    assert all(w[n][-1] == init[n] for n in c.order)
