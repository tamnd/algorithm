# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zhang-suen-thinning/. The authors are listed in prov/PA7FJM.jsonl.

import random

from zhang_suen_thinning import RING, zhang_suen


def parse(rows):
    return [[1 if c == "#" else 0 for c in r] for r in rows]


def pad(shape, m=1):
    w = len(shape[0]) + 2 * m
    blank = [[0] * w for _ in range(m)]
    return blank + [[0] * m + list(r) + [0] * m for r in shape] + [[0] * w for _ in range(m)]


def count(img):
    return sum(map(sum, img))


def reference_states(x):
    """An independent Zhang-Suen. It pads the image with background, computes A by
    counting the substring '01' in the ring written as text, and returns the image
    after every subiteration, up to the first iteration that deletes nothing."""
    h, w = len(x), len(x[0])
    img = pad(x)
    states = []
    while True:
        deleted = 0
        for step in (1, 2):
            snap = [list(r) for r in img]
            for y in range(1, h + 1):
                for xx in range(1, w + 1):
                    if not snap[y][xx]:
                        continue
                    p = {k: snap[y + dy][xx + dx] for k, (dx, dy) in zip(range(2, 10), RING)}
                    ring = "".join(str(p[k]) for k in range(2, 10))
                    b = ring.count("1")
                    a = (ring + ring[0]).count("01")
                    if step == 1:
                        ok = not (p[2] and p[4] and p[6]) and not (p[4] and p[6] and p[8])
                    else:
                        ok = not (p[2] and p[4] and p[8]) and not (p[2] and p[6] and p[8])
                    if 2 <= b <= 6 and a == 1 and ok:
                        img[y][xx] = 0
                        deleted += 1
            states.append([row[1:w + 1] for row in img[1:h + 1]])
        if deleted == 0:
            return states


def test_two_by_two_square_disappears_in_first_subiteration():
    sq = pad([[1, 1], [1, 1]])
    out, iterations = zhang_suen(sq)
    assert count(out) == 0
    assert iterations == 2
    assert count(reference_states(sq)[0]) == 0


def test_example_block():
    block = pad([[1] * 7 for _ in range(4)])
    states = reference_states(block)
    counts = [count(s) for s in states]
    assert counts == [17, 9, 3, 3, 3, 3]
    out, iterations = zhang_suen(block)
    assert out == parse([".........", ".........", "...###...", ".........", ".........", "........."])
    assert iterations == 3


def test_squares_iteration_counts():
    for k in range(1, 12):
        out, iterations = zhang_suen(pad([[1] * k for _ in range(k)]))
        assert iterations == (1 if k == 1 else k // 2 + 1)
        assert count(out) == (0 if k == 2 else 1)


def test_small_shapes():
    assert zhang_suen(pad([[1]]))[0] == pad([[1]])  # a single pixel stays
    line = pad([[1] * 6])
    assert zhang_suen(line)[0] == line  # a one pixel wide line stays whole
    bar = pad([[1] * 9 for _ in range(3)])
    assert zhang_suen(bar)[0][2] == [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0]


def test_two_pixel_thick_diagonal_is_destroyed():
    diag = pad(parse(["##....", ".##...", "..##..", "...##.", "....##"]))
    out, _ = zhang_suen(diag)
    assert count(diag) == 10
    assert count(out) == 2


def test_ring_stays_a_closed_curve():
    ring = pad(parse([
        "##########",
        "##########",
        "##########",
        "###....###",
        "###....###",
        "###....###",
        "##########",
        "##########",
    ]))
    out, iterations = zhang_suen(ring)
    assert iterations == 2
    assert out == pad(parse([
        "..........",
        ".########.",
        ".#......#.",
        ".#......#.",
        ".#......#.",
        ".#......#.",
        ".#######..",
        "..........",
    ]))


def test_against_reference_subset_and_fixed_point():
    rng = random.Random(6601)
    for _ in range(600):
        w, h = rng.randint(1, 9), rng.randint(1, 9)
        p = rng.choice([0.5, 0.7, 0.9])
        x = [[1 if rng.random() < p else 0 for _ in range(w)] for _ in range(h)]
        out, iterations = zhang_suen(x)
        states = reference_states(x)
        assert out == states[-1]
        assert iterations == len(states) // 2
        assert all(o <= i for ro, ri in zip(out, x) for o, i in zip(ro, ri))
        again, it2 = zhang_suen(out)
        assert again == out and it2 == 1
        assert iterations <= count(x) + 1


def ring_bits(code):
    return [(code >> i) & 1 for i in range(8)]  # P2..P9


def test_step_conditions_name_the_boundaries():
    for code in range(256):
        p2, p3, p4, p5, p6, p7, p8, p9 = ring_bits(code)
        step1 = p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0
        step2 = p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0
        assert step1 == (p4 == 0 or p6 == 0 or (p2 == 0 and p8 == 0))
        assert step2 == (p2 == 0 or p8 == 0 or (p4 == 0 and p6 == 0))


def components(cells, adjacent):
    cells = set(cells)
    seen, n = set(), 0
    for c in cells:
        if c in seen:
            continue
        n += 1
        stack = [c]
        seen.add(c)
        while stack:
            a = stack.pop()
            for b in cells:
                if b not in seen and adjacent(a, b):
                    seen.add(b)
                    stack.append(b)
    return n


def test_a_deletable_pixel_is_simple_alone():
    """Over all 256 rings: if 2 <= B <= 6 and A = 1, the foreground neighbors form one
    8-connected set, the background neighbors form one 4-connected set, and that set
    holds an edge neighbor, so deleting the center alone keeps the topology."""
    adj8 = lambda a, b: max(abs(a[0] - b[0]), abs(a[1] - b[1])) == 1
    adj4 = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1
    edge = {(0, -1), (1, 0), (0, 1), (-1, 0)}
    for code in range(256):
        n = ring_bits(code)
        b = sum(n)
        a = sum(1 for i in range(8) if n[i] == 0 and n[(i + 1) % 8] == 1)
        if not (2 <= b <= 6 and a == 1):
            continue
        fg = [RING[i] for i in range(8) if n[i]]
        bg = [RING[i] for i in range(8) if not n[i]]
        assert components(fg, adj8) == 1
        assert components(bg, adj4) == 1
        assert edge & set(bg)
