# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karp-miller-rosenberg-algorithm/. The authors are listed in prov/NP7V4M.jsonl.

from collections.abc import Sequence


def _radix_sort_pairs(items: list[int], first: list[int], second: list[int], buckets: int) -> list[int]:
    """Stable LSD radix sort of items by (first[i], second[i]), keys in 0 .. buckets - 1."""
    for key in (second, first):
        count = [0] * (buckets + 1)
        for i in items:
            count[key[i] + 1] += 1
        for b in range(buckets):
            count[b + 1] += count[b]
        out = [0] * len(items)
        for i in items:
            out[count[key[i]]] = i
            count[key[i]] += 1
        items = out
    return items


def kmr(text: Sequence) -> list[list[int]]:
    """Return the dictionary of basic factors: names[j][i] for 0 <= i <= n - 2^j.

    names[j][i] is the rank of the factor text[i : i + 2^j] among the distinct
    factors of length 2^j, so equal factors get equal names and the order of
    names is the lexicographic order of the factors. Symbols need a total order.
    Positions are 0-based; no sentinel is used. Time and space O(n log n).
    """
    n = len(text)
    if n == 0:
        return []
    code = {c: r for r, c in enumerate(sorted(set(text)))}
    names = [[code[c] for c in text]]  # @line L1
    j = 0  # @line L2
    while 2 ** (j + 1) <= n:  # @line L3
        half, cur = 2**j, names[j]
        m = n - 2 * half + 1
        second = [cur[i + half] for i in range(m)]  # @line L4
        order = _radix_sort_pairs(list(range(m)), cur, second, n)  # @line L5
        new = [0] * m
        r = -1
        prev = None
        for i in order:  # @line L6
            if (cur[i], second[i]) != prev:  # @line L7
                r += 1
                prev = (cur[i], second[i])
            new[i] = r  # @line L8
        names.append(new)
        j += 1  # @line L9
    return names  # @line L10


def substring_compare(names: list[list[int]], p: int, q: int, length: int) -> int:
    """Compare text[p : p + length] with text[q : q + length] in O(1): -1, 0 or 1."""
    if length == 0:
        return 0
    j = length.bit_length() - 1
    a = (names[j][p], names[j][p + length - 2**j])
    b = (names[j][q], names[j][q + length - 2**j])
    return (a > b) - (a < b)


def suffix_array(text: Sequence) -> list[int]:
    """Suffix array by naming the prefixes of length 2^j of the suffixes; a missing half sorts first."""
    n = len(text)
    if n == 0:
        return []
    code = {c: r + 1 for r, c in enumerate(sorted(set(text)))}
    rank = [code[c] for c in text]
    k = 1
    while True:
        second = [rank[i + k] if i + k < n else 0 for i in range(n)]
        order = _radix_sort_pairs(list(range(n)), rank, second, n + 2)
        new = [0] * n
        r = 0
        for t, i in enumerate(order):
            if t == 0 or (rank[i], second[i]) != (rank[order[t - 1]], second[order[t - 1]]):
                r += 1
            new[i] = r
        rank = new
        if r == n or k >= n:
            return order
        k *= 2


def longest_repeat(text: Sequence) -> tuple[int, int, int]:
    """Return (length, p, q) of a longest factor that occurs at two positions p < q; (0, -1, -1) if none.

    Binary lifting over the basic factors: the length is built from the highest
    power of two down, and a name for each tested length is a pair of names.
    """
    names = kmr(text)
    n = len(text)
    length, cur = 0, [0] * (n + 1)  # the empty factor has one name
    for j in range(len(names) - 1, -1, -1):
        step = 2**j
        m = n - (length + step) + 1
        if m < 2:
            continue
        pairs = [(cur[i], names[j][i + length]) for i in range(m)]
        seen: dict[tuple[int, int], int] = {}
        for i, key in enumerate(pairs):
            if key in seen:
                break
            seen[key] = i
        else:
            continue
        ids = {key: r for r, key in enumerate(sorted(set(pairs)))}
        cur = [ids[key] for key in pairs]
        length += step
    if length == 0:
        return 0, -1, -1
    first: dict[int, int] = {}
    for i in range(n - length + 1):
        if cur[i] in first:
            return length, first[cur[i]], i
        first[cur[i]] = i
    raise AssertionError("unreachable")
