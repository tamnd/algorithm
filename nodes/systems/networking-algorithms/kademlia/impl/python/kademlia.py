# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kademlia/. The authors are listed in prov/Z8T5G5.jsonl.

"""Kademlia: the XOR metric, k-buckets and the iterative node lookup.

This is a sequential simulation of the protocol of Maymounkov and Mazieres
(2002). Node identifiers are `bits`-bit integers. A call such as
network.find_node(x, u, t) is one remote call from u to x; a failed node
does not answer. One round of the lookup sends its calls "in parallel":
the answers are merged only after all calls of the round return.
"""

from typing import Callable, Optional


def distance(a: int, b: int) -> int:
    """The XOR distance d(a, b) = a xor b."""
    return a ^ b


def bucket_index(own: int, other: int) -> int:
    """The index i with 2**i <= d(own, other) < 2**(i + 1)."""
    return (own ^ other).bit_length() - 1


class RoutingTable:
    """One k-bucket for each index i; each bucket has the least recently
    seen contact at the head and the most recently seen at the tail."""

    def __init__(self, own: int, bits: int, k: int):
        self.own, self.bits, self.k = own, bits, k
        self.buckets: list[list[int]] = [[] for _ in range(bits)]

    def contacts(self) -> list[int]:
        return [c for b in self.buckets for c in b]

    def update(self, c: int, answers_ping: Callable[[int], bool]) -> None:
        """Section 2.2: the rule for a message from contact c."""
        if c == self.own:
            return
        b = self.buckets[bucket_index(self.own, c)]  # @line L1
        if c in b:  # @line L2
            b.remove(c)
            b.append(c)
        elif len(b) < self.k:  # @line L3
            b.append(c)
        elif answers_ping(b[0]):  # @line L4: the head is live; keep it
            b.append(b.pop(0))
        else:  # @line L5: the head is dead; evict it
            b.pop(0)
            b.append(c)

    def remove(self, c: int) -> None:
        b = self.buckets[bucket_index(self.own, c)]
        if c in b:
            b.remove(c)

    def closest(self, t: int, count: int) -> list[int]:
        """The count contacts of this table closest to t."""
        return sorted(self.contacts(), key=lambda c: c ^ t)[:count]


class Node:
    __slots__ = ("ident", "table", "alive")

    def __init__(self, ident: int, bits: int, k: int):
        self.ident = ident
        self.table = RoutingTable(ident, bits, k)
        self.alive = True


class Network:
    def __init__(self, bits: int = 32, k: int = 20, alpha: int = 3):
        self.bits, self.k, self.alpha = bits, k, alpha
        self.nodes: dict[int, Node] = {}
        self.rpcs = 0

    def live_ids(self) -> list[int]:
        return sorted(i for i, v in self.nodes.items() if v.alive)

    def alive(self, i: int) -> bool:
        return i in self.nodes and self.nodes[i].alive

    def fail(self, i: int) -> None:
        self.nodes[i].alive = False

    def update(self, at: int, c: int) -> None:
        self.nodes[at].table.update(c, self.ping)

    def ping(self, x: int) -> bool:
        self.rpcs += 1
        return self.alive(x)

    # -- the remote call -----------------------------------------------------

    def find_node(self, x: int, sender: int, t: int) -> Optional[list[int]]:
        """FIND_NODE sent by sender to x. None if x does not answer."""
        self.rpcs += 1
        if not self.alive(x):
            return None
        self.update(x, sender)  # @line L18
        return self.nodes[x].table.closest(t, self.k)  # @line L19

    # -- the lookup ----------------------------------------------------------

    def lookup(self, u: int, t: int) -> tuple[list[int], int]:
        """The k closest live nodes to t (u included), and the rounds used."""
        k, alpha = self.k, self.alpha
        key = lambda c: c ^ t  # noqa: E731
        S = {u} | set(self.nodes[u].table.closest(t, k))  # @line L6
        Q, F = {u}, set()  # @line L7
        best = min(S, key=key)
        width = alpha
        rounds = 0
        while True:  # @line L8
            K = sorted(S, key=key)[:k]  # @line L9
            C = [x for x in K if x not in Q][:width]  # @line L10
            if not C:  # @line L11
                return K, rounds
            rounds += 1
            answers = []
            for x in C:  # @line L12: these calls run in parallel
                Q.add(x)  # @line L13
                answers.append((x, self.find_node(x, u, t)))
            for x, A in answers:
                if A is not None:  # @line L14
                    S |= set(A) - F
                    self.update(u, x)
                else:  # @line L15
                    S.discard(x)
                    F.add(x)
                    self.nodes[u].table.remove(x)
            new_best = min(S, key=key)
            if key(new_best) < key(best):  # @line L16
                best, width = new_best, alpha
            else:  # @line L17
                width = k

    # -- set-up and joins ----------------------------------------------------

    def add_node(self, ident: int) -> None:
        if ident in self.nodes:
            raise ValueError("identifier in use")
        self.nodes[ident] = Node(ident, self.bits, self.k)

    def join(self, ident: int, via: int, rng) -> None:
        """Section 2.3: insert via, look up the own ID, refresh the buckets
        farther away than the closest neighbour."""
        self.add_node(ident)
        self.update(ident, via)
        found, _ = self.lookup(ident, ident)
        for c in found:
            if c != ident:
                self.update(ident, c)
        near = [c for c in found if c != ident]
        if not near:
            return
        lowest = bucket_index(ident, near[0])
        for i in range(lowest + 1, self.bits):
            target = ident ^ ((1 << i) | rng.getrandbits(i))  # a random ID in bucket i
            self.lookup(ident, target)


def full_network(ids, bits: int, k: int, alpha: int, rng) -> Network:
    """Every bucket of every node holds min(k, size of its range) live nodes,
    chosen at random from its range."""
    net = Network(bits, k, alpha)
    ids = sorted(set(ids))
    for i in ids:
        net.add_node(i)
    for i in ids:
        ranges: list[list[int]] = [[] for _ in range(bits)]
        for j in ids:
            if j != i:
                ranges[bucket_index(i, j)].append(j)
        table = net.nodes[i].table
        for b, members in enumerate(ranges):
            table.buckets[b] = rng.sample(members, min(k, len(members)))
    return net


def sparse_network(ids, bits: int, k: int, alpha: int, rng) -> Network:
    """Every bucket of every node holds exactly one live node of its range if
    the range is not empty (the invariant of Section 3 of the paper)."""
    net = Network(bits, k, alpha)
    ids = sorted(set(ids))
    for i in ids:
        net.add_node(i)
    for i in ids:
        ranges: list[list[int]] = [[] for _ in range(bits)]
        for j in ids:
            if j != i:
                ranges[bucket_index(i, j)].append(j)
        table = net.nodes[i].table
        for b, members in enumerate(ranges):
            table.buckets[b] = [rng.choice(members)] if members else []
    return net


def brute_closest(ids, t: int, k: int) -> list[int]:
    """The reference: the k identifiers closest to t by XOR."""
    return sorted(ids, key=lambda c: c ^ t)[:k]
