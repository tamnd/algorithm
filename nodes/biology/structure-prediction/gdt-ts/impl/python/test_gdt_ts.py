# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gdt-ts/. The authors are listed in prov/36CBME.jsonl.

import itertools
import math
import random

from gdt_ts import TS_CUTOFFS, gdt_counts, gdt_ha, gdt_ts, superpose


def helix(n):
    """An ideal alpha-helix C-alpha trace: radius 2.3 A, 100 degrees and 1.5 A per residue."""
    return [(2.3 * math.cos(math.radians(100 * i)), 2.3 * math.sin(math.radians(100 * i)), 1.5 * i) for i in range(n)]


def hinge(pts, k, deg):
    c = pts[k - 1]
    a = math.radians(deg)
    out = list(pts[:k])
    for p in pts[k:]:
        y, z = p[1] - c[1], p[2] - c[2]
        out.append((p[0], c[1] + y * math.cos(a) - z * math.sin(a), c[2] + y * math.sin(a) + z * math.cos(a)))
    return out


def apply(rot, t, pts):
    return [tuple(sum(rot[r][c] * p[c] for c in range(3)) + t[r] for r in range(3)) for p in pts]


def counts_at(rot, t, model, native, cutoffs):
    moved = apply(rot, t, model)
    ds = [math.dist(m, q) for m, q in zip(moved, native)]
    return [sum(1 for d in ds if d <= c) for c in cutoffs]


def random_rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(c * c for c in q))
    w, x, y, z = (c / n for c in q)
    return [[w * w + x * x - y * y - z * z, 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), w * w - x * x + y * y - z * z, 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), w * w - x * x - y * y + z * z]]


def test_example_of_the_page() -> None:
    native = helix(40)
    model = hinge(native, 30, 40)
    counts = gdt_counts(model, native)
    assert counts == [31, 34, 38, 40]
    assert abs(gdt_ts(model, native) - 89.375) < 1e-9
    r, t = superpose(model, native)
    assert counts_at(r, t, model, native, TS_CUTOFFS) == [10, 26, 37, 40]
    r, t = superpose(model[:30], native[:30])
    core = counts_at(r, t, model, native, TS_CUTOFFS)
    assert all(a >= b for a, b in zip(counts, core))


def test_edges() -> None:
    native = helix(10)
    assert abs(gdt_ts(native, native) - 100.0) < 1e-9
    assert abs(gdt_ha(native, native) - 100.0) < 1e-9
    assert abs(gdt_ts(native, native, length=20) - 50.0) < 1e-9
    try:
        gdt_counts(native[:2], native[:2])
        assert False
    except ValueError:
        pass


def test_against_exhaustive_subset_fits() -> None:
    """The search fits only subsets of at least 3 residues, so each count is at most the
    best over all such subsets, and at least the count of the fit on all residues."""
    rng = random.Random(12)
    for _ in range(500):
        n = rng.randint(3, 6)
        native = [tuple(rng.uniform(-6, 6) for _ in range(3)) for _ in range(n)]
        noise = rng.choice([0.3, 1.0, 2.5, 5.0])
        model = [tuple(c + rng.gauss(0, noise) for c in p)
                 for p in apply(random_rotation(rng), (2.0, -1.0, 0.5), native)]
        counts = gdt_counts(model, native)
        assert counts == sorted(counts)
        r_all, t_all = superpose(model, native)
        full = counts_at(r_all, t_all, model, native, TS_CUTOFFS)
        assert all(a >= b for a, b in zip(counts, full))
        best = [0] * 4
        for k in range(3, n + 1):
            for sub in itertools.combinations(range(n), k):
                r, t = superpose([model[i] for i in sub], [native[i] for i in sub])
                best = [max(a, b) for a, b in zip(best, counts_at(r, t, model, native, TS_CUTOFFS))]
        assert all(a <= b for a, b in zip(counts, best))


def test_planted_core() -> None:
    rng = random.Random(4)
    for _ in range(25):
        n = rng.randint(15, 30)
        native = [tuple(rng.uniform(-12, 12) for _ in range(3)) for _ in range(n)]
        core = rng.randint(n // 2, n - 2)
        model = apply(random_rotation(rng), (3.0, 3.0, 3.0), native)
        model = model[:core] + [tuple(c + rng.uniform(10, 20) for c in p) for p in model[core:]]
        counts = gdt_counts(model, native)
        assert counts[0] >= core
