# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutmap/. The authors are listed in prov/7KTJSE.jsonl.

import random
from itertools import combinations

from cutmap import (
    cutmap,
    enumerate_cuts,
    equivalent,
    flowmap_labels,
    lut_depth,
    primary_inputs,
    topo_order,
)

PAGE_NET = {
    "g0": ("XOR", ["c", "b"]),
    "g1": ("OR", ["d", "b"]),
    "g2": ("OR", ["g1", "g0"]),
    "g3": ("XOR", ["g2", "a"]),
}


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
    """Minimal K-feasible cuts of v, found by testing every small node set."""
    cone, stack = set(), [v]
    while stack:
        s = stack.pop()
        if s in net:
            for f in net[s][1]:
                if f not in cone:
                    cone.add(f)
                    stack.append(f)

    def is_cut(c):
        # every path from a primary input to v meets c
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


def brute_labels(net: dict, k: int) -> dict:
    label = {p: 0 for p in primary_inputs(net)}
    for g in topo_order(net):
        label[g] = min(1 + max(label[u] for u in c) for c in brute_cuts(net, g, k))
    return label


def brute_min_luts(net: dict, outputs: list, k: int, depth: int) -> int:
    """The fewest LUTs of a mapping with depth at most `depth`, by trying
    every choice of a minimal cut at every LUT root."""
    label = brute_labels(net, k)
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
            if max(label[u] for u in c) > required[v] - 1:
                continue
            new_roots = set(roots)
            new_req = dict(required)
            for u in c:
                if u in net:
                    new_roots.add(u)
                    new_req[u] = min(new_req.get(u, depth), required[v] - 1)
            search(i + 1, new_roots, new_req)

    gate_outs = [o for o in outputs if o in net]
    search(0, set(gate_outs), {o: depth for o in gate_outs})
    return best[0]


def flowmap_count(net: dict, outputs: list, k: int) -> int:
    """FlowMap's mapping phase: each root takes a least-height cut, and among
    those the one that covers the most gates."""
    cuts = enumerate_cuts(net, k)
    label = flowmap_labels(net, cuts)

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
        h = label[v] - 1
        c = max((c for c in cuts[v] if max(label[u] for u in c) == h), key=lambda c: (volume(v, c), sorted(c)))
        stack.extend(u for u in c if u in net)
    return len(roots)


def test_page_example():
    labels = flowmap_labels(PAGE_NET, enumerate_cuts(PAGE_NET, 3))
    assert [labels[g] for g in ("g0", "g1", "g2", "g3")] == [1, 1, 1, 2]
    luts, d = cutmap(PAGE_NET, ["g3"], 3)
    assert d == 2
    assert {v: sorted(c) for v, c in luts.items()} == {"g3": ["a", "g2"], "g2": ["b", "c", "d"]}
    assert equivalent(PAGE_NET, luts, ["g3"])
    assert lut_depth(PAGE_NET, luts, ["g3"]) == 2
    assert brute_min_luts(PAGE_NET, ["g3"], 3, 2) == 2
    assert flowmap_count(PAGE_NET, ["g3"], 3) == 3


def test_labels_match_brute_force():
    rng = random.Random(11)
    for _ in range(40):
        net, outs = random_net(rng, rng.randint(2, 5), rng.randint(2, 7), 3)
        for k in (3, 4):
            assert flowmap_labels(net, enumerate_cuts(net, k)) == brute_labels(net, k)


def test_depth_optimal_and_equivalent():
    rng = random.Random(1995)
    for _ in range(200):
        net, outs = random_net(rng, rng.randint(2, 5), rng.randint(2, 8), 3)
        for k in (3, 4):
            luts, d = cutmap(net, outs, k)
            label = brute_labels(net, k)
            assert d == max(label[o] for o in outs)
            assert lut_depth(net, luts, outs) == d
            assert equivalent(net, luts, outs)
            for v, c in luts.items():
                assert len(c) <= k


def test_area_against_exhaustive():
    rng = random.Random(5)
    equal = 0
    total = 0
    for _ in range(200):
        net, outs = random_net(rng, rng.randint(3, 5), rng.randint(3, 7), 2)
        luts, d = cutmap(net, outs, 3)
        opt = brute_min_luts(net, outs, 3, d)
        assert len(luts) >= opt
        total += 1
        equal += len(luts) == opt
    assert equal >= total // 2


def test_relaxed_depth():
    rng = random.Random(3)
    for _ in range(20):
        net, outs = random_net(rng, 4, 6, 2)
        luts, d = cutmap(net, outs, 3)
        luts2, d2 = cutmap(net, outs, 3, depth=d + 1)
        assert lut_depth(net, luts2, outs) <= d + 1
        assert equivalent(net, luts2, outs)
