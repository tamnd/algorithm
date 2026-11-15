# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/positional-intersection/. The authors are listed in prov/DS6M6D.jsonl.

from collections import deque
from typing import Any, Sequence

Entry = tuple[int, Sequence[int]]


def positional_intersect(
    p1: Sequence[Entry], p2: Sequence[Entry], k: int, stats: dict[str, int] | None = None
) -> list[tuple[int, int, int]]:
    """Return the triples (d, x, y) with d in both lists, x a position of the first term in d,
    y a position of the second term in d, and |x - y| <= k, in increasing order of (d, x, y).

    Each list holds (doc_id, positions) pairs with strictly increasing ids, and each
    positions list is strictly increasing. Precondition: k >= 0.

    If stats is a dict, it receives "doc_steps" (the steps of the merge of the ids) and
    "pos_steps" (the passes of the inner scan of the second position list).
    """
    out: list[tuple[int, int, int]] = []
    doc_steps = pos_steps = 0
    i = j = 0  # @line L1
    while i < len(p1) and j < len(p2):  # @line L2
        doc_steps += 1
        d1, d2 = p1[i][0], p2[j][0]
        if d1 == d2:  # @line L3
            xs, ys = p1[i][1], p2[j][1]
            window: deque[int] = deque()  # @line L4
            b = 0
            for x in xs:  # @line L5
                while b < len(ys):  # @line L6
                    pos_steps += 1
                    y = ys[b]
                    if abs(x - y) <= k:  # @line L7
                        window.append(y)
                    elif y > x:  # @line L8
                        break
                    b += 1  # @line L9
                while window and abs(window[0] - x) > k:  # @line L10
                    window.popleft()
                for y in window:  # @line L11
                    out.append((d1, x, y))
            i += 1  # @line L12
            j += 1
        elif d1 < d2:  # @line L13
            i += 1
        else:
            j += 1  # @line L14
    if stats is not None:
        stats["doc_steps"] = doc_steps
        stats["pos_steps"] = pos_steps
    return out  # @line L15


def phrase_matches(lists: Sequence[Sequence[Entry]], stats: dict[str, int] | None = None) -> list[tuple[int, int]]:
    """Return the pairs (d, x) such that term r of the phrase stands at position x + r of
    document d for each r, where lists[r] is the positional list of term r.

    The ids are intersected by a merge, and in each common document the position lists
    are intersected after the offset of each term is taken off. Precondition: at least
    one list. If stats is a dict, it receives "steps", the number of passes of the inner
    loops.
    """
    out: list[tuple[int, int]] = []
    steps = 0
    idx = [0] * len(lists)
    while all(idx[r] < len(lists[r]) for r in range(len(lists))):
        steps += 1
        top = max(lists[r][idx[r]][0] for r in range(len(lists)))
        moved = False
        for r in range(len(lists)):
            if lists[r][idx[r]][0] < top:
                idx[r] += 1
                moved = True
        if moved:
            continue
        cand = list(lists[0][idx[0]][1])
        for r in range(1, len(lists)):
            ys = lists[r][idx[r]][1]
            keep: list[int] = []
            b = 0
            for x in cand:
                while b < len(ys) and ys[b] - r < x:
                    steps += 1
                    b += 1
                steps += 1
                if b < len(ys) and ys[b] - r == x:
                    keep.append(x)
            cand = keep
        out.extend((top, x) for x in cand)
        for r in range(len(lists)):
            idx[r] += 1
    if stats is not None:
        stats["steps"] = steps
    return out
