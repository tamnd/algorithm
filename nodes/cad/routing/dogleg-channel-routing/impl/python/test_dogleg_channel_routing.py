# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dogleg-channel-routing/. The authors are listed in prov/SJ43AX.jsonl.

import itertools
import random

from channel import check_routing, density, intervals, realize, vcg_edges
from dogleg_channel_routing import dogleg_route, left_edge_pieces, piece_vcg, split_nets


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


def checker_optimum(top, bottom, pieces, max_tracks: int):
    """Fewest tracks over all maps from pieces to tracks whose realized routing passes the checker."""
    keys = sorted(pieces)
    for t in range(1, max_tracks + 1):
        for assign in itertools.product(range(1, t + 1), repeat=len(keys)):
            track = dict(zip(keys, assign))
            if not check_routing(top, bottom, t, realize(top, bottom, pieces, track, t)):
                return t
    return None


def rule_optimum(pieces, edges, max_tracks: int):
    """The same optimum by backtracking with the rules written out."""
    keys = sorted(pieces)
    eset = set(edges)

    def fits(track, p, k):
        net, l, r = pieces[p]
        for q, j in track.items():
            y, l2, r2 = pieces[q]
            if j == k and net != y and not (r < l2 or r2 < l):
                return False
            if ((p, q) in eset and k >= j) or ((q, p) in eset and j >= k):
                return False
        return True

    def search(i, track, t):
        if i == len(keys):
            return True
        for k in range(1, t + 1):
            if fits(track, keys[i], k):
                track[keys[i]] = k
                if search(i + 1, track, t):
                    return True
                del track[keys[i]]
        return False

    for t in range(1, max_tracks + 1):
        if search(0, {}, t):
            return t
    return None


def test_example_page() -> None:
    top = [1, 2, 1, 3, 0, 0]
    bottom = [2, 0, 0, 1, 3, 3]
    assert vcg_edges(top, bottom) == [(1, 2), (3, 1)]
    assert density(top, bottom) == 2
    pieces = split_nets(top, bottom)
    assert pieces == {(1, 0): (1, 1, 3), (1, 1): (1, 3, 4), (2, 0): (2, 1, 2), (3, 0): (3, 4, 5), (3, 1): (3, 5, 6)}
    assert piece_vcg(top, bottom, pieces) == [((1, 0), (2, 0)), ((3, 0), (1, 1))]
    t, track, wires = dogleg_route(top, bottom)
    assert t == 2
    assert track == {(1, 0): 1, (3, 0): 1, (3, 1): 1, (2, 0): 2, (1, 1): 2}
    assert check_routing(top, bottom, t, wires) == []
    whole = {x: (x, l, r) for x, (l, r) in intervals(top, bottom).items()}
    assert checker_optimum(top, bottom, whole, 3) == 3


def test_cycle_broken() -> None:
    top, bottom = [1, 1, 2], [2, 0, 1]
    t, track, wires = dogleg_route(top, bottom)
    assert t == 3 and track == {(1, 0): 1, (2, 0): 2, (1, 1): 3}
    assert check_routing(top, bottom, t, wires) == []


def test_cycle_not_broken() -> None:
    top, bottom = [1, 2], [2, 1]
    assert dogleg_route(top, bottom) is None
    assert checker_optimum(top, bottom, split_nets(top, bottom), 3) is None


def test_edges() -> None:
    assert dogleg_route([], []) == (0, {}, [])
    assert dogleg_route([1, 1], [0, 0])[:2] == (1, {(1, 0): 1})
    assert left_edge_pieces({}, []) == {}


def test_against_checker_brute_force(seed: int = 2) -> None:
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(2, 5)
        top, bottom = random_channel(rng, n, rng.randint(1, min(3, n)), 3)
        pieces = split_nets(top, bottom)
        if len(pieces) > 5:
            continue
        best = checker_optimum(top, bottom, pieces, 4)
        assert best == rule_optimum(pieces, piece_vcg(top, bottom, pieces), 4)
        r = dogleg_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires = r
        assert check_routing(top, bottom, t, wires) == []
        assert best is not None and t >= best >= density(top, bottom)


def test_against_rule_brute_force(seed: int = 9) -> None:
    rng = random.Random(seed)
    for _ in range(200):
        n = rng.randint(4, 9)
        top, bottom = random_channel(rng, n, rng.randint(2, min(5, n)), 3)
        pieces = split_nets(top, bottom)
        edges = piece_vcg(top, bottom, pieces)
        best = rule_optimum(pieces, edges, len(pieces))
        r = dogleg_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires = r
        assert check_routing(top, bottom, t, wires) == []
        assert t >= best >= density(top, bottom)


def test_two_pin_nets_have_one_piece(seed: int = 4) -> None:
    rng = random.Random(seed)
    for _ in range(200):
        n = rng.randint(3, 12)
        top, bottom = random_channel(rng, n, rng.randint(1, n // 2 + 1), 2)
        pieces = split_nets(top, bottom)
        assert len(pieces) == len(intervals(top, bottom))
        r = dogleg_route(top, bottom)
        if r is not None:
            assert check_routing(top, bottom, r[0], r[2]) == []
