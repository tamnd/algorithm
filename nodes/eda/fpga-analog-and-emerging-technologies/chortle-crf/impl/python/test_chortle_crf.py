# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chortle-crf/. The authors are listed in prov/H1WBNA.jsonl.

import random
from functools import lru_cache
from itertools import combinations, product

from chortle_crf import chortle_crf, equivalent, ffd_bins, tree_roots


def random_tree(rng: random.Random, gates: int, max_fanin: int) -> tuple[dict, list]:
    """A fanout-free tree of AND, OR and XOR gates. Each leaf is its own input."""
    net = {}
    pending = ["g0"]
    made = 1
    leaves = 0
    while pending:
        g = pending.pop()
        d = rng.randint(2, max_fanin)
        fanins = []
        for _ in range(d):
            if made < gates and rng.random() < 0.5:
                child = f"g{made}"
                made += 1
                pending.append(child)
                fanins.append(child)
            else:
                fanins.append(f"x{leaves}")
                leaves += 1
        net[g] = (rng.choice(["AND", "OR", "XOR"]), fanins)
    return net, ["g0"]


def brute_tree_luts(net: dict, root: str, k: int) -> int:
    """The fewest K-LUTs over every way to split each gate into smaller gates
    of the same operator and to cover the result with LUTs, for a tree."""

    @lru_cache(maxsize=None)
    def group(opens: tuple, wires: int) -> dict:
        # opens: sorted sizes of child root LUTs that are still open.
        # wires: the number of single wires (inputs or closed LUT outputs).
        # Returns {root size: fewest closed LUTs}.
        best = {}
        total = sum(opens) + wires
        if total <= k:
            best[total] = 0
        n = len(opens)
        for r in range(n + 1):
            for idx in combinations(range(n), r):
                chosen = sum(opens[i] for i in idx)
                rest = tuple(opens[i] for i in range(n) if i not in idx)
                for w in range(wires + 1):
                    if r + w == 0 or chosen + w > k:
                        continue
                    if r + w == 1 and r == 0:
                        continue  # a LUT that only copies a wire
                    for u, e in group(rest, wires - w + 1).items():
                        if e + 1 < best.get(u, 10**9):
                            best[u] = e + 1
        return best

    def options(g: str) -> dict:
        op, fanins = net[g]
        child_opts, wires = [], 0
        for f in fanins:
            if f in net:
                child_opts.append(sorted(options(f).items()))
            else:
                wires += 1
        best = {}
        for choice in product(*child_opts):
            base = sum(e for _, e in choice)
            opens = tuple(sorted(u for u, _ in choice))
            for u, e in group(opens, wires).items():
                if base + e < best.get(u, 10**9):
                    best[u] = base + e
        return best

    return min(options(root).values()) + 1


def check_luts(net, outputs, luts, k, rng=None):
    for name, inputs, _ in luts:
        assert len(inputs) <= k, (name, inputs)
    assert equivalent(net, outputs, luts, rng)


def test_page_example():
    net = {"x": ("AND", ["a", "b", "c"]), "y": ("AND", ["d", "e"]), "f": ("OR", ["x", "y", "g", "h"])}
    luts = chortle_crf(net, ["f"], 4)
    check_luts(net, ["f"], luts, 4)
    assert len(luts) == 2
    assert brute_tree_luts(net, "f", 4) == 2


def test_ffd_bins():
    assert ffd_bins([3, 3, 2, 2, 2], 5) == [[0, 2], [1, 3], [4]]
    assert ffd_bins([1, 1, 1, 1], 4) == [[0, 1, 2, 3]]


def test_wide_gate():
    # a single AND of 10 inputs with K = 4 needs ceil((10 - 1) / 3) = 3 LUTs
    net = {"f": ("AND", [f"x{i}" for i in range(10)])}
    luts = chortle_crf(net, ["f"], 4)
    check_luts(net, ["f"], luts, 4)
    assert len(luts) == 3


def test_optimal_on_trees_k_up_to_5():
    rng = random.Random(1991)
    for k in (2, 3, 4, 5):
        for _ in range(60):
            net, outs = random_tree(rng, rng.randint(1, 5), 4)
            luts = chortle_crf(net, outs, k)
            check_luts(net, outs, luts, k, rng)
            assert len(luts) == brute_tree_luts(net, "g0", k)


def test_never_below_optimum_k_6_and_7():
    rng = random.Random(6)
    for k in (6, 7):
        for _ in range(25):
            net, outs = random_tree(rng, rng.randint(1, 4), 5)
            luts = chortle_crf(net, outs, k)
            check_luts(net, outs, luts, k, rng)
            assert len(luts) >= brute_tree_luts(net, "g0", k)


def test_dag_split_into_trees():
    # n has two readers, so it is the root of its own tree
    net = {
        "n": ("AND", ["a", "b"]),
        "p": ("OR", ["n", "c", "d"]),
        "q": ("XOR", ["n", "e"]),
        "r": ("AND", ["p", "q", "f"]),
    }
    assert sorted(tree_roots(net, ["r"])) == ["n", "r"]
    for k in (2, 3, 4, 5):
        luts = chortle_crf(net, ["r"], k)
        check_luts(net, ["r"], luts, k)


def test_random_dags_equivalent():
    rng = random.Random(7)
    for _ in range(40):
        net = {}
        signals = [f"x{i}" for i in range(5)]
        for i in range(rng.randint(2, 7)):
            g = f"g{i}"
            net[g] = (rng.choice(["AND", "OR", "XOR"]), rng.sample(signals, rng.randint(2, min(4, len(signals)))))
            signals.append(g)
        outs = [g for g in net if not any(g in f for _, f in net.values())]
        k = rng.randint(2, 5)
        luts = chortle_crf(net, outs, k)
        check_luts(net, outs, luts, k)
