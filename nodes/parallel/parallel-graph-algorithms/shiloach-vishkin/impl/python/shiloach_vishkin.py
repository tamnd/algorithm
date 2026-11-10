# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-vishkin/. The authors are listed in prov/NADX4Y.jsonl.

"""Shiloach-Vishkin connectivity in the Awerbuch-Shiloach form, simulated one CRCW PRAM step at a time.

Each step reads the state from before the step, then applies its writes.
Concurrent writes to one cell follow the arbitrary rule: a seeded random
generator picks the winner, so a test can try many winners.

Precondition: n >= 0 and edges is a list of pairs (u, v) with 0 <= u, v < n.
Cost: each iteration is O(1) PRAM steps with one processor for each vertex and
each edge direction, so O(n + m) work and O(1) span per iteration. The number
of iterations is O(log n) (Awerbuch and Shiloach). With full_shortcut=True each
iteration ends with pointer jumping until all trees are stars, and the number
of iterations is at most ceil(log2 n) + 1.
"""

import random


class Cost:
    """Counters for work, span and iterations."""

    def __init__(self) -> None:
        self.work = 0
        self.span = 0
        self.iterations = 0


def apply_writes(P: list[int], writes: list[tuple[int, int]], rng: random.Random) -> set[int]:
    """Arbitrary CRCW rule: for each address one of the writers wins. Returns the written addresses."""
    by_addr: dict[int, list[int]] = {}
    for addr, val in writes:
        by_addr.setdefault(addr, []).append(val)
    for addr, vals in by_addr.items():
        P[addr] = rng.choice(vals)
    return set(by_addr)


def star_flags(P: list[int]) -> list[bool]:
    """The three-step star test: st[v] is true if and only if the tree of v has height at most 1."""
    n = len(P)
    st = [True] * n
    for v in range(n):  # one parallel step; all reads see the old P
        if P[v] != P[P[v]]:
            st[v] = False
            st[P[P[v]]] = False
    return [st[v] and st[P[v]] for v in range(n)]  # one parallel step


def shiloach_vishkin(
    n: int,
    edges: list[tuple[int, int]],
    rng: random.Random | None = None,
    cost: Cost | None = None,
    full_shortcut: bool = False,
) -> list[int]:
    """Return P with P[u] == P[v] if and only if u and v are in the same connected component."""
    rng = rng if rng is not None else random.Random(0)
    c = cost if cost is not None else Cost()
    arcs = [(u, v) for u, v in edges] + [(v, u) for u, v in edges]
    P = list(range(n))  # @line L1
    c.work += n
    c.span += 1
    while True:  # @line L2
        c.iterations += 1
        old = P[:]
        st = star_flags(P)  # @line L3
        # conditional star hooking
        writes = []
        for u, v in arcs:  # @line L4
            if st[u] and P[u] > P[v]:  # @line L5
                writes.append((P[u], P[v]))
        hooked = apply_writes(P, writes, rng)
        received = {old[P[r]] for r in hooked}  # the old root of the winning target of each hooked root
        # unconditional hooking of stagnant stars
        stagnant = [st[v] and old[v] not in hooked and old[v] not in received for v in range(n)]  # @line L6
        writes = []
        for u, v in arcs:  # @line L7
            if stagnant[u] and P[u] != P[v]:  # @line L8
                writes.append((P[u], P[v]))
        apply_writes(P, writes, rng)
        # shortcut
        P = [P[P[v]] for v in range(n)]  # @line L9
        steps = 9
        if full_shortcut:
            while any(P[v] != P[P[v]] for v in range(n)):
                P = [P[P[v]] for v in range(n)]
                steps += 2
        c.work += steps * (n + len(arcs))
        c.span += steps
        if P == old:  # @line L10
            return P  # @line L11
