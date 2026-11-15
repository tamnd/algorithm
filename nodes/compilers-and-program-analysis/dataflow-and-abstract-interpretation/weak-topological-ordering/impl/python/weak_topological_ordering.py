# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-topological-ordering/. The authors are listed in prov/X5B201.jsonl.
"""Bourdoncle's weak topological ordering and the recursive iteration strategy.

A graph is given by a function succ(v) that returns the successors of v in a
fixed order, and a root. weak_topological_ordering returns a list of elements;
an element is a vertex or a Component(head, body), where body is again a list
of elements. iterate runs the recursive strategy over such a list.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Generator, Hashable, Iterable, TypeVar, Union

D = TypeVar("D")

INF = math.inf


@dataclass
class Component:
    """A component of a WTO: its head, then its body, which is a WTO itself."""

    head: Hashable
    body: list["Element"] = field(default_factory=list)


Element = Union[Hashable, Component]
Frame = Generator[tuple, object, object]


class _State:
    def __init__(self, succ: Callable[[Hashable], Iterable[Hashable]]) -> None:
        self.succ = succ
        self.dfn: dict[Hashable, float] = {}  # a missing key means DFN = 0
        self.num = 0
        self.stack: list[Hashable] = []


def _visit(v: Hashable, part: list[Element], st: _State) -> Frame:
    st.stack.append(v)  # @line L5
    st.num += 1  # @line L5
    st.dfn[v] = st.num  # @line L5
    head: float = st.dfn[v]  # @line L6
    loop = False  # @line L6
    for w in st.succ(v):  # @line L7
        if st.dfn.get(w, 0) == 0:  # @line L8
            low = yield ("visit", w, part)  # @line L8
        else:
            low = st.dfn[w]  # @line L8
        if low <= head:  # @line L9
            head = low  # @line L9
            loop = True  # @line L9
    if head == st.dfn[v]:  # @line L10
        st.dfn[v] = INF  # @line L11
        e = st.stack.pop()  # @line L11
        if loop:  # @line L12
            while e != v:  # @line L13
                st.dfn[e] = 0  # @line L13
                e = st.stack.pop()  # @line L13
            comp = yield ("component", v)  # @line L14
            part.append(comp)  # @line L14
        else:
            part.append(v)  # @line L15
    return head  # @line L16


def _component(v: Hashable, st: _State) -> Frame:
    body: list[Element] = []  # @line L17
    for w in st.succ(v):  # @line L18
        if st.dfn.get(w, 0) == 0:  # @line L19
            yield ("visit", w, body)  # @line L19
    body.reverse()  # elements were appended; one reversal equals adding each to the front
    return Component(v, body)  # @line L20


def weak_topological_ordering(
    succ: Callable[[Hashable], Iterable[Hashable]], root: Hashable
) -> list[Element]:
    """Return Bourdoncle's WTO of the vertices reachable from root.

    The WTO is a list of vertices and Components in a nested topological
    order: every cycle of the graph contains the head of a component that
    contains the whole cycle. Successors are explored in the order that succ
    gives. Precondition: succ(v) is defined for every vertex reachable from
    root. Cost: O((k + 1)(n + m)) time for n reachable vertices, m edges
    among them and nesting depth k, and O(n) extra space; no Python recursion.
    """
    st = _State(succ)  # @line L1
    part: list[Element] = []  # @line L2
    # Each generator frame plays the role of one recursive call. A frame
    # yields a request ("visit", w, partition) or ("component", v); the driver
    # starts a new frame for it and sends the frame's result back.
    frames: list[Frame] = [_visit(root, part, st)]  # @line L3
    value: object = None
    while frames:
        try:
            req = frames[-1].send(value)
        except StopIteration as stop:
            frames.pop()
            value = stop.value
            continue
        value = None
        if req[0] == "visit":
            frames.append(_visit(req[1], req[2], st))
        else:
            frames.append(_component(req[1], st))
    part.reverse()  # elements were appended; one reversal equals adding each to the front
    return part  # @line L4


class _Values(dict):
    """The current values; a vertex with no value yet has the value bottom."""

    def __init__(self, bottom: object) -> None:
        super().__init__()
        self.bottom = bottom

    def __missing__(self, key: Hashable) -> object:
        return self.bottom


@dataclass
class _Pass:
    elems: list[Element]
    i: int
    comp: Component | None


def iterate(
    wto: list[Element],
    f: Callable[[Hashable, dict], D],
    leq: Callable[[D, D], bool],
    widen: Callable[[D, D], D],
    bottom: D,
) -> dict:
    """Run Bourdoncle's recursive iteration strategy over a WTO.

    f(v, x) computes the right side F_v of the equation of v from the current
    values x, a dict in which a vertex with no value yet reads as bottom.
    Each head is widened, each other vertex is assigned. Precondition: every
    F_v is monotone and widen is a widening. Then the run ends, and the
    result has f(v, x) <= x[v] for every vertex of the WTO. Cost: one call of
    f per assignment and per stop test; the number of passes depends on the
    widening. No Python recursion.
    """
    x = _Values(bottom)
    stack = [_Pass(wto, 0, None)]
    while stack:
        p = stack[-1]
        if p.i == len(p.elems):  # the pass over this list is over
            stack.pop()
            if p.comp is None:
                continue
            h = p.comp.head
            t = f(h, x)  # @line L27
            if leq(t, x[h]):  # @line L28
                continue
            x[h] = widen(x[h], t)  # @line L29
            stack.append(_Pass(p.comp.body, 0, p.comp))  # @line L26
            continue
        e = p.elems[p.i]  # @line L21
        p.i += 1
        if not isinstance(e, Component):
            x[e] = f(e, x)  # @line L22
        else:
            h = e.head  # @line L23
            x[h] = widen(x[h], f(h, x))  # @line L24
            stack.append(_Pass(e.body, 0, e))  # @line L25 L26
    return dict(x)


def flatten(wto: list[Element]) -> list[Hashable]:
    """The vertices of a WTO in its total order: each head before its body."""
    out: list[Hashable] = []
    todo: list[Element] = list(reversed(wto))
    while todo:
        e = todo.pop()
        if isinstance(e, Component):
            out.append(e.head)
            todo.extend(reversed(e.body))
        else:
            out.append(e)
    return out


def heads_of(wto: list[Element]) -> dict[Hashable, list[Hashable]]:
    """Map each vertex v to omega(v), the heads of the components that contain v, outermost first."""
    out: dict[Hashable, list[Hashable]] = {}
    todo: list[tuple[Element, tuple]] = [(e, ()) for e in wto]
    while todo:
        e, hs = todo.pop()
        if isinstance(e, Component):
            inner = hs + (e.head,)
            out[e.head] = list(inner)
            todo.extend((b, inner) for b in e.body)
        else:
            out[e] = list(hs)
    return out


def show(wto: list[Element]) -> str:
    """Bourdoncle's notation, for example: a (b c (d e) f) g."""
    tokens: list[str] = []
    todo: list[object] = list(reversed(wto))
    while todo:
        e = todo.pop()
        if e == ")":
            tokens.append(")")
        elif isinstance(e, Component):
            tokens.append("(" + str(e.head))
            todo.append(")")
            todo.extend(reversed(e.body))
        else:
            tokens.append(str(e))
    return " ".join(tokens).replace(" )", ")")
