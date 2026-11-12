# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rosetta/. The authors are listed in prov/2J2HZZ.jsonl.
"""The two-resolution Rosetta ab initio protocol, on a toy lattice model.

Rosetta (Rohl, Strauss, Misura and Baker 2004) folds a chain in two phases.
A low-resolution phase represents each side chain by one centroid and runs
Monte Carlo fragment insertion, first with 9-residue and then with 3-residue
fragments. A high-resolution phase adds all side-chain atoms, packs rotamers,
and refines with small backbone moves, rotamer changes and minimization under
the full-atom energy. This file keeps that structure on the square lattice:

- Backbone: residue 0 at (0, 0), residue 1 at (1, 0), then a word w over
  "LSR" (turn left, go straight, turn right) places residues 2 .. n - 1.
- Centroid score: minus the number of H-H contacts between backbone beads
  (the HP energy); two beads on one site is a clash (infinite energy).
- Full-atom model: residue i also has one side-chain bead on a lattice
  neighbour of its backbone bead. The rotamer r_i in {0, 1, 2, 3} is a turn
  relative to the heading of the bond into residue i, so side chains move
  rigidly with the backbone. The full-atom score is minus the number of
  pairs of H side-chain beads at distance 1; any two of the 2n beads on one
  site is a clash.

Like Rosetta, this is a heuristic: no bound on the distance to the optimum
holds after a finite number of steps. What holds is that the output is a
valid (clash-free) structure, its reported energy is exact, and it is a local
minimum of the full-atom score under single moves (see the correctness proof).
Cost: O(n) per Monte Carlo step, so O((S + R) n) for S centroid and R
refinement steps; the final descent costs O(n^2) per round.
"""

import math
import random
from typing import Optional

Point = tuple[int, int]
HEADINGS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
TURN = {"L": 1, "S": 0, "R": -1}


def backbone(word: str) -> tuple[list[Point], list[int]]:
    """Backbone coordinates and the heading index of the bond into each residue."""
    coords, heads = [(0, 0), (1, 0)], [0, 0]
    h = 0
    for c in word:
        h = (h + TURN[c]) % 4
        x, y = coords[-1]
        dx, dy = HEADINGS[h]
        coords.append((x + dx, y + dy))
        heads.append(h)
    return coords, heads


def centroid_score(seq: str, word: str) -> Optional[int]:
    """Low-resolution score: HP energy of the backbone beads, None on a clash."""
    coords, _ = backbone(word)
    where: dict[Point, int] = {}
    for i, p in enumerate(coords):
        if p in where:
            return None
        where[p] = i
    c = 0
    for i, (x, y) in enumerate(coords):
        if seq[i] == "H":
            for dx, dy in HEADINGS:
                j = where.get((x + dx, y + dy))
                if j is not None and j > i + 1 and seq[j] == "H":
                    c += 1
    return -c


def side_chains(word: str, rot: list[int]) -> tuple[list[Point], list[Point]]:
    """Backbone beads and side-chain beads of a full-atom structure."""
    coords, heads = backbone(word)
    sc = []
    for (x, y), h, r in zip(coords, heads, rot):
        dx, dy = HEADINGS[(h + r) % 4]
        sc.append((x + dx, y + dy))
    return coords, sc


def full_atom_score(seq: str, word: str, rot: list[int]) -> Optional[int]:
    """High-resolution score: minus the H-H side-chain contacts, None on a clash."""
    coords, sc = side_chains(word, rot)
    if len(set(coords + sc)) != 2 * len(coords):
        return None
    where = {p: i for i, p in enumerate(sc)}
    c = 0
    for i, (x, y) in enumerate(sc):
        if seq[i] == "H":
            for dx, dy in HEADINGS:
                j = where.get((x + dx, y + dy))
                if j is not None and j > i and seq[j] == "H":
                    c += 1
    return -c


def accept(e_old: int, e_new: Optional[int], temp: float, u: float) -> bool:
    """Metropolis criterion with an infinite energy for a clash."""
    if e_new is None:
        return False
    return e_new <= e_old or u < math.exp(-(e_new - e_old) / temp)


def fragment_stage(seq, word, k, lib, steps, t0, t1, rng):
    """Monte Carlo fragment insertion under the centroid score; returns the best word."""
    n = len(seq)
    e = centroid_score(seq, word)
    best_e, best_w = e, word
    for t in range(steps):
        temp = t0 * (t1 / t0) ** (t / max(steps - 1, 1))
        j = rng.randrange(n - 1 - k)
        w2 = word[:j] + rng.choice(lib[j]) + word[j + k:]
        e2 = centroid_score(seq, w2)
        if accept(e, e2, temp, rng.random()):
            word, e = w2, e2
            if e < best_e:
                best_e, best_w = e, word
    return best_w


def pack(seq: str, word: str) -> Optional[list[int]]:
    """Rotamer packing: a clash-free assignment by backtracking, then rotamer trials.

    Rotamer trials visit residues in order and give each the rotamer of lowest
    full-atom score with the others fixed, until a full pass changes nothing.
    Returns None when no clash-free assignment exists. Explicit stack.
    """
    n = len(seq)
    coords, heads = backbone(word)
    taken = set(coords)
    rot: list[int] = []
    choice = [0]
    while len(rot) < n:
        if not choice:
            return None
        i = len(rot)
        r = choice[-1]
        if r == 4:
            choice.pop()
            if rot:
                old = rot.pop()
                dx, dy = HEADINGS[(heads[i - 1] + old) % 4]
                taken.discard((coords[i - 1][0] + dx, coords[i - 1][1] + dy))
            continue
        choice[-1] = r + 1
        dx, dy = HEADINGS[(heads[i] + r) % 4]
        p = (coords[i][0] + dx, coords[i][1] + dy)
        if p in taken:
            continue
        taken.add(p)
        rot.append(r)
        choice.append(0)
    e = full_atom_score(seq, word, rot)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for r in range(4):
                trial = rot[:i] + [r] + rot[i + 1:]
                e2 = full_atom_score(seq, word, trial)
                if e2 is not None and e2 < e:
                    rot, e, changed = trial, e2, True
    return rot


def neighbours(word: str, rot: list[int]):
    """The single moves: one backbone letter or one rotamer changed."""
    for i in range(len(word)):
        for c in "LSR":
            if c != word[i]:
                yield word[:i] + c + word[i + 1:], rot
    for i in range(len(rot)):
        for r in range(4):
            if r != rot[i]:
                yield word, rot[:i] + [r] + rot[i + 1:]


def rosetta(
    seq: str,
    centroid_stages: list[tuple[int, dict[int, list[str]], int]],
    refine_steps: int,
    rng: random.Random,
    t_cen: tuple[float, float] = (2.0, 0.5),
    t_fa: tuple[float, float] = (1.0, 0.1),
) -> tuple[int, str, list[int]]:
    """Fold seq with the two-phase protocol. Returns (full-atom energy, word, rotamers).

    centroid_stages is a list of (k, fragment library, steps), long fragments
    first. Precondition: len(seq) >= 3 and each library has a nonempty list of
    length-k words for every window 0 .. n - 2 - k.
    """
    n = len(seq)
    word = "S" * (n - 2)                                         # @line L1
    for k, lib, steps in centroid_stages:                        # @line L2
        word = fragment_stage(seq, word, k, lib, steps, t_cen[0], t_cen[1], rng)  # @line L3
    rot = pack(seq, word)                                        # @line L4
    if rot is None:                                              # @line L5
        word = "S" * (n - 2)                                     # @line L5
        rot = pack(seq, word)                                    # @line L5
    assert rot is not None
    e = full_atom_score(seq, word, rot)                          # @line L6
    best = (e, word, rot)                                        # @line L6
    for t in range(refine_steps):                                # @line L7
        temp = t_fa[0] * (t_fa[1] / t_fa[0]) ** (t / max(refine_steps - 1, 1))
        if rng.random() < 0.5:                                   # @line L8
            i = rng.randrange(n - 2)                             # @line L8
            w2, r2 = word[:i] + rng.choice("LSR") + word[i + 1:], rot  # @line L8
        else:
            i = rng.randrange(n)                                 # @line L9
            w2, r2 = word, rot[:i] + [rng.randrange(4)] + rot[i + 1:]  # @line L9
        e2 = full_atom_score(seq, w2, r2)                        # @line L10
        if accept(e, e2, temp, rng.random()):                    # @line L11
            word, rot, e = w2, r2, e2                            # @line L11
            if e < best[0]:                                      # @line L12
                best = (e, word, rot)                            # @line L12
    e, word, rot = best                                          # @line L13
    improved = True
    while improved:                                              # @line L14
        improved = False
        for w2, r2 in neighbours(word, rot):                     # @line L15
            e2 = full_atom_score(seq, w2, r2)
            if e2 is not None and e2 < e:                        # @line L16
                word, rot, e, improved = w2, r2, e2, True        # @line L16
                break
    return e, word, rot                                          # @line L17
