# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spin-lock/. The authors are listed in prov/S4E1T8.jsonl.
"""A deterministic interleaving explorer for shared memory algorithms.

A process is a generator. It yields one operation for each shared memory
step and receives the result. explore() visits every interleaving of a small
system with state caching; run() follows one schedule.

Operations: ('read', w), ('write', w, v), ('tas', w), ('faa', w, d),
('swap', w, v), ('cas', w, old, new) (returns True when it wrote),
('mark', label[, data]) (a local step), ('coin', k) (returns 0 .. k - 1),
('atomic', f, guard): f(mem, pid) returns a list of alternatives
(result, updates), and guard(mem, pid) says when the step is enabled.

The marks 'try', 'doorway', 'cs', 'exit' and 'rem' give the section of the
process; 'doorway', 'cs' and 'rem' are part of the step before them. The
marks 'inv' and 'res' record operations for a linearizability check.

Remote memory references: in the CC model a read is remote when the process
has no valid copy of the cache line (map `lines`, default one word per
line), and each write or read-modify-write is remote and removes the other
copies. In the DSM model an access is remote when the word does not live
with the process (map `home`).

State caching reads the local variables and resume points of the generator
frames, so processes keep their state in hashable locals. Locals whose name
starts with an underscore are ignored.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Callable, Iterable

EAGER = frozenset({"doorway", "cs", "rem"})


def local_key(g) -> tuple:
    parts = []
    while g is not None:
        f = g.gi_frame
        if f is None:
            parts.append(None)
            break
        loc = tuple(sorted((k, v) for k, v in f.f_locals.items() if not k.startswith("_")))
        parts.append((g.gi_code.co_name, f.f_lasti, loc))
        g = g.gi_yieldfrom
    return tuple(parts)


class Config:
    def __init__(self, procs, init, home=None, lines=None, cs_limit=1):
        self.procs, self.init, self.cs_limit = procs, init, cs_limit
        self.home, self.lines = dict(home or {}), dict(lines or {})


class Machine:
    """One system state: memory, processes, sections, caches and counters."""

    LISTS = ("gens", "pending", "section", "door", "opened", "seq", "entries", "log", "violations", "lk")

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.words = tuple(cfg.init)
        self.mem = dict(cfg.init)
        self.n = n = len(cfg.procs)
        self.gens = [make(p) for p, make in enumerate(cfg.procs)]
        self.pending: list = [None] * n
        self.section = ["rem"] * n
        self.door = [False] * n
        self.cache = [set() for _ in range(n)]
        self.rmr = {"cc": [0] * n, "dsm": [0] * n}
        self.passage = {"cc": [0] * n, "dsm": [0] * n}
        self.passages: list = [[] for _ in range(n)]
        self.ahead = frozenset()
        self.opened: list = [None] * n
        self.history = frozenset()
        self.seq = [0] * n
        self.entries: list = []
        self.log: list = []
        self.violations: list = []
        self.steps = 0
        self.results: list = [[] for _ in range(n)]
        self.owned = [True] * n
        self.lk: list = [None] * n
        for p in range(n):
            self._resume(p, None, first=True)

    def clone(self) -> "Machine":
        """A copy that shares the generators until one copy moves a process."""
        c = object.__new__(Machine)
        c.__dict__.update(self.__dict__)
        c.mem = dict(self.mem)
        for name in self.LISTS:
            setattr(c, name, list(getattr(self, name)))
        c.cache = [set(x) for x in self.cache]
        c.rmr = {k: list(v) for k, v in self.rmr.items()}
        c.passage = {k: list(v) for k, v in self.passage.items()}
        c.passages = [list(x) for x in self.passages]
        c.results = [list(x) for x in self.results]
        c.owned = [False] * self.n
        self.owned = [False] * self.n
        return c

    def _own(self, p):
        g = self.cfg.procs[p](p)
        next(g)
        for r in self.results[p]:
            g.send(r)
        self.gens[p] = g
        self.owned[p] = True

    def _resume(self, p, value, first=False):
        try:
            if first:
                self.pending[p] = next(self.gens[p])
            else:
                self.results[p].append(value)
                self.pending[p] = self.gens[p].send(value)
            self.lk[p] = local_key(self.gens[p])
        except StopIteration:
            self.pending[p] = None
            self.lk[p] = None

    def done(self, p: int) -> bool:
        return self.pending[p] is None

    def choices(self, p: int) -> int:
        """The number of alternatives of the next step of p (0 when p cannot move)."""
        op = self.pending[p]
        if op is None:
            return 0
        if op[0] == "coin":
            return op[1]
        if op[0] == "atomic":
            if op[2] is not None and not op[2](self.mem, p):
                return 0
            return len(op[1](self.mem, p))
        return 1

    def _alternative(self, p, op, alt):
        kind = op[0]
        if kind == "mark":
            return None, {}, (), ()
        if kind == "coin":
            return alt, {}, (), ()
        if kind == "atomic":
            result, upd = op[1](self.mem, p)[alt]
            return result, upd, (), tuple(upd)
        w = op[1]
        old = self.mem[w]
        if kind == "read":
            return old, {}, (w,), ()
        if kind == "write":
            return None, {w: op[2]}, (), (w,)
        if kind == "tas":
            return old, {w: True}, (), (w,)
        if kind == "faa":
            return old, {w: old + op[2]}, (), (w,)
        if kind == "swap":
            return old, {w: op[2]}, (), (w,)
        if kind == "cas":
            ok = old == op[2]
            return ok, ({w: op[3]} if ok else {}), (), (w,)
        raise ValueError(f"unknown operation {op!r}")

    def step(self, p: int, alt: int = 0) -> tuple:
        """Run one step of p. Return (CC remote count, DSM remote count, entered cs)."""
        op = self.pending[p]
        result, upd, reads, writes = self._alternative(p, op, alt)
        if not self.owned[p]:
            self._own(p)
        lines, home = self.cfg.lines, self.cfg.home
        cc = dsm = 0
        for w in reads:
            ln = lines.get(w, w)
            if ln not in self.cache[p]:
                cc += 1
                self.cache[p].add(ln)
            dsm += home.get(w) != p
        for w in writes:
            ln = lines.get(w, w)
            cc += 1
            for q in range(self.n):
                if q != p:
                    self.cache[q].discard(ln)
            self.cache[p].add(ln)
            dsm += home.get(w) != p
        for w, v in upd.items():
            if w not in self.mem:
                raise KeyError(f"word {w!r} is not declared")
            self.mem[w] = v
        for model, x in (("cc", cc), ("dsm", dsm)):
            self.rmr[model][p] += x
            self.passage[model][p] += x
        entered = self._mark(p, op) if op[0] == "mark" else False
        self.steps += 1
        self._resume(p, result)
        while self.pending[p] is not None and self.pending[p][0] == "mark" and self.pending[p][1] in EAGER:
            entered = self._mark(p, self.pending[p]) or entered
            self._resume(p, None)
        return cc, dsm, entered

    def _mark(self, p, op) -> bool:
        label = op[1]
        self.log.append((p, label) if len(op) < 3 else (p, label, op[2]))
        if label == "try":
            self.section[p] = "try"
            self.door[p] = False
            self.passage["cc"][p] = self.passage["dsm"][p] = 0
        elif label == "doorway":
            # each q that is not in its trying section now must not enter before p
            self.door[p] = True
            self.ahead = self.ahead | {(p, q) for q in range(self.n) if q != p and self.section[q] != "try"}
        elif label == "cs":
            self.section[p] = "cs"
            if sum(s == "cs" for s in self.section) > self.cfg.cs_limit:
                self.violations.append(("mutual exclusion", self.steps))
            if any(b == p and self.section[a] == "try" for a, b in self.ahead):
                self.violations.append(("fifo", self.steps))
            self.ahead = frozenset(x for x in self.ahead if p not in x)
            self.entries.append(p)
            return True
        elif label == "exit":
            self.section[p] = "exit"
        elif label == "rem":
            self.section[p] = "rem"
            self.passages[p].append((self.passage["cc"][p], self.passage["dsm"][p]))
        elif label == "inv":
            self.opened[p] = (op[2], frozenset(self.history))
        elif label == "res":
            data, before = self.opened[p]
            self.history = self.history | {(p, self.seq[p], data, op[2], before)}
            self.seq[p] += 1
            self.opened[p] = None
        return False

    def key(self, with_cache: bool) -> tuple:
        k = (tuple(self.mem[w] for w in self.words), tuple(self.lk), tuple(self.section), tuple(self.door), self.ahead, self.history, tuple(self.opened))
        if with_cache:
            k = k + (tuple(frozenset(c) for c in self.cache),)
        return k


def replay(cfg: Config, schedule: Iterable) -> Machine:
    m = Machine(cfg)
    for p, a in schedule:
        m.step(p, a)
    return m


class Graph:
    """The reachable state graph. Each edge is (pid, alt, dst, cc, dsm, entered)."""

    def __init__(self):
        self.parent: list = []
        self.section: list = []
        self.done: list = []
        self.enabled: list = []
        self.edges: list = []
        self.violation = None
        self.stuck: list = []
        self.histories: list = []

    def size(self) -> int:
        return len(self.parent)

    def schedule(self, s: int) -> list:
        out = []
        while self.parent[s] is not None:
            s, step = self.parent[s]
            out.append(step)
        return out[::-1]


def explore(procs, init, home=None, lines=None, cache=False, cs_limit=1, max_states=300000, stop=False) -> Graph:
    """Visit every interleaving by breadth first search.

    cache=True puts the CC caches into the state, so that the CC counts on the
    edges are exact. g.violation keeps the first violation of mutual exclusion
    or FIFO order with a schedule; stop=True ends the search there. g.stuck
    lists the states where no process can move and some process is not done.
    """
    cfg = Config(procs, init, home, lines, cs_limit)
    g = Graph()
    ids: dict = {}
    queue: deque = deque()

    def add(m, parent):
        k = m.key(cache)
        if k in ids:
            return ids[k]
        s = g.size()
        if s >= max_states:
            raise RuntimeError("too many states")
        ids[k] = s
        g.parent.append(parent)
        g.section.append(tuple(m.section))
        g.done.append(tuple(m.done(p) for p in range(m.n)))
        g.enabled.append(tuple(m.choices(p) > 0 for p in range(m.n)))
        g.edges.append([])
        g.histories.append(m.history if all(g.done[s]) else None)
        if not any(g.enabled[s]) and not all(g.done[s]):
            g.stuck.append(s)
        m.entries, m.log = [], []
        queue.append((s, m))
        return s

    add(Machine(cfg), None)
    while queue:
        s, base = queue.popleft()
        steps = [(p, a) for p in range(base.n) for a in range(base.choices(p))]
        for i, (p, a) in enumerate(steps):
            m = base if i == len(steps) - 1 else base.clone()
            cc, dsm, entered = m.step(p, a)
            if m.violations and g.violation is None:
                g.violation = (m.violations[0][0], g.schedule(s) + [(p, a)])
                if stop:
                    return g
            t = add(m, (s, (p, a)))
            g.edges[s].append((p, a, t, cc, dsm, entered))
    return g


def _sccs(nodes, succ) -> list:
    """Strongly connected components by iterative Tarjan."""
    index: dict = {}
    low: dict = {}
    on: set = set()
    stack: list = []
    out: list = []
    counter = 0
    for root in nodes:
        if root in index:
            continue
        work = [(root, iter(succ(root)))]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter
                    counter += 1
                    stack.append(w)
                    on.add(w)
                    work.append((w, iter(succ(w))))
                    advanced = True
                    break
                if w in on:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                low[work[-1][0]] = min(low[work[-1][0]], low[v])
            if low[v] == index[v]:
                comp = set()
                while True:
                    w = stack.pop()
                    on.discard(w)
                    comp.add(w)
                    if w == v:
                        break
                out.append(comp)
    return out


def fair_cycles(g: Graph, node_ok: Callable, edge_ok: Callable = lambda s, e: True) -> list:
    """Components in which a weakly fair run can stay forever.

    Weakly fair: a process that is not idle (in its remainder section, or
    done) and stays enabled takes infinitely many steps.
    """
    nodes = [s for s in range(g.size()) if node_ok(s)]
    keep = set(nodes)

    def succ(s):
        return [e[2] for e in g.edges[s] if e[2] in keep and edge_ok(s, e)]

    found = []
    for comp in _sccs(nodes, succ):
        inner = [(s, e) for s in comp for e in g.edges[s] if e[2] in comp and edge_ok(s, e)]
        if not inner:
            continue
        movers = {e[0] for _, e in inner}
        s0 = next(iter(comp))
        fair = all(q in movers or g.done[s0][q] or g.section[s0][q] == "rem" or any(not g.enabled[s][q] for s in comp) for q in range(len(g.section[s0])))
        if fair:
            found.append((comp, inner))
    return found


def lasso(g: Graph, comp: set, inner: list, want: list) -> tuple:
    """A schedule to the component and a cycle in it that takes an edge chosen by each test in want."""
    start = min(comp, key=lambda s: len(g.schedule(s)))
    adj: dict = {}
    for s, e in inner:
        adj.setdefault(s, []).append(e)

    def path(a, b):
        prev = {a: None}
        dq = deque([a])
        while dq:
            u = dq.popleft()
            if u == b:
                break
            for e in adj.get(u, []):
                if e[2] not in prev:
                    prev[e[2]] = (u, e)
                    dq.append(e[2])
        out = []
        while prev[b] is not None:
            u, e = prev[b]
            out.append((e[0], e[1]))
            b = u
        return out[::-1]

    cycle: list = []
    cur = start
    for pick in want:
        s, e = next((s, e) for s, e in inner if pick(s, e))
        cycle += path(cur, s) + [(e[0], e[1])]
        cur = e[2]
    cycle += path(cur, start)
    return g.schedule(start), cycle


def starvation(g: Graph, p: int) -> list:
    """Fair components where p stays in its trying section while some process enters."""
    return [(c, i) for c, i in fair_cycles(g, lambda s: g.section[s][p] == "try") if any(e[5] for _, e in i)]


def no_progress(g: Graph) -> list:
    """Fair components where some process tries forever and no process enters."""
    return fair_cycles(g, lambda s: "try" in g.section[s], lambda s, e: not e[5])


def max_passage_rmr(g: Graph, p: int, model: str) -> float:
    """The most remote references of p in one passage (from 'try' to 'rem'), or inf.

    For the CC model the graph must come from explore(..., cache=True).
    """
    col = 3 if model == "cc" else 4
    nodes = [s for s in range(g.size()) if g.section[s][p] != "rem" and not g.done[s][p]]
    keep = set(nodes)
    comps = _sccs(nodes, lambda s: [e[2] for e in g.edges[s] if e[2] in keep])
    where = {s: i for i, c in enumerate(comps) for s in c}
    for c in comps:
        if any(e[2] in c and e[0] == p and e[col] > 0 for s in c for e in g.edges[s]):
            return float("inf")
    best = [0] * len(comps)
    for i, c in enumerate(comps):
        for s in c:
            for e in g.edges[s]:
                w = e[col] if e[0] == p else 0
                if e[2] in keep and where[e[2]] != i:
                    best[i] = max(best[i], w + best[where[e[2]]])
                elif e[2] not in keep:
                    best[i] = max(best[i], w)
    starts = {e[2] for s in range(g.size()) if s not in keep for e in g.edges[s] if e[2] in keep}
    return max((best[where[s]] for s in starts), default=0)


def at_random(t, enabled, rng):
    return rng.choice(enabled)


def lockstep(n: int) -> Callable:
    """Move process t mod n at time t, or the first enabled one when that one cannot move."""
    def policy(t, enabled, rng):
        p = t % n
        return p if p in enabled else enabled[0]
    return policy


def run(procs, init, home=None, lines=None, policy=at_random, seed=0, max_steps=20000, cs_limit=1) -> Machine:
    """Run one schedule. policy(t, enabled, rng) picks the next process, or None to stop.

    Coins and other choices come from a second generator seeded from seed.
    """
    m = Machine(Config(procs, init, home, lines, cs_limit))
    rng = random.Random(seed)
    coins = random.Random(seed + 7919)
    for t in range(max_steps):
        enabled = [p for p in range(m.n) if m.choices(p) > 0]
        if not enabled:
            break
        p = policy(t, enabled, rng)
        if p is None:
            break
        k = m.choices(p)
        m.step(p, coins.randrange(k) if k > 1 else 0)
    return m


def linearizable(history: Iterable, spec: Callable, initial) -> bool:
    """Brute force: some order that respects real time is legal for spec.

    history holds (pid, seq, (name, arg), result, before); before is the set
    of operations that responded before this one was invoked.
    spec(state, name, arg) returns (new state, result).
    """
    ops = list(history)
    ident = [(o[0], o[1]) for o in ops]
    preds = [{(b[0], b[1]) for b in o[4]} for o in ops]
    seen: set = set()
    stack = [(frozenset(), initial)]
    while stack:
        used, state = stack.pop()
        if len(used) == len(ops):
            return True
        if (used, state) in seen:
            continue
        seen.add((used, state))
        names = {ident[i] for i in used}
        for i in range(len(ops)):
            if i in used or not preds[i] <= names:
                continue
            new, res = spec(state, *ops[i][2])
            if res == ops[i][3]:
                stack.append((used | {i}, new))
    return False
