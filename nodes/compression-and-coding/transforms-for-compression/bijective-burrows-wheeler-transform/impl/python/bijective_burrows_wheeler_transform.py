# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bijective-burrows-wheeler-transform/. The authors are listed in prov/R9BPTQ.jsonl.

"""The bijective Burrows-Wheeler transform (BBWT) of Gil and Scott, in the
form that Kufleitner (PSC 2009) proves correct.

Forward: cut T into its Lyndon factors w_1 >= w_2 >= ... >= w_m with Duval's
algorithm, take every rotation of every factor (a multiset of n words), sort
them in the omega order (u before v when the infinite word uuu... is smaller
than vvv...), and output the last symbol of each. No sentinel and no index.

Inverse: the LF mapping of the output is a permutation whose cycles are the
factors. The smallest row of each cycle is the factor itself. Read each cycle,
then concatenate the factors in nonincreasing order.

This version sorts with a naive key: the first 2n symbols of r^omega. By the
theorem of Fine and Wilf, two words u, v with |u| + |v| <= 2n have the same
infinite power iff these prefixes agree, so the key gives the exact omega
order. Time O(n^2 log n) for the forward step and O(n log n) for the inverse;
linear-time algorithms exist (Bannai, Kärkkäinen, Köppl and Piątkowski, 2021).
"""

from collections.abc import Sequence


def lyndon_factorization(s: str) -> list[str]:
    """Duval's algorithm: the Lyndon factors of s, in order. Time O(n), O(1) extra."""
    n, i, out = len(s), 0, []
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            k = i if s[k] < s[j] else k + 1
            j += 1
        while i <= k:
            out.append(s[i : i + j - k])
            i += j - k
    return out


def omega_key(r: str, n: int) -> str:
    """The first 2n symbols of r r r ...; it orders words of length <= n by omega order."""
    reps = -(-2 * n // len(r))
    return (r * reps)[: 2 * n]


def bbwt(text: str) -> str:
    """The bijective BWT of text. The output is a permutation of text."""
    n = len(text)
    factors = lyndon_factorization(text)  # @line L1
    rotations: list[str] = []  # @line L2
    for w in factors:  # @line L3
        for i in range(len(w)):  # @line L4
            rotations.append(w[i:] + w[:i])
    rotations.sort(key=lambda r: omega_key(r, n))  # @line L5
    out = [r[-1] for r in rotations]  # @line L6
    return "".join(out)  # @line L7


def lf_mapping(last: Sequence[str]) -> list[int]:
    """LF[i] = (number of symbols of last smaller than last[i])
    + (number of occurrences of last[i] in last[0 .. i-1])."""
    count: dict[str, int] = {}
    for c in last:
        count[c] = count.get(c, 0) + 1
    smaller, total = {}, 0
    for c in sorted(count):
        smaller[c] = total
        total += count[c]
    seen = dict.fromkeys(count, 0)
    lf = []
    for c in last:
        lf.append(smaller[c] + seen[c])
        seen[c] += 1
    return lf


def inverse_bbwt(last: str) -> str:
    """Recover the text from its bijective BWT. Every string is a valid input."""
    n = len(last)
    lf = lf_mapping(last)
    visited = [False] * n
    words: list[str] = []
    for r in range(n):
        if visited[r]:
            continue
        chars: list[str] = []
        i = r
        while not visited[i]:
            visited[i] = True
            chars.append(last[i])
            i = lf[i]
        words.append("".join(reversed(chars)))
    words.sort(reverse=True)
    return "".join(words)
