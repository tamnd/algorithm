# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diagnoser-automaton/. The authors are listed in prov/8VN8F2.jsonl.

"""The diagnoser of Sampath et al. (1995) for a partially observed automaton.

The plant G is a dict with the keys "init" and "delta" (a dict that maps
(state, event) to the next state). `observable` is the set of observable
events. `faults` maps each fault event to its fault type; fault events must
be unobservable. A label is a frozenset of fault types; the empty label is
"normal".

diagnoser(g, observable, faults) returns {"init", "states", "delta"}. A
diagnoser state is a frozenset of pairs (x, label). After an observed word
y, the state holds exactly the pairs (state of G, faults so far) of the
strings s of L(G) with P(s) = y that end with an observable event (or s is
empty and y is empty). This needs no cycle of unobservable events in G.

diagnosable(g, observable, faults, kind) decides diagnosability for one
fault type by a search for an indeterminate cycle: a cycle in the graph of
triples (diagnoser state, a pair with the fault, a pair without it).

Cost: the diagnoser has at most 2^(|X| 2^m) states for |X| states of G and
m fault types. Each diagnoser transition costs O(|X|^2 4^m) set operations
after the moves of every pair are cached.
"""

from collections import deque
from typing import Hashable, Iterable

Pair = tuple
Label = frozenset


def out_edges(delta: dict) -> dict:
    out: dict = {}
    for (q, e), r in delta.items():
        out.setdefault(q, {})[e] = r
    return out


def moves(out: dict, pair: Pair, observable: set, faults: dict) -> dict:
    """For a pair (x, label), map each observable event sigma to the set of pairs reached by u sigma, u unobservable."""
    result: dict = {}
    seen = {pair}
    stack = [pair]
    while stack:
        x, label = stack.pop()
        for e, y in out.get(x, {}).items():
            if e in observable:
                result.setdefault(e, set()).add((y, label))
            else:
                nxt = (y, label | {faults[e]} if e in faults else label)
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return result


class _Moves:
    """Cache of moves() for one plant."""

    def __init__(self, g: dict, observable: Iterable, faults: dict):
        self.out = out_edges(g["delta"])
        self.observable = set(observable)
        self.faults = dict(faults)
        self.cache: dict = {}

    def __call__(self, pair: Pair) -> dict:
        if pair not in self.cache:
            self.cache[pair] = moves(self.out, pair, self.observable, self.faults)
        return self.cache[pair]


def diagnoser(g: dict, observable: Iterable, faults: dict) -> dict:
    """The diagnoser automaton of g, built on the reachable diagnoser states."""
    mv = _Moves(g, observable, faults)
    events = sorted(mv.observable, key=repr)
    q0 = frozenset({(g["init"], Label())})  # @line L1
    states = {q0}
    delta = {}
    queue = deque([q0])  # @line L2
    while queue:  # @line L3
        q = queue.popleft()  # @line L4
        for sigma in events:  # @line L5
            nxt: set = set()  # @line L6
            for pair in q:  # @line L7
                nxt |= mv(pair).get(sigma, set())
            if nxt:  # @line L8
                r = frozenset(nxt)
                delta[(q, sigma)] = r
                if r not in states:
                    states.add(r)
                    queue.append(r)
    return {"init": q0, "states": states, "delta": delta}  # @line L9


def verdict(q: frozenset, kind: Hashable) -> str:
    """'F' if every pair of q has the fault type, 'N' if none has it, else 'uncertain'."""
    has = [kind in label for _, label in q]
    if all(has):
        return "F"
    if not any(has):
        return "N"
    return "uncertain"


def observe(d: dict, word: Iterable) -> frozenset:
    """The diagnoser state after the observed word, or None if the word cannot be observed."""
    q = d["init"]
    for sigma in word:
        q = d["delta"].get((q, sigma))
        if q is None:
            return None
    return q


def has_cycle(nodes: set, succ: dict) -> bool:
    """Kahn's algorithm: True if the graph on nodes has a cycle."""
    indeg = {v: 0 for v in nodes}
    for v in nodes:
        for w in succ.get(v, ()):
            indeg[w] += 1
    queue = deque(v for v in nodes if indeg[v] == 0)
    removed = 0
    while queue:
        v = queue.popleft()
        removed += 1
        for w in succ.get(v, ()):
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    return removed < len(nodes)


def diagnosable(g: dict, observable: Iterable, faults: dict, kind: Hashable) -> bool:
    """True if the fault type `kind` is diagnosable: no indeterminate cycle in the diagnoser."""
    mv = _Moves(g, observable, faults)
    d = diagnoser(g, observable, faults)  # @line L10
    nodes = set()
    for q in d["states"]:  # @line L11
        for a in q:
            for b in q:
                if kind in a[1] and kind not in b[1]:
                    nodes.add((q, a, b))
    succ: dict = {}
    for q, a, b in nodes:  # @line L12
        for sigma in mv.observable:
            r = d["delta"].get((q, sigma))
            if r is None:
                continue
            for a2 in mv(a).get(sigma, ()):
                for b2 in mv(b).get(sigma, ()):
                    if kind not in b2[1]:
                        succ.setdefault((q, a, b), []).append((r, a2, b2))
    return not has_cycle(nodes, succ)  # @line L13


def has_uncertain_cycle(g: dict, observable: Iterable, faults: dict, kind: Hashable) -> bool:
    """True if the diagnoser has a cycle of uncertain states. If False, the fault type is diagnosable; True proves nothing."""
    d = diagnoser(g, observable, faults)
    nodes = {q for q in d["states"] if verdict(q, kind) == "uncertain"}
    succ: dict = {}
    for (q, _), r in d["delta"].items():
        if q in nodes and r in nodes:
            succ.setdefault(q, []).append(r)
    return has_cycle(nodes, succ)
