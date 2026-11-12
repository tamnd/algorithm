# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-phylogenetic-inference/. The authors are listed in prov/SBJ5QF.jsonl.

"""Metropolis-Hastings sampling of unrooted trees and branch lengths under the Jukes-Cantor model.

The model is small on purpose, so that the exact posterior can be found by enumeration:
- n taxa 0 .. n - 1 with aligned DNA sequences of length m,
- the Jukes-Cantor (JC69) substitution model, branch lengths in expected substitutions per site,
- a uniform prior on the (2n - 5)!! unrooted binary topologies,
- each of the 2n - 3 branch lengths drawn on its own and uniformly from the finite set LENGTHS.

A state is (tree, lengths). The tree is an adjacency map: leaves 0 .. n - 1 have degree 1 and
every other vertex has degree 3. lengths maps each edge, named by its split (the leaf set on
the side without leaf 0), to its length. The keys of lengths are all 2n - 3 splits, so they
fix the topology too.

Two proposals, each picked with probability 1/2:
- NNI: pick one of the n - 3 internal edges and one of its 2 interchanges. An NNI keeps every
  split but the central one, so every branch keeps its length, and the central branch keeps
  its length under its new split.
- length: pick one of the 2n - 3 edges and a different value from LENGTHS.
Both proposals are symmetric, so the acceptance probability is min(1, posterior ratio). With a
uniform prior on the states that is min(1, likelihood ratio).
"""

import math
import random
from typing import Dict, FrozenSet, Iterator, List, Sequence, Set, Tuple

Tree = Dict[int, Set[int]]
Split = FrozenSet[int]
Lengths = Dict[Split, float]
LENGTHS = (0.05, 0.3)
STATES = "ACGT"


def copy_tree(tree: Tree) -> Tree:
    return {v: set(nb) for v, nb in tree.items()}


def _order(tree: Tree) -> Tuple[List[int], Dict[int, int]]:
    parent = {0: -1}
    order = [0]
    stack = [0]
    while stack:
        v = stack.pop()
        for w in tree[v]:
            if w not in parent:
                parent[w] = v
                order.append(w)
                stack.append(w)
    return order, parent


def edge_splits(tree: Tree, n: int) -> Dict[Tuple[int, int], Split]:
    """Map each edge (parent, child), rooted at leaf 0, to its split."""
    order, parent = _order(tree)
    below: Dict[int, Set[int]] = {}
    for v in reversed(order):
        s = {v} if v < n else set()
        for w in tree[v]:
            if parent.get(w) == v:
                s |= below[w]
        below[v] = s
    return {(parent[v], v): frozenset(below[v]) for v in order[1:]}


def topology_of(lengths: Lengths, n: int) -> FrozenSet[Split]:
    """The set of nontrivial splits of the state."""
    return frozenset(s for s in lengths if 2 <= len(s) <= n - 2)


def jc_prob(t: float) -> Tuple[float, float]:
    """JC69 probabilities of no change and of a change to one given other state, after time t."""
    e = math.exp(-4.0 * t / 3.0)
    return 0.25 + 0.75 * e, 0.25 - 0.25 * e


def log_likelihood(tree: Tree, lengths: Lengths, seqs: Sequence[str]) -> float:
    """Felsenstein pruning rooted at leaf 0. O(n m) for DNA."""
    n = len(seqs)
    order, parent = _order(tree)
    split_of = edge_splits(tree, n)
    probs = {v: jc_prob(lengths[split_of[(parent[v], v)]]) for v in order[1:]}
    total = 0.0
    for j in range(len(seqs[0])):
        partial: Dict[int, List[float]] = {}
        for v in reversed(order[1:]):
            if v < n:
                partial[v] = [1.0 if c == seqs[v][j] else 0.0 for c in STATES]
                continue
            vec = [1.0] * 4
            for w in tree[v]:
                if parent.get(w) == v:
                    same, diff = probs[w]
                    lw = partial[w]
                    sw = sum(lw)
                    for x in range(4):
                        vec[x] *= diff * sw + (same - diff) * lw[x]
            partial[v] = vec
        child = order[1]
        same, diff = probs[child]
        lc = partial[child]
        x = STATES.index(seqs[0][j])
        total += math.log(0.25 * (diff * sum(lc) + (same - diff) * lc[x]))
    return total


def internal_edges(tree: Tree) -> List[Tuple[int, int]]:
    return sorted((u, v) for u in tree for v in tree[u] if u < v and len(tree[u]) == 3 and len(tree[v]) == 3)


def nni_move(tree: Tree, lengths: Lengths, n: int, u: int, v: int, which: int) -> Tuple[Tree, Lengths]:
    """Interchange across the internal edge {u, v}; which = 0 or 1 picks the partner of b."""
    a, b = sorted(tree[u] - {v})
    x = sorted(tree[v] - {u})[which]
    central = edge_splits(tree, n)
    central_split = next(s for e, s in central.items() if set(e) == {u, v})
    t = copy_tree(tree)
    t[u].discard(b)
    t[b].discard(u)
    t[v].discard(x)
    t[x].discard(v)
    t[u].add(x)
    t[x].add(u)
    t[v].add(b)
    t[b].add(v)
    lens = {s: lengths.get(s, lengths[central_split]) for s in edge_splits(t, n).values()}
    return t, lens


def proposals(tree: Tree, lengths: Lengths, n: int) -> Iterator[Tuple[float, Tree, Lengths]]:
    """Yield every proposal (probability, tree, lengths) from the state. They sum to 1."""
    edges = internal_edges(tree)
    for u, v in edges:
        for which in (0, 1):
            t, lens = nni_move(tree, lengths, n, u, v, which)
            yield 0.5 / (2 * len(edges)), t, lens
    others = len(LENGTHS) - 1
    for s in sorted(lengths, key=sorted):
        for val in LENGTHS:
            if val != lengths[s]:
                lens = dict(lengths)
                lens[s] = val
                yield 0.5 / (len(lengths) * others), tree, lens


def propose(tree: Tree, lengths: Lengths, n: int, rng: random.Random) -> Tuple[Tree, Lengths]:
    """Draw one proposal with the probabilities that proposals() lists."""
    if rng.random() < 0.5:
        u, v = rng.choice(internal_edges(tree))
        return nni_move(tree, lengths, n, u, v, rng.randrange(2))
    s = rng.choice(sorted(lengths, key=sorted))
    lens = dict(lengths)
    lens[s] = rng.choice([x for x in LENGTHS if x != lengths[s]])
    return tree, lens


def mcmc(seqs: Sequence[str], start: Tree, steps: int, burn_in: int, rng: random.Random) -> Dict[FrozenSet[Split], float]:
    """Run Metropolis-Hastings and return the sampled frequency of each topology after burn-in.

    Each step costs one proposal, O(n^2), and one likelihood, O(n m). The likelihood of each
    state is cached, because the state space here is small.
    """
    n = len(seqs)
    cache: Dict[FrozenSet, float] = {}

    def logl_of(t: Tree, lens: Lengths) -> float:
        key = frozenset(lens.items())
        if key not in cache:
            cache[key] = log_likelihood(t, lens, seqs)
        return cache[key]

    tree = start  # @line L1
    lengths: Lengths = {s: LENGTHS[0] for s in edge_splits(tree, n).values()}
    logl = logl_of(tree, lengths)
    counts: Dict[FrozenSet[Split], int] = {}
    for step in range(steps):  # @line L2
        t2, l2 = propose(tree, lengths, n, rng)  # @line L3
        logl2 = logl_of(t2, l2)  # @line L4
        if rng.random() < math.exp(min(0.0, logl2 - logl)):  # @line L5
            tree, lengths, logl = t2, l2, logl2  # @line L6
        if step >= burn_in:  # @line L7
            k = topology_of(lengths, n)
            counts[k] = counts.get(k, 0) + 1
    total = steps - burn_in
    return {k: c / total for k, c in counts.items()}  # @line L8
