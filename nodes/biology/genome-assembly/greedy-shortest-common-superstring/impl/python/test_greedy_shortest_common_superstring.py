# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-shortest-common-superstring/. The authors are listed in prov/D91MJT.jsonl.

import itertools
import random
from fractions import Fraction
from typing import List, Sequence, Tuple

from greedy_shortest_common_superstring import (
    greedy_assemble,
    greedy_superstring,
    overlap,
    reduce_reads,
)


def naive_ov(a: str, b: str) -> int:
    for k in range(min(len(a), len(b)) - 1, 0, -1):
        if a[len(a) - k:] == b[:k]:
            return k
    return 0


def naive_greedy(reads: Sequence[str], tau: int) -> List[str]:
    # String form: recompute overlaps of the current strings at every round.
    s = reduce_reads(reads)
    cur: List[Tuple[str, int, int]] = [(r, i, i) for i, r in enumerate(s)]
    while len(cur) >= 2:
        best = None
        for x in range(len(cur)):
            for y in range(len(cur)):
                if x == y:
                    continue
                key = (naive_ov(cur[x][0], cur[y][0]), -cur[x][2], -cur[y][1])
                if best is None or key > best[0]:
                    best = (key, x, y)
        assert best is not None
        (w, _, _), x, y = best
        if w < tau:
            break
        a, b = cur[x], cur[y]
        merged = (a[0] + b[0][w:], a[1], b[2])
        cur = [c for k, c in enumerate(cur) if k not in (x, y)] + [merged]
    cur.sort(key=lambda c: c[1])
    return [c[0] for c in cur]


def scs_length(reads: Sequence[str]) -> int:
    s = reduce_reads(reads)
    if not s:
        return 0
    total = sum(len(r) for r in s)
    best = 0
    for perm in itertools.permutations(range(len(s))):
        o = sum(naive_ov(s[perm[q]], s[perm[q + 1]]) for q in range(len(s) - 1))
        best = max(best, o)
    return total - best


def longest_repeat(x: str) -> int:
    r = 0
    for k in range(1, len(x)):
        seen = set()
        found = False
        for p in range(len(x) - k + 1):
            u = x[p:p + k]
            if u in seen:
                found = True
                break
            seen.add(u)
        if not found:
            break
        r = k
    return r


def test_overlap() -> None:
    assert overlap("ACGTT", "GTTCA") == 3
    assert overlap("aaa", "aaa") == 2
    assert overlap("ab", "ab") == 0
    assert overlap("", "x") == 0
    rng = random.Random(1)
    for _ in range(500):
        a = "".join(rng.choice("ab") for _ in range(rng.randrange(0, 7)))
        b = "".join(rng.choice("ab") for _ in range(rng.randrange(0, 7)))
        assert overlap(a, b) == naive_ov(a, b)


def test_page_example() -> None:
    genome = "ATGGCGTGCAATG"
    reads = ["ATGGCGT", "GGCGTGC", "CGTGCAA", "TGCAATG", "GCGTG"]
    assert reduce_reads(reads) == ["ATGGCGT", "GGCGTGC", "CGTGCAA", "TGCAATG"]
    assert greedy_assemble(reads, 3) == [genome]
    assert greedy_superstring(reads) == genome


def test_repeat_example() -> None:
    reads = ["CATTGA", "TTGACA", "GACAGT", "CAGTTG", "GTTGAC", "TTGACG"]
    out = greedy_superstring(reads)
    assert out == "CATTGACGTTGACAGTTG"
    assert scs_length(reads) == len("CATTGACAGTTGACG") == 15
    assert greedy_assemble(reads, 2) == ["CATTGACG", "GTTGACAGTTG"]


def test_edges() -> None:
    assert greedy_assemble([]) == []
    assert greedy_superstring([]) == ""
    assert greedy_superstring(["", ""]) == ""
    assert greedy_superstring(["abc"]) == "abc"
    assert greedy_superstring(["abc", "abc", "b"]) == "abc"
    assert greedy_assemble(["abc", "xyz"], 1) == ["abc", "xyz"]
    assert greedy_assemble(["abc", "bcd", "cde"], 3) == ["abc", "bcd", "cde"]
    assert greedy_assemble(["abc", "bcd", "cde"], 2) == ["abcde"]


def test_random_against_string_form_and_optimum() -> None:
    rng = random.Random(20261112)
    for _ in range(600):
        k = rng.randrange(1, 7)
        alphabet = rng.choice(["ab", "acgt"])
        reads = ["".join(rng.choice(alphabet) for _ in range(rng.randrange(1, 7))) for _ in range(k)]
        tau = rng.randrange(0, 4)
        assert greedy_assemble(reads, tau) == naive_greedy(reads, tau)
        out = greedy_superstring(reads)
        for r in reads:
            assert r in out
        assert Fraction(len(out)) <= Fraction(7, 2) * scs_length(reads)


def test_reconstruction_when_overlaps_exceed_repeats() -> None:
    rng = random.Random(7)
    for _ in range(300):
        g = rng.randrange(12, 50)
        x = "".join(rng.choice("ACGT") for _ in range(g))
        r = longest_repeat(x)
        reads: List[str] = []
        start = 0
        while True:
            length = rng.randrange(r + 2, r + 9)
            end = min(start + length, g)
            reads.append(x[start:end])
            if end == g:
                break
            start = rng.randrange(max(start + 1, end - length + 1), end - r)
        for _ in range(rng.randrange(0, 4)):
            p = rng.randrange(0, g)
            q = rng.randrange(p + 1, g + 1)
            if any(x.find(rd) <= p and q <= x.find(rd) + len(rd) for rd in reads if len(rd) > r):
                reads.append(x[p:q])
        rng.shuffle(reads)
        assert greedy_assemble(reads, r + 1) == [x]
        assert greedy_superstring(reads) == x
