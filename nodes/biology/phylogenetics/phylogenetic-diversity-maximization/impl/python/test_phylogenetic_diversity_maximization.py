# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phylogenetic-diversity-maximization/. The authors are listed in prov/BFRDCF.jsonl.

import itertools
import random

from phylogenetic_diversity_maximization import (
    budgeted_pd,
    greedy_rooted,
    greedy_unrooted,
    pd_rooted,
    pd_unrooted,
    taxa,
)


def random_tree(rng: random.Random, nodes: int):
    """A random rooted tree: node i > 0 hangs below a uniform earlier node."""
    parent = [-1] + [rng.randrange(i) for i in range(1, nodes)]
    length = [0] + [rng.randrange(6) for _ in range(1, nodes)]
    return parent, length


def path_edges(parent, v, stop=None):
    out = set()
    while parent[v] >= 0 and v != stop:
        out.add(v)
        v = parent[v]
    return out


def naive_pd(parent, length, chosen, rooted: bool):
    """PD from the definition: the union of the root paths (rooted), or of
    the pairwise paths (unrooted), of the chosen taxa."""
    chosen = list(chosen)
    edges = set()
    if rooted:
        for x in chosen:
            edges |= path_edges(parent, x)
    else:
        for x, y in itertools.combinations(chosen, 2):
            edges |= path_edges(parent, x) ^ path_edges(parent, y)
    return sum(length[e] for e in edges)


def best_by_brute_force(parent, length, k, rooted: bool):
    pd = pd_rooted if rooted else pd_unrooted
    return max(pd(parent, length, s) for s in itertools.combinations(taxa(parent), k))


def test_pd_matches_definition() -> None:
    rng = random.Random(41)
    for _ in range(200):
        parent, length = random_tree(rng, rng.randrange(2, 12))
        leaves = taxa(parent)
        s = rng.sample(leaves, rng.randrange(len(leaves) + 1))
        assert pd_rooted(parent, length, s) == naive_pd(parent, length, s, True)
        assert pd_unrooted(parent, length, s) == naive_pd(parent, length, s, False)


def test_greedy_rooted_is_optimal_for_every_k() -> None:
    rng = random.Random(42)
    for _ in range(150):
        parent, length = random_tree(rng, rng.randrange(2, 13))
        order = greedy_rooted(parent, length, len(taxa(parent)))
        for k in range(len(order) + 1):
            got = pd_rooted(parent, length, order[:k])
            assert got == best_by_brute_force(parent, length, k, True)


def test_greedy_unrooted_is_optimal() -> None:
    rng = random.Random(43)
    for _ in range(150):
        parent, length = random_tree(rng, rng.randrange(3, 13))
        n = len(taxa(parent))
        for k in range(2, n + 1):
            chosen = greedy_unrooted(parent, length, k)
            assert len(set(chosen)) == k
            assert pd_unrooted(parent, length, chosen) == best_by_brute_force(parent, length, k, False)


def test_budgeted_dp_matches_brute_force() -> None:
    rng = random.Random(44)
    for _ in range(120):
        parent, length = random_tree(rng, rng.randrange(2, 11))
        leaves = taxa(parent)
        cost = {x: rng.randrange(1, 5) for x in leaves}
        for budget in range(0, 9):
            best = 0
            for r in range(len(leaves) + 1):
                for s in itertools.combinations(leaves, r):
                    if sum(cost[x] for x in s) <= budget:
                        best = max(best, pd_rooted(parent, length, s))
            assert budgeted_pd(parent, length, cost, budget) == best


def test_star_tree_is_knapsack() -> None:
    # A star: root 0 with taxa 1..4. PD of a set is the sum of its edge lengths.
    parent, length = [-1, 0, 0, 0, 0], [0, 6, 10, 12, 7]
    cost = {1: 1, 2: 2, 3: 3, 4: 2}
    assert budgeted_pd(parent, length, cost, 5) == 6 + 10 + 7  # taxa 1, 2, 4
    # Greedy by length per cost takes 1 and 2 (16) and then cannot fit 3 or 4.
    assert budgeted_pd(parent, length, cost, 4) == 6 + 12  # taxa 1, 3
