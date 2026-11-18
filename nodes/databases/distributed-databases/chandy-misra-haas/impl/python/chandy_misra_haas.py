# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chandy-misra-haas/. The authors are listed in prov/H4QN6P.jsonl.
"""Chandy-Misra-Haas edge chasing for the resource model.

A small simulation in one thread of the resource model of Chandy, Misra and
Haas (1983), Section 2.1. Each site has a controller that manages the
resources at the site. A transaction t has a home site h and at most one
process per site; the process (t, s) is named by the pair. The home process
asks for resources one at a time. A resource at the home site is asked of
the home controller. For a resource at another site m, the home controller
sends the request to the process (t, m), which asks its own controller, and
which replies when it gets the resource. All locks are exclusive, and the
queue of each resource is first in, first out.

Wait edges:
  local  (u, s) -> (h, s)  the process (u, s) waits for a resource that the
                           transaction h holds at s;
  remote (t, h) -> (t, m)  the home process waits for the reply of (t, m);
  remote (t, m) -> (t, h)  the agent (t, m) has replied and holds resources
                           at m, and it waits for the home process to tell
                           it to release them.
A process is idle while it waits. The home process is executing between
two requests, and it stops waiting when it commits or aborts. Without the
third kind of edge, a cycle can pass through an agent that holds a resource
and looks executing, and the detector misses a real deadlock.

The probe computation is that of Section 3.1, with two changes that the
page explains: each computation has a number, so that a later computation
by the same process is not stopped by the flags of an earlier one, and with
literal=False a controller also declares P_i deadlocked when P_i is locally
dependent on the process that the probe reaches.

The network delivers messages in an order chosen by a seeded random.Random,
first in, first out on each channel (one ordered pair of sites).
"""


class Controller:
    def __init__(self, sid):
        self.sid = sid
        self.holder = {}          # resource -> transaction that holds it
        self.queue = {}           # resource -> [transaction] waiting, in order
        self.waiting = {}         # transaction -> resource its process here waits for
        self.held = {}            # transaction -> set of resources held here
        self.dependent = {}       # process (t, sid) -> {initiator: computation number}
        self.aborted = set()


class Txn:
    def __init__(self, tid, home, plan):
        self.tid = tid
        self.home = home
        self.plan = list(plan)    # [(resource, site)]
        self.i = 0
        self.status = "active"    # active, committed, aborted
        self.outstanding = None   # site of the remote request not yet answered
        self.contacted = set()


class CMH:
    def __init__(self, sites, literal=False, numbered=True, resolve=True, timers=True):
        self.ctl = {s: Controller(s) for s in sites}
        self.literal = literal
        self.numbered = numbered
        self.resolve = resolve
        self.timers = timers
        self.txns = {}
        self.net = []             # (src, dst, payload)
        self.seq = {}             # initiator -> number of its last computation
        self.messages = 0
        self.probes = 0
        self.declared = []        # processes declared deadlocked, in order
        self.on_declare = None    # test hook, called with the process

    # ------------------------------------------------------------ network
    def send(self, src, dst, payload):
        if src != dst:
            self.messages += 1
            if payload[0] == "probe":
                self.probes += 1
        self.net.append((src, dst, payload))

    def deliver(self, k):
        chan = self.net[k][:2]
        k = next(j for j, m in enumerate(self.net) if m[:2] == chan)   # FIFO per channel
        src, dst, payload = self.net.pop(k)
        getattr(self, "on_" + payload[0])(self.ctl[dst], src, *payload[1:])

    def drain(self, rng, hold=lambda msg: False):
        """Deliver messages in a random order until none is left, or all
        that are left are held by the caller."""
        while True:
            heads, seen = [], set()
            for k, m in enumerate(self.net):
                if m[:2] not in seen:            # the first message of each channel
                    seen.add(m[:2])
                    if not hold(m):
                        heads.append(k)
            if not heads:
                return
            self.deliver(heads[rng.randrange(len(heads))])

    # ------------------------------------------------------ process state
    def idle(self, p):
        # Only the state of the controller of p: its waiting table, and for
        # a home process the request that it has sent and not seen answered.
        t, s = p
        c = self.ctl[s]
        if t in c.waiting:
            return True
        tx = self.txns.get(t)
        if tx is None:
            return False
        if s == tx.home:
            return tx.status == "active" and tx.outstanding is not None
        return bool(c.held.get(t))     # it has replied and waits for the release

    def local_reach(self, k):
        """LD*(k): the idle processes that k reaches by local wait edges,
        with k itself. Uses only the state of the controller of k."""
        s = k[1]
        c = self.ctl[s]
        seen, stack = [k], [k]
        while stack:
            u = stack.pop()[0]
            if u in c.waiting:
                h = (c.holder[c.waiting[u]], s)
                if self.idle(h) and h not in seen:
                    seen.append(h)
                    stack.append(h)
        return seen

    def on_local_cycle(self, i):
        s = i[1]
        c = self.ctl[s]
        u = i[0]
        if u not in c.waiting:
            return False
        h = (c.holder[c.waiting[u]], s)
        return self.idle(h) and i in self.local_reach(h)

    def remote_edges(self, procs):
        out = []
        for a in procs:
            t = self.txns[a[0]]
            c = self.ctl[a[1]]
            if a[1] == t.home:
                if t.status == "active" and t.outstanding is not None:
                    out.append((a, (a[0], t.outstanding)))
            elif a[0] not in c.waiting and c.held.get(a[0]):
                out.append((a, (a[0], t.home)))
        return out

    def became_executing(self, p):
        self.ctl[p[1]].dependent.pop(p, None)                 # @line L10

    def became_idle(self, p):
        if self.timers:
            self.send(p[1], p[1], ("timer", p))

    # ----------------------------------------------------- probe computation
    def initiate(self, i):
        if not self.idle(i):
            return
        if self.on_local_cycle(i):                            # @line L1
            self.declare(i)
            return
        m = self.seq.get(i, 0) + 1                            # @line L2
        self.seq[i] = m
        for a, b in self.remote_edges(self.local_reach(i)):  # @line L3
            self.send(i[1], b[1], ("probe", i, m, a, b))      # @line L4

    def on_probe(self, ctl, src, i, m, j, k):
        dep = ctl.dependent.setdefault(k, {})
        fresh = dep.get(i, 0) < m if self.numbered else i not in dep
        # (iii): k has not replied to j. If k is an agent, j is its home and
        # the request of j still waits here. If k is the home, j is an agent
        # that waits for the home; a new request to j answers that wait, so
        # the probe is stale if k has a request out to the site of j.
        t = self.txns[k[0]]
        if k[1] == t.home:
            unanswered = t.outstanding != j[1]
        else:
            unanswered = k[0] in ctl.waiting
        if not (self.idle(k) and unanswered and fresh):       # @line L5
            return
        dep[i] = m                                            # @line L6
        reach = self.local_reach(k)
        if k == i or (not self.literal and i in reach):       # @line L7
            self.declare(i)
            return
        for a, b in self.remote_edges(reach):                 # @line L8
            self.send(k[1], b[1], ("probe", i, m, a, b))      # @line L9

    def declare(self, i):
        self.declared.append(i)
        if self.on_declare:
            self.on_declare(i)
        if self.resolve:
            t = self.txns[i[0]]
            self.send(i[1], t.home, ("abort", t.tid))

    def on_timer(self, ctl, src, p):
        self.initiate(p)

    # --------------------------------------------------- the transactions
    def start(self, tid, home, plan):
        t = Txn(tid, home, plan)
        self.txns[tid] = t
        self.step(t)

    def step(self, t):
        if t.i == len(t.plan):
            self.commit(t)
            return
        res, s = t.plan[t.i]
        if s == t.home:
            self.lock(self.ctl[s], t.tid, res)
        else:
            t.outstanding = s
            t.contacted.add(s)
            self.send(t.home, s, ("request", t.tid, res))
            self.became_idle((t.tid, t.home))

    def lock(self, ctl, tid, res):
        """The process (tid, ctl.sid) asks its controller for res."""
        if ctl.holder.get(res) is None:
            self.grant(ctl, tid, res)
        else:
            ctl.queue.setdefault(res, []).append(tid)
            ctl.waiting[tid] = res
            self.became_idle((tid, ctl.sid))

    def grant(self, ctl, tid, res):
        ctl.holder[res] = tid
        ctl.held.setdefault(tid, set()).add(res)
        ctl.waiting.pop(tid, None)
        self.became_executing((tid, ctl.sid))
        t = self.txns[tid]
        if ctl.sid == t.home:
            self.send(ctl.sid, ctl.sid, ("next", tid))
        else:
            self.send(ctl.sid, t.home, ("granted", tid, res))

    def unlock_all(self, ctl, tid):
        ctl.waiting.pop(tid, None)
        for res in list(ctl.queue):
            ctl.queue[res] = [u for u in ctl.queue[res] if u != tid]
        for res in sorted(ctl.held.pop(tid, ())):
            ctl.holder[res] = None
            if ctl.queue.get(res):
                self.grant(ctl, ctl.queue[res].pop(0), res)
        self.became_executing((tid, ctl.sid))

    def on_request(self, ctl, src, tid, res):
        if tid in ctl.aborted:
            return
        self.lock(ctl, tid, res)

    def on_granted(self, ctl, src, tid, res):
        t = self.txns[tid]
        if t.status != "active":
            return
        t.outstanding = None
        self.became_executing((tid, t.home))
        self.send(ctl.sid, ctl.sid, ("next", tid))

    def on_next(self, ctl, src, tid):
        t = self.txns[tid]
        if t.status != "active":
            return
        t.i += 1
        self.step(t)

    def commit(self, t):
        t.status = "committed"
        self.unlock_all(self.ctl[t.home], t.tid)
        for s in sorted(t.contacted):
            self.send(t.home, s, ("release", t.tid))

    def on_release(self, ctl, src, tid):
        self.unlock_all(ctl, tid)

    def on_abort(self, ctl, src, tid):
        t = self.txns[tid]
        if ctl.sid == t.home:
            if t.status != "active":
                return
            t.status = "aborted"
            t.outstanding = None
            self.unlock_all(ctl, tid)
            for s in sorted(t.contacted):
                self.send(t.home, s, ("abort", tid))
        else:
            ctl.aborted.add(tid)
            self.unlock_all(ctl, tid)

    # ---------------------------------------------------------------- run
    def run(self, rng, txns, auto=True):
        """txns: {tid: (home, plan)}. Start all, deliver until quiet. When
        nothing is in transit and auto is set, start a probe computation
        for every idle process, and go on while this finds deadlocks.
        Returns the transactions that are still active at the end."""
        for tid in sorted(txns):
            self.start(tid, *txns[tid])
        while True:
            self.drain(rng)
            stuck = sorted(p for t in self.txns.values() for p in self.processes(t) if self.idle(p))
            if not stuck or not auto:
                break
            before = len(self.declared)
            for p in stuck:
                self.initiate(p)
            self.drain(rng)
            if len(self.declared) == before or not self.resolve:
                break
        return sorted(t.tid for t in self.txns.values() if t.status == "active")

    def processes(self, t):
        return [(t.tid, s) for s in sorted({t.home} | t.contacted)]
