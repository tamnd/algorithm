# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backpressure-routing/. The authors are listed in prov/0WEF6V.jsonl.

"""Backpressure routing (Tassiulas and Ephremides, IEEE TAC 1992).

Each node keeps one queue per commodity; a commodity is the set of packets
for one destination. In each slot, every link (a, b) gets the weight
W = max over commodities c of (Q_a^c - Q_b^c), floored at 0, and the
commodity that attains it. The scheduler activates the feasible set of
links with the largest sum of rate times weight, and each active link with
a positive weight moves up to its rate of packets of its commodity. No
routing table is used: packets flow from long queues to short ones, and
the destination queue is always empty.

Feasible sets are given as an explicit list (for a wired network, the set
of all links). Packets move from the queues as they were at the start of
the slot; arrivals are added at the end of the slot.
"""


class Backpressure:
    def __init__(self, nodes: list, links: list, rates: list, activation_sets: list, commodities: list) -> None:
        self.nodes = list(nodes)
        self.links = list(links)  # (a, b) pairs
        self.rates = list(rates)  # mu_l, packets per slot
        self.sets = [list(s) for s in activation_sets]  # lists of link indices
        self.commodities = list(commodities)  # destinations
        self.q = {n: {c: 0 for c in self.commodities} for n in self.nodes}
        self.delivered = {c: 0 for c in self.commodities}

    def link_weights(self):
        """Return, for each link, (W_l, c_l)."""
        out = []
        for a, b in self.links:  # @line L1
            best_c, best_d = None, None
            for c in self.commodities:  # @line L2
                d = self.q[a][c] - self.q[b][c]
                if best_d is None or d > best_d:
                    best_c, best_d = c, d
            out.append((max(best_d, 0), best_c))  # @line L3
        return out

    def choose(self, weights: list) -> list:
        best, best_v = self.sets[0], None
        for s in self.sets:  # @line L4
            v = sum(self.rates[l] * weights[l][0] for l in s)
            if best_v is None or v > best_v:
                best, best_v = s, v
        return best

    def step(self, arrivals: dict) -> list:
        """Run one slot. arrivals: (node, commodity) -> packets that arrive
        at the end of the slot. Returns the chosen set of links."""
        weights = self.link_weights()
        chosen = self.choose(weights)
        start = {n: dict(self.q[n]) for n in self.nodes}
        moved = []
        for l in chosen:  # @line L5
            w, c = weights[l]
            if w <= 0:
                continue
            a, b = self.links[l]
            k = min(self.rates[l], start[a][c])  # @line L6
            start[a][c] -= k
            self.q[a][c] -= k
            moved.append((b, c, k))
        for b, c, k in moved:
            if b == c:  # @line L7
                self.delivered[c] += k
            else:
                self.q[b][c] += k
        for (n, c), k in arrivals.items():  # @line L8
            if n == c:
                self.delivered[c] += k
            else:
                self.q[n][c] += k
        return chosen

    def total_backlog(self) -> int:
        return sum(sum(v.values()) for v in self.q.values())


def diamond(wireless: bool = True) -> Backpressure:
    """s -> a -> d and s -> b -> d, one packet per slot per link. In the
    wireless form a node cannot send and receive at once, so the feasible
    sets are {s->a, b->d} and {s->b, a->d} (and the empty set); the
    capacity from s to d is then 1 packet per slot. In the wired form all
    four links run together and the capacity is 2."""
    links = [("s", "a"), ("s", "b"), ("a", "d"), ("b", "d")]
    sets = [[0, 3], [1, 2]] if wireless else [[0, 1, 2, 3]]
    return Backpressure(["s", "a", "b", "d"], links, [1, 1, 1, 1], sets, ["d"])
