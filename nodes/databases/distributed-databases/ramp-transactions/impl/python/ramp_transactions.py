# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ramp-transactions/. The authors are listed in prov/1YZCSM.jsonl.
"""RAMP-Fast and RAMP-Small read atomic multi-partition transactions.

A small simulation in one thread of the algorithms of Bailis, Fekete,
Hellerstein, Ghodsi and Stoica (SIGMOD 2014). Each key lives on one
partition. A writer prepares a new version of each key it writes, and only
when all partitions have acknowledged does it tell them to commit. A reader
first asks each partition for its last committed version, and then, if the
metadata shows that it missed a version of a sibling write, asks again for
that exact version.

Clients and partitions exchange messages through a network that delivers
them in an order chosen by a seeded random.Random. A writer can crash
after any step; a crashed writer sends nothing more. Every operation that
starts also finishes, because no step waits for another transaction.

mode = "fast"   RAMP-F: versions carry the set of sibling keys.
mode = "small"  RAMP-S: versions carry no metadata; a reader always asks
                again, with the set of timestamps it saw in the first round.
mode = "naive"  one round of reads of the last committed versions; this
                is not read atomic, and the tests show it.
"""

BOTTOM = (0, 0)      # the timestamp of the initial versions


class Partition:
    def __init__(self, keys):
        self.versions = {k: {BOTTOM: (0, frozenset())} for k in keys}   # key -> ts -> (value, md)
        self.last_commit = {k: BOTTOM for k in keys}

    def prepare(self, key, ts, value, md):
        self.versions[key][ts] = (value, md)                  # @line L9

    def commit(self, key, ts):
        if ts > self.last_commit[key]:                        # @line L10
            self.last_commit[key] = ts

    def get(self, key, ts_req):
        if ts_req is None:                                    # @line L11
            ts = self.last_commit[key]
        else:
            ts = ts_req
        value, md = self.versions[key][ts]
        return ts, value, md

    def get_small(self, key, ts_set):
        """RAMP-S second round: the version with the highest timestamp in
        ts_set that this partition has. The timestamp that the reader saw
        here in the first round is in ts_set, so there is one."""
        ts = max(t for t in self.versions[key] if t in ts_set)
        return ts, self.versions[key][ts][0], frozenset()


class Writer:
    def __init__(self, cid, seq, writes):
        self.cid = cid
        self.ts = (seq, cid)                                  # @line L1
        self.writes = dict(writes)
        self.state = "new"           # new, preparing, committing, done, crashed
        self.acks = set()
        self.rounds = 0


class Reader:
    def __init__(self, cid, keys):
        self.cid = cid
        self.keys = sorted(keys)
        self.state = "new"           # new, round1, round2, done
        self.ret = {}
        self.wait = set()
        self.rounds = 0


class RampDB:
    def __init__(self, placement, mode="fast"):
        """placement: {key: partition name}."""
        self.placement = dict(placement)
        self.mode = mode
        names = sorted(set(placement.values()))
        self.parts = {p: Partition([k for k in placement if placement[k] == p]) for p in names}
        self.clients = {}
        self.net = []                # (dst, payload); clients and partitions are named
        self.messages = 0
        self.log = []                # (event, ...) for the tests

    def send(self, dst, payload):
        self.messages += 1
        self.net.append((dst, payload))

    # ------------------------------------------------------------ writers
    def put_all(self, cid, seq, writes):
        if cid in self.clients and self.clients[cid].state == "crashed":
            return
        w = Writer(cid, seq, writes)
        self.clients[cid] = w
        w.state = "preparing"
        w.rounds = 1
        for k in sorted(w.writes):                            # @line L2
            md = frozenset(w.writes) - {k} if self.mode == "fast" else frozenset()
            self.send(self.placement[k], ("prepare", cid, k, w.ts, w.writes[k], md))

    def on_prepared(self, w, key):
        if w.state != "preparing":
            return
        w.acks.add(key)
        if w.acks == set(w.writes):                           # @line L3
            w.state = "committing"
            w.rounds = 2
            self.log.append(("commit", w.ts, tuple(sorted(w.writes))))
            w.acks = set()
            for k in sorted(w.writes):                        # @line L4
                self.send(self.placement[k], ("commit", w.cid, k, w.ts))

    def on_committed(self, w, key):
        if w.state != "committing":
            return
        w.acks.add(key)
        if w.acks == set(w.writes):
            w.state = "done"

    def crash(self, cid):
        if cid not in self.clients:          # it crashes before it starts
            self.clients[cid] = Writer(cid, 0, {})
        c = self.clients[cid]
        if c.state != "done":
            c.state = "crashed"
        self.net = [m for m in self.net if not (m[0] == cid)]

    # ------------------------------------------------------------ readers
    def get_all(self, cid, keys):
        r = Reader(cid, keys)
        self.clients[cid] = r
        r.state = "round1"
        r.rounds = 1
        r.wait = set(r.keys)
        for k in r.keys:                                      # @line L5
            self.send(self.placement[k], ("get", cid, k, None))

    def on_value(self, r, key, ts, value, md):
        r.ret[key] = (ts, value, md)
        r.wait.discard(key)
        if r.wait:
            return
        if r.state == "round1" and self.mode == "fast":
            v_latest = {}
            for k in r.keys:                                  # @line L6
                ts_k, _, md_k = r.ret[k]
                for y in md_k:
                    if y in r.ret and ts_k > v_latest.get(y, BOTTOM):
                        v_latest[y] = ts_k
            need = [k for k in r.keys if v_latest.get(k, BOTTOM) > r.ret[k][0]]
            if need:
                r.state, r.rounds, r.wait = "round2", 2, set(need)
                for k in need:                                # @line L7
                    self.send(self.placement[k], ("get", r.cid, k, v_latest[k]))
                return
        elif r.state == "round1" and self.mode == "small":
            ts_set = frozenset(r.ret[k][0] for k in r.keys)
            r.state, r.rounds, r.wait = "round2", 2, set(r.keys)
            for k in r.keys:
                self.send(self.placement[k], ("get_small", r.cid, k, ts_set))
            return
        r.state = "done"                                      # @line L8
        self.log.append(("read", r.cid, {k: r.ret[k][0] for k in r.keys}))

    # ------------------------------------------------------------ network
    def deliver(self, k):
        dst, payload = self.net.pop(k)
        kind, cid = payload[0], payload[1]
        if dst in self.parts:
            part = self.parts[dst]
            if kind == "prepare":
                _, _, key, ts, value, md = payload
                part.prepare(key, ts, value, md)
                self.send(cid, ("prepared", key))
            elif kind == "commit":
                _, _, key, ts = payload
                part.commit(key, ts)
                self.send(cid, ("committed", key))
            elif kind == "get":
                _, _, key, ts_req = payload
                self.send(cid, ("value", key) + part.get(key, ts_req))
            else:
                _, _, key, ts_set = payload
                self.send(cid, ("value", key) + part.get_small(key, ts_set))
            return
        c = self.clients[dst]
        if c.state == "crashed":
            return
        if kind == "prepared":
            self.on_prepared(c, payload[1])
        elif kind == "committed":
            self.on_committed(c, payload[1])
        else:
            self.on_value(c, *payload[1:])

    def run(self, rng, ops, crash_at=()):
        """ops: [(step, "w", cid, seq, writes) or (step, "r", cid, keys)].
        crash_at: [(step, cid)]. Delivers until no message is left."""
        events = sorted([(o[0], 0, o) for o in ops] + [(s, 1, ("crash", c)) for s, c in crash_at],
                        key=lambda e: (e[0], e[1], str(e[2])))
        step = 0
        while events or self.net:
            while events and events[0][0] <= step:
                _, _, o = events.pop(0)
                if o[0] == "crash":
                    self.crash(o[1])
                elif o[1] == "w":
                    self.put_all(o[2], o[3], o[4])
                else:
                    self.get_all(o[2], o[3])
            if self.net:
                self.deliver(rng.randrange(len(self.net)))
            step += 1
