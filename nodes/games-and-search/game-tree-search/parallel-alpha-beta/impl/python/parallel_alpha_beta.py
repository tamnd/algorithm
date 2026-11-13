# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-alpha-beta/. The authors are listed in prov/8BYDFQ.jsonl.

"""Parallel alpha-beta with the Young Brothers Wait rule, on a simulated machine.

The machine has P processors, and each visit of a node costs one time unit.
A search task is a Python generator that yields requests to the scheduler:

    TICK                 use one time unit (one node visit)
    ("spawn", specs)     make child tasks available to idle processors
    ("wait", handles)    block until one of the handles has finished
    ("cancel", handles)  stop these tasks and all tasks they spawned

The scheduler is deterministic. Ready tasks are kept on a stack, so an idle
processor takes the newest work, which keeps the search close to depth-first
order. In each time step, every processor runs its task up to its next TICK.

The search is fail-soft negamax alpha-beta. At a node, the eldest child is
searched first and alone; only then are the younger children spawned. A child
reads the window of its parent when it starts, so a later child uses a better
bound. A cutoff cancels the children that are still running. The simulator
does not send better bounds to children that are already running.
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
    """Sequential fail-soft alpha-beta, the reference search."""
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


def ybw(g, n: Node, depth: int, alpha: int, beta: int, wait_for_eldest: bool = True, min_split: int = 2):
    """Generator for the parallel search of n with the window (alpha, beta).

    Returns a fail-soft value for n. With wait_for_eldest false, all children
    are spawned at once, which is a parallel search without the Young Brothers
    Wait rule. Nodes with depth below min_split are searched sequentially
    inside the task.
    """
    yield TICK
    kids = g.moves(n)
    if depth == 0 or not kids:  # @line L1
        return g.static(n)
    m = -INF  # @line L2
    rest = kids
    if wait_for_eldest or depth < min_split:
        first = kids[0]  # @line L3
        m = -(yield from ybw(g, first, depth - 1, -beta, -alpha, wait_for_eldest, min_split))  # @line L4
        if m >= beta:  # @line L5
            return m
        rest = kids[1:]
    if depth < min_split:
        for c in rest:
            t = -(yield from ybw(g, c, depth - 1, -beta, -max(m, alpha), wait_for_eldest, min_split))
            m = max(m, t)
            if m >= beta:
                return m
        return m
    w = Window(m, alpha, beta)
    handles = yield ("spawn", [(c, depth - 1, w, wait_for_eldest, min_split) for c in rest])  # @line L6
    pending = set(handles)
    while pending:
        h, val = yield ("wait", pending)
        pending.discard(h)
        w.m = max(w.m, -val)  # @line L9
        if w.m >= beta:  # @line L10
            yield ("cancel", pending)
            return w.m
    return w.m  # @line L11


def _child(g, c: Node, depth: int, w: Window, wait_for_eldest: bool, min_split: int):
    a = max(w.m, w.alpha)  # @line L7
    v = yield from ybw(g, c, depth, -w.beta, -a, wait_for_eldest, min_split)  # @line L8
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

    Returns (root value, total node visits of all tasks, time steps). The
    root value equals that of sequential alpha-beta. Precondition: processors >= 1.
    Cost: one generator step per node visit, plus O(1) per scheduler request.
    """
    tasks: Dict[int, _Task] = {0: _Task(ybw(g, root, depth, -INF, INF, wait_for_eldest, min_split), None)}
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
        steps += busy > 0  # a step counts if some processor visited a node
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
