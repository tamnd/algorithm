# SPDX-License-Identifier: MIT
# Shared helper of the qualitative calculus pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Qualitative calculi and qualitative constraint networks.

A calculus has the base relations 0 .. m-1. A relation is a set of base
relations, stored as an int bit mask: bit b is set when base relation b is in
the set. The calculus keeps the converse of each base relation and the
composition table: table[a][b] is the mask of the base relations that can hold
between x and z when x a y and y b z. The table is computed from concrete
values (integers for points, integer pairs for intervals). It is never typed in.

A network on the nodes 0 .. n-1 is a dict that maps a pair (i, j) with i < j
to a mask. A missing pair has the universal relation. label(calc, net, i, j)
reads a label in either direction.

consistent_scenarios(calc, n, net) is the brute force oracle. It tries the
scenarios of the network (one base relation on each pair) and yields those
that have a realization by concrete values. It is for n <= 5 only. It does not
use the composition table.
"""

from collections.abc import Callable, Iterator
from itertools import combinations

Network = dict[tuple[int, int], int]
Atoms = dict[tuple[int, int], int]


class Calculus:
    """A finite set of base relations with converse and a composition table."""

    def __init__(self, names: list[str], base_of: Callable, values: list,
                 realize: Callable[[int, Atoms], list | None]) -> None:
        """base_of(x, y) is the base relation between two values. values must
        realize every configuration of three values. realize(n, atoms) returns
        n values that satisfy the atomic constraints, or None if there are none."""
        self.names = list(names)
        self.size = len(self.names)
        self.universal = (1 << self.size) - 1
        self.base_of = base_of
        self.realize = realize
        self.conv = [-1] * self.size
        self.table = [[0] * self.size for _ in range(self.size)]
        self.identity = 0
        for x in values:
            self.identity |= 1 << base_of(x, x)
            for y in values:
                a = base_of(x, y)
                assert self.conv[a] in (-1, base_of(y, x))
                self.conv[a] = base_of(y, x)
                for z in values:
                    self.table[a][base_of(y, z)] |= 1 << base_of(x, z)
        assert -1 not in self.conv
        self._comp: dict[tuple[int, int], int] = {}

    def rel(self, *names: str) -> int:
        """The mask of the named base relations."""
        m = 0
        for nm in names:
            m |= 1 << self.names.index(nm)
        return m

    def names_of(self, r: int) -> list[str]:
        return [nm for b, nm in enumerate(self.names) if r >> b & 1]

    def converse(self, r: int) -> int:
        out = 0
        for b in range(self.size):
            if r >> b & 1:
                out |= 1 << self.conv[b]
        return out

    def compose(self, r: int, s: int) -> int:
        """The union of table[a][b] over a in r and b in s. Memoized."""
        key = (r, s)
        out = self._comp.get(key)
        if out is None:
            out = 0
            for a in range(self.size):
                if r >> a & 1:
                    for b in range(self.size):
                        if s >> b & 1:
                            out |= self.table[a][b]
            self._comp[key] = out
        return out


def label(calc: Calculus, net: Network, i: int, j: int) -> int:
    """The label of the pair (i, j) in either direction."""
    if i == j:
        return calc.identity
    if i < j:
        return net.get((i, j), calc.universal)
    return calc.converse(net.get((j, i), calc.universal))


def network(calc: Calculus, n: int, constraints) -> Network:
    """The complete network on n nodes: each label is the universal relation
    intersected with every constraint (i, j, mask) on the pair."""
    net = {(i, j): calc.universal for i, j in combinations(range(n), 2)}
    for i, j, r in constraints:
        if i < j:
            net[(i, j)] &= r
        else:
            net[(j, i)] &= calc.converse(r)
    return net


def order_points(n: int, cons: list[tuple[int, int, int]]) -> list[int] | None:
    """Integers v[0 .. n-1] with sign(v[p] - v[q]) == c for each (p, q, c),
    or None. Merges the = classes, then sorts the < graph topologically."""
    parent = list(range(n))

    def find(p: int) -> int:
        while parent[p] != p:
            parent[p] = parent[parent[p]]
            p = parent[p]
        return p

    for p, q, c in cons:
        if c == 0:
            parent[find(p)] = find(q)
    succ: dict[int, set[int]] = {find(p): set() for p in range(n)}
    for p, q, c in cons:
        if c != 0:
            lo, hi = (find(p), find(q)) if c < 0 else (find(q), find(p))
            if lo == hi:
                return None
            succ[lo].add(hi)
    indeg = {u: 0 for u in succ}
    for u in succ:
        for w in succ[u]:
            indeg[w] += 1
    level = {u: 0 for u in succ}
    stack = [u for u in succ if indeg[u] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for w in succ[u]:
            level[w] = max(level[w], level[u] + 1)
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    if seen < len(succ):
        return None
    return [level[find(p)] for p in range(n)]


def _sign(x: int) -> int:
    return (x > 0) - (x < 0)


def point_algebra() -> Calculus:
    """The point algebra: base relations <, =, > between numbers."""
    def base_of(x: int, y: int) -> int:
        return _sign(x - y) + 1

    def realize(n: int, atoms: Atoms) -> list[int] | None:
        return order_points(n, [(i, j, b - 1) for (i, j), b in atoms.items()])

    return Calculus(["<", "=", ">"], base_of, [0, 1, 2], realize)


ALLEN_NAMES = ["b", "m", "o", "s", "d", "f", "eq", "fi", "di", "si", "oi", "mi", "bi"]
# sign(x- - y-), sign(x- - y+), sign(x+ - y-), sign(x+ - y+) for each base relation
ALLEN_SIGNS = [(-1, -1, -1, -1), (-1, -1, 0, -1), (-1, -1, 1, -1), (0, -1, 1, -1),
               (1, -1, 1, -1), (1, -1, 1, 0), (0, -1, 1, 0), (-1, -1, 1, 0),
               (-1, -1, 1, 1), (0, -1, 1, 1), (1, -1, 1, 1), (1, 0, 1, 1), (1, 1, 1, 1)]


def allen() -> Calculus:
    """Allen's interval algebra: intervals are integer pairs (start, end), start < end."""
    index = {sg: b for b, sg in enumerate(ALLEN_SIGNS)}

    def base_of(x: tuple[int, int], y: tuple[int, int]) -> int:
        return index[(_sign(x[0] - y[0]), _sign(x[0] - y[1]),
                      _sign(x[1] - y[0]), _sign(x[1] - y[1]))]

    def realize(n: int, atoms: Atoms) -> list[tuple[int, int]] | None:
        cons = [(2 * i, 2 * i + 1, -1) for i in range(n)]
        for (i, j), b in atoms.items():
            for (p, q), c in zip(((0, 0), (0, 1), (1, 0), (1, 1)), ALLEN_SIGNS[b]):
                cons.append((2 * i + p, 2 * j + q, c))
        v = order_points(2 * n, cons)
        return None if v is None else [(v[2 * i], v[2 * i + 1]) for i in range(n)]

    values = [(a, b) for a in range(6) for b in range(a + 1, 6)]
    return Calculus(ALLEN_NAMES, base_of, values, realize)


def consistent_scenarios(calc: Calculus, n: int, net: Network) -> Iterator[tuple[Atoms, list]]:
    """Yield (scenario, realization) for every scenario of net that has a
    realization. A partial scenario with no realization is cut off, which is
    safe because a scenario that extends it has no realization either."""
    assert n <= 5, "brute force is for at most 5 nodes"
    pairs = list(combinations(range(n), 2))
    atoms: Atoms = {}

    def search(t: int) -> Iterator[tuple[Atoms, list]]:
        if t == len(pairs):
            vals = calc.realize(n, atoms)
            assert vals is not None
            assert all(calc.base_of(vals[i], vals[j]) == b for (i, j), b in atoms.items())
            yield dict(atoms), vals
            return
        r = net.get(pairs[t], calc.universal)
        for b in range(calc.size):
            if r >> b & 1:
                atoms[pairs[t]] = b
                if calc.realize(n, atoms) is not None:
                    yield from search(t + 1)
                del atoms[pairs[t]]

    yield from search(0)


def consistent(calc: Calculus, n: int, net: Network) -> list | None:
    """A realization of net, or None if it is inconsistent (brute force)."""
    for _, vals in consistent_scenarios(calc, n, net):
        return vals
    return None


def minimal_network(calc: Calculus, n: int, net: Network) -> Network:
    """For each pair, the union of the base relations that occur in some
    consistent scenario (brute force)."""
    out = {p: 0 for p in combinations(range(n), 2)}
    for atoms, _ in consistent_scenarios(calc, n, net):
        for p, b in atoms.items():
            out[p] |= 1 << b
    return out
