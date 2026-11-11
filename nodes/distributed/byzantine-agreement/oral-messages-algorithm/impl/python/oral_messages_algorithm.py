# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/oral-messages-algorithm/. The authors are listed in prov/SEB968.jsonl.

"""The oral messages algorithm OM(m) of Lamport, Shostak and Pease (1982).

Synchronous model, n generals 0 .. n - 1 on a complete graph, oral messages
(assumptions A1 to A3: every message is delivered, the receiver knows the
sender, a missing message is detected and replaced by RETREAT). OM(m) is run
in its round form: all sub-instances of the same depth share one round, and a
message carries the path of generals that relayed it. A message of round r has
a path of length r, so OM(m) takes m + 1 rounds.

Traitors run the loyal code to learn what a loyal general would send, and a
seeded strategy then changes or drops each of their messages. The strategy may
depend on the round, the sender, the receiver and the path, so it can
equivocate. hexagon_runs builds the scenario attack of Fischer, Lynch and
Merritt (1986) on OM(m) with n = 3m.
"""

import random
from itertools import combinations
from typing import Callable, Hashable, Optional

RETREAT = 0
VALUES = (0, 1, 2)
Path = tuple[int, ...]
Strategy = Callable[[random.Random, int, int, int, Path, Hashable], Optional[Hashable]]


def majority(values: list[Hashable]) -> Hashable:
    """The value held by more than half of the list, else RETREAT (LSP choice 1)."""
    counts: dict[Hashable, int] = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    for v, c in counts.items():
        if 2 * c > len(values):
            return v
    return RETREAT


class OralGeneral:
    """The local state of one general: the value received on each path."""

    def __init__(self, pid: int, n: int, m: int, commander: int, value: Hashable = None) -> None:
        self.pid, self.n, self.m, self.commander = pid, n, m, commander
        self.value = value
        self.val: dict[Path, Hashable] = {}

    def send(self, r: int) -> list[tuple[int, Path, Hashable]]:
        """The messages of round r, as (receiver, path, value)."""
        out = []
        if r == 1:
            if self.pid == self.commander:
                for q in range(self.n):  # @line L1
                    if q != self.pid:
                        out.append((q, (self.pid,), self.value))
            return out
        for path in sorted(self.val):
            if len(path) == r - 1:
                new = path + (self.pid,)  # @line L4
                for q in range(self.n):
                    if q not in new:
                        out.append((q, new, self.val[path]))
        return out

    def receive(self, r: int, sender: int, path: Path, x: Hashable) -> None:
        """Keep a message only if its path is well formed and ends at the sender (A2)."""
        if self.pid == self.commander or len(path) != r or path[-1] != sender:
            return
        if path[0] != self.commander or self.pid in path or len(set(path)) != len(path):
            return
        if r > self.m + 1 or path in self.val:
            return
        self.val[path] = x  # @line L2

    def decide(self) -> Hashable:
        """Evaluate the recursion of OM(m) bottom-up over the paths."""
        if self.pid == self.commander:
            return self.value
        levels: list[list[Path]] = [[(self.commander,)]]
        for _ in range(self.m):
            nxt = []
            for p in levels[-1]:
                for j in range(self.n):
                    if j not in p and j != self.pid:
                        nxt.append(p + (j,))
            levels.append(nxt)
        res: dict[Path, Hashable] = {}
        for p in levels[-1]:
            res[p] = self.val.get(p, RETREAT)  # @line L3
        for depth in range(len(levels) - 2, -1, -1):
            for p in levels[depth]:  # @line L5
                ys = [self.val.get(p, RETREAT)]  # @line L7
                for j in range(self.n):
                    if j not in p and j != self.pid:
                        ys.append(res[p + (j,)])  # @line L6
                res[p] = majority(ys)  # @line L8
        return res[(self.commander,)]


def honest(rng, r, sender, receiver, path, x):
    return x


def silent(rng, r, sender, receiver, path, x):
    return None


def flip(rng, r, sender, receiver, path, x):
    return (x + 1) % len(VALUES)


def equivocate(rng, r, sender, receiver, path, x):
    return receiver % len(VALUES)


def split(rng, r, sender, receiver, path, x):
    return x if receiver % 2 == 0 else (x + 1) % len(VALUES)


def rand(rng, r, sender, receiver, path, x):
    if rng.random() < 0.15:
        return None
    return rng.choice(VALUES)


STRATEGIES: dict[str, Strategy] = {
    "honest": honest,
    "silent": silent,
    "flip": flip,
    "equivocate": equivocate,
    "split": split,
    "random": rand,
}


def om(
    n: int,
    m: int,
    value: Hashable,
    traitors: frozenset[int] = frozenset(),
    strategy: Strategy = honest,
    seed: int = 0,
    commander: int = 0,
) -> dict:
    """Run OM(m) on n generals; return decisions of loyal lieutenants and the costs."""
    rng = random.Random(seed)
    gens = [OralGeneral(i, n, m, commander, value if i == commander else None) for i in range(n)]
    messages = loyal_messages = 0
    for r in range(1, m + 2):
        batch = []
        for g in gens:
            for q, path, x in g.send(r):
                if g.pid in traitors:
                    x = strategy(rng, r, g.pid, q, path, x)
                    if x is None:
                        continue
                else:
                    loyal_messages += 1
                batch.append((g.pid, q, path, x))
        for p, q, path, x in batch:
            gens[q].receive(r, p, path, x)
        messages += len(batch)
    decisions = {g.pid: g.decide() for g in gens if g.pid not in traitors and g.pid != commander}
    return {"decisions": decisions, "rounds": m + 1, "messages": messages, "loyal_messages": loyal_messages}


def om_messages(n: int, m: int) -> int:
    """Messages of OM(m) when every general sends all it should: sum of (n-1)(n-2)..(n-k)."""
    total, prod = 0, 1
    for k in range(1, m + 2):
        prod *= n - k
        total += prod
    return total


def ic1(decisions: dict[int, Hashable]) -> bool:
    return len(set(decisions.values())) <= 1


def ic2(decisions: dict[int, Hashable], commander_loyal: bool, value: Hashable) -> bool:
    return not commander_loyal or all(d == value for d in decisions.values())


def check(n: int, m: int, value: Hashable, traitors: frozenset[int], strategy: Strategy, seed: int) -> bool:
    res = om(n, m, value, traitors, strategy, seed)
    return ic1(res["decisions"]) and ic2(res["decisions"], 0 not in traitors, value)


def traitor_sets(n: int, k: int):
    for size in range(k + 1):
        yield from (frozenset(c) for c in combinations(range(n), size))


# The scenario (hexagon) attack for n = 3m. Groups A = {0..m-1} (with the
# commander 0), B = {m..2m-1} and C = {2m..3m-1}. Two copies of each group sit
# on a ring A0 B0 C0 A1 B1 C1, and each copy talks to the adjacent copy of each
# other group. Commander copy A0 has value 0, A1 has value 1.

RING = {("A", 0): 0, ("B", 0): 1, ("C", 0): 2, ("A", 1): 3, ("B", 1): 4, ("C", 1): 5}


def group(p: int, m: int) -> str:
    return "ABC"[p // m]


def partner(m: int, p: int, x: int, q: int) -> int:
    """The copy of q that copy x of p talks to."""
    gp, gq = group(p, m), group(q, m)
    if gp == gq:
        return x
    for y in (0, 1):
        if (RING[(gq, y)] - RING[(gp, x)]) % 6 in (1, 5):
            return y
    raise AssertionError


def hexagon(m: int, values: tuple[Hashable, Hashable] = (0, 1)) -> tuple[dict, dict]:
    """Run OM(m) code on the doubled system of 6m copies. Copy x of the commander
    has the value values[x]. Return the views and the decisions of all copies."""
    n = 3 * m
    node = {(p, x): OralGeneral(p, n, m, 0, values[x] if p == 0 else None) for p in range(n) for x in (0, 1)}
    views: dict[tuple[int, int], list] = {k: [] for k in node}
    for r in range(1, m + 2):
        batch = []
        for (p, x), g in sorted(node.items()):
            for q, path, val in g.send(r):
                batch.append(((p, x), (q, partner(m, p, x, q)), path, val))
        for (p, x), dst, path, val in batch:
            views[dst].append((r, p, path, val))
            node[dst].receive(r, p, path, val)
    decisions = {k: g.decide() for k, g in node.items()}
    return views, decisions


def scenario(m: int, correct: tuple[tuple[str, int], tuple[str, int]], values: tuple = (0, 1)) -> dict:
    """A real run on n = 3m generals. The two named group copies are loyal; the
    third group is traitorous and sends what its hexagon copies send."""
    n = 3 * m
    hviews, _ = hexagon(m, values)
    copy_of = dict(correct)
    loyal = [p for p in range(n) if group(p, m) in copy_of]
    value = values[copy_of["A"]] if "A" in copy_of else None
    gens = {p: OralGeneral(p, n, m, 0, value if p == 0 else None) for p in loyal}
    views: dict[int, list] = {p: [] for p in loyal}
    for r in range(1, m + 2):
        batch = []
        for p in loyal:
            for q, path, val in gens[p].send(r):
                if q in gens:
                    batch.append((p, q, path, val))
        for q in loyal:  # the traitors replay the hexagon
            y = copy_of[group(q, m)]
            for rr, p, path, val in hviews[(q, y)]:
                if rr == r and group(p, m) not in copy_of:
                    batch.append((p, q, path, val))
        for p, q, path, val in batch:
            views[q].append((r, p, path, val))
            gens[q].receive(r, p, path, val)
    same = all(sorted(views[p]) == sorted(hviews[(p, copy_of[group(p, m)])]) for p in loyal)
    decisions = {p: gens[p].decide() for p in loyal if p != 0}
    commander_loyal = "A" in copy_of
    ok = ic1(decisions) and ic2(decisions, commander_loyal, value)
    return {"decisions": decisions, "views_match": same, "ok": ok, "commander_loyal": commander_loyal}


def hexagon_runs(m: int, values: tuple = (0, 1)) -> list[dict]:
    """The three runs of the proof: A0 B0 loyal, B0 C0 loyal, C0 A1 loyal."""
    pairs = [(("A", 0), ("B", 0)), (("B", 0), ("C", 0)), (("C", 0), ("A", 1))]
    return [scenario(m, pr, values) for pr in pairs]
