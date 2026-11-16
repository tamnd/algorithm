# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tracking-learning-detection/. The authors are listed in prov/CCWPAB.jsonl.

import math
import random

from tracking_learning_detection import (
    TLD,
    Ferns,
    NearestNeighbor,
    box_variance,
    integral_images,
    iou,
    median_flow,
    patch,
)


def texture(seed, k, lo, hi):
    rng = random.Random(seed)
    blobs = [(rng.uniform(lo, hi), rng.uniform(lo, hi), rng.uniform(1.5, 3), rng.uniform(-80, 80))
             for _ in range(k)]

    def f(u, v):
        return 120 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in blobs)

    return f


def render(f, n, du=0.0, dv=0.0):
    return [[f(u - du, v - dv) for u in range(n)] for v in range(n)]


def test_iou():
    assert abs(iou((0, 0, 2, 2), (1, 1, 3, 3)) - 1 / 7) < 1e-12
    assert abs(iou((0, 0, 2, 2), (1, 0, 3, 2)) - 1 / 3) < 1e-12
    assert iou((0, 0, 2, 2), (2, 0, 4, 2)) == 0.0
    assert iou((1, 2, 5, 7), (1, 2, 5, 7)) == 1.0


def test_box_variance_by_integral_images():
    rng = random.Random(1)
    img = [[rng.randint(0, 255) for _ in range(13)] for _ in range(9)]
    tables = integral_images(img)
    for _ in range(50):
        x1, x2 = sorted(rng.sample(range(14), 2))
        y1, y2 = sorted(rng.sample(range(10), 2))
        vals = [img[v][u] for v in range(y1, y2) for u in range(x1, x2)]
        mean = sum(vals) / len(vals)
        want = sum((t - mean) ** 2 for t in vals) / len(vals)
        assert abs(box_variance(tables, (x1, y1, x2, y2)) - want) < 1e-6


def test_median_flow_follows_a_translation():
    f = texture(2, 60, -4, 40)
    a, b = render(f, 36), render(f, 36, 1.5, -1.0)
    box = (10, 12, 24, 26)
    got = median_flow(a, b, box)
    want = (11.5, 11.0, 25.5, 25.0)
    assert max(abs(s - t) for s, t in zip(got, want)) < 0.1


def test_median_flow_ignores_an_occluded_part():
    f = texture(3, 60, -4, 40)
    a, b = render(f, 36), render(f, 36, 1.0, 1.0)
    for v in range(10, 30):
        for u in range(8, 15):
            b[v][u] = 40.0  # a flat occluder over the left part of the box
    got = median_flow(a, b, (10, 12, 24, 26))
    want = (11.0, 13.0, 25.0, 27.0)
    assert max(abs(s - t) for s, t in zip(got, want)) < 0.3


def test_nearest_neighbor_similarities():
    rng = random.Random(4)
    img = [[rng.uniform(0, 255) for _ in range(20)] for _ in range(20)]
    p = patch(img, (2, 2, 12, 12))
    flipped = patch([[255 - t for t in row] for row in img], (2, 2, 12, 12))
    assert abs(NearestNeighbor.sim(p, p) - 1) < 1e-12
    assert abs(NearestNeighbor.sim(p, flipped)) < 1e-12
    nn = NearestNeighbor()
    nn.pos.append(p)
    assert nn.relative(patch(img, (8, 8, 18, 18))) == 1.0  # no negatives yet
    q = patch(img, (8, 8, 18, 18))
    nn.neg.append(q)
    assert abs(nn.relative(p) - 1 / (1 + NearestNeighbor.sim(p, q))) < 1e-12
    nn.pos.append(q)  # a newer positive is not used by the conservative similarity
    assert nn.relative(q) == 0.5
    assert nn.conservative(q) < 0.5


def test_fern_posterior_counts():
    ferns = Ferns(count=2, depth=2, seed=0)
    ferns.update([1, 3], True)
    ferns.update([1, 2], False)
    ferns.update([1, 3], True)
    assert ferns.posterior([1, 3]) == (2 / 3 + 1) / 2
    assert ferns.posterior([0, 2]) == 0.0


def test_tracks_loses_and_finds_the_target_again():
    n, side = 40, 10
    rng = random.Random(2)
    pix = [[rng.choice([30, 90, 160, 230]) for _ in range(side)] for _ in range(side)]
    back = render(texture(1, 12, 0, n), n)

    def frame(pos):
        img = [row[:] for row in back]
        for v in range(28, 38):  # two textured distractors
            for u in range(2, 14):
                img[v][u] = 40 if (u // 2 + v // 2) % 2 else 220
        for v in range(2, 14):
            for u in range(28, 38):
                img[v][u] = 40 if (u // 3) % 2 else 220
        if pos:
            for j in range(side):
                for i in range(side):
                    img[pos[1] + j][pos[0] + i] = pix[j][i]
        else:
            for v in range(3, 25):  # a flat occluder over the target
                for u in range(9, 31):
                    img[v][u] = 128.0
        return img

    truth = [(6 + 2 * t, 4 + t) for t in range(5)] + [None, None, (26, 22), (25, 24)]
    frames = [frame(p) for p in truth]
    tld = TLD(frames[0], (6, 4, 16, 14))
    for k in range(1, len(frames)):
        box = tld.update(frames[k - 1], frames[k])
        if truth[k] is None:
            assert box is None and not tld.valid
        else:
            x, y = truth[k]
            assert iou(box, (x, y, x + side, y + side)) > 0.85
            assert tld.valid
