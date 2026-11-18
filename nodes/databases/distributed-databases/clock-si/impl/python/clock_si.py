# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock-si/. The authors are listed in prov/9E7PE4.jsonl.
"""A toy model of Clock-SI (Du, Elnikety and Zwaenepoel, SRDS 2013).

This is not a database. One process simulates a few partitions in steps of
global time called ticks. Each partition has a physical clock that is the
global time plus a fixed skew. A clock reading at partition p is
(tick + skew) * 1000 + p, and two readings at one partition differ by at
least 10, so all timestamps are unique and every clock only moves forward.

Each transaction starts at its originating partition, which is also its
coordinator. It reads first and then writes; the writes stay in a
workspace until commit. A message between partitions takes 1 or 2 ticks,
chosen with a seeded random.Random, so messages can arrive in any order. A
write to stable storage takes log_delay ticks. A coordinator can crash
during two-phase commit. Messages sent to it while it is down are lost.
When it comes back it reads its log: it sends the commit again if it
logged the commit, and else it aborts.

The flags in `checks` turn off parts of the protocol, so that the tests can
show that each part is needed.
"""

STRIDE = 10                  # so at most 10 partitions


class Txn:
    def __init__(self, tid, origin, reads, writes, start):
        """reads, writes: lists of keys. Each written value is a function of
        the values read, so a wrong read shows in the final state too."""
        self.tid, self.origin, self.start = tid, origin, start
        self.read_keys, self.write_keys = list(reads), list(writes)
        self.snapshot = self.commit = None
        self.reads, self.writes = {}, {}
        self.status = "active"       # active, committed, aborted


class Request:
    def __init__(self, kind, t, keys=(), ts=None, index=0):
        self.kind, self.t, self.keys, self.ts, self.index = kind, t, list(keys), ts, index
        self.counted = False         # counted as a delay already


class Partition:
    def __init__(self, pid, skew):
        self.pid, self.skew = pid, skew
        self.last = None
        self.queue = []

    def now(self, tick):
        phys = (tick + self.skew) * 1000 + self.pid
        return phys if self.last is None else max(phys, self.last)

    def read_clock(self, tick):
        v = (tick + self.skew) * 1000 + self.pid
        if self.last is not None:
            v = max(v, self.last + STRIDE)
        self.last = v
        return v


class ClockSI:
    def __init__(self, place, skews, init, rng, delta=0, log_delay=2, checks=None):
        """place: {key: partition}; skews: the skew of each partition, in
        ticks; delta: the snapshot age, in ticks."""
        self.place, self.rng = dict(place), rng
        self.parts = [Partition(p, s) for p, s in enumerate(skews)]
        self.delta, self.log_delay = delta * 1000, log_delay
        self.checks = {"clock": True, "pending": True, "max": True}
        self.checks.update(checks or {})
        self.versions = {k: [(-10 ** 9, v, 0)] for k, v in init.items()}   # (ts, value, tid)
        self.pending = {k: {} for k in init}       # key -> tid -> (state, prepare or commit ts)
        self.tick = 0
        self.net = []                # (tick, seq, destination, payload)
        self.seq = 0
        self.coord = {}              # tid -> [generator, replies needed, replies]
        self.down = set()
        self.delays = {"clock": 0, "pending": 0}
        self.messages = 0

    def send(self, src, dst, payload, delay=None):
        """dst is a partition number or ("coord", tid)."""
        if delay is None:
            here = dst if isinstance(dst, int) else self.txn[dst[1]].origin
            delay = 0 if here == src else self.rng.randint(1, 2)
            self.messages += here != src
        self.seq += 1
        self.net.append((self.tick + delay, self.seq, dst, payload))

    def reply(self, q, req, value):
        self.send(q, ("coord", req.t.tid), ("reply", req.index, value))

    # --------------------------------------------------------- partitions
    def try_request(self, q, req):
        """Serve one request at partition q. Returns False if it must wait."""
        part, t = self.parts[q], req.t
        if q != t.origin and req.kind in ("read", "prepare", "local"):
            if self.checks["clock"] and t.snapshot >= part.now(self.tick):           # @line L2
                self.delays["clock"] += not req.counted
                req.counted = True
                return False
        if req.kind == "read":
            k = req.keys[0]
            if self.checks["pending"] and any(ts < t.snapshot for _, ts in self.pending[k].values()):  # @line L3
                self.delays["pending"] += not req.counted
                req.counted = True
                return False
            _, v, _ = max(x for x in self.versions[k] if x[0] < t.snapshot)            # @line L4
            self.reply(q, req, v)
        elif req.kind in ("prepare", "local"):
            ok = all(not self.pending[k] and max(self.versions[k])[0] < t.snapshot      # @line L8
                     for k in req.keys)
            if not ok:
                self.reply(q, req, None)
            elif req.kind == "prepare":
                ts = part.read_clock(self.tick)
                for k in req.keys:
                    self.pending[k][t.tid] = ("prepared", ts)
                self.reply(q, req, ts)
            else:
                ts = part.read_clock(self.tick)                                        # @line L6
                for k in req.keys:
                    self.pending[k][t.tid] = ("committing", ts)
                self.send(q, q, Request("logged", t, req.keys, ts, req.index), self.log_delay)
        elif req.kind == "logged":           # the local commit record is on disk
            self.install(t, req.keys, req.ts)
            self.reply(q, req, req.ts)
        elif req.kind == "commit":
            self.install(t, req.keys, req.ts)
        elif req.kind == "abort":
            for k in req.keys:
                self.pending[k].pop(t.tid, None)
        return True

    def install(self, t, keys, ts):
        for k in keys:                                                                # @line L10
            self.versions[k].append((ts, t.writes[k], t.tid))
            self.pending[k].pop(t.tid, None)

    # -------------------------------------------------------- coordinator
    def coordinator(self, t):
        """A generator. It yields a list of requests and gets their replies,
        or yields ("sleep", ticks) or ("down", ticks)."""
        o = t.origin
        t.snapshot = self.parts[o].read_clock(self.tick) - self.delta                  # @line L1
        for k in t.read_keys:
            (v,) = yield [(self.place[k], Request("read", t, [k]))]
            t.reads[k] = v
        base = sum(t.reads.values())
        t.writes = {k: base + 100 * t.tid + i for i, k in enumerate(t.write_keys)}
        if not t.writes:                                                              # @line L5
            t.status = "committed"
            return
        by_part = {}
        for k in t.write_keys:
            by_part.setdefault(self.place[k], []).append(k)
        if len(by_part) == 1:
            (q, keys), = by_part.items()
            (ts,) = yield [(q, Request("local", t, keys))]
            t.status, t.commit = ("committed", ts) if ts is not None else ("aborted", None)
            return
        parts = sorted(by_part)
        votes = yield [(q, Request("prepare", t, by_part[q])) for q in parts]          # @line L7
        if votes is not None and None not in votes:
            t.commit = (max if self.checks["max"] else min)(votes)                     # @line L9
            yield ("sleep", self.log_delay)          # the decision is logged
            t.status = "committed"
            if self.crash == (t.tid, "decided"):
                yield ("down", self.down_ticks)
            for q in parts:
                self.send(o, q, Request("commit", t, by_part[q], t.commit))
        else:
            t.status = "aborted"                                                      # @line L11
            for q in parts:
                self.send(o, q, Request("abort", t, by_part[q]))

    def resume(self, tid, value):
        gen = self.coord[tid][0]
        try:
            out = gen.send(value)
        except StopIteration:
            del self.coord[tid]
            return
        me = ("coord", tid)
        if out[0] == "sleep":
            self.coord[tid] = [gen, 1, []]
            self.send(None, me, ("wake",), out[1])
        elif out[0] == "down":
            self.coord[tid] = [gen, 1, []]
            self.down.add(tid)
            self.send(None, me, ("recover",), out[1])
        else:
            self.coord[tid] = [gen, len(out), [None] * len(out)]
            self.coord[tid].append(0)
            for i, (q, req) in enumerate(out):
                req.index = i
                self.send(self.txn[tid].origin, q, req)
            if self.crash == (tid, "prepare") and out[0][1].kind == "prepare":
                self.down.add(tid)               # it crashes before the votes arrive
                self.send(None, me, ("recover",), self.down_ticks)

    def to_coordinator(self, tid, payload):
        if tid not in self.coord:
            return
        entry = self.coord[tid]
        if payload[0] == "recover":
            self.down.discard(tid)
            # A vote that arrived while it was down is lost, and nothing in
            # the log says commit, so the transaction aborts.
            self.resume(tid, None)
        elif tid in self.down:
            return
        elif payload[0] == "wake":
            self.resume(tid, None)
        else:
            _, i, value = payload
            entry[2][i] = value
            entry[3] += 1
            if entry[3] == entry[1]:
                self.resume(tid, entry[2])

    # ---------------------------------------------------------------- run
    def run(self, txns, crash=None, down_ticks=6, limit=5000):
        """crash: None, or (tid, "prepare") or (tid, "decided")."""
        self.crash, self.down_ticks = crash, down_ticks
        self.txn = {t.tid: t for t in txns}
        todo = sorted(txns, key=lambda t: (t.start, t.tid))
        while todo or self.coord or self.net or any(p.queue for p in self.parts):
            while todo and todo[0].start <= self.tick:
                t = todo.pop(0)
                self.coord[t.tid] = [self.coordinator(t)]
                self.resume(t.tid, None)
            progress = True
            while progress:
                progress = False
                due = sorted((m for m in self.net if m[0] <= self.tick), key=lambda m: m[1])
                self.net = [m for m in self.net if m[0] > self.tick]
                for _, _, dst, payload in due:
                    progress = True
                    if isinstance(dst, tuple):
                        self.to_coordinator(dst[1], payload)
                    else:
                        self.parts[dst].queue.append(payload)
                for part in self.parts:
                    waiting = []
                    for req in part.queue:
                        if self.try_request(part.pid, req):
                            progress = True
                        else:
                            waiting.append(req)
                    part.queue = waiting
            self.tick += 1
            assert self.tick < limit, "no progress"
        return self.tick

    def state(self):
        return {k: max(vs)[1] for k, vs in self.versions.items()}
