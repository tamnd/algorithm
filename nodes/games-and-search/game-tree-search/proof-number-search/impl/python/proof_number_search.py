# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proof-number-search/. The authors are listed in prov/8X9ESA.jsonl.

"""Proof-number search (Allis, van der Meulen and van den Herik 1994) on an
AND/OR tree.

The goal is to prove or disprove a statement about the root, such as "the
first player wins". At an OR node the prover moves and one proved child is
enough; at an AND node the opponent moves and every child must be proved.
The node types alternate. A game is given by two functions:

    children(state) -> list of states
    terminal(state, is_or) -> True (proved), False (disproved) or None

terminal is called first; children is called only when it returns None."""

import math
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

INF = math.inf


class Node:
    __slots__ = ("state", "is_or", "pn", "dn", "children", "parent", "value")

    def __init__(self, state: Any, is_or: bool, parent: Optional["Node"]):
        self.state = state
        self.is_or = is_or
        self.parent = parent
        self.children: Optional[List["Node"]] = None  # None until expanded
        self.value: Optional[bool] = None  # set for terminal nodes
        self.pn = 1
        self.dn = 1


def evaluate(node: Node, terminal) -> None:
    """Give a new node its numbers: 0 and INF for a proved terminal node,
    INF and 0 for a disproved one, 1 and 1 for an unknown frontier node."""
    node.value = terminal(node.state, node.is_or)
    if node.value is True:  # @line L16
        node.pn, node.dn = 0, INF  # @line L16
    elif node.value is False:  # @line L17
        node.pn, node.dn = INF, 0  # @line L17
    else:
        node.pn, node.dn = 1, 1  # @line L18


def set_numbers(node: Node) -> None:
    """The rules for an expanded node."""
    if node.is_or:  # @line L19
        node.pn = min(c.pn for c in node.children)  # @line L19
        node.dn = sum(c.dn for c in node.children)  # @line L19
    else:
        node.pn = sum(c.pn for c in node.children)  # @line L20
        node.dn = min(c.dn for c in node.children)  # @line L20


def select_most_proving(node: Node) -> Node:
    """Walk down from node: at an OR node to a child with the smallest proof
    number, at an AND node to a child with the smallest disproof number."""
    while node.children is not None:  # @line L4
        if node.is_or:  # @line L5
            node = next(c for c in node.children if c.pn == node.pn)  # @line L5
        else:
            node = next(c for c in node.children if c.dn == node.dn)  # @line L6
    return node


def expand(node: Node, children, terminal) -> None:
    kids = []
    for s in children(node.state):  # @line L7
        c = Node(s, not node.is_or, node)  # @line L7
        evaluate(c, terminal)  # @line L7
        kids.append(c)
    if not kids:
        # no move: the OR player fails here and the AND player has no escape
        node.value = not node.is_or
        node.pn, node.dn = (0, INF) if node.value else (INF, 0)
        return
    node.children = kids
    set_numbers(node)  # @line L8


def update_ancestors(node: Node) -> None:
    """Recompute the numbers on the path to the root; stop when a node keeps
    its numbers, since then no ancestor changes."""
    node = node.parent  # @line L9
    while node is not None:  # @line L10
        old = (node.pn, node.dn)  # @line L11
        set_numbers(node)  # @line L12
        if (node.pn, node.dn) == old:  # @line L13
            return  # @line L13
        node = node.parent  # @line L14


class Result:
    def __init__(self, value: Optional[bool], root: Node, expansions: int):
        self.value = value  # True proved, False disproved, None budget hit
        self.root = root
        self.expansions = expansions


def proof_number_search(
    state: Any,
    children: Callable[[Any], Sequence[Any]],
    terminal: Callable[[Any, bool], Optional[bool]],
    root_is_or: bool = True,
    max_expansions: Optional[int] = None,
    on_select: Optional[Callable[[Node, Node], None]] = None,
) -> Result:
    """Run PNS from `state`. on_select(root, node) is called with each node
    chosen for expansion, before it is expanded (for tests)."""
    root = Node(state, root_is_or, None)
    evaluate(root, terminal)  # @line L1
    expansions = 0
    while root.pn != 0 and root.dn != 0:  # @line L2
        if max_expansions is not None and expansions >= max_expansions:
            return Result(None, root, expansions)
        mpn = select_most_proving(root)  # @line L3
        if on_select is not None:
            on_select(root, mpn)
        expand(mpn, children, terminal)
        expansions += 1
        update_ancestors(mpn)
    return Result(root.pn == 0, root, expansions)  # @line L15


# Checks used by the tests and by the page.

def rules_hold(root: Node) -> bool:
    """Every node obeys the rules: terminal and frontier values, min and sum."""
    stack = [root]
    while stack:
        n = stack.pop()
        if n.children is None:
            want = (0, INF) if n.value is True else (INF, 0) if n.value is False else (1, 1)
        elif not n.children:
            return False
        elif n.is_or:
            want = (min(c.pn for c in n.children), sum(c.dn for c in n.children))
        else:
            want = (sum(c.pn for c in n.children), min(c.dn for c in n.children))
        if (n.pn, n.dn) != want:
            return False
        if n.children:
            stack.extend(n.children)
    return True


def root_numbers_if(node: Node, pn, dn) -> Tuple[Any, Any]:
    """The root numbers that would result if `node` had numbers (pn, dn),
    without changing the tree."""
    child, cpn, cdn = node, pn, dn
    n = node.parent
    while n is not None:
        pns = [cpn if c is child else c.pn for c in n.children]
        dns = [cdn if c is child else c.dn for c in n.children]
        if n.is_or:
            cpn, cdn = min(pns), sum(dns)
        else:
            cpn, cdn = sum(pns), min(dns)
        child, n = n, n.parent
    return cpn, cdn


def is_most_proving(root: Node, node: Node) -> bool:
    """Allis's property: proving the node lowers the root proof number by
    exactly one, and disproving it lowers the root disproof number by one."""
    after_proof = root_numbers_if(node, 0, INF)
    after_disproof = root_numbers_if(node, INF, 0)
    return after_proof[0] == root.pn - 1 and after_disproof[1] == root.dn - 1


def proof_tree_is_valid(node: Node) -> bool:
    """For a proved node: an OR node has a proved child, an AND node has
    all children proved, and the leaves are proved terminal positions."""
    if node.pn != 0:
        return False
    if node.children is None:
        return node.value is True
    if node.is_or:
        return any(proof_tree_is_valid(c) for c in node.children if c.pn == 0)
    return all(proof_tree_is_valid(c) for c in node.children)


def and_or_value(state, children, terminal, is_or: bool = True) -> bool:
    """Full AND/OR search: the reference answer."""
    t = terminal(state, is_or)
    if t is not None:
        return t
    vals = (and_or_value(s, children, terminal, not is_or) for s in children(state))
    return any(vals) if is_or else all(vals)


# Example problems.

def tree_problem(tree):
    """An explicit tree: True or False is a terminal node; a list is an
    interior node. States are (path, subtree) so that every node is named."""

    def children(state):
        path, sub = state
        return [(path + (i,), c) for i, c in enumerate(sub)]

    def terminal(state, is_or):
        sub = state[1]
        if isinstance(sub, bool):
            return sub
        if not sub:
            return not is_or  # a player with no move: OR fails, AND is proved
        return None

    return ((), tree), children, terminal


def random_tree(rng, depth: int, branching: Tuple[int, int], p_true: float, p_stop: float = 0.15):
    if depth == 0 or (depth < 4 and rng.random() < p_stop):
        return rng.random() < p_true
    return [random_tree(rng, depth - 1, branching, p_true, p_stop) for _ in range(rng.randint(*branching))]


def nim_problem(heaps: Sequence[int]):
    """Normal-play Nim: prove that the player to move at the root wins.
    The position is a sorted tuple of heap sizes."""

    def children(state):
        out = set()
        for i, h in enumerate(state):
            for k in range(h):
                out.add(tuple(sorted(state[:i] + (k,) + state[i + 1 :])))
        return sorted(out)

    def terminal(state, is_or):
        if not any(state):
            return not is_or  # the player to move has lost
        return None

    return tuple(sorted(heaps)), children, terminal


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def tic_tac_toe_problem(goal: str, board: str = "........."):
    """Tic-tac-toe with X to move at the root (X is the OR player).
    goal "win": X wins; goal "not lose": X wins or draws."""

    def line_of(b: str, p: str) -> bool:
        return any(b[i] == b[j] == b[k] == p for i, j, k in LINES)

    def children(b):
        p = "X" if b.count("X") == b.count("O") else "O"
        return [b[:i] + p + b[i + 1 :] for i in range(9) if b[i] == "."]

    def terminal(b, is_or):
        if line_of(b, "X"):
            return True
        if line_of(b, "O"):
            return False
        if "." not in b:
            return goal == "not lose"
        return None

    return board, children, terminal
