# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-moore-code/. The authors are listed in prov/0R8C9C.jsonl.

"""The Gilbert-Moore code (1959), an order-preserving prefix code.

gilbert_moore_code takes positive integer counts in the order of the
symbols. Symbol i, of count w_i out of a total T, gets the first
l_i = ceil(log2(T / w_i)) + 1 bits of the midpoint (W_i + w_i / 2) / T,
where W_i is the sum of the counts before it. All arithmetic is on
integers, so the bits are exact.

optimal_alphabetic_cost is the O(n^3) dynamic program of the same paper
for the best order-preserving code. It returns the cost and the lengths.
"""

from typing import Sequence


def gilbert_moore_code(counts: Sequence[int]) -> list[str]:
    """Codewords of the Gilbert-Moore code, in the order of the symbols."""
    if not counts or any(w <= 0 for w in counts):
        raise ValueError("counts must be positive")
    total = sum(counts)
    words = []
    before = 0  # @line L1  W, the sum of the counts before the symbol
    for w in counts:  # @line L2
        num, den = 2 * before + w, 2 * total  # @line L3  the midpoint as num / den
        m = 0
        while (w << m) < total:  # @line L4  m = ceil(log2(T / w)), then one more bit
            m += 1
        length = m + 1
        bits = (num << length) // den  # @line L5  the first l bits of the midpoint
        words.append(format(bits, "0{}b".format(length)))
        before += w  # @line L6
    return words


def optimal_alphabetic_cost(weights: Sequence[int]) -> tuple[int, list[int]]:
    """Least cost sum(w_i * l_i) of an alphabetic prefix code, and its lengths.

    c[i][j] is the least cost of a binary tree with leaves i..j in order,
    each leaf counted at its depth below the root of that tree:
    c[i][i] = 0 and c[i][j] = W(i, j) + min over i <= k < j of
    c[i][k] + c[k + 1][j]. This is O(n^3).
    """
    n = len(weights)
    if n == 0:
        raise ValueError("need at least one symbol")
    if n == 1:
        return 0, [0]
    pre = [0]
    for w in weights:
        pre.append(pre[-1] + w)
    c = [[0] * n for _ in range(n)]
    cut = [[0] * n for _ in range(n)]
    for size in range(2, n + 1):
        for i in range(n - size + 1):
            j = i + size - 1
            best, arg = None, i
            for k in range(i, j):
                v = c[i][k] + c[k + 1][j]
                if best is None or v < best:
                    best, arg = v, k
            c[i][j] = best + pre[j + 1] - pre[i]
            cut[i][j] = arg
    lengths = [0] * n
    stack = [(0, n - 1, 0)]
    while stack:
        i, j, d = stack.pop()
        if i == j:
            lengths[i] = d
            continue
        k = cut[i][j]
        stack.append((i, k, d + 1))
        stack.append((k + 1, j, d + 1))
    return c[0][n - 1], lengths


def alphabetic_words(lengths: Sequence[int]) -> list[str]:
    """Codewords in order for lengths that come from an alphabetic tree:
    each word is the previous one plus 1, shifted to the new length."""
    words = []
    code, prev = 0, None
    for l in lengths:
        if prev is None:
            code = 0
        else:
            if l >= prev:
                code = (code + 1) << (l - prev)
            else:  # in a full tree the dropped bits of code + 1 are zeros
                code = (code + 1) >> (prev - l)
        words.append(format(code, "0{}b".format(l)) if l else "")
        prev = l
    return words


def is_prefix_free(words: Sequence[str]) -> bool:
    s = sorted(words)
    return all(not b.startswith(a) for a, b in zip(s, s[1:]))
