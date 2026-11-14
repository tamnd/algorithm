# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flowmap/. The authors are listed in prov/R5X3KJ.jsonl.

import random
from itertools import combinations, product

from flowmap import flowmap, lut_depth

# The example of the page, k = 3: inputs a, b, c, d, e are nodes 0 to 4.
EXAMPLE = [[], [], [], [], [], [0, 1], [1, 2], [2, 3], [5, 6], [6, 7], [8, 9, 4]]


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
    """Every set of at most k nodes, without v, that cuts v from the inputs."""
    nodes = sorted(cone(fanins, v) - {v})
    return [frozenset(c) for size in range(1, k + 1) for c in combinations(nodes, size)
            if is_cut(fanins, v, frozenset(c))]


def best_depths(fanins, k) -> list:
    """d(v) = least depth of a LUT mapping of v, over every k-feasible cut."""
    d = [0] * len(fanins)
    for v in range(len(fanins)):
        if fanins[v]:
            d[v] = min(1 + max(d[u] for u in c) for c in all_lut_cuts(fanins, v, k))
    return d


def exhaustive_depth(fanins, outputs, k) -> int:
    """Try every choice of one cut for each inner node."""
    inner = [v for v in range(len(fanins)) if fanins[v]]
    choices = [all_lut_cuts(fanins, v, k) for v in inner]
    best = None
    for pick in product(*choices):
        cut = dict(zip(inner, pick))
        memo: dict = {}

        def depth(v):
            if not fanins[v]:
                return 0
            if v not in memo:
                memo[v] = 1 + max(depth(u) for u in cut[v])
            return memo[v]

        dd = max(depth(v) for v in outputs)
        best = dd if best is None else min(best, dd)
    return best


def random_dag(rng, n_in, n_gates, k):
    f = [[] for _ in range(n_in)]
    for v in range(n_in, n_in + n_gates):
        f.append(sorted(rng.sample(range(v), rng.randint(1, min(k, v)))))
    return f


def evaluate(fanins, ops, n_in, m):
    val = [(m >> (n_in - 1 - i)) & 1 for i in range(n_in)]
    for w in range(n_in, len(fanins)):
        val.append(ops[w]([val[u] for u in fanins[w]]))
    return val


def check_function(fanins, ops, n_in, outputs, luts) -> None:
    """The LUT network computes the outputs of the original network."""
    tables = {}
    for v, leaves in luts.items():
        order = sorted(leaves)
        table = {}
        for m in range(1 << n_in):
            val = evaluate(fanins, ops, n_in, m)
            key = tuple(val[u] for u in order)
            assert table.setdefault(key, val[v]) == val[v]  # v is a function of its cut
        tables[v] = (order, table)
    for m in range(1 << n_in):
        val = evaluate(fanins, ops, n_in, m)
        lut_val = {i: val[i] for i in range(n_in)}

        def get(v):
            if v not in lut_val:
                order, table = tables[v]
                lut_val[v] = table[tuple(get(u) for u in order)]
            return lut_val[v]

        for o in outputs:
            assert get(o) == val[o]


OPS = [lambda xs: int(all(xs)), lambda xs: int(any(xs)), lambda xs: sum(xs) & 1,
       lambda xs: 1 - int(all(xs))]


def test_example() -> None:
    label, luts = flowmap(EXAMPLE, [10], 3)
    assert label == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2]
    assert luts == {10: frozenset([4, 8, 9]), 9: frozenset([1, 2, 3]),
                    8: frozenset([0, 1, 2])}
    assert lut_depth(EXAMPLE, luts, [10]) == 2
    assert label == best_depths(EXAMPLE, 3)


def test_labels_are_optimal_depths() -> None:
    rng = random.Random(5)
    for _ in range(500):
        k = rng.choice([2, 3, 4])
        f = random_dag(rng, rng.randint(1, 6), rng.randint(1, 14), k)
        outs = [len(f) - 1]
        label, luts = flowmap(f, outs, k)
        assert label == best_depths(f, k)
        assert lut_depth(f, luts, outs) == max(label[o] for o in outs)
        assert all(len(c) <= k for c in luts.values())


def test_against_all_mappings() -> None:
    rng = random.Random(9)
    done = 0
    while done < 40:
        k = 3
        f = random_dag(rng, rng.randint(2, 4), rng.randint(3, 8), k)
        inner = [v for v in range(len(f)) if f[v]]
        size = 1
        for v in inner:
            size *= len(all_lut_cuts(f, v, k))
        if size > 20000 or size < 20:
            continue
        outs = sorted(set([len(f) - 1, rng.randrange(len(f))]))
        outs = [o for o in outs if f[o]] or [len(f) - 1]
        _, luts = flowmap(f, outs, k)
        assert lut_depth(f, luts, outs) == exhaustive_depth(f, outs, k)
        done += 1


def test_function_is_kept() -> None:
    rng = random.Random(13)
    for _ in range(80):
        k = rng.choice([2, 3])
        n_in = rng.randint(2, 5)
        f = random_dag(rng, n_in, rng.randint(1, 10), k)
        ops = [None] * n_in + [rng.choice(OPS) for _ in range(len(f) - n_in)]
        outs = sorted(set(rng.sample(range(n_in, len(f)), min(2, len(f) - n_in))))
        _, luts = flowmap(f, outs, k)
        check_function(f, ops, n_in, outs, luts)


def test_rejects_unbounded() -> None:
    try:
        flowmap([[], [], [], [0, 1, 2]], [3], 2)
    except ValueError:
        return
    raise AssertionError("a node with 3 fanins must be rejected for k = 2")
