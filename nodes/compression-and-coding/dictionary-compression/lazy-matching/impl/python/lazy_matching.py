# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-matching/. The authors are listed in prov/XTSE0P.jsonl.

"""Lazy matching as in zlib's deflate_slow (compression levels 4 to 9).

The parser makes the same token sequence as zlib 1.2.12 for an input of less
than 32506 bytes: the same 3-byte hash, the same hash chains with position 0
as the end marker, the same chain limit, good_length, nice_length and
max_lazy rules, and the same TOO_FAR rule for far matches of length 3. The
output is a list of tokens: ("L", byte) for a literal and ("M", length,
distance) for a match. No Huffman coding is done here.

Cost: O(n * max_chain * MAX_MATCH) time in the worst case, O(n) extra space.
"""

MIN_MATCH = 3
MAX_MATCH = 258
WSIZE = 32768
MIN_LOOKAHEAD = MAX_MATCH + MIN_MATCH + 1
MAX_DIST = WSIZE - MIN_LOOKAHEAD  # 32506
TOO_FAR = 4096
HASH_BITS = 15  # memLevel 8 gives hash_bits = 8 + 7
HASH_MASK = (1 << HASH_BITS) - 1
NIL = 0  # zlib uses position 0 as the end of a chain

# zlib configuration_table for the levels that use deflate_slow:
# level: (good_length, max_lazy, nice_length, max_chain)
ZLIB_LEVELS = {
    4: (4, 4, 16, 16),
    5: (8, 16, 32, 32),
    6: (8, 16, 128, 128),
    7: (8, 32, 128, 256),
    8: (32, 128, 258, 1024),
    9: (32, 258, 258, 4096),
}

Token = tuple


def _hash3(data: bytes, i: int) -> int:
    """zlib's rolling hash of data[i .. i+2] with hash_shift 5, in closed form."""
    return ((data[i] << 10) ^ (data[i + 1] << 5) ^ data[i + 2]) & HASH_MASK


def lazy_parse(
    data: bytes,
    good_length: int = 8,
    max_lazy: int = 16,
    nice_length: int = 128,
    max_chain: int = 128,
    too_far: int = TOO_FAR,
) -> list[Token]:
    """Parse data into literals and matches with zlib's lazy evaluation.

    The defaults are those of zlib level 6. Set too_far to 0 to switch off
    the rule that drops a match of length 3 at a distance above too_far.
    """
    n = len(data)
    head = [NIL] * (1 << HASH_BITS)
    prev = [NIL] * max(n, 1)
    out: list[Token] = []

    def insert(i: int) -> int:
        h = _hash3(data, i)
        old = head[h]
        prev[i] = old
        head[h] = i
        return old

    def longest_match(i: int, cur: int, prev_length: int) -> tuple[int, int]:
        chain = max_chain
        if prev_length >= good_length:
            chain >>= 2
        nice = min(nice_length, n - i)
        limit = i - MAX_DIST if i > MAX_DIST else NIL
        best, start = prev_length, -1
        cap = min(MAX_MATCH, n - i)
        while True:
            k = 0
            while k < cap and data[cur + k] == data[i + k]:
                k += 1
            if k > best:
                best, start = k, cur
                if k >= nice:
                    break
            cur = prev[cur]
            if cur <= limit:
                break
            chain -= 1
            if chain == 0:
                break
        return best, start

    strstart = 0  # @line L1
    match_length = MIN_MATCH - 1
    match_start = 0
    match_available = False
    while strstart < n:
        lookahead = n - strstart
        hash_head = NIL
        if lookahead >= MIN_MATCH:
            hash_head = insert(strstart)  # @line L2
        prev_length, prev_match = match_length, match_start  # @line L3
        match_length = MIN_MATCH - 1
        if hash_head != NIL and prev_length < max_lazy and strstart - hash_head <= MAX_DIST:  # @line L4
            match_length, s = longest_match(strstart, hash_head, prev_length)  # @line L5
            if s >= 0:
                match_start = s
            if too_far and match_length == MIN_MATCH and strstart - match_start > too_far:
                match_length = MIN_MATCH - 1  # @line L6
        if prev_length >= MIN_MATCH and match_length <= prev_length:  # @line L7
            max_insert = strstart + lookahead - MIN_MATCH
            out.append(("M", prev_length, strstart - 1 - prev_match))  # @line L8
            for _ in range(prev_length - 2):
                strstart += 1
                if strstart <= max_insert:
                    insert(strstart)
            match_available = False
            match_length = MIN_MATCH - 1
            strstart += 1  # @line L9
        elif match_available:  # @line L10
            out.append(("L", data[strstart - 1]))  # @line L11
            strstart += 1
        else:  # @line L12
            match_available = True  # @line L13
            strstart += 1
    if match_available:
        out.append(("L", data[strstart - 1]))  # @line L14
    return out


def lazy_parse_level(data: bytes, level: int = 6) -> list[Token]:
    """lazy_parse with the zlib parameters of a level from 4 to 9."""
    good, lazy, nice, chain = ZLIB_LEVELS[level]
    return lazy_parse(data, good, lazy, nice, chain)


def greedy_parse(data: bytes, max_chain: int = 128, nice_length: int = 128) -> list[Token]:
    """Greedy parse with the same hash chains: take the match at once.

    Every position is inserted, so this is the plain greedy rule, not zlib's
    deflate_fast, which skips the insertion of positions inside long matches.
    """
    n = len(data)
    head = [NIL] * (1 << HASH_BITS)
    prev = [NIL] * max(n, 1)
    out: list[Token] = []
    i = 0
    while i < n:
        best, start = MIN_MATCH - 1, -1
        if n - i >= MIN_MATCH:
            h = _hash3(data, i)
            cur = head[h]
            prev[i] = cur
            head[h] = i
            chain = max_chain
            cap = min(MAX_MATCH, n - i)
            nice = min(nice_length, cap)
            while cur != NIL and i - cur <= MAX_DIST and chain > 0:
                k = 0
                while k < cap and data[cur + k] == data[i + k]:
                    k += 1
                if k > best:
                    best, start = k, cur
                    if k >= nice:
                        break
                cur = prev[cur]
                chain -= 1
        if start >= 0:
            out.append(("M", best, i - start))
            for j in range(i + 1, i + best):
                if n - j >= MIN_MATCH:
                    h = _hash3(data, j)
                    prev[j] = head[h]
                    head[h] = j
            i += best
        else:
            out.append(("L", data[i]))
            i += 1
    return out


def decode(tokens: list[Token]) -> bytes:
    """Rebuild the input from the tokens. A match may overlap its own output."""
    out = bytearray()
    for t in tokens:
        if t[0] == "L":
            out.append(t[1])
        else:
            _, length, dist = t
            if not 1 <= dist <= len(out):
                raise ValueError("distance out of range")
            for _ in range(length):
                out.append(out[-dist])
    return bytes(out)
