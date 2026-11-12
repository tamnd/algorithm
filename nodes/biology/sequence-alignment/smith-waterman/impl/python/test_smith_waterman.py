# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-waterman/. The authors are listed in prov/G3HRJ9.jsonl.

import random
from typing import Iterator

from smith_waterman import GAP, LocalAlignment, alignment_score, match_mismatch, smith_waterman

TOY = match_mismatch(2, -1)


def all_alignments(x: str, y: str) -> Iterator[tuple[str, str]]:
    """Every global alignment of x and y, as (top, bottom) rows."""
    if not x and not y:
        yield "", ""
        return
    if x and y:
        for t, b in all_alignments(x[1:], y[1:]):
            yield x[0] + t, y[0] + b
    if x:
        for t, b in all_alignments(x[1:], y):
            yield x[0] + t, GAP + b
    if y:
        for t, b in all_alignments(x, y[1:]):
            yield GAP + t, y[0] + b


def brute_substrings(x: str, y: str, s, d: int) -> int:
    """Best score over all pairs of substrings and all their global alignments."""
    best = 0
    subs_x = {x[a:b] for a in range(len(x) + 1) for b in range(a, len(x) + 1)}
    subs_y = {y[a:b] for a in range(len(y) + 1) for b in range(a, len(y) + 1)}
    for u in subs_x:
        for v in subs_y:
            for t, b in all_alignments(u, v):
                best = max(best, alignment_score(t, b, s, d))
    return best


def brute_blocks(x: str, y: str, s, d: int) -> int:
    """Best score of a run of consecutive columns of a global alignment of x and y."""
    best = 0
    for t, b in all_alignments(x, y):
        for lo in range(len(t)):
            for hi in range(lo + 1, len(t) + 1):
                best = max(best, alignment_score(t[lo:hi], b[lo:hi], s, d))
    return best


def check(x: str, y: str, s, d: int, r: LocalAlignment) -> None:
    assert len(r.top) == len(r.bottom)
    assert r.top.replace(GAP, "") == x[r.x_start : r.x_end]
    assert r.bottom.replace(GAP, "") == y[r.y_start : r.y_end]
    assert alignment_score(r.top, r.bottom, s, d) == r.score
    if r.score > 0 and d >= 0:
        # An optimal local alignment starts and ends with an aligned pair.
        assert GAP not in (r.top[0], r.bottom[0], r.top[-1], r.bottom[-1])


def test_worked_example() -> None:
    r = smith_waterman("TCAGTTGCA", "GAGTGCAT", TOY, 2)
    assert r == LocalAlignment(10, "AGTTGCA", "AG-TGCA", 2, 9, 1, 7)


def test_edges() -> None:
    assert smith_waterman("", "", TOY, 2) == LocalAlignment(0, "", "", 0, 0, 0, 0)
    assert smith_waterman("ACG", "", TOY, 2).score == 0
    assert smith_waterman("AAA", "CCC", TOY, 2) == LocalAlignment(0, "", "", 0, 0, 0, 0)
    assert smith_waterman("GGACGTT", "ACG", TOY, 2)[:3] == (6, "ACG", "ACG")
    # A positive expected score: every pair scores +1, so the alignment spans both strings.
    r = smith_waterman("ACGTAC", "TTGACA", match_mismatch(1, 1), 10)
    assert (r.score, r.x_start, r.x_end, r.y_start, r.y_end) == (6, 0, 6, 0, 6)


def test_against_substring_brute_force() -> None:
    rng = random.Random(1981)
    for _ in range(150):
        x = "".join(rng.choice("ACG") for _ in range(rng.randrange(5)))
        y = "".join(rng.choice("ACG") for _ in range(rng.randrange(5)))
        s = match_mismatch(rng.randrange(1, 4), rng.randrange(-4, 1))
        d = rng.randrange(0, 5)
        r = smith_waterman(x, y, s, d)
        assert r.score == brute_substrings(x, y, s, d)
        check(x, y, s, d, r)


def test_against_block_brute_force() -> None:
    rng = random.Random(147)
    alphabet = "ACGT"
    for _ in range(400):
        table = {(a, b): rng.randrange(-4, 4) for a in alphabet for b in alphabet}
        s = lambda a, b, t=table: t[a, b]
        x = "".join(rng.choice(alphabet) for _ in range(rng.randrange(6)))
        y = "".join(rng.choice(alphabet) for _ in range(rng.randrange(6)))
        d = rng.randrange(0, 5)
        r = smith_waterman(x, y, s, d)
        assert r.score == brute_blocks(x, y, s, d)
        check(x, y, s, d, r)
