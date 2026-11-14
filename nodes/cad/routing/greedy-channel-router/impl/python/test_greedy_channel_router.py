# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-channel-router/. The authors are listed in prov/N38E4M.jsonl.

import random

from channel import check_routing, density, intervals, tracks_used, vcg_edges
from greedy_channel_router import greedy_route


def random_channel(rng: random.Random, n: int, nets: int, maxpins: int):
    while True:
        slots = [(c, s) for c in range(n) for s in "TB"]
        rng.shuffle(slots)
        top, bottom = [0] * n, [0] * n
        k, ok = 0, True
        for x in range(1, nets + 1):
            p = rng.randint(2, maxpins)
            mine = slots[k:k + p]
            k += p
            if len(mine) < 2 or len({c for c, _ in mine}) < 2:
                ok = False
                break
            for c, s in mine:
                (top if s == "T" else bottom)[c] = x
        if ok:
            return top, bottom


def has_cycle(top, bottom) -> bool:
    """Plain depth-first search for a cycle in the vertical constraint graph."""
    succ = {}
    for a, b in vcg_edges(top, bottom):
        succ.setdefault(a, []).append(b)
    state = {}

    def visit(v) -> bool:
        state[v] = 1
        for w in succ.get(v, []):
            if state.get(w) == 1 or (w not in state and visit(w)):
                return True
        state[v] = 2
        return False

    return any(v not in state and visit(v) for v in list(succ))


def check(top, bottom):
    t, wires, extra = greedy_route(top, bottom)
    assert check_routing(top, bottom, t, wires, extra_columns=extra) == []
    assert tracks_used(wires) == t
    assert t >= density(top, bottom)
    return t, extra


def test_example_page() -> None:
    top = [1, 2, 1, 3, 0, 0]
    bottom = [2, 0, 0, 1, 3, 3]
    assert check(top, bottom) == (2, 0)


def test_cycle_needs_extension() -> None:
    top, bottom = [1, 2], [2, 1]
    assert has_cycle(top, bottom)
    t, extra = check(top, bottom)
    assert extra >= 1


def test_edges() -> None:
    assert greedy_route([], []) == (0, [], 0)
    assert check([1, 1], [0, 0]) == (1, 0)
    assert check([1, 0], [0, 1]) == (1, 0)
    assert check([1, 2, 1, 2], [0, 0, 0, 0])[0] == 2


def test_checker_rejects_broken_routings(seed: int = 3) -> None:
    rng = random.Random(seed)
    for _ in range(100):
        n = rng.randint(3, 10)
        top, bottom = random_channel(rng, n, rng.randint(2, min(5, n)), 3)
        t, wires, extra = greedy_route(top, bottom)
        branches = [k for k, w in enumerate(wires) if w[0] == "V" and (0 in w[3:] or t + 1 in w[3:])]
        k = rng.choice(branches)
        assert check_routing(top, bottom, t, wires[:k] + wires[k + 1:], extra_columns=extra) != []
        x = wires[k]
        other = [y for y in intervals(top, bottom) if y != x[1]]
        if other:
            moved = wires[:k] + [(x[0], other[0]) + x[2:]] + wires[k + 1:]
            assert check_routing(top, bottom, t, moved, extra_columns=extra) != []
        assert check_routing(top, bottom, t - 1, wires, extra_columns=extra) != []


def test_random_channels(seed: int = 21) -> None:
    rng = random.Random(seed)
    extended = cyclic = 0
    for _ in range(400):
        n = rng.randint(2, 16)
        top, bottom = random_channel(rng, n, rng.randint(1, min(9, n)), 4)
        t, extra = check(top, bottom)
        extended += extra > 0
        cyclic += has_cycle(top, bottom)
        assert t <= density(top, bottom) + 2 * (n + extra)
    assert cyclic > 0 and extended > 0


def test_one_side_pins_meet_density(seed: int = 4) -> None:
    rng = random.Random(seed)
    for _ in range(200):
        n = rng.randint(2, 14)
        top, _ = random_channel(rng, n, rng.randint(1, max(1, n // 2)), 3)
        top = [x for x in top]
        bottom = [0] * n
        spans = intervals(top, bottom)
        if any(l == r for l, r in spans.values()):
            continue
        check(top, bottom)
