# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/honeybadger-bft/. The authors are listed in prov/QX6G31.jsonl.

"""One epoch of HoneyBadgerBFT (Miller, Xia, Croman, Shi and Song, CCS 2016)
in a deterministic asynchronous simulator.

Each node threshold-encrypts a batch of transactions and sends the
ciphertext by erasure-coded reliable broadcast (AVID, after Cachin and
Tessaro). The asynchronous common subset of Ben-Or, Kelmer and Rabin runs n
binary agreements (here the protocol of Mostefaoui, Moumen and Raynal with
a threshold common coin). The ciphertexts of the agreed subset are then
decrypted with f + 1 shares each.

Cryptography is modelled by unforgeable tokens in Crypto: a fragment is
valid only if it was made by the encoder of its Merkle root, and a coin or
decryption share only if the named node made it. Faulty nodes can make
their own shares, but cannot make shares for others.

The scheduler is the adversary: it delivers the pending messages in a
seeded random order, and it delays messages from or to the nodes in
`slow` as long as other messages are pending.
"""

import math
import random

STRATEGIES = ("silent", "equivocate", "wrong_votes", "bad_encoding", "forge")


class Crypto:
    def __init__(self, n, f, seed):
        self.n, self.f = n, f
        self.rng = random.Random(seed)
        self.roots = {}  # root -> (value, size, consistent)
        self.tokens = set()
        self.plain = {}
        self.coins = {}

    # erasure code with a Merkle tree
    def encode(self, value, size, consistent=True):
        root = ("root", len(self.roots))
        self.roots[root] = (value, size, consistent)
        frags = []
        for j in range(self.n):
            tok = ("frag", root, j)
            self.tokens.add(tok)
            frags.append(tok)
        return root, frags

    def frag_ok(self, root, frag):
        return frag in self.tokens and frag[1] == root

    def decode(self, root, frags):
        """Rebuild the value from n - 2f valid fragments and re-encode it;
        None (abort) if the encoding was not consistent."""
        assert len({fr[2] for fr in frags if self.frag_ok(root, fr)}) >= self.n - 2 * self.f
        value, _, consistent = self.roots[root]
        return value if consistent else None

    def frag_bytes(self, root):
        size = self.roots[root][1]
        return math.ceil(size / (self.n - 2 * self.f)) + 32 * (1 + math.ceil(math.log2(self.n)))

    # threshold encryption
    def encrypt(self, txs):
        ct = ("ct", len(self.plain))
        self.plain[ct] = tuple(txs)
        return ct

    def dec_share(self, ct, i):
        tok = ("dec", ct, i)
        self.tokens.add(tok)
        return tok

    def decrypt(self, ct, shares):
        good = {s[2] for s in shares if s in self.tokens and s[1] == ct}
        return self.plain[ct] if len(good) >= self.f + 1 else None

    # threshold common coin
    def coin_share(self, inst, r, i):
        tok = ("coin", inst, r, i)
        self.tokens.add(tok)
        return tok

    def coin(self, inst, r, shares):
        good = {s[3] for s in shares if s in self.tokens and s[1:3] == (inst, r)}
        if len(good) < self.f + 1:
            return None
        if (inst, r) not in self.coins:
            self.coins[(inst, r)] = self.rng.randrange(2)
        return self.coins[(inst, r)]


class ABA:
    """Binary agreement of Mostefaoui, Moumen and Raynal (PODC 2014)."""

    def __init__(self):
        self.est = None
        self.r = 0
        self.est_from = {}  # (r, b) -> senders
        self.sent_est = set()  # (r, b)
        self.bin = {}  # r -> list of values in bin_values
        self.aux = {}  # r -> {sender: b}
        self.sent_aux = set()
        self.coin_shares = {}  # r -> set of tokens
        self.sent_coin = set()
        self.decided = None
        self.rounds = 0
        self.term = {}  # b -> senders of TERM(b)
        self.halted = False


class Node:
    def __init__(self, i, sim):
        self.i, self.sim = i, sim
        n = sim.n
        self.echo = [dict() for _ in range(n)]  # root -> {sender: frag}
        self.ready = [dict() for _ in range(n)]  # root -> senders
        self.sent_echo = [False] * n
        self.sent_ready = [False] * n
        self.rbc_out = [None] * n
        self.aba = [ABA() for _ in range(n)]
        self.dec = {}  # ct -> shares
        self.sent_dec = False
        self.subset = None
        self.block = None

    def send_all(self, msg):
        for j in range(self.sim.n):
            self.sim.send(self.i, j, msg)

    # ---- the epoch --------------------------------------------------------
    def propose(self, txs):
        ct = self.sim.crypto.encrypt(txs)  # @line L1
        size = 64 + len(txs) * self.sim.tx_size
        root, frags = self.sim.crypto.encode(ct, size)
        for j in range(self.sim.n):
            self.sim.send(self.i, j, ("VAL", self.i, root, frags[j]))  # @line L2

    def receive(self, src, msg):
        kind = msg[0]
        c = self.sim.crypto
        if kind == "VAL":
            _, j, root, frag = msg
            if src == j and not self.sent_echo[j] and c.frag_ok(root, frag) and frag[2] == self.i:
                self.sent_echo[j] = True
                self.send_all(("ECHO", j, root, frag))
        elif kind == "ECHO":
            _, j, root, frag = msg
            if c.frag_ok(root, frag) and frag[2] == src:
                self.echo[j].setdefault(root, {}).setdefault(src, frag)
                self.rbc_step(j, root)
        elif kind == "READY":
            _, j, root = msg
            self.ready[j].setdefault(root, set()).add(src)
            self.rbc_step(j, root)
        elif kind == "EST":
            _, j, r, b = msg
            a = self.aba[j]
            got = a.est_from.setdefault((r, b), set())
            got.add(src)
            if len(got) >= self.sim.f + 1 and (r, b) not in a.sent_est:
                a.sent_est.add((r, b))
                self.send_all(("EST", j, r, b))
            if len(got) >= 2 * self.sim.f + 1 and b not in a.bin.setdefault(r, []):
                a.bin[r].append(b)
            self.aba_step(j)
        elif kind == "AUX":
            _, j, r, b = msg
            self.aba[j].aux.setdefault(r, {}).setdefault(src, b)
            self.aba_step(j)
        elif kind == "COIN":
            _, j, r, share = msg
            self.aba[j].coin_shares.setdefault(r, set()).add(share)
            self.aba_step(j)
        elif kind == "TERM":
            # A decided node keeps running rounds until 2f + 1 nodes say TERM;
            # f + 1 TERM(b) contain an honest decision for b.
            _, j, b = msg
            a = self.aba[j]
            got = a.term.setdefault(b, set())
            got.add(src)
            if len(got) >= self.sim.f + 1 and a.decided is None:
                self.decide(j, b)
            if a.decided == b and len(got) >= 2 * self.sim.f + 1:
                a.halted = True
        elif kind == "DEC":
            _, ct, share = msg
            self.dec.setdefault(ct, set()).add(share)
            self.finish()

    # ---- reliable broadcast (AVID) ----------------------------------------
    def rbc_step(self, j, root):
        n, f, c = self.sim.n, self.sim.f, self.sim.crypto
        echoes = self.echo[j].get(root, {})
        readies = self.ready[j].get(root, set())
        if not self.sent_ready[j] and len(echoes) >= n - f:
            if c.decode(root, list(echoes.values())) is None:
                return  # the fragments do not re-encode to the root: abort
            self.sent_ready[j] = True
            self.send_all(("READY", j, root))
        if not self.sent_ready[j] and len(readies) >= f + 1:
            self.sent_ready[j] = True
            self.send_all(("READY", j, root))
        if self.rbc_out[j] is None and len(readies) >= 2 * f + 1 and len(echoes) >= n - 2 * f:
            value = c.decode(root, list(echoes.values()))
            if value is not None:
                self.rbc_out[j] = value
                if self.aba[j].est is None:
                    self.aba_input(j, 1)  # @line L3
                self.finish()

    # ---- binary agreement -------------------------------------------------
    def aba_input(self, j, b):
        a = self.aba[j]
        a.est = b
        a.sent_est.add((0, b))
        self.send_all(("EST", j, 0, b))

    def aba_step(self, j):
        a = self.aba[j]
        n, f = self.sim.n, self.sim.f
        while a.est is not None and not a.halted:
            r = a.r
            bins = a.bin.get(r, [])
            if bins and r not in a.sent_aux:
                a.sent_aux.add(r)
                self.send_all(("AUX", j, r, bins[0]))
            aux = a.aux.get(r, {})
            ok = [b for b in aux.values() if b in bins]
            if len(ok) < n - f:
                return
            if r not in a.sent_coin:
                a.sent_coin.add(r)
                self.send_all(("COIN", j, r, self.sim.crypto.coin_share(j, r, self.i)))
            s = self.sim.crypto.coin(j, r, a.coin_shares.get(r, set()))
            if s is None:
                return
            vals = set(ok)
            if len(vals) == 1:
                (b,) = vals
                a.est = b
                if b == s and a.decided is None:
                    self.decide(j, b)
            else:
                a.est = s
            a.r = r + 1
            if (a.r, a.est) not in a.sent_est:
                a.sent_est.add((a.r, a.est))
                self.send_all(("EST", j, a.r, a.est))

    def decide(self, j, b):
        a = self.aba[j]
        a.decided, a.rounds = b, a.r + 1
        if a.est is None:
            self.aba_input(j, b)  # decided through TERM before it had an input
        self.send_all(("TERM", j, b))
        self.on_decide(j)

    def on_decide(self, j):
        n, f = self.sim.n, self.sim.f
        ones = sum(1 for a in self.aba if a.decided == 1)
        if ones >= n - f:
            for k in range(n):
                if self.aba[k].est is None:
                    self.aba_input(k, 0)  # @line L4
        self.finish()

    # ---- the subset and decryption ----------------------------------------
    def finish(self):
        if self.block is not None:
            return
        if self.subset is None:
            if any(a.decided is None for a in self.aba):
                return
            S = [j for j in range(self.sim.n) if self.aba[j].decided == 1]
            if any(self.rbc_out[j] is None for j in S):
                return
            self.subset = S  # @line L5
        if not self.sent_dec:
            self.sent_dec = True
            for j in self.subset:
                ct = self.rbc_out[j]
                self.send_all(("DEC", ct, self.sim.crypto.dec_share(ct, self.i)))  # @line L6
        plain = []
        for j in self.subset:
            ct = self.rbc_out[j]
            x = self.sim.crypto.decrypt(ct, self.dec.get(ct, set()))  # @line L7
            if x is None:
                return
            plain.extend(x)
        self.block = tuple(sorted(set(plain)))  # @line L8
        self.sim.done += 1


class Faulty:
    """A Byzantine node. It never helps; it only attacks."""

    def __init__(self, i, sim, strategy):
        self.i, self.sim, self.strategy = i, sim, strategy
        self.voted = set()
        self.block = None

    def propose(self, txs):
        c, n, s = self.sim.crypto, self.sim.n, self.strategy
        size = 64 + len(txs) * self.sim.tx_size
        if s == "equivocate":
            r1, f1 = c.encode(c.encrypt(txs), size)
            r2, f2 = c.encode(c.encrypt(txs[:1]), size)
            for j in range(n):
                frags, root = (f1, r1) if j % 2 == 0 else (f2, r2)
                self.sim.send(self.i, j, ("VAL", self.i, root, frags[j]))
        elif s == "bad_encoding":
            root, frags = c.encode(c.encrypt(txs), size, consistent=False)
            for j in range(n):
                self.sim.send(self.i, j, ("VAL", self.i, root, frags[j]))

    def receive(self, src, msg):
        n, f, c = self.sim.n, self.sim.f, self.sim.crypto
        if self.strategy == "wrong_votes" and msg[0] == "EST":
            _, j, r, _ = msg
            if (j, r) not in self.voted:
                self.voted.add((j, r))
                for k in range(n):
                    for b in (0, 1):
                        self.sim.send(self.i, k, ("EST", j, r, b))
                    self.sim.send(self.i, k, ("AUX", j, r, k % 2))
                    self.sim.send(self.i, k, ("COIN", j, r, c.coin_share(j, r, self.i)))
        if self.strategy == "forge" and msg[0] in ("VAL", "ECHO", "COIN", "DEC") and len(self.voted) < 50:
            key = (msg[0], msg[1], msg[2] if msg[0] == "COIN" else 0)
            if key in self.voted:
                return
            self.voted.add(key)
            other = (self.i + 1) % n
            for k in range(n):
                if msg[0] in ("VAL", "ECHO"):
                    fake = ("frag", msg[2], self.i)  # a fragment the encoder never made
                    self.sim.send(self.i, k, ("ECHO", msg[1], msg[2], fake))
                elif msg[0] == "COIN":
                    for b in range(f + 1):
                        self.sim.send(self.i, k, ("COIN", msg[1], msg[2], ("coin", msg[1], msg[2], (other + b) % n)))
                else:
                    self.sim.send(self.i, k, ("DEC", msg[1], ("dec", msg[1], other)))


class Sim:
    def __init__(self, n, f, faulty=(), strategy="silent", seed=0, batch=None, tx_size=250, slow=(), slow_until=4000):
        self.n, self.f = n, f
        self.rng = random.Random(seed)
        self.crypto = Crypto(n, f, seed + 1)
        self.tx_size = tx_size
        self.batch = batch if batch is not None else n * n
        self.slow = set(slow)
        self.slow_until, self.steps = slow_until, 0
        self.pool, self.slow_pool = [], []
        self.bytes = 0
        self.messages = 0
        self.done = 0
        self.faulty = set(faulty)
        self.nodes = [Faulty(i, self, strategy) if i in self.faulty else Node(i, self) for i in range(n)]

    def size(self, msg):
        if msg[0] in ("VAL", "ECHO"):
            return 16 + self.crypto.frag_bytes(msg[2])
        if msg[0] == "READY":
            return 16 + 32
        if msg[0] in ("COIN", "DEC"):
            return 16 + 48
        return 16

    def send(self, src, dst, msg):
        self.messages += 1
        self.bytes += self.size(msg)
        item = (src, dst, msg)
        (self.slow_pool if src in self.slow or dst in self.slow else self.pool).append(item)

    def step(self):
        if self.slow_pool and (self.steps >= self.slow_until or not self.pool):
            self.pool.extend(self.slow_pool)  # the delay ends: every message is delivered
            self.slow_pool.clear()
            self.slow = set()
        pool = self.pool
        self.steps += 1
        k = self.rng.randrange(len(pool))
        pool[k], pool[-1] = pool[-1], pool[k]
        src, dst, msg = pool.pop()
        self.nodes[dst].receive(src, msg)

    def run(self, max_steps=2_000_000):
        per = self.batch // self.n
        for i, node in enumerate(self.nodes):
            node.propose([("tx", i, k) for k in range(per)])
        honest = self.n - len(self.faulty)
        steps = 0
        while self.done < honest and (self.pool or self.slow_pool) and steps < max_steps:
            self.step()
            steps += 1
        return self


def epoch(n, f, faulty=(), strategy="silent", seed=0, batch=None, tx_size=250, slow=()):
    """Run one epoch. Returns a dict with the block of each honest node, the
    agreed subset, the ABA rounds, the message and byte counts."""
    s = Sim(n, f, faulty, strategy, seed, batch, tx_size, slow).run()
    honest = [x for x in s.nodes if isinstance(x, Node)]
    return {
        "blocks": {x.i: x.block for x in honest},
        "subsets": {x.i: x.subset for x in honest},
        "aba_rounds": [a.rounds for x in honest for a in x.aba],
        "messages": s.messages,
        "bytes": s.bytes,
        "txs": len(honest[0].block or ()),
    }


def check(res, n, f):
    errs = []
    blocks = set(res["blocks"].values())
    if None in blocks:
        errs.append("termination")
    if len(blocks - {None}) > 1:
        errs.append("agreement")
    subsets = [s for s in res["subsets"].values() if s is not None]
    if subsets and len(subsets[0]) < n - f:
        errs.append("subset smaller than n - f")
    return errs


if __name__ == "__main__":
    for n, f in ((4, 1), (7, 2), (10, 3)):
        r = epoch(n, f, batch=40 * n * n)
        print(n, f, check(r, n, f), r["txs"], r["messages"], round(r["bytes"] / r["txs"] / (250 * n), 2))
