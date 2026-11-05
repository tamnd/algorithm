# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-manber/. The authors are listed in prov/2AQSRW.jsonl.

from collections.abc import Hashable, Sequence


def build_tables(patterns: Sequence[Sequence[Hashable]], block: int):
    """Return (lmin, b, shift, hash_table, prefix) for the nonempty patterns.

    lmin is the shortest nonempty length and b = min(block, lmin) the block size. shift maps
    a block (a tuple of b characters) to its shift; blocks that are absent have the default
    shift lmin - b + 1. hash_table maps the last block of the first lmin characters of a
    pattern to the list of its indices, and prefix[j] is the tuple of the first b characters.
    """
    lmin = min(len(p) for p in patterns if len(p) > 0)
    b = min(block, lmin)  # @line L3
    shift: dict[tuple, int] = {}  # @line L4
    for pat in patterns:  # @line L5
        if len(pat) == 0:
            continue
        for q in range(b, lmin + 1):
            x = tuple(pat[q - b : q])
            if lmin - q < shift.get(x, lmin - b + 1):
                shift[x] = lmin - q
    hash_table: dict[tuple, list[int]] = {}
    prefix: dict[int, tuple] = {}
    for j, pat in enumerate(patterns):  # @line L6
        if len(pat) == 0:
            continue
        hash_table.setdefault(tuple(pat[lmin - b : lmin]), []).append(j)
        prefix[j] = tuple(pat[:b])
    return lmin, b, shift, hash_table, prefix


def wu_manber(
    text: Sequence[Hashable],
    patterns: Sequence[Sequence[Hashable]],
    block: int = 2,
    stats: dict[str, int] | None = None,
) -> list[tuple[int, int]]:
    """Return the sorted pairs (s, j) such that patterns[j] occurs in text at the 0-based position s.

    Occurrences may overlap, a pattern listed twice is reported once for each index, and an
    empty pattern occurs at every s in 0..len(text). block is the block size B (at least 1;
    it is lowered to the shortest pattern length). If stats is a dict, the number of
    windows, of windows with shift 0 and of full comparisons are stored in it.
    """
    if block < 1:
        raise ValueError("the block size must be at least 1")
    n = len(text)
    res: list[tuple[int, int]] = []
    windows = zero = compares = 0
    empty = [j for j, pat in enumerate(patterns) if len(pat) == 0]
    res.extend((s, j) for s in range(n + 1) for j in empty)  # @line L1
    if len(empty) < len(patterns):  # @line L2
        lmin, b, shift, hash_table, prefix = build_tables(patterns, block)
        default = lmin - b + 1
        pos = lmin - 1  # @line L7
        while pos <= n - 1:  # @line L8
            windows += 1
            x = tuple(text[pos - b + 1 : pos + 1])  # @line L9
            d = shift.get(x, default)
            if d > 0:  # @line L10
                pos += d
            else:  # @line L11
                zero += 1
                s = pos - lmin + 1  # @line L12
                for j in hash_table.get(x, ()):  # @line L13
                    pat = patterns[j]
                    if tuple(text[s : s + b]) == prefix[j] and s + len(pat) <= n:  # @line L14
                        compares += 1
                        if all(text[s + i] == pat[i] for i in range(len(pat))):
                            res.append((s, j))
                pos += 1  # @line L15
    if stats is not None:
        stats["windows"] = windows
        stats["zero"] = zero
        stats["compares"] = compares
    res.sort()
    return res
