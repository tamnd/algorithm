# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/young-brothers-wait/. The authors are listed in prov/QFBJRN.jsonl.

"""The Young Brothers Wait rule, on a simulated parallel machine.

A parallel fail-soft negamax alpha-beta search runs on P processors, and each
visit of a node costs one time unit. With the rule (wait_for_eldest true), a
node gives its younger children to other processors only after its eldest
child is searched. Without the rule, all children are given out at once.

A search task is a Python generator that yields requests to the scheduler:

    TICK                 use one time unit (one node visit)
    ("spawn", specs)     make child tasks available to idle processors
    ("wait", handles)    block until one of the handles has finished
    ("cancel", handles)  stop these tasks and all tasks they spawned

The scheduler is deterministic. Ready tasks are kept on a stack, so an idle
processor takes the newest work. A child reads the window of its parent when
it starts. A cutoff cancels the children that are still running.
"""

import random
from typing import Dict, List, Optional, Tuple

INF = 10**9
TICK = ("tick",)
Node = Tuple[int, ...]


class Window:
    """The live state of a node, read by its children when they start."""

    __slots__ = ("m", "alpha", "beta")

    def __init__(self, m: int, alpha: int, beta: int) -> None:
        self.m, self.alpha, self.beta = m, alpha, beta


def alphabeta(g, n: Node, depth: int, alpha: int, beta: int, counter: Optional[List[int]] = None) -> int:
    """Sequential fail-soft alpha-beta, the reference search. Counts every call."""
    if counter is not None:
        counter[0] += 1
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    m = -INF
    for c in kids:
        t = -alphabeta(g, c, depth - 1, -beta, -max(m, alpha), counter)
        if t > m:
            m = t
        if m >= beta:
            return m
    return m


def search(g, n: Node, depth: int, alpha: int, beta: int, wait_for_eldest: bool, min_split: int):
    """Generator for the parallel search of n with the window (alpha, beta).

    Returns a fail-soft value for n. Nodes with depth below min_split are
    searched sequentially inside the task.
    """
    yield TICK
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    m = -INF
    rest = kids
    if wait_for_eldest or depth < min_split:
        m = -(yield from search(g, kids[0], depth - 1, -beta, -alpha, wait_for_eldest, min_split))
        if m >= beta:
            return m
        rest = kids[1:]
    if depth < min_split:
        for c in rest:
            t = -(yield from search(g, c, depth - 1, -beta, -max(m, alpha), wait_for_eldest, min_split))
            m = max(m, t)
            if m >= beta:
                return m
        return m
    w = Window(m, alpha, beta)
    handles = yield ("spawn", [(c, depth - 1, w, wait_for_eldest, min_split) for c in rest])
    pending = set(handles)
    while pending:
        h, val = yield ("wait", pending)
        pending.discard(h)
        w.m = max(w.m, -val)
        if w.m >= beta:
            yield ("cancel", pending)
            return w.m
    return w.m


def _child(g, c: Node, depth: int, w: Window, wait_for_eldest: bool, min_split: int):
    a = max(w.m, w.alpha)  # the bound of the parent when this child starts
    v = yield from search(g, c, depth, -w.beta, -a, wait_for_eldest, min_split)
    return v


class _Task:
    __slots__ = ("gen", "parent", "kids", "inbox", "waiting", "cancelled", "done", "send")

    def __init__(self, gen, parent: Optional[int]) -> None:
        self.gen, self.parent = gen, parent
        self.kids: List[int] = []
        self.inbox: List[Tuple[int, int]] = []
        self.waiting: Optional[set] = None
        self.cancelled = self.done = False
        self.send = None


def simulate(g, root: Node, depth: int, processors: int, wait_for_eldest: bool = True,
             min_split: int = 2) -> Tuple[int, int, int]:
    """Run the parallel search of root on the simulated machine.

    Returns (root value, total node visits of all tasks, time steps). A time
    step counts when at least one processor visits a node in it.
    Precondition: processors >= 1. Cost: one generator step per node visit,
    plus O(1) per scheduler request.
    """
    tasks: Dict[int, _Task] = {0: _Task(search(g, root, depth, -INF, INF, wait_for_eldest, min_split), None)}
    ready: List[int] = [0]
    running: List[Optional[int]] = [None] * processors
    nodes = steps = 0
    result: List[int] = []

    def cancel(tid: int) -> None:
        stack = [tid]
        while stack:
            t = tasks[stack.pop()]
            if not t.done:
                t.cancelled = True
                stack.extend(t.kids)

    def finish(tid: int, value: int) -> None:
        t = tasks[tid]
        t.done = True
        if t.parent is None:
            result.append(value)
            return
        p = tasks[t.parent]
        if p.cancelled:
            return
        if p.waiting is not None and tid in p.waiting:
            p.waiting, p.send = None, (tid, value)
            ready.append(t.parent)
        else:
            p.inbox.append((tid, value))

    def step(p: int) -> bool:
        """Advance processor p up to its next TICK; False if it has no work."""
        while not result:
            tid = running[p]
            if tid is not None and tasks[tid].cancelled:
                running[p] = tid = None
            if tid is None:
                while ready and tasks[ready[-1]].cancelled:
                    ready.pop()
                if not ready:
                    return False
                tid = running[p] = ready.pop()
            t = tasks[tid]
            reply, t.send = t.send, None
            while True:
                try:
                    req = t.gen.send(reply)
                except StopIteration as stop:
                    running[p] = None
                    finish(tid, stop.value)
                    break
                if req is TICK:
                    return True
                kind, arg = req
                if kind == "spawn":
                    reply = []
                    for spec in arg:
                        nid = len(tasks)
                        tasks[nid] = _Task(_child(g, *spec), tid)
                        t.kids.append(nid)
                        reply.append(nid)
                    ready.extend(reversed(reply))  # the eldest of them on top
                elif kind == "cancel":
                    for h in arg:
                        cancel(h)
                    reply = None
                else:  # wait
                    got = next((e for e in t.inbox if e[0] in arg), None)
                    if got is None:
                        t.waiting = set(arg)
                        running[p] = None
                        break
                    t.inbox.remove(got)
                    reply = got
        return False

    while not result:
        busy = 0
        for p in range(processors):
            if step(p):
                busy += 1
        nodes += busy
        steps += busy > 0
    return result[0], nodes, steps


class RandomGame:
    """A lazy random game tree of branching factor b and the given height. A
    node is the tuple of move indices from the root, a move changes the score
    of the mover by an integer in [-swing, swing], and the moves are ordered by
    their static score, best for the mover first."""

    def __init__(self, seed: int, b: int, height: int, swing: int = 9) -> None:
        self.seed, self.b, self.height, self.swing = seed, b, height, swing
        self._static: Dict[Node, int] = {(): 0}
        self._kids: Dict[Node, List[Node]] = {}

    def moves(self, n: Node) -> List[Node]:
        if n in self._kids:
            return self._kids[n]
        out: List[Node] = []
        if len(n) < self.height:
            rng = random.Random(f"{self.seed}/{n}")
            s = self._static[n]
            for i in range(self.b):
                c = n + (i,)
                self._static[c] = -(s + rng.randint(-self.swing, self.swing))
                out.append(c)
            out.sort(key=lambda c: (self._static[c], c))
        self._kids[n] = out
        return out

    def static(self, n: Node) -> int:
        if n not in self._static:
            self.moves(n[:-1])
        return self._static[n]


def negamax(g, n: Node, depth: int) -> int:
    """Plain negamax to a fixed depth, with no pruning."""
    kids = g.moves(n)
    if depth == 0 or not kids:
        return g.static(n)
    return max(-negamax(g, c, depth - 1) for c in kids)


class PerfectOrder:
    """The same tree as g, with the children of each node sorted by their true
    value, best for the mover first. The search depth must equal the height."""

    def __init__(self, g, height: int) -> None:
        self.g, self.height = g, height
        self._kids: Dict[Node, List[Node]] = {}
        self._value: Dict[Node, int] = {}

    def _v(self, n: Node) -> int:
        if n not in self._value:
            self._value[n] = negamax(self.g, n, self.height - len(n))
        return self._value[n]

    def moves(self, n: Node) -> List[Node]:
        if n not in self._kids:
            self._kids[n] = sorted(self.g.moves(n), key=lambda c: (self._v(c), c))
        return self._kids[n]

    def static(self, n: Node) -> int:
        return self.g.static(n)


def critical_nodes(b: int, d: int) -> int:
    """The number of nodes of the minimal tree of Knuth and Moore on a uniform
    tree of branching factor b and depth d, summed over the levels 0 to d."""
    return sum(b ** ((k + 1) // 2) + b ** (k // 2) - 1 for k in range(d + 1))
