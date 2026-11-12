# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-routing/. The authors are listed in prov/NZAZBW.jsonl.

"""Valiant's two-phase randomized routing on the n-dimensional hypercube.

Model: synchronous steps. Node u has one outgoing edge per dimension, and in
one step each directed edge carries at most one packet. A packet that waits
for an edge sits in the FIFO queue of that edge; ties among packets that join
a queue in the same step go by packet number. Queues are unbounded.

Routes are bit-fixing routes: the bits are fixed from the most significant
(dimension n - 1) down to dimension 0.

valiant_route sends packet p from node p to an intermediate node r[p] chosen
uniformly at random, then from r[p] to dest[p]. With phased=True the second
phase starts only when every packet has finished the first, as in the proof.
greedy_route sends each packet straight to dest[p] by bit-fixing.
"""

import random
from collections import deque


def bit_fixing_dims(n: int, u: int, t: int) -> list[int]:
    """Dimensions crossed by the bit-fixing route from u to t, in order."""
    dims = []
    for i in range(n - 1, -1, -1):  # @line L6
        if (u ^ t) >> i & 1:  # @line L7
            dims.append(i)
    return dims


def run_phase(n: int, start: list[int], target: list[int]) -> tuple[int, list[int], list[int]]:
    """Route all packets at once. Returns (steps, delay of each packet, route sets).

    The delay of a packet is its arrival step minus its route length.
    """
    count = len(start)
    hops = [deque(bit_fixing_dims(n, start[p], target[p])) for p in range(count)]
    length = [len(h) for h in hops]
    at = list(start)
    arrival = [0] * count
    queues: dict[int, deque] = {}

    def enqueue(p: int) -> None:
        edge = at[p] * n + hops[p][0]
        queues.setdefault(edge, deque()).append(p)  # @line L8

    for p in range(count):
        if hops[p]:
            enqueue(p)
    step = 0
    while queues:
        step += 1
        moved = []
        for edge in list(queues):
            q = queues[edge]
            p = q.popleft()  # one packet crosses each busy edge
            if not q:
                del queues[edge]
            at[p] ^= 1 << hops[p].popleft()
            moved.append(p)
        for p in sorted(moved):
            if hops[p]:
                enqueue(p)
            else:
                arrival[p] = step
    if at != list(target):
        raise AssertionError("a packet did not reach its target")
    delay = [arrival[p] - length[p] if length[p] else 0 for p in range(count)]
    return step, delay, length


def greedy_route(n: int, dest: list[int]) -> int:
    """Deterministic bit-fixing straight to the destination. Returns the steps."""
    steps, _, _ = run_phase(n, list(range(1 << n)), dest)
    return steps


def valiant_route(n: int, dest: list[int], rng: random.Random, phased: bool = True) -> int:
    """Valiant's two-phase routing. Returns the number of steps until all packets arrive."""
    size = 1 << n
    r = [0] * size
    for p in range(size):  # @line L1
        r[p] = rng.randrange(size)  # @line L2
    if not phased:
        return _pipelined(n, r, dest)
    total = 0
    for phase in (1, 2):  # @line L3
        start = list(range(size)) if phase == 1 else r  # @line L4
        target = r if phase == 1 else dest  # @line L5
        steps, _, _ = run_phase(n, start, target)
        total += steps  # @line L9
    return total  # @line L10


def _pipelined(n: int, r: list[int], dest: list[int]) -> int:
    """Each packet starts phase 2 as soon as it reaches r[p]."""
    size = 1 << n
    hops = [deque(bit_fixing_dims(n, p, r[p]) + bit_fixing_dims(n, r[p], dest[p])) for p in range(size)]
    at = list(range(size))
    queues: dict[int, deque] = {}
    for p in range(size):
        if hops[p]:
            queues.setdefault(at[p] * n + hops[p][0], deque()).append(p)
    step = 0
    while queues:
        step += 1
        moved = []
        for edge in list(queues):
            q = queues[edge]
            p = q.popleft()
            if not q:
                del queues[edge]
            at[p] ^= 1 << hops[p].popleft()
            moved.append(p)
        for p in sorted(moved):
            if hops[p]:
                queues.setdefault(at[p] * n + hops[p][0], deque()).append(p)
    return step


def bit_reversal(n: int) -> list[int]:
    return [int(format(x, "0{}b".format(n))[::-1], 2) for x in range(1 << n)]


def transpose(n: int) -> list[int]:
    """Swap the two halves of the address (n even)."""
    h = n // 2
    mask = (1 << h) - 1
    return [((x & mask) << h) | (x >> h) for x in range(1 << n)]


def shared_edge_counts(n: int, start: list[int], target: list[int]) -> list[int]:
    """|S_p|: the number of other packets whose route shares an edge with the route of p."""
    users: dict[int, list[int]] = {}
    routes = []
    for p in range(len(start)):
        u, edges = start[p], []
        for i in bit_fixing_dims(n, start[p], target[p]):
            edges.append(u * n + i)
            u ^= 1 << i
        routes.append(edges)
        for e in edges:
            users.setdefault(e, []).append(p)
    out = []
    for p, edges in enumerate(routes):
        s = set()
        for e in edges:
            s.update(users[e])
        s.discard(p)
        out.append(len(s))
    return out
