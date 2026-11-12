# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dead-end-elimination/. The authors are listed in prov/161ER1.jsonl.

"""Dead-end elimination (DEE) for side-chain packing.

The model: residues 0 .. n-1 on a fixed backbone. Residue i has rotamers
0 .. p_i - 1. The energy of an assignment x is

    E(x) = sum_i E_i(x_i) + sum_{i < j} E_ij(x_i, x_j).

self_e[i][r] is E_i(r). pair_e[(i, j)][r][s], with i < j, is E_ij(r, s).
A missing pair (i, j) means that E_ij is zero. Energies can be int or
fractions.Fraction; the tests use Fraction so that each comparison is exact.
"""

import random
from itertools import product
from typing import Callable, Dict, List, Optional, Sequence, Tuple

SelfE = Sequence[Sequence]
PairE = Dict[Tuple[int, int], Sequence[Sequence]]
Live = List[List[int]]


def pair_energy(pair_e: PairE, i: int, r: int, j: int, s: int):
    """E_ij(r, s) for i != j, read from the table of the ordered pair."""
    if i < j:
        table = pair_e.get((i, j))
        return 0 if table is None else table[r][s]
    table = pair_e.get((j, i))
    return 0 if table is None else table[s][r]


def total_energy(self_e: SelfE, pair_e: PairE, x: Sequence[int]):
    """E(x) for a full assignment x, one rotamer index per residue."""
    e = sum(self_e[i][x[i]] for i in range(len(self_e)))
    for (i, j), table in pair_e.items():
        e += table[x[i]][x[j]]
    return e


def desmet(self_e: SelfE, pair_e: PairE, live: Live, i: int, r: int, t: int) -> bool:
    """The criterion of Desmet et al. (1992): t makes r a dead end.

    E_i(r) + sum_j min_s E_ij(r, s) > E_i(t) + sum_j max_s E_ij(t, s),
    with s over the live rotamers of each residue j != i.
    """
    lhs = self_e[i][r]
    rhs = self_e[i][t]
    for j in range(len(self_e)):
        if j == i:
            continue
        lhs += min(pair_energy(pair_e, i, r, j, s) for s in live[j])
        rhs += max(pair_energy(pair_e, i, t, j, s) for s in live[j])
    return lhs > rhs


def goldstein(self_e: SelfE, pair_e: PairE, live: Live, i: int, r: int, t: int) -> bool:
    """The criterion of Goldstein (1994): t makes r a dead end.

    E_i(r) - E_i(t) + sum_j min_s [E_ij(r, s) - E_ij(t, s)] > 0,
    with s over the live rotamers of each residue j != i.
    """
    g = self_e[i][r] - self_e[i][t]
    for j in range(len(self_e)):
        if j == i:
            continue
        g += min(pair_energy(pair_e, i, r, j, s) - pair_energy(pair_e, i, t, j, s) for s in live[j])
    return g > 0


Criterion = Callable[[SelfE, PairE, Live, int, int, int], bool]

CRITERIA: Dict[str, Criterion] = {"desmet": desmet, "goldstein": goldstein}


def dead_end_elimination(
    self_e: SelfE, pair_e: PairE, criterion: str = "goldstein", rng: Optional[random.Random] = None
) -> Live:
    """Remove dead-end rotamers until no test succeeds. Return the live sets, sorted.

    Each residue keeps at least one rotamer, because a rotamer is removed
    only when a different live rotamer of the same residue beats it.
    Every global minimum of E uses only live rotamers. If rng is given, each
    pass visits the residues and the rotamers in a random order; the final
    sets do not depend on the order.
    Cost: O(n^3 p^4) time for n residues with at most p rotamers each.
    """
    test = CRITERIA[criterion]
    live: Live = [list(range(len(row))) for row in self_e]
    changed = True
    while changed:  # @line L1 @line L9
        changed = False  # @line L2
        residues = list(range(len(self_e)))
        if rng is not None:
            rng.shuffle(residues)
        for i in residues:  # @line L3
            candidates = list(live[i])
            if rng is not None:
                rng.shuffle(candidates)
            for r in candidates:  # @line L4
                for t in live[i]:  # @line L5
                    if t != r and test(self_e, pair_e, live, i, r, t):  # @line L6
                        live[i].remove(r)  # @line L7
                        changed = True
                        break  # @line L8
    return [sorted(s) for s in live]  # @line L10


def brute_force(self_e: SelfE, pair_e: PairE, live: Live = None) -> Tuple[object, List[Tuple[int, ...]]]:
    """The least energy over all assignments from the live sets, and every assignment that reaches it."""
    if live is None:
        live = [list(range(len(row))) for row in self_e]
    best = None
    argmins: List[Tuple[int, ...]] = []
    for x in product(*live):
        e = total_energy(self_e, pair_e, x)
        if best is None or e < best:
            best, argmins = e, [x]
        elif e == best:
            argmins.append(x)
    return best, argmins


def solve(self_e: SelfE, pair_e: PairE, criterion: str = "goldstein") -> Tuple[object, Tuple[int, ...], Live]:
    """DEE, then an exhaustive search over the live rotamers. Return (energy, assignment, live sets)."""
    live = dead_end_elimination(self_e, pair_e, criterion)  # @line L11
    best, argmins = brute_force(self_e, pair_e, live)  # @line L12
    return best, argmins[0], live
