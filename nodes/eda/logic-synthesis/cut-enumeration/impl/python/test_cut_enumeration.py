# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cut-enumeration/. The authors are listed in prov/B4M940.jsonl.

import random
from itertools import combinations

from cut_enumeration import cut_function, enumerate_cuts

AND = lambda xs: int(all(xs))  # noqa: E731

# The example of the page: inputs a, b, c, d are nodes 0 to 3.
EXAMPLE = [[], [], [], [], [0, 1], [1, 2], [4, 5], [5, 3], [6, 7]]


def is_cut(fanins, v, cut) -> bool:
    """Every path from a primary input to v meets the set."""
    if v in cut:
        return True
    seen, stack = set(), [v]
    while stack:
        w = stack.pop()
        if w in seen or w in cut:
            continue
        seen.add(w)
        if not fanins[w]:
            return False  # a primary input reaches v around the set
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


def brute_minimal_cuts(fanins, v, k) -> set:
    nodes = sorted(cone(fanins, v))
    found = set()
    for size in range(1, k + 1):
        for c in combinations(nodes, size):
            s = frozenset(c)
            if is_cut(fanins, v, s) and not any(is_cut(fanins, v, s - {x}) for x in s):
                found.add(s)
    return found


def random_dag(rng: random.Random, n_in: int, n_gates: int, max_fanin: int):
    fanins = [[] for _ in range(n_in)]
    for v in range(n_in, n_in + n_gates):
        d = rng.randint(1, min(max_fanin, v))
        fanins.append(sorted(rng.sample(range(v), d)))
    return fanins


def test_example_k3() -> None:
    cuts = enumerate_cuts(EXAMPLE, 3)
    got = [sorted(sorted(c) for c in cs) for cs in cuts]
    assert got[6] == [[0, 1, 2], [0, 1, 5], [1, 2, 4], [4, 5], [6]]
    assert got[7] == [[1, 2, 3], [3, 5], [7]]
    assert got[8] == [[3, 4, 5], [3, 5, 6], [4, 5, 7], [6, 7], [8]]


def test_example_k4() -> None:
    cuts = enumerate_cuts(EXAMPLE, 4)
    assert len(cuts[8]) == 12
    assert frozenset([0, 1, 2, 3]) in cuts[8]
    assert frozenset([1, 2, 4, 7]) in cuts[8]
    assert sum(len(c) for c in cuts) == 4 + 2 + 2 + 5 + 3 + 12


def test_unpruned_contains_redundant() -> None:
    # x = 0, y = 1, a = AND(x, y), b = AND(x, a), v = AND(a, b).
    # The union of {a} and the cut {x, y} of b is {a, x, y}, which holds {a, x}.
    f = [[], [], [0, 1], [0, 2], [2, 3]]
    pruned = enumerate_cuts(f, 3)[4]
    raw = enumerate_cuts(f, 3, prune=False)[4]
    assert frozenset([0, 1, 2]) in raw
    assert frozenset([0, 1, 2]) not in pruned
    assert set(pruned) == {frozenset([4]), frozenset([2, 3]), frozenset([0, 2]), frozenset([0, 1])}


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for trial in range(150):
        f = random_dag(rng, rng.randint(1, 4), rng.randint(1, 7), 3)
        for k in (1, 2, 3, 4):
            cuts = enumerate_cuts(f, k)
            raw = enumerate_cuts(f, k, prune=False)
            for v in range(len(f)):
                assert set(cuts[v]) == brute_minimal_cuts(f, v, k), (trial, k, v)
                for c in raw[v]:
                    assert len(c) <= k and is_cut(f, v, c)


def test_cut_function_matches_simulation() -> None:
    rng = random.Random(11)
    for _ in range(60):
        n_in = rng.randint(2, 4)
        f = random_dag(rng, n_in, rng.randint(1, 6), 2)
        ops = [None] * n_in + [rng.choice([AND, lambda xs: int(any(xs)), lambda xs: sum(xs) & 1])
                               for _ in range(len(f) - n_in)]
        for v in range(n_in, len(f)):
            for c in enumerate_cuts(f, 3)[v]:
                leaves = sorted(c)
                t = cut_function(f, ops, v, leaves)
                # evaluate the whole network on each primary input point
                for m in range(1 << n_in):
                    val = [(m >> (n_in - 1 - i)) & 1 for i in range(n_in)]
                    for w in range(n_in, len(f)):
                        val.append(ops[w]([val[u] for u in f[w]]))
                    idx = 0
                    for leaf in leaves:
                        idx = 2 * idx + val[leaf]
                    assert (t >> idx) & 1 == val[v]
