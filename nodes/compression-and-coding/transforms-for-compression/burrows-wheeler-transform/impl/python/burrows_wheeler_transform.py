# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burrows-wheeler-transform/. The authors are listed in prov/6F6TAM.jsonl.

"""The Burrows-Wheeler transform, built from a linear-time suffix array.

Convention: the text T[0 .. n-1] gets a sentinel $ at its end. The sentinel is
unique and smaller than every symbol of T. The output L has n + 1 symbols and
L[i] = T'[SA[i] - 1], where T' = T$ and SA is the suffix array of T'. The
symbol before position 0 is the sentinel itself.

The module also gives the convention of the 1994 report (sort the n rotations
of T, output the last column and the row of T) and a naive rotation sort that
the tests use as an oracle.
"""

from collections.abc import Sequence

SENTINEL = -1  # the sentinel in an output list of integer codes


def _sais(s: list[int], k: int) -> list[int]:
    """Suffix array of s by SA-IS (Nong, Zhang and Chan). Time O(n + k).

    Precondition: s[-1] == 0, 0 occurs nowhere else, and 0 <= s[i] < k.
    The recursion depth is O(log n), because each level at least halves n.
    """
    n = len(s)
    if n == 1:
        return [0]
    stype = [False] * n  # True for an S-type position
    stype[n - 1] = True
    for i in range(n - 2, -1, -1):
        stype[i] = s[i] < s[i + 1] or (s[i] == s[i + 1] and stype[i + 1])
    lms = [i for i in range(1, n) if stype[i] and not stype[i - 1]]
    is_lms = [False] * n
    for i in lms:
        is_lms[i] = True
    cnt = [0] * k
    for c in s:
        cnt[c] += 1

    def bucket_heads() -> list[int]:
        h, acc = [0] * k, 0
        for c in range(k):
            h[c] = acc
            acc += cnt[c]
        return h

    def bucket_tails() -> list[int]:
        t, acc = [0] * k, 0
        for c in range(k):
            acc += cnt[c]
            t[c] = acc
        return t

    def induce(seeds: list[int]) -> list[int]:
        sa = [-1] * n
        tail = bucket_tails()
        for i in reversed(seeds):
            c = s[i]
            tail[c] -= 1
            sa[tail[c]] = i
        head = bucket_heads()
        for j in range(n):
            p = sa[j]
            if p > 0 and not stype[p - 1]:
                c = s[p - 1]
                sa[head[c]] = p - 1
                head[c] += 1
        tail = bucket_tails()
        for j in range(n - 1, -1, -1):
            p = sa[j]
            if p > 0 and stype[p - 1]:
                c = s[p - 1]
                tail[c] -= 1
                sa[tail[c]] = p - 1
        return sa

    sa = induce(lms)

    def same_lms_substring(a: int, b: int) -> bool:
        if a == n - 1 or b == n - 1:
            return a == b
        j = 0
        while True:
            if s[a + j] != s[b + j] or stype[a + j] != stype[b + j]:
                return False
            if j > 0 and (is_lms[a + j] or is_lms[b + j]):
                return is_lms[a + j] and is_lms[b + j]
            j += 1

    name = [-1] * n
    current, previous = -1, -1
    for p in sa:
        if is_lms[p]:
            if previous < 0 or not same_lms_substring(previous, p):
                current += 1
            name[p] = current
            previous = p
    reduced = [name[i] for i in lms]
    if current + 1 == len(lms):
        order = [0] * len(lms)
        for j, r in enumerate(reduced):
            order[r] = j
    else:
        order = _sais(reduced, current + 1)
    return induce([lms[j] for j in order])


def suffix_array(t: Sequence[int]) -> list[int]:
    """Suffix array of T$ for a list of integer codes T (each code >= 0).

    The result has len(t) + 1 entries, and entry 0 is len(t), the sentinel.
    Time O(n + max code), by SA-IS.
    """
    if any(c < 0 for c in t):
        raise ValueError("codes must be non-negative")
    k = (max(t) + 2) if t else 1
    return _sais([c + 1 for c in t] + [0], k)


def bwt_codes(t: Sequence[int]) -> list[int]:
    """BWT of T$ for integer codes; the sentinel appears as SENTINEL (-1).

    Precondition: each code is >= 0. Time O(n + max code), space O(n).
    """
    codes = list(t)  # @line L1 (suffix_array appends the sentinel)
    sa = suffix_array(codes)  # @line L2
    out: list[int] = []
    for i in range(len(sa)):  # @line L3
        if sa[i] == 0:  # @line L4
            out.append(SENTINEL)
        else:
            out.append(t[sa[i] - 1])  # @line L5
    return out  # @line L6


def bwt(text: str, sentinel: str = "$") -> str:
    """BWT of text + sentinel, as a string of length len(text) + 1.

    Precondition: the sentinel does not occur in text and is smaller than
    each character of text.
    """
    if sentinel in text or (text and sentinel > min(text)):
        raise ValueError("the sentinel must be unique and smaller than each character")
    out = bwt_codes([ord(ch) for ch in text])
    return "".join(sentinel if c == SENTINEL else chr(c) for c in out)


def bwt_bytes(data: bytes) -> tuple[bytes, int]:
    """BWT of a byte string with an implicit sentinel.

    Returns (L without the sentinel, the row where the sentinel was). This is
    the same information as the n + 1 symbols of the sentinel form.
    """
    out = bwt_codes(list(data))
    k = out.index(SENTINEL)
    return bytes(c for c in out if c != SENTINEL), k


def bwt_rotations(text: str) -> tuple[str, int]:
    """The 1994 convention: sort the n rotations of text (no sentinel).

    Returns (the last column, the index of a row equal to text). Equal
    rotations, which occur when text is periodic, are equal rows, so the
    output does not depend on how they are ordered. Time O(n), by SA-IS
    on text + text: the first n characters of the suffix at i < n form the
    rotation at i.
    """
    n = len(text)
    if n == 0:
        return "", 0
    sa = suffix_array([ord(ch) for ch in text + text])
    rows = [i for i in sa if i < n]
    last = "".join(text[i - 1] for i in rows)
    return last, rows.index(0)


def bwt_naive(text: str, sentinel: str = "$") -> str:
    """Oracle: sort all rotations of text + sentinel. Time O(n^2 log n)."""
    t = text + sentinel
    rotations = sorted(t[i:] + t[:i] for i in range(len(t)))
    return "".join(r[-1] for r in rotations)


def bwt_rotations_naive(text: str) -> tuple[str, int]:
    """Oracle for bwt_rotations: sort the rotations by brute force."""
    n = len(text)
    if n == 0:
        return "", 0
    rows = sorted(range(n), key=lambda i: text[i:] + text[:i])
    last = "".join(text[i - 1] for i in rows)
    index = next(r for r, i in enumerate(rows) if text[i:] + text[:i] == text)
    return last, index
