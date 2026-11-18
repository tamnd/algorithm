# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-one-write-all/. The authors are listed in prov/JG3SB7.jsonl.
"""Read-one write-all (ROWA) and the available copies form (ROWA-A).

This is a small simulation in one thread. Each site holds copies of some
items and runs strict two-phase locking on its own copies. A transaction is
a client that sends lock requests as messages. The network holds the
messages in flight, and a seeded random.Random picks the next one to deliver.

A read locks and reads one copy. A write locks all copies (ROWA) or all
copies whose sites answer (ROWA-A). A site can fail: it loses its lock table
and its queued requests, and a message to a failed site comes back as "no
response". A site that recovers marks its copies unreadable and starts one
copier transaction per item, which reads an available copy and writes the
local copy. ROWA-A commits a transaction only after the two validations of
Bernstein, Hadzilacos and Goodman (1987), Section 8.6. The copier is an
ordinary transaction: it writes the value it read to all available copies,
so it conflicts with every reader of x. With copier_writes_all=False it
writes only the recovered copy; the tests show that this breaks one-copy
serializability.

Simplifications, as stated on the page: the commit step (validation and the
installation of the writes at every site the transaction accessed) is one
atomic step, so it stands for an atomic commitment protocol such as
two-phase commit; deadlocks are found by a central detector that reads the
lock tables of all sites that are up.

The physical history uses copy names "x@A" (the copy of x at site A), so
that the one-copy serializability test of the tests can map it back to items.
"""

SHARED, EXCLUSIVE = "S", "X"


class Site:
    def __init__(self, sid, items):
        self.sid = sid
        self.items = sorted(items)
        self.value = {x: 0 for x in self.items}
        self.readable = set(self.items)
        self.up = True
        self.epoch = 0
        self.holders = {x: {} for x in self.items}   # item -> {txn: mode}
        self.queue = {x: [] for x in self.items}     # item -> [(txn, mode, op, value)]
        self.staged = {}                              # txn -> {item: value}

    def compatible(self, x, txn, mode):
        for h, m in self.holders[x].items():
            if h != txn and (mode == EXCLUSIVE or m == EXCLUSIVE):
                return False
        return True


class Txn:
    def __init__(self, tid, ops, copier_site=None):
        self.tid = tid
        self.ops = list(ops)          # ("r", x) or ("w", x)
        self.copier_site = copier_site
        self.i = 0
        self.status = "active"
        self.reads = {}
        self.accessed = []            # (site, item, epoch) for each granted lock
        self.missed = []              # (site, item) for each write that got no response
        self.touched = set()
        self.candidates = []
        self.pending = set()
        self.granted = 0


class ReplicatedDB:
    """Sites, clients and the network. mode is "rowa" or "available"."""

    def __init__(self, placement, mode="available", copier_writes_all=True):
        self.mode = mode
        self.copier_writes_all = copier_writes_all
        self.placement = {x: sorted(s) for x, s in placement.items()}
        sites = sorted({s for ss in placement.values() for s in ss})
        self.sites = {s: Site(s, [x for x in placement if s in placement[x]])
                      for s in sites}
        self.txns = {}
        self.net = []                 # messages in flight: (dst, payload)
        self.history = []             # physical history: (kind, txn, "x@A" or None)
        self.messages = 0
        self.next_copier = 1000
        self.victims = []

    # ------------------------------------------------------------ network
    def send(self, dst, payload):
        self.messages += 1
        self.net.append((dst, payload))

    def deliver(self, k):
        dst, payload = self.net.pop(k)
        if dst[0] == "site":
            site = self.sites[dst[1]]
            if not site.up:
                tid = payload[1]
                self.send(("txn", tid), ("nores", tid, site.sid, payload[2]))
            else:
                self.on_site(site, payload)
        else:
            self.on_reply(self.txns[dst[1]], payload)
        self.detect_deadlocks()

    # ------------------------------------------------------------- sites
    def on_site(self, site, payload):
        op, tid, x, value = payload
        t = self.txns[tid]
        if t.status != "active":
            return
        if op == "r" and x not in site.readable:
            self.send(("txn", tid), ("unreadable", tid, site.sid, x))
            return
        mode = SHARED if op == "r" else EXCLUSIVE
        req = (tid, mode, op, value)
        if not site.queue[x] and site.compatible(x, tid, mode):
            self.grant(site, x, req)
        else:
            site.queue[x].append(req)

    def grant(self, site, x, req):
        tid, mode, op, value = req
        h = site.holders[x]
        h[tid] = EXCLUSIVE if mode == EXCLUSIVE or h.get(tid) == EXCLUSIVE else SHARED
        copy = "%s@%s" % (x, site.sid)
        if op == "r":
            self.history.append(("r", tid, copy))
            self.send(("txn", tid), ("granted", tid, site.sid, x, site.value[x], site.epoch))
        else:
            site.staged.setdefault(tid, {})[x] = value
            self.history.append(("w", tid, copy))
            self.send(("txn", tid), ("granted", tid, site.sid, x, None, site.epoch))

    def release(self, site, tid):
        site.staged.pop(tid, None)
        for x in site.items:
            site.holders[x].pop(tid, None)
            site.queue[x] = [q for q in site.queue[x] if q[0] != tid]
        for x in site.items:
            while site.queue[x] and site.compatible(x, site.queue[x][0][0], site.queue[x][0][1]):
                self.grant(site, x, site.queue[x].pop(0))

    def fail(self, sid):
        site = self.sites[sid]
        if not site.up:
            return
        for x in site.items:
            for tid, _, op, _ in site.queue[x]:
                self.send(("txn", tid), ("nores", tid, sid, x))
        site.up = False
        site.holders = {x: {} for x in site.items}
        site.queue = {x: [] for x in site.items}
        site.staged = {}

    def recover(self, sid):
        site = self.sites[sid]
        if site.up:
            return
        site.up = True
        site.epoch += 1
        site.readable = set()
        for x in site.items:
            if len(self.placement[x]) > 1:
                self.start(self.next_copier, [("r", x), ("w", x)], copier_site=sid)
                self.next_copier += 1
            else:
                site.readable.add(x)

    # ----------------------------------------------------------- clients
    def start(self, tid, ops, copier_site=None):
        t = Txn(tid, ops, copier_site)
        self.txns[tid] = t
        self.issue(t)

    def write_value(self, t):
        return t.tid * 100 + sum(t.reads[x] for x in sorted(t.reads)) % 100

    def issue(self, t):
        if t.i == len(t.ops):
            self.commit(t)
            return
        kind, x = t.ops[t.i]                              # @line L1
        if kind == "r":                                   # @line L2
            # @line L3
            t.candidates = [s for s in self.placement[x] if s != t.copier_site]
            self.read_next(t, x)
        else:                                             # @line L6
            # @line L7
            if t.copier_site and not self.copier_writes_all:
                targets = [t.copier_site]
            else:
                targets = self.placement[x]
            t.pending = set(targets)
            t.granted = 0
            value = t.reads[x] if t.copier_site else self.write_value(t)
            for s in targets:
                t.touched.add(s)
                self.send(("site", s), ("w", t.tid, x, value))

    def read_next(self, t, x):
        if not t.candidates:
            self.abort(t)                                 # @line L5
            return
        s = t.candidates.pop(0)
        t.touched.add(s)
        self.send(("site", s), ("r", t.tid, x, None))     # @line L4

    def on_reply(self, t, payload):
        if t.status != "active":
            return
        kind, x = t.ops[t.i]
        if kind == "r":
            if payload[0] == "granted":
                _, _, s, _, value, epoch = payload
                t.reads[x] = value
                t.accessed.append((s, x, epoch))
                t.i += 1
                self.issue(t)
            else:
                self.read_next(t, x)
            return
        # @line L8
        s = payload[2]
        if payload[0] == "granted":
            t.granted += 1
            t.accessed.append((s, x, payload[5]))
        else:
            t.missed.append((s, x))                       # @line L10
        t.pending.discard(s)
        if t.pending:
            return
        if t.granted == 0 or (self.mode == "rowa" and any(m[1] == x for m in t.missed)):
            self.abort(t)                                 # @line L9
            return
        t.i += 1
        self.issue(t)

    def commit(self, t):
        # One atomic step: the two validations, then the commit at every site.
        # mode "naive" skips the validations; it is the wrong protocol that
        # the tests use as a non-example.
        check = self.mode != "naive"
        for s, x in t.missed:                             # @line L11
            if check and self.sites[s].up:
                self.abort(t)                             # @line L12
                return
        for s, x, epoch in t.accessed:                    # @line L13
            site = self.sites[s]
            if check and (not site.up or site.epoch != epoch):
                self.abort(t)                             # @line L14
                return
        # @line L15
        for s in sorted(t.touched):
            site = self.sites[s]
            if not site.up:
                continue
            for x, v in site.staged.get(t.tid, {}).items():
                site.value[x] = v
                site.readable.add(x)
            self.release(site, t.tid)
        t.status = "committed"
        self.history.append(("c", t.tid, None))

    def abort(self, t):
        t.status = "aborted"
        self.history.append(("a", t.tid, None))
        for s in sorted(t.touched):
            if self.sites[s].up:
                self.release(self.sites[s], t.tid)

    # ---------------------------------------------------------- deadlocks
    def waits_for(self):
        """Edges waiter -> txn it waits for, from the lock tables of up sites."""
        edges = {}
        for s in sorted(self.sites):
            site = self.sites[s]
            if not site.up:
                continue
            for x in site.items:
                q = site.queue[x]
                for pos, (w, mode, _, _) in enumerate(q):
                    for h, m in site.holders[x].items():
                        if h != w and (mode == EXCLUSIVE or m == EXCLUSIVE):
                            edges.setdefault(w, set()).add(h)
                    for w2, m2, _, _ in q[:pos]:
                        if w2 != w and (mode == EXCLUSIVE or m2 == EXCLUSIVE):
                            edges.setdefault(w, set()).add(w2)
        return edges

    def find_cycle(self, edges):
        color = {}
        stack = []

        def dfs(u):
            color[u] = 1
            stack.append(u)
            for v in sorted(edges.get(u, ())):
                if color.get(v, 0) == 1:
                    return stack[stack.index(v):]
                if color.get(v, 0) == 0:
                    c = dfs(v)
                    if c:
                        return c
            stack.pop()
            color[u] = 2
            return None

        for u in sorted(edges):
            if color.get(u, 0) == 0:
                c = dfs(u)
                if c:
                    return c
        return None

    def detect_deadlocks(self):
        while True:
            cycle = self.find_cycle(self.waits_for())
            if not cycle:
                return
            victim = max(cycle)
            self.victims.append((victim, tuple(cycle)))
            self.abort(self.txns[victim])

    # ---------------------------------------------------------------- run
    def run(self, rng, txns, events=(), start_spread=3):
        """txns: {tid: ops}. events: [(step, "fail" or "recover", site)].
        Transactions start at random steps in range(start_spread)."""
        starts = sorted((rng.randrange(start_spread), tid) for tid in sorted(txns))
        events = sorted(events)
        step = 0
        while True:
            while starts and starts[0][0] <= step:
                _, tid = starts.pop(0)
                self.start(tid, txns[tid])
            while events and events[0][0] <= step:
                _, what, s = events.pop(0)
                if what == "fail":
                    self.fail(s)
                else:
                    self.recover(s)
                self.detect_deadlocks()
            if self.net:
                self.deliver(rng.randrange(len(self.net)))
            elif starts or events:
                nxt = [starts[0][0]] if starts else []
                nxt += [events[0][0]] if events else []
                step = max(step, min(nxt))
                continue
            else:
                break
            step += 1
        stuck = [t for t in self.txns.values() if t.status == "active"]
        if stuck:
            raise RuntimeError("transactions left waiting: %r" % [t.tid for t in stuck])
        return self.history
