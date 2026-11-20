# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/su-rental-harmony-algorithm/. The authors are listed in prov/QR1JRG.jsonl.

"""Su's path-following algorithm for rental harmony.

There are n rooms and n tenants, both numbered 0 to n - 1, and a total rent
R. The price simplex {p >= 0, sum p = R} is cut by a grid of size N into
small simplices (cells). A point of the grid is stored by its partial sums
s = (s_0, ..., s_{n-2}) with 0 <= s_0 <= ... <= s_{n-2} <= N; the room
prices are R x / N with x_0 = s_0, x_j = s_j - s_{j-1} and
x_{n-1} = N - s_{n-2}. The cells are the Freudenthal (Kuhn) simplices: a
cell (b, pi) has the vertices b, b + e_pi[0], b + e_pi[0] + e_pi[1], ...

Each grid point has an owner, the tenant sum(s) mod n; the n vertices of a
cell have n different owners. The label of a grid point is the room that its
owner chooses at its prices. A cell with all n labels gives the assignment.
"""

from fractions import Fraction
from itertools import permutations, product
from typing import Callable, Sequence

Point = tuple[int, ...]
Cell = tuple[Point, tuple[int, ...]]
Chooser = Callable[[int, list[Fraction]], int]


def prices(s: Point, n: int, rent: Fraction, grid: int) -> list[Fraction]:
    x = [s[0]] + [s[j] - s[j - 1] for j in range(1, n - 1)] + [grid - s[-1]]
    return [Fraction(rent) * xj / grid for xj in x]


def owner(s: Point, n: int) -> int:
    return sum(s) % n


def vertices(cell: Cell) -> list[Point]:
    b, pi = cell
    out = [b]
    cur = list(b)
    for j in pi:
        cur[j] += 1
        out.append(tuple(cur))
    return out


def in_region(s: Point, grid: int) -> bool:
    if s[0] < 0 or s[-1] > grid:
        return False
    return all(s[j - 1] <= s[j] for j in range(1, len(s)))


def cell_in_region(cell: Cell, grid: int) -> bool:
    return all(in_region(v, grid) for v in vertices(cell))


def pivot(cell: Cell, t: int) -> tuple[Cell, int]:
    """The cell across the facet without vertex t, and the index of its new vertex."""
    b, pi = cell
    d = len(pi)
    if 0 < t < d:
        q = list(pi)
        q[t - 1], q[t] = q[t], q[t - 1]
        return (b, tuple(q)), t
    if t == 0:
        nb = list(b)
        nb[pi[0]] += 1
        return (tuple(nb), pi[1:] + pi[:1]), d
    nb = list(b)
    nb[pi[-1]] -= 1
    return (tuple(nb), pi[-1:] + pi[:-1]), 0


class Labeler:
    """Ask each owner its choice at most once per grid point, and count the questions."""

    def __init__(self, n: int, rent, grid: int, choose: Chooser) -> None:
        self.n, self.rent, self.grid, self.choose = n, Fraction(rent), grid, choose
        self.cache: dict[Point, int] = {}

    def __call__(self, s: Point) -> int:
        if s not in self.cache:
            p = prices(s, self.n, self.rent, self.grid)
            room = self.choose(owner(s, self.n), p)
            if not 0 <= room < self.n:
                raise ValueError("a tenant must choose a room 0 to n - 1")
            self.cache[s] = room
        return self.cache[s]

    @property
    def questions(self) -> int:
        return len(self.cache)


def boundary_doors(n: int, grid: int, label: Labeler) -> list[tuple[Cell, int]]:
    """The doors on the boundary, as (cell, index of the vertex not in the door).

    A door is a facet whose labels are exactly 0 to n - 2. With miserly
    tenants and grid >= n, every boundary door lies in a cell whose base has
    all coordinates at most n - 2, near the corner where room n - 1 costs R.
    """
    d = n - 1
    want = set(range(n - 1))
    found = []
    top = min(n - 2, grid)
    for b in product(range(top + 1), repeat=d):
        if not in_region(b, grid):
            continue
        for pi in permutations(range(d)):
            cell = (b, pi)
            if not cell_in_region(cell, grid):
                continue
            vs = vertices(cell)
            for t in range(n):
                labs = [label(v) for k, v in enumerate(vs) if k != t]
                if set(labs) != want:
                    continue
                if not cell_in_region(pivot(cell, t)[0], grid):
                    found.append((cell, t))
    return found


def su_rental_harmony(n: int, rent, grid: int, choose: Chooser):
    """Return (rooms, price, questions, steps).

    rooms[i] is the room of tenant i, price is the average of the vertex prices
    of the fully labeled cell (it sums to the rent), questions is the number of
    grid points asked, and steps is the number of cells visited.
    """
    if n < 2 or grid < n:
        raise ValueError("su_rental_harmony needs n >= 2 and grid >= n")
    label = Labeler(n, rent, grid, choose)  # @line L1
    steps = 0
    for cell, new in boundary_doors(n, grid, label):  # @line L2
        while True:  # @line L3
            steps += 1
            vs = vertices(cell)  # @line L4
            labs = [label(v) for v in vs]
            if len(set(labs)) == n:  # @line L5
                rooms = [0] * n
                for v, r in zip(vs, labs):
                    rooms[owner(v, n)] = r  # @line L6
                ps = [prices(v, n, label.rent, grid) for v in vs]
                price = [sum(p[j] for p in ps) / n for j in range(n)]  # @line L7
                return rooms, price, label.questions, steps
            u = next(k for k in range(n) if k != new and labs[k] == labs[new])  # @line L8
            nxt, nnew = pivot(cell, u)  # @line L9
            if not cell_in_region(nxt, grid):
                break  # the path left through another boundary door
            cell, new = nxt, nnew  # @line L10
    raise RuntimeError("no fully labeled cell found; are the tenants miserly?")


def fully_labeled_cells(n: int, rent, grid: int, choose: Chooser) -> list[Cell]:
    """Brute force: every cell of the region with all n labels (for tests)."""
    label = Labeler(n, rent, grid, choose)
    d = n - 1
    out = []
    for b in product(range(grid + 1), repeat=d):
        if not in_region(b, grid):
            continue
        for pi in permutations(range(d)):
            cell = (b, pi)
            if cell_in_region(cell, grid) and len({label(v) for v in vertices(cell)}) == n:
                out.append(cell)
    return out


def count_cells(n: int, grid: int) -> int:
    d = n - 1
    return sum(
        1
        for b in product(range(grid + 1), repeat=d)
        if in_region(b, grid)
        for pi in permutations(range(d))
        if cell_in_region((b, pi), grid)
    )


def envy(costs: Sequence[Sequence[int]], rooms: list[int], price: list[Fraction]) -> Fraction:
    """For the test tenants who pay costs[i][j] * p_j, the largest extra cost of a tenant."""
    worst = Fraction(0)
    for i, r in enumerate(rooms):
        mine = costs[i][r] * price[r]
        for j in range(len(rooms)):
            worst = max(worst, mine - costs[i][j] * price[j])
    return worst
