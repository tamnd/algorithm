# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/games-on-graphs/. The authors are listed in prov/9S85XA.jsonl.

"""Two forms of the game on a directed graph, each with a linear-time
solver and a brute-force reference.

1. The token game: a token sits on a vertex, the player to move pushes it
   along an out-edge, a player with no move loses, and an infinite play is a
   draw. Each vertex gets W, L or D for the player to move.
2. The reachability game: each vertex has an owner (0 or 1) who moves from
   it, and player 0 wins when the token reaches a target vertex. The winning
   region of player 0 is the attractor of the target.

Vertices are 0..n-1 and edges are pairs (u, v)."""

from collections import deque
from typing import Dict, List, Sequence, Set, Tuple

WIN, LOSS, DRAW = "W", "L", "D"


def _adjacency(n: int, edges: Sequence[Tuple[int, int]]):
    succ: List[List[int]] = [[] for _ in range(n)]
    pred: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        succ[u].append(v)
        pred[v].append(u)
    return succ, pred


def solve_token_game(n: int, edges: Sequence[Tuple[int, int]]) -> List[str]:
    """Backward labeling with an out-degree counter, O(n + m)."""
    succ, pred = _adjacency(n, edges)
    label = [DRAW] * n
    left = [len(s) for s in succ]
    queue = deque(v for v in range(n) if left[v] == 0)
    for v in queue:
        label[v] = LOSS
    while queue:
        v = queue.popleft()
        for u in pred[v]:
            if label[u] != DRAW:
                continue
            if label[v] == LOSS:
                label[u] = WIN
                queue.append(u)
            else:
                left[u] -= 1
                if left[u] == 0:
                    label[u] = LOSS
                    queue.append(u)
    return label


def token_game_by_depth(n: int, edges: Sequence[Tuple[int, int]], depth: int) -> List[str]:
    """Reference: win_d(v) means the mover can force a win within d moves,
    lose_d(v) means the opponent can. Values not decided within depth are
    reported as draws."""
    succ, _ = _adjacency(n, edges)
    win = [False] * n
    lose = [False] * n
    for _ in range(depth):
        new_win = [any(lose[w] for w in succ[v]) for v in range(n)]
        new_lose = [all(win[w] for w in succ[v]) for v in range(n)]
        win, lose = new_win, new_lose
    return [WIN if win[v] else LOSS if lose[v] else DRAW for v in range(n)]


def attractor(
    n: int, edges: Sequence[Tuple[int, int]], owner: Sequence[int], target: Set[int], player: int = 0
) -> Set[int]:
    """Vertices from which player can force the token into target. A vertex
    of player joins when one successor is in the set; a vertex of the other
    player joins when all its successors are. A vertex with no successor that
    is not in target belongs to the other player's region."""
    succ, pred = _adjacency(n, edges)
    attr = set(target)
    left = [len(s) for s in succ]
    queue = deque(target)
    while queue:
        v = queue.popleft()
        for u in pred[v]:
            if u in attr:
                continue
            if owner[u] == player:
                attr.add(u)
                queue.append(u)
            else:
                left[u] -= 1
                if left[u] == 0:
                    attr.add(u)
                    queue.append(u)
    return attr


def reachability_by_depth(
    n: int, edges: Sequence[Tuple[int, int]], owner: Sequence[int], target: Set[int], depth: int
) -> Set[int]:
    """Reference: the set from which player 0 can reach target within depth
    moves, by the definition. A dead end that is not a target is a loss for
    player 0 whoever owns it."""
    succ, _ = _adjacency(n, edges)
    good = [v in target for v in range(n)]
    for _ in range(depth):
        new = []
        for v in range(n):
            if v in target:
                new.append(True)
            elif not succ[v]:
                new.append(False)
            elif owner[v] == 0:
                new.append(any(good[w] for w in succ[v]))
            else:
                new.append(all(good[w] for w in succ[v]))
        good = new
    return {v for v in range(n) if good[v]}


def token_game_as_reachability(n: int, edges: Sequence[Tuple[int, int]]):
    """The token game as a reachability game on two copies of the graph:
    vertex (v, p) means the token is on v and player p is to move. Player 0
    wins when player 1 is to move at a dead end."""
    succ, _ = _adjacency(n, edges)
    big_edges = []
    owner = []
    for p in (0, 1):
        for v in range(n):
            owner.append(p)
            for w in succ[v]:
                big_edges.append((p * n + v, (1 - p) * n + w))
    target = {n + v for v in range(n) if not succ[v]}
    return 2 * n, big_edges, owner, target


def random_graph(rng, n: int, p: float) -> List[Tuple[int, int]]:
    return [(u, v) for u in range(n) for v in range(n) if u != v and rng.random() < p]
