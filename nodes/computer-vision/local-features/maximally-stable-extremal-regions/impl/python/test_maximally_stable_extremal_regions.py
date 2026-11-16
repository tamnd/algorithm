# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximally-stable-extremal-regions/. The authors are listed in prov/C7478H.jsonl.

import random
from fractions import Fraction

from maximally_stable_extremal_regions import dark_regions, mser


def component(img, seed, inside):
    """The 4-connected component of the pixels where inside(value) holds that contains seed, by BFS."""
    h, w = len(img), len(img[0])
    if not inside(img[seed // w][seed % w]):
        return frozenset()
    seen, stack = {seed}, [seed]
    while stack:
        p = stack.pop()
        u, v = p % w, p // w
        for q, ok in ((p - 1, u > 0), (p + 1, u < w - 1), (p - w, v > 0), (p + w, v < h - 1)):
            if ok and q not in seen and inside(img[q // w][q % w]):
                seen.add(q)
                stack.append(q)
    return frozenset(seen)


def oracle(img, delta, levels):
    """Maximally stable dark regions from the definition, with components found by BFS at every level."""
    h, w = len(img), len(img[0])
    comps = []
    for g in range(levels):
        done, level = set(), []
        for p in range(h * w):
            if p not in done and img[p // w][p % w] <= g:
                c = component(img, p, lambda x, g=g: x <= g)
                done |= c
                level.append(c)
        comps.append(level)
    tracks = {}  # key (birth, seed) -> {level: region}
    current = {}  # region at the previous level -> key
    for g in range(levels):
        nxt = {}
        for c in comps[g]:
            children = [d for d in current if d <= c]
            if not children:
                key = (g, min(c))
                tracks[key] = {}
            else:
                key = min((current[d] for d in children),
                          key=lambda k: (-len(next(d for d in children if current[d] == k)), k))
            tracks[key][g] = c
            nxt[c] = key
        current = nxt
    out = []
    for (birth, seed), regs in tracks.items():
        last = max(regs)
        q = {}
        for g in range(birth, min(last, levels - 1 - delta) + 1):
            big = len(component(img, seed, lambda x: x <= g + delta))
            small = len(regs[g - delta]) if g - delta >= birth else 0
            q[g] = Fraction(big - small, len(regs[g]))
        gs = sorted(q)
        for i in range(1, len(gs) - 1):
            g = gs[i]
            if q[gs[i - 1]] <= q[g]:
                continue
            j = i
            while j + 1 < len(gs) and q[gs[j + 1]] == q[g]:
                j += 1
            if j + 1 < len(gs) and q[gs[j + 1]] > q[g]:
                out.append((g, seed, len(regs[g]), q[g]))
    return sorted(out)


def example():
    img = [[200] * 10 for _ in range(10)]
    for v in range(2, 8):
        for u in range(2, 8):
            img[v][u] = 120
    for v in range(3, 6):
        for u in range(3, 6):
            img[v][u] = 40
    img[4][4] = 30
    img[6][8] = 90
    img[8][1] = 150
    return img


def pixel_set(img, region, levels=256):
    pol, level, u, v, _ = region
    inside = (lambda x: x <= level) if pol == "dark" else (lambda x: x >= level)
    return component(img, v * len(img[0]) + u, inside)


def test_against_the_definition():
    rng = random.Random(2002)
    for _ in range(600):
        h, w, levels = rng.randint(1, 5), rng.randint(1, 5), rng.randint(4, 12)
        img = [[rng.randrange(levels) for _ in range(w)] for _ in range(h)]
        delta = rng.randint(1, 3)
        assert sorted(dark_regions(img, delta, levels)) == oracle(img, delta, levels)


def test_regions_are_the_reported_components():
    rng = random.Random(5)
    for _ in range(100):
        img = [[rng.randrange(8) for _ in range(6)] for _ in range(5)]
        for r in mser(img, delta=1, levels=8):
            assert len(pixel_set(img, r)) == r[4]


def test_worked_example():
    img = example()
    assert mser(img, delta=10) == [
        ("bright", 80, 0, 0, 91), ("bright", 110, 0, 0, 90), ("bright", 140, 0, 0, 63), ("bright", 190, 0, 0, 62),
        ("dark", 50, 4, 4, 9), ("dark", 100, 8, 6, 1), ("dark", 130, 4, 4, 37), ("dark", 160, 1, 8, 1)]
    q = {g: v for g, _, _, v in dark_regions(img, 10, 256)}
    assert q[50] == 0 and q[130] == 0
    assert mser(img, delta=10, min_area=4, max_area=50) == [("dark", 50, 4, 4, 9), ("dark", 130, 4, 4, 37)]


def test_flat_image_and_single_pixel():
    assert mser([[7] * 5 for _ in range(4)], delta=2) == []
    assert mser([[3]], delta=1, levels=8) == []


def test_offset_and_rotation():
    img = example()
    shifted = [[x + 10 for x in row] for row in img]
    a = [(p, lv + 10, u, v, s) for p, lv, u, v, s in mser(img, delta=10)]
    assert mser(shifted, delta=10) == a
    h, w = len(img), len(img[0])
    rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(w)]
    sets = {(r[0], r[1], frozenset((p % w, p // w) for p in pixel_set(img, r))) for r in mser(img, delta=10)}
    rsets = set()
    for r in mser(rot, delta=10):
        # rot pixel (u', v') holds img pixel (v', h - 1 - u')
        rsets.add((r[0], r[1], frozenset((p // h, h - 1 - p % h) for p in pixel_set(rot, r))))
    assert sets == rsets
