# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yoshimura-kuh-algorithm/. The authors are listed in prov/MQ0AC7.jsonl.

import itertools
import random

from channel import check_routing, density, intervals, realize, vcg_edges
from yoshimura_kuh_algorithm import merge_nets, yoshimura_kuh_route, zones


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


def checker_optimum(top, bottom, max_tracks: int):
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


def rule_optimum(top, bottom, max_tracks: int):
    """The same optimum by backtracking: no overlap on a track, and a above b for each edge (a, b)."""
    spans = intervals(top, bottom)
    edges = set(vcg_edges(top, bottom))
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


def brute_zones(top, bottom):
    spans = intervals(top, bottom)
    sets = [frozenset(x for x, (l, r) in spans.items() if l <= c <= r) for c in range(1, len(top) + 1)]
    maximal = {s for s in sets if s and not any(s < t for t in sets)}
    return sorted(maximal, key=lambda s: min(c for c, t in enumerate(sets) if t == s))


def test_example_page() -> None:
    top = [5, 0, 0, 1, 0, 0, 1, 0]
    bottom = [2, 2, 4, 5, 3, 3, 1, 4]
    assert zones(top, bottom) == [frozenset({2, 5}), frozenset({1, 4, 5}), frozenset({1, 3, 4})]
    groups, gspan, _ = merge_nets(top, bottom)
    assert groups == {1: [1], 2: [2, 4], 5: [5, 3]}
    assert gspan == {1: (4, 7), 2: (1, 8), 5: (1, 6)}
    t, track, wires, _ = yoshimura_kuh_route(top, bottom)
    assert t == 3 == density(top, bottom)
    assert track == {1: 1, 5: 2, 3: 2, 2: 3, 4: 3}
    assert check_routing(top, bottom, t, wires) == []


def test_cycle() -> None:
    assert yoshimura_kuh_route([1, 2], [2, 1]) is None


def test_edges() -> None:
    assert yoshimura_kuh_route([], [])[:2] == (0, {})
    assert yoshimura_kuh_route([1, 1], [0, 0])[:2] == (1, {1: 1})
    assert yoshimura_kuh_route([1, 1, 2, 2], [0, 0, 0, 0])[:2] == (1, {1: 1, 2: 1})


def test_zones(seed: int = 1) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(2, 12)
        top, bottom = random_channel(rng, n, rng.randint(1, min(6, n)), 3)
        assert zones(top, bottom) == brute_zones(top, bottom)


def test_merged_nets_are_disjoint(seed: int = 6) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(3, 14)
        top, bottom = random_channel(rng, n, rng.randint(1, min(8, n)), 3)
        merged = merge_nets(top, bottom)
        if merged is None:
            continue
        spans = intervals(top, bottom)
        for xs in merged[0].values():
            for x, y in itertools.combinations(xs, 2):
                assert spans[x][1] < spans[y][0] or spans[y][1] < spans[x][0]
                assert (x, y) not in vcg_edges(top, bottom) and (y, x) not in vcg_edges(top, bottom)


def test_against_checker_brute_force(seed: int = 8) -> None:
    rng = random.Random(seed)
    for _ in range(120):
        n = rng.randint(2, 6)
        top, bottom = random_channel(rng, n, rng.randint(1, min(4, n)), 3)
        best = checker_optimum(top, bottom, 4)
        assert best == rule_optimum(top, bottom, 4)
        r = yoshimura_kuh_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires, _ = r
        assert check_routing(top, bottom, t, wires) == []
        assert best is not None and t >= best >= density(top, bottom)


def test_against_rule_brute_force(seed: int = 12) -> None:
    rng = random.Random(seed)
    for _ in range(200):
        n = rng.randint(4, 11)
        top, bottom = random_channel(rng, n, rng.randint(2, min(7, n)), 3)
        best = rule_optimum(top, bottom, 7)
        r = yoshimura_kuh_route(top, bottom)
        if r is None:
            assert best is None
            continue
        t, _, wires, _ = r
        assert check_routing(top, bottom, t, wires) == []
        assert t >= best >= density(top, bottom)
