# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/set-horspool/. The authors are listed in prov/3G04XE.jsonl.

from collections.abc import Hashable, Sequence


def build(patterns: Sequence[Sequence[Hashable]]):
    """Return (children, out, lmin, shift) for the nonempty patterns.

    children[v] maps a character to the child of node v in the trie of the reversed
    patterns, out[v] lists the indices j whose reversed pattern spells node v, lmin is the
    shortest nonempty length, and shift maps a character to its shift (lmin if absent).
    """
    children: list[dict[Hashable, int]] = [{}]
    out: list[list[int]] = [[]]
    for j, pat in enumerate(patterns):
        if len(pat) == 0:
            continue
        v = 0
        for ch in reversed(pat):
            nxt = children[v].get(ch)
            if nxt is None:
                nxt = len(children)
                children[v][ch] = nxt
                children.append({})
                out.append([])
            v = nxt
        out[v].append(j)
    lmin = min(len(pat) for pat in patterns if len(pat) > 0)  # @line L4
    shift: dict[Hashable, int] = {}  # @line L5
    for pat in patterns:  # @line L6
        if len(pat) == 0:
            continue
        ell = len(pat)
        for i in range(ell - lmin, ell - 1):
            d = ell - 1 - i
            if d < shift.get(pat[i], lmin):
                shift[pat[i]] = d
    return children, out, lmin, shift


def set_horspool(
    text: Sequence[Hashable],
    patterns: Sequence[Sequence[Hashable]],
    stats: dict[str, int] | None = None,
) -> list[tuple[int, int]]:
    """Return the sorted pairs (s, j) such that patterns[j] occurs in text at the 0-based position s.

    Occurrences may overlap, a pattern listed twice is reported once for each index, and an
    empty pattern occurs at every s in 0..len(text). Characters may be any hashable values,
    and text and patterns must be indexable sequences such as str, list or tuple. If stats is
    a dict, the number of text characters read and the number of windows are stored in it.
    """
    n = len(text)
    res: list[tuple[int, int]] = []
    reads = windows = 0
    empty = [j for j, pat in enumerate(patterns) if len(pat) == 0]
    res.extend((s, j) for s in range(n + 1) for j in empty)  # @line L1
    if len(empty) < len(patterns):  # @line L2
        children, out, lmin, shift = build(patterns)  # @line L3
        pos = lmin - 1  # @line L7
        while pos <= n - 1:  # @line L8
            windows += 1
            v, i = 0, pos  # @line L9
            while i >= 0 and text[i] in children[v]:  # @line L10
                v = children[v][text[i]]  # @line L11
                i -= 1
                reads += 1
                res.extend((i + 1, j) for j in out[v])  # @line L12
            if i >= 0:
                reads += 1  # the character that had no child was read too
            pos += shift.get(text[pos], lmin)  # @line L13
    if stats is not None:
        stats["reads"] = reads
        stats["windows"] = windows
    res.sort()
    return res
