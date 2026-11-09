# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctl-labelling-algorithm/. The authors are listed in prov/JZ943Y.jsonl.

"""The CTL labelling algorithm of Clarke, Emerson and Sistla (1986).

A Kripke structure is given by three plain values:
- states: a list of hashable states,
- succ: a dict that maps each state to the list of its successors,
- label: a dict that maps each state to the set of atomic propositions true there.

A CTL formula is a nested tuple:
("true",), ("false",), ("ap", p), ("not", f), ("and", f, g), ("or", f, g),
("implies", f, g), ("EX", f), ("AX", f), ("EU", f, g), ("AU", f, g),
("EF", f), ("AF", f), ("EG", f), ("AG", f).

sat(...) returns the set of states that satisfy the formula. Without fairness
it runs in O(|phi| (|S| + |R|)) time: each subformula costs O(|S| + |R|).
With justice sets and compassion pairs it uses fair SCC analysis.
"""

from collections import deque
from typing import Hashable, Iterable, Sequence

State = Hashable
Formula = tuple


def predecessors(states: Sequence[State], succ: dict) -> dict:
    """Return the reverse adjacency lists. O(|S| + |R|)."""
    pred: dict = {s: [] for s in states}
    for s in states:
        for t in succ[s]:
            pred[t].append(s)
    return pred


def subformulas(phi: Formula) -> list:
    """The distinct subformulas of phi, each one after all of its parts.

    An explicit stack gives a post-order without deep recursion.
    """
    order: list = []
    seen: set = set()
    stack = [(phi, False)]
    while stack:
        f, done = stack.pop()
        if done:
            if f not in seen:
                seen.add(f)
                order.append(f)
            continue
        if f in seen:
            continue
        stack.append((f, True))
        if f[0] not in ("ap", "true", "false"):
            for g in f[1:]:
                stack.append((g, False))
    return order


def check_ex(states: Sequence[State], succ: dict, a: set) -> set:
    """States with at least one successor in a."""
    return {s for s in states if any(t in a for t in succ[s])}


def check_eu(pred: dict, a: set, b: set) -> set:
    """E[a U b]: backward search from b through states of a. O(|S| + |R|)."""
    x = set(b)  # @line L13
    queue = deque(b)
    while queue:  # @line L14
        t = queue.popleft()  # @line L15
        for s in pred[t]:  # @line L16
            if s in a and s not in x:  # @line L17
                x.add(s)
                queue.append(s)
    return x  # @line L18


def check_au(states: Sequence[State], succ: dict, pred: dict, a: set, b: set) -> set:
    """A[a U b]: a state of a joins when all of its successors have joined.

    The counter of s holds the number of successors of s that have not joined.
    O(|S| + |R|).
    """
    count = {s: len(succ[s]) for s in states}  # @line L19
    x = set(b)
    queue = deque(b)
    while queue:  # @line L20
        t = queue.popleft()
        for s in pred[t]:  # @line L21
            count[s] -= 1
            if count[s] == 0 and s in a and s not in x:  # @line L22
                x.add(s)
                queue.append(s)
    return x  # @line L23


def sccs(nodes: Iterable[State], succ: dict, inside: set) -> list:
    """Tarjan's algorithm on the subgraph induced by `inside`, without recursion.

    Returns a list of SCCs, each a list of states. O(|S| + |R|).
    """
    index: dict = {}
    low: dict = {}
    on_stack: set = set()
    stack: list = []
    out: list = []
    counter = 0
    for root in nodes:
        if root not in inside or root in index:
            continue
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        work = [(root, iter(succ[root]))]
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in inside:
                    continue
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(succ[w])))
                    advanced = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def nontrivial(comp: list, succ: dict) -> bool:
    """An SCC is nontrivial when it has an edge: two or more states, or a self-loop."""
    return len(comp) > 1 or comp[0] in succ[comp[0]]


def check_eg(states: Sequence[State], succ: dict, pred: dict, a: set) -> set:
    """EG a: reach a nontrivial SCC of the subgraph on a, inside a. O(|S| + |R|)."""
    x: set = set()  # @line L24
    for comp in sccs(states, succ, a):
        if nontrivial(comp, succ):  # @line L25
            x.update(comp)
    queue = deque(x)
    while queue:  # @line L26
        t = queue.popleft()
        for s in pred[t]:  # @line L27
            if s in a and s not in x:
                x.add(s)
                queue.append(s)
    return x  # @line L28


def fair_cycle_states(states: Sequence[State], succ: dict, a: set, pairs: list) -> set:
    """States of the SCCs, inside a, that can carry a fair path forever.

    `pairs` is a list of compassion pairs (p, q): a fair path that visits p
    infinitely often also visits q infinitely often. A justice set J is the
    pair (all states, J). An SCC that visits p_i but not q_i loses the states
    of p_i, and its rest is split again. Each round removes all states of at
    least one pair, so there are at most len(pairs) + 1 rounds.
    """
    good: set = set()
    work = [set(a)]
    while work:
        part = work.pop()
        for comp in sccs(states, succ, part):
            if not nontrivial(comp, succ):
                continue
            cset = set(comp)
            bad = [p for (p, q) in pairs if cset & p and not cset & q]
            if not bad:
                good |= cset
            else:
                rest = cset.difference(*bad)
                if rest:
                    work.append(rest)
    return good


def check_fair_eg(states: Sequence[State], succ: dict, pred: dict, a: set, pairs: list) -> set:
    """E_f G a: reach, inside a, a fair SCC of the subgraph on a."""
    x = fair_cycle_states(states, succ, a, pairs)
    queue = deque(x)
    while queue:
        t = queue.popleft()
        for s in pred[t]:
            if s in a and s not in x:
                x.add(s)
                queue.append(s)
    return x


def sat(
    states: Sequence[State],
    succ: dict,
    label: dict,
    phi: Formula,
    justice: Sequence[set] = (),
    compassion: Sequence[tuple] = (),
) -> set:
    """Return the set of states of the Kripke structure that satisfy phi.

    Precondition: every state has at least one successor. With justice sets or
    compassion pairs, the path quantifiers range over fair paths only.
    """
    for s in states:
        if not succ[s]:
            raise ValueError(f"state {s!r} has no successor")
    all_states = set(states)
    pred = predecessors(states, succ)
    pairs = [(all_states, set(j)) for j in justice] + [(set(p), set(q)) for (p, q) in compassion]
    fair_on = bool(pairs)
    fair = check_fair_eg(states, succ, pred, all_states, pairs) if fair_on else all_states

    def eg(a: set) -> set:
        if fair_on:
            return check_fair_eg(states, succ, pred, a, pairs)
        return check_eg(states, succ, pred, a)

    def eu(a: set, b: set) -> set:
        return check_eu(pred, a, b & fair)

    def ex(a: set) -> set:
        return check_ex(states, succ, a & fair)

    def au(a: set, b: set) -> set:
        if not fair_on:
            return check_au(states, succ, pred, a, b)
        # A_f[a U b] = not E_f[not b U (not a and not b)] and not E_f G not b
        nb = all_states - b
        return all_states - (eu(nb, nb - a) | eg(nb))

    t: dict = {}
    for f in subformulas(phi):  # @line L1
        op = f[0]  # @line L2
        if op == "true":
            t[f] = set(all_states)
        elif op == "false":
            t[f] = set()
        elif op == "ap":
            t[f] = {s for s in states if f[1] in label[s]}  # @line L3
        elif op == "not":
            t[f] = all_states - t[f[1]]  # @line L4
        elif op == "and":
            t[f] = t[f[1]] & t[f[2]]  # @line L5
        elif op == "or":
            t[f] = t[f[1]] | t[f[2]]  # @line L6
        elif op == "implies":
            t[f] = (all_states - t[f[1]]) | t[f[2]]
        elif op == "EX":
            t[f] = ex(t[f[1]])  # @line L7
        elif op == "AX":
            t[f] = all_states - ex(all_states - t[f[1]])  # @line L8
        elif op == "EU":
            t[f] = eu(t[f[1]], t[f[2]])  # @line L9
        elif op == "AU":
            t[f] = au(t[f[1]], t[f[2]])  # @line L10
        elif op == "EG":
            t[f] = eg(t[f[1]])  # @line L11
        elif op == "EF":
            t[f] = eu(all_states, t[f[1]])
        elif op == "AF":
            t[f] = au(all_states, t[f[1]]) if not fair_on else all_states - eg(all_states - t[f[1]])
        elif op == "AG":
            t[f] = all_states - eu(all_states, all_states - t[f[1]])
        else:
            raise ValueError(f"unknown operator {op!r}")
    return t[phi]  # @line L12
