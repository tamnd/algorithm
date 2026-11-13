# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/monte-carlo-tree-search/. The authors are listed in prov/73PV1J.jsonl.

"""Monte Carlo tree search for two-player alternating games with payoffs in [0, 1].

Each iteration has the four phases of Coulom (2006) and Browne et al. (2012): select a path in the
stored tree with a tree policy (here UCB1), expand one new node, simulate a random playout to the
end of the game, and back up the result along the path. The move returned is the most visited
child of the root.

A game object has these methods for a state s:
    moves(s) -> list of moves, empty at the end of the game
    play(s, m) -> the state after move m (s is not changed)
    player(s) -> 0 or 1, the player to move
    reward(s) -> payoff in [0, 1] to player 0 at a terminal state (player 1 gets 1 minus it)
"""

import math
import random


class Node:
    __slots__ = ("move", "parent", "children", "untried", "visits", "wins", "mover")

    def __init__(self, untried, move=None, parent=None, mover=None):
        self.move = move
        self.parent = parent
        self.children: list["Node"] = []
        self.untried = list(untried)
        self.visits = 0
        self.wins = 0.0  # total reward of `mover`, the player who made `move`
        self.mover = mover

    def ucb(self, c: float) -> float:
        return self.wins / self.visits + c * math.sqrt(math.log(self.parent.visits) / self.visits)


def mcts(game, state, playouts: int, rng: random.Random, c: float = math.sqrt(2)):
    """Return (best move, root node) after `playouts` iterations from state.

    Precondition: state is not terminal, playouts >= 1. Cost: O(playouts * (depth + playout
    length)) game operations, and one stored node per iteration.
    """
    root = Node(game.moves(state))  # @line L1
    for _ in range(playouts):  # @line L2
        node, s = root, state  # @line L3
        # Selection: descend while every move of the node has a child.
        while not node.untried and node.children:
            node = max(node.children, key=lambda ch: ch.ucb(c))  # @line L4
            s = game.play(s, node.move)
        # Expansion: add one child for an untried move.
        if node.untried:
            m = node.untried.pop(rng.randrange(len(node.untried)))
            mover = game.player(s)
            s = game.play(s, m)
            child = Node(game.moves(s), m, node, mover)  # @line L5
            node.children.append(child)
            node = child
        # Simulation: uniform random moves to the end of the game.
        ms = game.moves(s)
        while ms:
            s = game.play(s, ms[rng.randrange(len(ms))])  # @line L6
            ms = game.moves(s)
        r = game.reward(s)  # @line L7
        # Backpropagation: each node keeps the reward of the player who moved into it.
        while node is not None:
            node.visits += 1  # @line L8
            if node.mover is not None:
                node.wins += r if node.mover == 0 else 1.0 - r
            node = node.parent
    best = max(root.children, key=lambda ch: ch.visits)  # @line L9
    return best.move, root


def flat_monte_carlo(game, state, playouts: int, rng: random.Random):
    """Baseline with no tree: share the playouts among the moves of the root and pick the best mean."""
    me = game.player(state)
    moves = game.moves(state)
    totals = [0.0] * len(moves)
    counts = [0] * len(moves)
    for k in range(playouts):
        i = k % len(moves)
        s = game.play(state, moves[i])
        ms = game.moves(s)
        while ms:
            s = game.play(s, ms[rng.randrange(len(ms))])
            ms = game.moves(s)
        r = game.reward(s)
        totals[i] += r if me == 0 else 1.0 - r
        counts[i] += 1
    means = [t / n if n else -1.0 for t, n in zip(totals, counts)]
    return moves[means.index(max(means))]


class TreeGame:
    """An explicit game tree: a leaf is a number in [0, 1] (payoff to player 0), an inner node is a
    list of children. Player 0 moves at even depth. A state is the path from the root."""

    def __init__(self, tree):
        self.tree = tree

    def node(self, s):
        t = self.tree
        for i in s:
            t = t[i]
        return t

    def moves(self, s):
        t = self.node(s)
        return list(range(len(t))) if isinstance(t, list) else []

    def play(self, s, m):
        return s + (m,)

    def player(self, s):
        return len(s) % 2

    def reward(self, s):
        return self.node(s)


class Nim:
    """Normal-play Nim: a move takes one or more objects from one heap, and the player who takes
    the last object wins. A state is (heaps, player to move)."""

    def moves(self, s):
        heaps, _ = s
        return [(i, k) for i, h in enumerate(heaps) for k in range(1, h + 1)]

    def play(self, s, m):
        heaps, p = s
        i, k = m
        return (heaps[:i] + (heaps[i] - k,) + heaps[i + 1:], 1 - p)

    def player(self, s):
        return s[1]

    def reward(self, s):
        # The player to move faces no objects: the other player took the last one.
        return 1.0 if s[1] == 1 else 0.0
