# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-cloaking/. The authors are listed in prov/JKVDFZ.jsonl.

import random

from spatial_cloaking import cloak, reciprocity_holds

USERS = [(1, 1), (3, 2), (2, 3), (0, 3), (5, 1), (6, 6), (7, 5), (2, 6)]


def test_example() -> None:
    assert cloak((1, 1), USERS, 3, 3) == (0, 0, 4)
    for u in USERS[:4]:
        assert cloak(u, USERS, 3, 3) == (0, 0, 4)
    for u in USERS[4:]:
        assert cloak(u, USERS, 3, 3) == (0, 0, 8)
    assert reciprocity_holds(USERS, 3, 3)


def test_not_reciprocal() -> None:
    users = [(0, 0), (1, 0), (0, 1), (3, 3)]
    assert cloak((0, 0), users, 3, 2) == (0, 0, 2)
    assert cloak((3, 3), users, 3, 2) == (0, 0, 4)
    assert not reciprocity_holds(users, 3, 2)


def test_edges() -> None:
    assert cloak((0, 0), [(0, 0)], 2, 3) is None
    assert cloak((0, 0), [(0, 0)], 1, 3) == (0, 0, 1)
    assert cloak((5, 5), [(5, 5)] * 4, 3, 3) == (5, 5, 1)
    assert cloak((0, 0), [(0, 0), (0, 0)], 2, 0) == (0, 0, 1)
    # with k = 1 the requester alone is enough, so the cell of side 1 comes back
    assert cloak((6, 2), USERS + [(6, 2)], 1, 3) == (6, 2, 1)


def oracle(p: tuple[int, int], users: list[tuple[int, int]], k: int, h: int) -> tuple[int, int, int] | None:
    best = None
    for d in range(h + 1):
        side = 1 << (h - d)
        x, y = p[0] // side * side, p[1] // side * side
        inside = sum(1 for u in users if u[0] // side * side == x and u[1] // side * side == y)
        if inside >= k:
            best = (x, y, side)
    return best


def test_against_oracle() -> None:
    rng = random.Random(11)
    for _ in range(600):
        h = rng.randint(0, 5)
        size = 1 << h
        n = rng.randint(1, 30)
        users = [(rng.randrange(size), rng.randrange(size)) for _ in range(n)]
        k = rng.randint(1, 8)
        p = rng.choice(users)
        got = cloak(p, users, k, h)
        assert got == oracle(p, users, k, h)
        if got is not None:
            x, y, side = got
            assert x <= p[0] < x + side and y <= p[1] < y + side
            assert sum(1 for u in users if x <= u[0] < x + side and y <= u[1] < y + side) >= k


def test_reciprocity_against_oracle() -> None:
    rng = random.Random(12)
    for _ in range(500):
        h = rng.randint(1, 4)
        size = 1 << h
        k = rng.randint(1, 4)
        n = rng.randint(k, 12)
        users = [(rng.randrange(size), rng.randrange(size)) for _ in range(n)]
        regions = [oracle(u, users, k, h) for u in users]
        want = all(regions.count(r) >= k for r in regions)
        assert reciprocity_holds(users, k, h) == want
