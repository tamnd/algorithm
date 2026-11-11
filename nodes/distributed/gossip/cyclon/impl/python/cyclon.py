# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cyclon/. The authors are listed in prov/NQF31F.jsonl.

"""Cyclon (Voulgaris, Gavidia and van Steen 2005), enhanced shuffling, in a
seeded simulator.

Every node keeps a cache of at most c entries (address, age). Once per cycle
each live node P, in random order, runs a shuffle of length l:

  increase the age of every entry by one; pick the entry Q with the highest
  age and l - 1 other random entries; remove Q from the cache; send to Q the
  l - 1 entries and a fresh entry (P, 0); Q answers with l random entries of
  its own cache; both discard received entries that point to themselves or
  that they already hold, put the rest first into empty slots and then in
  the place of entries they sent.

If Q has crashed, P has already removed it and the shuffle ends. A join
runs c random walks from an introducer; the node at the end of each walk
swaps one of its entries for a fresh entry of the joiner and gives that
entry to the joiner.
"""

import random


class Cyclon:
    def __init__(self, n: int, c: int, l: int, seed: int, init: str = "random"):
        self.rng = random.Random(seed)
        self.c, self.l = c, l
        self.alive = set(range(n))
        self.next_id = n
        self.cache: dict[int, dict[int, int]] = {}
        for p in range(n):
            if init == "ring":
                peers = [(p + k) % n for k in range(1, c + 1)]
            else:
                peers = self.rng.sample([q for q in range(n) if q != p], c)
            self.cache[p] = {q: 0 for q in peers}

    def _merge(self, me: int, received: list[tuple[int, int]], sent: list[int]) -> None:
        cache = self.cache[me]
        sent = [a for a in sent if a in cache]
        for a, age in received:
            if a == me or a in cache:                            # @line L7
                continue
            if len(cache) < self.c:                              # @line L8
                cache[a] = age
            elif sent:
                del cache[sent.pop()]                            # @line L9
                cache[a] = age

    def shuffle(self, p: int) -> None:
        cache = self.cache[p]
        if not cache:
            return
        for a in cache:                                          # @line L1
            cache[a] += 1
        q = max(cache, key=lambda a: (cache[a], self.rng.random()))   # @line L2
        others = self.rng.sample([a for a in cache if a != q], min(self.l - 1, len(cache) - 1))
        del cache[q]                                             # @line L3
        out = [(a, cache[a]) for a in others] + [(p, 0)]         # @line L4
        if q not in self.alive:                                  # @line L5
            return
        qcache = self.cache[q]
        back_keys = self.rng.sample(list(qcache), min(self.l, len(qcache)))
        back = [(a, qcache[a]) for a in back_keys]               # @line L6
        self._merge(q, out, back_keys)
        self._merge(p, back, others)

    def cycle(self) -> None:
        order = sorted(self.alive)
        self.rng.shuffle(order)
        for p in order:
            if p in self.alive:
                self.shuffle(p)

    # ------------------------------------------------------------ membership

    def crash(self, fraction: float) -> None:
        k = int(fraction * len(self.alive))
        for p in self.rng.sample(sorted(self.alive), k):
            self.alive.discard(p)

    def join(self, walk_length: int = 5) -> int:
        p = self.next_id
        self.next_id += 1
        intro = self.rng.choice(sorted(self.alive))
        self.cache[p] = {}
        for _ in range(self.c):
            a = intro
            for _ in range(walk_length):
                live = [b for b in self.cache[a] if b in self.alive]
                if not live:
                    break
                a = self.rng.choice(live)
            ca = self.cache[a]
            if a == p or not ca or p in ca:
                continue
            e = self.rng.choice(list(ca))
            if e == p or e in self.cache[p]:
                continue
            age = ca.pop(e)
            ca[p] = 0
            self.cache[p][e] = age
        self.alive.add(p)
        return p

    def churn_cycle(self, rate: float) -> None:
        k = int(rate * len(self.alive))
        self.crash(k / len(self.alive))
        for _ in range(k):
            self.join()
        self.cycle()

    # ------------------------------------------------------------ measures

    def in_degrees(self) -> dict[int, int]:
        deg = {p: 0 for p in self.alive}
        for p in self.alive:
            for q in self.cache[p]:
                if q in deg:
                    deg[q] += 1
        return deg

    def dead_links(self) -> int:
        return sum(1 for p in self.alive for q in self.cache[p] if q not in self.alive)

    def pointers_to(self, d: int) -> int:
        return sum(1 for p in self.alive if d in self.cache[p])

    def largest_component(self) -> int:
        nb = {p: set() for p in self.alive}
        for p in self.alive:
            for q in self.cache[p]:
                if q in nb:
                    nb[p].add(q)
                    nb[q].add(p)
        seen, best = set(), 0
        for s in nb:
            if s in seen:
                continue
            stack, size = [s], 0
            seen.add(s)
            while stack:
                v = stack.pop()
                size += 1
                for w in nb[v]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
            best = max(best, size)
        return best

    def clustering(self) -> float:
        """Mean local clustering coefficient of the undirected overlay."""
        nb = {p: set() for p in self.alive}
        for p in self.alive:
            for q in self.cache[p]:
                if q in nb:
                    nb[p].add(q)
                    nb[q].add(p)
        total = 0.0
        for p, s in nb.items():
            k = len(s)
            if k < 2:
                continue
            links = sum(1 for a in s for b in nb[a] if b in s) / 2
            total += links / (k * (k - 1) / 2)
        return total / len(nb)


def stats(xs) -> tuple[float, float]:
    xs = list(xs)
    m = sum(xs) / len(xs)
    return m, sum((x - m) ** 2 for x in xs) / len(xs)
