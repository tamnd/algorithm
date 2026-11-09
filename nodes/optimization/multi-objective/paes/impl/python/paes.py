# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/paes/. The authors are listed in prov/J8DPVZ.jsonl.

"""(1+1)-PAES, the Pareto archived evolution strategy of Knowles and Corne (2000).

All objectives are minimized. One current solution c is mutated into m per
step. A bounded archive of non-dominated images decides the acceptance:
when c and m do not dominate each other, the one in the less crowded cell of
an adaptive grid becomes the current solution. The grid splits the range of
the archive and m in each objective into 2^l equal parts; this version
recomputes the range at each step.
"""

import random
from typing import Callable, Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for u, v in zip(a, b):
        if u > v:
            return False
        if u < v:
            strict = True
    return strict


def weakly_dominates(a: Vector, b: Vector) -> bool:
    return all(u <= v for u, v in zip(a, b))


class Grid:
    """Cells of 2^l equal parts per objective over the range of the given images."""

    def __init__(self, images: Sequence[Vector], l: int):
        p = len(images[0])
        self.lo = [min(y[k] for y in images) for k in range(p)]
        self.hi = [max(y[k] for y in images) for k in range(p)]
        self.parts = 2**l

    def cell(self, y: Vector) -> tuple[int, ...]:
        out = []
        for v, lo, hi in zip(y, self.lo, self.hi):
            if hi == lo:
                out.append(0)
            else:
                out.append(min(self.parts - 1, int((v - lo) * self.parts // (hi - lo))))
        return tuple(out)


def archive_add(archive: list, m: tuple, cap: int, l: int, rng: random.Random) -> bool:
    """Try to add m = (x, y) to the archive. Return True when it was added."""
    if any(weakly_dominates(z, m[1]) for _, z in archive):  # @line L11
        return False
    archive[:] = [(x, z) for x, z in archive if not dominates(m[1], z)]  # @line L12
    if len(archive) < cap:  # @line L13
        archive.append(m)
        return True
    grid = Grid([z for _, z in archive] + [m[1]], l)
    counts: dict = {}
    for _, z in archive:
        counts[grid.cell(z)] = counts.get(grid.cell(z), 0) + 1
    top = max(counts.values())
    if counts.get(grid.cell(m[1]), 0) < top:  # @line L14
        crowded = [i for i, (_, z) in enumerate(archive) if counts[grid.cell(z)] == top]
        del archive[rng.choice(crowded)]
        archive.append(m)
        return True
    return False


def paes(
    init: Callable[[random.Random], object],
    f: Callable,
    mutate: Callable[[object, random.Random], object],
    cap: int,
    l: int,
    steps: int,
    rng: random.Random,
    on_step: Callable[[tuple, tuple, list], None] | None = None,
) -> list:
    """Run (1+1)-PAES with archive bound cap and l bisections per objective. Return the archive."""
    x0 = init(rng)
    c = (x0, tuple(f(x0)))  # @line L1
    archive = [c]
    for _ in range(steps):  # @line L2
        xm = mutate(c[0], rng)
        m = (xm, tuple(f(xm)))  # @line L3
        if dominates(c[1], m[1]):  # @line L4
            pass
        elif dominates(m[1], c[1]):  # @line L5
            c = m
            archive_add(archive, m, cap, l, rng)
        elif any(dominates(z, m[1]) for _, z in archive):  # @line L6
            pass
        else:  # @line L7
            archive_add(archive, m, cap, l, rng)  # @line L8
            grid = Grid([z for _, z in archive] + [m[1], c[1]], l)
            cm, cc = grid.cell(m[1]), grid.cell(c[1])
            nm = sum(1 for _, z in archive if grid.cell(z) == cm)
            nc = sum(1 for _, z in archive if grid.cell(z) == cc)
            if nm < nc:  # @line L9
                c = m
        if on_step is not None:
            on_step(c, m, archive)
    return archive  # @line L10
