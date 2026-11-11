# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hotstuff/. The authors are listed in prov/XGV05H.jsonl.

"""Basic HotStuff (Yin, Malkhi, Reiter, Golan Gueta and Abraham, PODC 2019).

n = 3f + 1 replicas build a tree of nodes. In each view the leader extends
the highest prepareQC it learns from n - f NEW-VIEW messages, and three
phases of votes (prepare, pre-commit, commit) each give a quorum certificate.
A replica locks on the precommitQC and executes the branch of a commitQC.

A quorum certificate is a threshold signature: n - f partial signatures on
the same (phase, view, node) combine into one token of constant size. Tokens
cannot be forged, since only Net.partial and Net.combine make them.

The network is a discrete-event simulation with a global stabilization time
(GST): before GST a seeded adversary picks delays in [1, pre], after GST every
delay is at most delta. The paper leaves the pacemaker open; this one moves to
the next view on a timeout that doubles, and lets a replica join view w + 1
when f + 1 others timed out in view w, or jump to view w when the leader of w
sends a valid message.
"""

import heapq
import random

GENESIS = ("genesis", None)  # a node is (command, parent node)


def extends(node, anc):
    while node is not None:
        if node == anc:
            return True
        node = node[1]
    return False


def branch(node):
    out = []
    while node is not None and node != GENESIS:
        out.append(node[0])
        node = node[1]
    return out[::-1]


class Net:
    def __init__(self, n, f, gst, pre, delta, seed):
        self.n, self.f, self.gst, self.pre, self.delta = n, f, gst, pre, delta
        self.rng = random.Random(seed)
        self.q, self.k, self.now = [], 0, 0
        self.tokens = set()
        self.sent = {"normal": 0, "timeout": 0}
        self.honest_ids = set()
        self.genesis_qc = ("qc", ("prepare", 0, GENESIS))
        self.tokens.add(self.genesis_qc)

    def partial(self, i, content):
        tok = ("ps", i, content)
        self.tokens.add(tok)
        return tok

    def combine(self, shares):
        if len({s[2] for s in shares}) != 1 or not all(s in self.tokens for s in shares):
            return None
        if len({s[1] for s in shares}) < self.n - self.f:
            return None
        qc = ("qc", shares[0][2])
        self.tokens.add(qc)
        return qc

    def ok(self, tok):
        return tok in self.tokens

    def send(self, src, dst, msg, kind="normal"):
        if src in self.honest_ids:
            self.sent[kind] += 1
        d = self.rng.randint(1, self.pre if self.now < self.gst else self.delta)
        self.k += 1
        heapq.heappush(self.q, (self.now + d, self.k, dst, src, msg))


def qc_view(qc):
    return qc[1][1]


def qc_node(qc):
    return qc[1][2]


class Replica:
    def __init__(self, i, n, f, net, reqs, base=30, byz=None, reps=None):
        self.i, self.n, self.f, self.net, self.reqs = i, n, f, net, reqs
        self.byz, self.reps = byz, reps
        self.view = 0
        self.locked = self.high = net.genesis_qc  # lockedQC and prepareQC
        self.voted = set()
        self.log = []
        self.violation = False
        self.nv, self.votes, self.tos = {}, {}, {}
        self.proposed, self.formed = set(), set()
        self.base = self.timeout = base
        self.deadline = base
        self.timed_out = 0  # the last view this replica gave up on

    def leader(self, v):
        return v % self.n

    def send(self, dst, msg, kind="normal"):
        if dst == self.i:
            self.receive(self.i, msg)
        else:
            self.net.send(self.i, dst, msg, kind)

    def bcast(self, msg, kind="normal", to=None):
        for d in (range(self.n) if to is None else to):
            self.send(d, msg, kind)

    # ---- pacemaker -----------------------------------------------------------
    def enter(self, w):
        if w <= self.view:
            return
        self.view = w
        self.deadline = self.net.now + self.timeout
        self.send(self.leader(w), ("NEWVIEW", w, self.high))  # @line L1

    def tick(self):
        if self.net.now >= self.deadline and self.timed_out < self.view:
            self.send_timeout(self.view)

    def send_timeout(self, w):
        self.timed_out = w
        self.timeout *= 2
        self.bcast(("TIMEOUT", w), "timeout")  # @line L11

    def on_timeout(self, src, w):
        if w < self.view:
            return
        box = self.tos.setdefault(w, set())
        box.add(src)
        if len(box - {self.i}) >= self.f + 1 and self.timed_out < w:
            self.send_timeout(w)  # join: f + 1 others gave up on view w
        if len(box) >= 2 * self.f + 1:
            self.enter(w + 1)  # a timeout certificate for view w

    # ---- leader --------------------------------------------------------------
    def try_lead(self, v):
        box = self.nv.get(v, {})
        if v != self.view or v in self.proposed or len(box) < self.n - self.f:
            return
        self.proposed.add(v)
        high = max(box.values(), key=qc_view)
        done = set(branch(qc_node(high)))
        cmd = next((r for r in self.reqs if r not in done), "noop%d" % v)
        if self.byz == "fork":
            high = self.net.genesis_qc
            cmd = "fork%d" % v
        if self.byz == "equivocate":
            for d in range(self.n):
                node = (cmd if d % 2 else "evil%d" % v, qc_node(high))
                self.send(d, ("PREPARE", v, node, high))
            return
        node = (cmd, qc_node(high))
        self.bcast(("PREPARE", v, node, high))  # @line L2

    def on_vote(self, share):
        if not self.net.ok(share):
            return
        phase, v, node = share[2]
        if self.leader(v) != self.i:
            return
        box = self.votes.setdefault(share[2], {})
        box[share[1]] = share
        if len(box) >= self.n - self.f and share[2] not in self.formed:
            self.formed.add(share[2])
            qc = self.net.combine(list(box.values()))
            to = None
            if self.byz == "fork":  # show the certificate to one honest replica only
                hon = sorted(self.net.honest_ids)
                to = [hon[self.net.rng.randrange(len(hon))]]
            if phase == "prepare":
                self.bcast(("PRECOMMIT", v, qc), to=to)  # @line L5
            elif phase == "pre-commit":
                self.bcast(("COMMIT", v, qc), to=to)  # @line L7
            else:
                self.bcast(("DECIDE", v, qc), to=to)  # @line L9

    # ---- replica -------------------------------------------------------------
    def vote(self, phase, v, node):
        if self.byz is None:
            if (phase, v) in self.voted:
                return
            self.voted.add((phase, v))
        self.send(self.leader(v), ("VOTE", self.net.partial(self.i, (phase, v, node))))

    def safe_node(self, node, qc):
        return extends(node, qc_node(self.locked)) or qc_view(qc) > qc_view(self.locked)  # @line L4

    def on_prepare(self, src, v, node, qc):
        if src != self.leader(v) or not self.net.ok(qc) or qc[1][0] != "prepare" or qc_view(qc) >= v:
            return
        self.enter(v)
        if v != self.view or node[1] != qc_node(qc):
            return
        if self.byz is not None or self.safe_node(node, qc):
            self.vote("prepare", v, node)  # @line L3

    def on_phase(self, src, kind, v, qc):
        want = {"PRECOMMIT": "prepare", "COMMIT": "pre-commit", "DECIDE": "commit"}[kind]
        if src != self.leader(v) or not self.net.ok(qc) or qc[1][0] != want or qc_view(qc) != v:
            return
        node = qc_node(qc)
        if kind == "DECIDE":
            b = branch(node)  # @line L10
            if b[: len(self.log)] != self.log and self.log[: len(b)] != b:
                self.violation = True
            if len(b) > len(self.log):
                self.log = b
            if v >= self.view:
                self.timeout = self.base
                self.enter(v + 1)
            return
        self.enter(v)
        if v != self.view:
            return
        if kind == "PRECOMMIT":
            if qc_view(qc) > qc_view(self.high):
                self.high = qc
            self.vote("pre-commit", v, node)  # @line L6
        else:
            self.locked = qc
            self.vote("commit", v, node)  # @line L8

    def receive(self, src, msg):
        if self.byz == "silent":
            return
        kind = msg[0]
        if kind == "NEWVIEW":
            _, v, qc = msg
            if self.net.ok(qc) and qc[1][0] == "prepare" and self.leader(v) == self.i and v >= self.view:
                self.nv.setdefault(v, {})[src] = qc
                self.try_lead(v)
        elif kind == "PREPARE":
            self.on_prepare(src, msg[1], msg[2], msg[3])
        elif kind == "VOTE":
            self.on_vote(msg[1])
        elif kind == "TIMEOUT":
            self.on_timeout(src, msg[1])
        else:
            self.on_phase(src, kind, msg[1], msg[2])
        self.try_lead(self.view)


def run(n, f, faulty, strategy, requests=5, gst=60, pre=25, delta=2, seed=0, horizon=6000):
    """Simulate until every honest replica executed every request, or the
    horizon. Returns the logs, the views, the time and the message counts."""
    net = Net(n, f, gst, pre, delta, seed)
    reqs = ["r%d" % k for k in range(requests)]
    reps = []
    for i in range(n):
        reps.append(Replica(i, n, f, net, reqs, byz=(strategy if i in faulty else None), reps=reps))
    net.honest_ids = {i for i in range(n) if i not in faulty}
    honest = sorted(net.honest_ids)
    net.now = 0
    for i in range(n):
        if strategy != "silent" or i not in faulty:
            reps[i].enter(1)
    t = 0
    while t < horizon:
        while net.q and net.q[0][0] <= t:
            _, _, dst, src, msg = heapq.heappop(net.q)
            net.now = t
            reps[dst].receive(src, msg)
        net.now = t
        for i in range(n):
            if i not in faulty or strategy != "silent":
                reps[i].tick()
        if t >= gst and all(set(reqs) <= set(reps[i].log) for i in honest):
            break
        t += 1
    return {
        "logs": {i: list(reps[i].log) for i in honest},
        "violation": any(reps[i].violation for i in honest),
        "views": {i: reps[i].view for i in honest},
        "time": t,
        "sent": dict(net.sent),
        "requests": reqs,
    }


def check(res):
    """Safety: honest logs are prefixes of one another. Liveness: every
    honest replica executed every request."""
    bad = []
    logs = list(res["logs"].values())
    if res["violation"] or any(a[: len(b)] != b[: len(a)] for a in logs for b in logs):
        bad.append("safety")
    if not all(set(res["requests"]) <= set(log) for log in logs):
        bad.append("liveness")
    return bad


STRATEGIES = ("silent", "equivocate", "fork")


if __name__ == "__main__":
    for strat in STRATEGIES:
        res = run(4, 1, {1}, strat, seed=1)
        print(strat, check(res), res["views"], res["time"], res["sent"])
