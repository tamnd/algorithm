# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dining-cryptographers/. The authors are listed in prov/1FPAEV.jsonl.
"""A dining cryptographers network (Chaum 1988) on a key graph.

* Parties 0 .. n-1 are the vertices of a key graph. For each edge {i, j},
  the two ends share a fresh random key of l bits for the round (a one-time
  pad, so the anonymity holds against any adversary).
* Each party announces the XOR of the keys on its edges; the sender also
  XORs in its message. The XOR of all announcements is the message, because
  each key is in exactly two announcements.
* Two senders in one round collide: the output is the XOR of their messages.
  A party that announces anything else jams the round, and nobody can tell
  who did it.

The module also has the tools of the tests: the view of a coalition, the
enumeration of all key values for a small case, and the check that the
honest part of the key graph is connected.

For study only. The code is not constant time, and it has no defense
against jamming. For real anonymous group messaging, use a maintained
system built on a DC-net with accountability, such as Dissent, rather than
this code.
"""

import itertools
import secrets
from collections import Counter, deque
from typing import Dict, FrozenSet, Iterable, List, Optional, Tuple

Edge = FrozenSet[int]


class KeyGraph:
    def __init__(self, n: int, edges: Iterable[Tuple[int, int]]) -> None:
        self.n = n
        self.edges: List[Edge] = []
        for i, j in edges:
            assert 0 <= i < n and 0 <= j < n and i != j
            e = frozenset((i, j))
            if e not in self.edges:
                self.edges.append(e)

    @staticmethod
    def complete(n: int) -> "KeyGraph":
        return KeyGraph(n, itertools.combinations(range(n), 2))

    @staticmethod
    def ring(n: int) -> "KeyGraph":
        return KeyGraph(n, ((i, (i + 1) % n) for i in range(n)))

    def at(self, i: int) -> List[Edge]:
        return [e for e in self.edges if i in e]


def share_keys(g: KeyGraph, bits: int) -> Dict[Edge, int]:
    """Each pair of neighbors shares a fresh random key of `bits` bits."""
    return {e: secrets.randbits(bits) for e in g.edges}  # @line L1


def announce(g: KeyGraph, keys: Dict[Edge, int], i: int, message: int = 0) -> int:
    a = 0
    for e in g.at(i):
        a ^= keys[e]  # @line L2
    return a ^ message  # @line L3


def dc_round(g: KeyGraph, keys: Dict[Edge, int], messages: Dict[int, int], jam: Optional[Dict[int, int]] = None) -> Tuple[List[int], int]:
    """messages maps each sender to its message. jam maps a cheating party to
    the bits it XORs into its announcement. Returns the announcements and the
    XOR of all of them, which every party computes."""
    jam = jam or {}
    ann = [announce(g, keys, i, messages.get(i, 0)) ^ jam.get(i, 0) for i in range(g.n)]  # @line L4
    out = 0
    for a in ann:
        out ^= a  # @line L5
    return ann, out  # @line L6


def send_bytes(g: KeyGraph, sender: int, msg: bytes) -> Tuple[List[int], bytes]:
    bits = 8 * len(msg)
    keys = share_keys(g, bits)
    ann, out = dc_round(g, keys, {sender: int.from_bytes(msg, "big")})
    return ann, out.to_bytes(len(msg), "big")


# ---------------------------------------------------------------- views and the anonymity check


def view(g: KeyGraph, keys: Dict[Edge, int], ann: List[int], coalition: FrozenSet[int]) -> tuple:
    """What a coalition sees: the keys on its own edges and all announcements."""
    own = tuple(sorted((tuple(sorted(e)), keys[e]) for e in g.edges if e & coalition))
    return own, tuple(ann)


def view_distribution(g: KeyGraph, coalition: FrozenSet[int], senders: Dict[int, int], jam: Optional[Dict[int, int]] = None, bits: int = 1) -> Counter:
    """Enumerate every value of every key (2^(bits * |E|) cases) and count the views."""
    dist: Counter = Counter()
    for values in itertools.product(range(2**bits), repeat=len(g.edges)):
        keys = dict(zip(g.edges, values))
        ann, _ = dc_round(g, keys, senders, jam)
        dist[view(g, keys, ann, coalition)] += 1
    return dist


def honest_connected(g: KeyGraph, coalition: FrozenSet[int]) -> bool:
    """Is the subgraph of the key graph on the honest parties connected? (breadth-first search)"""
    honest = [i for i in range(g.n) if i not in coalition]
    if not honest:
        return True
    seen, queue = {honest[0]}, deque([honest[0]])
    while queue:
        i = queue.popleft()
        for e in g.at(i):
            (j,) = e - {i}
            if j not in coalition and j not in seen:
                seen.add(j)
                queue.append(j)
    return len(seen) == len(honest)
