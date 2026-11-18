# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/texture-clipmap/. The authors are listed in prov/NPGSAB.jsonl.

import random
from fractions import Fraction

from texture_clipmap import Clipmap, build_mipmap, in_window, mip_sample, texel_counts, window

N, C = 64, 8


def make_mip(rng):
    return build_mipmap([[rng.randrange(256) for _ in range(N)] for _ in range(N)])


def centers(rng, k):
    return [(rng.randrange(-8, N + 8), rng.randrange(-8, N + 8)) for _ in range(k)]


def test_stack_after_moves_equals_a_fresh_fill():
    rng = random.Random(1)
    mip = make_mip(rng)
    cm = Clipmap(mip, C, (N // 2, N // 2))
    for c in centers(rng, 60):
        olds = [set((x, y) for x in range(w[0], w[2]) for y in range(w[1], w[3])) for w in cm.win]
        written = cm.recenter(c)
        fresh = Clipmap(mip, C, c)
        expected = 0
        for l in range(cm.k):
            w = window(c, l, C)
            assert cm.win[l] == w == fresh.win[l]
            pts = [(x, y) for x in range(w[0], w[2]) for y in range(w[1], w[3])]
            expected += len(set(pts) - olds[l])
            for x, y in pts:
                slot = cm.S[l][x % C][y % C]
                assert slot == fresh.S[l][x % C][y % C]
                if 0 <= x < len(mip[l]) and 0 <= y < len(mip[l]):
                    assert slot == mip[l][x][y]
        assert written == expected


def test_a_move_writes_only_the_new_strips():
    mip = make_mip(random.Random(2))
    cm = Clipmap(mip, C, (32, 32))
    assert cm.k == 3
    # The windows of the levels 0, 1 and 2 move by 8, 4 and 2 texels.
    assert cm.recenter((40, 32)) == C * (8 + 4 + 2)
    assert cm.recenter((40, 32)) == 0


def test_lookup_equals_the_full_mipmap_at_the_level_it_uses():
    rng = random.Random(3)
    mip = make_mip(rng)
    full = 0
    for c in centers(rng, 20):
        cm = Clipmap(mip, C, c)
        for _ in range(40):
            u = Fraction(rng.randrange(0, 16 * N), 16)
            v = Fraction(rng.randrange(0, 16 * N), 16)
            lam = Fraction(rng.randrange(0, 4 * len(mip)), 4)
            lmin = cm.finest_level(u, v)
            assert cm.lookup(u, v, lam) == mip_sample(mip, u, v, max(lam, lmin))
            if lmin <= int(lam):
                full += 1
                assert cm.lookup(u, v, lam) == mip_sample(mip, u, v, lam)
    assert full > 0


def test_windows_nest_for_clip_sizes_of_at_least_four():
    rng = random.Random(4)
    for size in (4, 8, 16, 32):
        for c in centers(rng, 200):
            for l in range(6):
                a, b = window(c, l, size), window(c, l + 1, size)
                lo = (a[0] * 2 ** l, a[1] * 2 ** l, a[2] * 2 ** l, a[3] * 2 ** l)
                hi = (b[0] * 2 ** (l + 1), b[1] * 2 ** (l + 1), b[2] * 2 ** (l + 1), b[3] * 2 ** (l + 1))
                assert hi[0] <= lo[0] and hi[1] <= lo[1] and lo[2] <= hi[2] and lo[3] <= hi[3]


def test_the_numbers_of_the_page():
    assert texel_counts(16384, 512) == (1660245, 357913941)
    c, p = (8000, 8000), (8400, 8100)
    held = [in_window(window(c, l, 512), (p[0] // 2 ** l, p[1] // 2 ** l)) for l in range(3)]
    assert held == [False, True, True]
