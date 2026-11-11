# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lz77/. The authors are listed in prov/380S00.jsonl.

"""LZ77 (Ziv and Lempel, 1977): a sliding-window coder that emits triples.

Each triple is (d, length, c): copy `length` symbols that start `d` positions
back, then append the literal symbol c. When length is 0, d is 0. The copy may
run past the current position (length > d), so the decoder copies one symbol
at a time.
"""

Triple = tuple[int, int, int]


def lz77_encode(data: bytes, window: int = 4096, max_len: int = 255) -> list[Triple]:
    """Greedy LZ77 parse of data into triples (d, length, next byte).

    The match search is exhaustive over the window: it tries each start j in
    [i - window, i - 1] with data[j] == data[i], nearest first, and keeps the
    longest match (the nearest one on a tie). The length is capped so that a
    next byte always exists, which means length <= n - i - 1.
    """
    if window < 1 or max_len < 0:
        raise ValueError("window must be at least 1 and max_len at least 0")
    n = len(data)
    out: list[Triple] = []
    where: list[list[int]] = [[] for _ in range(256)]  # positions of each byte value
    i = 0  # @line L1
    while i < n:  # @line L2
        best_d, best_len = 0, 0  # @line L3
        cap = min(max_len, n - i - 1)
        cands = where[data[i]]
        lo = i - window
        for idx in range(len(cands) - 1, -1, -1):  # @line L4
            j = cands[idx]
            if j < lo or best_len == cap:
                break
            k = 0  # @line L5
            while k < cap and data[j + k] == data[i + k]:  # @line L6
                k += 1
            if k > best_len:  # @line L7
                best_d, best_len = i - j, k
        out.append((best_d, best_len, data[i + best_len]))  # @line L8
        for p in range(i, i + best_len + 1):
            where[data[p]].append(p)
        i += best_len + 1  # @line L9
    return out  # @line L10


def lz77_decode(triples: list[Triple]) -> bytes:
    """Invert lz77_encode. Copies byte by byte, so an overlapping copy works."""
    s = bytearray()  # @line L11
    for d, length, c in triples:  # @line L12
        if length > 0 and not 1 <= d <= len(s):
            raise ValueError("offset points before the start of the output")
        start = len(s) - d  # @line L13
        for k in range(length):  # @line L14
            s.append(s[start + k])
        s.append(c)  # @line L15
    return bytes(s)  # @line L16
