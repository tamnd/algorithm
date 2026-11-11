# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lazy-matching/. The authors are listed in prov/XTSE0P.jsonl.

import random
import zlib

from lazy_matching import (
    MAX_MATCH,
    ZLIB_LEVELS,
    decode,
    greedy_parse,
    lazy_parse,
    lazy_parse_level,
)

# ---------------------------------------------------------------- a DEFLATE reader
# It reads the raw DEFLATE stream that zlib makes (RFC 1951) and returns the
# tokens in it, so that the parse of zlib itself is the oracle.

LEN_BASE = [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17, 19, 23, 27, 31, 35, 43, 51, 59,
            67, 83, 99, 115, 131, 163, 195, 227, 258]
LEN_EXTRA = [0] * 8 + [1] * 4 + [2] * 4 + [3] * 4 + [4] * 4 + [5] * 4 + [0]
DIST_BASE = [1, 2, 3, 4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97, 129, 193, 257, 385, 513,
             769, 1025, 1537, 2049, 3073, 4097, 6145, 8193, 12289, 16385, 24577]
DIST_EXTRA = [0, 0, 0, 0] + [k for k in range(1, 14) for _ in (0, 1)]
CL_ORDER = [16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15]


class _Bits:
    def __init__(self, buf: bytes) -> None:
        self.buf, self.pos = buf, 0

    def get(self, k: int) -> int:
        v = 0
        for j in range(k):
            byte = self.buf[self.pos >> 3]
            v |= ((byte >> (self.pos & 7)) & 1) << j
            self.pos += 1
        return v


def _table(lengths: list[int]) -> dict[tuple[int, int], int]:
    count = [0] * 16
    for x in lengths:
        if x:
            count[x] += 1
    code, nxt = 0, [0] * 16  # canonical codes, RFC 1951 Section 3.2.2
    for b in range(1, 16):
        code = (code + count[b - 1]) << 1
        nxt[b] = code
    t = {}
    for sym, x in enumerate(lengths):
        if x:
            t[(x, nxt[x])] = sym
            nxt[x] += 1
    return t


def _sym(bits: _Bits, t: dict[tuple[int, int], int]) -> int:
    code = 0
    for x in range(1, 16):
        code = (code << 1) | bits.get(1)
        if (x, code) in t:
            return t[(x, code)]
    raise ValueError("bad code")


def inflate_tokens(raw: bytes):
    """Return (tokens, data), or (None, data) if a stored block occurs."""
    bits, out, toks, stored = _Bits(raw), bytearray(), [], False
    while True:
        final, btype = bits.get(1), bits.get(2)
        if btype == 0:
            bits.pos = (bits.pos + 7) & ~7
            ln = bits.get(16)
            bits.get(16)
            for _ in range(ln):
                out.append(bits.get(8))
            stored = True
        else:
            if btype == 1:
                lit = _table([8] * 144 + [9] * 112 + [7] * 24 + [8] * 8)
                dist = _table([5] * 30)
            else:
                hlit, hdist, hclen = bits.get(5) + 257, bits.get(5) + 1, bits.get(4) + 4
                cl = [0] * 19
                for k in range(hclen):
                    cl[CL_ORDER[k]] = bits.get(3)
                clt = _table(cl)
                lens: list[int] = []
                while len(lens) < hlit + hdist:
                    s = _sym(bits, clt)
                    if s < 16:
                        lens.append(s)
                    elif s == 16:
                        lens += [lens[-1]] * (3 + bits.get(2))
                    elif s == 17:
                        lens += [0] * (3 + bits.get(3))
                    else:
                        lens += [0] * (11 + bits.get(7))
                lit, dist = _table(lens[:hlit]), _table(lens[hlit:])
            while True:
                s = _sym(bits, lit)
                if s < 256:
                    out.append(s)
                    toks.append(("L", s))
                elif s == 256:
                    break
                else:
                    k = s - 257
                    length = LEN_BASE[k] + bits.get(LEN_EXTRA[k])
                    d = _sym(bits, dist)
                    distance = DIST_BASE[d] + bits.get(DIST_EXTRA[d])
                    for _ in range(length):
                        out.append(out[-distance])
                    toks.append(("M", length, distance))
        if final:
            break
    return (None if stored else toks), bytes(out)


def zlib_tokens(data: bytes, level: int):
    c = zlib.compressobj(level, zlib.DEFLATED, -15, 8, zlib.Z_DEFAULT_STRATEGY)
    raw = c.compress(data) + c.flush()
    toks, back = inflate_tokens(raw)
    assert back == data
    return toks


# ---------------------------------------------------------------- a reference lazy rule


def _longest(data: bytes, i: int) -> tuple[int, int]:
    """Brute force: longest match of length 3 to 258 at i, source at 1 or more, closest on ties."""
    n, best, dist = len(data), 0, 0
    for j in range(i - 1, 0, -1):
        k = 0
        while k < min(MAX_MATCH, n - i) and data[j + k] == data[i + k]:
            k += 1
        if k > best:
            best, dist = k, i - j
    return (best, dist) if best >= 3 else (0, 0)


def reference_lazy(data: bytes) -> list:
    """The textbook one-step lazy rule with an exhaustive match search."""
    n, i, out = len(data), 0, []
    cur = _longest(data, 0) if n else (0, 0)
    while i < n:
        if cur[0] >= 3:
            nxt = _longest(data, i + 1) if i + 1 < n else (0, 0)
            if nxt[0] > cur[0]:
                out.append(("L", data[i]))
                i, cur = i + 1, nxt
                continue
            out.append(("M", cur[0], cur[1]))
            i += cur[0]
        else:
            out.append(("L", data[i]))
            i += 1
        cur = _longest(data, i) if i < n else (0, 0)
    return out


def _inputs(rng: random.Random, count: int, maxlen: int):
    for _ in range(count):
        kind = rng.randrange(4)
        n = rng.randrange(maxlen)
        if kind == 0:
            yield bytes(rng.choice(b"ab") for _ in range(n))
        elif kind == 1:
            yield bytes(rng.choice(b"abcd") for _ in range(n))
        elif kind == 2:
            words = [b"the ", b"then ", b"there ", b"other ", b"them "]
            yield b"".join(rng.choice(words) for _ in range(n // 4))
        else:
            unit = bytes(rng.choice(b"xyz") for _ in range(rng.randrange(1, 9)))
            yield (unit * (n // len(unit) + 1))[:n]


def _lits(s: bytes) -> list:
    return [("L", c) for c in s]


def test_page_example_lazy_wins() -> None:
    data = b"yabcxbcdeabcde"
    g = greedy_parse(data, max_chain=10**9, nice_length=258)
    lz = lazy_parse(data, good_length=259, max_lazy=258, nice_length=258, max_chain=10**9)
    assert g == _lits(b"yabcxbcde") + [("M", 3, 8)] + _lits(b"de")
    assert lz == _lits(b"yabcxbcde") + [("L", ord("a")), ("M", 4, 5)]
    for level in ZLIB_LEVELS:
        assert zlib_tokens(data, level) == lz


def test_page_example_lazy_loses() -> None:
    data = b"baaadaaaaad"
    g = greedy_parse(data, max_chain=10**9, nice_length=258)
    lz = lazy_parse_level(data, 6)
    assert g == _lits(b"baaad") + [("M", 3, 4), ("M", 3, 6)]
    assert lz == _lits(b"baaada") + [("M", 4, 1), ("L", ord("d"))]
    assert zlib_tokens(data, 6) == lz


def test_edges() -> None:
    for data in (b"", b"a", b"ab", b"abc", b"aaaa", b"a" * 1000, b"ab" * 300):
        for level in ZLIB_LEVELS:
            toks = lazy_parse_level(data, level)
            assert decode(toks) == data


def test_long_run() -> None:
    data = b"a" * 1000
    toks = lazy_parse_level(data, 6)
    # zlib never matches position 0, so the run starts with two literals
    assert toks[:2] == [("L", 97), ("L", 97)]
    assert toks[2] == ("M", 258, 1)
    assert toks == zlib_tokens(data, 6)


def test_same_tokens_as_zlib() -> None:
    rng = random.Random(1951)
    checked = 0
    for data in _inputs(rng, 160, 1500):
        for level in (4, 6, 9):
            want = zlib_tokens(data, level)
            if want is None:  # zlib chose a stored block
                continue
            assert lazy_parse_level(data, level) == want
            checked += 1
    assert checked > 300


def test_unlimited_search_is_the_lazy_rule() -> None:
    rng = random.Random(77)
    for data in _inputs(rng, 400, 60):
        got = lazy_parse(data, good_length=259, max_lazy=258, nice_length=258,
                         max_chain=10**9, too_far=0)
        assert got == reference_lazy(data)


def test_round_trip_random_bytes() -> None:
    rng = random.Random(5)
    for _ in range(50):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(400)))
        assert decode(lazy_parse_level(data, 6)) == data
        assert decode(greedy_parse(data)) == data
