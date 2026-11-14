# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wong-liu-floorplanning/. The authors are listed in prov/0Y56MN.jsonl.

import itertools
import random
from collections import deque
from fractions import Fraction

from wong_liu_floorplanning import (
    chains,
    cost,
    is_normalized,
    m3_ok,
    move_m1,
    move_m2,
    move_m3,
    realize,
    wong_liu_floorplan,
)


def all_npe(n: int) -> list[tuple]:
    """All normalized Polish expressions on blocks 0..n-1, by brute force over words."""
    out = []
    for opos in itertools.combinations(range(2 * n - 1), n - 1):
        for perm in itertools.permutations(range(n)):
            for ops in itertools.product("HV", repeat=n - 1):
                w: list = [None] * (2 * n - 1)
                for p, o in zip(opos, ops):
                    w[p] = o
                it = iter(perm)
                for i in range(2 * n - 1):
                    if w[i] is None:
                        w[i] = next(it)
                if is_normalized(w):
                    out.append(tuple(w))
    return out


def neighbours(e: tuple) -> set[tuple]:
    """All words one move M1, M2 or M3 away from e."""
    out = set()
    pos = [k for k, t in enumerate(e) if t not in ("H", "V")]
    for a in range(len(pos) - 1):
        f = list(e)
        f[pos[a]], f[pos[a + 1]] = f[pos[a + 1]], f[pos[a]]
        out.add(tuple(f))
    for s, t in chains(list(e)):
        f = list(e)
        for k in range(s, t):
            f[k] = "V" if f[k] == "H" else "H"
        out.add(tuple(f))
    prefix = [0]
    for t in e:
        prefix.append(prefix[-1] + (t in ("H", "V")))
    for i in range(len(e) - 1):
        f = list(e)
        f[i], f[i + 1] = f[i + 1], f[i]
        assert m3_ok(list(e), i, prefix) == (
            (e[i] in ("H", "V")) != (e[i + 1] in ("H", "V")) and is_normalized(f)
        )
        if m3_ok(list(e), i, prefix):
            out.add(tuple(f))
    return out


def overlap(p, q) -> bool:
    return p[0] < q[0] + q[2] and q[0] < p[0] + p[2] and p[1] < q[1] + q[3] and q[1] < p[1] + p[3]


def test_moves_on_example() -> None:
    e = [0, 1, "V", 2, "H", 3, "V"]
    assert chains(e) == [(2, 3), (4, 5), (6, 7)]
    prefix = [0, 0, 0, 1, 1, 2, 2, 3]
    assert [i for i in range(6) if m3_ok(e, i, prefix)] == [2, 4]
    assert not m3_ok(e, 3, prefix)  # 0 1 V H 2 3 V breaks the balloting property
    assert chains([0, 1, "V", 2, 3, "H", "V"]) == [(2, 3), (5, 7)]
    rng = random.Random(0)
    assert move_m2([0, 1, "V", 2, 3, "H", "V"], random.Random(1)) in (
        [0, 1, "H", 2, 3, "H", "V"],
        [0, 1, "V", 2, 3, "V", "H"],
    )
    assert sorted(t for t in move_m1(e, rng) if t not in ("H", "V")) == [0, 1, 2, 3]


def test_m3_check_and_connectivity() -> None:
    for n in range(1, 6):
        words = all_npe(n)
        start = [0]
        for b in range(1, n):
            start += [b, "V"]
        seen = {tuple(start)}
        queue = deque([tuple(start)])
        while queue:
            e = queue.popleft()
            for f in neighbours(e):
                assert is_normalized(list(f))
                if f not in seen:
                    seen.add(f)
                    queue.append(f)
        assert seen == set(words)


def test_random_moves_keep_normal_form() -> None:
    rng = random.Random(3)
    for _ in range(600):
        n = rng.randint(1, 12)
        e = [0]
        for b in range(1, n):
            e += [b, "V"]
        for _ in range(20):
            e = rng.choice((move_m1, move_m2, move_m3))(e, rng)
            assert is_normalized(e)
            assert sorted(t for t in e if t not in ("H", "V")) == list(range(n))


def test_realize_no_overlap() -> None:
    rng = random.Random(4)
    for _ in range(300):
        n = rng.randint(1, 10)
        shapes = {}
        for b in range(n):
            w, h = rng.randint(1, 9), rng.randint(1, 9)
            shapes[b] = [(w, h), (h, w)]
        e = [0]
        for b in range(1, n):
            e += [b, "V"]
        for _ in range(10):
            e = rng.choice((move_m1, move_m2, move_m3))(e, rng)
        area, place = realize(e, shapes)
        rects = list(place.values())
        assert area >= sum(w * h for w, h in (s[0] for s in shapes.values()))
        for i in range(n):
            assert (rects[i][2], rects[i][3]) in shapes[list(place)[i]]
            for j in range(i + 1, n):
                assert not overlap(rects[i], rects[j])


def test_annealing_fixed_seed() -> None:
    rng = random.Random(5)
    for trial in range(6):
        n = 4 + trial % 2
        shapes = {}
        for b in range(n):
            w, h = rng.randint(1, 6), rng.randint(1, 6)
            shapes[b] = [(w, h), (h, w)]
        opt = min(cost(list(e), shapes, [], Fraction(0)) for e in all_npe(n))
        visited = []

        def check(e: list) -> None:
            assert is_normalized(e)
            visited.append(cost(e, shapes, [], Fraction(0)))

        best, c = wong_liu_floorplan(shapes, random.Random(100 + trial), k=5, on_state=check)
        assert is_normalized(best)
        assert c == cost(best, shapes, [], Fraction(0))
        assert c >= opt >= sum(s[0][0] * s[0][1] for s in shapes.values())
        assert visited and c == min(visited + [c])
        again, c2 = wong_liu_floorplan(shapes, random.Random(100 + trial), k=5)
        assert (again, c2) == (best, c)


def test_wirelength_term() -> None:
    shapes = {0: [(2, 2)], 1: [(2, 2)], 2: [(2, 2)], 3: [(2, 2)]}
    nets = [[0, 3]]
    e = [0, 1, "V", 2, "V", 3, "V"]
    assert cost(e, shapes, nets, Fraction(1)) == 16 + 6
    best, c = wong_liu_floorplan(shapes, random.Random(9), nets=nets, lam=Fraction(1), k=5)
    assert c == 16 + 2  # a 4 by 4 square with blocks 0 and 3 side by side
