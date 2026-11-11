# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pbft/. The authors are listed in prov/VDRRCB.jsonl.

"""PBFT (Castro and Liskov 1999, 2002) in a partially synchronous network.

n = 3f + 1 replicas order client requests by sequence number with the
three phases PRE-PREPARE, PREPARE and COMMIT, take checkpoints that move
the low watermark h, and replace a faulty or slow primary by a view change
with VIEW-CHANGE and NEW-VIEW messages.

The network is a discrete-event simulation. Before the global stabilization
time GST a seeded adversary picks message delays in [1, pre]; from GST on,
every delay is at most delta. Signatures are unforgeable tokens: a replica
can only sign as itself, and a token is valid only if it was made by sign().
Faulty replicas run the code with Byzantine changes chosen by a strategy.
"""

import heapq
import random


class Net:
    def __init__(self, n, gst, pre, delta, seed):
        self.n, self.gst, self.pre, self.delta = n, gst, pre, delta
        self.rng = random.Random(seed)
        self.q, self.k, self.now = [], 0, 0
        self.tokens = set()
        self.sent = {"normal": 0, "view": 0}
        self.honest_ids = set()

    def sign(self, i, content):
        tok = ("sig", i, content)
        self.tokens.add(tok)
        return tok

    def ok(self, tok):
        return isinstance(tok, tuple) and len(tok) == 3 and tok in self.tokens

    def send(self, src, dst, msg, kind="normal"):
        if src in self.honest_ids:
            self.sent[kind] += 1
        if self.now < self.gst:
            d = self.rng.randint(1, self.pre)
        else:
            d = self.rng.randint(1, self.delta)
        self.k += 1
        heapq.heappush(self.q, (self.now + d, self.k, dst, src, msg))

    def bcast(self, src, msg, kind="normal"):
        for d in range(self.n):
            if d != src:
                self.send(src, d, msg, kind)


class Replica:
    def __init__(self, i, n, f, net, requests, K=4, L=8, timeout=20, byz=None):
        self.i, self.n, self.f, self.net = i, n, f, net
        self.K, self.L, self.timeout = K, L, timeout
        self.byz = byz  # None for honest, else a strategy name
        self.view, self.vc_target = 0, None  # vc_target set while changing view
        self.h = 0
        self.ckpt_proof = []
        self.pp = {}  # (v, s) -> signed pre-prepare
        self.prep = {}  # (v, s, d) -> {j: signed prepare}
        self.comm = {}  # (v, s, d) -> {j: signed commit}
        self.prepared = {}  # s -> (v, d, pp, [prepares]), the highest view
        self.committed = {}  # s -> d
        self.executed = []  # list of (s, d); the state
        self.ck = {}  # (s, state) -> {j: signed checkpoint}
        self.vcs = {}  # target view -> {j: signed view-change}
        self.pending = list(requests)
        self.next_s = 0
        self.deadline = timeout
        self.sent_nv = set()
        self.future = []

    def primary(self, v):
        return v % self.n

    def state(self, upto=None):
        return tuple((s, d) for s, d in self.executed if upto is None or s <= upto)

    # ---- normal case ---------------------------------------------------------
    def propose(self):
        v = self.view
        if self.vc_target is not None or self.primary(v) != self.i or self.byz == "silent":
            return
        done = {d for _, d in self.executed} | {self.pp[k][2][3] for k in self.pp if k[0] == v}
        for m in self.pending:
            if m in done:
                continue
            s = max(self.next_s, self.h) + 1
            if s > self.h + self.L:
                return
            self.next_s = s
            if self.byz == "equivocate":
                other = "x%d" % s
                for d in range(self.n):
                    pp = self.net.sign(self.i, ("PP", v, s, m if d % 2 else other))
                    if d != self.i:
                        self.net.send(self.i, d, pp)
                self.pp[(v, s)] = self.net.sign(self.i, ("PP", v, s, m))
                continue
            pp = self.net.sign(self.i, ("PP", v, s, m))
            self.pp[(v, s)] = pp
            self.net.bcast(self.i, pp)  # @line L1
            done.add(m)

    def on_pp(self, pp):
        _, v, s, d = pp[2]
        if pp[1] != self.primary(v) or v != self.view or self.vc_target is not None:
            return
        if not (self.h < s <= self.h + self.L):
            return
        if (v, s) in self.pp and self.pp[(v, s)][2] != pp[2]:
            return
        self.pp[(v, s)] = pp
        if self.i != self.primary(v):
            dd = d if self.byz != "equivocate" else "y%d" % s
            p = self.net.sign(self.i, ("P", v, s, dd, self.i))
            self.prep.setdefault((v, s, dd), {})[self.i] = p
            self.net.bcast(self.i, p)  # @line L2
        self.check(v, s, d)

    def on_vote(self, msg):
        kind, v, s, d, j = msg[2]
        if j != msg[1]:
            return
        box = self.prep if kind == "P" else self.comm
        box.setdefault((v, s, d), {})[j] = msg
        self.check(v, s, d)

    def is_prepared(self, v, s, d):
        pp = self.pp.get((v, s))
        if pp is None or pp[2][3] != d:
            return False
        backups = [j for j in self.prep.get((v, s, d), {}) if j != self.primary(v)]
        return len(backups) >= 2 * self.f  # @line L3

    def check(self, v, s, d):
        if v != self.view or s <= self.h or self.vc_target is not None:
            return  # a replica that sent VIEW-CHANGE takes no part in view v
        if self.is_prepared(v, s, d):
            old = self.prepared.get(s)
            if old is None or old[0] < v:
                ps = [m for j, m in self.prep[(v, s, d)].items() if j != self.primary(v)][: 2 * self.f]
                self.prepared[s] = (v, d, self.pp[(v, s)], ps)
                dd = d if self.byz != "equivocate" else "z%d" % s
                c = self.net.sign(self.i, ("C", v, s, dd, self.i))
                self.comm.setdefault((v, s, dd), {})[self.i] = c
                self.net.bcast(self.i, c)  # @line L4
            if len(self.comm.get((v, s, d), {})) >= 2 * self.f + 1 and s not in self.committed:
                self.committed[s] = d  # @line L5
                self.execute()

    def execute(self):
        last = self.executed[-1][0] if self.executed else 0
        while last + 1 in self.committed:
            last += 1
            d = self.committed[last]
            self.executed.append((last, d))  # @line L6
            if d in self.pending:
                self.pending.remove(d)
            self.deadline = self.net.now + self.timeout
            if last % self.K == 0:
                c = self.net.sign(self.i, ("CK", last, self.state(last), self.i))
                self.on_ck(c)
                self.net.bcast(self.i, c)  # @line L7

    def on_ck(self, c):
        _, s, st, j = c[2]
        if j != c[1]:
            return
        box = self.ck.setdefault((s, st), {})
        box[j] = c
        if len(box) >= 2 * self.f + 1 and s > self.h:
            self.h = s
            self.ckpt_proof = list(box.values())[: 2 * self.f + 1]
            if (self.executed[-1][0] if self.executed else 0) < s:
                self.executed = list(st)  # state transfer from the stable checkpoint
                for _, d in st:
                    if d in self.pending:
                        self.pending.remove(d)
            for k in [k for k in self.pp if k[1] <= s]:
                del self.pp[k]
            for s2 in [x for x in self.prepared if x <= s]:
                del self.prepared[s2]

    # ---- view change ---------------------------------------------------------
    def tick(self):
        if not self.pending and self.vc_target is None:
            return
        if self.net.now >= self.deadline:
            self.start_vc((self.vc_target or self.view) + 1)

    def start_vc(self, target):
        self.vc_target = target
        self.timeout *= 2
        self.deadline = self.net.now + self.timeout
        P = [] if self.byz == "hide" else [self.prepared[s] for s in sorted(self.prepared) if s > self.h]
        vc = self.net.sign(self.i, ("VC", target, self.h, tuple(self.ckpt_proof), tuple((v, d, pp, tuple(ps)) for v, d, pp, ps in P), self.i))
        self.on_vc(vc)
        self.net.bcast(self.i, vc, "view")  # @line L8

    def valid_vc(self, vc):
        if not self.net.ok(vc) or vc[2][0] != "VC" or vc[2][5] != vc[1]:
            return False
        _, target, h, C, P, j = vc[2]
        if h > 0:
            sts = {c[2][2] for c in C}
            if len({c[1] for c in C if self.net.ok(c) and c[2][1] == h}) < 2 * self.f + 1 or len(sts) != 1:
                return False
        for v, d, pp, ps in P:
            if v >= target or not self.net.ok(pp) or pp[2] != ("PP", v, pp[2][2], d) or pp[1] != self.primary(v):
                return False
            s = pp[2][2]
            good = {p[1] for p in ps if self.net.ok(p) and p[2] == ("P", v, s, d, p[1]) and p[1] != self.primary(v)}
            if len(good) < 2 * self.f or s <= h:
                return False
        return True

    def on_vc(self, vc):
        if not self.valid_vc(vc):
            return
        target = vc[2][1]
        if target <= self.view:
            return
        self.vcs.setdefault(target, {})[vc[1]] = vc
        # join a view change that f + 1 other replicas already started
        higher = {j for t, box in self.vcs.items() if t > (self.vc_target or self.view) for j in box} - {self.i}
        if len(higher) >= self.f + 1:
            self.start_vc(min(t for t, box in self.vcs.items() if t > (self.vc_target or self.view)))
        if self.primary(target) == self.i and len(self.vcs[target]) >= 2 * self.f + 1 and target not in self.sent_nv:
            self.send_nv(target)

    def compute_O(self, target, V):
        min_s = max(vc[2][2] for vc in V)
        best = {}
        for vc in V:
            for v, d, pp, ps in vc[2][4]:
                s = pp[2][2]
                if s > min_s and (s not in best or best[s][0] < v):
                    best[s] = (v, d)
        max_s = max(best) if best else min_s
        return min_s, [(s, best[s][1] if s in best else "null") for s in range(min_s + 1, max_s + 1)]

    def send_nv(self, target):
        self.sent_nv.add(target)
        vcs = list(self.vcs[target].values())
        subsets = [vcs[: 2 * self.f + 1]]
        if self.byz == "equivocate" and len(vcs) > 2 * self.f + 1:
            subsets.append(vcs[-(2 * self.f + 1):])
        for d in range(self.n):
            V = tuple(subsets[d % len(subsets)])
            _, O = self.compute_O(target, V)
            Opp = tuple(self.net.sign(self.i, ("PP", target, s, m)) for s, m in O)
            nv = self.net.sign(self.i, ("NV", target, V, Opp))
            if d == self.i:
                self.on_nv(nv)
            else:
                self.net.send(self.i, d, nv, "view")  # @line L9

    def on_nv(self, nv):
        _, target, V, Opp = nv[2]
        if nv[1] != self.primary(target) or target <= self.view:
            return
        if len({vc[1] for vc in V}) < 2 * self.f + 1 or not all(self.valid_vc(vc) and vc[2][1] == target for vc in V):
            return
        min_s, O = self.compute_O(target, V)
        if [(pp[2][2], pp[2][3]) for pp in Opp] != O or not all(self.net.ok(pp) and pp[1] == nv[1] for pp in Opp):
            return
        if min_s > self.h:  # bring the state up to the checkpoint in V
            for vc in V:
                if vc[2][2] == min_s:
                    for c in vc[2][3]:
                        self.on_ck(c)
                    break
        self.view, self.vc_target = target, None  # @line L10
        self.deadline = self.net.now + self.timeout
        self.next_s = max([min_s] + [s for s, _ in O])
        for pp in Opp:
            self.on_pp(pp)
        later, self.future = self.future, []
        for m in later:
            self.receive(m[1], m)
        self.propose()

    # ---- dispatch ------------------------------------------------------------
    def receive(self, src, msg):
        if self.byz == "silent" or not self.net.ok(msg):
            return
        kind = msg[2][0]
        if kind in ("PP", "P", "C") and msg[2][1] > self.view:
            self.future.append(msg)  # keep messages of a later view until NEW-VIEW
            return
        if kind == "PP":
            self.on_pp(msg)
        elif kind in ("P", "C"):
            self.on_vote(msg)
        elif kind == "CK":
            self.on_ck(msg)
        elif kind == "VC":
            self.on_vc(msg)
        elif kind == "NV":
            self.on_nv(msg)
        self.propose()


def run(n, f, faulty, strategy, requests=6, gst=60, pre=25, delta=2, seed=0, horizon=4000, K=4, L=8):
    """Simulate until every honest replica executed every request, or the
    horizon. Returns the executed logs, the views and the message counts."""
    net = Net(n, gst, pre, delta, seed)
    reqs = ["r%d" % k for k in range(requests)]
    reps = [Replica(i, n, f, net, reqs, K, L, byz=(strategy if i in faulty else None)) for i in range(n)]
    net.honest_ids = {i for i in range(n) if i not in faulty}
    honest = sorted(net.honest_ids)
    for r in reps:
        r.propose()
    t, done_at = 0, None
    while t < horizon:
        while net.q and net.q[0][0] <= t:
            _, _, dst, src, msg = heapq.heappop(net.q)
            net.now = t
            reps[dst].receive(src, msg)
        net.now = t
        for i in honest:
            reps[i].tick()
        for i in faulty:
            if strategy != "silent":
                reps[i].tick()
        if done_at is None and all(sum(1 for i in honest if r in {d for _, d in reps[i].executed}) >= f + 1 for r in reqs):
            done_at = t  # every client can now collect f + 1 matching replies
        if all(len({d for _, d in reps[i].executed} & set(reqs)) == len(reqs) for i in honest) and t >= gst:
            break
        t += 1
    return {"logs": {i: list(reps[i].executed) for i in honest}, "views": {i: reps[i].view for i in honest}, "time": t, "done_at": done_at, "sent": dict(net.sent), "requests": reqs}


def check(res, f):
    """Safety: no two honest replicas execute different requests at one
    sequence number. Liveness: each request is executed by at least f + 1
    honest replicas, so its client gets f + 1 matching replies. (A replica
    that fell behind catches up at the next stable checkpoint.)"""
    bad = []
    at = {}
    for log in res["logs"].values():
        for s, d in log:
            at.setdefault(s, set()).add(d)
    if any(len(ds) > 1 for ds in at.values()):
        bad.append("safety")
    for r in res["requests"]:
        if sum(1 for log in res["logs"].values() if r in {d for _, d in log}) < f + 1:
            bad.append("liveness")
            break
    return bad


STRATEGIES = ("silent", "equivocate", "hide")


if __name__ == "__main__":
    for strat in STRATEGIES:
        res = run(4, 1, {0}, strat, seed=1)
        print(strat, check(res, 1), res["views"], res["time"], res["sent"])
