# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filon-quadrature/. The authors are listed in prov/1BJZ9V.jsonl.

import math
import random
import unittest
from fractions import Fraction

from filon_quadrature import (
    exact_monomial,
    filon,
    filon_coefficients,
    integrate,
    series_coefficients,
)

U = 2.0 ** -52


def exact_exp(c, a, b, w):
    """Integral of e^(c x) e^(i w x) over [a, b]."""
    def e(x):
        return complex(math.exp(c * x) * math.cos(w * x), math.exp(c * x) * math.sin(w * x))
    return (e(b) - e(a)) / complex(c, w)


def simpson(g, a, b, m):
    h = (b - a) / m
    s = g(a) + g(b) + 4 * math.fsum(g(a + i * h) for i in range(1, m, 2)) + 2 * math.fsum(g(a + i * h) for i in range(2, m, 2))
    return s * h / 3


_X5 = [0.0, math.sqrt(5 - 2 * math.sqrt(10 / 7)) / 3, math.sqrt(5 + 2 * math.sqrt(10 / 7)) / 3]
_W5 = [128 / 225, (322 + 13 * math.sqrt(70)) / 900, (322 - 13 * math.sqrt(70)) / 900]


def gauss5(g, a, b, panels):
    """Composite 5-point Gauss-Legendre, used as an independent reference."""
    h = (b - a) / panels
    terms = []
    for p in range(panels):
        c = a + (p + 0.5) * h
        terms.append(_W5[0] * g(c))
        for x, w in zip(_X5[1:], _W5[1:]):
            terms.append(w * g(c - 0.5 * h * x))
            terms.append(w * g(c + 0.5 * h * x))
    return math.fsum(terms) * h / 2


class Counter:
    def __init__(self, f):
        self.f, self.n = f, 0

    def __call__(self, x):
        self.n += 1
        return self.f(x)


# ---- formal power series in theta with complex Fraction coefficients ----
ORDER = 20
I_POW = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def smul(p, q):
    out = [(Fraction(0), Fraction(0))] * (ORDER + 1)
    for i in range(ORDER + 1):
        for j in range(ORDER + 1 - i):
            t = cmul(p[i], q[j])
            out[i + j] = (out[i + j][0] + t[0], out[i + j][1] + t[1])
    return out


def sadd(*ps):
    return [(sum(p[i][0] for p in ps), sum(p[i][1] for p in ps)) for i in range(ORDER + 1)]


def sscale(p, c):
    return [cmul(t, c) for t in p]


def real_series(coeffs):
    return [(Fraction(coeffs[i]) if i < len(coeffs) else Fraction(0), Fraction(0)) for i in range(ORDER + 1)]


def exp_series(sign):
    """e^(sign i theta)."""
    out = []
    for j in range(ORDER + 1):
        r, im = I_POW[(j if sign > 0 else -j) % 4]
        out.append((Fraction(r, math.factorial(j)), Fraction(im, math.factorial(j))))
    return out


def rule_series(k):
    """Filon-Simpson on [-1, 1], m = 2 (h = 1), for f = u^k, as a series in theta."""
    ca, cb, cg = series_coefficients()
    A, B, G = real_series(ca), real_series(cb), real_series(cg)
    ep, em = exp_series(1), exp_series(-1)
    f1, fm1, f0 = 1, (-1) ** k, 1 if k == 0 else 0
    # C + i S = -i alpha (f1 e^(i th) - fm1 e^(-i th)) + beta (f1 e^(i th) + fm1 e^(-i th)) / 2 + gamma f0
    diff = sadd(sscale(ep, (Fraction(f1), 0)), sscale(em, (Fraction(-fm1), 0)))
    half = sadd(sscale(ep, (Fraction(f1, 2), 0)), sscale(em, (Fraction(fm1, 2), 0)))
    return sadd(sscale(smul(A, diff), (0, Fraction(-1))), smul(B, half), sscale(G, (Fraction(f0), 0)))


def exact_series(k):
    """Integral of u^k e^(i theta u) over [-1, 1] as a series in theta."""
    out = []
    for j in range(ORDER + 1):
        if (k + j) % 2:
            out.append((Fraction(0), Fraction(0)))
        else:
            r, im = I_POW[j % 4]
            c = Fraction(2, math.factorial(j) * (k + j + 1))
            out.append((r * c, im * c))
    return out


class TestCoefficients(unittest.TestCase):
    def test_series_matches_abramowitz_stegun(self):
        ca, cb, cg = series_coefficients()
        self.assertEqual(ca[:8], [0, 0, 0, Fraction(2, 45), 0, Fraction(-2, 315), 0, Fraction(2, 4725)])
        self.assertEqual(cb[:7], [Fraction(2, 3), 0, Fraction(2, 15), 0, Fraction(-4, 105), 0, Fraction(2, 567)])
        self.assertEqual(cg[:7], [Fraction(4, 3), 0, Fraction(-2, 15), 0, Fraction(1, 210), 0, Fraction(-1, 11340)])

    def test_series_agrees_with_closed_form_near_switch(self):
        ca, cb, cg = series_coefficients()
        for t in [0.5, 0.8, 1.0, 1.2, 1.5, -1.0]:
            s, c = math.sin(t), math.cos(t)
            closed = ((t * t + t * s * c - 2 * s * s) / t ** 3,
                      2 * (t * (1 + c * c) - 2 * s * c) / t ** 3,
                      4 * (s - t * c) / t ** 3)
            series = [math.fsum(float(x) * t ** k for k, x in enumerate(cs)) for cs in (ca, cb, cg)]
            for u, v in zip(closed, series):
                self.assertLess(abs(u - v), 1e-13 * max(1.0, abs(v)))

    def test_closed_form_cancels_for_small_theta(self):
        t = 1e-4
        s, c = math.sin(t), math.cos(t)
        closed = (t * t + t * s * c - 2 * s * s) / t ** 3
        alpha = filon_coefficients(t)[0]
        self.assertLess(abs(alpha - (2 * t ** 3 / 45 - 2 * t ** 5 / 315)) / alpha, 1e-14)
        self.assertGreater(abs(closed - alpha) / alpha, 0.5)  # every digit lost

    def test_parity(self):
        for t in [0.3, 2.7]:
            a1, b1, g1 = filon_coefficients(t)
            a2, b2, g2 = filon_coefficients(-t)
            self.assertAlmostEqual(a1, -a2, delta=1e-16)
            self.assertAlmostEqual(b1, b2, delta=1e-16)
            self.assertAlmostEqual(g1, g2, delta=1e-16)

    def test_theta_zero_gives_simpson_weights(self):
        self.assertEqual(filon_coefficients(0.0), (0.0, 2 / 3, 4 / 3))


class TestExactness(unittest.TestCase):
    def test_formal_exactness_for_quadratics_and_failure_at_cubic(self):
        for k in range(3):
            self.assertEqual(rule_series(k), exact_series(k), k)
        diff = [(p[0] - q[0], p[1] - q[1]) for p, q in zip(rule_series(3), exact_series(3))]
        first = next(i for i, d in enumerate(diff) if d != (0, 0))
        self.assertEqual(first, 1)  # theta^0 term matches (Simpson is exact for cubics), theta^1 does not
        self.assertEqual(diff[1], (Fraction(0), Fraction(4, 15)))  # u^3 and u agree at the nodes: 2/3 - 2/5

    def test_exact_monomial_helper_against_series(self):
        t = 0.7
        for k in range(4):
            ser = exact_series(k)
            z = complex(math.fsum(float(c[0]) * t ** i for i, c in enumerate(ser)),
                        math.fsum(float(c[1]) * t ** i for i, c in enumerate(ser)))
            self.assertLess(abs(exact_monomial(k, -1.0, 1.0, t) - z), 1e-12)

    def test_constant_f_is_exact_for_every_omega(self):
        for w in [0.5, 3.0, 77.0, 1e4]:
            for m in [2, 10]:
                c, s = filon(lambda x: 1.0, -0.3, 2.1, w, m)
                self.assertLess(abs(c - (math.sin(2.1 * w) - math.sin(-0.3 * w)) / w), 1e-14)
                self.assertLess(abs(s + (math.cos(2.1 * w) - math.cos(-0.3 * w)) / w), 1e-14)

    def test_cubic_fails_in_float(self):
        c, s = filon(lambda x: x ** 3, 0.0, 1.0, 5.0, 2)
        z = exact_monomial(3, 0.0, 1.0, 5.0)
        self.assertGreater(abs(complex(c, s) - z), 1e-4)

    def test_omega_zero_is_composite_simpson(self):
        for f in [math.exp, math.sin, lambda x: x ** 4]:
            for m in [2, 8, 30]:
                c, s = filon(f, 0.2, 1.7, 0.0, m)
                self.assertLess(abs(c - simpson(f, 0.2, 1.7, m)), 1e-15)
                self.assertEqual(s, 0.0)

    def test_random_quadratics_oracle(self):
        rng = random.Random(20261108)
        for _ in range(600):
            co = [rng.uniform(-1, 1) for _ in range(3)]
            a = rng.uniform(-3, 3)
            b = a + rng.choice([-1, 1]) * rng.uniform(0.1, 3)
            w = rng.choice([-1, 1]) * rng.uniform(1, 200)
            m = 2 * rng.randint(1, 32)
            c, s = filon(lambda x: co[0] + co[1] * x + co[2] * x * x, a, b, w, m)
            z = sum(co[k] * exact_monomial(k, a, b, w) for k in range(3))
            self.assertLess(abs(complex(c, s) - z), 1e-12, (co, a, b, w, m))


class TestErrorBounds(unittest.TestCase):
    def test_random_exponentials_obey_both_bounds(self):
        rng = random.Random(7)
        for _ in range(500):
            cexp = rng.uniform(-2, 2)
            a = rng.uniform(-1, 1)
            b = a + rng.uniform(0.2, 2)
            w = rng.uniform(1, 2000)
            m = 2 * rng.randint(1, 50)
            h = (b - a) / m
            M3 = abs(cexp) ** 3 * max(math.exp(cexp * a), math.exp(cexp * b))
            c, s = filon(lambda x: math.exp(cexp * x), a, b, w, m)
            err = abs(complex(c, s) - exact_exp(cexp, a, b, w))
            bound = min((b - a) * h ** 3 * M3 / (9 * math.sqrt(3)), 7 / 3 * (b - a) * h * M3 / w ** 2)
            self.assertLessEqual(err, bound + 1e-13, (cexp, a, b, w, m))

    def test_h4_rate_for_fixed_omega(self):
        for w in [1.0, 10.0]:
            z = exact_exp(1, 0, 1, w).real
            errs = [abs(filon(math.exp, 0, 1, w, m)[0] - z) for m in [32, 64, 128]]
            for e1, e2 in zip(errs, errs[1:]):
                self.assertTrue(15.5 < e1 / e2 < 16.6, errs)

    def test_beats_simpson_when_oscillating(self):
        z = exact_exp(1, 0, 1, 100).real
        fe = abs(filon(math.exp, 0, 1, 100, 32)[0] - z)
        se = abs(simpson(lambda x: math.exp(x) * math.cos(100 * x), 0, 1, 32) - z)
        self.assertLess(fe, 1e-6)
        self.assertGreater(se, 0.1)

    def test_error_shrinks_as_omega_grows_at_fixed_m(self):
        errs = []
        for w in [400, 800, 1600, 3200]:
            c, s = filon(math.exp, 0, 1, w, 8)
            errs.append(abs(complex(c, s) - exact_exp(1, 0, 1, w)))
        self.assertLess(errs[-1], errs[0] / 20)


class TestClosedForms(unittest.TestCase):
    def test_exp(self):
        c, s = filon(math.exp, 0, 1, 50, 256)
        z = exact_exp(1, 0, 1, 50)
        self.assertLess(abs(c - z.real), 1e-9)
        self.assertLess(abs(s - z.imag), 1e-9)

    def test_sin_times_cos(self):
        w = 30.5
        ex = 0.5 * ((1 - math.cos((1 + w) * math.pi)) / (1 + w) + (1 - math.cos((1 - w) * math.pi)) / (1 - w))
        c, _ = filon(math.sin, 0, math.pi, w, 128)
        self.assertLess(abs(c - ex), 1e-8)

    def test_exp_cos_gives_bessel(self):
        def besseli(k, x):
            return math.fsum((x / 2) ** (2 * j + k) / (math.factorial(j) * math.factorial(j + k)) for j in range(40))
        for k, m, tol in [(5, 128, 2e-7), (20, 128, 1e-14)]:
            c, s = filon(lambda x: math.exp(math.cos(x)), 0, 2 * math.pi, k, m)
            self.assertLess(abs(c - 2 * math.pi * besseli(k, 1.0)), tol)
            self.assertLess(abs(s), 1e-13)

    def test_runge_against_gauss_reference(self):
        w = 50
        ref = gauss5(lambda x: math.cos(w * x) / (1 + x * x), -5, 5, 2000)
        c, _ = filon(lambda x: 1 / (1 + x * x), -5, 5, w, 1024)
        self.assertLess(abs(c - ref), 2e-12)

    def test_sqrt_rate_is_h_to_three_halves(self):
        w = 50
        ref = gauss5(lambda t: 2 * t * t * math.cos(w * t * t), 0, 1, 4000)
        errs = [abs(filon(math.sqrt, 0, 1, w, m)[0] - ref) for m in [128, 256, 512, 1024]]
        for e1, e2 in zip(errs, errs[1:]):
            self.assertTrue(2.6 < e1 / e2 < 3.2, errs)

    def test_cos_omega_x_alone(self):
        c, s = filon(lambda x: 1.0, 0, 1, 1000, 2)
        self.assertLess(abs(c - math.sin(1000) / 1000), 1e-16)
        self.assertLess(abs(s - (1 - math.cos(1000)) / 1000), 1e-16)


class TestEdgeCases(unittest.TestCase):
    def test_empty_interval(self):
        f = Counter(math.exp)
        self.assertEqual(filon(f, 2.0, 2.0, 10.0, 4), (0.0, 0.0))
        self.assertEqual(f.n, 0)
        self.assertEqual(integrate(math.exp, 1.0, 1.0, 3.0)[:4], (0.0, 0.0, 0.0, 0))

    def test_reversed_interval(self):
        c1, s1 = filon(math.exp, 0, 1, 17, 20)
        c2, s2 = filon(math.exp, 1, 0, 17, 20)
        self.assertLess(abs(c1 + c2), 1e-15)
        self.assertLess(abs(s1 + s2), 1e-15)

    def test_negative_omega(self):
        c1, s1 = filon(math.exp, 0, 1, 17, 20)
        c2, s2 = filon(math.exp, 0, 1, -17, 20)
        self.assertLess(abs(c1 - c2), 1e-15)
        self.assertLess(abs(s1 + s2), 1e-15)

    def test_single_panel_pair_and_bad_m(self):
        c, s = filon(lambda x: x * x, 0, 1, 40, 2)
        z = exact_monomial(2, 0, 1, 40)
        self.assertLess(abs(complex(c, s) - z), 1e-15)
        for m in [0, 1, 3, 7]:
            with self.assertRaises(ValueError):
                filon(math.exp, 0, 1, 1, m)

    def test_evaluation_count(self):
        for m in [2, 10, 64]:
            f = Counter(math.exp)
            filon(f, 0, 1, 9, m)
            self.assertEqual(f.n, m + 1)

    def test_endpoint_singularity_is_evaluated(self):
        with self.assertRaises(ValueError):
            filon(math.log, 0, 1, 10, 8)
        with self.assertRaises(ZeroDivisionError):
            filon(lambda x: x ** -0.5, 0, 1, 10, 8)

    def test_jump_converges_like_h(self):
        w = 50
        ex = (math.sin(w) - math.sin(w / 3)) / w
        f = lambda x: 1.0 if x > 1 / 3 else 0.0
        errs = [abs(filon(f, 0, 1, w, m)[0] - ex) for m in [128, 256, 512, 1024]]
        for e1, e2 in zip(errs, errs[1:]):
            self.assertTrue(1.8 < e1 / e2 < 2.2, errs)

    def test_infinite_interval_by_truncation(self):
        for w in [1.0, 20.0]:
            c, s = filon(lambda x: math.exp(-x), 0, 40, w, 4096)
            self.assertLess(abs(c - 1 / (1 + w * w)), 1e-8)
            self.assertLess(abs(s - w / (1 + w * w)), 1e-8)


class TestDriver(unittest.TestCase):
    def test_evaluations_by_tolerance(self):
        z = exact_exp(1, 0, 1, 100)
        counts = []
        for tol in [1e-8, 1e-10, 1e-12]:
            c, s, est, ev, status = integrate(math.exp, 0, 1, 100, tol)
            self.assertEqual(status, "ok")
            self.assertLessEqual(abs(complex(c, s) - z), tol)
            counts.append(ev)
        self.assertEqual(counts, [129, 513, 1025])

    def test_counts_match_reuse(self):
        f = Counter(math.exp)
        c, s, est, ev, status = integrate(f, 0, 1, 30, 1e-9)
        self.assertEqual(f.n, ev)
        m = ev - 1
        self.assertEqual(m & (m - 1), 0)
        self.assertEqual((c, s), filon(math.exp, 0, 1, 30, m))

    def test_false_convergence_on_plateau(self):
        # While omega h is large the error stalls, two results agree, and the test stops early.
        c, s, est, ev, status = integrate(math.exp, 0, 1, 100, 1e-6)
        err = abs(complex(c, s) - exact_exp(1, 0, 1, 100))
        self.assertEqual((status, ev), ("ok", 17))
        self.assertLess(est, 1e-6)
        self.assertGreater(err, 1e-6)

    def test_unreachable_tolerance(self):
        c, s, est, ev, status = integrate(math.sqrt, 0, 1, 50, 1e-12, max_m=2 ** 12)
        self.assertEqual(status, "limit")
        self.assertEqual(ev, 2 ** 12 + 1)
        self.assertGreater(est, 1e-12)
        c, s, est, ev, status = integrate(math.exp, 0, 1, 5, 0.0, max_m=2 ** 10)
        self.assertEqual(status, "limit")
        _, _, est, ev, status = integrate(math.exp, 0, 1, 5, 1e-3, max_m=2)
        self.assertEqual((ev, status), (3, "limit"))
        self.assertEqual(est, float("inf"))


if __name__ == "__main__":
    unittest.main()
