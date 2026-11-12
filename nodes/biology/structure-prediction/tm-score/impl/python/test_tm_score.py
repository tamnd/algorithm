# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tm-score/. The authors are listed in prov/NQBJJN.jsonl.

import itertools
import math
import random

from tm_score import d0_of_length, superpose, tm_score


def helix(n):
    """An ideal alpha-helix C-alpha trace: radius 2.3 A, 100 degrees and 1.5 A per residue."""
    return [(2.3 * math.cos(math.radians(100 * i)), 2.3 * math.sin(math.radians(100 * i)), 1.5 * i) for i in range(n)]


def hinge(pts, k, deg):
    """Turn residues k.. by deg degrees about the x direction through residue k - 1."""
    c = pts[k - 1]
    a = math.radians(deg)
    out = list(pts[:k])
    for p in pts[k:]:
        y, z = p[1] - c[1], p[2] - c[2]
        out.append((p[0], c[1] + y * math.cos(a) - z * math.sin(a), c[2] + y * math.sin(a) + z * math.cos(a)))
    return out


def apply(rot, t, pts):
    return [tuple(sum(rot[r][c] * p[c] for c in range(3)) + t[r] for r in range(3)) for p in pts]


def direct_tm(rot, t, model, native, length):
    """The definition, written out again: (1/L) sum 1 / (1 + (d_i/d0)^2)."""
    d0 = d0_of_length(length)
    moved = apply(rot, t, model)
    return sum(1.0 / (1.0 + math.dist(m, q) ** 2 / d0 ** 2) for m, q in zip(moved, native)) / length


def random_rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(c * c for c in q))
    w, x, y, z = (c / n for c in q)
    return [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]


def test_d0() -> None:
    assert d0_of_length(10) == 0.5 and d0_of_length(21) == 0.5
    assert abs(d0_of_length(40) - 1.8257819953839538) < 1e-12
    assert abs(d0_of_length(100) - (1.24 * 85 ** (1 / 3) - 1.8)) < 1e-12
    assert d0_of_length(22) > 0.5


def test_example_of_the_page() -> None:
    native = helix(40)
    model = hinge(native, 30, 40)
    r_all, t_all = superpose(model, native)
    moved = apply(r_all, t_all, model)
    rmsd = math.sqrt(sum(math.dist(m, q) ** 2 for m, q in zip(moved, native)) / 40)
    assert abs(rmsd - 2.2245) < 1e-4
    assert abs(direct_tm(r_all, t_all, model, native, 40) - 0.5647) < 1e-4
    sc, rot, t = tm_score(model, native)
    assert abs(sc - 0.7933) < 1e-4
    assert abs(sc - direct_tm(rot, t, model, native, 40)) < 1e-12
    moved = apply(rot, t, model)
    assert max(math.dist(m, q) for m, q in zip(moved[:30], native[:30])) < 1e-6


def test_edges() -> None:
    native = helix(12)
    sc, _, _ = tm_score(native, native)
    assert abs(sc - 1.0) < 1e-9
    sc2, _, _ = tm_score(native, native, length=24)  # normalized by a longer target
    assert abs(sc2 - 0.5) < 1e-9
    try:
        tm_score(native[:2], native[:2])
        assert False
    except ValueError:
        pass


def test_rigid_motion_does_not_change_the_score() -> None:
    rng = random.Random(3)
    native = helix(30)
    model = hinge(native, 18, 60)
    sc, _, _ = tm_score(model, native)
    moved = apply(random_rotation(rng), (5.0, -3.0, 2.0), model)
    sc2, _, _ = tm_score(moved, native)
    assert abs(sc - sc2) < 1e-9


def test_against_exhaustive_subset_fits() -> None:
    """The search fits only subsets of at least 3 residues, so it is at most the best
    over all such subsets, and at least the fit on all residues."""
    rng = random.Random(21)
    for _ in range(500):
        n = rng.randint(3, 6)
        native = [tuple(rng.uniform(-6, 6) for _ in range(3)) for _ in range(n)]
        r0 = random_rotation(rng)
        noise = rng.choice([0.3, 1.0, 3.0])
        model = [tuple(c + rng.gauss(0, noise) for c in p) for p in apply(r0, (1.0, 2.0, 3.0), native)]
        length = n + rng.randint(0, 30)
        sc, rot, t = tm_score(model, native, length=length)
        assert 0.0 < sc <= 1.0
        assert abs(sc - direct_tm(rot, t, model, native, length)) < 1e-9
        r_all, t_all = superpose(model, native)
        assert sc >= direct_tm(r_all, t_all, model, native, length) - 1e-12
        best = 0.0
        for k in range(3, n + 1):
            for sub in itertools.combinations(range(n), k):
                r, tt = superpose([model[i] for i in sub], [native[i] for i in sub])
                best = max(best, direct_tm(r, tt, model, native, length))
        assert sc <= best + 1e-9


def test_planted_core_is_found() -> None:
    rng = random.Random(5)
    for _ in range(25):
        n = rng.randint(20, 36)
        native = [tuple(rng.uniform(-15, 15) for _ in range(3)) for _ in range(n)]
        core = rng.randint(n // 2, n - 3)
        r0 = random_rotation(rng)
        model = apply(r0, (4.0, 0.0, -2.0), native)
        model = model[:core] + [tuple(c + rng.uniform(5, 12) for c in p) for p in model[core:]]
        sc, _, _ = tm_score(model, native)
        r_core, t_core = superpose(model[:core], native[:core])
        assert sc >= direct_tm(r_core, t_core, model, native, n) - 1e-9
        assert sc >= core / n - 1e-9
