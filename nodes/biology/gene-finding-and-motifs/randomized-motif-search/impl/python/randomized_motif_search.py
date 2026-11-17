# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-motif-search/. The authors are listed in prov/V85QPB.jsonl.
"""Randomized motif search (RandomizedMotifSearch of Compeau and Pevzner) with
random restarts and Laplace pseudocounts.

Positions are 0-based in this code; the page numbers them from 1.
"""

import random
from typing import List, NamedTuple, Sequence, Tuple

from bioseq import DNA, kmers

_INDEX = {a: k for k, a in enumerate(DNA)}


class RunResult(NamedTuple):
    """The windows, 0-based starts and score at the end of one run, and the
    number of profile steps the run made."""

    motifs: Tuple[str, ...]
    starts: Tuple[int, ...]
    score: int
    steps: int


class RandomizedResult(NamedTuple):
    """The best windows over all restarts, their starts and score, and the
    number of profile steps of each restart."""

    motifs: Tuple[str, ...]
    starts: Tuple[int, ...]
    score: int
    steps: Tuple[int, ...]


def motif_score(windows: Sequence[str]) -> int:
    """The number of letters that differ from the consensus: sum over columns of n - max count."""
    n = len(windows)
    return sum(n - max(col.count(a) for a in DNA) for col in zip(*windows))


def count_matrix(windows: Sequence[str], L: int, pseudo: int = 1) -> List[List[int]]:
    """counts[j][a] = the number of windows with letter a in column j, plus pseudo.

    The profile is counts[j][a] / (n + 4 pseudo); every row has the same sum.
    """
    counts = [[pseudo] * 4 for _ in range(L)]
    for w in windows:
        for j, a in enumerate(w):
            counts[j][_INDEX[a]] += 1
    return counts


def most_probable(seq: str, counts: List[List[int]]) -> int:
    """The 0-based start of the first window of seq with the largest product of counts.

    The rows of counts have equal sums, so this is the window with the largest
    profile probability. Integers keep the comparison exact.
    """
    L = len(counts)
    best_q, best_v = 0, -1
    for q, w in enumerate(kmers(seq, L)):
        v = 1
        for j, a in enumerate(w):
            v *= counts[j][_INDEX[a]]
        if v > best_v:
            best_q, best_v = q, v
    return best_q


def _check(seqs: Sequence[str], L: int) -> None:
    if L <= 0:
        raise ValueError("L must be positive")
    if not seqs:
        raise ValueError("need at least one sequence")
    for s in seqs:
        if len(s) < L or set(s) - set(DNA):
            raise ValueError("sequences must be over ACGT with length at least L")


def improve(seqs: Sequence[str], L: int, starts: Sequence[int], pseudo: int = 1) -> RunResult:
    """One run from the given starts: replace the windows by the most probable
    windows of their own profile while the score drops strictly.

    This is lines L4 to L9 of the page, without the random draw.
    """
    _check(seqs, L)
    if len(starts) != len(seqs) or any(not 0 <= q <= len(s) - L for s, q in zip(seqs, starts)):
        raise ValueError("one valid start per sequence is needed")
    cur = tuple(starts)
    motifs = tuple(s[q:q + L] for s, q in zip(seqs, cur))
    sc = motif_score(motifs)  # @line L4
    steps = 0
    while True:  # @line L5
        counts = count_matrix(motifs, L, pseudo)  # @line L6
        nxt = tuple(most_probable(s, counts) for s in seqs)  # @line L7
        steps += 1
        new_motifs = tuple(s[q:q + L] for s, q in zip(seqs, nxt))
        new_sc = motif_score(new_motifs)
        if new_sc < sc:  # @line L8
            cur, motifs, sc = nxt, new_motifs, new_sc
        else:
            break  # @line L9
    return RunResult(motifs, cur, sc, steps)


def randomized_motif_search(seqs: Sequence[str], L: int, restarts: int, seed: int = 0,
                            pseudo: int = 1) -> RandomizedResult:
    """Run improve from random starts `restarts` times and keep the best result.

    Draw order: random.Random(seed); for each restart, one rng.randrange(W_i)
    per sequence, in the order of the sequences. Among restarts with the same
    score the first one wins. Each restart makes at most
    L (n - ceil(n / 4)) + 1 profile steps, each of cost O(n W L).
    """
    _check(seqs, L)
    if restarts < 1:
        raise ValueError("restarts must be at least 1")
    if pseudo < 1:
        raise ValueError("pseudo must be at least 1")
    rng = random.Random(seed)
    best = None  # @line L1
    steps = []
    for _ in range(restarts):  # @line L2
        starts = [rng.randrange(len(s) - L + 1) for s in seqs]  # @line L3
        run = improve(seqs, L, starts, pseudo)
        steps.append(run.steps)
        if best is None or run.score < best.score:  # @line L10
            best = run
    return RandomizedResult(best.motifs, best.starts, best.score, tuple(steps))  # @line L11
