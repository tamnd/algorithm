# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newscast/. The authors are listed in prov/BZKMAQ.jsonl.

"""Newscast (Jelasity, Kowalczyk and van Steen 2003) in a seeded simulator.

Every node keeps a cache of at most c news items. An item is a pair of a
node address and the time stamp at which that node created the item. Once
per cycle each live node, in random order, picks a uniform address from its
cache and the two nodes exchange caches, each adding a fresh item about
itself. Both keep the c freshest items of the union, at most one per
address, and never an item about themselves. A contact with a crashed node
fails and changes nothing.

Failure mode: crash(fraction) removes nodes at once. Churn mode:
churn_cycle replaces a fraction of the nodes by new nodes that know one
random live contact. The application news of the paper is left out; only
the membership part is simulated.
"""

import random


class Newscast:
    def __init__(self, n: int, c: int, seed: int, init: str = "random"):
        self.rng = random.Random(seed)
        self.c = c
        self.time = 0
        self.alive = set(range(n))
        self.next_id = n
        self.cache: dict[int, dict[int, int]] = {}
        for p in range(n):
            if init == "ring":
                peers = [(p + k) % n for k in range(1, c + 1)]
            else:
                peers = self.rng.sample([q for q in range(n) if q != p], c)
            self.cache[p] = {q: 0 for q in peers}

    def exchange(self, p: int, q: int) -> None:
        t = self.time
        merged = dict(self.cache[p])                             # @line L3
        for a, ts in self.cache[q].items():
            if merged.get(a, -1) < ts:                           # @line L4
                merged[a] = ts
        merged[p] = t
        merged[q] = t
        items = list(merged.items())
        self.rng.shuffle(items)                                  # random tie break
        items.sort(key=lambda it: -it[1])
        self.cache[p] = dict([it for it in items if it[0] != p][: self.c])   # @line L5
        self.cache[q] = dict([it for it in items if it[0] != q][: self.c])   # @line L6

    def cycle(self) -> None:
        self.time += 1
        order = sorted(self.alive)
        self.rng.shuffle(order)
        for p in order:
            if p not in self.alive or not self.cache[p]:
                continue
            q = self.rng.choice(list(self.cache[p]))             # @line L1
            if q in self.alive:                                  # @line L2
                self.exchange(p, q)

    # ------------------------------------------------------------ failures

    def crash(self, fraction: float) -> None:
        k = int(fraction * len(self.alive))
        for p in self.rng.sample(sorted(self.alive), k):
            self.alive.discard(p)

    def join(self) -> int:
        p = self.next_id
        self.next_id += 1
        contact = self.rng.choice(sorted(self.alive))
        self.cache[p] = {contact: self.time}
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

    def largest_component(self) -> int:
        """Size of the largest weakly connected component among live nodes."""
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


def stats(xs) -> tuple[float, float]:
    xs = list(xs)
    m = sum(xs) / len(xs)
    return m, sum((x - m) ** 2 for x in xs) / len(xs)
