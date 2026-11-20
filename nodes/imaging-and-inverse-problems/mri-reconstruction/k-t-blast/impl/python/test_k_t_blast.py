# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/k-t-blast/. The authors are listed in prov/MVRMMT.jsonl.

import cmath
import math
import random

from imgla import solve
from k_t_blast import (
    acquire,
    alias_groups,
    k_t_blast,
    lattice_mask,
    time_ft,
    time_ift,
    training_power,
    unfold_group,
    xf_alias,
)


def rand_c(rng):
    return complex(rng.gauss(0, 1), rng.gauss(0, 1))


def rand_series(rng, nt, n):
    return [[rand_c(rng) for _ in range(n)] for _ in range(nt)]


def rel_err(u, v):
    num = sum(abs(a - b) ** 2 for fu, fv in zip(u, v) for a, b in zip(fu, fv))
    return math.sqrt(num / sum(abs(b) ** 2 for fv in v for b in fv))


def unitary_dft(x):
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) / math.sqrt(n) for k in range(n)]


def test_lattice_mask():
    m = lattice_mask(8, 4, 4, 1)
    assert [k for k in range(8) if m[2][k]] == [2, 6]
    assert all(sum(m[t][k] for t in range(4)) == 1 for k in range(8))
    for bad in ((8, 4, 4, 2), (6, 4, 4, 1)):
        try:
            lattice_mask(*bad)
            assert False
        except ValueError:
            pass


def test_alias_formula_by_brute_force():
    rng = random.Random(1)
    n, nt, r, shift = 8, 6, 2, 1
    x = rand_series(rng, nt, n)
    coils = [[rand_c(rng) for _ in range(n)] for _ in range(2)]
    mask = lattice_mask(n, nt, r, shift)
    for maps in (None, coils):
        alias = xf_alias(acquire(x, mask, maps))
        for c, cmap in enumerate(maps or [[1.0] * n]):
            weighted = [[cmap[y] * x[t][y] for y in range(n)] for t in range(nt)]
            # rho(y, f) by a direct sum, not by the code under test.
            rho = [[unitary_dft([weighted[t][y] for t in range(nt)])[f] for y in range(n)] for f in range(nt)]
            for y in range(n):
                for f in range(nt):
                    want = sum(rho[(f + j * shift * nt // r) % nt][(y + j * n // r) % n] for j in range(r)) / r
                    assert abs(alias[c][f][y] - want) < 1e-12


def test_groups_partition_the_grid():
    for n, nt, r, shift in ((8, 4, 2, 1), (12, 6, 3, 2), (16, 8, 4, 3)):
        seen = [p for g in alias_groups(n, nt, r, shift) for p in g]
        assert len(seen) == n * nt and len(set(seen)) == n * nt


def test_time_transform_round_trip():
    rng = random.Random(2)
    x = rand_series(rng, 6, 5)
    assert rel_err(time_ift(time_ft(x)), x) < 1e-14


def test_unfold_group_woodbury_form():
    rng = random.Random(3)
    nc, r, psi = 3, 2, 0.3
    a = [[rand_c(rng) for _ in range(r)] for _ in range(nc)]
    power = [0.7, 2.5]
    v = [rand_c(rng) for _ in range(nc)]
    got = unfold_group(a, power, psi, v)
    # (A^H A / psi + P^(-1))^(-1) A^H v / psi
    lhs = [[sum(a[i][p].conjugate() * a[i][q] for i in range(nc)) / psi + (1 / power[p] if p == q else 0) for q in range(r)] for p in range(r)]
    rhs = [sum(a[i][p].conjugate() * v[i] for i in range(nc)) / psi for p in range(r)]
    want = solve(lhs, rhs)
    assert max(abs(g - w) for g, w in zip(got, want)) < 1e-12
    assert unfold_group(a, [0.0, 0.0], 0.0, v) == [0j, 0j]


def test_one_signal_point_per_group_is_exact():
    n, nt, r, shift = 8, 8, 2, 1
    points = {(1, 1): 0.8, (6, 3): -0.5j, (3, 6): 0.4 + 0.2j}
    groups = alias_groups(n, nt, r, shift)
    owner = {p: i for i, g in enumerate(groups) for p in g}
    assert len({owner[p] for p in points}) == len(points)
    rho = [[0j] * n for _ in range(nt)]
    for (y, f), val in points.items():
        rho[f][y] = val
    dyn = time_ift(rho)
    x = [[dyn[t][y] + (1.0 if 2 <= y < 6 else 0.0) for y in range(n)] for t in range(nt)]
    mask = lattice_mask(n, nt, r, shift)
    out = k_t_blast(acquire(x, mask), mask, r, shift, training_power(x), 1e-12)
    assert rel_err(out, x) < 1e-9


def test_k_t_sense_with_r_coils_is_exact():
    rng = random.Random(4)
    n, nt, r = 8, 4, 2
    x = rand_series(rng, nt, n)
    coils = [[rand_c(rng) for _ in range(n)] for _ in range(r)]
    mask = lattice_mask(n, nt, r, 1)
    flat = [[1.0] * n for _ in range(nt)]
    out = k_t_blast(acquire(x, mask, coils), mask, r, 1, flat, 1e-13, coils, False)
    assert rel_err(out, x) < 1e-6


def test_full_sampling_and_static_series():
    rng = random.Random(5)
    n, nt = 6, 4
    x = rand_series(rng, nt, n)
    mask = lattice_mask(n, nt, 1, 1)
    out = k_t_blast(acquire(x, mask), mask, 1, 1, [[1.0] * n for _ in range(nt)], 1e-13, None, False)
    assert rel_err(out, x) < 1e-10
    static = [x[0]] * 4
    mask = lattice_mask(n, nt, 2, 1)
    zero = [[0.0] * n for _ in range(nt)]
    out = k_t_blast(acquire(static, mask), mask, 2, 1, zero, 0.1)
    assert rel_err(out, static) < 1e-12


def test_training_beats_a_flat_prior():
    n, nt, r = 32, 16, 4
    x = []
    for t in range(nt):
        a = 12 - 2.5 * math.cos(2 * math.pi * t / nt)
        b = 20 + 2.5 * math.cos(2 * math.pi * t / nt)
        frame = [0j] * n
        for y in range(4, 28):
            frame[y] = 1.0 + 1.0 / (1 + math.exp(-(y - a) / 0.6)) - 1.0 / (1 + math.exp(-(y - b) / 0.6))
        for y in range(24, 27):
            frame[y] += 0.5 * t / nt
        x.append(frame)
    mask = lattice_mask(n, nt, r, 1)
    data = acquire(x, mask)
    train = []
    for frame in x:
        k = unitary_dft(frame)
        k = [v if min(i, n - i) < 4 else 0j for i, v in enumerate(k)]
        train.append([sum(k[i] * cmath.exp(2j * math.pi * i * y / n) for i in range(n)) / math.sqrt(n) for y in range(n)])
    with_training = rel_err(k_t_blast(data, mask, r, 1, training_power(train), 1e-6), x)
    flat = rel_err(k_t_blast(data, mask, r, 1, [[1.0] * n for _ in range(nt)], 1e-9), x)
    assert with_training < 0.06 and flat > 0.13
