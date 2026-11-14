# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/priority-cuts/. The authors are listed in prov/TMZ6X8.jsonl.

import random
from itertools import combinations

from priority_cuts import priority_cut_map


def is_cut(fanins, v, s) -> bool:
    if v in s:
        return True
    seen, stack = set(), [v]
    while stack:
        w = stack.pop()
        if w in seen or w in s:
            continue
        seen.add(w)
        if not fanins[w]:
            return False
        stack.extend(fanins[w])
    return True


def cone(fanins, v) -> set:
    out, stack = set(), [v]
    while stack:
        w = stack.pop()
        if w not in out:
            out.add(w)
            stack.extend(fanins[w])
    return out


def all_lut_cuts(fanins, v, k) -> list:
    nodes = sorted(cone(fanins, v) - {v})
    return [frozenset(c) for size in range(1, k + 1) for c in combinations(nodes, size)
            if is_cut(fanins, v, frozenset(c))]


def best_depths(fanins, k) -> list:
    """Least LUT depth of each node over every k-feasible cut (brute force)."""
    d = [0] * len(fanins)
    for v in range(len(fanins)):
        if fanins[v]:
            d[v] = min(1 + max(d[u] for u in c) for c in all_lut_cuts(fanins, v, k))
    return d


def random_dag(rng, n_in, n_gates, k):
    f = [[] for _ in range(n_in)]
    for v in range(n_in, n_in + n_gates):
        f.append(sorted(rng.sample(range(v), rng.randint(1, min(k, v)))))
    return f


def lut_depth(fanins, luts, outputs) -> int:
    memo: dict = {}

    def d(v):
        if not fanins[v]:
            return 0
        if v not in memo:
            memo[v] = 1 + max(d(u) for u in luts[v])
        return memo[v]

    return max(d(v) for v in outputs)


def evaluate(fanins, ops, n_in, m):
    val = [(m >> (n_in - 1 - i)) & 1 for i in range(n_in)]
    for w in range(n_in, len(fanins)):
        val.append(ops[w]([val[u] for u in fanins[w]]))
    return val


def check_function(fanins, ops, n_in, outputs, luts) -> None:
    """Each LUT is a function of its inputs, and the LUT network gives the outputs."""
    tables = {}
    for v, leaves in luts.items():
        order = sorted(leaves)
        table = {}
        for m in range(1 << n_in):
            val = evaluate(fanins, ops, n_in, m)
            key = tuple(val[u] for u in order)
            assert table.setdefault(key, val[v]) == val[v]
        tables[v] = (order, table)
    for m in range(1 << n_in):
        val = evaluate(fanins, ops, n_in, m)
        got = {i: val[i] for i in range(n_in)}

        def get(v):
            if v not in got:
                order, table = tables[v]
                got[v] = table[tuple(get(u) for u in order)]
            return got[v]

        for o in outputs:
            assert get(o) == val[o]


OPS = [lambda xs: int(all(xs)), lambda xs: int(any(xs)), lambda xs: sum(xs) & 1,
       lambda xs: 1 - int(all(xs))]


def case(rng, k):
    n_in = rng.randint(2, 5)
    f = random_dag(rng, n_in, rng.randint(2, 12), k)
    inner = list(range(n_in, len(f)))
    outs = sorted(set([len(f) - 1] + rng.sample(inner, min(2, len(inner)))))
    return n_in, f, outs


def test_stored_cuts_are_k_feasible() -> None:
    rng = random.Random(3)
    for _ in range(150):
        k = rng.choice([2, 3, 4])
        _, f, outs = case(rng, k)
        luts, _, _, m = priority_cut_map(f, outs, k, rng.choice([1, 2, 4]))
        for v in range(len(f)):
            if not f[v]:
                continue
            assert 1 <= len(m.prio[v]) <= m.c
            for c in m.prio[v] + [m.best[v]]:
                assert len(c) <= k and v not in c and is_cut(f, v, c)


def test_unlimited_c_gives_optimal_depth() -> None:
    rng = random.Random(4)
    for _ in range(200):
        k = rng.choice([2, 3, 4])
        _, f, outs = case(rng, k)
        luts, d1, d_end, _ = priority_cut_map(f, outs, k, 10 ** 6)
        opt = max(best_depths(f, k)[o] for o in outs)
        assert d1 == opt
        assert d_end <= d1 and lut_depth(f, luts, outs) == d_end


def test_small_c_never_beats_the_optimum_and_area_keeps_depth() -> None:
    rng = random.Random(6)
    for _ in range(200):
        k = rng.choice([2, 3, 4])
        _, f, outs = case(rng, k)
        luts, d1, d_end, _ = priority_cut_map(f, outs, k, rng.choice([1, 2, 3]))
        opt = max(best_depths(f, k)[o] for o in outs)
        assert d1 >= opt
        assert d_end <= d1
        assert lut_depth(f, luts, outs) == d_end


def test_exact_area_pass_does_not_add_luts() -> None:
    rng = random.Random(8)
    for _ in range(200):
        k = rng.choice([3, 4])
        _, f, outs = case(rng, k)
        c = rng.choice([1, 2, 4, 8])
        after_flow, _, _, _ = priority_cut_map(f, outs, k, c, area_passes=1)
        after_exact, _, _, _ = priority_cut_map(f, outs, k, c, area_passes=2)
        assert len(after_exact) <= len(after_flow)


def test_function_is_kept() -> None:
    rng = random.Random(10)
    for _ in range(80):
        k = rng.choice([2, 3])
        n_in, f, outs = case(rng, k)
        ops = [None] * n_in + [rng.choice(OPS) for _ in range(len(f) - n_in)]
        luts, _, _, _ = priority_cut_map(f, outs, k, rng.choice([1, 3]))
        check_function(f, ops, n_in, outs, luts)
