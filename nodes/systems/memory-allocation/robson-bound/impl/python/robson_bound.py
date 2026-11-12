# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robson-bound/. The authors are listed in prov/71MSB3.jsonl.

"""Robson's bound on the heap size of a non-moving online allocator.

A heap state is a sorted tuple of live blocks (p, s): the block covers the
addresses p, p+1, ..., p+s-1. The program keeps at most M words live and
asks only for sizes 1, 2, 4, ..., n. The heap size of a run is the largest
address used plus one.
"""

from collections import deque
from collections.abc import Callable

Block = tuple[int, int]
State = tuple[Block, ...]
Policy = Callable[[State, int], int]


def power_sizes(n: int) -> list[int]:
    return [1 << i for i in range(n.bit_length()) if (1 << i) <= n]


def robson_power_of_two(m: int, n: int) -> int:
    """Robson (1974): the least safe heap size, sizes powers of two, n | M."""
    if n < 1 or n & (n - 1) or m % n:
        raise ValueError("n must be a power of two that divides M")
    k = n.bit_length() - 1
    return m + (m * k) // 2 - n + 1


def end(state: State) -> int:
    return max((p + s for p, s in state), default=0)


def is_free(state: State, p: int, s: int) -> bool:
    return all(p + s <= q or q + t <= p for q, t in state)


def first_fit(state: State, s: int) -> int:
    """Lowest address p such that [p, p+s) meets no live block."""
    p = 0
    while not is_free(state, p, s):
        p += 1
    return p


def segregated_policy(m: int) -> Policy:
    """Class 2^j gets its own region [j*M, (j+1)*M) cut into aligned slots."""

    def place(state: State, s: int) -> int:
        j = s.bit_length() - 1
        for p in range(j * m, (j + 1) * m - s + 1, s):
            if is_free(state, p, s):
                return p
        raise RuntimeError("no free slot; the bound M(log2 n + 1) is violated")

    return place


def game_min_heap(m: int, n: int) -> int:
    """Exact least H such that some allocator survives every sequence.

    It solves the safety game in [0, H): the adversary wins from a state if it
    can free a block into a winning state, or ask for a size s with
    live + s <= M such that every free place for s leads to a winning state.
    """
    sizes = power_sizes(n)

    def states(h: int) -> list[State]:
        out: list[State] = []
        stack: list[tuple[int, State, int]] = [(0, (), 0)]
        while stack:
            p, blocks, live = stack.pop()
            if p >= h:
                out.append(blocks)
                continue
            stack.append((p + 1, blocks, live))
            for s in sizes:
                if p + s <= h and live + s <= m:
                    stack.append((p + s, blocks + ((p, s),), live + s))
        return out

    def adversary_wins(h: int) -> bool:
        every = states(h)
        lost: set[State] = set()
        changed = True
        while changed:
            changed = False
            for c in every:
                if c in lost:
                    continue
                live = sum(s for _, s in c)
                win = any(c[:i] + c[i + 1:] in lost for i in range(len(c)))
                for s in sizes:
                    if win or live + s > m:
                        continue
                    safe = any(
                        is_free(c, p, s)
                        and tuple(sorted(c + ((p, s),))) not in lost
                        for p in range(h - s + 1)
                    )
                    win = not safe
                if win:
                    lost.add(c)
                    changed = True
        return () in lost

    h = m
    while adversary_wins(h):
        h += 1
    return h


def worst_heap(m: int, n: int, place: Policy) -> tuple[int, list[tuple]]:
    """Largest heap size a fixed policy reaches over all request sequences.

    Breadth-first search over the reachable states. It returns the size and
    one shortest request sequence that reaches it.
    """
    sizes = power_sizes(n)
    parent: dict[State, tuple[State, tuple] | None] = {(): None}
    queue: deque[State] = deque([()])
    best, arg = 0, ()
    while queue:
        c = queue.popleft()
        live = sum(s for _, s in c)
        moves = [(c[:i] + c[i + 1:], ("free", c[i])) for i in range(len(c))]
        for s in sizes:
            if live + s <= m:
                p = place(c, s)
                moves.append((tuple(sorted(c + ((p, s),))), ("alloc", s, p)))
        for nc, mv in moves:
            if nc not in parent:
                parent[nc] = (c, mv)
                queue.append(nc)
                if end(nc) > best:
                    best, arg = end(nc), nc
    path: list[tuple] = []
    c = arg
    while parent[c] is not None:
        c, mv = parent[c]
        path.append(mv)
    return best, path[::-1]


def two_size_adversary(place: Policy, m: int) -> int:
    """The adversary of the proof for sizes 1 and 2; returns the heap reached."""
    if m % 4:
        raise ValueError("the proof assumes that 4 divides M")
    state: State = ()
    top = 0
    for _ in range(m):
        p = place(state, 1)
        if not is_free(state, p, 1):
            raise RuntimeError("the policy returned a used address")
        state = tuple(sorted(state + ((p, 1),)))
        top = max(top, p + 1)
    even = [b for b in state if b[0] % 2 == 0]
    odd = [b for b in state if b[0] % 2 == 1]
    kept = even if len(even) >= len(odd) else odd
    if len(kept) % 2:
        kept = kept[1:]
    state = tuple(kept)
    for _ in range((m - len(kept)) // 2):
        p = place(state, 2)
        if not is_free(state, p, 2):
            raise RuntimeError("the policy returned a used address")
        state = tuple(sorted(state + ((p, 2),)))
        top = max(top, p + 2)
    return top
