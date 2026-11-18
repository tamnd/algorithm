# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ggx-distribution/. The authors are listed in prov/CCM8S7.jsonl.

"""Tests of the GGX distribution by quadrature and by sampling."""

import math
import random

from ggx_distribution import beckmann_d, cdf_theta, ggx_d, ggx_d_aniso, ggx_d_slope, sample_ggx


def legendre_nodes(n: int) -> list[tuple[float, float]]:
    """Gauss-Legendre nodes and weights on [-1, 1], by Newton's method."""
    out = []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1.0)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        out.append((x, 2.0 / ((1.0 - x * x) * dp * dp)))
    return out


GL = legendre_nodes(16)


def integrate(f, a: float, b: float, panels: int) -> float:
    """Composite Gauss-Legendre rule with 16 nodes per panel."""
    total = 0.0
    hw = (b - a) / panels / 2.0
    for k in range(panels):
        mid = a + (2 * k + 1) * hw
        total += hw * sum(w * f(mid + hw * x) for x, w in GL)
    return total


def test_normalization() -> None:
    # The integral of D(h) (n.h) over the hemisphere, in theta_h.
    for alpha in (0.02, 0.1, 0.3, 0.5, 1.0, 2.0):
        val = integrate(
            lambda t: ggx_d(math.cos(t), alpha) * math.cos(t) * math.sin(t) * 2.0 * math.pi,
            0.0,
            math.pi / 2.0,
            200,
        )
        assert abs(val - 1.0) < 1e-6


def test_anisotropic_normalization() -> None:
    for ax, ay in ((0.2, 0.6), (0.5, 0.1), (0.4, 0.4)):
        def ring(t: float) -> float:
            st, ct = math.sin(t), math.cos(t)
            inner = integrate(
                lambda p: ggx_d_aniso((st * math.cos(p), st * math.sin(p), ct), ax, ay),
                0.0,
                2.0 * math.pi,
                8,
            )
            return inner * ct * st

        val = integrate(ring, 0.0, math.pi / 2.0, 40)
        assert abs(val - 1.0) < 1e-3


def test_forms_agree() -> None:
    rng = random.Random(1)
    for _ in range(200):
        alpha = rng.uniform(0.05, 1.5)
        t = rng.uniform(0.0, 1.5)
        st, ct = math.sin(t), math.cos(t)
        p = rng.uniform(0.0, 2.0 * math.pi)
        d = ggx_d(ct, alpha)
        assert abs(ggx_d_slope(ct, alpha) - d) < 1e-9 * d
        assert abs(ggx_d_aniso((st * math.cos(p), st * math.sin(p), ct), alpha, alpha) - d) < 1e-9 * d


def test_peak_and_tail() -> None:
    for alpha in (0.1, 0.3, 0.7):
        assert abs(ggx_d(1.0, alpha) - 1.0 / (math.pi * alpha * alpha)) < 1e-9
        assert abs(beckmann_d(1.0, alpha) - ggx_d(1.0, alpha)) < 1e-9
    # Values on the page, alpha = 0.3.
    assert abs(ggx_d(math.cos(math.radians(30.0)), 0.3) - 0.28419) < 1e-5
    assert abs(beckmann_d(math.cos(math.radians(30.0)), 0.3) - 0.15488) < 1e-5
    # The tail of GGX is longer: past some angle it is above Beckmann.
    for deg in (45.0, 60.0, 75.0):
        c = math.cos(math.radians(deg))
        assert ggx_d(c, 0.3) > 100.0 * beckmann_d(c, 0.3)
    # D falls like cos^-4 / tan^4 far from the peak: D sin^4 tends to alpha^2 / pi.
    c = math.cos(math.radians(89.99))
    assert abs(ggx_d(c, 0.3) * (1.0 - c * c) ** 2 - 0.09 / math.pi) < 1e-6


def test_sampling_matches_cdf() -> None:
    rng = random.Random(2)
    n = 20000
    for alpha in (0.1, 0.5):
        thetas = sorted(math.acos(min(1.0, sample_ggx(rng, alpha)[2])) for _ in range(n))
        ks = max(abs((i + 1) / n - cdf_theta(t, alpha)) for i, t in enumerate(thetas))
        assert ks < 1.63 / math.sqrt(n)  # the 1 percent level of the Kolmogorov test


def test_monte_carlo_normalization() -> None:
    # Uniform directions on the hemisphere: E[2 pi D(h) (n.h)] = 1.
    rng = random.Random(3)
    n = 40000
    alpha = 0.5
    vals = []
    for _ in range(n):
        cos_h = rng.random()  # uniform on the hemisphere has a uniform cos
        vals.append(2.0 * math.pi * ggx_d(cos_h, alpha) * cos_h)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / (n - 1)
    assert abs(mean - 1.0) < 4.0 * math.sqrt(var / n)
