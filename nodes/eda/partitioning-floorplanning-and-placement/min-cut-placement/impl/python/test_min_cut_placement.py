# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-cut-placement/. The authors are listed in prov/S0NJTB.jsonl.

import random
from itertools import permutations

from min_cut_placement import fm_with_fixed, hpwl, min_cut_placement


def direct_hpwl(pos, nets) -> int:
    """HPWL by a direct sum over pairs of pins: the largest x gap plus the largest y gap."""
    total = 0
    for e in nets:
        total += max(abs(pos[a][0] - pos[b][0]) for a in e for b in e)
        total += max(abs(pos[a][1] - pos[b][1]) for a in e for b in e)
    return total


def crossings(pos, nets) -> int:
    """Sum over the lines x = j + 1/2 and y = j + 1/2 of the number of nets that cross the line."""
    xs = [p[0] for p in pos]
    ys = [p[1] for p in pos]
    total = 0
    for j in range(min(xs) - 1, max(xs) + 1):
        total += sum(1 for e in nets if min(pos[p][0] for p in e) <= j < max(pos[p][0] for p in e))
    for j in range(min(ys) - 1, max(ys) + 1):
        total += sum(1 for e in nets if min(pos[p][1] for p in e) <= j < max(pos[p][1] for p in e))
    return total


def brute_force(n, nets, pads, width, height) -> int:
    sites = [(x, y) for x in range(width) for y in range(height)]
    best = None
    for perm in permutations(sites, n):
        h = hpwl(list(perm) + list(pads), nets)
        if best is None or h < best:
            best = h
    return best


def random_instance(rng, n, width, height, m):
    q = rng.randint(0, 3)
    pads = []
    for _ in range(q):
        if rng.random() < 0.5:
            pads.append((rng.choice([-1, width]), rng.randrange(height)))
        else:
            pads.append((rng.randrange(width), rng.choice([-1, height])))
    pins = n + q
    nets = []
    for _ in range(m):
        size = rng.choice([2, 2, 3, 3, 4])
        e = rng.sample(range(pins), min(size, pins))
        if any(p < n for p in e) and len(e) >= 2:
            nets.append(e)
    return pads, nets


def check_legal(pos, n, width, height):
    assert len(pos) == n
    assert len(set(pos)) == n
    for x, y in pos:
        assert 0 <= x < width and 0 <= y < height


def page_example():
    # 8 cells on a 4 x 2 grid, pad 8 at the left (x = -1) and pad 9 at the right (x = 4).
    nets = [[8, 0], [0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [3, 4], [4, 5], [4, 6], [5, 6], [5, 7], [6, 7], [7, 9]]
    pads = [(-1, 0), (4, 1)]
    return 8, nets, pads, 4, 2


def test_page_example():
    n, nets, pads, w, h = page_example()
    pos = min_cut_placement(n, nets, pads, w, h, random.Random(1))
    check_legal(pos, n, w, h)
    full = pos + pads
    assert hpwl(full, nets) == direct_hpwl(full, nets) == crossings(full, nets)
    assert hpwl(full, nets) >= brute_force(n, nets, pads, w, h)


def test_hpwl_identity_and_direct_sum():
    rng = random.Random(3)
    for _ in range(300):
        n = rng.randint(1, 8)
        w, h = rng.randint(1, 4), rng.randint(1, 4)
        if n > w * h:
            continue
        pads, nets = random_instance(rng, n, w, h, rng.randint(0, 10))
        sites = rng.sample([(x, y) for x in range(w) for y in range(h)], n)
        full = sites + pads
        assert hpwl(full, nets) == direct_hpwl(full, nets) == crossings(full, nets)


def test_fm_with_fixed_keeps_balance_and_never_worse():
    rng = random.Random(9)
    for _ in range(300):
        k = rng.randint(1, 9)
        nets = []
        for _ in range(rng.randint(0, 12)):
            e = sorted(set(rng.sample(range(k + 2), min(k + 2, rng.randint(2, 4)))))
            if any(v < k for v in e):
                nets.append(e)
        t = rng.randint(0, k)
        side = [0] * t + [1] * (k - t)
        rng.shuffle(side)
        fixed = {k: 0, k + 1: 1}

        def cut(s):
            full = list(s) + [0, 1]
            return sum(1 for e in nets if len({full[v] for v in e}) == 2)

        out = fm_with_fixed(k, nets, fixed, side, t, t)
        assert out.count(0) == t
        assert cut(out) <= cut(side)


def test_against_brute_force_on_small_grids():
    rng = random.Random(2026)
    for trial in range(120):
        w, h = rng.choice([(1, 3), (2, 2), (3, 1), (2, 3), (3, 2), (1, 5), (4, 1)])
        n = rng.randint(1, w * h)
        pads, nets = random_instance(rng, n, w, h, rng.randint(1, 8))
        for tp in (True, False):
            pos = min_cut_placement(n, nets, pads, w, h, random.Random(trial), terminal_propagation=tp)
            check_legal(pos, n, w, h)
            full = pos + pads
            got = hpwl(full, nets)
            assert got == direct_hpwl(full, nets) == crossings(full, nets)
            assert got >= brute_force(n, nets, pads, w, h)


def test_larger_grid_is_legal():
    rng = random.Random(4)
    for _ in range(10):
        w, h = rng.randint(3, 6), rng.randint(3, 6)
        n = rng.randint(1, w * h)
        pads, nets = random_instance(rng, n, w, h, 2 * n)
        pos = min_cut_placement(n, nets, pads, w, h, rng)
        check_legal(pos, n, w, h)
