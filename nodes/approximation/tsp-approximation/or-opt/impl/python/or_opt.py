# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/or-opt/. The authors are listed in prov/WJY5MZ.jsonl.

from typing import Sequence

EPS = 1e-12


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    n = len(tour)
    if n < 2:
        return 0.0
    return sum(cost[tour[i]][tour[(i + 1) % n]] for i in range(n))


def or_moves(n: int, max_len: int = 3):
    """All Or-opt moves (s, length, p, flip) on a tour of n cities.

    The segment tour[s .. s+length-1] (positions modulo n) goes between the cities at positions
    p and p+1, which are outside the segment and not its two neighbors' pair. flip reverses it.
    """
    for length in range(1, min(max_len, n - 3) + 1):
        for s in range(n):
            inside = {(s + t) % n for t in range(length)}
            before = (s - 1) % n
            for p in range(n):
                if p in inside or p == before:
                    continue
                for flip in (False, True):
                    if length == 1 and flip:
                        continue
                    yield s, length, p, flip


def or_gain(cost: Sequence[Sequence[float]], tour: Sequence[int], s: int, length: int, p: int, flip: bool) -> float:
    n = len(tour)
    first, last = tour[s], tour[(s + length - 1) % n]
    prev, after = tour[(s - 1) % n], tour[(s + length) % n]
    u, v = tour[p], tour[(p + 1) % n]
    head, tail = (last, first) if flip else (first, last)
    removed = cost[prev][first] + cost[last][after] + cost[u][v]
    added = cost[prev][after] + cost[u][head] + cost[tail][v]
    return removed - added


def apply_or_move(tour: Sequence[int], s: int, length: int, p: int, flip: bool) -> list[int]:
    n = len(tour)
    segment = [tour[(s + t) % n] for t in range(length)]
    rest = [tour[(s + length + t) % n] for t in range(n - length)]  # starts after the segment
    u = tour[p]
    at = rest.index(u) + 1
    return rest[:at] + (segment[::-1] if flip else segment) + rest[at:]


def or_opt(cost: Sequence[Sequence[float]], tour: Sequence[int], max_len: int = 3) -> tuple[list[int], int]:
    """Move segments of 1 to max_len cities, in either direction, while a move gains."""
    t = list(tour)
    moves = 0
    improved = True
    while improved:  # @line L1
        improved = False
        for s, length, p, flip in or_moves(len(t), max_len):  # @line L2
            if or_gain(cost, t, s, length, p, flip) > EPS:  # @line L3
                t = apply_or_move(t, s, length, p, flip)  # @line L4
                moves += 1
                improved = True
                break
    return t, moves  # @line L5


def is_or_optimal(cost: Sequence[Sequence[float]], tour: Sequence[int], max_len: int = 3) -> bool:
    return all(or_gain(cost, tour, *move) <= EPS for move in or_moves(len(tour), max_len))
