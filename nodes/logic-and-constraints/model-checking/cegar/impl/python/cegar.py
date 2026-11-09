# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cegar/. The authors are listed in prov/WZ22QB.jsonl.

"""Counterexample-guided abstraction refinement (Clarke, Grumberg, Jha, Lu and Veith 2000).

The concrete system has the states 0 .. n-1, a dict succ from each state to
its list of successors, a set init of initial states and a set bad of bad
states. The property is the invariant "no bad state is reachable" (AG not bad).

An abstraction is a partition of the states into blocks. The abstract system
is the existential abstraction: block B has an edge to block C when some
state of B has a successor in C. Each block lies inside bad or outside bad,
so the abstraction keeps the property labels exact.
"""

from collections import deque
from typing import Dict, FrozenSet, List, Optional, Sequence, Set, Tuple

Block = FrozenSet[int]


def abstract_edges(blocks: List[Block], succ: Dict[int, Sequence[int]]) -> List[Set[int]]:
    """The edges of the existential abstraction, as sets of block indices."""
    where = {s: b for b, blk in enumerate(blocks) for s in blk}
    edges: List[Set[int]] = [set() for _ in blocks]
    for b, blk in enumerate(blocks):
        for s in blk:
            for t in succ.get(s, ()):
                edges[b].add(where[t])
    return edges


def abstract_path(blocks: List[Block], edges: List[Set[int]], init: Set[int], bad: Set[int]) -> Optional[List[int]]:
    """A shortest abstract path from an initial block to a bad block, or None."""
    start = [b for b, blk in enumerate(blocks) if blk & init]
    parent = {b: -1 for b in start}
    queue = deque(start)
    while queue:
        b = queue.popleft()
        if blocks[b] & bad:
            path = [b]
            while parent[path[-1]] >= 0:
                path.append(parent[path[-1]])
            return path[::-1]
        for c in edges[b]:
            if c not in parent:
                parent[c] = b
                queue.append(c)
    return None


def simulate(path: List[int], blocks: List[Block], succ, init: Set[int]):
    """Concrete states along the abstract path: S0 = init in b0, S(i+1) = post(Si) in b(i+1).

    Returns (sets, i) where i is the last index with a nonempty set.
    """
    sets = [set(blocks[path[0]]) & init]
    for b in path[1:]:
        nxt = {t for s in sets[-1] for t in succ.get(s, ()) if t in blocks[b]}
        if not nxt:
            return sets, len(sets) - 1
        sets.append(nxt)
    return sets, len(sets) - 1


def concrete_trace(sets: List[Set[int]], succ) -> List[int]:
    """A concrete path s0 .. sk with si in sets[i], built backward."""
    trace = [min(sets[-1])]
    for i in range(len(sets) - 2, -1, -1):
        trace.append(min(s for s in sets[i] if trace[-1] in succ.get(s, ())))
    return trace[::-1]


def cegar(n: int, succ: Dict[int, Sequence[int]], init: Set[int], bad: Set[int], partition: Optional[List[Set[int]]] = None):
    """Run CEGAR from the given partition (default: one block for bad, one for the rest).

    Returns ("holds", blocks, rounds) when no bad state is reachable, or
    ("fails", trace, rounds) with a concrete path from init to a bad state.
    """
    start = partition if partition is not None else [set(range(n))]
    blocks: List[Block] = []
    for part in start:  # @line L1
        for piece in (set(part) & bad, set(part) - bad):
            if piece:
                blocks.append(frozenset(piece))
    rounds = 0
    while True:  # @line L2
        rounds += 1
        edges = abstract_edges(blocks, succ)  # @line L3
        path = abstract_path(blocks, edges, init, bad)  # @line L4
        if path is None:  # @line L5
            return "holds", blocks, rounds
        sets, i = simulate(path, blocks, succ, init)  # @line L6
        if i == len(path) - 1:  # @line L7
            return "fails", concrete_trace(sets, succ), rounds
        dead = frozenset(sets[i])
        b = path[i]
        rest = blocks[b] - dead
        blocks[b] = dead  # @line L8
        blocks.append(rest)
