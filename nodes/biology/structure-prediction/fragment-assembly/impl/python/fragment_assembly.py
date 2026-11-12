# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fragment-assembly/. The authors are listed in prov/B7NM52.jsonl.
"""Fragment assembly by Monte Carlo fragment insertion, on a toy lattice model.

The model stands in for the backbone torsion angles of a real protein. A
chain of n residues lies on the square lattice. Residue 0 is at (0, 0) and
residue 1 at (1, 0). Each later residue turns left (L), goes straight (S) or
turns right (R) relative to the last bond. So a conformation is a word w of
n - 2 letters over "LSR", and residue i + 2 is placed by the letter w[i].

A fragment of length k is a word of k letters. The library gives, for each
window start j, a list of fragments taken from known structures. One move
copies a fragment into w[j .. j + k - 1], as Rosetta copies the torsion
angles of a 9 or 3 residue fragment into the chain. The score is the HP
energy (minus the number of H-H contacts), and a move that makes two
residues collide is rejected (infinite energy). Moves are accepted by the
Metropolis criterion at a temperature that falls geometrically.

This is a heuristic. It returns the best conformation that it visits, and
no bound on the gap to the optimum holds after a finite number of steps.
Cost: O(n) time per step to rebuild and score the chain, so O(S n) for S
steps in total, and O(n) extra space besides the library.
"""

import math
import random
from typing import Optional

Point = tuple[int, int]
Library = dict[int, list[str]]

# heading vectors in counterclockwise order: +x, +y, -x, -y
HEADINGS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
TURN = {"L": 1, "S": 0, "R": -1}


def build(word: str) -> list[Point]:
    """The lattice coordinates of the chain with n = len(word) + 2 residues."""
    coords = [(0, 0), (1, 0)]
    h = 0
    for c in word:
        h = (h + TURN[c]) % 4
        x, y = coords[-1]
        dx, dy = HEADINGS[h]
        coords.append((x + dx, y + dy))
    return coords


def score(seq: str, word: str) -> Optional[int]:
    """HP energy of the chain, or None when two residues collide (infinite energy)."""
    coords = build(word)
    where: dict[Point, int] = {}
    for i, p in enumerate(coords):
        if p in where:
            return None
        where[p] = i
    contacts = 0
    for i, (x, y) in enumerate(coords):
        if seq[i] != "H":
            continue
        for dx, dy in HEADINGS:
            j = where.get((x + dx, y + dy))
            if j is not None and j > i + 1 and seq[j] == "H":
                contacts += 1
    return -contacts


def accept(e_old: int, e_new: Optional[int], temp: float, u: float) -> bool:
    """Metropolis criterion: accept with probability min(1, exp(-(e_new - e_old) / temp))."""
    if e_new is None:
        return False
    if e_new <= e_old:
        return True
    return u < math.exp(-(e_new - e_old) / temp)


def pick_fragments(seq: str, database: list[tuple[str, str]], k: int, top: int) -> Library:
    """For each window, the `top` fragments whose local HP pattern is closest to the target.

    database holds pairs (hp sequence, word) of known structures. A fragment for
    window j is a piece db_word[a .. a + k - 1]; its local sequence is
    db_seq[a .. a + k + 1], the residues that the k turns involve. The distance
    is the Hamming distance to seq[j .. j + k + 1]. Ties keep database order.
    """
    n = len(seq)
    lib: Library = {}
    for j in range(n - 1 - k):
        target = seq[j:j + k + 2]
        cands = []
        for s, w in database:
            for a in range(len(w) - k + 1):
                d = sum(1 for x, y in zip(target, s[a:a + k + 2]) if x != y)
                cands.append((d, len(cands), w[a:a + k]))
        cands.sort()
        frags: list[str] = []
        for _, _, f in cands:
            if f not in frags:
                frags.append(f)
            if len(frags) == top:
                break
        lib[j] = frags
    return lib


def full_library(n: int, k: int) -> Library:
    """Every word of length k at every window: the move set then reaches every conformation."""
    words = [""]
    for _ in range(k):
        words = [w + c for w in words for c in "LSR"]
    return {j: list(words) for j in range(n - 1 - k)}


def fragment_assembly(
    seq: str,
    stages: list[tuple[int, Library, int]],
    t_start: float,
    t_end: float,
    rng: random.Random,
) -> tuple[int, str]:
    """Assemble a fold of seq from fragments. Returns (best energy, best word).

    stages is a list of (k, library, steps): first long fragments, then short
    ones, as in Rosetta. Precondition: len(seq) >= 3, every fragment in a
    library for k has length k, every window 0 .. n - 2 - k has a nonempty list,
    and 0 < t_end <= t_start.
    """
    n = len(seq)
    w = "S" * (n - 2)                                  # @line L1
    e = score(seq, w)                                  # @line L2
    assert e is not None
    best_e, best_w = e, w                              # @line L2
    for k, lib, steps in stages:                       # @line L3
        for t in range(steps):                         # @line L4
            frac = t / (steps - 1) if steps > 1 else 1.0
            temp = t_start * (t_end / t_start) ** frac  # @line L5
            j = rng.randrange(n - 1 - k)               # @line L6
            f = rng.choice(lib[j])                     # @line L7
            w2 = w[:j] + f + w[j + k:]                 # @line L8
            e2 = score(seq, w2)                        # @line L9
            if accept(e, e2, temp, rng.random()):      # @line L10
                w, e = w2, e2                          # @line L11
                if e < best_e:                         # @line L12
                    best_e, best_w = e, w              # @line L13
    return best_e, best_w                              # @line L14
