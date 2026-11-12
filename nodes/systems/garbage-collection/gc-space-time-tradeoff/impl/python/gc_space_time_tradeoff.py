# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gc-space-time-tradeoff/. The authors are listed in prov/4J3Z1T.jsonl.

"""The amortized cost of garbage collection as a function of the heap size.

Model: the program allocates objects of one word. At every collection the
live data is exactly L words. A copying collector with memory H has two
semispaces of H / 2 words and pays c for each live word it copies. A
mark-sweep collector with memory H pays m for each live word it marks and s
for each heap word it sweeps. The formulas give the collector cost per
allocated word in the steady state:

    copying:     c L / (H / 2 - L)          (needs H > 2 L)
    mark-sweep:  (m L + s H) / (H - L)      (needs H > L)

The two simulators run real collectors on a heap of one-word objects in
which the live objects are the L most recently allocated ones, and count
the cost exactly with fractions.
"""

from __future__ import annotations

from fractions import Fraction


def copying_cost(H: int, L: int, c: Fraction | int = 1) -> Fraction:
    """Collector cost per allocated word of a semispace collector."""
    if 2 * L >= H:
        raise ValueError("a copying collector needs H > 2 L")
    return Fraction(c) * L / (Fraction(H, 2) - L)


def mark_sweep_cost(H: int, L: int, m: Fraction | int = 1, s: Fraction | int = 1) -> Fraction:
    """Collector cost per allocated word of a mark-sweep collector."""
    if L >= H:
        raise ValueError("a mark-sweep collector needs H > L")
    return (Fraction(m) * L + Fraction(s) * H) / (H - L)


def simulate_copying(H: int, L: int, cycles: int, c: Fraction | int = 1) -> Fraction:
    """Run a semispace collector; return the collector cost per allocated word.

    The run starts just after a collection, with the L live objects in to-space.
    """
    S = H // 2
    to = [("init", i) for i in range(L)]  # the objects in to-space, in address order
    roots = list(to)  # the mutator holds the L most recently allocated objects
    next_id, cost, allocated = 0, Fraction(0), 0
    for _ in range(cycles):
        while len(to) < S:  # bump allocation until to-space is full
            obj = ("new", next_id)
            next_id += 1
            to.append(obj)
            allocated += 1
            roots = (roots + [obj])[len(roots) + 1 - L:]
        live = set(roots)  # collect: copy the reachable objects to the other semispace
        copied = [obj for obj in to if obj in live]
        cost += Fraction(c) * len(copied)
        to = copied
    return cost / allocated


def simulate_mark_sweep(H: int, L: int, cycles: int, m: Fraction | int = 1,
                        s: Fraction | int = 1) -> Fraction:
    """Run a mark-sweep collector; return the collector cost per allocated word.

    The run starts just after a collection, with the L live objects in the cells
    0 to L - 1 and the other cells on the free list.
    """
    cells: list[tuple[str, int] | None] = [("init", i) for i in range(L)] + [None] * (H - L)
    roots = [cells[i] for i in range(L)]
    free = list(range(H - 1, L - 1, -1))
    next_id, cost, allocated = 0, Fraction(0), 0
    for _ in range(cycles):
        while free:  # allocate from the free list until it is empty
            a = free.pop()
            obj = ("new", next_id)
            next_id += 1
            cells[a] = obj
            allocated += 1
            roots = (roots + [obj])[len(roots) + 1 - L:]
        live = set(roots)  # mark: one unit of m for each live object
        marked = [cells[a] in live for a in range(H)]
        cost += Fraction(m) * sum(marked)
        for a in range(H - 1, -1, -1):  # sweep: one unit of s for each cell
            cost += Fraction(s)
            if not marked[a]:
                cells[a] = None
                free.append(a)
    return cost / allocated
