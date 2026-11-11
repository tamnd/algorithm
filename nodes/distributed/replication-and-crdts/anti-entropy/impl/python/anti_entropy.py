# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/anti-entropy/. The authors are listed in prov/E24PC5.jsonl.

"""Anti-entropy between replicas of a key-value store.

Each replica maps keys to entries (stamp, value); the merge keeps the entry
with the larger stamp (last-writer-wins), so a tombstone is just an entry whose
value is None. In a session, two replicas find the keys where they differ by
comparing Merkle trees over a fixed split of the key space into buckets, and
then push, pull or push-pull the differing entries (Demers et al., PODC 1987).

spread_rounds simulates only who knows one update, in the random phone call
model, to measure the number of rounds.
"""

import hashlib
import random

Entry = tuple[tuple[int, int], object]  # ((time, writer id), value)


def h(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()[:8]


def bucket_of(key: str, depth: int) -> int:
    return int.from_bytes(hashlib.sha256(key.encode()).digest()[:4], "big") >> (32 - depth)


class Replica:
    def __init__(self, rid: int, depth: int = 4) -> None:
        self.rid = rid
        self.depth = depth
        self.data: dict[str, Entry] = {}
        self._tree: list[bytes] | None = None

    def write(self, key: str, value: object, time: int) -> None:
        self.merge(key, ((time, self.rid), value))

    def merge(self, key: str, e: Entry) -> bool:
        old = self.data.get(key)
        if old is None or e[0] > old[0]:  # @line L5
            self.data[key] = e
            self._tree = None
            return True
        return False

    def bucket(self, b: int) -> list[tuple[str, Entry]]:
        return sorted((k, e) for k, e in self.data.items() if bucket_of(k, self.depth) == b)

    def tree(self) -> list[bytes]:
        """A complete binary tree in an array: node 1 is the root, the leaves are
        2^depth .. 2^(depth+1) - 1, and leaf 2^depth + b covers bucket b."""
        if self._tree is None:
            L = 1 << self.depth
            t = [b""] * (2 * L)
            items: list[list] = [[] for _ in range(L)]
            for k, e in self.data.items():
                items[bucket_of(k, self.depth)].append((k, e))
            for b in range(L):
                t[L + b] = h(repr(sorted(items[b])).encode())
            for i in range(L - 1, 0, -1):
                t[i] = h(t[2 * i] + t[2 * i + 1])
            self._tree = t
        return self._tree


def merkle_diff(a: Replica, b: Replica, stats: dict | None = None) -> set[str]:
    """The keys whose entries differ between a and b (missing counts as different)."""
    ta, tb = a.tree(), b.tree()
    L = 1 << a.depth
    out: set[str] = set()
    stack = [1]
    while stack:
        i = stack.pop()
        if stats is not None:
            stats["compared"] = stats.get("compared", 0) + 1
        if ta[i] == tb[i]:  # @line L6
            continue
        if i >= L:
            da, db = dict(a.bucket(i - L)), dict(b.bucket(i - L))
            out |= {k for k in da.keys() | db.keys() if da.get(k) != db.get(k)}  # @line L7
        else:
            stack += [2 * i, 2 * i + 1]  # @line L8
    return out


def session(p: Replica, q: Replica, mode: str) -> int:
    """One anti-entropy session started by p with partner q. Returns the number
    of entries sent."""
    diff = merkle_diff(p, q)  # @line L2
    sent = 0
    if mode in ("push", "push-pull"):
        for k in sorted(diff):
            if k in p.data:
                q.merge(k, p.data[k])  # @line L3
                sent += 1
    if mode in ("pull", "push-pull"):
        for k in sorted(diff):
            if k in q.data:
                p.merge(k, q.data[k])  # @line L4
                sent += 1
    return sent


def round_of_sessions(reps: list[Replica], mode: str, rng: random.Random) -> None:
    n = len(reps)
    for i in range(n):
        j = rng.randrange(n - 1)  # @line L1
        j += j >= i
        session(reps[i], reps[j], mode)


def converged(reps: list[Replica]) -> bool:
    return all(r.data == reps[0].data for r in reps)


def spread_rounds(n: int, mode: str, rng: random.Random) -> int:
    """Rounds until one update reaches all n nodes. In each round every node
    calls a uniform random other node; exchanges use the state at the start of
    the round (the random phone call model)."""
    informed = [False] * n
    informed[0] = True
    count, rounds = 1, 0
    while count < n:
        rounds += 1
        new = informed[:]
        for i in range(n):
            j = rng.randrange(n - 1)
            j += j >= i
            if informed[i] and mode in ("push", "push-pull"):
                new[j] = True
            if informed[j] and mode in ("pull", "push-pull"):
                new[i] = True
        informed = new
        count = sum(informed)
    return rounds


def one_round_residue(n: int, p: float, mode: str, rng: random.Random) -> float:
    """Start with a fraction p of nodes that lack the update; return the fraction
    that still lacks it after one round."""
    s = int(p * n)
    informed = [i >= s for i in range(n)]
    new = informed[:]
    for i in range(n):
        j = rng.randrange(n - 1)
        j += j >= i
        if informed[i] and mode in ("push", "push-pull"):
            new[j] = True
        if informed[j] and mode in ("pull", "push-pull"):
            new[i] = True
    return new.count(False) / n
