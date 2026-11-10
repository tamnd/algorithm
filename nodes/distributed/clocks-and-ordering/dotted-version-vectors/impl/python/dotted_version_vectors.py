# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dotted-version-vectors/. The authors are listed in prov/Q366JY.jsonl.

"""Dotted version vectors (Preguiça, Baquero, Almeida, Fonte and Gonçalves 2010).

A clock is a version vector over server ids plus at most one dot (r, n).
Its causal history is C = {(i, k) : 1 <= k <= vv[i]} plus the dot. Servers
keep, for one key, a set of siblings (clock, value). Clients read with GET,
which returns the values and a context, and write with PUT(context, value)
at some server r. The model is asynchronous; servers exchange their sibling
sets with SYNC. Costs: comparison O(s), where s is the number of server ids;
SYNC of sets of sizes a and b costs O(a b s).
"""

import random

Dot = tuple[str, int]


class DottedVersionVector:
    """An immutable clock: a version vector vv and an optional dot (r, n) with n > vv[r] + 1."""

    __slots__ = ("vv", "dot")

    def __init__(self, vv: dict[str, int], dot: Dot | None = None) -> None:
        vv = {i: m for i, m in vv.items() if m > 0}
        if dot is not None and dot[1] == vv.get(dot[0], 0) + 1:
            vv[dot[0]] = dot[1]  # normal form: a contiguous dot joins the vector
            dot = None
        self.vv = vv
        self.dot = dot

    def history(self) -> frozenset[Dot]:
        """The causal history C of the clock. O(sum of the entries)."""
        out = {(i, k) for i, m in self.vv.items() for k in range(1, m + 1)}
        if self.dot is not None:
            out.add(self.dot)
        return frozenset(out)

    def contains(self, d: Dot) -> bool:
        """Is the event d in C? O(1)."""
        return d[1] <= self.vv.get(d[0], 0) or d == self.dot

    def leq(self, other: "DottedVersionVector") -> bool:
        """C[self] is a subset of C[other]. O(s)."""
        for i, m in self.vv.items():  # @line L1
            if m > other.vv.get(i, 0) and not (m == other.vv.get(i, 0) + 1 and other.dot == (i, m)):
                return False
        if self.dot is not None and not other.contains(self.dot):  # @line L2
            return False
        return True  # @line L3

    def lt(self, other: "DottedVersionVector") -> bool:
        return self.leq(other) and not other.leq(self)

    def key(self) -> tuple:
        return (tuple(sorted(self.vv.items())), self.dot)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DottedVersionVector) and self.key() == other.key()

    def __hash__(self) -> int:
        return hash(self.key())

    def __repr__(self) -> str:
        return f"DVV({self.vv}, {self.dot})"


Sibling = tuple[DottedVersionVector, object]


def sync(s1: set[Sibling], s2: set[Sibling]) -> set[Sibling]:
    """Keep each sibling that no sibling of the other set strictly dominates."""
    keep1 = {x for x in s1 if not any(x[0].lt(y[0]) for y in s2)}  # @line L4
    keep2 = {y for y in s2 if not any(y[0].lt(x[0]) for x in s1)}
    return keep1 | keep2


def context(s: set[Sibling]) -> dict[str, int]:
    """The ceiling of a set of clocks: for each id, the largest counter in a vector entry or a dot."""
    ctx: dict[str, int] = {}
    for c, _ in s:
        for i, m in c.vv.items():
            ctx[i] = max(ctx.get(i, 0), m)  # @line L5
        if c.dot is not None:
            ctx[c.dot[0]] = max(ctx.get(c.dot[0], 0), c.dot[1])
    return ctx


def update(ctx: dict[str, int], s_r: set[Sibling], r: str) -> DottedVersionVector:
    """The clock of a new write at server r with client context ctx."""
    n = context(s_r).get(r, 0) + 1  # @line L6
    return DottedVersionVector(dict(ctx), (r, n))  # @line L7


class Server:
    """The sibling set of one key at one server r."""

    def __init__(self, r: str) -> None:
        self.r = r
        self.siblings: set[Sibling] = set()

    def get(self) -> tuple[list[object], dict[str, int]]:
        """Return the values and the context of the key."""
        return [v for _, v in self.siblings], context(self.siblings)  # @line L10

    def put(self, ctx: dict[str, int], value: object) -> DottedVersionVector:
        """Write a value with the context of an earlier GET. Return the new clock."""
        u = update(ctx, self.siblings, self.r)  # @line L8
        self.siblings = sync({(u, value)}, self.siblings)  # @line L9
        return u

    def sync_with(self, other: "Server") -> None:
        """Anti-entropy between two servers: both end with the same siblings."""
        merged = sync(self.siblings, other.siblings)
        self.siblings = set(merged)
        other.siblings = set(merged)


def random_schedule(servers: list[str], clients: int, steps: int, rng: random.Random) -> list[tuple]:
    """A seeded schedule of ("get", c, server), ("put", c, server) and ("sync", s1, s2)."""
    ops: list[tuple] = []
    for _ in range(steps):
        x = rng.random()
        if x < 0.4:
            ops.append(("get", rng.randrange(clients), rng.choice(servers)))
        elif x < 0.8:
            ops.append(("put", rng.randrange(clients), rng.choice(servers)))
        elif len(servers) > 1:
            a, b = rng.sample(servers, 2)
            ops.append(("sync", a, b))
    return ops
