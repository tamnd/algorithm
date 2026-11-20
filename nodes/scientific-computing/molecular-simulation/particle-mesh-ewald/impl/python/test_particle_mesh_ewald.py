# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-mesh-ewald/. The authors are listed in prov/QV4418.jsonl.

import math
import random

from particle_mesh_ewald import fft, lagrange_weights, pme_reciprocal

BOX, ALPHA = 6.0, 0.8


def system(seed: int, n: int) -> tuple[list[float], list[list[float]]]:
    rng = random.Random(seed)
    pos = [[rng.uniform(0, BOX) for _ in range(3)] for _ in range(n)]
    q = [rng.uniform(-1, 1) for _ in range(n - 1)]
    q.append(-sum(q))
    return q, pos


def exact_reciprocal(q, pos, box, alpha, mmax):
    """The reciprocal Ewald sum term by term, the reference for PME."""
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


def test_fft_against_the_definition() -> None:
    rng = random.Random(11)
    a = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(16)]
    out = fft(a)
    for m in range(16):
        ref = sum(a[g] * complex(math.cos(2 * math.pi * m * g / 16), -math.sin(2 * math.pi * m * g / 16)) for g in range(16))
        assert abs(out[m] - ref) < 1e-12


def test_lagrange_weights_reproduce_polynomials() -> None:
    for p in (1, 2, 3):
        for u in (0.0, 0.3, 4.71, 9.99):
            first, w = lagrange_weights(u, p)
            for deg in range(2 * p):
                val = sum(wj * (first + j) ** deg for j, wj in enumerate(w))
                assert abs(val - u ** deg) < 1e-9 * max(1.0, u ** deg)


def test_error_falls_with_order_and_grid() -> None:
    q, pos = system(7, 8)
    e0, f0 = exact_reciprocal(q, pos, BOX, ALPHA, 9)
    errs = {}
    for k in (8, 16):
        for p in (1, 2, 3):
            e, f = pme_reciprocal(q, pos, BOX, ALPHA, k, p)
            errs[k, p] = (abs(e - e0) / abs(e0), rel_force_error(f, f0))
    for k in (8, 16):
        assert errs[k, 1][0] > errs[k, 2][0] > errs[k, 3][0]
        assert errs[k, 1][1] > errs[k, 2][1] > errs[k, 3][1]
    for p in (1, 2, 3):
        assert errs[16, p][0] < errs[8, p][0]
    assert errs[16, 3][0] < 2e-3 and errs[16, 3][1] < 1e-3


def test_reciprocal_forces_sum_to_zero() -> None:
    q, pos = system(8, 10)
    for k, p in ((8, 1), (8, 3), (16, 2)):
        _, f = pme_reciprocal(q, pos, BOX, ALPHA, k, p)
        for a in range(3):
            assert abs(sum(fi[a] for fi in f)) < 1e-12


def test_shift_by_one_grid_spacing_changes_nothing() -> None:
    q, pos = system(9, 6)
    e, f = pme_reciprocal(q, pos, BOX, ALPHA, 8, 2)
    shifted = [[x + BOX / 8 for x in p] for p in pos]
    e2, f2 = pme_reciprocal(q, shifted, BOX, ALPHA, 8, 2)
    assert abs(e - e2) < 1e-12
    assert rel_force_error(f2, f) < 1e-10
