# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stalmarck-algorithm/. The authors are listed in prov/JF7B8D.jsonl.

"""Stalmarck's method on CNF input, with AND triplets x <-> (y & z).

The state E is an equivalence relation on literals, kept as a union-find
with parity: node 0 is TRUE, nodes 1..n are the input variables, and the
other nodes name the AND gates of the triplets. A literal is 2*node + neg,
so TRUE = 0 and FALSE = 1. The simple rules close E over the triplets, and
the dilemma rule branches on a variable, saturates both branches, and keeps
what the two branches agree on. Clauses are lists of DIMACS ints.
"""

TRUE, FALSE = 0, 1


def neg(lit: int) -> int:
    return lit ^ 1


class Equiv:
    """Union-find with parity. value(node) = value(root) xor parity."""

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.parity = [0] * size
        self.bad = False  # TRUE == FALSE has been derived

    def copy(self) -> "Equiv":
        e = Equiv(0)
        e.parent, e.parity, e.bad = list(self.parent), list(self.parity), self.bad
        return e

    def find(self, node: int) -> tuple[int, int]:
        p = 0
        root = node
        while self.parent[root] != root:
            p ^= self.parity[root]
            root = self.parent[root]
        return root, p

    def rep(self, lit: int) -> tuple[int, int]:
        root, p = self.find(lit >> 1)
        return root, p ^ (lit & 1)

    def union(self, a: int, b: int) -> bool:
        """Make literal a equivalent to literal b. True if E changed."""
        (ra, pa), (rb, pb) = self.rep(a), self.rep(b)
        if ra == rb:
            if pa != pb:
                self.bad = True
            return False
        if rb == 0:  # keep TRUE as a root
            ra, pa, rb, pb = rb, pb, ra, pa
        self.parent[rb] = ra
        self.parity[rb] = pa ^ pb
        return True

    def same(self, a: int, b: int) -> bool:
        return self.rep(a) == self.rep(b)

    def opposite(self, a: int, b: int) -> bool:
        (ra, pa), (rb, pb) = self.rep(a), self.rep(b)
        return ra == rb and pa != pb

    def classes(self) -> int:
        return len({self.find(v)[0] for v in range(len(self.parent))})


def build(clauses: list[list[int]], n: int):
    """Triplets (x, y, z) meaning x <-> (y & z), and the clause literals that must be TRUE."""
    triplets: list[tuple[int, int, int]] = []
    size = n + 1

    def lit(d: int) -> int:
        return 2 * abs(d) + (d < 0)

    def gate(y: int, z: int) -> int:
        nonlocal size
        x = 2 * size
        size += 1
        triplets.append((x, y, z))
        return x

    roots = []
    for c in clauses:
        if not c:
            roots.append(FALSE)
            continue
        acc = neg(lit(c[0]))  # the clause is false iff all its literals are false
        for d in c[1:]:
            acc = gate(acc, neg(lit(d)))
        roots.append(neg(acc))
    return triplets, roots, size


def simple_rules(triplets, e: Equiv) -> None:
    """0-saturation: apply the simple rules until nothing changes or E is contradictory."""
    changed = True
    while changed and not e.bad:
        changed = False
        for x, y, z in triplets:
            ch = False
            if e.same(x, TRUE):
                ch |= e.union(y, TRUE) | e.union(z, TRUE)
            if e.same(y, FALSE) or e.same(z, FALSE):
                ch |= e.union(x, FALSE)
            if e.same(y, TRUE):
                ch |= e.union(x, z)
            if e.same(z, TRUE):
                ch |= e.union(x, y)
            if e.same(y, z):
                ch |= e.union(x, y)
            if e.opposite(y, z):
                ch |= e.union(x, FALSE)
            if e.opposite(x, y):
                ch |= e.union(y, TRUE) | e.union(z, FALSE)
            if e.opposite(x, z):
                ch |= e.union(z, TRUE) | e.union(y, FALSE)
            changed |= ch
            if e.bad:
                return


def intersect(e1: Equiv, e0: Equiv) -> Equiv:
    """The pairs of literals that are equivalent in both relations."""
    if e1.bad:
        return e0.copy()
    if e0.bad:
        return e1.copy()
    size = len(e1.parent)
    out = Equiv(size)
    first: dict[tuple[int, int, int], tuple[int, int]] = {}
    for v in range(size):
        (r1, p1), (r0, p0) = e1.find(v), e0.find(v)
        key = (r1, r0, p1 ^ p0)
        if key in first:
            u, pu = first[key]
            out.union(2 * u, 2 * v + (pu ^ p1))
        else:
            first[key] = (v, p1)
    return out


def free_inputs(e: Equiv, n: int, used: set[int]) -> list[int]:
    """One input variable from each class that holds an unfixed input variable."""
    seen, out = set(), []
    for v in sorted(used):
        root, _ = e.find(v)
        if root != 0 and root not in seen:
            seen.add(root)
            out.append(v)
    return out


class Stats:
    def __init__(self) -> None:
        self.dilemmas = 0


def saturate(triplets, e: Equiv, k: int, n: int, used: set[int], stats: Stats) -> Equiv:
    """k-saturation of E."""
    e = e.copy()
    while True:  # @line L7
        simple_rules(triplets, e)  # @line L8
        if e.bad or k == 0:  # @line L9
            return e
        before = e.classes()
        for v in free_inputs(e, n, used):  # @line L10
            if e.find(v)[0] == 0:
                continue  # fixed by an earlier dilemma of this round
            stats.dilemmas += 1
            e1, e0 = e.copy(), e.copy()
            e1.union(2 * v, TRUE)
            e0.union(2 * v, FALSE)
            e1 = saturate(triplets, e1, k - 1, n, used, stats)  # @line L11
            e0 = saturate(triplets, e0, k - 1, n, used, stats)
            if e1.bad and e0.bad:
                e.bad = True
                return e
            e = intersect(e1, e0)  # @line L12
        if e.classes() == before:  # @line L13
            return e


def extend(triplets, e: Equiv, k: int, n: int, used: set[int], stats: Stats) -> dict[int, bool] | None:
    """Fix the free variables one at a time under k-saturation. None if both values fail."""
    for v in sorted(used):
        if e.find(v)[0] == 0:
            continue
        trial = e.copy()
        trial.union(2 * v, TRUE)
        trial = saturate(triplets, trial, k, n, used, stats)
        if trial.bad:
            trial = e.copy()
            trial.union(2 * v, FALSE)
            trial = saturate(triplets, trial, k, n, used, stats)
        if trial.bad:
            return None  # E has no model, but k-saturation cannot see it yet
        e = trial
    model = {}
    for v in range(1, n + 1):
        root, p = e.find(v)
        model[v] = (root == 0 and p == 0) if v in used else False
    return model


def stalmarck(clauses: list[list[int]], n: int, stats: Stats | None = None):
    """Returns (model or None, k): the level k of saturation that decided F."""
    stats = stats if stats is not None else Stats()
    triplets, roots, size = build(clauses, n)  # @line L1
    used = {abs(d) for c in clauses for d in c}
    e = Equiv(size)
    for r in roots:
        e.union(r, TRUE)
    k = 0
    while True:  # @line L2
        e = saturate(triplets, e, k, n, used, stats)  # @line L3
        if e.bad:  # @line L4
            return None, k
        model = extend(triplets, e, k, n, used, stats)  # @line L5
        if model is not None:
            return model, k
        k += 1  # @line L6
