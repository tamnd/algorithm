# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/path-vector-routing/. The authors are listed in prov/CAQP3D.jsonl.

"""Path-vector routing toward one destination, and the stable paths problem.

PathVector simulates the protocol as Griffin, Shepherd and Wilfong describe
it (SPVP): each node keeps the last path heard from each neighbour, drops
paths that contain itself, picks the best permitted path by its own ranking,
and sends it to its neighbours when it changes. Links are reliable FIFO
channels with seeded random delays.

The SPP helpers work on an instance given as ranked lists of permitted
paths: they test stability, list all stable assignments by brute force, and
build the graph of states reachable when one node at a time re-selects its
best path.
"""

import heapq
import itertools
import random

EPS = ()  # the empty path: no route


def hop_count_rank(u, path):
    """Default ranking: fewer hops first, then the smaller node sequence."""
    return (len(path), tuple(repr(x) for x in path))


def list_rank(prefs):
    """Ranking from SPP lists: prefs[u] lists the permitted paths of u,
    most preferred first. A path that is not listed is not permitted."""
    pos = {u: {tuple(p): i for i, p in enumerate(ps)} for u, ps in prefs.items()}

    def rank(u, path):
        return pos.get(u, {}).get(tuple(path))
    return rank


class PathVector:
    def __init__(self, graph, dest, rank=hop_count_rank, export=None,
                 rng=None, max_delay=3, batch=3):
        self.adj = {u: set(nb) for u, nb in graph.items()}
        self.d, self.rank = dest, rank
        self.export = export or (lambda u, v, path: True)
        self.rng = rng if rng is not None else random.Random(0)
        self.max_delay, self.batch, self.pending = max_delay, batch, set()
        self.rib_in = {u: {} for u in self.adj}
        self.best = {u: EPS for u in self.adj}
        self.events, self.seq, self.now = [], 0, 0
        self.last_arrival = {}
        self.sent = 0
        self.changes = 0
        for u in sorted(self.adj, key=repr):  # @line L1
            if u == self.d:
                self.best[u] = (u,)
                self._send_all(u)

    def _push(self, t, ev):
        self.seq += 1
        heapq.heappush(self.events, (t, self.seq, ev))

    def _send(self, u, v, path):
        self.sent += 1
        if not self.export(u, v, path):
            path = EPS                       # a filtered route is a withdrawal
        t = self.now + self.rng.randint(1, self.max_delay)
        t = max(t, self.last_arrival.get((u, v), 0))   # FIFO per link
        self.last_arrival[(u, v)] = t
        self._push(t, ("msg", v, u, path))

    def _send_all(self, u):
        # Changes made within one batch interval go out as one update with
        # the latest path, as BGP's MRAI timer does.
        if self.batch == 0:
            self._flush(u)
        elif u not in self.pending:
            self.pending.add(u)
            self._push(self.now + self.rng.randint(1, self.batch), ("flush", u))

    def _flush(self, u):
        self.pending.discard(u)
        for v in sorted(self.adj[u], key=repr):  # @line L9
            self._send(u, v, self.best[u])

    def _recompute(self, u):
        if u == self.d:  # @line L5
            return
        cands = []
        for v, p in self.rib_in[u].items():
            if p and u not in p:  # @line L6
                q = (u,) + p
                r = self.rank(u, q)
                if r is not None:
                    cands.append((r, q))
        new = min(cands)[1] if cands else EPS  # @line L7
        if new != self.best[u]:  # @line L8
            self.best[u] = new
            self.changes += 1
            self._send_all(u)

    def link_down(self, t, u, v):
        self._push(t, ("down", u, v))

    def link_up(self, t, u, v):
        self._push(t, ("up", u, v))

    def run(self, until=None, max_events=10 ** 6):
        """Process events; returns True if no message is left (converged)."""
        n = 0
        while self.events and n < max_events:
            if until is not None and self.events[0][0] > until:
                break
            t, _, ev = heapq.heappop(self.events)
            self.now, n = t, n + 1
            if ev[0] == "msg":
                _, u, v, p = ev
                if v in self.adj[u]:
                    self.rib_in[u][v] = p  # @line L2
                    self._recompute(u)  # @line L3
            elif ev[0] == "flush":
                self._flush(ev[1])
            elif ev[0] == "down":
                _, u, v = ev
                self.adj[u].discard(v)
                self.adj[v].discard(u)
                for a, b in ((u, v), (v, u)):
                    self.rib_in[a].pop(b, None)  # @line L4
                    self._recompute(a)
            elif ev[0] == "up":
                _, u, v = ev
                self.adj[u].add(v)
                self.adj[v].add(u)
                for a, b in ((u, v), (v, u)):
                    self._send(a, b, self.best[a])  # @line L10
        return not self.events

    def next_hop(self, u):
        p = self.best[u]
        return p[1] if len(p) > 1 else None


# ------------------------------------------------------------------ SPP

def choices(prefs, pi, u, adj, origin):
    """The permitted paths u.pi(v) over the neighbours v of u."""
    out = []
    allowed = {tuple(p) for p in prefs.get(u, [])}
    for v in adj[u]:
        p = pi.get(v, EPS)
        if p and (u,) + p in allowed:
            out.append((u,) + p)
    return out


def best_of(prefs, u, paths):
    rank = {tuple(p): i for i, p in enumerate(prefs.get(u, []))}
    return min(paths, key=lambda p: rank[p]) if paths else EPS


def is_stable(prefs, pi, adj, origin):
    for u in adj:
        if u == origin:
            if pi[u] != (origin,):
                return False
        elif pi[u] != best_of(prefs, u, choices(prefs, pi, u, adj, origin)):
            return False
    return True


def stable_assignments(prefs, adj, origin):
    """All stable path assignments, by trying every combination."""
    nodes = sorted((u for u in adj if u != origin), key=repr)
    options = [[EPS] + [tuple(p) for p in prefs.get(u, [])] for u in nodes]
    out = []
    for combo in itertools.product(*options):
        pi = dict(zip(nodes, combo))
        pi[origin] = (origin,)
        if is_stable(prefs, pi, adj, origin):
            out.append(pi)
    return out


def activation_graph(prefs, adj, origin):
    """States reachable from 'only the origin has a path' when one node at a
    time sets its path to its best choice. Returns (states, edges), where a
    state is a tuple of paths in sorted node order and edges excludes
    self-loops."""
    nodes = sorted(adj, key=repr)
    start = tuple((origin,) if u == origin else EPS for u in nodes)
    seen, stack, edges = {start}, [start], set()
    while stack:
        s = stack.pop()
        pi = dict(zip(nodes, s))
        for i, u in enumerate(nodes):
            if u == origin:
                continue
            new = best_of(prefs, u, choices(prefs, pi, u, adj, origin))
            if new != s[i]:
                t = s[:i] + (new,) + s[i + 1:]
                edges.add((s, t))
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
    return seen, edges


def has_cycle(states, edges):
    out = {s: [] for s in states}
    for a, b in edges:
        out[a].append(b)
    color = {s: 0 for s in states}
    for s0 in states:
        if color[s0]:
            continue
        stack = [(s0, iter(out[s0]))]
        color[s0] = 1
        while stack:
            s, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[s] = 2
                stack.pop()
            elif color[nxt] == 1:
                return True
            elif color[nxt] == 0:
                color[nxt] = 1
                stack.append((nxt, iter(out[nxt])))
    return False


def parse(paths):
    """'130' -> (1, 3, 0), for the single-digit gadgets of the paper."""
    return [tuple(int(c) for c in p) for p in paths]


GADGET_EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 4), (3, 4)]


def gadget(name):
    """The SPP instances of Griffin, Shepherd and Wilfong (2002)."""
    if name == "DISAGREE":
        adj = {0: {1, 2}, 1: {0, 2}, 2: {0, 1}}
        prefs = {1: parse(["120", "10"]), 2: parse(["210", "20"])}
        return adj, prefs
    adj = {u: set() for u in range(5)}
    for u, v in GADGET_EDGES:
        adj[u].add(v)
        adj[v].add(u)
    prefs = {1: parse(["130", "10"]), 2: parse(["210", "20"])}
    prefs[3] = parse(["30"] if name == "GOOD" else ["3420", "30"])
    prefs[4] = parse(["420", "430"] if name == "BAD" else ["430", "420"])
    return adj, prefs
