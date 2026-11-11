# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bracha-asynchronous-agreement/. The authors are listed in prov/R0F3DQ.jsonl.

"""Bracha's randomized asynchronous binary Byzantine agreement (1987), n > 3t.

Each round has three steps. In each step a process sends its value by
Bracha reliable broadcast, accepts a delivered message only when it is
valid (an honest process could have sent it, given n - t valid messages of
the step before), and waits for n - t valid messages.

  step 1: value -> majority of the n - t values (0 on a tie)
  step 2: if more than n/2 of the n - t values are w, send ("d", w), else "?"
  step 3: more than 2t ("d", w): decide w; more than t ("d", w): take w;
          else take a local coin.

The network is a pool of messages in transit, and a seeded scheduler picks
the next one, so runs are asynchronous and reproducible. Faulty processes
inject messages chosen by a seeded strategy.
"""

import random

D0, D1, Q = ("d", 0), ("d", 1), "?"


class Pool:
    """Messages in transit. "random" delivers a random one; "fifo" the
    oldest; "adversarial" first the messages of faulty processes, and the
    messages to the victim (the first honest process) last."""

    def __init__(self, scheduler, faulty, victim, rng):
        self.scheduler, self.faulty, self.victim, self.rng = scheduler, faulty, victim, rng
        self.buckets = [[], [], [], []]
        self.size = 0

    def append(self, m):
        b = 0
        if self.scheduler == "adversarial":
            b = 2 * (m[0] not in self.faulty) + (m[1] == self.victim)
        self.buckets[b].append(m)
        self.size += 1

    def extend(self, ms):
        for m in ms:
            self.append(m)

    def __bool__(self):
        return self.size > 0

    def pop_next(self):
        self.size -= 1
        b = next(x for x in self.buckets if x)
        if self.scheduler == "fifo":
            return b.pop(0)
        i = self.rng.randrange(len(b))
        b[i], b[-1] = b[-1], b[i]
        return b.pop()


class Run:
    def __init__(self, n, t, inputs, faulty, strategy, scheduler="random", seed=0, max_steps=400000):
        assert n > 3 * t and len(faulty) <= t
        self.n, self.t, self.faulty = n, t, set(faulty)
        self.rng = random.Random(seed)
        self.coin = random.Random(seed * 7919 + 1)  # the local coins of the honest processes
        self.strategy, self.scheduler, self.max_steps = strategy, scheduler, max_steps
        self.honest = [p for p in range(n) if p not in self.faulty]
        self.pending = Pool(scheduler, self.faulty, self.honest[0], self.rng)
        self.messages = 0
        self.inputs = inputs
        self.rbc = {p: {} for p in self.honest}  # instance -> relay state
        self.delivered = {p: {} for p in self.honest}  # (r, k) -> {sender: value}
        self.valid = {p: {} for p in self.honest}  # (r, k) -> {sender: value}, in order of acceptance
        self.waiting = {p: [] for p in self.honest}  # delivered, not yet valid
        self.st = {p: {"r": 1, "k": 1, "v": inputs[p], "decided": None, "round": None, "halted": False} for p in self.honest}  # @line L1
        self.coins = 0

    # ---- reliable broadcast (Bracha) -------------------------------------
    def send_all(self, src, kind, inst, v):
        for d in range(self.n):
            self.pending.append((src, d, kind, inst, v))
        if src not in self.faulty:
            self.messages += self.n

    def rbc_recv(self, p, src, kind, inst, v):
        s = self.rbc[p].setdefault(inst, {"echoed": False, "ready": None, "done": False, "echo": {}, "readys": {}})
        if kind == "initial":
            if src == inst[0] and not s["echoed"]:
                s["echoed"] = True
                self.send_all(p, "echo", inst, v)
        elif kind == "echo":
            s["echo"].setdefault(v, set()).add(src)
        else:
            s["readys"].setdefault(v, set()).add(src)
        if s["ready"] is None:
            for w in list(s["echo"]) + list(s["readys"]):
                if 2 * len(s["echo"].get(w, ())) > self.n + self.t or len(s["readys"].get(w, ())) > self.t:
                    s["ready"] = w
                    self.send_all(p, "ready", inst, w)
                    break
        if not s["done"]:
            for w, snd in s["readys"].items():
                if len(snd) >= 2 * self.t + 1:
                    s["done"] = True
                    sender, r, k = inst
                    self.delivered[p].setdefault((r, k), {})[sender] = w
                    self.waiting[p].append((r, k, sender, w))
                    return True
        return False

    # ---- validation --------------------------------------------------------
    def justified(self, p, r, k, v):
        """Is there a set of n - t valid messages of the step before that
        would make an honest process send v in step k of round r?"""
        n, t, m = self.n, self.t, self.n - self.t
        if k == 1 and r == 1:
            return v in (0, 1)  # @line L12
        prev = self.valid[p].get((r - 1, 3) if k == 1 else (r, k - 1), {})
        if len(prev) < m:
            return False
        vals = list(prev.values())
        if k == 2:  # v must be the majority of some n - t step-1 values
            if v not in (0, 1):
                return False
            a = min(vals.count(v), m)
            b = m - a
            return b <= vals.count(1 - v) and (a > b or (a == b and v == 0))
        if k == 3:
            c = [vals.count(0), vals.count(1)]
            if v in (D0, D1):
                return min(c[v[1]], m) * 2 > n
            if v == Q:  # some n - t set with no value more than n/2 times
                return any(2 * a <= n and 2 * (m - a) <= n and a <= c[0] and m - a <= c[1] for a in range(m + 1))
            return False
        # k == 1, r > 1: v must follow from some n - t step-3 messages
        if v not in (0, 1):
            return False
        cd = {0: vals.count(D0), 1: vals.count(D1)}
        cq = vals.count(Q)
        if min(cd[v], m) > t:
            return True
        # a set with at most t messages ("d", w) for each w gives a coin
        return any(a <= t and b <= t and a <= cd[0] and b <= cd[1] and m - a - b <= cq for a in range(t + 1) for b in range(t + 1) if a + b <= m)

    def accept(self, p):
        """Move delivered messages that became valid into the valid set."""
        waiting = self.waiting[p]
        changed = True
        while changed and waiting:
            changed = False
            for item in list(waiting):
                r, k, s, v = item
                if self.justified(p, r, k, v):
                    self.valid[p].setdefault((r, k), {})[s] = v
                    waiting.remove(item)
                    changed = True

    # ---- the agreement protocol ------------------------------------------
    def start_step(self, p):
        s = self.st[p]
        self.send_all(p, "initial", (p, s["r"], s["k"]), s["v"])  # @line L4

    def advance(self, p):
        n, t = self.n, self.t
        s = self.st[p]
        while not s["halted"]:
            got = self.valid[p].get((s["r"], s["k"]), {})
            if len(got) < n - t:
                return
            vals = list(got.values())[: n - t]  # @line L5
            if s["k"] == 1:
                s["v"] = 1 if vals.count(1) > vals.count(0) else 0  # @line L6
            elif s["k"] == 2:
                w = 1 if vals.count(1) > vals.count(0) else 0
                s["v"] = ("d", w) if 2 * vals.count(w) > n else Q  # @line L7
            else:
                cnt = {w: vals.count(("d", w)) for w in (0, 1)}
                w = 1 if cnt[1] > cnt[0] else 0
                if cnt[w] > 2 * t and s["decided"] is None:
                    s["decided"], s["round"] = w, s["r"]  # @line L8
                if cnt[w] > t:
                    s["v"] = w  # @line L9
                else:
                    s["v"] = self.coin.randint(0, 1)  # @line L10
                    self.coins += 1
                if s["decided"] is not None and s["r"] >= s["round"] + 1:
                    s["halted"] = True  # @line L11
                    return
            if s["k"] == 3:
                s["r"], s["k"] = s["r"] + 1, 1  # @line L2
            else:
                s["k"] += 1  # @line L3
            self.start_step(p)

    def go(self):
        for p in self.honest:
            self.start_step(p)
        for f in sorted(self.faulty):
            self.pending.extend(self.strategy(self, f, None))
        steps = 0
        while self.pending and steps < self.max_steps:
            steps += 1
            msg = self.pending.pop_next()
            src, dst, kind, inst, v = msg
            if dst in self.faulty:
                self.pending.extend(self.strategy(self, dst, msg))
                continue
            if self.rbc_recv(dst, src, kind, inst, v):
                self.accept(dst)
                self.advance(dst)
        dec = {p: self.st[p]["decided"] for p in self.honest}
        rounds = max((self.st[p]["round"] or 0) for p in self.honest)
        return {"decision": dec, "rounds": rounds, "messages": self.messages, "steps": steps, "coins": self.coins}


def run(n, t, inputs, faulty, strategy, scheduler="random", seed=0):
    return Run(n, t, inputs, faulty, strategy, scheduler, seed).go()


def check(inputs, faulty, res):
    bad = []
    d = res["decision"]
    if any(v is None for v in d.values()):
        bad.append("termination")
    vals = {v for v in d.values() if v is not None}
    if len(vals) > 1:
        bad.append("agreement")
    hv = {inputs[p] for p in d}
    if len(hv) == 1 and vals - hv:
        bad.append("validity")
    return bad


# ---- Byzantine strategies ---------------------------------------------------
# strategy(run, f, msg) -> messages (src, dst, kind, instance, value) to inject.
# msg is None once at the start, then each message that f receives.

def silent(R, f, msg):
    return []


def _own_step(R, f, msg, pick):
    """On the first message of instance (r, k) that f sees, broadcast its
    own value for (r, k) chosen by pick; relay others' broadcasts eagerly."""
    out = []
    if msg is None:
        return [(f, d, "initial", (f, 1, 1), pick(R, f, 1, 1, d)) for d in range(R.n)]
    src, _, kind, inst, v = msg
    sender, r, k = inst
    seen = R.__dict__.setdefault("seen", set())
    if (f, r, k) not in seen and r <= 60:
        seen.add((f, r, k))
        out += [(f, d, "initial", (f, r, k), pick(R, f, r, k, d)) for d in range(R.n)]
    if kind == "initial" and (f, inst) not in seen:
        seen.add((f, inst))
        out += [(f, d, "echo", inst, v) for d in range(R.n)]
        out += [(f, d, "ready", inst, v) for d in range(R.n)]
    return out


def _wrong(R, f, r, k, d):
    return {1: 1 - R.inputs[R.honest[0]], 2: 1 - R.inputs[R.honest[0]], 3: D1}[k]


def _random(R, f, r, k, d):
    return R.rng.choice([0, 1] if k < 3 else [D0, D1, Q])


def _split(R, f, r, k, d):
    return [d % 2, d % 2, ("d", d % 2)][k - 1]


def wrong_votes(R, f, msg):
    """Send the same value to all, chosen against the first honest input,
    and ("d", 1) in step 3 whether or not it is valid."""
    return _own_step(R, f, msg, _wrong)


def random_votes(R, f, msg):
    return _own_step(R, f, msg, _random)


def equivocate(R, f, msg):
    """As a sender, give 0 to even receivers and 1 to odd ones; reliable
    broadcast must stop this from splitting the honest processes."""
    return _own_step(R, f, msg, _split)


STRATEGIES = {"silent": silent, "wrong": wrong_votes, "random": random_votes, "equivocate": equivocate}


if __name__ == "__main__":
    res = run(4, 1, [0, 1, 0, 1], {3}, equivocate, "random", 1)
    print(res)
