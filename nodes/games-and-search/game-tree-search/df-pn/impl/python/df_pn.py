# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/df-pn/. The authors are listed in prov/PYWCCV.jsonl.

"""Depth-first proof-number search (df-pn, Nagai 2002) with a transposition
table, and the 1 + epsilon threshold of Pawlewicz and Lew as an option.

The problem is the one of proof-number search: prove a goal at an AND/OR
tree or DAG. A game is given by

    children(state) -> list of states
    terminal(state, is_or) -> True (proved), False (disproved) or None

and the node types alternate, OR at the root unless root_is_or is False.
The table maps (state, is_or) to the pair (pn, dn); a missing entry means a
frontier node with numbers (1, 1)."""

import math
from typing import Any, Callable, Dict, Optional, Sequence, Tuple

INF = math.inf
Key = Tuple[Any, bool]


class DfpnResult:
    def __init__(self, value: Optional[bool], table: Dict[Key, Tuple[Any, Any]], mid_calls: int, expanded: int):
        self.value = value  # True proved, False disproved, None budget hit
        self.table = table
        self.mid_calls = mid_calls
        self.expanded = expanded  # number of distinct nodes whose children were generated


class _Budget(Exception):
    pass


def dfpn(
    state: Any,
    children: Callable[[Any], Sequence[Any]],
    terminal: Callable[[Any, bool], Optional[bool]],
    root_is_or: bool = True,
    epsilon: Optional[float] = None,
    max_mid_calls: Optional[int] = None,
    on_expand: Optional[Callable[[Any, bool], None]] = None,
    on_mid: Optional[Callable[[Any, bool, Any, Any], None]] = None,
) -> DfpnResult:
    table: Dict[Key, Tuple[Any, Any]] = {}
    expanded = set()
    calls = 0

    def lookup(s: Any, is_or: bool) -> Tuple[Any, Any]:
        key = (s, is_or)
        if key in table:
            return table[key]
        t = terminal(s, is_or)
        if t is True:
            table[key] = (0, INF)
        elif t is False:
            table[key] = (INF, 0)
        else:
            return (1, 1)
        return table[key]

    def mid(s: Any, is_or: bool, thpn, thdn) -> None:
        nonlocal calls
        calls += 1
        if max_mid_calls is not None and calls > max_mid_calls:
            raise _Budget
        if on_mid is not None:
            on_mid(s, is_or, thpn, thdn)
        key = (s, is_or)
        if terminal(s, is_or) is not None:  # @line L3
            lookup(s, is_or)  # @line L3
            return  # @line L3
        kids = list(children(s))  # @line L4
        if key not in expanded:
            expanded.add(key)
            if on_expand is not None:
                on_expand(s, is_or)
        if not kids:
            table[key] = (INF, 0) if is_or else (0, INF)
            return
        while True:  # @line L5
            nums = [lookup(c, not is_or) for c in kids]  # @line L6
            if is_or:
                pn = min(p for p, _ in nums)  # @line L6
                dn = sum(d for _, d in nums)  # @line L6
            else:
                pn = sum(p for p, _ in nums)  # @line L6
                dn = min(d for _, d in nums)  # @line L6
            if pn >= thpn or dn >= thdn:  # @line L7
                table[key] = (pn, dn)  # @line L7
                return  # @line L7
            if is_or:  # @line L8
                i = min(range(len(kids)), key=lambda j: nums[j][0])  # @line L9
                p2 = min((nums[j][0] for j in range(len(kids)) if j != i), default=INF)  # @line L9
                mid(kids[i], False, min(thpn, step(p2)), thdn - dn + nums[i][1])  # @line L10
            else:  # @line L11
                i = min(range(len(kids)), key=lambda j: nums[j][1])  # @line L12
                d2 = min((nums[j][1] for j in range(len(kids)) if j != i), default=INF)  # @line L12
                mid(kids[i], True, thpn - pn + nums[i][0], min(thdn, step(d2)))  # @line L13

    def step(second):
        """The bound for the best child: one more than the second best, or
        the 1 + epsilon form of Pawlewicz and Lew."""
        if epsilon is None or second == INF:
            return second + 1
        return max(second + 1, math.ceil(second * (1 + epsilon)))

    try:
        mid(state, root_is_or, INF, INF)  # @line L1
    except _Budget:
        return DfpnResult(None, table, calls, len(expanded))
    pn, dn = lookup(state, root_is_or)
    return DfpnResult(pn == 0, table, calls, len(expanded))  # @line L2


# Checks used by the tests.

def numbers_from_children(table, state, is_or, children, terminal) -> Tuple[Any, Any]:
    """The pair that the rules give for an expanded node, from the table."""

    def get(s, o):
        if (s, o) in table:
            return table[(s, o)]
        t = terminal(s, o)
        return (0, INF) if t is True else (INF, 0) if t is False else (1, 1)

    nums = [get(c, not is_or) for c in children(state)]
    if is_or:
        return min(p for p, _ in nums), sum(d for _, d in nums)
    return sum(p for p, _ in nums), min(d for _, d in nums)


def proof_is_valid(table, state, is_or, children, terminal) -> bool:
    """Follow the table: an OR node needs a child with pn 0, an AND node
    needs all children with pn 0, down to proved terminal positions."""
    t = terminal(state, is_or)
    if t is not None:
        return t
    kids = children(state)
    if not kids:
        return not is_or
    proved = [c for c in kids if table.get((c, not is_or), (1, 1))[0] == 0 or terminal(c, not is_or) is True]
    if is_or:
        return any(proof_is_valid(table, c, False, children, terminal) for c in proved)
    return len(proved) == len(kids) and all(proof_is_valid(table, c, True, children, terminal) for c in kids)


def and_or_value(state, children, terminal, is_or: bool = True, memo=None) -> bool:
    """Full AND/OR search with a memo: the reference answer."""
    if memo is None:
        memo = {}
    key = (state, is_or)
    if key in memo:
        return memo[key]
    t = terminal(state, is_or)
    if t is None:
        vals = (and_or_value(s, children, terminal, not is_or, memo) for s in children(state))
        t = any(vals) if is_or else all(vals)
    memo[key] = t
    return t


def mirror_numbers(state, is_or, expanded, children, terminal, override=None) -> Tuple[Any, Any]:
    """Proof and disproof numbers of the PNS tree whose expanded nodes are
    `expanded`, computed from scratch. override maps a key to forced numbers."""
    key = (state, is_or)
    if override and key in override:
        return override[key]
    t = terminal(state, is_or)
    if t is True:
        return 0, INF
    if t is False:
        return INF, 0
    if key not in expanded:
        return 1, 1
    nums = [mirror_numbers(c, not is_or, expanded, children, terminal, override) for c in children(state)]
    if not nums:
        return (INF, 0) if is_or else (0, INF)
    if is_or:
        return min(p for p, _ in nums), sum(d for _, d in nums)
    return sum(p for p, _ in nums), min(d for _, d in nums)


# Example problems (the same as on the proof-number search page).

def tree_problem(tree):
    def children(state):
        path, sub = state
        return [(path + (i,), c) for i, c in enumerate(sub)] if isinstance(sub, tuple) else []

    def terminal(state, is_or):
        sub = state[1]
        if isinstance(sub, bool):
            return sub
        if not sub:
            return not is_or
        return None

    def freeze(t):
        return t if isinstance(t, bool) else tuple(freeze(c) for c in t)

    return ((), freeze(tree)), children, terminal


def random_tree(rng, depth: int, branching: Tuple[int, int], p_true: float, p_stop: float = 0.15):
    if depth == 0 or (depth < 4 and rng.random() < p_stop):
        return rng.random() < p_true
    return [random_tree(rng, depth - 1, branching, p_true, p_stop) for _ in range(rng.randint(*branching))]


def nim_problem(heaps: Sequence[int]):
    def children(state):
        out = set()
        for i, h in enumerate(state):
            for k in range(h):
                out.add(tuple(sorted(state[:i] + (k,) + state[i + 1 :])))
        return sorted(out)

    def terminal(state, is_or):
        return (not is_or) if not any(state) else None

    return tuple(sorted(heaps)), children, terminal


LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def tic_tac_toe_problem(goal: str, board: str = "........."):
    def line_of(b, p):
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
