# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tendermint/. The authors are listed in prov/66KH53.jsonl.

"""Tendermint consensus, Algorithm 1 of Buchman, Kwon and Milosevic,
"The latest gossip on BFT consensus" (arXiv 1807.04938).

n = 3f + 1 processes decide one value per height. Each round has a proposer
and three steps: propose, prevote and precommit. A process locks on a value
when it sees a polka (2f + 1 prevotes for it) and precommits it; it decides
on a proposal with 2f + 1 precommits in one round. Timeouts grow with the
round number.

Messages are signed tokens (Net.sign); a token cannot be forged. Honest
processes gossip: they relay every new valid message once to all others, so
a message that reaches one honest process reaches all of them. The network
is a discrete-event simulation with a global stabilization time (GST).
"""

import heapq
import random


class Net:
    def __init__(self, n, gst, pre, delta, seed):
        self.n, self.gst, self.pre, self.delta = n, gst, pre, delta
        self.rng = random.Random(seed)
        self.q, self.k, self.now = [], 0, 0
        self.tokens = set()
        self.sent = {"own": 0, "relay": 0}
        self.honest_ids = set()

    def sign(self, i, content):
        tok = ("sig", i, content)
        self.tokens.add(tok)
        return tok

    def send(self, src, dst, tok, kind="own"):
        if src in self.honest_ids:
            self.sent[kind] += 1
        d = self.rng.randint(1, self.pre if self.now < self.gst else self.delta)
        self.k += 1
        heapq.heappush(self.q, (self.now + d, self.k, dst, src, tok))


class Proc:
    def __init__(self, i, n, f, net, byz=None, lock=True, base=12, inc=6):
        self.i, self.n, self.f, self.net, self.byz, self.lock = i, n, f, net, byz, lock
        self.base, self.inc = base, inc
        self.h, self.decision = 0, {}
        self.msgs, self.seen = {}, set()
        self.timers, self.tk = [], 0
        self.reset()

    def reset(self):
        self.round, self.step = 0, "propose"
        self.locked_value, self.locked_round = None, -1
        self.valid_value, self.valid_round = None, -1
        self.done36, self.sched34, self.sched47 = set(), set(), set()

    def proposer(self, h, r):
        return (h + r) % self.n

    def timeout(self, r):
        return self.base + self.inc * r

    def get_value(self):
        return "v%d.%d" % (self.h, self.i)

    def box(self, h):
        if h not in self.msgs:
            self.msgs[h] = {"prop": {}, "PREVOTE": {}, "PRECOMMIT": {}, "senders": {}}
        return self.msgs[h]

    # ---- messages ------------------------------------------------------------
    def store(self, tok):
        kind, h, r = tok[2][0], tok[2][1], tok[2][2]
        M = self.box(h)
        M["senders"].setdefault(r, {})[tok[1]] = True
        if kind == "PROPOSAL":
            if tok[1] == self.proposer(h, r):
                plist = M["prop"].setdefault(r, [])
                if (tok[2][3], tok[2][4]) not in plist:
                    plist.append((tok[2][3], tok[2][4]))
        else:
            M[kind].setdefault(r, {}).setdefault(tok[2][3], {})[tok[1]] = True

    def bcast(self, content):
        tok = self.net.sign(self.i, content)
        self.seen.add(tok)
        self.store(tok)
        for d in range(self.n):
            if d != self.i:
                self.net.send(self.i, d, tok)

    def receive(self, src, tok):
        if self.byz == "silent" or tok in self.seen or tok not in self.net.tokens:
            return
        self.seen.add(tok)
        self.store(tok)
        if self.byz is None:  # gossip: relay each new message once
            for d in range(self.n):
                if d not in (self.i, src, tok[1]):
                    self.net.send(self.i, d, tok, "relay")
        elif tok[2][0] == "PROPOSAL":  # a Byzantine voter backs every proposal
            _, h, r, v, _ = tok[2]
            self.bcast(("PREVOTE", h, r, v))
            self.bcast(("PRECOMMIT", h, r, v))
        self.evaluate()

    # ---- the rules of Algorithm 1 --------------------------------------------
    def start_round(self, r):
        self.round, self.step = r, "propose"
        if self.proposer(self.h, r) == self.i:
            v = self.valid_value if self.valid_value is not None else self.get_value()
            vr = self.valid_round
            if self.byz == "fresh":
                v, vr = "x%d.%d.%d" % (self.h, r, self.i), -1
            if self.byz == "equivocate":
                for d in range(self.n):
                    tok = self.net.sign(self.i, ("PROPOSAL", self.h, r, "%s.%d" % (v, d % 2), vr))
                    if d == self.i:
                        self.seen.add(tok)
                        self.store(tok)
                    else:
                        self.net.send(self.i, d, tok)
                return
            self.bcast(("PROPOSAL", self.h, r, v, vr))  # @line L1
        else:
            self.schedule("propose", r)

    def schedule(self, kind, r):
        self.tk += 1
        heapq.heappush(self.timers, (self.net.now + self.timeout(r), self.tk, kind, self.h, r))

    def count(self, kind, r, v=None, any_value=False):
        votes = self.box(self.h)[kind].get(r, {})
        if any_value:
            return len({j for box in votes.values() for j in box})
        return len(votes.get(v, {}))

    def prevote(self, v):
        self.bcast(("PREVOTE", self.h, self.round, v))
        self.step = "prevote"

    def precommit(self, v):
        self.bcast(("PRECOMMIT", self.h, self.round, v))
        self.step = "precommit"

    def evaluate(self):
        q = 2 * self.f + 1
        changed = True
        while changed:
            changed = False
            M = self.box(self.h)
            props = M["prop"].get(self.round, [])
            if self.step == "propose":
                for v, vr in props:
                    if vr == -1:
                        ok = not self.lock or self.locked_round == -1 or self.locked_value == v
                        self.prevote(v if ok else None)  # @line L2
                        changed = True
                        break
                    if 0 <= vr < self.round and self.count("PREVOTE", vr, v) >= q:
                        ok = not self.lock or self.locked_round <= vr or self.locked_value == v
                        self.prevote(v if ok else None)  # @line L3
                        changed = True
                        break
                if changed:
                    continue
            if self.step == "prevote" and self.round not in self.sched34 and self.count("PREVOTE", self.round, any_value=True) >= q:
                self.sched34.add(self.round)
                self.schedule("prevote", self.round)
            if self.step in ("prevote", "precommit") and self.round not in self.done36:
                for v, _ in props:
                    if v is not None and self.count("PREVOTE", self.round, v) >= q:  # a polka for v
                        self.done36.add(self.round)
                        if self.step == "prevote":
                            self.locked_value, self.locked_round = v, self.round  # @line L4
                            self.precommit(v)
                        self.valid_value, self.valid_round = v, self.round  # @line L5
                        changed = True
                        break
                if changed:
                    continue
            if self.step == "prevote" and self.count("PREVOTE", self.round, None) >= q:
                self.precommit(None)  # @line L6
                changed = True
                continue
            if self.round not in self.sched47 and self.count("PRECOMMIT", self.round, any_value=True) >= q:
                self.sched47.add(self.round)
                self.schedule("precommit", self.round)
            for r, plist in sorted(M["prop"].items()):
                for v, _ in plist:
                    if v is not None and self.count("PRECOMMIT", r, v) >= q and self.h not in self.decision:
                        self.decision[self.h] = v  # @line L7
                        self.h += 1
                        self.reset()
                        self.start_round(0)
                        changed = True
                        break
                if changed:
                    break
            if changed:
                continue
            ahead = [r for r, s in M["senders"].items() if r > self.round and len(s) >= self.f + 1]
            if ahead:
                self.start_round(max(ahead))  # @line L8
                changed = True

    def tick(self):
        fired = False
        while self.timers and self.timers[0][0] <= self.net.now:
            _, _, kind, h, r = heapq.heappop(self.timers)
            if h != self.h or r != self.round:
                continue
            fired = True
            if kind == "propose" and self.step == "propose":
                self.prevote(None)  # @line L9
            elif kind == "prevote" and self.step == "prevote":
                self.precommit(None)  # @line L10
            elif kind == "precommit":
                self.start_round(self.round + 1)  # @line L11
        if fired:
            self.evaluate()


def run(n, f, faulty, strategy, heights=3, gst=60, pre=25, delta=2, seed=0, horizon=5000, lock=True):
    """Simulate until every honest process decided `heights` values, or the
    horizon. Returns the decisions, the rounds and the message counts."""
    net = Net(n, gst, pre, delta, seed)
    procs = [Proc(i, n, f, net, byz=(strategy if i in faulty else None), lock=lock) for i in range(n)]
    net.honest_ids = {i for i in range(n) if i not in faulty}
    honest = sorted(net.honest_ids)
    active = [i for i in range(n) if i not in faulty or strategy != "silent"]
    for i in active:
        procs[i].start_round(0)
    for i in active:
        procs[i].evaluate()
    t = 0
    while t < horizon:
        while net.q and net.q[0][0] <= t:
            _, _, dst, src, tok = heapq.heappop(net.q)
            net.now = t
            procs[dst].receive(src, tok)
        net.now = t
        for i in active:
            procs[i].tick()
        if all(len(procs[i].decision) >= heights for i in honest):
            break
        t += 1
    return {
        "decisions": {i: dict(procs[i].decision) for i in honest},
        "time": t,
        "sent": dict(net.sent),
        "heights": heights,
    }


def check(res):
    """Safety: at each height all honest decisions are equal. Liveness: each
    honest process decided every height."""
    bad = []
    at = {}
    for dec in res["decisions"].values():
        for h, v in dec.items():
            at.setdefault(h, set()).add(v)
    if any(len(vs) > 1 for vs in at.values()):
        bad.append("safety")
    if not all(len(dec) >= res["heights"] for dec in res["decisions"].values()):
        bad.append("liveness")
    return bad


STRATEGIES = ("silent", "equivocate", "fresh")


if __name__ == "__main__":
    for strat in STRATEGIES:
        res = run(4, 1, {1}, strat, seed=1)
        print(strat, check(res), res["decisions"], res["time"], res["sent"])
