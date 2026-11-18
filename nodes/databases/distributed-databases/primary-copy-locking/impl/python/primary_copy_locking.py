# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/primary-copy-locking/. The authors are listed in prov/SBHSMT.jsonl.
"""Primary copy two-phase locking on replicated data.

A small simulation in one thread. Each item has copies at some sites, and
one copy is the primary copy. Only the site of the primary copy keeps locks
for the item. A transaction runs at a home site. It gets an S lock at the
primary before it reads any copy, and an X lock at the primary before it
writes. At commit it sends its writes to every copy and waits for the
acknowledgments. Only then does it tell the primary sites to install the
writes on the primary copies and release its locks (strict 2PL).

The network delivers messages in a random order chosen by a seeded
random.Random, but first in, first out on each channel (one pair of sites).
Only messages between different sites are counted. A site can fail and stay
down: a message to it comes back as "no response". The primary of an item
whose site is down cannot be locked, so the item is unavailable.

With early_release=True, the primary releases the locks when the writes are
sent, not after they are acknowledged. The tests show that this breaks
one-copy serializability.

The history uses copy names "x@A". A read is recorded when a copy returns
its value, a write when a copy installs it. Only committed transactions
install writes, so every write in the history is committed.
"""

SHARED, EXCLUSIVE = "S", "X"


class Site:
    def __init__(self, sid, items, primary_of):
        self.sid = sid
        self.value = {x: 0 for x in items}
        self.up = True
        self.primary_of = sorted(primary_of)
        self.holders = {x: {} for x in self.primary_of}   # item -> {txn: mode}
        self.queue = {x: [] for x in self.primary_of}     # item -> [(txn, mode, read_here)]

    def compatible(self, x, txn, mode):
        for h, m in self.holders[x].items():
            if h != txn and (mode == EXCLUSIVE or m == EXCLUSIVE):
                return False
        return True


class Txn:
    def __init__(self, tid, ops, home):
        self.tid = tid
        self.ops = list(ops)
        self.home = home
        self.i = 0
        self.status = "active"       # active, committing, committed, aborted
        self.reads = {}
        self.writes = {}
        self.contacted = set()       # primary sites that may hold a lock or a request
        self.pending = set()


class PrimaryCopyDB:
    def __init__(self, placement, primary=None, early_release=False):
        self.placement = {x: sorted(s) for x, s in placement.items()}
        self.primary = dict(primary or {x: s[0] for x, s in self.placement.items()})
        self.early_release = early_release
        names = sorted({s for ss in placement.values() for s in ss})
        self.sites = {s: Site(s, [x for x in placement if s in placement[x]],
                              [x for x in placement if self.primary[x] == s])
                      for s in names}
        self.txns = {}
        self.net = []                # (src, dst, payload)
        self.history = []            # (kind, txn, "x@A" or None)
        self.commit_order = []
        self.messages = 0
        self.victims = []

    # ------------------------------------------------------------ network
    def send(self, src, dst, payload):
        if src != dst:
            self.messages += 1
        self.net.append((src, dst, payload))

    def deliver(self, k):
        chan = self.net[k][:2]
        k = next(j for j, m in enumerate(self.net) if m[:2] == chan)   # FIFO per channel
        src, dst, payload = self.net.pop(k)
        if payload[0] in ("granted", "value", "ack", "nores"):
            self.on_txn(self.txns[payload[1]], payload)
        elif not self.sites[dst].up:
            if payload[0] != "release":
                self.send(dst, src, ("nores", payload[1], payload, dst))
        else:
            self.on_site(self.sites[dst], src, payload)
        self.detect_deadlocks()

    # ------------------------------------------------------------- sites
    def on_site(self, site, src, payload):
        kind, tid = payload[0], payload[1]
        if kind == "lock":
            _, _, x, mode, read_here = payload
            if self.txns[tid].status == "aborted":
                return
            req = (tid, mode, read_here)
            if not site.queue[x] and site.compatible(x, tid, mode):
                self.grant(site, x, req)
            else:
                site.queue[x].append(req)
        elif kind == "read":
            x = payload[2]
            self.history.append(("r", tid, "%s@%s" % (x, site.sid)))
            self.send(site.sid, self.txns[tid].home, ("value", tid, x, site.value[x]))
        elif kind == "install":
            _, _, x, v = payload
            site.value[x] = v
            self.history.append(("w", tid, "%s@%s" % (x, site.sid)))
            self.send(site.sid, self.txns[tid].home, ("ack", tid, x, site.sid))
        elif kind == "release":
            for x, v in payload[2].items():
                site.value[x] = v
                self.history.append(("w", tid, "%s@%s" % (x, site.sid)))
            self.release(site, tid)

    def grant(self, site, x, req):
        tid, mode, read_here = req
        h = site.holders[x]
        h[tid] = EXCLUSIVE if mode == EXCLUSIVE or h.get(tid) == EXCLUSIVE else SHARED
        value = None
        if read_here:
            value = site.value[x]
            self.history.append(("r", tid, "%s@%s" % (x, site.sid)))
        self.send(site.sid, self.txns[tid].home, ("granted", tid, x, value))

    def release(self, site, tid):
        for x in site.primary_of:
            site.holders[x].pop(tid, None)
            site.queue[x] = [q for q in site.queue[x] if q[0] != tid]
        for x in site.primary_of:
            while site.queue[x] and site.compatible(x, site.queue[x][0][0], site.queue[x][0][1]):
                self.grant(site, x, site.queue[x].pop(0))

    def fail(self, sid):
        site = self.sites[sid]
        if not site.up:
            return
        site.up = False
        lost = {tid for x in site.primary_of for tid in site.holders[x]}
        lost |= {q[0] for x in site.primary_of for q in site.queue[x]}
        site.holders = {x: {} for x in site.primary_of}
        site.queue = {x: [] for x in site.primary_of}
        for tid in sorted(lost):
            t = self.txns[tid]
            if t.status == "active":      # a committing transaction keeps going
                self.abort(t)

    # ----------------------------------------------------------- clients
    def start(self, tid, ops, home):
        t = Txn(tid, ops, home)
        self.txns[tid] = t
        self.issue(t)

    def write_value(self, t):
        return t.tid * 100 + sum(t.reads[x] for x in sorted(t.reads)) % 100

    def issue(self, t):
        if t.i == len(t.ops):
            self.commit(t)
            return
        kind, x = t.ops[t.i]                                  # @line L1
        p = self.primary[x]
        t.contacted.add(p)
        if kind == "r":                                       # @line L2
            local = t.home in self.placement[x] and t.home != p
            # @line L3
            self.send(t.home, p, ("lock", t.tid, x, SHARED, not local))
        else:                                                 # @line L5
            # @line L6
            self.send(t.home, p, ("lock", t.tid, x, EXCLUSIVE, False))

    def on_txn(self, t, payload):
        if t.status in ("aborted", "committed"):
            return
        kind = payload[0]
        if t.status == "committing":
            # an ack, or "no response" from a copy whose site is down
            x, s = (payload[2], payload[3]) if kind == "ack" else (payload[2][2], payload[3])
            t.pending.discard((x, s))                         # @line L9
            if not t.pending:
                self.finish(t)
            return
        op, x = t.ops[t.i]
        if kind == "nores":
            if payload[2][0] == "read":
                # the local copy is down; read the primary copy, still under the lock
                self.send(t.home, self.primary[x], ("read", t.tid, x))
                return
            self.abort(t)                                     # the primary is down
            return
        if kind == "granted" and op == "r" and payload[3] is None:
            self.send(t.home, t.home, ("read", t.tid, x))     # @line L4
            return
        if op == "r":
            t.reads[x] = payload[3]                           # @line L4
        else:
            t.writes[x] = self.write_value(t)
        t.i += 1
        self.issue(t)

    def commit(self, t):
        # T holds all its locks here, so this is its lock point.
        t.status = "committing"                               # @line L7
        self.history.append(("c", t.tid, None))
        self.commit_order.append(t.tid)
        t.pending = set()
        for x in sorted(t.writes):                            # @line L8
            for s in self.placement[x]:
                if s != self.primary[x]:
                    t.pending.add((x, s))
                    self.send(t.home, s, ("install", t.tid, x, t.writes[x]))
        if self.early_release or not t.pending:
            self.finish(t)

    def finish(self, t):
        for p in sorted(t.contacted):                         # @line L10
            mine = {x: v for x, v in t.writes.items() if self.primary[x] == p}
            self.send(t.home, p, ("release", t.tid, mine))
        t.status = "committed"

    def abort(self, t):
        t.status = "aborted"
        self.history.append(("a", t.tid, None))
        for p in sorted(t.contacted):
            self.send(t.home, p, ("release", t.tid, {}))

    # ---------------------------------------------------------- deadlocks
    def waits_for(self):
        edges = {}
        for s in sorted(self.sites):
            site = self.sites[s]
            if not site.up:
                continue
            for x in site.primary_of:
                q = site.queue[x]
                for pos, (w, mode, _) in enumerate(q):
                    if self.txns[w].status != "active":
                        continue
                    for h, m in site.holders[x].items():
                        if h != w and (mode == EXCLUSIVE or m == EXCLUSIVE):
                            edges.setdefault(w, set()).add(h)
                    for w2, m2, _ in q[:pos]:
                        if w2 != w and (mode == EXCLUSIVE or m2 == EXCLUSIVE):
                            edges.setdefault(w, set()).add(w2)
        return edges

    def find_cycle(self, edges):
        color, stack = {}, []

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
            active = [v for v in cycle if self.txns[v].status == "active"]
            victim = max(active)
            self.victims.append((victim, tuple(cycle)))
            self.abort(self.txns[victim])

    # ---------------------------------------------------------------- run
    def run(self, rng, txns, homes, events=(), start_spread=3):
        """txns: {tid: ops}; homes: {tid: site}; events: [(step, "fail", site)]."""
        starts = sorted((rng.randrange(start_spread), tid) for tid in sorted(txns))
        events = sorted(events)
        step = 0
        while True:
            while starts and starts[0][0] <= step:
                _, tid = starts.pop(0)
                self.start(tid, txns[tid], homes[tid])
            while events and events[0][0] <= step:
                self.fail(events.pop(0)[2])
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
        stuck = [t.tid for t in self.txns.values() if t.status not in ("committed", "aborted")]
        if stuck:
            raise RuntimeError("transactions left waiting: %r" % stuck)
        return self.history
