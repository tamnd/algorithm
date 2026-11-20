# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subgame-perfect-equilibrium/. The authors are listed in prov/E96CN1.jsonl.
"""Backward induction on a finite game tree of perfect information.

A tree is a dict from node ids to nodes, with the root at id 0:

    ("leaf", (u_1, ..., u_n))              payoffs, as Fraction
    ("chance", [(p, child), ...])          probabilities as Fraction, summing to 1
    ("move", i, [(action, child), ...])    player i (0-based) chooses an action

A pure strategy profile of the whole game is a dict from the ids of the
"move" nodes to actions. Every node of a perfect information game starts a
subgame, so a subgame perfect equilibrium is a profile that is a Nash
equilibrium below every node.
"""

from fractions import Fraction
from itertools import product


def backward_induction(tree, root=0):
    """Return (value, profile, calls).

    value[h] is the payoff vector of the subgame at h under the returned
    profile, profile[h] is the action chosen at each move node, and calls is
    the number of nodes visited (each node once). Ties go to the first
    action in the list of the node.
    """
    value = {}
    profile = {}
    calls = [0]

    def solve(h):
        calls[0] += 1
        node = tree[h]
        if node[0] == "leaf":  # @line L1
            value[h] = tuple(node[1])
            return value[h]
        if node[0] == "chance":  # @line L2
            parts = [(p, solve(c)) for p, c in node[1]]
            n = len(parts[0][1])
            value[h] = tuple(sum((p * v[k] for p, v in parts), Fraction(0)) for k in range(n))
            return value[h]
        _, i, moves = node  # @line L3
        best = None
        for a, c in moves:  # @line L4
            v = solve(c)  # @line L5
            if best is None or v[i] > best[i]:  # @line L6
                best = v
                profile[h] = a
        value[h] = best  # @line L7
        return best

    solve(root)
    return value, profile, calls[0]


def play_value(tree, profile, h=0):
    """The expected payoff vector of the subgame at h when everyone follows profile."""
    node = tree[h]
    if node[0] == "leaf":
        return tuple(node[1])
    if node[0] == "chance":
        parts = [(p, play_value(tree, profile, c)) for p, c in node[1]]
        n = len(parts[0][1])
        return tuple(sum((p * v[k] for p, v in parts), Fraction(0)) for k in range(n))
    _, _, moves = node
    child = dict(moves)[profile[h]]
    return play_value(tree, profile, child)


def move_nodes(tree, h=0):
    """The ids of the move nodes in the subgame at h, in depth-first order."""
    node = tree[h]
    if node[0] == "leaf":
        return []
    if node[0] == "chance":
        out = []
        for _, c in node[1]:
            out += move_nodes(tree, c)
        return out
    out = [h]
    for _, c in node[2]:
        out += move_nodes(tree, c)
    return out


def all_pure_profiles(tree):
    """Every pure strategy profile of the whole game, as dicts."""
    nodes = move_nodes(tree)
    choices = [[a for a, _ in tree[h][2]] for h in nodes]
    for pick in product(*choices):
        yield dict(zip(nodes, pick))


def is_nash_in_subgame(tree, profile, h):
    """Brute force: no player gains by any change of their own actions below h."""
    base = play_value(tree, profile, h)
    nodes = move_nodes(tree, h)
    players = {tree[g][1] for g in nodes}
    for i in players:
        own = [g for g in nodes if tree[g][1] == i]
        choices = [[a for a, _ in tree[g][2]] for g in own]
        for pick in product(*choices):
            dev = dict(profile)
            dev.update(zip(own, pick))
            if play_value(tree, dev, h)[i] > base[i]:
                return False
    return True


def is_subgame_perfect(tree, profile):
    """A pure profile is subgame perfect if it is Nash below every inner node."""
    inner = [h for h, node in tree.items() if node[0] != "leaf"]
    return all(is_nash_in_subgame(tree, profile, h) for h in inner)
