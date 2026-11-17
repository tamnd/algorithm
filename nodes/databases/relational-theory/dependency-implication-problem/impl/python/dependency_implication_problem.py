# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dependency-implication-problem/. The authors are listed in prov/THAFBS.jsonl.

"""Implication of functional dependencies, equivalence of FD sets, and keys.

implies decides F |= X -> Y by the test Y subset of X+. The closure is the
linear counter algorithm. all_keys is the algorithm of Lucchesi and Osborn
(1978), which lists the candidate keys in time polynomial in |U|, |F| and the
number of keys. keys_brute_force is the reference: it tries every subset.

An FD is a pair (lhs, rhs) of frozensets of attribute names.
"""

from collections import deque
from collections.abc import Hashable, Iterable, Sequence
from itertools import combinations

FD = tuple[frozenset, frozenset]


def fd(lhs: Iterable[Hashable], rhs: Iterable[Hashable]) -> FD:
    return (frozenset(lhs), frozenset(rhs))


def closure(fds: Sequence[FD], x: Iterable[Hashable]) -> frozenset:
    """X+ under fds, by the linear-time counter algorithm."""
    count = [len(lhs) for lhs, _ in fds]
    users: dict[Hashable, list[int]] = {}
    for i, (lhs, _) in enumerate(fds):
        for a in lhs:
            users.setdefault(a, []).append(i)
    out = set(x)
    queue = deque(out)
    for i, (_, rhs) in enumerate(fds):
        if count[i] == 0:
            for b in rhs - out:
                out.add(b)
                queue.append(b)
    while queue:
        a = queue.popleft()
        for i in users.get(a, ()):
            count[i] -= 1
            if count[i] == 0:
                for b in fds[i][1] - out:
                    out.add(b)
                    queue.append(b)
    return frozenset(out)


def implies(fds: Sequence[FD], dep: FD) -> bool:
    """Decide F |= X -> Y: true exactly when Y is a subset of X+."""
    lhs, rhs = dep
    return rhs <= closure(fds, lhs)


def equivalent(f: Sequence[FD], g: Sequence[FD]) -> bool:
    """F and G are equivalent when each implies every FD of the other."""
    return all(implies(f, d) for d in g) and all(implies(g, d) for d in f)


def is_superkey(universe: frozenset, fds: Sequence[FD], k: Iterable[Hashable]) -> bool:
    return closure(fds, k) >= universe


def minimize(universe: frozenset, fds: Sequence[FD], s: Iterable[Hashable]) -> frozenset:
    """Shrink a superkey S to a key: drop each attribute whose removal keeps a superkey."""
    k = set(s)
    for a in sorted(k, key=repr):
        if is_superkey(universe, fds, k - {a}):
            k.discard(a)
    return frozenset(k)


def all_keys(universe: Iterable[Hashable], fds: Sequence[FD]) -> list[frozenset]:
    """Lucchesi and Osborn: list every candidate key of (U, F)."""
    u = frozenset(universe)
    keys = [minimize(u, fds, u)]
    i = 0
    while i < len(keys):
        k = keys[i]
        for lhs, rhs in fds:
            s = lhs | (k - rhs)
            if not any(j <= s for j in keys):
                keys.append(minimize(u, fds, s))
        i += 1
    return keys


def keys_brute_force(universe: Iterable[Hashable], fds: Sequence[FD]) -> list[frozenset]:
    """Every minimal superkey, found by trying all subsets by increasing size."""
    u = sorted(set(universe), key=repr)
    keys: list[frozenset] = []
    for size in range(len(u) + 1):
        for c in combinations(u, size):
            s = frozenset(c)
            if not any(k <= s for k in keys) and closure(fds, s) >= frozenset(u):
                keys.append(s)
    return keys


def prime_attributes(universe: Iterable[Hashable], fds: Sequence[FD]) -> frozenset:
    """The attributes that occur in at least one candidate key."""
    out: frozenset = frozenset()
    for k in all_keys(universe, fds):
        out |= k
    return out


def vertex_cover_schema(n: int, edges: Sequence[tuple[int, int]]) -> tuple[frozenset, list[FD]]:
    """Map a graph to a schema whose smallest key has the size of a smallest vertex cover.

    The attributes are ("v", i) for each vertex and ("e", j) for each edge.
    Each end of edge j determines ("e", j), and the set of all edge attributes
    determines all vertex attributes.
    """
    vs = [("v", i) for i in range(n)]
    es = [("e", j) for j in range(len(edges))]
    fds = []
    for j, (a, b) in enumerate(edges):
        fds.append(fd([vs[a]], [es[j]]))
        fds.append(fd([vs[b]], [es[j]]))
    fds.append(fd(es, vs))
    return frozenset(vs + es), fds
