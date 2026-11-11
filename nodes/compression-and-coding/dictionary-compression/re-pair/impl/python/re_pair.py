# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/re-pair/. The authors are listed in prov/GPGX6R.jsonl.

"""Re-Pair (Larsson and Moffat): replace the most frequent pair until no pair repeats.

The input is a sequence of integer symbols, all smaller than ``first``. The output is
the list of rules ``(A, a, b)`` for ``A -> a b`` in the order of creation, and the final
sequence. The frequency of a pair is the number of non-overlapping occurrences, so a
run of ``k`` equal symbols counts as ``k // 2`` occurrences of ``aa``. Ties between
pairs of the same frequency go to the smallest pair ``(a, b)``.

This version keeps the positions in a doubly linked list, the occurrences of each pair
in a hash set, the runs of equal symbols by their two ends, and the frequencies in a
binary heap with lazy deletion. The time is O(n log n) for n symbols, with expected
O(1) hash operations. Larsson and Moffat use a bucket queue and reach O(n) expected time.
"""

from heapq import heappop, heappush
from typing import Sequence

Rule = tuple[int, int, int]


def re_pair(text: Sequence[int], first: int = 256) -> tuple[list[Rule], list[int]]:
    """Return (rules, final sequence) of Re-Pair on text. Precondition: 0 <= s < first."""
    n = len(text)
    sym = list(text)
    if any(s < 0 or s >= first for s in sym):
        raise ValueError("each symbol must be in range(first)")
    prv = list(range(-1, n - 1))  # @line L1
    nxt = list(range(1, n + 1))
    if n:
        nxt[-1] = -1
    occ: dict[tuple[int, int], set[int]] = {}
    cnt: dict[tuple[int, int], int] = {}
    heap: list[tuple[int, int, int]] = []
    run_end: dict[int, int] = {}  # start of a run of length >= 2 -> its end
    run_start: dict[int, int] = {}  # end -> start
    run_len: dict[int, int] = {}  # start -> length

    def bump(pair: tuple[int, int], delta: int) -> None:
        c = cnt.get(pair, 0) + delta
        if c:
            cnt[pair] = c
        else:
            cnt.pop(pair, None)
        if c >= 2:
            heappush(heap, (-c, pair[0], pair[1]))

    def add_pair(i: int) -> None:  # the pair at node i, two different symbols
        pair = (sym[i], sym[nxt[i]])
        occ.setdefault(pair, set()).add(i)
        bump(pair, 1)

    def drop_pair(i: int) -> None:
        pair = (sym[i], sym[nxt[i]])
        occ[pair].discard(i)
        bump(pair, -1)

    def new_run(s: int, e: int, length: int) -> None:
        run_end[s], run_start[e], run_len[s] = e, s, length
        occ.setdefault((sym[s], sym[s]), set()).add(s)

    def run_lose_end(e: int) -> None:  # e is the right end of a run, and it leaves the run
        s = run_start.pop(e)
        length = run_len.pop(s)
        del run_end[s]
        a = sym[e]
        occ[(a, a)].discard(s)
        bump((a, a), (length - 1) // 2 - length // 2)
        if length - 1 >= 2:
            new_run(s, prv[e], length - 1)

    def run_lose_start(s: int) -> None:  # s is the left end of a run, and it leaves the run
        e = run_end.pop(s)
        length = run_len.pop(s)
        del run_start[e]
        a = sym[s]
        occ[(a, a)].discard(s)
        bump((a, a), (length - 1) // 2 - length // 2)
        if length - 1 >= 2:
            new_run(nxt[s], e, length - 1)

    def run_grow(p: int, i: int) -> None:  # sym[p] == sym[i], i is new right of p
        a = sym[i]
        if p in run_start:
            s = run_start.pop(p)
            length = run_len[s]
            run_end[s], run_start[i], run_len[s] = i, s, length + 1
            bump((a, a), (length + 1) // 2 - length // 2)
        else:
            new_run(p, i, 2)
            bump((a, a), 1)

    def unlink(j: int) -> None:  # remove node j from the list
        p, q = prv[j], nxt[j]
        nxt[p] = q
        if q != -1:
            prv[q] = p

    i = 0  # @line L2
    while i < n:
        j = i
        while j + 1 < n and sym[j + 1] == sym[i]:
            j += 1
        if j > i:
            new_run(i, j, j - i + 1)
            bump((sym[i], sym[i]), (j - i + 1) // 2)
        if j + 1 < n:
            add_pair(j)
        i = j + 1
    for pair, c in cnt.items():  # @line L3
        if c >= 2:
            heappush(heap, (-c, pair[0], pair[1]))

    rules: list[Rule] = []  # @line L4
    new = first
    while heap:  # @line L5
        negc, x, y = heappop(heap)  # @line L6
        if cnt.get((x, y), 0) != -negc:
            continue  # a stale heap entry
        del cnt[(x, y)]
        places = sorted(occ.pop((x, y)))
        if x != y:
            for i in places:  # @line L7
                j = nxt[i]
                p, q = prv[i], nxt[j]
                if p != -1:  # @line L8
                    if sym[p] == x:
                        run_lose_end(i)
                    else:
                        drop_pair(p)
                if q != -1:
                    if sym[q] == y:
                        run_lose_start(j)
                    else:
                        drop_pair(j)
                sym[i] = new  # @line L9
                unlink(j)
                if p != -1:  # @line L10
                    if sym[p] == new:
                        run_grow(p, i)
                    else:
                        add_pair(p)
                if q != -1:
                    add_pair(i)
        else:
            for s in places:  # @line L7
                e = run_end.pop(s)
                length = run_len.pop(s)
                del run_start[e]
                p, q = prv[s], nxt[e]
                if p != -1:  # @line L8
                    drop_pair(p)
                if q != -1:
                    drop_pair(e)
                k, last = s, -1
                for _ in range(length // 2):
                    sym[k] = new  # @line L9
                    unlink(nxt[k])
                    if last != -1:
                        run_grow(last, k)  # @line L10
                    last, k = k, nxt[k]
                if p != -1:
                    add_pair(p)
                if q != -1 or length % 2:
                    add_pair(last)
                if length % 2 and q != -1:
                    add_pair(e)
        rules.append((new, x, y))  # @line L11
        new += 1
    out = []  # @line L12
    k = 0 if n else -1
    while k != -1:
        out.append(sym[k])
        k = nxt[k]
    return rules, out


def expand(rules: Sequence[Rule], seq: Sequence[int]) -> list[int]:
    """Expand the final sequence with the rules, with an explicit stack. Time O(output length)."""
    rhs = {a: (x, y) for a, x, y in rules}
    out: list[int] = []
    stack = list(reversed(seq))
    while stack:
        s = stack.pop()
        if s in rhs:
            x, y = rhs[s]
            stack.append(y)
            stack.append(x)
        else:
            out.append(s)
    return out


def grammar_size(rules: Sequence[Rule], seq: Sequence[int]) -> int:
    """Total length of the right-hand sides: 2 for each rule plus the final sequence."""
    return 2 * len(rules) + len(seq)
