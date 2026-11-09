# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zielonka-algorithm/. The authors are listed in prov/X0EDJD.jsonl.

"""Zielonka's recursive algorithm for parity games.

A game is a dict that maps each vertex to a tuple (owner, priority, successors).
The owner is 0 (Even) or 1 (Odd), the priority is an int at least 0, and
successors is a non-empty list of vertices of the game. A play is won by
player 0 when the largest priority seen infinitely often is even.
"""

from collections import deque
from typing import Hashable

Vertex = Hashable
Game = dict[Vertex, tuple[int, int, list[Vertex]]]


def attractor(
    game: Game, alive: set[Vertex], target: set[Vertex], player: int
) -> tuple[set[Vertex], dict[Vertex, Vertex]]:
    """Return the attractor of `player` to `target` in the subgame on `alive`.

    Also return an attractor strategy: for each vertex of `player` in the
    attractor but not in the target, a successor that was added earlier.
    Precondition: target is a subset of alive, and every vertex of alive has a
    successor in alive. Cost: O(n + m) for the subgame.
    """
    attr = set(target)
    queue = deque(target)  # @line L13
    pred: dict[Vertex, list[Vertex]] = {v: [] for v in alive}
    count: dict[Vertex, int] = {}
    for v in alive:  # @line L14
        succ = [w for w in game[v][2] if w in alive]
        count[v] = len(succ)
        for w in succ:
            pred[w].append(v)
    strategy: dict[Vertex, Vertex] = {}
    while queue:  # @line L15
        w = queue.popleft()  # @line L16
        for v in pred[w]:  # @line L17
            if v in attr:
                continue
            if game[v][0] == player:  # @line L18
                attr.add(v)
                strategy[v] = w
                queue.append(v)
            else:
                count[v] -= 1  # @line L19
                if count[v] == 0:  # @line L20
                    attr.add(v)
                    queue.append(v)
    return attr, strategy  # @line L21


def _solve(game: Game, alive: set[Vertex]) -> tuple[list[set[Vertex]], dict[Vertex, Vertex]]:
    won: list[set[Vertex]] = [set(), set()]  # @line L1
    strat: dict[Vertex, Vertex] = {}
    g = set(alive)
    while g:  # @line L2
        p = max(game[v][1] for v in g)  # @line L3
        i = p % 2
        u = {v for v in g if game[v][1] == p}  # @line L4
        a, a_strat = attractor(game, g, u, i)  # @line L5
        sub, sub_strat = _solve(game, g - a)  # @line L6
        if not sub[1 - i]:  # @line L7
            won[i] |= g  # @line L8
            strat.update(sub_strat)
            strat.update(a_strat)
            for v in u:
                if game[v][0] == i:
                    strat[v] = next(w for w in game[v][2] if w in g)
            return won, strat
        b, b_strat = attractor(game, g, sub[1 - i], 1 - i)  # @line L9
        for v in sub[1 - i]:
            if game[v][0] == 1 - i:
                strat[v] = sub_strat[v]
        strat.update(b_strat)
        won[1 - i] |= b  # @line L10
        g -= b  # @line L11
    return won, strat  # @line L12


def zielonka(game: Game) -> tuple[set[Vertex], set[Vertex], dict[Vertex, Vertex]]:
    """Solve a parity game with the max-parity winning condition.

    Return (W0, W1, strategy). W0 and W1 partition the vertices. For each
    vertex v of W_j owned by player j, strategy[v] is a successor, and these
    choices form a positional strategy that wins for player j from all of W_j.
    Precondition: every successor list is non-empty and inside the game.
    Cost: O(m * (n + 1)^d) in the worst case, d the number of distinct
    priorities; the recursion depth is at most d + 1.
    """
    for v, (owner, prio, succ) in game.items():
        if owner not in (0, 1) or prio < 0 or not succ or any(w not in game for w in succ):
            raise ValueError(f"bad vertex {v!r}")
    won, strat = _solve(game, set(game))
    return won[0], won[1], strat
