# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/daomap/. The authors are listed in prov/HAXQH6.jsonl.

import random
from itertools import combinations

from daomap import (
    arrival_and_area,
    daomap,
    enumerate_cuts,
    equivalent,
    lut_depth,
    primary_inputs,
    topo_order,
)

PAGE_NET = {
    "g0": ("OR", ["c", "d"]),
    "g1": ("AND", ["b", "d"]),
    "g2": ("AND", ["g1", "g0"]),
    "g3": ("OR", ["g1", "a"]),
    "g4": ("XOR", ["a", "g2"]),
}
PAGE_OUTS = ["g3", "g4"]


def random_net(rng: random.Random, n_in: int, n_gates: int, fanin: int) -> tuple[dict, list]:
    net = {}
    signals = [f"x{i}" for i in range(n_in)]
    for i in range(n_gates):
        g = f"g{i}"
        d = rng.randint(2, min(fanin, len(signals)))
        net[g] = (rng.choice(["AND", "OR", "XOR", "NAND"]), rng.sample(signals, d))
        signals.append(g)
    read = {f for _, fs in net.values() for f in fs}
    outs = [g for g in net if g not in read]
    return net, outs


def brute_cuts(net: dict, v: str, k: int) -> list:
    """Minimal K-feasible cuts of v, by testing every small set of nodes."""
    cone, stack = set(), [v]
    while stack:
        s = stack.pop()
        if s in net:
            for f in net[s][1]:
                if f not in cone:
                    cone.add(f)
                    stack.append(f)

    def is_cut(c):
        seen, stack = set(), [v]
        while stack:
            s = stack.pop()
            if s in c:
                continue
            if s not in net:
                return False
            for f in net[s][1]:
                if f not in seen:
                    seen.add(f)
                    stack.append(f)
        return True

    found = [frozenset(c) for r in range(1, k + 1) for c in combinations(sorted(cone), r) if is_cut(set(c))]
    return [c for c in found if not any(o < c for o in found)]


def brute_depth(net: dict, k: int) -> dict:
    """The least LUT depth of each node, by a recursion over all cuts."""
    depth = {p: 0 for p in primary_inputs(net)}
    for g in topo_order(net):
        depth[g] = min(1 + max(depth[u] for u in c) for c in brute_cuts(net, g, k))
    return depth


def brute_min_luts(net: dict, outputs: list, k: int, d: int) -> int:
    """The fewest LUTs of any mapping of depth at most d, by trying every
    minimal cut at every LUT root under the required time rule."""
    least = brute_depth(net, k)
    cuts = {g: brute_cuts(net, g, k) for g in net}
    order = list(reversed(topo_order(net)))
    best = [10**9]

    def search(i, roots, required):
        if len(roots) >= best[0]:
            return
        while i < len(order) and order[i] not in roots:
            i += 1
        if i == len(order):
            best[0] = len(roots)
            return
        v = order[i]
        for c in cuts[v]:
            if max(least[u] for u in c) > required[v] - 1:
                continue
            new_roots, new_req = set(roots), dict(required)
            for u in c:
                if u in net:
                    new_roots.add(u)
                    new_req[u] = min(new_req.get(u, d), required[v] - 1)
            search(i + 1, new_roots, new_req)

    outs = [o for o in outputs if o in net]
    search(0, set(outs), {o: d for o in outs})
    return best[0]


def flowmap_count(net: dict, outputs: list, k: int) -> int:
    """FlowMap's mapping phase: each root takes a cut of least height, and
    among those the one that covers the most gates."""
    cuts = enumerate_cuts(net, k)
    arr, _, _ = arrival_and_area(net, outputs, cuts)

    def volume(v, c):
        seen, stack = set(), [v]
        while stack:
            s = stack.pop()
            if s in c or s in seen or s not in net:
                continue
            seen.add(s)
            stack.extend(net[s][1])
        return len(seen)

    roots, stack = set(), [o for o in outputs if o in net]
    while stack:
        v = stack.pop()
        if v in roots:
            continue
        roots.add(v)
        c = max((c for c in cuts[v] if max(arr[u] for u in c) == arr[v] - 1), key=lambda c: (volume(v, c), sorted(c)))
        stack.extend(u for u in c if u in net)
    return len(roots)


def test_page_example():
    cuts = enumerate_cuts(PAGE_NET, 3)
    arr, area, cut_area = arrival_and_area(PAGE_NET, PAGE_OUTS, cuts)
    assert [arr[g] for g in ("g0", "g1", "g2", "g3", "g4")] == [1, 1, 1, 1, 2]
    rounded = {(v, tuple(sorted(c))): round(a, 3) for (v, c), a in cut_area.items()}
    assert rounded[("g2", ("b", "c", "d"))] == 1.333
    assert rounded[("g2", ("c", "d", "g1"))] == 1.5
    assert rounded[("g4", ("a", "g2"))] == 2.333
    assert rounded[("g4", ("a", "g0", "g1"))] == 2.5
    assert rounded[("g3", ("a", "g1"))] == 1.5
    assert rounded[("g3", ("a", "b", "d"))] == 1.333
    luts, d = daomap(PAGE_NET, PAGE_OUTS, 3)
    assert d == 2
    assert {v: sorted(c) for v, c in luts.items()} == {
        "g4": ["a", "g2"],
        "g3": ["a", "b", "d"],
        "g2": ["b", "c", "d"],
    }
    assert equivalent(PAGE_NET, luts, PAGE_OUTS)
    assert brute_min_luts(PAGE_NET, PAGE_OUTS, 3, 2) == 3
    assert flowmap_count(PAGE_NET, PAGE_OUTS, 3) == 4


def test_arrival_is_least_depth():
    rng = random.Random(7)
    for _ in range(40):
        net, outs = random_net(rng, rng.randint(2, 5), rng.randint(2, 7), 3)
        for k in (3, 4):
            arr, _, _ = arrival_and_area(net, outs, enumerate_cuts(net, k))
            assert arr == brute_depth(net, k)


def test_depth_optimal_and_equivalent():
    rng = random.Random(2004)
    for _ in range(200):
        net, outs = random_net(rng, rng.randint(2, 5), rng.randint(2, 8), 3)
        for k in (3, 4):
            luts, d = daomap(net, outs, k)
            least = brute_depth(net, k)
            assert d == max(least[o] for o in outs)
            assert lut_depth(net, luts, outs) == d
            assert equivalent(net, luts, outs)
            assert all(len(c) <= k for c in luts.values())


def test_area_against_exhaustive():
    rng = random.Random(5)
    total = equal = 0
    for _ in range(200):
        net, outs = random_net(rng, rng.randint(3, 5), rng.randint(3, 7), 2)
        luts, d = daomap(net, outs, 3)
        opt = brute_min_luts(net, outs, 3, d)
        assert len(luts) >= opt
        total += 1
        equal += len(luts) == opt
    assert equal >= total // 2


def test_one_iteration_is_valid():
    rng = random.Random(1)
    for _ in range(30):
        net, outs = random_net(rng, 4, 6, 2)
        luts, d = daomap(net, outs, 3, iterations=1)
        assert lut_depth(net, luts, outs) == d
        assert equivalent(net, luts, outs)
