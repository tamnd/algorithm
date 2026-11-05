# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chang-lawler-algorithm/. The authors are listed in prov/K5VMHF.jsonl.

"""The sublinear expected time (SET) algorithm of Chang and Lawler.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.

The text is cut into blocks of length b = (m - k) // 2. From the start of a
block the algorithm makes k + 1 jumps, each over a maximal substring of the
pattern plus one symbol, with the suffix automaton of the pattern. If the
jumps stay inside the block, no match contains the block. Sellers' dynamic
program runs only on the windows around the other blocks. All loops are
iterative.
"""


class SuffixAutomaton:
    """The suffix automaton of a string: it accepts exactly its substrings."""

    def __init__(self, s: str) -> None:
        self.next: list[dict[str, int]] = [{}]
        link = [-1]
        length = [0]
        last = 0
        for c in s:
            cur = len(self.next)
            self.next.append({})
            length.append(length[last] + 1)
            link.append(0)
            p = last
            while p != -1 and c not in self.next[p]:
                self.next[p][c] = cur
                p = link[p]
            if p != -1:
                q = self.next[p][c]
                if length[p] + 1 == length[q]:
                    link[cur] = q
                else:
                    clone = len(self.next)
                    self.next.append(dict(self.next[q]))
                    length.append(length[p] + 1)
                    link.append(link[q])
                    while p != -1 and self.next[p].get(c) == q:
                        self.next[p][c] = clone
                        p = link[p]
                    link[q] = clone
                    link[cur] = clone
            last = cur

    def longest_prefix(self, text: str, p: int) -> int:
        """Return ms(p): the length of the longest prefix of text[p:] that is
        a substring of the pattern. Cost: O(ms(p) + 1)."""
        state, j = 0, p
        while j < len(text) and text[j] in self.next[state]:
            state = self.next[state][text[j]]
            j += 1
        return j - p


def sellers(pattern: str, text: str, k: int) -> list[int]:
    """End positions j in 0..len(text) of substrings within distance k."""
    m = len(pattern)
    col = list(range(m + 1))
    ends = [0] if col[m] <= k else []
    for j in range(1, len(text) + 1):
        t = text[j - 1]
        prev, col[0] = col[0], 0
        for i in range(1, m + 1):
            new = min(col[i] + 1, col[i - 1] + 1, prev + (pattern[i - 1] != t))
            prev, col[i] = col[i], new
        if col[m] <= k:
            ends.append(j)
    return ends


def live_blocks(pattern: str, text: str, k: int) -> list[int]:
    """Return the numbers t of the blocks that the jumps do not rule out."""
    m, n = len(pattern), len(text)
    b = (m - k) // 2
    sa = SuffixAutomaton(pattern)
    live = []
    for t in range(n // b):
        end = (t + 1) * b
        p = t * b  # p_0 = tb, then p_(r+1) = p_r + ms(p_r) + 1
        for _ in range(k + 1):  # @line L4
            if p >= end:  # then p_(k+1) > end
                p = end + 1
                break
            p += sa.longest_prefix(text, p) + 1
        if p > end:  # @line L5
            live.append(t)
    return live


def chang_lawler(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: O(m + n) time for the jumps plus Sellers'
    O(m) time per text symbol of the windows around live blocks; O(m)
    expected work per block on random text when k is small against m.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    if m - k < 2:  # @line L1
        return sellers(pattern, text, k)
    b = (m - k) // 2  # @line L2
    windows: list[list[int]] = []
    for t in live_blocks(pattern, text, k):  # @line L3
        lo = max(0, (t + 1) * b - m - k)  # @line L6
        hi = min(n, t * b + m + k)
        if windows and lo <= windows[-1][1]:  # @line L7
            windows[-1][1] = hi
        else:
            windows.append([lo, hi])
    ends: list[int] = []
    for lo, hi in windows:  # @line L8
        ends.extend(lo + j for j in sellers(pattern, text[lo:hi], k))
    return sorted(set(ends))  # @line L9
