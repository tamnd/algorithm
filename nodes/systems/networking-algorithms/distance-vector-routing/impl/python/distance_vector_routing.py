# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-vector-routing/. The authors are listed in prov/DWVTYT.jsonl.

"""Distance-vector routing as a discrete-event simulation.

Each router keeps the last distance vector that it heard from each neighbour
and recomputes its own table from them (the Bellman-Ford rule). It sends its
vector to every neighbour on a periodic timer, and at once after a change when
triggered updates are on. Metrics are integers, and INF = 16 means
unreachable, as in RIP. The time is an integer clock; nothing here sleeps.

Modes for the vector sent to a neighbour x:
  "none"   : send every route.
  "split"  : simple split horizon, omit the routes whose next hop is x.
  "poison" : split horizon with poison reverse, send INF for those routes.

Cost of one RECOMPUTE: O(k * deg) for k destinations and deg neighbours.
"""

import heapq
import random

INF = 16

# event classes, in the order in which events at the same time run
_LINK, _DELIVER, _TIMER = 0, 1, 2


class DVNetwork:
    """A network of distance-vector routers.

    graph: dict node -> dict neighbour -> positive int cost (symmetric).
    """

    def __init__(self, graph, mode="none", period=30, delay=1, timeout=180,
                 triggered=False, jitter=0, rng=None, inf=INF):
        assert mode in ("none", "split", "poison")
        self.w = {u: dict(nb) for u, nb in graph.items()}
        self.mode, self.period, self.delay = mode, period, delay
        self.timeout, self.triggered, self.inf = timeout, triggered, inf
        self.rng = rng if rng is not None else random.Random(0)
        self.now = 0
        self.cut = set()          # links that drop messages silently
        self.V = {u: {} for u in self.w}       # V[y][x] = last vector from x
        self.heard = {u: {} for u in self.w}   # heard[y][x] = time of it
        self.D = {u: {u: (0, u)} for u in self.w}   # @line L1
        self.events = []
        self.seq = 0
        self.messages = 0
        for u in sorted(self.w):
            start = self.rng.randint(0, jitter) if jitter else 0
            self._push(start, _TIMER, ("timer", u))

    def _push(self, t, cls, ev):
        self.seq += 1
        heapq.heappush(self.events, (t, cls, self.seq, ev))

    # ---------------------------------------------------------- handlers
    def _receive(self, y, x, vec):
        if x not in self.w[y]:
            return                  # the link went down while in flight
        self.V[y][x] = vec  # @line L2
        self.heard[y][x] = self.now
        self._recompute(y)  # @line L3

    def _timer(self, y):
        for x in list(self.V[y]):
            if self.now - self.heard[y].get(x, 0) >= self.timeout:  # @line L4
                del self.V[y][x]
        self._recompute(y, send=False)  # @line L5
        self._send_all(y)
        self._push(self.now + self.period, _TIMER, ("timer", y))

    def _link_down(self, y, x):
        self.V[y].pop(x, None)  # @line L6
        self.w[y].pop(x, None)
        self._recompute(y)

    def _recompute(self, y, send=True):
        inf = self.inf
        dests = set(self.D[y])
        for vec in self.V[y].values():
            dests.update(vec)
        changed = False
        for d in sorted(dests, key=repr):  # @line L7
            if d == y:
                continue
            m, h = inf, None  # @line L8
            for x in sorted(self.V[y], key=repr):  # @line L9
                if d in self.V[y][x]:
                    c = min(inf, self.w[y][x] + self.V[y][x][d])
                    if c < m:
                        m, h = c, x
            old = self.D[y].get(d)
            if old is None or old[0] != m or old[1] != h:
                self.D[y][d] = (m, h)  # @line L10
                if old is None or old[0] != m:
                    changed = True
        if changed and self.triggered and send:  # @line L11
            self._send_all(y)

    def vector_for(self, y, x):
        """The vector that y sends to its neighbour x."""
        vec = {}
        for d, (m, h) in self.D[y].items():
            if h == x and h != y:  # @line L12
                if self.mode == "split":
                    continue
                if self.mode == "poison":
                    vec[d] = self.inf
                    continue
            vec[d] = m
        return vec

    def _send_all(self, y):
        for x in sorted(self.w[y], key=repr):
            vec = self.vector_for(y, x)
            self.messages += 1
            if (y, x) in self.cut:
                continue
            self._push(self.now + self.delay, _DELIVER, ("msg", x, y, vec))  # @line L13

    # ---------------------------------------------------------- driver
    def link_down(self, t, u, v):
        """Both ends detect the failure of link (u, v) at time t."""
        self._push(t, _LINK, ("down", u, v))

    def link_cut(self, t, u, v):
        """Link (u, v) drops all messages from time t; the ends do not know."""
        self._push(t, _LINK, ("cut", u, v))

    def set_cost(self, t, u, v, c):
        self._push(t, _LINK, ("cost", u, v, c))

    def run(self, until):
        """Process all events with time <= until."""
        while self.events and self.events[0][0] <= until:
            t, _, _, ev = heapq.heappop(self.events)
            self.now = t
            kind = ev[0]
            if kind == "timer":
                self._timer(ev[1])
            elif kind == "msg":
                self._receive(ev[1], ev[2], ev[3])
            elif kind == "down":
                _, u, v = ev
                self._link_down(u, v)
                self._link_down(v, u)
            elif kind == "cut":
                _, u, v = ev
                self.cut.update({(u, v), (v, u)})
            elif kind == "cost":
                _, u, v, c = ev
                self.w[u][v] = self.w[v][u] = c
                self._recompute(u)
                self._recompute(v)
        self.now = until
        return self

    def metric(self, y, d):
        return self.D[y].get(d, (self.inf, None))[0]

    def next_hop(self, y, d):
        return self.D[y].get(d, (self.inf, None))[1]


def synchronous(graph, mode="none", inf=INF):
    """A network that runs in synchronous rounds.

    Every router sends at times 0, 2, 4, ...; messages arrive one tick later.
    Round r ends at time 2r. No triggered updates.
    """
    return DVNetwork(graph, mode=mode, period=2, delay=1, timeout=10 ** 9,
                     triggered=False, inf=inf)


def rounds_to_reach(net, routers, dest, value, start_round, max_rounds=200):
    """Run net round by round from start_round; return the first round count
    (after start_round) at which every router in routers has metric value."""
    for r in range(1, max_rounds + 1):
        net.run(2 * (start_round + r))
        if all(net.metric(y, dest) == value for y in routers):
            return r
    return None
