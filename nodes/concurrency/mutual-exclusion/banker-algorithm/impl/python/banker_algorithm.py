# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/banker-algorithm/. The authors are listed in prov/47TX1V.jsonl.

"""The banker's algorithm for several resource types (Habermann's form).

Vectors are lists of length m. For vectors, x <= y means x[r] <= y[r] for
every r. need[i] = maximum[i] - alloc[i] is what process i may still ask for.
"""

from typing import Callable, Iterator, Optional

from procsim import Sim

Vec = list[int]


def _le(x: Vec, y: Vec) -> bool:
    return all(a <= b for a, b in zip(x, y))


def is_safe(avail: Vec, alloc: list[Vec], need: list[Vec]) -> Optional[list[int]]:
    """Return a safe sequence if the state is safe, else None.

    Precondition: all entries are nonnegative and the lists have n rows of m
    entries. Cost: O(m n^2) time, O(m + n) extra space.
    """
    n = len(alloc)
    work, finish, order = list(avail), [False] * n, []  # @line L1
    while True:  # @line L2
        progress = False  # @line L3
        for i in range(n):  # @line L4
            if not finish[i] and _le(need[i], work):  # @line L5
                work = [w + a for w, a in zip(work, alloc[i])]  # @line L6
                finish[i], progress = True, True
                order.append(i)
        if not progress:  # @line L7
            break
    return order if all(finish) else None  # @line L8


class Banker:
    """The state of the banker: total units, maximum claims and allocations."""

    def __init__(self, total: Vec, maximum: list[Vec]) -> None:
        """Precondition: maximum[i] <= total for every i. Cost: O(m n)."""
        assert all(_le(row, total) for row in maximum)
        self.avail = list(total)
        self.maximum = [list(row) for row in maximum]
        self.alloc = [[0] * len(total) for _ in maximum]
        self.need = [list(row) for row in maximum]

    def request(self, i: int, req: Vec) -> bool:
        """Grant req to process i if the new state is safe; else change nothing.

        Precondition: the current state is safe. Raises ValueError if i asks
        for more than its remaining claim. Cost: O(m n^2).
        """
        if not _le(req, self.need[i]):  # @line L9
            raise ValueError("process exceeded its maximum claim")
        if not _le(req, self.avail):  # @line L10
            return False
        self._move(i, req, 1)  # @line L11
        if is_safe(self.avail, self.alloc, self.need) is not None:  # @line L12
            return True
        self._move(i, req, -1)  # @line L13
        return False

    def release(self, i: int, rel: Vec) -> None:
        """Process i returns rel. Precondition: rel <= alloc[i]. Cost: O(m)."""
        assert _le(rel, self.alloc[i])
        self._move(i, rel, -1)  # @line L14

    def _move(self, i: int, x: Vec, sign: int) -> None:
        for r, k in enumerate(x):
            self.avail[r] -= sign * k
            self.alloc[i][r] += sign * k
            self.need[i][r] -= sign * k


# Processes in the simulator. Each process asks for one unit at a time.

def _client(sim: Sim, me: str, plan: list[tuple], guard: Callable[[Sim, str, int], bool]) -> Iterator[tuple]:
    """Run a plan of ("get", r) and ("put", r) steps, then return every unit held."""

    def get(r: int) -> Callable[[Sim], None]:
        def f(s: Sim) -> None:
            s.v["avail"][r] -= 1
            s.v["alloc"][me][r] += 1
        return f

    def put(r: int) -> Callable[[Sim], None]:
        def f(s: Sim) -> None:
            s.v["avail"][r] += 1
            s.v["alloc"][me][r] -= 1
        return f

    for kind, r in plan:
        if kind == "get":
            yield ("when", lambda s, r=r: guard(s, me, r), get(r), r)
        else:
            yield ("atomic", put(r))
    for r in range(len(sim.v["avail"])):
        while sim.v["alloc"][me][r] > 0:
            yield ("atomic", put(r))


def _fits(s: Sim, me: str, r: int) -> bool:
    return s.v["avail"][r] > 0


def _banker_guard(maximum: dict[str, Vec]) -> Callable[[Sim, str, int], bool]:
    def ok(s: Sim, me: str, r: int) -> bool:
        if s.v["avail"][r] == 0:
            return False
        names = sorted(maximum)
        avail = list(s.v["avail"])
        avail[r] -= 1
        alloc = [list(s.v["alloc"][p]) for p in names]
        alloc[names.index(me)][r] += 1
        need = [[mx - a for mx, a in zip(maximum[p], row)] for p, row in zip(names, alloc)]
        return is_safe(avail, alloc, need) is not None
    return ok


def build(total: Vec, maximum: dict[str, Vec], plans: dict[str, list[tuple]],
          start: Optional[dict[str, Vec]] = None, banker: bool = True) -> Sim:
    """A system of clients. With banker=True each unit is granted only if the result is safe.

    Precondition: each plan stays within the process's maximum claim, and the
    start allocation is within the maximum. Cost: O(n) to build.
    """
    s = Sim()
    start = start or {p: [0] * len(total) for p in plans}
    s.v["alloc"] = {p: list(start[p]) for p in plans}
    s.v["avail"] = [t - sum(start[p][r] for p in plans) for r, t in enumerate(total)]
    guard = _banker_guard(maximum) if banker else _fits
    for p in sorted(plans):
        s.spawn(p, _client, plans[p], guard)
    return s
