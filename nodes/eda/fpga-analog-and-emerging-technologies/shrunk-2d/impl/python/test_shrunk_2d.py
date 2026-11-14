# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shrunk-2d/. The authors are listed in prov/BTYXM7.jsonl.

import math
import random

from shrunk_2d import (
    SCALE,
    bin_diffs,
    bin_limits,
    cut_nets,
    fm_split,
    hpwl,
    initial_split,
    quadratic_place,
    shrink,
    shrunk_2d,
)


def random_design(rng, n, m, die=10.0):
    widths = [rng.choice([1.0, 1.0, 2.0]) for _ in range(n)]
    heights = [1.0] * n
    nets = []
    for i in range(n):
        if i % 3 == 0:
            nets.append(([i], [(rng.uniform(0, die), rng.choice([0.0, die]))]))
        else:
            nets.append(([i, (i + 1) % n], []))
    for _ in range(m):
        nets.append((rng.sample(range(n), rng.choice([2, 2, 3, 4])), []))
    return widths, heights, nets, die


def balanced(areas, bins, side, eps):
    limit = bin_limits(areas, bins, eps)
    return all(abs(d) <= limit[b] + 1e-12 for b, d in bin_diffs(areas, bins, side).items())


def brute_cut(areas, bins, nets, eps):
    n, best = len(areas), None
    for mask in range(1 << n):
        side = [(mask >> i) & 1 for i in range(n)]
        if balanced(areas, bins, side, eps):
            c = len(cut_nets(nets, side))
            best = c if best is None else min(best, c)
    return best


def test_page_example():
    # Cells a..h are 0..7, of unit area. a..d are in the left bin, e..h in the right one.
    areas = [1.0] * 8
    nets = [([0, 1, 2, 3], []), ([4, 5, 6, 7], []), ([3, 4], [])]
    per_bin = [0, 0, 0, 0, 1, 1, 1, 1]
    side = fm_split(areas, per_bin, nets, initial_split(areas, per_bin), eps=0.1)
    assert balanced(areas, per_bin, side, 0.1)
    assert len(cut_nets(nets, side)) == 2 == brute_cut(areas, per_bin, nets, 0.1)
    one_bin = [0] * 8
    assert brute_cut(areas, one_bin, nets, 0.0) == 1
    assert sorted(bin_limits(areas, per_bin, 0.1).values()) == [2.0, 2.0]


def test_shrink_scales_hpwl_by_one_over_root_two():
    rng = random.Random(3)
    for _ in range(5):
        w, h, nets, die = random_design(rng, 30, 40)
        n = len(w)
        x1, y1 = quadratic_place(n, nets, die)
        sw, sh, snets, sdie = shrink(w, h, nets, die)
        assert math.isclose(sum(a * b for a, b in zip(sw, sh)), sum(a * b for a, b in zip(w, h)) / 2)
        x2, y2 = quadratic_place(n, snets, sdie)
        for a, b in zip(x1 + y1, x2 + y2):
            assert math.isclose(b, a * SCALE, rel_tol=1e-9)
        ratio = hpwl(x2, y2, snets) / hpwl(x1, y1, nets)
        assert math.isclose(ratio, SCALE, rel_tol=1e-9)
        assert math.isclose(1 - ratio, 0.2929, abs_tol=1e-4)


def test_split_against_exhaustive_optimum():
    rng = random.Random(0)
    hits, worst = 0, 0
    for _ in range(200):
        n = rng.randint(6, 10)
        w, h, nets, die = random_design(rng, n, rng.randint(n, 2 * n))
        r = shrunk_2d(w, h, nets, die, k=2, eps=0.1)
        areas = [a * b for a, b in zip(w, h)]
        assert balanced(areas, r["bins"], r["side"], 0.1)
        opt = brute_cut(areas, r["bins"], nets, 0.1)
        got = len(r["mivs"])
        assert got >= opt
        hits += got == opt
        worst = max(worst, got - opt)
    assert hits == 180
    assert worst == 3


def test_fm_keeps_balance_and_never_raises_the_cut():
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randint(4, 40)
        areas = [rng.choice([1.0, 2.0, 3.0]) for _ in range(n)]
        bins = [rng.randrange(4) for _ in range(n)]
        nets = [(rng.sample(range(n), rng.randint(2, min(5, n))), []) for _ in range(n)]
        eps = rng.choice([0.0, 0.1, 0.3])
        start = initial_split(areas, bins)
        assert balanced(areas, bins, start, eps)
        side = fm_split(areas, bins, nets, start, eps)
        assert balanced(areas, bins, side, eps)
        assert len(cut_nets(nets, side)) <= len(cut_nets(nets, start))


def test_one_miv_per_cut_net_inside_its_box():
    rng = random.Random(2)
    for _ in range(20):
        w, h, nets, die = random_design(rng, 25, 30)
        r = shrunk_2d(w, h, nets, die, k=3)
        assert r["die"] == die * SCALE
        cut = cut_nets(nets, r["side"])
        assert [e for e, _, _ in r["mivs"]] == cut
        for e, mx, my in r["mivs"]:
            cells, pads = nets[e]
            xs = [r["x"][c] for c in cells] + [p[0] * SCALE for p in pads]
            ys = [r["y"][c] for c in cells] + [p[1] * SCALE for p in pads]
            assert min(xs) <= mx <= max(xs) and min(ys) <= my <= max(ys)
