# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aodv/. The authors are listed in prov/NQ1A74.jsonl.
"""AODV route discovery and maintenance in an asynchronous message-passing model.

Each directed link is a FIFO queue. A scheduler driven by a seeded random generator
picks a nonempty queue and delivers its first message. Removing a link drops the
messages on it. Both ends of a link see its failure at once.

A route entry is [next hop, hops, seq, valid]. Sequence numbers start at 0, and a
requested sequence number of 0 means unknown.
"""

from collections import deque

NEXT, HOPS, SEQ, VALID = 0, 1, 2, 3


class AODV:
    def __init__(self, n, links, rng):
        self.n = n
        self.adj = [set() for _ in range(n)]
        for u, v in links:
            self.adj[u].add(v)
            self.adj[v].add(u)
        self.rng = rng
        self.seq = [0] * n  # own sequence number of each node
        self.table = [dict() for _ in range(n)]  # table[u][d] = [next, hops, seq, valid]
        self.seen = [set() for _ in range(n)]  # (originator, request id) pairs seen
        self.rreq_id = [0] * n
        self.queues = {}  # (u, v) -> deque of messages from u to v
        self.messages = 0

    # ----- links and sending -------------------------------------------------
    def send(self, u, v, msg):
        if v in self.adj[u]:
            self.queues.setdefault((u, v), deque()).append(msg)
            self.messages += 1

    def broadcast(self, u, msg):
        for v in sorted(self.adj[u]):
            self.send(u, v, msg)

    def add_link(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def remove_link(self, u, v):
        self.adj[u].discard(v)
        self.adj[v].discard(u)
        self.queues.pop((u, v), None)
        self.queues.pop((v, u), None)
        self.link_broken(u, v)
        self.link_broken(v, u)

    # ----- route entries -----------------------------------------------------
    @staticmethod
    def fresher(entry, seq, hops):
        """The update rule: a larger seq, or the same seq with fewer hops or an invalid entry."""
        if entry is None or seq > entry[SEQ]:
            return True
        return seq == entry[SEQ] and (not entry[VALID] or hops < entry[HOPS])

    def update(self, u, dest, nxt, hops, seq):
        if dest == u:
            return False
        e = self.table[u].get(dest)
        if not self.fresher(e, seq, hops):
            return False
        self.table[u][dest] = [nxt, hops, seq, True]
        return True

    def valid_route(self, u, dest):
        e = self.table[u].get(dest)
        return e if e is not None and e[VALID] else None

    # ----- the protocol ------------------------------------------------------
    def request(self, s, d):
        """s starts a route discovery for d."""
        self.seq[s] += 1  # @line L1 fresh own number, then flood the request
        self.rreq_id[s] += 1
        self.seen[s].add((s, self.rreq_id[s]))
        e = self.table[s].get(d)
        known = e[SEQ] if e is not None else 0
        self.broadcast(s, ("RREQ", s, self.seq[s], self.rreq_id[s], d, known, 0))

    def on_rreq(self, u, v, msg):
        _, orig, orig_seq, rid, dest, dest_seq, hops = msg
        if (orig, rid) in self.seen[u]:  # @line L2 drop a request seen before
            return
        self.seen[u].add((orig, rid))
        hops += 1
        self.update(u, orig, v, hops, orig_seq)  # @line L3 reverse route to the originator
        back = self.valid_route(u, orig)
        if u == dest:
            self.seq[u] = max(self.seq[u], dest_seq)  # @line L4 the destination answers
            if back is not None:
                self.send(u, back[NEXT], ("RREP", orig, dest, self.seq[u], 0))
            return
        e = self.valid_route(u, dest)
        if e is not None and e[SEQ] >= dest_seq:  # @line L5 an intermediate node with a fresh enough route answers
            if back is not None:
                self.send(u, back[NEXT], ("RREP", orig, dest, e[SEQ], e[HOPS]))
            return
        known = self.table[u][dest][SEQ] if dest in self.table[u] else 0
        self.broadcast(u, ("RREQ", orig, orig_seq, rid, dest, max(dest_seq, known), hops))  # @line L6

    def on_rrep(self, u, v, msg):
        _, orig, dest, dest_seq, hops = msg
        hops += 1
        if not self.update(u, dest, v, hops, dest_seq):  # @line L7 forward route to the destination
            return
        if u == orig:
            return
        back = self.valid_route(u, orig)
        if back is not None:  # @line L8 pass the reply on toward the originator
            self.send(u, back[NEXT], ("RREP", orig, dest, dest_seq, hops))

    def link_broken(self, u, v):
        lost = []
        for d, e in sorted(self.table[u].items()):
            if e[VALID] and e[NEXT] == v:
                e[VALID] = False
                e[SEQ] += 1  # @line L9 invalidate with a larger number and report it
                lost.append((d, e[SEQ]))
        if lost:
            self.broadcast(u, ("RERR", tuple(lost)))

    def on_rerr(self, u, v, msg):
        lost = []
        for d, r in msg[1]:
            e = self.table[u].get(d)
            if e is not None and e[VALID] and e[NEXT] == v:  # @line L10 only routes through the sender
                e[VALID] = False
                e[SEQ] = max(e[SEQ], r)
                lost.append((d, e[SEQ]))
        if lost:
            self.broadcast(u, ("RERR", tuple(lost)))

    def step(self):
        """Deliver one message. Return False when no message is in flight."""
        keys = sorted(k for k, q in self.queues.items() if q)
        if not keys:
            return False
        u, v = self.rng.choice(keys)
        msg = self.queues[(u, v)].popleft()
        {"RREQ": self.on_rreq, "RREP": self.on_rrep, "RERR": self.on_rerr}[msg[0]](v, u, msg)
        return True

    def run(self, max_steps=10 ** 6, check=None):
        steps = 0
        while steps < max_steps and self.step():
            steps += 1
            if check is not None:
                check(self)
        return steps

    # ----- inspection --------------------------------------------------------
    def state(self, j, dest):
        """(seq, hops, valid) of node j for dest; the destination itself counts as (own seq, 0, valid)."""
        if j == dest:
            return self.seq[j], 0, True
        e = self.table[j].get(dest)
        if e is None:
            return None
        return e[SEQ], e[HOPS], e[VALID]

    def invariant_violations(self):
        """Valid entries i -> j for d where j is not strictly ahead in (seq, -hops)."""
        bad = []
        for i in range(self.n):
            for d, e in self.table[i].items():
                if not e[VALID]:
                    continue
                st = self.state(e[NEXT], d)
                if st is None:
                    bad.append((i, d))
                    continue
                s_j, h_j, ok_j = st
                if not (s_j > e[SEQ] or (s_j == e[SEQ] and ok_j and h_j < e[HOPS])):
                    bad.append((i, d))
        return bad

    def has_loop(self):
        """True if, for some destination, following valid next hops revisits a node."""
        for d in range(self.n):
            for start in range(self.n):
                seen = set()
                u = start
                while u != d and u not in seen:
                    seen.add(u)
                    e = self.valid_route(u, d)
                    if e is None:
                        break
                    u = e[NEXT]
                else:
                    if u != d:
                        return True
        return False

    def route(self, s, d):
        """The path from s to d along valid entries over existing links, or None."""
        path = [s]
        u = s
        while u != d:
            e = self.valid_route(u, d)
            if e is None or e[NEXT] not in self.adj[u] or len(path) > self.n:
                return None
            u = e[NEXT]
            path.append(u)
        return path
