# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-linearization-method/. The authors are listed in prov/3NRTQF.jsonl.

import itertools
import math
import random

import pytest

from direct_linearization_method import (
    clutch_loops,
    dlm,
    fourbar_loops,
    linear_stack_loops,
    loop_residual,
    solve_assembly,
)

CLUTCH_X = {"a": 27.645, "c": 11.43, "e": 50.8}
CLUTCH_MAN = ["a", "c", "e"]
CLUTCH_KIN = ["b", "phi"]
CLUTCH_GUESS = {"b": 4.0, "phi": 0.1}


def clutch_exact(x):
    """Closed form of the clutch: cos(phi) = (a + c) / (e - c)."""
    a, c, e = x["a"], x["c"], x["e"]
    q = (a + c) / (e - c)
    return math.acos(q), math.sqrt((e - c) ** 2 - (a + c) ** 2)


def clutch_phi(x):
    return solve_assembly(clutch_loops(), x, CLUTCH_GUESS, CLUTCH_KIN)["phi"]


def test_clutch_solution_matches_closed_form():
    v = solve_assembly(clutch_loops(), CLUTCH_X, CLUTCH_GUESS, CLUTCH_KIN)
    phi, b = clutch_exact(CLUTCH_X)
    assert v["phi"] == pytest.approx(phi, abs=1e-12)
    assert v["b"] == pytest.approx(b, abs=1e-10)
    assert math.degrees(v["phi"]) == pytest.approx(7.0, abs=0.05)
    assert max(abs(r) for r in loop_residual(clutch_loops(), v)) < 1e-10


def test_clutch_sensitivities_analytic_and_finite_differences():
    T = {"a": 0.01, "c": 0.0025, "e": 0.0125}
    res = dlm(clutch_loops(), CLUTCH_X, CLUTCH_GUESS, CLUTCH_MAN, CLUTCH_KIN, T, "phi")
    a, c, e = CLUTCH_X["a"], CLUTCH_X["c"], CLUTCH_X["e"]
    s = math.sin(res["nominal"])
    analytic = {
        "a": -1 / (e - c) / s,
        "c": -(e + a) / (e - c) ** 2 / s,
        "e": (a + c) / (e - c) ** 2 / s,
    }
    for name in CLUTCH_MAN:
        assert res["sens"][name] == pytest.approx(analytic[name], rel=1e-9)
        h = 1e-6
        xp, xm = dict(CLUTCH_X), dict(CLUTCH_X)
        xp[name] += h
        xm[name] -= h
        fd = (clutch_phi(xp) - clutch_phi(xm)) / (2 * h)
        assert res["sens"][name] == pytest.approx(fd, rel=1e-6)
    wc = sum(abs(analytic[n]) * T[n] for n in CLUTCH_MAN)
    rss = math.sqrt(sum((analytic[n] * T[n]) ** 2 for n in CLUTCH_MAN))
    assert res["worst"] == pytest.approx(wc, rel=1e-9)
    assert res["rss"] == pytest.approx(rss, rel=1e-9)
    assert res["rss"] <= res["worst"] <= math.sqrt(3) * res["rss"] + 1e-15


def corner_range(x0, T, names, f):
    vals = []
    for signs in itertools.product((-1, 1), repeat=len(names)):
        x = dict(x0)
        for s, n in zip(signs, names):
            x[n] += s * T[n]
        vals.append(f(x))
    return min(vals), max(vals)


def test_clutch_linearization_error_is_second_order():
    """The gap between the DLM worst case and the corner range shrinks like T^2."""
    errs = []
    phi0 = clutch_exact(CLUTCH_X)[0]
    for k in (0.02, 0.002):
        T = {n: k for n in CLUTCH_MAN}
        res = dlm(clutch_loops(), CLUTCH_X, CLUTCH_GUESS, CLUTCH_MAN, CLUTCH_KIN, T, "phi")
        lo, hi = corner_range(CLUTCH_X, T, CLUTCH_MAN, lambda x: clutch_exact(x)[0])
        err = max(abs((hi - phi0) - res["worst"]), abs((phi0 - lo) - res["worst"]))
        errs.append((err, res["worst"]))
    assert errs[0][0] > 0
    assert errs[1][0] / errs[0][0] < 0.02
    assert errs[0][0] < 0.2 * errs[0][1]


FOUR_X = {"a": 40.0, "b": 120.0, "c": 80.0, "d": 100.0, "th2": math.radians(40)}
FOUR_MAN = ["a", "b", "c", "d"]
FOUR_KIN = ["th3", "th4"]


def freudenstein_theta4(x, branch):
    """Closed form for the rocker angle (open branch -1, crossed branch +1)."""
    a, b, c, d, t2 = x["a"], x["b"], x["c"], x["d"], x["th2"]
    k1, k2, k3 = d / a, d / c, (a * a - b * b + c * c + d * d) / (2 * a * c)
    A = math.cos(t2) - k1 - k2 * math.cos(t2) + k3
    B = -2 * math.sin(t2)
    C = k1 - (k2 + 1) * math.cos(t2) + k3
    return 2 * math.atan2(-B + branch * math.sqrt(B * B - 4 * A * C), 2 * A)


def angle_diff(p, q):
    return math.remainder(p - q, 2 * math.pi)


def fourbar_guess(x):
    t4 = freudenstein_theta4(x, -1)
    px = x["c"] * math.cos(t4) + x["d"] - x["a"] * math.cos(x["th2"])
    py = x["c"] * math.sin(t4) - x["a"] * math.sin(x["th2"])
    return {"th3": math.atan2(py, px) + 0.05, "th4": t4 - 0.05}


def test_fourbar_matches_freudenstein():
    rng = random.Random(7)
    for _ in range(40):
        x = dict(FOUR_X)
        x["th2"] = rng.uniform(0, 2 * math.pi)
        v = solve_assembly(fourbar_loops(), x, fourbar_guess(x), FOUR_KIN)
        assert abs(angle_diff(v["th4"], freudenstein_theta4(x, -1))) < 1e-10


def test_fourbar_sensitivities_against_finite_differences():
    T = {"a": 0.05, "b": 0.1, "c": 0.08, "d": 0.1}
    rng = random.Random(11)
    for _ in range(10):
        x0 = dict(FOUR_X)
        x0["th2"] = rng.uniform(0.2, 2 * math.pi - 0.2)
        res = dlm(fourbar_loops(), x0, fourbar_guess(x0), FOUR_MAN, FOUR_KIN, T, "th4")
        for name in FOUR_MAN:
            h = 1e-5
            xp, xm = dict(x0), dict(x0)
            xp[name] += h
            xm[name] -= h
            fd = angle_diff(freudenstein_theta4(xp, -1), freudenstein_theta4(xm, -1)) / (2 * h)
            assert res["sens"][name] == pytest.approx(fd, rel=1e-6, abs=1e-9)


def test_linear_stack_gives_stack_up_formulas():
    x0 = {"A": 50.0, "B": 20.0, "C": 15.0, "D": 14.8}
    T = {"A": 0.10, "B": 0.05, "C": 0.05, "D": 0.05}
    res = dlm(linear_stack_loops(), x0, {"G": 0.0, "h": 0.0}, list(x0), ["G", "h"], T, "G")
    assert res["nominal"] == pytest.approx(0.20, abs=1e-12)
    assert res["sens"] == pytest.approx({"A": 1.0, "B": -1.0, "C": -1.0, "D": -1.0}, abs=1e-12)
    assert res["worst"] == pytest.approx(0.25, abs=1e-12)
    assert res["rss"] == pytest.approx(math.sqrt(0.0175), abs=1e-12)


def random_linear_loop(rng, n):
    """A loop with n manufactured lengths and two kinematic lengths, all at fixed angles."""
    names = ["x%d" % i for i in range(n)]
    loop = [(rng.choice((-1, 1)), nm, (rng.uniform(0, 2 * math.pi), {})) for nm in names]
    t = rng.uniform(0, 2 * math.pi)
    loop.append((1, "p", (t, {})))
    loop.append((1, "q", (t + rng.uniform(0.5, 2.6), {})))
    x0 = {nm: rng.uniform(5, 20) for nm in names}
    return [loop], x0, names


def test_linear_loops_are_exact_for_large_changes():
    rng = random.Random(2026)
    for _ in range(50):
        n = rng.randint(1, 6)
        loops, x0, names = random_linear_loop(rng, n)
        T = {nm: 1.0 for nm in names}
        res = dlm(loops, x0, {"p": 0.0, "q": 0.0}, names, ["p", "q"], T, "q")
        x1 = {nm: v + rng.uniform(-3, 3) for nm, v in x0.items()}
        q1 = solve_assembly(loops, x1, {"p": 0.0, "q": 0.0}, ["p", "q"])["q"]
        pred = res["nominal"] + sum(res["sens"][nm] * (x1[nm] - x0[nm]) for nm in names)
        assert q1 == pytest.approx(pred, abs=1e-8)


def test_singular_b_is_reported():
    loops = [[(1, "x", (0.0, {})), (-1, "p", (0.0, {})), (-1, "q", (0.0, {}))]]
    with pytest.raises(ValueError):
        dlm(loops, {"x": 3.0}, {"p": 1.0, "q": 1.0}, ["x"], ["p", "q"], {"x": 0.1}, "p")
