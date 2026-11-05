# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dc3-skew-algorithm/. The authors are listed in prov/M5ZHTB.jsonl.

from collections.abc import Sequence


def _radix_pass(items: list[int], key: list[int], offset: int, k: int) -> list[int]:
    """Stable counting sort of items by key[x + offset], with keys in 0 .. k."""
    count = [0] * (k + 2)
    for x in items:
        count[key[x + offset] + 1] += 1
    for b in range(k + 1):
        count[b + 1] += count[b]
    out = [0] * len(items)
    for x in items:
        out[count[key[x + offset]]] = x
        count[key[x + offset]] += 1
    return out


def _dc3(t: list[int], n: int, k: int) -> list[int]:
    """Suffix array of t[0 .. n-1] with symbols in 1 .. k and t[n] = t[n+1] = t[n+2] = 0.

    The recursion is on a string of length about 2n/3, so its depth is O(log n).
    """
    if n <= 1:
        return list(range(n))
    n0, n1, n2 = (n + 2) // 3, (n + 1) // 3, n // 3
    n02 = n0 + n2
    sample = [i for i in range(n + (n0 - n1)) if i % 3 != 0]  # @line L1
    for offset in (2, 1, 0):  # @line L2
        sample = _radix_pass(sample, t, offset, k)
    name, last = 0, None
    rank = [0] * (n02 + 3)  # rank[i // 3] for i = 1 mod 3, rank[i // 3 + n0] for i = 2 mod 3
    for p in sample:  # @line L3
        triple = (t[p], t[p + 1], t[p + 2])
        if triple != last:
            name, last = name + 1, triple
        rank[p // 3 if p % 3 == 1 else p // 3 + n0] = name
    if name < n02:  # @line L4
        reduced = rank[:n02] + [0, 0, 0]  # @line L5
        sa12 = _dc3(reduced, n02, name)  # @line L6
        for r, x in enumerate(sa12):
            rank[x] = r + 1
    else:
        sa12 = [0] * n02  # @line L7
        for x in range(n02):
            sa12[rank[x] - 1] = x
    sa0 = _radix_pass([3 * x for x in sa12 if x < n0], t, 0, k)  # @line L8

    def pos12(x: int) -> int:
        return 3 * x + 1 if x < n0 else 3 * (x - n0) + 2

    out: list[int] = []
    a, b = n0 - n1, 0  # skip the dummy sample suffix when n = 1 mod 3
    while a < n02 and b < n0:  # @line L9
        x, j = sa12[a], sa0[b]
        i = pos12(x)
        if x < n0:
            left = (t[i], rank[x + n0])
            right = (t[j], rank[j // 3])
        else:
            left = (t[i], t[i + 1], rank[x - n0 + 1])
            right = (t[j], t[j + 1], rank[j // 3 + n0])
        if left <= right:
            out.append(i)
            a += 1
        else:
            out.append(j)
            b += 1
    out.extend(pos12(x) for x in sa12[a:])
    out.extend(sa0[b:])
    return out  # @line L10


def dc3(text: Sequence) -> list[int]:
    """Suffix array of text by the DC3 (skew) algorithm of Karkkainen and Sanders.

    Symbols need a total order; they are coded 1 .. sigma and the text is padded
    with three zeros, which act as end markers, so no sentinel is part of the
    output and a proper prefix sorts first. Positions are 0-based.
    """
    n = len(text)
    code = {c: r + 1 for r, c in enumerate(sorted(set(text)))}
    t = [code[c] for c in text] + [0, 0, 0]
    return _dc3(t, n, len(code))
