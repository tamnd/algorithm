# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alc-tableau-algorithm/. The authors are listed in prov/W9NV76.jsonl.
"""The tableau algorithm for ALC concept satisfiability, with an optional general TBox.

The search builds a tree of nodes depth first. Each node has a label, a set of concepts in negation
normal form. The and-rule and the or-rule complete the label of one node (the or-rule with
backtracking), then the exists-rule makes one child for each existential restriction, and the
all-rule puts the matching universal restrictions into the child. With a nonempty TBox, every node
also gets the concept nnf(not C or D) of each inclusion C subsumed by D, and subset blocking against
the ancestors stops the search. When the answer is yes, the result holds a finite model.
"""

from dataclasses import dataclass, field
from typing import Iterator, Optional, Sequence

from dl import BOTTOM, GCI, Concept, Interpretation, conj, disj, neg, nnf, show


class NonTermination(Exception):
    """Raised when a search without blocking passes the depth limit."""


@dataclass
class Stats:
    nodes: int = 0  # calls of NODE, one for each node that is expanded
    blocked: int = 0  # children that were not created because an ancestor blocks them
    clashes: int = 0  # completions that ended in a clash
    depth: int = 0  # the largest depth of a node, the root has depth 0


@dataclass
class Result:
    satisfiable: bool
    model: Optional[Interpretation] = None  # when satisfiable: a model, and element 0 is in the concept
    stats: Stats = field(default_factory=Stats)


class _Node:
    __slots__ = ("label", "edges")

    def __init__(self, label: frozenset) -> None:
        self.label = label
        self.edges: list[tuple[str, "_Node"]] = []


def _completions(s: frozenset, st: Stats) -> Iterator[frozenset]:
    """Yield the clash-free completions of the label s under the and-rule and the or-rule."""
    lab: set = set()
    stack = list(s)
    while stack:
        c = stack.pop()
        if c in lab:
            continue
        lab.add(c)
        if c[0] == "and":  # @line L11
            stack.append(c[1])
            stack.append(c[2])
    if BOTTOM in lab or any(c[0] == "not" and c[1] in lab for c in lab):  # @line L12
        st.clashes += 1
        return
    pending = [c for c in lab if c[0] == "or" and c[1] not in lab and c[2] not in lab]
    if pending:  # @line L13
        # Any choice of the disjunction is correct. Take first a disjunction with a disjunct that
        # clashes at once (bottom, or a literal whose complement is in the label), so that only one
        # branch is left. Break ties by the printed form, so that runs are repeatable.
        def dead(d: Concept) -> bool:
            return d == BOTTOM or (d[0] == "not" and d[1] in lab) or (d[0] == "atom" and ("not", d) in lab)

        c = min(pending, key=lambda c: (not (dead(c[1]) or dead(c[2])), show(c)))
        yield from _completions(frozenset(lab | {c[1]}), st)  # @line L14
        yield from _completions(frozenset(lab | {c[2]}), st)
    else:
        yield frozenset(lab)  # @line L15


def _node(s: frozenset, path: list, tc: frozenset, blocking: bool, max_depth: int, st: Stats) -> Optional[_Node]:
    """NODE(S, P): return the root of a model piece for the label s, or None when there is none."""
    st.nodes += 1
    st.depth = max(st.depth, len(path))
    if not blocking and len(path) > max_depth:
        raise NonTermination(f"depth {len(path)} without blocking")
    for lab in _completions(s, st):  # @line L3
        node = _Node(lab)
        ok = True  # @line L4
        for c in sorted((c for c in lab if c[0] == "some"), key=show):  # @line L5
            r = c[1]
            child = frozenset({c[2]} | {d[2] for d in lab if d[0] == "all" and d[1] == r}) | tc  # @line L6
            if blocking:
                blocker = next((a for a in path + [node] if child <= a.label), None)  # @line L7
                if blocker is not None:
                    st.blocked += 1
                    node.edges.append((r, blocker))
                    continue
            sub = _node(child, path + [node], tc, blocking, max_depth, st)  # @line L8
            if sub is None:
                ok = False
                break
            node.edges.append((r, sub))
        if ok:
            return node  # @line L9
    return None  # @line L10


def _model(root: _Node) -> Interpretation:
    ids: dict[int, int] = {id(root): 0}
    order = [root]
    k = 0
    while k < len(order):
        for _, t in order[k].edges:
            if id(t) not in ids:
                ids[id(t)] = len(order)
                order.append(t)
        k += 1
    conc: dict[str, set] = {}
    roles: dict[str, set] = {}
    for x, n in enumerate(order):
        for c in n.label:
            if c[0] == "atom":
                conc.setdefault(c[1], set()).add(x)
        for r, t in n.edges:
            roles.setdefault(r, set()).add((x, ids[id(t)]))
    return Interpretation(list(range(len(order))), conc, roles)


def tbox_concepts(tbox: Sequence[GCI]) -> frozenset:
    """The concepts nnf(not C or D), one for each inclusion C subsumed by D."""
    return frozenset(nnf(disj(neg(c), d)) for c, d in tbox)  # @line L1


def tableau(c: Concept, tbox: Sequence[GCI] = (), blocking: Optional[bool] = None, max_depth: int = 60) -> Result:
    """SAT(C, T). Decide whether c is satisfiable with respect to the TBox.

    Blocking is on by default when the TBox is not empty. With blocking off and a cyclic TBox the
    search need not stop; it raises NonTermination at max_depth.
    """
    tc = tbox_concepts(tbox)
    if blocking is None:
        blocking = bool(tc)
    st = Stats()
    root = _node(frozenset({nnf(c)}) | tc, [], tc, blocking, max_depth, st)  # @line L2
    if root is None:
        return Result(False, None, st)
    return Result(True, _model(root), st)


def is_satisfiable(c: Concept, tbox: Sequence[GCI] = ()) -> bool:
    return tableau(c, tbox).satisfiable


def subsumes(c: Concept, d: Concept, tbox: Sequence[GCI] = ()) -> bool:
    """True when c is subsumed by d with respect to the TBox: c and not d is unsatisfiable."""
    return not tableau(conj(c, neg(d)), tbox).satisfiable
