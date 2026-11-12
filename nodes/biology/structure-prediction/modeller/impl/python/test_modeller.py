# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modeller/. The authors are listed in prov/1ZBXCP.jsonl.

import math
import random

from modeller import (
    CA_CA, conjugate_gradients, derive_restraints, dist, gradient, initial_model, modeller, objective,
)


def random_chain(rng: random.Random, n: int):
    """A C-alpha chain with steps of 3.8 A and no two non-neighbours closer than 4.5 A."""
    while True:
        x = [(0.0, 0.0, 0.0)]
        for _ in range(n - 1):
            for _ in range(200):
                u = [rng.gauss(0.0, 1.0) for _ in range(3)]
                nu = math.sqrt(sum(c * c for c in u))
                p = tuple(x[-1][k] + CA_CA * u[k] / nu for k in range(3))
                if all(dist(p, q) >= 4.5 for q in x[:-1]):
                    x.append(p)
                    break
            else:
                break
        if len(x) == n:
            return x


def restrained_drms(x, restraints) -> float:
    return math.sqrt(sum((dist(x[i], x[j]) - d0) ** 2 for i, j, d0, _ in restraints) / len(restraints))


def test_objective_is_negative_log_density() -> None:
    rng = random.Random(1)
    t = random_chain(rng, 8)
    r = derive_restraints(t, [(i, i) for i in range(8)], 8)
    x = [tuple(c + rng.gauss(0.0, 0.5) for c in p) for p in t]  # near the template, so no density underflows
    nll = 0.0
    for i, j, d0, s in r:
        d = dist(x[i], x[j])
        density = math.exp(-0.5 * ((d - d0) / s) ** 2) / (s * math.sqrt(2 * math.pi))
        nll -= math.log(density)
    const = sum(math.log(s * math.sqrt(2 * math.pi)) for _, _, _, s in r)
    assert abs(objective(x, r) - (nll - const)) <= 1e-9 * max(1.0, nll)


def test_gradient_matches_finite_differences() -> None:
    rng = random.Random(2)
    t = random_chain(rng, 7)
    r = derive_restraints(t, [(i, i) for i in range(7)], 7)
    x = [tuple(rng.uniform(-5, 5) for _ in range(3)) for _ in range(7)]
    g = gradient(x, r)
    h = 1e-6
    for i in range(7):
        for k in range(3):
            up = [list(p) for p in x]
            dn = [list(p) for p in x]
            up[i][k] += h
            dn[i][k] -= h
            fd = (objective(up, r) - objective(dn, r)) / (2 * h)
            assert abs(fd - g[i][k]) <= 1e-4 * max(1.0, abs(fd))


def test_restraints_come_from_aligned_pairs_only() -> None:
    rng = random.Random(3)
    t = random_chain(rng, 6)
    alignment = [(0, 0), (1, 1), (4, 3), (5, 4)]  # target residues 2 and 3 are an insertion
    r = derive_restraints(t, alignment, 6, cutoff=1e9)
    long_range = {(i, j) for i, j, _, s in r if s != 0.1}
    # Pairs of aligned target residues, without the chain neighbours (0, 1) and (4, 5).
    assert long_range == {(0, 4), (0, 5), (1, 4), (1, 5)}
    assert {(i, j) for i, j, _, s in r if s == 0.1} == {(i, i + 1) for i in range(5)}
    for i, j, d0, s in r:
        if (i, j) == (1, 4):
            assert d0 == dist(t[1], t[3])


def test_template_is_a_global_minimum() -> None:
    rng = random.Random(4)
    t = random_chain(rng, 9)
    r = derive_restraints(t, [(i, i) for i in range(9)], 9)
    assert objective(t, r) <= 1e-18
    assert max(abs(v) for row in gradient(t, r) for v in row) <= 1e-9


def test_cg_recovers_the_template_from_a_perturbed_start() -> None:
    for seed in range(4):
        rng = random.Random(10 + seed)
        t = random_chain(rng, 9)
        # All pairs restrained, so the template is rigid and F has an isolated minimum (up to motion).
        r = derive_restraints(t, [(i, i) for i in range(9)], 9, cutoff=1e9)
        x0 = [tuple(c + rng.gauss(0.0, 0.3) for c in p) for p in t]
        x = conjugate_gradients(x0, r)
        assert objective(x, r) <= 1e-8
        assert restrained_drms(x, r) <= 1e-3


def test_mirror_image_has_the_same_objective() -> None:
    rng = random.Random(5)
    t = random_chain(rng, 8)
    r = derive_restraints(t, [(i, i) for i in range(8)], 8)
    x = [tuple(rng.uniform(-5, 5) for _ in range(3)) for _ in range(8)]
    mirror = [(-p[0], p[1], p[2]) for p in x]
    assert abs(objective(x, r) - objective(mirror, r)) <= 1e-9


def test_full_pipeline_with_an_insertion() -> None:
    rng = random.Random(3)
    t = random_chain(rng, 8)
    alignment = [(i, i) for i in range(4)] + [(i + 2, i) for i in range(4, 8)]  # 2 inserted residues
    n = 10
    x0 = initial_model(t, alignment, n, random.Random(3))
    x, r = modeller(t, alignment, n, random.Random(3))
    assert objective(x, r) <= objective(x0, r)
    assert objective(x, r) <= 1.0
    for i in range(n - 1):
        assert abs(dist(x[i], x[i + 1]) - CA_CA) <= 0.05
