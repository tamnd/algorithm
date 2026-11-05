# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/palindrome-partition-backtracking/. The authors are listed in prov/8C52F0.jsonl.

"""All partitions of a string into palindromes, by backtracking with an explicit stack.

Indices are 0-based and s[i..j] includes both ends. Pieces may be odd or even
palindromes. Symbols are only tested for equality.
"""

from collections.abc import Iterator


def palindrome_ends(s: str) -> list[list[int]]:
    """Return ends with ends[i] the sorted list of j such that s[i..j] is a palindrome."""
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    ends: list[list[int]] = [[] for _ in range(n)]
    for i in range(n - 1, -1, -1):  # @line L1
        for j in range(i, n):  # @line L2
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])  # @line L3
            if pal[i][j]:  # @line L4
                ends[i].append(j)
    return ends


def palindrome_partitions(s: str) -> Iterator[list[str]]:
    """Yield every partition of s into nonempty palindromes, each one time.

    The partitions come in lexicographic order of their piece lengths, so the
    first one is the split into single symbols. The empty string has one
    partition, the empty list.
    """
    n = len(s)
    ends = palindrome_ends(s)
    path: list[str] = []
    stack: list[list[int]] = [[0, 0]]  # @line L5
    while stack:  # @line L6
        frame = stack[-1]  # @line L7
        i, k = frame
        if i == n:  # @line L8
            yield list(path)
            stack.pop()
            if i > 0:
                path.pop()
            continue
        if k == len(ends[i]):  # @line L9
            stack.pop()
            if i > 0:
                path.pop()
            continue
        frame[1] = k + 1  # @line L10
        j = ends[i][k]
        path.append(s[i : j + 1])  # @line L11
        stack.append([j + 1, 0])


def count_palindrome_partitions(s: str) -> int:
    """Return the number of palindromic partitions of s, by the prefix recurrence."""
    n = len(s)
    ends = palindrome_ends(s)
    ways = [0] * (n + 1)
    ways[n] = 1
    for i in range(n - 1, -1, -1):
        ways[i] = sum(ways[j + 1] for j in ends[i])
    return ways[0]
