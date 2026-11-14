# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-edge-algorithm/. The authors are listed in prov/NN5MVW.jsonl.

import itertools
import random

from channel import check_routing, density, intervals, realize, vcg_edges
from left_edge_algorithm import left_edge, left_edge_route


def random_channel(rng: random.Random, n: int, nets: int, maxpins: int, one_side: bool = False):
    """A random channel of n columns. With one_side, each column has at most one pin."""
    while True:
        if one_side:
            slots = [(c, rng.choice("TB")) for c in range(n)]
        else:
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


def no_dogleg_optimum(top, bottom, max_tracks: int):
    """Fewest tracks over all maps from nets to tracks whose realized routing passes the checker."""
    spans = intervals(top, bottom)
    nets = sorted(spans)
    pieces = {x: (x, l, r) for x, (l, r) in spans.items()}
    for t in range(1, max_tracks + 1):
        for assign in itertools.product(range(1, t + 1), repeat=len(nets)):
            track = dict(zip(nets, assign))
            if not check_routing(top, bottom, t, realize(top, bottom, pieces, track, t)):
                return t
    return None


def no_dogleg_optimum_fast(top, bottom, max_tracks: int):
    """The same optimum, with the two rules written out: no overlap on a track, and every edge a -> b has a above b."""
    spans = intervals(top, bottom)
    edges = vcg_edges(top, bottom)
    nets = sorted(spans)

    def fits(track, x, k):
        for y, j in track.items():
            if j == k and not (spans[x][1] < spans[y][0] or spans[y][1] < spans[x][0]):
                return False
            if ((x, y) in edges and k >= j) or ((y, x) in edges and j >= k):
                return False
        return True

    def search(i, track, t):
        if i == len(nets):
            return True
        for k in range(1, t + 1):
            if fits(track, nets[i], k):
                track[nets[i]] = k
                if search(i + 1, track, t):
                    return True
                del track[nets[i]]
        return False

    for t in range(1, max_tracks + 1):
        if search(0, {}, t):
            return t
    return None


def test_example_page() -> None:
    top = [1, 0, 3, 1, 0, 4, 6, 4, 0, 5]
    bottom = [3, 6, 0, 2, 2, 0, 3, 6, 5, 2]
    assert intervals(top, bottom) == {1: (1, 4), 2: (4, 10), 3: (1, 7), 4: (6, 8), 5: (9, 10), 6: (2, 8)}
    assert vcg_edges(top, bottom) == [(1, 2), (1, 3), (4, 6), (5, 2), (6, 3)]
    assert density(top, bottom) == 4
    t, track, wires = left_edge_route(top, bottom)
    assert t == 4
    assert track == {1: 1, 4: 1, 5: 1, 6: 2, 3: 3, 2: 4}
    assert check_routing(top, bottom, t, wires) == []
    # Without the vertical constraints, net 3 would take track 2 and short with net 6 in column 7.
    free = left_edge(intervals(top, bottom), [])
    assert free[3] == 2 and free[6] == 3
    pieces = {x: (x, l, r) for x, (l, r) in intervals(top, bottom).items()}
    assert check_routing(top, bottom, 4, realize(top, bottom, pieces, free, 4)) != []


def test_example_not_optimal() -> None:
    top = [5, 0, 0, 1, 0, 0, 1, 0]
    bottom = [2, 2, 4, 5, 3, 3, 1, 4]
    assert density(top, bottom) == 3
    t, track, wires = left_edge_route(top, bottom)
    assert t == 4 and track == {4: 1, 1: 2, 5: 3, 3: 3, 2: 4}
    assert check_routing(top, bottom, t, wires) == []
    assert no_dogleg_optimum(top, bottom, 4) == 3


def test_cycle() -> None:
    top, bottom = [1, 2], [2, 1]
    assert left_edge_route(top, bottom) is None
    assert no_dogleg_optimum(top, bottom, 3) is None


def test_edges() -> None:
    assert left_edge({}, []) == {}
    assert left_edge({1: (1, 2)}, []) == {1: 1}
    assert left_edge({1: (1, 2), 2: (2, 3)}, []) == {1: 1, 2: 2}
    assert left_edge({1: (1, 2), 2: (3, 4)}, []) == {1: 1, 2: 1}
    assert left_edge({1: (1, 2), 2: (3, 4)}, [(2, 1)]) == {2: 1, 1: 2}


def test_no_constraints_meets_density(seed: int = 11) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(4, 14)
        top, bottom = random_channel(rng, n, rng.randint(1, n // 2), 3, one_side=True)
        assert vcg_edges(top, bottom) == []
        t, track, wires = left_edge_route(top, bottom)
        assert t == density(top, bottom)
        assert check_routing(top, bottom, t, wires) == []


def test_against_checker_brute_force(seed: int = 5) -> None:
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(2, 6)
        top, bottom = random_channel(rng, n, rng.randint(1, min(4, n)), 3)
        best = no_dogleg_optimum(top, bottom, 4)
        assert best == no_dogleg_optimum_fast(top, bottom, 4)
        r = left_edge_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires = r
        assert check_routing(top, bottom, t, wires) == []
        assert best is not None and t >= best >= density(top, bottom)


def test_against_fast_brute_force(seed: int = 3) -> None:
    rng = random.Random(seed)
    worse = 0
    for _ in range(150):
        n = rng.randint(4, 10)
        top, bottom = random_channel(rng, n, rng.randint(2, min(6, n)), 3)
        best = no_dogleg_optimum_fast(top, bottom, 6)
        r = left_edge_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires = r
        assert check_routing(top, bottom, t, wires) == []
        assert t >= best >= density(top, bottom)
        worse += t > best
    assert worse > 0
