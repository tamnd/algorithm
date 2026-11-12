# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vector-quantization/. The authors are listed in prov/ERP96S.jsonl.

import math
import random

from vector_quantization import (
    HEXAGON_CELL_AREA,
    HEXAGON_G,
    SQRT3,
    TreeVQ,
    dist2,
    distortion,
    hexagonal_nearest,
    lbg,
    lloyd,
    mean,
    nearest,
)


def correlated_gaussian(seed: int, n: int, rho: float = 0.9):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        a = rng.gauss(0, 1)
        out.append((a, rho * a + math.sqrt(1 - rho * rho) * rng.gauss(0, 1)))
    return out


def test_worked_example() -> None:
    data = [(0, 0), (1, 0), (0, 1), (4, 4), (5, 4), (4, 5)]
    cb, per_size = lbg(data, 2)
    assert sorted((round(a, 9), round(b, 9)) for a, b in cb) == [(round(1 / 3, 9),) * 2, (round(13 / 3, 9),) * 2]
    assert abs(per_size[0] - sum(dist2(x, (7 / 3, 7 / 3)) for x in data) / 6) < 1e-12
    assert abs(per_size[0] - 76 / 9) < 1e-12
    assert abs(per_size[1] - 4 / 9) < 1e-12
    assert nearest((1.9, 2.0), cb) == nearest((0, 0), cb)


def test_distortion_never_increases() -> None:
    data = correlated_gaussian(1, 1500)
    rng = random.Random(5)
    start = rng.sample(data, 8)
    _, hist = lloyd(data, start, tol=0.0, max_iter=40)
    assert all(a >= b - 1e-12 for a, b in zip(hist, hist[1:]))
    _, per_size = lbg(data, 8)
    assert all(a >= b - 1e-12 for a, b in zip(per_size, per_size[1:]))


def test_fixed_point_meets_both_conditions() -> None:
    data = correlated_gaussian(3, 300)
    cb, _ = lloyd(data, data[:4], tol=0.0, max_iter=500)
    cells = [[] for _ in cb]
    for x in data:
        cells[nearest(x, cb)].append(x)
    for c, cell in zip(cb, cells):  # centroid condition
        assert cell and dist2(c, mean(cell)) < 1e-20


def test_vq_beats_scalar_quantization_at_same_rate() -> None:
    train = correlated_gaussian(1, 2000)
    test = correlated_gaussian(2, 2000)
    cb, _ = lbg(train, 4)  # 2 bits per vector, 1 bit per component
    vq = distortion(test, cb) / 2
    s = math.sqrt(2 / math.pi)  # Lloyd-Max with 2 levels per component, 1 bit each
    sq = distortion(test, [(a, b) for a in (-s, s) for b in (-s, s)]) / 2
    # Reverse water-filling on the eigenvalues 1.9 and 0.1 at 2 bits per vector.
    bound = (1.9 / 16 + 0.1) / 2
    assert bound < vq < 0.2 < 0.33 < sq
    # Along the main diagonal: the codewords lie near the line a = b.
    assert all(abs(a - b) < 0.1 for a, b in cb)


def test_one_dimension_is_lloyd_max() -> None:
    rng = random.Random(8)
    data = [(rng.gauss(0, 1),) for _ in range(4000)]
    cb, _ = lbg(data, 2)
    levels = sorted(c[0] for c in cb)
    assert abs(levels[0] + math.sqrt(2 / math.pi)) < 0.05 and abs(levels[1] - math.sqrt(2 / math.pi)) < 0.05


def test_tree_structured_vq() -> None:
    train = correlated_gaussian(1, 1000)
    test = correlated_gaussian(2, 1000)
    tree = TreeVQ(train, 3)
    leaves = tree.leaves()
    assert len(leaves) == 8
    tree_d = sum(dist2(x, tree.encode(x)) for x in test) / len(test)
    # Full search over the same codebook is never worse than the tree search.
    assert distortion(test, leaves) <= tree_d + 1e-12
    for x in test[:50]:
        assert tree.encode(x) in leaves


def test_hexagonal_lattice() -> None:
    rng = random.Random(3)
    # Nearest point agrees with a search over nearby lattice points.
    for _ in range(500):
        x, y = rng.uniform(-10, 10), rng.uniform(-10, 10)
        p = hexagonal_nearest(x, y)
        pts = [(i + 0.5 * (j % 2), j * SQRT3 / 2) for i in range(-13, 14) for j in range(-14, 15)]
        best = min(dist2((x, y), q) for q in pts)
        assert abs(dist2((x, y), p) - best) < 1e-12
    # Monte Carlo of the normalized second moment G = E|x - Q(x)|^2 / (2 V).
    n = 100000
    acc = 0.0
    for _ in range(n):
        x, y = rng.uniform(-50, 50), rng.uniform(-50, 50)
        acc += dist2((x, y), hexagonal_nearest(x, y))
    g = acc / n / (2 * HEXAGON_CELL_AREA)
    assert abs(g / HEXAGON_G - 1) < 0.01
    assert HEXAGON_G < 1 / 12
    assert abs(10 * math.log10((1 / 12) / HEXAGON_G) - 0.1671) < 1e-4  # dB gain over the square lattice
