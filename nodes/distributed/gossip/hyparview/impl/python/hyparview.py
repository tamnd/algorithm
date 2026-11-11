# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hyparview/. The authors are listed in prov/9B51BZ.jsonl.

"""HyParView (Leitao, Pereira and Rodrigues 2007) in a seeded simulator.

Every node keeps a small symmetric active view (the overlay used for
flooding) and a larger passive view (a reserve of addresses for repair).
A join is spread by FORWARDJOIN random walks. A node that finds a crashed
active neighbour replaces it by a node of its passive view with a
NEIGHBOR request, of high priority if its active view is empty. Passive
views are refreshed by SHUFFLE random walks.

Messages are processed one at a time and at once, so the simulator is
sequential. A crash is found when a node tries to send to the crashed node,
as with a broken TCP connection: during a broadcast, or in check_failures.
"""

import random


class HyParView:
    def __init__(self, seed: int, active: int = 5, passive: int = 30,
                 arwl: int = 6, prwl: int = 3, ka: int = 3, kp: int = 4):
        self.rng = random.Random(seed)
        self.amax = active
        self.pmax = passive
        self.arwl = arwl
        self.prwl = prwl
        self.ka = ka
        self.kp = kp
        self.active: dict[int, set[int]] = {0: set()}
        self.passive: dict[int, set[int]] = {0: set()}
        self.alive = {0}
        self.next_id = 1
        self.messages = 0

    # ------------------------------------------------------------ views

    def _add_passive(self, p: int, q: int) -> None:
        if q == p or q in self.active[p] or q in self.passive[p]:
            return
        if len(self.passive[p]) >= self.pmax:
            self.passive[p].discard(self.rng.choice(sorted(self.passive[p])))
        self.passive[p].add(q)

    def _drop_random_active(self, p: int) -> None:
        r = self.rng.choice(sorted(self.active[p]))                      # @line L6
        self.active[p].discard(r)
        self.active[r].discard(p)   # DISCONNECT: r also drops p
        self.messages += 1
        self._add_passive(p, r)
        self._add_passive(r, p)

    def _add_active(self, p: int, q: int) -> None:
        """Add the link p - q to both active views (links are symmetric)."""
        if q == p or q in self.active[p]:
            return
        for x in (p, q):
            if len(self.active[x]) >= self.amax:
                self._drop_random_active(x)
        self.passive[p].discard(q)
        self.passive[q].discard(p)
        self.active[p].add(q)
        self.active[q].add(p)

    # ------------------------------------------------------------ join

    def join(self, contact=None) -> int:
        n = self.next_id
        self.next_id += 1
        if contact is None:
            contact = self.rng.choice(sorted(self.alive))
        self.active[n] = set()
        self.passive[n] = set()
        self.alive.add(n)
        others = sorted(self.active[contact])
        self._add_active(contact, n)                                     # @line L1
        for q in others:                                                 # @line L2
            if q in self.alive:
                self._forward_join(q, contact, n, self.arwl)
        return n

    def _forward_join(self, p: int, sender: int, n: int, ttl: int) -> None:
        while True:
            self.messages += 1
            if n == p:
                return
            if ttl == 0 or len(self.active[p]) <= 1:                     # @line L3
                self._add_active(p, n)
                return
            if ttl == self.prwl:                                         # @line L4
                self._add_passive(p, n)
            nxt = [q for q in self.active[p] if q != sender and q != n and q in self.alive]
            if not nxt:
                self._add_active(p, n)
                return
            sender, p, ttl = p, self.rng.choice(sorted(nxt)), ttl - 1    # @line L5

    def grow(self, n: int) -> None:
        while len(self.alive) < n:
            self.join()

    # ------------------------------------------------------------ failures

    def crash(self, nodes) -> None:
        for x in nodes:
            self.alive.discard(x)

    def _neighbor_request(self, p: int, r: int, high: bool) -> bool:
        """p asks r to become an active neighbour. True if r accepts."""
        self.messages += 1
        if high or len(self.active[r]) < self.amax:                       # @line L8
            self._add_active(p, r)
            return True
        return False

    def _on_failure(self, p: int, q: int) -> None:
        """p has found that its active neighbour q crashed."""
        self.active[p].discard(q)                                        # @line L7
        tried = set()
        while len(self.active[p]) < self.amax:
            cand = sorted(self.passive[p] - tried)
            if not cand:
                return
            r = self.rng.choice(cand)
            tried.add(r)
            if r not in self.alive:
                self.passive[p].discard(r)
                continue
            if self._neighbor_request(p, r, high=not self.active[p]):
                return

    def check_failures(self, refill: bool = False) -> None:
        """Every live node probes its active links once, as a broken TCP
        connection would tell it. With refill, a node whose active view is
        not full also asks passive nodes to fill it; the paper repairs only
        on failure, and refill is a common addition of implementations."""
        for p in sorted(self.alive):
            dead = [q for q in sorted(self.active[p]) if q not in self.alive]
            for q in dead:
                self._on_failure(p, q)
            if refill and not dead and len(self.active[p]) < self.amax:
                self._fill(p)

    def _fill(self, p: int) -> None:
        tried = set()
        while len(self.active[p]) < self.amax:
            cand = sorted(self.passive[p] - tried)
            if not cand:
                return
            r = self.rng.choice(cand)
            tried.add(r)
            if r not in self.alive:
                self.passive[p].discard(r)
                continue
            if self._neighbor_request(p, r, high=not self.active[p]) and self.active[p]:
                if len(self.active[p]) >= self.amax:
                    return

    # ------------------------------------------------------------ shuffle

    def shuffle(self, p: int) -> None:
        a = [q for q in sorted(self.active[p]) if q in self.alive]
        if not a:
            return
        sent = {p}                                                       # @line L9
        sent.update(self.rng.sample(a, min(self.ka, len(a))))
        pas = sorted(self.passive[p])
        sent.update(self.rng.sample(pas, min(self.kp, len(pas))))
        # random walk of length arwl along active views
        sender, q, ttl = p, self.rng.choice(a), self.arwl - 1
        while True:
            self.messages += 1
            nxt = [x for x in self.active[q] if x != sender and x in self.alive]
            if ttl == 0 or not nxt:
                break
            sender, q, ttl = q, self.rng.choice(sorted(nxt)), ttl - 1
        if q == p:
            return
        pq = sorted(self.passive[q])
        reply = set(self.rng.sample(pq, min(len(sent), len(pq))))
        self.messages += 1
        self._integrate(q, sent, reply)
        self._integrate(p, reply, sent)

    def _integrate(self, x: int, got: set, gave: set) -> None:
        """Put the received entries into the passive view of x, evicting the
        entries that x sent first, then random ones."""
        gave = [g for g in sorted(gave) if g != x]
        for e in sorted(got):
            if e == x or e in self.active[x] or e in self.passive[x]:
                continue
            if len(self.passive[x]) >= self.pmax:
                ev = [g for g in gave if g in self.passive[x]]
                if ev:
                    self.passive[x].discard(ev[0])
                    gave.remove(ev[0])
                else:
                    self.passive[x].discard(self.rng.choice(sorted(self.passive[x])))
            self.passive[x].add(e)

    def shuffle_round(self) -> None:
        order = sorted(self.alive)
        self.rng.shuffle(order)
        for p in order:
            self.shuffle(p)

    # ------------------------------------------------------------ broadcast

    def broadcast(self, src: int) -> float:
        """Flood a message over the active views. A send to a crashed node
        fails, and the sender repairs its view at once (the message is not
        resent). Returns the fraction of live nodes that got the message."""
        got = {src}
        queue = [(src, None)]
        while queue:
            p, frm = queue.pop()
            for q in sorted(self.active[p]):
                if q == frm:
                    continue
                self.messages += 1
                if q not in self.alive:
                    self._on_failure(p, q)
                    continue
                if q not in got:
                    got.add(q)
                    queue.append((q, p))
        return len(got) / len(self.alive)

    # ------------------------------------------------------------ measures

    def largest_component(self) -> int:
        seen = set()
        best = 0
        for s in self.alive:
            if s in seen:
                continue
            comp = 0
            stack = [s]
            seen.add(s)
            while stack:
                v = stack.pop()
                comp += 1
                for w in self.active[v]:
                    if w in self.alive and w not in seen:
                        seen.add(w)
                        stack.append(w)
            best = max(best, comp)
        return best

    def symmetric(self) -> bool:
        return all(p in self.active[q] for p in self.alive for q in self.active[p])
