# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gale-church-alignment/. The authors are listed in prov/TXM3A8.jsonl.

import math
import random

from gale_church_alignment import (
    BEADS,
    PRIORS,
    align,
    alignment_cost,
    bead_cost,
    delta,
    log_two_sided_tail,
)

X = [62, 31, 44, 18, 70]
Y = [66, 80, 21, 72]


def all_alignments(nx, ny):
    """Every monotone sequence of beads from (0, 0) to (nx, ny)."""
    if nx == 0 and ny == 0:
        yield []
        return
    for p, q in BEADS:
        if p <= nx and q <= ny:
            for rest in all_alignments(nx - p, ny - q):
                yield rest + [(nx - p, nx, ny - q, ny)]


def test_worked_example() -> None:
    beads, cost = align(X, Y)
    assert beads == [(0, 1, 0, 1), (1, 3, 1, 2), (3, 4, 2, 3), (4, 5, 3, 4)]
    assert math.isclose(cost, 3.4283, abs_tol=1e-4)
    assert math.isclose(cost, alignment_cost(X, Y, beads), rel_tol=1e-12)
    # the 2-1 bead joins 31 + 44 = 75 characters with 80
    assert math.isclose(delta(75, 80), 5 / math.sqrt(6.8 * 77.5), rel_tol=1e-12)


def test_delete_or_merge() -> None:
    # a short last sentence goes into a 2-1 bead, not into a 1-0 bead
    beads, _ = align([40, 25, 30, 62, 12], [43, 58, 65])
    assert beads == [(0, 1, 0, 1), (1, 3, 1, 2), (3, 5, 2, 3)]


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(150):
        nx, ny = rng.randint(0, 5), rng.randint(0, 5)
        x = [rng.randint(1, 120) for _ in range(nx)]
        y = [rng.randint(1, 120) for _ in range(ny)]
        beads, cost = align(x, y)
        best = min(alignment_cost(x, y, b) for b in all_alignments(nx, ny))
        assert math.isclose(cost, best, rel_tol=1e-9, abs_tol=1e-9)
        assert math.isclose(alignment_cost(x, y, beads), cost, rel_tol=1e-9, abs_tol=1e-9)
        # every sentence is in exactly one bead, in order
        assert [b[0] for b in beads] + [nx] == [0] + [b[1] for b in beads]
        assert [b[2] for b in beads] + [ny] == [0] + [b[3] for b in beads]


def test_count_of_alignments() -> None:
    # the brute force really enumerates every path of the six steps
    counts = {(0, 0): 1}
    for i in range(4):
        for j in range(4):
            if (i, j) != (0, 0):
                counts[(i, j)] = sum(counts.get((i - p, j - q), 0) for p, q in BEADS)
    assert sum(1 for _ in all_alignments(3, 3)) == counts[(3, 3)]


def test_edges() -> None:
    assert align([], []) == ([], 0.0)
    beads, cost = align([30], [])
    assert beads == [(0, 1, 0, 0)]
    assert math.isclose(cost, bead_cost(30, 0, 1, 0))
    beads, _ = align([], [10, 20])
    assert beads == [(0, 0, 0, 1), (0, 0, 1, 2)]
    # the program's delta is defined for 0-1 beads; the text form l1 = 0 is not
    assert math.isclose(delta(0, 50), 50 / math.sqrt(6.8 * 25))
    assert delta(0, 0) == 0.0


def test_priors() -> None:
    assert math.isclose(sum(PRIORS.values()), 1.0988, rel_tol=1e-12)
    assert math.isclose(bead_cost(50, 50, 1, 1), -math.log(0.89), rel_tol=1e-12)


def test_tail() -> None:
    for x in (0.0, 0.5, 1.96, 5.0, 12.0, 29.0):
        assert math.isclose(log_two_sided_tail(x), math.log(math.erfc(x / math.sqrt(2))), rel_tol=1e-12)
    assert math.isclose(log_two_sided_tail(1.96), math.log(0.05), rel_tol=1e-3)
    # the asymptotic branch joins the erfc branch at 30
    below = math.log(math.erfc(29.999 / math.sqrt(2)))
    assert math.isclose(log_two_sided_tail(30.0), below - (30.0**2 - 29.999**2) / 2, rel_tol=1e-6)
    # far out the cost stays finite, where erfc itself is 0
    assert math.erfc(60 / math.sqrt(2)) == 0.0
    assert math.isfinite(log_two_sided_tail(60.0))
    assert log_two_sided_tail(-3.0) == log_two_sided_tail(3.0)
