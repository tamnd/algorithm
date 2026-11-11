# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dekker-algorithm/. The authors are listed in prov/D4K719.jsonl.
"""A deterministic interleaving explorer for shared-memory locks.

A process is a generator. It yields one operation at each shared step, in
the form ``v = yield op``, and it gets the result of a read or of an atomic
read-modify-write back from the yield. Keep loop state in named local
variables: the explorer identifies the local state of a process by the code
position and the local variables of its frames.

The explorer runs one operation of one process at a time, so a run is a
sequentially consistent interleaving, unless the mode is "tso" (each process
has a FIFO store buffer) or "safe" (a read that overlaps a write of another
process may return any value of the domain of the register).
``Explorer.explore`` builds the graph of all reachable states for small
cases, and ``walk`` runs one seeded random schedule for larger cases.
"""
from __future__ import annotations

import random
from collections import deque
from typing import Any, Callable, Iterator

REM: tuple = ("rem",)    # in the remainder section; a step starts the entry
CS: tuple = ("cs",)      # in the critical section; a step starts the exit
DOOR: tuple = ("door",)  # marks the end of the doorway; takes no step
FENCE: tuple = ("fence",)
START, PASSDOOR, ENTER = 1, 2, 4
RMW = ("cas", "xchg", "faa", "dec", "tas")


def R(a: Any) -> tuple:
    return ("r", a)


def W(a: Any, v: Any) -> tuple:
    return ("w", a, v)


def client(lock: Callable, unlock: Callable, i: int, rounds: int) -> Iterator:
    """Process i: remainder, entry, critical section, exit; rounds times, or forever if rounds < 0."""
    k = rounds
    while k != 0:
        v = yield REM
        yield from lock(i)
        v = yield CS
        yield from unlock(i)
        if k > 0:
            k -= 1


def procs(lock: Callable, unlock: Callable, n: int, rounds: int) -> list:
    return [lambda i=i: client(lock, unlock, i, rounds) for i in range(n)]


def _freeze(v: Any) -> Any:
    if v is None or isinstance(v, (bool, int, str, float)):
        return v
    if isinstance(v, (tuple, list)):
        return tuple(_freeze(x) for x in v)
    return "-"


def _key(g: Any) -> tuple:
    out = []
    while g is not None and g.gi_frame is not None:
        f = g.gi_frame
        loc = sorted((k, _freeze(x)) for k, x in f.f_locals.items() if not callable(x))
        out.append((f.f_lasti, tuple(loc)))
        g = g.gi_yieldfrom
    return tuple(out)


class _Proc:
    """The memoized step function of one process: (local state id, value) to (local state id, op, door)."""

    def __init__(self, make: Callable) -> None:
        self.make, self.rep, self.memo, self.ids = make, {}, {}, {}

    def _run(self, g: Any, op: Any, hist: list) -> tuple:
        door = False
        try:
            while op == DOOR:
                door = True
                hist.append(None)
                op = g.send(None)
        except StopIteration:
            op = None
        k = self.ids.setdefault(_key(g) if op is not None else (), len(self.ids))
        self.rep.setdefault(k, tuple(hist))
        return k, op, door

    def start(self) -> tuple:
        g = self.make()
        try:
            op = next(g)
        except StopIteration:
            op = None
        return self._run(g, op, [])

    def step(self, k: int, v: Any) -> tuple:
        if (k, v) not in self.memo:
            g, hist = self.make(), list(self.rep[k])
            next(g)
            for x in hist:
                g.send(x)
            hist.append(v)
            try:
                op = g.send(v)
            except StopIteration:
                op = None
            self.memo[(k, v)] = self._run(g, op, hist)
        return self.memo[(k, v)]


def _set(t: tuple, j: int, x: Any) -> tuple:
    return t[:j] + (x,) + t[j + 1:]


class Explorer:
    """All interleavings of the processes made by ``makes`` on the memory ``mem``.

    mode is "sc", "tso" or "safe"; domain maps an address to the values that
    a safe read may return; rmr is None, "cc" or "dsm"; home maps an address
    to the process whose memory module holds it (DSM).
    A state is (memory values, one record per process). A record is (local
    state id, pending op, section R/T/C/X/F, doorway passed, store buffer,
    write in progress, futex address it sleeps on, cached addresses).
    """

    def __init__(self, makes: list, mem: dict, mode: str = "sc", domain: dict | None = None,
                 rmr: str | None = None, home: dict | None = None) -> None:
        self.ps = [_Proc(m) for m in makes]
        self.addrs = list(mem)
        self.at = {a: j for j, a in enumerate(self.addrs)}
        self.mode, self.domain, self.rmr, self.home = mode, domain or {}, rmr, home or {}
        recs = []
        for p in self.ps:
            k, op, _ = p.start()
            sect = "R" if op == REM else ("F" if op is None else "T")
            recs.append((k, op, sect, False, (), None, None, frozenset()))
        self.s0 = (tuple(mem[a] for a in self.addrs), tuple(recs))
        self.states: list = []
        self.edges: list = []
        self.bad: list | None = None

    def value(self, s: tuple, a: Any) -> Any:
        return s[0][self.at[a]]

    def inside(self, s: tuple) -> list:
        return [p for p, r in enumerate(s[1]) if r[2] == "C"]

    def _cost(self, ps: list, p: int, a: Any, write: bool) -> int:
        if self.rmr == "dsm":
            return int(self.home.get(a) != p)
        if self.rmr != "cc":
            return 0
        if write:
            for q, r in enumerate(ps):
                if q != p and a in r[7]:
                    ps[q] = _set(r, 7, r[7] - {a})
        c = 0 if (a in ps[p][7] and not write) else 1
        ps[p] = _set(ps[p], 7, ps[p][7] | {a})
        return c

    def _adv(self, ps: list, p: int, v: Any) -> int:
        r, fl = list(ps[p]), 0
        if r[1] == REM:
            r[2], r[3], fl = "T", False, START
        elif r[1] == CS:
            r[2] = "X"
        r[0], r[1], door = self.ps[p].step(r[0], v)
        if door:
            r[3], fl = True, fl | PASSDOOR
        if r[1] == CS:
            r[2], fl = "C", fl | ENTER
        elif r[1] == REM:
            r[2], r[3] = "R", False
        elif r[1] is None:
            r[2] = "F"
        ps[p] = tuple(r)
        return fl

    def succ(self, s: tuple) -> list:
        """All moves from s, as (process, label, next state, flags, RMR cost)."""
        out = []
        n = len(s[1])
        for p in range(n):
            rec = s[1][p]
            if rec[4]:
                (a, v), ps = rec[4][0], list(s[1])
                ps[p] = _set(rec, 4, rec[4][1:])
                out.append((p, ("flush", a, v), (_set(s[0], self.at[a], v), tuple(ps)), 0, 0))
            op = rec[1]
            if op is None or rec[6] is not None or (rec[4] and (op[0] in RMW or op == FENCE)):
                continue
            vals = [None]
            if op[0] == "r":
                a = op[1]
                if self.mode == "safe" and any(r[5] and r[5][0] == a for r in s[1]):
                    vals = list(self.domain[a])
                else:
                    vals = [self.value(s, a)]
                    for b, x in rec[4]:
                        if b == a:
                            vals = [x]
            for v in vals:
                out.extend(self._one(s, p, op, v))
        return out

    def _one(self, s: tuple, p: int, op: tuple, v: Any) -> list:
        mem, ps = s[0], list(s[1])
        kind, label, c = op[0], op, 0
        if kind == "r":
            c, label = self._cost(ps, p, op[1], False), ("r", op[1], v)
        elif kind == "w":
            a, x = op[1], op[2]
            if self.mode == "tso":
                ps[p] = _set(ps[p], 4, ps[p][4] + ((a, x),))
            elif self.mode == "safe" and ps[p][5] is None:
                ps[p] = _set(ps[p], 5, (a, x))
                return [(p, ("begin", a, x), (mem, tuple(ps)), 0, 0)]
            else:
                mem, ps[p] = _set(mem, self.at[a], x), _set(ps[p], 5, None)
                c = self._cost(ps, p, a, True)
        elif kind in RMW:
            j = self.at[op[1]]
            v = mem[j]
            if kind == "cas":
                new = op[3] if v == op[2] else v
            elif kind in ("xchg", "faa"):
                new = op[2] if kind == "xchg" else v + op[2]
            else:
                new = 1 if kind == "tas" else v - 1
            mem, c, label = _set(mem, j, new), self._cost(ps, p, op[1], True), op + (v,)
        elif kind == "futex_wait":
            if mem[self.at[op[1]]] == op[2]:
                ps[p] = _set(ps[p], 6, op[1])
                return [(p, op, (mem, tuple(ps)), 0, 0)]
            v = -1
        elif kind == "futex_wake":
            sleepers = [q for q in range(len(ps)) if ps[q][6] == op[1]]
            groups = [[q] for q in sleepers] if op[2] == 1 else [sleepers[:op[2]]]
            res = []
            for g in groups:
                p2 = list(ps)
                for w in g:
                    p2[w] = _set(p2[w], 6, None)
                    self._adv(p2, w, 0)
                fl = self._adv(p2, p, len(g))
                res.append((p, op + (tuple(g),), (mem, tuple(p2)), fl, 0))
            if res and groups[0]:
                return res
            v = 0
        fl = self._adv(ps, p, v)
        return [(p, label, (mem, tuple(ps)), fl, c)]

    def explore(self, limit: int = 300000) -> "Explorer":
        """Breadth-first search of all reachable states.

        It stops at the first state with two processes in the critical
        section and keeps the schedule that leads there in ``bad``.
        Cost: O(S * n) moves for S reachable states; raises if S > limit.
        """
        ids, parent = {self.s0: 0}, [None]
        self.states, self.edges = [self.s0], [[]]
        queue = deque([0])
        while queue:
            u = queue.popleft()
            for p, label, t, fl, c in self.succ(self.states[u]):
                w = ids.get(t)
                if w is None:
                    w = ids[t] = len(self.states)
                    self.states.append(t)
                    self.edges.append([])
                    parent.append((u, p, label))
                    if len(self.states) > limit:
                        raise RuntimeError("too many states")
                    if len(self.inside(t)) > 1:
                        self.bad = []
                        while parent[w] is not None:
                            u, q, label = parent[w]
                            self.bad.append((q, label))
                            w = u
                        self.bad.reverse()
                        return self
                    queue.append(w)
                self.edges[u].append((p, w, fl, c))
        return self

    def move(self, s: tuple, p: Any) -> tuple:
        """The state after the first move of process p (or of ("flush", p)) from s."""
        flush = isinstance(p, tuple)
        q = p[1] if flush else p
        for mover, label, t, _, _ in self.succ(s):
            if mover == q and (label[0] == "flush") == flush:
                return t
        raise ValueError(f"process {p} has no move")

    def run(self, order: list, s: tuple | None = None) -> tuple:
        for p in order:
            s = self.move(self.s0 if s is None else s, p)
        return self.s0 if s is None else s

    def sect(self, u: int, p: int) -> str:
        return self.states[u][1][p][2]

    def _sccs(self, ok: Callable, eok: Callable) -> list:
        """Strongly connected components of the subgraph, sinks first (iterative Tarjan)."""
        index: dict = {}
        low: dict = {}
        on: set = set()
        stack: list = []
        out: list = []
        for root in range(len(self.states)):
            if root in index or not ok(root):
                continue
            index[root] = low[root] = len(index)
            stack.append(root)
            on.add(root)
            work = [(root, 0)]
            while work:
                v, i = work[-1]
                es, down = self.edges[v], False
                while i < len(es):
                    e = es[i]
                    i += 1
                    w = e[1]
                    if not ok(w) or not eok(e):
                        continue
                    if w not in index:
                        work[-1] = (v, i)
                        index[w] = low[w] = len(index)
                        stack.append(w)
                        on.add(w)
                        work.append((w, 0))
                        down = True
                        break
                    if w in on:
                        low[v] = min(low[v], index[w])
                if down:
                    continue
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = stack.pop()
                        on.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    out.append(comp)
        return out

    def _fair_cycle(self, ok: Callable, eok: Callable) -> list | None:
        """States of a fair infinite run, or a dead end, inside the subgraph.

        A run is fair if every process that takes no step in it stays in
        the remainder, is finished, or sleeps on a futex.
        """
        for u in range(len(self.states)):
            if ok(u) and not self.edges[u]:
                return [u]
        for comp in self._sccs(ok, eok):
            cs, movers = set(comp), set()
            for v in comp:
                for e in self.edges[v]:
                    if e[1] in cs and eok(e):
                        movers.add(e[0])
            recs = self.states[comp[0]][1]
            if movers and all(q in movers or r[2] in "RF" or r[6] is not None for q, r in enumerate(recs)):
                return comp
        return None

    def starvation(self, p: int) -> list | None:
        """States of a fair run in which p stays in its entry section forever, or None."""
        return self._fair_cycle(lambda u: self.sect(u, p) == "T", lambda e: True)

    def deadlock(self) -> list | None:
        """States of a fair run in which some process tries or exits forever and no process enters."""
        def ok(u: int) -> bool:
            ss = [r[2] for r in self.states[u][1]]
            return "C" not in ss and ("T" in ss or "X" in ss)
        return self._fair_cycle(ok, lambda e: not e[2] & ENTER)

    def bypass(self, p: int, frm: int = PASSDOOR, cap: int = 64) -> int:
        """The most entries of other processes into the critical section while p waits.

        The count starts at p's move with flag frm (START or PASSDOOR) and
        stops when p enters; cap stands for "unbounded".
        """
        best, seen, todo = 0, {(0, -1)}, [(0, -1)]
        while todo:
            u, c = todo.pop()
            for q, w, fl, _ in self.edges[u]:
                d = c
                if q == p:
                    if fl & frm:
                        d = 0
                    if fl & ENTER:
                        best, d = max(best, d), -1
                elif fl & ENTER and d >= 0:
                    d = min(d + 1, cap)
                if (w, d) not in seen:
                    seen.add((w, d))
                    todo.append((w, d))
        return best

    def fcfs(self, p: int) -> bool:
        """True if no process that starts its entry after p's doorway enters before p."""
        seen, todo = {(0, None)}, [(0, None)]
        while todo:
            u, late = todo.pop()
            for q, w, fl, _ in self.edges[u]:
                l2 = late
                if q == p:
                    l2 = frozenset() if fl & PASSDOOR else l2
                    l2 = None if fl & ENTER else l2
                elif l2 is not None:
                    if fl & ENTER and q in l2:
                        return False
                    l2 = l2 | {q} if fl & START else l2
                if (w, l2) not in seen:
                    seen.add((w, l2))
                    todo.append((w, l2))
        return True

    def max_cost(self, p: int) -> float:
        """The most RMRs of p in one entry section; inf if a cycle can repeat RMRs."""
        ok = lambda u: self.sect(u, p) == "T"
        val: dict = {}
        best = 0.0
        for comp in self._sccs(ok, lambda e: True):
            cs, m = set(comp), 0.0
            for v in comp:
                for q, w, fl, c in self.edges[v]:
                    c = c if q == p else 0
                    if w in cs:
                        if c:
                            return float("inf")
                    else:
                        m = max(m, c + val.get(w, 0))
            for v in comp:
                val[v] = m
            best = max(best, m)
        return best


def walk(makes: list, mem: dict, seed: int, steps: int, pick: Callable | None = None, **kw: Any) -> dict:
    """Run one seeded random schedule of at most ``steps`` moves.

    pick(rng, moves) returns the index of the next move; the default is
    uniform. The result has the entries per process, the most processes
    seen in the critical section at once, the most RMRs of one entry
    section, and the most entries of others between a doorway and the
    entry of the same process.
    """
    ex, rng = Explorer(makes, mem, **kw), random.Random(seed)
    s, n = ex.s0, len(makes)
    entries, cost, wait, most, worst, byp = [0] * n, [0] * n, [-1] * n, 0, 0, 0
    for _ in range(steps):
        moves = ex.succ(s)
        if not moves:
            break
        p, _, s, fl, c = moves[pick(rng, moves) if pick else rng.randrange(len(moves))]
        cost[p] = c if fl & START else cost[p] + c
        wait[p] = 0 if fl & PASSDOOR else wait[p]
        if fl & ENTER:
            entries[p] += 1
            worst, byp, wait[p] = max(worst, cost[p]), max(byp, wait[p]), -1
            wait = [w + 1 if w >= 0 and q != p else w for q, w in enumerate(wait)]
        most = max(most, len(ex.inside(s)))
    return {"entries": entries, "most_in_cs": most, "max_rmr": worst, "max_bypass": byp, "state": s}
