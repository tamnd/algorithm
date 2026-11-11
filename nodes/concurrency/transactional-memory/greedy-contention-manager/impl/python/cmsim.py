# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-contention-manager/. The authors are listed in prov/Z33CZD.jsonl.
"""A small model of conflict resolution in an obstruction-free STM such as DSTM.

Each process runs one transaction, given as the list of objects it opens for
writing, in order. An object is owned by at most one active transaction. A
step of process i is one of these atomic actions:

- restart: i was aborted by another transaction; it starts again at its
  first object (the manager decides what it keeps, for example a timestamp);
- backoff: i spends one step of a backoff interval;
- open: the next object is free (or i owns it), so i takes it;
- abort: the next object is owned by active transaction j, and the manager
  says "abort the enemy": i changes the status of j from active to aborted
  (one compare-and-swap), which frees all objects of j, and takes the object;
- wait: the manager says "wait": i sets its waiting flag and asks again at a
  later step (after the backoff that the manager sets, if any);
- commit: i has opened all its objects; it changes its status from active to
  committed and frees its objects.

A contention manager is an object with the methods begin, opened, resolve,
restarted and committed (see Aggressive). Time is counted in steps, so a
randomized backoff of the real managers becomes a fixed number of steps, and
the scheduler, not a clock, decides how long a process waits.

The state is finite: the priorities of Karma and Polka are stored relative to
the smallest priority of a transaction that is not done, since the managers
compare only differences.

Precondition: programs are short lists of object indices; the managers keep
their numbers small. Cost: one step is O(n + m) work for n transactions and
m objects; `explore` visits each reachable state once.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any, NamedTuple

ACTIVE, ABORTED, DONE = 0, 1, 2


class Tx(NamedTuple):
    """The public state of one transaction."""

    status: int = ACTIVE
    pos: int = 0          # index of the next object to open
    waiting: bool = False
    ts: int = 0           # timestamp (smaller is older)
    prio: int = 0         # priority of Karma and Polka (relative)
    tries: int = 0        # conflicts met on the current object
    left: int = 0         # backoff steps left


Owners = tuple[int, ...]
State = tuple[Owners, tuple[Tx, ...]]


class Aggressive:
    """Always abort the enemy. It is obstruction-free but can livelock."""

    name = "aggressive"

    def begin(self, ts: int) -> Tx:
        return Tx(ts=ts)

    def opened(self, me: Tx) -> Tx:
        return me._replace(tries=0)

    def resolve(self, me: Tx, enemy: Tx) -> tuple[bool, Tx]:
        return True, me

    def restarted(self, me: Tx) -> Tx:
        return me

    def committed(self, me: Tx) -> Tx:
        return me


def initial(progs: list[list[int]], cm: Any, order: list[int] | None = None) -> State:
    """All transactions start at once; order[i] is the timestamp of i."""
    nobj = 1 + max((o for p in progs for o in p), default=0)
    ts = order if order is not None else list(range(len(progs)))
    return (-1,) * nobj, tuple(cm.begin(ts[i]) for i in range(len(progs)))


def _normalize(txs: list[Tx]) -> tuple[Tx, ...]:
    live = [t.prio for t in txs if t.status != DONE]
    low = min(live) if live else 0
    return tuple(t._replace(prio=t.prio - low) if t.status != DONE else t._replace(prio=0)
                 for t in txs)


def enabled(state: State) -> list[int]:
    return [i for i, t in enumerate(state[1]) if t.status != DONE]


def step(progs: list[list[int]], cm: Any, state: State, i: int) -> tuple[State, str]:
    """Run one step of process i; return the new state and the kind of step."""
    owners = list(state[0])
    txs = list(state[1])
    t = txs[i]
    prog = progs[i]
    if t.status == DONE:
        raise ValueError("process %d has no step left" % i)
    if t.status == ABORTED:
        t = cm.restarted(t._replace(status=ACTIVE, pos=0, waiting=False, tries=0, left=0))
        event = "restart"
    elif t.left > 0:
        t = t._replace(left=t.left - 1)
        event = "backoff"
    elif t.pos == len(prog):
        owners = [-1 if o == i else o for o in owners]
        t = cm.committed(t._replace(status=DONE, waiting=False))
        event = "commit"
    else:
        obj = prog[t.pos]
        j = owners[obj]
        if j == -1 or j == i:
            owners[obj] = i
            t = cm.opened(t._replace(pos=t.pos + 1, waiting=False))
            event = "open"
        else:
            kill, t = cm.resolve(t, txs[j])
            if kill:
                txs[j] = txs[j]._replace(status=ABORTED, waiting=False, left=0)
                owners = [-1 if o == j else o for o in owners]
                owners[obj] = i
                t = cm.opened(t._replace(pos=t.pos + 1, waiting=False))
                event = "abort"
            else:
                t = t._replace(waiting=True)
                event = "wait"
    txs[i] = t
    return (tuple(owners), _normalize(txs)), event


def explore(progs: list[list[int]], cm: Any, order: list[int] | None = None,
            limit: int = 200_000, partial: bool = False
            ) -> tuple[list[State], list[list[tuple[int, str, int]]]]:
    """All reachable states and the labelled edges (process, event, target).

    If the state space has more than limit states, raise an error, or, with
    partial=True, keep only the first limit states and the edges between
    them. A cycle in the partial graph is still a real cycle.
    """
    start = initial(progs, cm, order)
    index = {start: 0}
    states = [start]
    edges: list[list[tuple[int, str, int]]] = [[]]
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for i in enabled(states[u]):
            v_state, ev = step(progs, cm, states[u], i)
            v = index.get(v_state)
            if v is None:
                if len(states) >= limit:
                    if partial:
                        continue
                    raise RuntimeError("state space too large")
                v = index[v_state] = len(states)
                states.append(v_state)
                edges.append([])
                queue.append(v)
            edges[u].append((i, ev, v))
    return states, edges


def _sccs(n: int, edges: list[list[tuple[int, str, int]]]) -> list[int]:
    """Iterative Tarjan; return the component number of each state."""
    index = [-1] * n
    low = [0] * n
    comp = [-1] * n
    on = [False] * n
    stack: list[int] = []
    counter = 0
    ncomp = 0
    for root in range(n):
        if index[root] != -1:
            continue
        work = [(root, 0)]
        index[root] = low[root] = counter
        counter += 1
        stack.append(root)
        on[root] = True
        while work:
            u, k = work[-1]
            if k < len(edges[u]):
                work[-1] = (u, k + 1)
                v = edges[u][k][2]
                if index[v] == -1:
                    index[v] = low[v] = counter
                    counter += 1
                    stack.append(v)
                    on[v] = True
                    work.append((v, 0))
                elif on[v]:
                    low[u] = min(low[u], index[v])
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                low[parent] = min(low[parent], low[u])
            if low[u] == index[u]:
                while True:
                    w = stack.pop()
                    on[w] = False
                    comp[w] = ncomp
                    if w == u:
                        break
                ncomp += 1
    return comp


def fair_livelocks(states: list[State], edges: list[list[tuple[int, str, int]]]) -> list[set[int]]:
    """Return the strongly connected sets of states in which every process
    that is not done takes a step on some edge inside the set.

    Such a set holds an infinite fair run (every live process keeps taking
    steps) in which no transaction commits, since a commit can never be
    undone and so cannot lie on a cycle.
    """
    comp = _sccs(len(states), edges)
    groups: dict[int, set[int]] = {}
    for u, c in enumerate(comp):
        groups.setdefault(c, set()).add(u)
    found = []
    for members in groups.values():
        movers = {i for u in members for i, _, v in edges[u] if v in members}
        if not movers:
            continue
        live = set(enabled(states[next(iter(members))]))
        if live <= movers:
            found.append(members)
    return found


def _path(edges: list[list[tuple[int, str, int]]], src: int, goal: Any,
          inside: set[int] | None) -> tuple[list[int], int]:
    """BFS from src to a state where goal(state) holds; return (pids, state)."""
    prev: dict[int, tuple[int, int] | None] = {src: None}
    queue = deque([src])
    while queue:
        u = queue.popleft()
        if goal(u):
            pids = []
            w = u
            while prev[w] is not None:
                pw, pid = prev[w]
                pids.append(pid)
                w = pw
            return pids[::-1], u
        for i, _, v in edges[u]:
            if v not in prev and (inside is None or v in inside):
                prev[v] = (u, i)
                queue.append(v)
    raise ValueError("no path")


def lasso(progs: list[list[int]], cm: Any, order: list[int] | None = None,
          limit: int = 200_000) -> tuple[list[int], list[int]] | None:
    """Return (prefix, cycle), two schedules: after prefix, running cycle
    returns to the same state, every live process steps in it, and nobody
    commits. Return None if none is found among the first limit states."""
    states, edges = explore(progs, cm, order, limit, partial=True)
    sets = fair_livelocks(states, edges)
    if not sets:
        return None
    members = sets[0]
    s = min(members)
    prefix, _ = _path(edges, 0, lambda u: u == s, None)
    cycle: list[int] = []
    cur = s
    for p in enabled(states[s]):
        hop, cur = _path(edges, cur, lambda u: any(i == p and v in members for i, _, v in edges[u]),
                         members)
        cycle += hop
        v = next(v for i, _, v in edges[cur] if i == p and v in members)
        cycle.append(p)
        cur = v
    back, _ = _path(edges, cur, lambda u: u == s, members)
    return prefix, cycle + back


def replay(progs: list[list[int]], cm: Any, schedule: list[int], state: State | None = None,
           order: list[int] | None = None) -> tuple[State, list[str]]:
    """Run the given steps from state (or from the start); return the state and events."""
    st = state if state is not None else initial(progs, cm, order)
    events = []
    for i in schedule:
        st, ev = step(progs, cm, st, i)
        events.append(ev)
    return st, events


def random_run(progs: list[list[int]], cm: Any, rng: random.Random, max_steps: int = 10_000,
               order: list[int] | None = None) -> dict[str, Any]:
    """Run random steps until all commit or max_steps; return counts."""
    st = initial(progs, cm, order)
    count = {"steps": 0, "abort": 0, "commit": 0, "wait": 0, "backoff": 0, "own": [0] * len(progs),
             "commit_at": [None] * len(progs), "done": False}
    for _ in range(max_steps):
        ready = enabled(st)
        if not ready:
            count["done"] = True
            break
        i = rng.choice(ready)
        st, ev = step(progs, cm, st, i)
        count["steps"] += 1
        count["own"][i] += 1
        if ev in count:
            count[ev] += 1
        if ev == "commit":
            count["commit_at"][i] = count["own"][i]
    else:
        count["done"] = not enabled(st)
    return count
