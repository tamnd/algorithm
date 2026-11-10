# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pointer-jumping/. The authors are listed in prov/MB1XCY.jsonl.

"""Pointer jumping (Wyllie 1979), simulated one synchronous PRAM step at a time.

Each round reads only the old arrays and builds new ones, so every item of a
list comprehension is the work of one processor in one step.
"""

from dataclasses import dataclass, field

Cell = tuple[str, int]


@dataclass
class Trace:
    """Costs of a run: rounds, work (processor steps that changed a cell) and an access log."""

    rounds: int = 0
    work: int = 0
    # one entry per substep: a list of (processor, cell) pairs, reads and writes together
    substeps: list[list[tuple[int, Cell]]] = field(default_factory=list)


def ceil_log2(n: int) -> int:
    """The least k >= 0 with 2^k >= n, for n >= 1; 0 for n = 0."""
    return 0 if n <= 1 else (n - 1).bit_length()


def pointer_jump_rank(nxt: list[int | None], trace: Trace | None = None) -> list[int]:
    """Return rank[i], the number of links from node i to the end of its list.

    nxt[i] is the successor of node i, or None at a tail. The successor map must be
    injective (a set of disjoint lists). The run takes ceil(log2 n) rounds, n processors
    and Theta(n log n) work. It is an EREW PRAM program with two read substeps a round.
    """
    n = len(nxt)
    nxt = list(nxt)
    rank = [0 if nxt[i] is None else 1 for i in range(n)]  # @line L1 @line L2
    for _ in range(ceil_log2(n)):  # @line L3
        old_rank, old_nxt = rank, nxt
        if trace is not None:
            trace.rounds += 1
            # substep a: each processor reads its own two cells
            trace.substeps.append([(i, (c, i)) for i in range(n) for c in ("rank", "next")])
            # substep b: processor i reads the cells of its successor j
            trace.substeps.append(
                [(i, (c, old_nxt[i])) for i in range(n) if old_nxt[i] is not None for c in ("rank", "next")]
            )
            # substep c: processor i writes its own two cells
            trace.substeps.append([(i, (c, i)) for i in range(n) if old_nxt[i] is not None for c in ("rank", "next")])
            trace.work += sum(1 for i in range(n) if old_nxt[i] is not None)
        rank = [  # @line L4 @line L5
            old_rank[i] + old_rank[old_nxt[i]] if old_nxt[i] is not None else old_rank[i] for i in range(n)
        ]
        nxt = [old_nxt[old_nxt[i]] if old_nxt[i] is not None else None for i in range(n)]  # @line L6
    return rank


def pointer_jump_roots(parent: list[int], trace: Trace | None = None) -> list[int]:
    """Return the root of each node of a rooted forest; a root r has parent[r] == r.

    A round sets parent[i] to parent[parent[i]] for all i at once. The number of rounds
    that change something is ceil(log2 h) for the largest depth h >= 1. Many nodes read
    the cell of the same root, so this form needs a CREW PRAM.
    """
    p = list(parent)
    while any(p[p[i]] != p[i] for i in range(len(p))):
        old = p
        p = [old[old[i]] for i in range(len(old))]
        if trace is not None:
            trace.rounds += 1
            trace.work += len(old)
    return p
