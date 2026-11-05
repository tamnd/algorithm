# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-superstring-merge/. The authors are listed in prov/HBAFAC.jsonl.

from typing import List, Optional, Sequence, Tuple

_SEP = object()


def _prefix_function(t: Sequence[object]) -> List[int]:
    pi = [0] * len(t)
    for q in range(1, len(t)):
        k = pi[q - 1]
        while k > 0 and t[q] != t[k]:
            k = pi[k - 1]
        if t[q] == t[k]:
            k += 1
        pi[q] = k
    return pi


def overlap(x: str, y: str) -> int:
    """Length of the longest suffix of x that is a prefix of y, below min(|x|, |y|) + 1.

    Uses the prefix function of y, a separator, then x: O(|x| + |y|) time.
    """
    if not x or not y:
        return 0
    t: List[object] = list(y)
    t.append(_SEP)
    t.extend(x)
    return _prefix_function(t)[-1]


def _occurs(p: str, t: str) -> bool:
    if not p:
        return True
    u: List[object] = list(p)
    u.append(_SEP)
    u.extend(t)
    return any(v == len(p) for v in _prefix_function(u))


def reduce_strings(strings: Sequence[str]) -> List[str]:
    """Drop duplicates (keeping the first copy) and strings inside other strings.

    The order of the kept strings is the input order. O(m * n) time.
    """
    distinct: List[str] = []
    seen = set()
    for s in strings:
        if s not in seen:
            seen.add(s)
            distinct.append(s)
    kept: List[str] = []
    for i, s in enumerate(distinct):
        if not any(j != i and _occurs(s, t) for j, t in enumerate(distinct)):
            kept.append(s)
    return kept


def greedy_merge_order(strings: Sequence[str]) -> Tuple[List[str], List[Tuple[int, int, int]]]:
    """Return the reduced list and the accepted merges (i, j, w) in greedy order.

    Pairs are tried by decreasing overlap w, ties by smaller i, then smaller j,
    where i and j index the reduced list.
    """
    # @line L1
    s = reduce_strings(strings)
    m = len(s)
    # @line L2
    pairs = [(overlap(s[i], s[j]), i, j) for i in range(m) for j in range(m) if i != j]
    # @line L3
    pairs.sort(key=lambda e: (-e[0], e[1], e[2]))
    nxt: List[Optional[int]] = [None] * m
    prv: List[Optional[int]] = [None] * m
    head_of = list(range(m))  # head_of[t] is the head of the chain whose tail is t
    tail_of = list(range(m))  # tail_of[h] is the tail of the chain whose head is h
    merges: List[Tuple[int, int, int]] = []
    # @line L4
    for w, i, j in pairs:
        # @line L5
        if nxt[i] is None and prv[j] is None and head_of[i] != j:
            # @line L6
            nxt[i] = j
            prv[j] = i
            h, t = head_of[i], tail_of[j]
            head_of[t] = h
            tail_of[h] = t
            merges.append((i, j, w))
            if len(merges) == m - 1:
                break
    return s, merges


def greedy_superstring(strings: Sequence[str]) -> str:
    """Greedy superstring of the given strings; the empty string for no input.

    Time O(m * n + m^2 log m), space O(n + m^2), for m strings of total length n.
    """
    s, merges = greedy_merge_order(strings)
    m = len(s)
    if m == 0:
        return ""
    nxt: List[Optional[int]] = [None] * m
    weight = [0] * m
    has_prev = [False] * m
    for i, j, w in merges:
        nxt[i] = j
        weight[i] = w
        has_prev[j] = True
    # @line L7
    h = has_prev.index(False)
    parts = [s[h]]
    # @line L8
    while nxt[h] is not None:
        j = nxt[h]
        assert j is not None
        parts.append(s[j][weight[h] :])
        h = j
    # @line L9
    return "".join(parts)
