# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hp-model/. The authors are listed in prov/HVWK9P.jsonl.
"""The HP lattice model of Dill (1985) and Lau and Dill (1989).

A sequence is a string over {"H", "P"}. A fold of a sequence of length n is a
self-avoiding walk with n vertices on the square lattice Z^2 or the cubic
lattice Z^3: residue i sits at vertex x_i, consecutive residues are lattice
neighbours, and no two residues share a vertex. The energy of a fold is minus
the number of topological H-H contacts: pairs i < j with j - i >= 2, both H,
at lattice distance 1.

fold_exact finds the minimum energy by exhaustive enumeration of all walks,
with the lattice symmetries factored out. It visits Theta(c_{n-1} / |G|)
walks, where c_m is the number of m-step self-avoiding walks and |G| is 8 in
2D and 48 in 3D, and does O(dim) work per vertex of the search tree. On the
square lattice c_m grows like mu^m with mu about 2.638, so exact search is
practical only for short chains (n up to about 16 in Python).
"""

from typing import Iterator, Optional

Point = tuple[int, ...]


def unit_steps(dim: int) -> list[Point]:
    """The 2 * dim unit vectors of Z^dim, in the order +x, -x, +y, -y, ..."""
    steps = []
    for a in range(dim):
        for s in (1, -1):
            v = [0] * dim
            v[a] = s
            steps.append(tuple(v))
    return steps


def is_self_avoiding(coords: list[Point]) -> bool:
    """True when consecutive points are lattice neighbours and no point repeats."""
    if len(set(coords)) != len(coords):
        return False
    for p, q in zip(coords, coords[1:]):
        if sum(abs(a - b) for a, b in zip(p, q)) != 1:
            return False
    return True


def hp_energy(seq: str, coords: list[Point]) -> int:
    """Minus the number of topological H-H contacts of a fold. O(n) time with a hash map."""
    where = {p: i for i, p in enumerate(coords)}
    dim = len(coords[0]) if coords else 2
    contacts = 0
    for i, p in enumerate(coords):
        if seq[i] != "H":
            continue
        for d in unit_steps(dim):
            j = where.get(tuple(a + b for a, b in zip(p, d)))
            if j is not None and j > i + 1 and seq[j] == "H":
                contacts += 1
    return -contacts


def weight(dim: int, used: int) -> int:
    """Number of walks in the symmetry class of a canonical walk that spans `used` axes."""
    if dim == 2:
        return 4 if used == 1 else 8
    if dim == 3:
        return {1: 6, 2: 24, 3: 48}[used]
    raise ValueError("dim must be 2 or 3")


def _search(n: int, dim: int, seq: Optional[str]) -> Iterator[tuple[list[Point], int, int]]:
    """Depth-first search over canonical walks with n vertices.

    Yields (walk, class size, H-H contacts). A walk is canonical when it
    starts at the origin with the step +x, and the first step along each new
    axis is positive, with the axes taken in the order x, y, z. Each class of
    walks under the lattice symmetries has exactly one canonical member.
    Explicit stack, no recursion.
    """
    origin = tuple([0] * dim)
    if n == 1:
        yield [origin], 1, 0
        return
    steps = unit_steps(dim)
    first = tuple([1] + [0] * (dim - 1))
    path = [origin, first]
    where = {origin: 0, first: 1}
    used = [1, 1]          # used[k]: number of axes spanned by path[0..k]
    gained = [0, 0]        # gained[k]: H-H contacts made when path[k] was placed
    total = 0
    stack = [0]            # stack[-1]: next step to try from path[-1]
    while stack:
        if len(path) == n:
            yield list(path), weight(dim, used[-1]), total
            stack.pop()
            del where[path.pop()]
            used.pop()
            total -= gained.pop()
            continue
        k = stack[-1]
        if k == len(steps):
            stack.pop()
            if len(path) > 2:
                del where[path.pop()]
                used.pop()
                total -= gained.pop()
            continue
        stack[-1] = k + 1
        d = steps[k]
        axis, sign = k // 2, d[k // 2]
        if axis > used[-1] or (axis == used[-1] and sign < 0):
            continue  # not canonical: a new axis must start in the + direction
        nxt = tuple(a + b for a, b in zip(path[-1], d))
        if nxt in where:
            continue  # not self-avoiding
        i = len(path)
        g = 0
        if seq is not None and seq[i] == "H":
            for e in steps:
                j = where.get(tuple(a + b for a, b in zip(nxt, e)))
                if j is not None and j < i - 1 and seq[j] == "H":
                    g += 1
        path.append(nxt)
        where[nxt] = i
        used.append(max(used[-1], axis + 1))
        gained.append(g)
        total += g
        stack.append(0)


def canonical_walks(n: int, dim: int = 2) -> Iterator[tuple[list[Point], int]]:
    """Yield one walk with n vertices per symmetry class, with the size of its class."""
    if n <= 0:
        return
    for walk, w, _ in _search(n, dim, None):
        yield walk, w


def count_saws(steps: int, dim: int = 2) -> int:
    """The number c_steps of self-avoiding walks with this many steps from the origin."""
    return sum(w for _, w in canonical_walks(steps + 1, dim))


def fold_exact(seq: str, dim: int = 2) -> tuple[int, int, list[Point]]:
    """Exact HP folding by enumeration of self-avoiding walks.

    Returns (E_min, classes, fold): the minimum energy, the number of optimal
    folds counted up to the symmetries of the lattice, and one optimal fold.
    Precondition: seq is a nonempty string over "HP" and dim is 2 or 3.
    """
    if not seq or set(seq) - {"H", "P"}:
        raise ValueError("seq must be a nonempty string over H and P")
    best, classes, best_fold = 1, 0, []
    for walk, _, contacts in _search(len(seq), dim, seq):
        e = -contacts
        if e < best:
            best, classes, best_fold = e, 1, walk
        elif e == best:
            classes += 1
    return best, classes, best_fold
