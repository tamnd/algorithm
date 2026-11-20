# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-particle-mesh-ewald/. The authors are listed in prov/WR206R.jsonl.

import math
import random

from smooth_particle_mesh_ewald import bspline, bspline_moduli, spme_reciprocal

BOX, ALPHA = 6.0, 0.8


def system(seed: int, n: int) -> tuple[list[float], list[list[float]]]:
    rng = random.Random(seed)
    pos = [[rng.uniform(0, BOX) for _ in range(3)] for _ in range(n)]
    q = [rng.uniform(-1, 1) for _ in range(n - 1)]
    q.append(-sum(q))
    return q, pos


def exact_reciprocal(q, pos, box, alpha, mmax):
    """The reciprocal Ewald sum term by term, the reference for SPME."""
    vol = box ** 3
    e, f = 0.0, [[0.0] * 3 for _ in q]
    for mx in range(-mmax, mmax + 1):
        for my in range(-mmax, mmax + 1):
            for mz in range(-mmax, mmax + 1):
                if mx == my == mz == 0:
                    continue
                k = [2 * math.pi * m / box for m in (mx, my, mz)]
                k2 = sum(x * x for x in k)
                g = math.exp(-k2 / (4 * alpha * alpha)) / k2
                ph = [sum(a * b for a, b in zip(k, p)) for p in pos]
                sr = sum(qi * math.cos(t) for qi, t in zip(q, ph))
                si = sum(qi * math.sin(t) for qi, t in zip(q, ph))
                e += 2 * math.pi / vol * g * (sr * sr + si * si)
                for i in range(len(q)):
                    c = 4 * math.pi / vol * q[i] * g * (math.sin(ph[i]) * sr - math.cos(ph[i]) * si)
                    for a in range(3):
                        f[i][a] += c * k[a]
    return e, f


def rel_force_error(f, f0) -> float:
    num = sum((a - b) ** 2 for u, v in zip(f, f0) for a, b in zip(u, v))
    den = sum(a * a for u in f0 for a in u)
    return math.sqrt(num / den)


def test_bspline_values() -> None:
    # M_4 at the integers is 1/6, 4/6, 1/6, and the weights form a partition of unity
    vals, _ = bspline(0.0, 4)
    assert all(abs(a - b) < 1e-15 for a, b in zip(vals, [0.0, 1 / 6, 4 / 6, 1 / 6]))
    for n in (3, 4, 5, 6, 8):
        for w in (0.0, 0.25, 0.5, 0.9):
            vals, ders = bspline(w, n)
            assert abs(sum(vals) - 1.0) < 1e-14
            assert abs(sum(ders)) < 1e-14
            h = 1e-6
            vp, _ = bspline(w + h, n) if w + h < 1 else bspline(w, n)
            vm, _ = bspline(w - h, n) if w - h >= 0 else bspline(w, n)
            if 0 < w - h and w + h < 1:
                for j in range(n):
                    assert abs((vp[j] - vm[j]) / (2 * h) - ders[j]) < 1e-7


def test_moduli_vanish_only_for_odd_order_at_nyquist() -> None:
    assert bspline_moduli(8, 5)[4] == 0.0
    assert min(bspline_moduli(8, 4)) > 0.0
    assert abs(bspline_moduli(8, 4)[0] - 1.0) < 1e-14


def test_forces_are_the_exact_gradient_of_the_spme_energy() -> None:
    q, pos = system(7, 6)
    k, n = 8, 4
    _, f = spme_reciprocal(q, pos, BOX, ALPHA, k, n)
    h = 1e-6
    for i in range(len(q)):
        for a in range(3):
            pp = [list(p) for p in pos]
            pm = [list(p) for p in pos]
            pp[i][a] += h
            pm[i][a] -= h
            num = -(spme_reciprocal(q, pp, BOX, ALPHA, k, n)[0] - spme_reciprocal(q, pm, BOX, ALPHA, k, n)[0]) / (2 * h)
            assert abs(num - f[i][a]) < 1e-6 * max(1.0, abs(f[i][a]))


def test_error_falls_with_order_and_grid() -> None:
    q, pos = system(7, 8)
    e0, f0 = exact_reciprocal(q, pos, BOX, ALPHA, 9)
    errs = {}
    for k in (8, 16):
        for n in (4, 6, 8):
            e, f = spme_reciprocal(q, pos, BOX, ALPHA, k, n)
            errs[k, n] = (abs(e - e0) / abs(e0), rel_force_error(f, f0))
    for k in (8, 16):
        assert errs[k, 4][0] > errs[k, 6][0] > errs[k, 8][0]
        assert errs[k, 4][1] > errs[k, 6][1] > errs[k, 8][1]
    assert errs[16, 8][0] < 2e-6 and errs[16, 8][1] < 2e-5


def test_net_force_is_small_but_not_zero() -> None:
    q, pos = system(7, 8)
    _, f = spme_reciprocal(q, pos, BOX, ALPHA, 8, 4)
    norm = math.sqrt(sum(x * x for fi in f for x in fi))
    net = max(abs(sum(fi[a] for fi in f)) for a in range(3))
    assert 1e-8 < net < 0.1 * norm
