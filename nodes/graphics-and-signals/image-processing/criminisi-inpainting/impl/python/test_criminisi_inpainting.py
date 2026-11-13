# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/criminisi-inpainting/. The authors are listed in prov/9PPPZC.jsonl.

import math
import random

import pytest

from criminisi_inpainting import criminisi_inpaint, priority


def brute_priority(img, filled, conf, x, y, r, alpha):
    """P = C D written out from the definitions, with no helper of the module."""
    h, w = len(img), len(img[0])
    box = [(qx, qy) for qy in range(y - r, y + r + 1) for qx in range(x - r, x + r + 1)
           if 0 <= qx < w and 0 <= qy < h]
    c = sum(conf[qy][qx] for qx, qy in box if filled[qy][qx]) / len(box)

    def known(qx, qy):
        return 0 <= qx < w and 0 <= qy < h and filled[qy][qx]

    def d1(qx, qy, ax, ay):
        lo, hi = known(qx - ax, qy - ay), known(qx + ax, qy + ay)
        if lo and hi:
            return (img[qy + ay][qx + ax] - img[qy - ay][qx - ax]) / 2
        if hi:
            return img[qy + ay][qx + ax] - img[qy][qx]
        if lo:
            return img[qy][qx] - img[qy - ay][qx - ax]
        return 0.0

    grads = [(d1(qx, qy, 1, 0), d1(qx, qy, 0, 1)) for qx, qy in box if filled[qy][qx]]
    gx, gy = 0.0, 0.0
    if grads:
        big = max(u * u + v * v for u, v in grads)
        gx, gy = next(g for g in grads if g[0] ** 2 + g[1] ** 2 == big)

    def hole(qx, qy):
        if not (0 <= qx < w and 0 <= qy < h):
            qx, qy = x, y
        return 0 if filled[qy][qx] else 1

    nx, ny = hole(x + 1, y) - hole(x - 1, y), hole(x, y + 1) - hole(x, y - 1)
    size = math.hypot(nx, ny)
    d = 0.0 if size == 0 else abs(-gy * nx + gx * ny) / size / alpha
    return c * d, c


def random_case(rng):
    r = rng.choice([0, 1, 1, 2])
    w, h = rng.randint(2 * r + 2, 9), rng.randint(2 * r + 2, 9)
    levels = rng.choice([2, 4, 256])
    img = [[rng.randrange(levels) * (255 // (levels - 1)) for _ in range(w)] for _ in range(h)]
    if rng.random() < 0.5:
        # an image with structure: a few vertical or diagonal bands
        k, slant = rng.randint(2, 4), rng.randint(0, 1)
        img = [[(x + slant * y) // k % 2 * 200 for x in range(w)] for y in range(h)]
    x0, y0 = rng.randrange(w), rng.randrange(h)
    x1, y1 = min(w - 1, x0 + rng.randint(0, 3)), min(h - 1, y0 + rng.randint(0, 3))
    mask = [[x0 <= x <= x1 and y0 <= y <= y1 for x in range(w)] for y in range(h)]
    for _ in range(rng.randint(0, 3)):
        mask[rng.randrange(h)][rng.randrange(w)] = True
    return img, mask, r


def has_source(mask, r):
    h, w = len(mask), len(mask[0])
    return any(all(not mask[qy][qx] for qy in range(y - r, y + r + 1) for qx in range(x - r, x + r + 1))
               for y in range(r, h - r) for x in range(r, w - r))


def test_random_against_brute_force():
    rng = random.Random(2004)
    done = 0
    while done < 500:
        img, mask, r = random_case(rng)
        if not has_source(mask, r):
            continue
        h, w = len(img), len(img[0])
        trace = []
        out = criminisi_inpaint(img, mask, radius=r, trace=trace)
        # known pixels never change, and every pixel gets a value from a source pixel
        for y in range(h):
            for x in range(w):
                if not mask[y][x]:
                    assert out[y][x] == img[y][x]
        assert len(trace) <= sum(map(sum, mask))
        for im, filled, conf, p, q in trace:
            fr = [(x, y) for y in range(h) for x in range(w) if not filled[y][x] and any(
                0 <= x + dx < w and 0 <= y + dy < h and filled[y + dy][x + dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            assert p in fr
            pr = {f: brute_priority(im, filled, conf, f[0], f[1], r, 255.0) for f in fr}
            best = max(pr.values())
            assert pr[p][0] >= best[0] - 1e-12
            assert priority(im, filled, conf, p[0], p[1], r, 255.0)[0] == pytest.approx(pr[p][0], abs=1e-12)
            # the exemplar is a source patch with the least SSD over the filled pixels
            def ssd(c):
                s = 0
                for dy in range(-r, r + 1):
                    for dx in range(-r, r + 1):
                        ax, ay = p[0] + dx, p[1] + dy
                        if 0 <= ax < w and 0 <= ay < h and filled[ay][ax]:
                            s += (im[ay][ax] - im[c[1] + dy][c[0] + dx]) ** 2
                return s
            cands = [(cx, cy) for cy in range(r, h - r) for cx in range(r, w - r)
                     if all(not mask[cy + dy][cx + dx] for dy in range(-r, r + 1) for dx in range(-r, r + 1))]
            assert q in cands
            assert ssd(q) == min(ssd(c) for c in cands)
        done += 1


def test_fill_order_is_best_first():
    # on a random case the order of the chosen pixels follows the recomputed maximum priority
    rng = random.Random(77)
    for _ in range(100):
        img, mask, r = random_case(rng)
        if not has_source(mask, r):
            continue
        trace = []
        criminisi_inpaint(img, mask, radius=r, trace=trace)
        h, w = len(img), len(img[0])
        for im, filled, conf, p, _ in trace:
            fr = [(x, y) for y in range(h) for x in range(w) if not filled[y][x] and any(
                0 <= x + dx < w and 0 <= y + dy < h and filled[y + dy][x + dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
            vals = [priority(im, filled, conf, f[0], f[1], r, 255.0)[:2] for f in fr]
            top = max(vals)
            assert vals[fr.index(p)] == top
            assert fr.index(p) == vals.index(top)


def test_page_example():
    w, h = 9, 8
    img = [[200 if x == 4 else 40 for x in range(w)] for y in range(h)]
    mask = [[3 <= x <= 5 and 2 <= y <= 4 for x in range(w)] for y in range(h)]
    work = [[0 if mask[y][x] else img[y][x] for x in range(w)] for y in range(h)]
    trace = []
    out = criminisi_inpaint(work, mask, radius=1, trace=trace)
    assert out == img
    assert [t[3] for t in trace] == [(3, 2), (5, 2), (5, 4), (3, 4)]
    assert [t[4] for t in trace] == [(3, 6), (5, 6), (5, 6), (3, 6)]
    im, filled, conf, _, _ = trace[0]
    p, c, d = priority(im, filled, conf, 3, 2, 1, 255.0)
    assert c == pytest.approx(5 / 9) and d == pytest.approx(80 / math.sqrt(2) / 255)
    p, c, d = priority(im, filled, conf, 4, 2, 1, 255.0)
    assert c == pytest.approx(3 / 9) and d == pytest.approx(80 / 255)
    assert priority(im, filled, conf, 3, 3, 1, 255.0)[2] == 0


def test_stripes_are_rebuilt():
    for k in (1, 2):
        w, h = 12, 12
        img = [[(x // k) % 2 * 255 for x in range(w)] for y in range(h)]
        mask = [[4 <= x <= 7 and 3 <= y <= 6 for x in range(w)] for y in range(h)]
        assert criminisi_inpaint(img, mask, radius=1) == img
        assert criminisi_inpaint(img, mask, radius=k) == img


def test_edges():
    img = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    none = [[False] * 3 for _ in range(3)]
    assert criminisi_inpaint(img, none, radius=1) == img
    one = [[False] * 3 for _ in range(3)]
    one[0][0] = True
    with pytest.raises(ValueError):
        criminisi_inpaint(img, one, radius=1)
    out = criminisi_inpaint(img, one, radius=0)
    assert out[0][0] in (2, 4) and out[1:] == img[1:]
    with pytest.raises(ValueError):
        criminisi_inpaint(img, [[False]], radius=1)
    with pytest.raises(ValueError):
        criminisi_inpaint([], [], radius=1)
