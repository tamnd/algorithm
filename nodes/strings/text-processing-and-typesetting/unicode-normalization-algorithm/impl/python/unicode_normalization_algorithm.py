# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-normalization-algorithm/. The authors are listed in prov/ZG8A1R.jsonl.

"""The four Unicode normalization forms (UAX 15 revision 56; core spec 16.0.0, section 3.11).

The code uses unicodedata only as data: decomposition() for the decomposition mappings and
combining() for the canonical combining class (ccc). It does not call unicodedata.normalize
or unicodedata.is_normalized. Hangul syllables use the arithmetic of core spec section 3.12.
"""

import unicodedata

# The code point fields of the data lines of sections 1 (script specifics, 67 code points)
# and 2 (post composition version, 14 code points) of CompositionExclusions-16.0.0.txt
# (Date: 2024-02-02), https://www.unicode.org/Public/16.0.0/ucd/CompositionExclusions.txt.
# Sections 3 (1035 singletons) and 4 (4 non-starter decompositions) are listed in the file
# "for reference" only, because they can be derived; full_composition_exclusions() derives them.
SCRIPT_SPECIFIC = """
0958 0959 095A 095B 095C 095D 095E 095F 09DC 09DD 09DF 0A33 0A36 0A59 0A5A 0A5B 0A5E
0B5C 0B5D 0F43 0F4D 0F52 0F57 0F5C 0F69 0F76 0F78 0F93 0F9D 0FA2 0FA7 0FAC 0FB9 FB1D
FB1F FB2A FB2B FB2C FB2D FB2E FB2F FB30 FB31 FB32 FB33 FB34 FB35 FB36 FB38 FB39 FB3A
FB3B FB3C FB3E FB40 FB41 FB43 FB44 FB46 FB47 FB48 FB49 FB4A FB4B FB4C FB4D FB4E
"""
POST_COMPOSITION_VERSION = """
2ADC 1D15E 1D15F 1D160 1D161 1D162 1D163 1D164 1D1BB 1D1BC 1D1BD 1D1BE 1D1BF 1D1C0
"""
COMPOSITION_EXCLUSIONS = frozenset(int(x, 16) for x in (SCRIPT_SPECIFIC + POST_COMPOSITION_VERSION).split())

SBASE, LBASE, VBASE, TBASE = 0xAC00, 0x1100, 0x1161, 0x11A7
LCOUNT, VCOUNT, TCOUNT = 19, 21, 28
NCOUNT, SCOUNT = VCOUNT * TCOUNT, LCOUNT * VCOUNT * TCOUNT


def ccc(c: int) -> int:
    return unicodedata.combining(chr(c))


def mapping(c: int, compat: bool) -> tuple[int, ...] | None:
    """The decomposition mapping of c from UnicodeData.txt, or None.

    A compatibility mapping starts with a tag such as <compat>; it is used only when compat holds.
    """
    d = unicodedata.decomposition(chr(c))
    if not d:
        return None
    if d.startswith("<"):
        if not compat:
            return None
        d = d.split(">", 1)[1]
    return tuple(int(x, 16) for x in d.split())


def full_decompose(c: int, compat: bool) -> list[int]:
    """The full canonical (or compatibility) decomposition of one code point, before reordering."""
    s = c - SBASE
    if 0 <= s < SCOUNT:  # @line L6
        jamo = [LBASE + s // NCOUNT, VBASE + (s % NCOUNT) // TCOUNT]
        return jamo + [TBASE + s % TCOUNT] if s % TCOUNT else jamo
    m = mapping(c, compat)  # @line L7
    if m is None:  # @line L8
        return [c]
    out: list[int] = []
    for d in m:  # @line L9
        out.extend(full_decompose(d, compat))
    return out


def canonical_order(d: list[int]) -> None:
    """Sort each run of non-starters by ccc, stably, in place (D108, D109)."""
    for i in range(1, len(d)):  # @line L10
        j = i  # @line L11
        while j > 0 and ccc(d[j - 1]) > ccc(d[j]) > 0:  # @line L12
            d[j - 1], d[j] = d[j], d[j - 1]  # @line L13
            j -= 1


def full_composition_exclusions() -> frozenset[int]:
    """Full_Composition_Exclusion: the listed exclusions, the singletons and the non-starter decompositions."""
    out = set(COMPOSITION_EXCLUSIONS)
    for c in range(0x110000):
        m = mapping(c, False)
        if m is None:
            continue
        if len(m) == 1 or ccc(c) != 0 or ccc(m[0]) != 0:
            out.add(c)
    return frozenset(out)


def build_primary_composites() -> dict[tuple[int, int], int]:
    """Map each pair (first, second) to its primary composite (D114). Hangul is done by arithmetic."""
    excluded = full_composition_exclusions()
    table = {}
    for c in range(0x110000):
        m = mapping(c, False)
        if m is not None and len(m) == 2 and c not in excluded:
            table[m] = c
    return table


PRIMARY = build_primary_composites()


def compose_pair(a: int, b: int) -> int | None:
    """The primary composite of a and b, or None."""
    if LBASE <= a < LBASE + LCOUNT and VBASE <= b < VBASE + VCOUNT:
        return SBASE + ((a - LBASE) * VCOUNT + (b - VBASE)) * TCOUNT
    s = a - SBASE
    if 0 <= s < SCOUNT and s % TCOUNT == 0 and TBASE < b < TBASE + TCOUNT:
        return a + (b - TBASE)
    return PRIMARY.get((a, b))


def compose(d: list[int]) -> list[int]:
    """The canonical composition algorithm (D117) on a canonically ordered sequence."""
    out: list[int] = []
    starter, last = -1, -1  # @line L14
    for c in d:  # @line L15
        k = ccc(c)  # @line L16
        # c is not blocked from out[starter] when nothing lies between them (last = -1),
        # or when every character between them is a non-starter with a smaller ccc.
        p = compose_pair(out[starter], c) if starter >= 0 and (last == -1 or 0 < last < k) else None  # @line L17
        if p is not None:
            out[starter] = p  # @line L18
            continue
        if k == 0:  # @line L19
            starter, last = len(out), -1
        else:
            last = k  # @line L20
        out.append(c)  # @line L21
    return out  # @line L22


def normalize(form: str, s: str) -> str:
    """toNFD, toNFC, toNFKD or toNFKC of s."""
    if form not in ("NFC", "NFD", "NFKC", "NFKD"):
        raise ValueError(form)
    compat = form.startswith("NFK")
    d: list[int] = []  # @line L1
    for ch in s:  # @line L2
        d.extend(full_decompose(ord(ch), compat))
    canonical_order(d)  # @line L3
    if form in ("NFC", "NFKC"):  # @line L4
        d = compose(d)
    return "".join(map(chr, d))  # @line L5


def canonically_equivalent(x: str, y: str) -> bool:
    """D70: equal full canonical decompositions (after canonical ordering)."""
    return normalize("NFD", x) == normalize("NFD", y)
