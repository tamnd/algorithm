# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unicode-line-breaking-algorithm/. The authors are listed in prov/D4NEZV.jsonl.
"""Line break opportunities by the rules LB1 to LB31 of UAX 14 (Unicode 16.0.0).

The algorithm finds the positions where a line may break and the positions where it
must break. It does not choose the breaks of a paragraph: a line breaker such as the
greedy method or Knuth-Plass picks some of these positions.

The class table is a short subset of LineBreak-16.0.0.txt (Date: 2024-07-29, 16:26:55
GMT). The class values are copied from the file; code points outside the subset get the
default XX of the @missing line, which LB1 resolves to AL. The East Asian width and the
general category (for Pi, Pf and Cn) come from unicodedata.
"""

import bisect
import unicodedata

# (first, last, class) from LineBreak-16.0.0.txt.
_LB_RANGES = [
    (0x0009, 0x0009, "BA"), (0x000A, 0x000A, "LF"), (0x000D, 0x000D, "CR"), (0x0020, 0x0020, "SP"),
    (0x0021, 0x0021, "EX"), (0x0022, 0x0022, "QU"), (0x0023, 0x0023, "AL"), (0x0024, 0x0024, "PR"),
    (0x0025, 0x0025, "PO"), (0x0027, 0x0027, "QU"), (0x0028, 0x0028, "OP"), (0x0029, 0x0029, "CP"),
    (0x002B, 0x002B, "PR"), (0x002C, 0x002C, "IS"), (0x002D, 0x002D, "HY"), (0x002E, 0x002E, "IS"),
    (0x002F, 0x002F, "SY"), (0x0030, 0x0039, "NU"), (0x003A, 0x003B, "IS"), (0x003F, 0x003F, "EX"),
    (0x0041, 0x005A, "AL"), (0x005B, 0x005B, "OP"), (0x005D, 0x005D, "CP"), (0x0061, 0x007A, "AL"),
    (0x007B, 0x007B, "OP"), (0x007D, 0x007D, "CL"), (0x00A0, 0x00A0, "GL"), (0x00AB, 0x00AB, "QU"),
    (0x00AD, 0x00AD, "BA"), (0x00BB, 0x00BB, "QU"), (0x0100, 0x017F, "AL"), (0x0300, 0x034E, "CM"),
    (0x034F, 0x034F, "GL"), (0x0350, 0x035B, "CM"), (0x035C, 0x0362, "GL"), (0x0363, 0x036F, "CM"),
    (0x05BE, 0x05BE, "BA"), (0x05D0, 0x05EA, "HL"), (0x0E01, 0x0E30, "SA"), (0x200B, 0x200B, "ZW"),
    (0x200D, 0x200D, "ZWJ"), (0x2010, 0x2010, "BA"), (0x2014, 0x2014, "B2"), (0x2018, 0x2019, "QU"),
    (0x201B, 0x201D, "QU"), (0x2060, 0x2060, "WJ"), (0x25CC, 0x25CD, "AL"), (0x3000, 0x3000, "BA"),
    (0x3001, 0x3002, "CL"), (0x4E00, 0x9FFF, "ID"), (0xAC00, 0xAC00, "H2"), (0xAC01, 0xAC1B, "H3"),
    (0xFF08, 0xFF08, "OP"), (0xFF09, 0xFF09, "CL"), (0xFF0C, 0xFF0C, "CL"), (0x1F000, 0x1F02F, "ID"),
    (0x1F1E6, 0x1F1FF, "RI"), (0x1F3FB, 0x1F3FF, "EM"), (0x1F466, 0x1F478, "EB"),
    (0x1F6CD, 0x1F6D7, "ID"), (0x20000, 0x2A6DF, "ID"),
]
_STARTS = [r[0] for r in _LB_RANGES]

# One line of emoji-data.txt 16.0.0 (Date: 2024-05-01), for rule LB30b:
#   1F005..1F0CE  ; Extended_Pictographic
_PICT = [(0x1F005, 0x1F0CE)]

HARD = ("BK", "CR", "LF", "NL")
DOTTED_CIRCLE = "◌"
HYPHEN = "‐"


def line_break_class(c: str) -> str:
    """The Line_Break value of c in the subset, XX if c is not in it."""
    cp = ord(c)
    k = bisect.bisect_right(_STARTS, cp) - 1
    if k >= 0 and _LB_RANGES[k][0] <= cp <= _LB_RANGES[k][1]:
        return _LB_RANGES[k][2]
    return "XX"


def resolve(c: str, lb=line_break_class) -> str:
    """Rule LB1: resolve AI, SG, XX, SA and CJ."""
    v = lb(c)
    if v in ("AI", "SG", "XX"):
        return "AL"
    if v == "SA":
        return "CM" if unicodedata.category(c) in ("Mn", "Mc") else "AL"
    if v == "CJ":
        return "NS"
    return v


def east_asian(c: str) -> bool:
    """Membership in $EastAsian: East_Asian_Width F, W or H."""
    return unicodedata.east_asian_width(c) in ("F", "W", "H")


def _pict_unassigned(c: str) -> bool:
    cp = ord(c)
    return any(a <= cp <= b for a, b in _PICT) and unicodedata.category(c) == "Cn"


def units(s: str, c: list) -> tuple:
    """Rules LB9 and LB10. X (CM | ZWJ)* is treated as X when X is not BK, CR, LF, NL, SP
    or ZW; any other CM or ZWJ is treated as AL. Return the units as (class, char) and the
    unit index of each code point."""
    out, unit_of = [], []
    for i, ch in enumerate(s):
        if c[i] in ("CM", "ZWJ"):
            if out and out[-1][0] not in HARD + ("SP", "ZW"):
                unit_of.append(len(out) - 1)
                continue
            out.append(("AL", ch))
        else:
            out.append((c[i], ch))
        unit_of.append(len(out) - 1)
    return out, unit_of


def ri_runs(u: list) -> list:
    """r[k] is the number of RI units that end at unit k, so that LB30a takes O(1) time."""
    r = []
    for k, (cl, _) in enumerate(u):
        r.append(r[-1] + 1 if cl == "RI" and k > 0 and u[k - 1][0] == "RI" else int(cl == "RI"))
    return r


def rule_break(u: list, k: int, ri: list) -> bool:
    """Rules LB11 to LB31 between the units u[k-1] and u[k]. True means a break.
    ri is the list of ri_runs(u)."""
    n = len(u)

    def cls(j):
        return u[j][0] if 0 <= j < n else None

    def back(j, skip):
        while j >= 0 and u[j][0] in skip:
            j -= 1
        return j

    def cat(j):
        return unicodedata.category(u[j][1])

    def ea(j):
        return east_asian(u[j][1])

    def ak(j):  # (AK | U+25CC | AS) of LB28a
        return 0 <= j < n and (u[j][0] in ("AK", "AS") or u[j][1] == DOTTED_CIRCLE)

    a, b = u[k - 1][0], u[k][0]
    j = back(k - 1, ("SP",))  # the unit before the spaces that end at k-1
    if a == "WJ" or b == "WJ":  # LB11
        return False
    if a == "GL":  # LB12
        return False
    if b == "GL" and a not in ("SP", "BA", "HY"):  # LB12a
        return False
    if b in ("CL", "CP", "EX", "SY"):  # LB13
        return False
    if j >= 0 and u[j][0] == "OP":  # LB14
        return False
    if j >= 0 and u[j][0] == "QU" and cat(j) == "Pi" and \
            (j == 0 or cls(j - 1) in HARD + ("OP", "QU", "GL", "SP", "ZW")):  # LB15a
        return False
    if b == "QU" and cat(k) == "Pf" and \
            cls(k + 1) in (None, "SP", "GL", "WJ", "CL", "QU", "CP", "EX", "IS", "SY", "ZW") + HARD:  # LB15b
        return False
    if a == "SP" and b == "IS" and cls(k + 1) == "NU":  # LB15c
        return True
    if b == "IS":  # LB15d
        return False
    if b == "NS" and j >= 0 and u[j][0] in ("CL", "CP"):  # LB16
        return False
    if b == "B2" and j >= 0 and u[j][0] == "B2":  # LB17
        return False
    if a == "SP":  # LB18
        return True
    if (b == "QU" and cat(k) != "Pi") or (a == "QU" and cat(k - 1) != "Pf"):  # LB19
        return False
    if b == "QU" and (not ea(k - 1) or k + 1 == n or not ea(k + 1)):  # LB19a
        return False
    if a == "QU" and (not ea(k) or k - 1 == 0 or not ea(k - 2)):
        return False
    if a == "CB" or b == "CB":  # LB20
        return True
    if (a == "HY" or u[k - 1][1] == HYPHEN) and b == "AL" and \
            (k - 1 == 0 or cls(k - 2) in HARD + ("SP", "ZW", "CB", "GL")):  # LB20a
        return False
    if b in ("BA", "HY", "NS") or a == "BB":  # LB21
        return False
    if cls(k - 2) == "HL" and (a == "HY" or (a == "BA" and not ea(k - 1))) and b != "HL":  # LB21a
        return False
    if a == "SY" and b == "HL":  # LB21b
        return False
    if b == "IN":  # LB22
        return False
    if (a in ("AL", "HL") and b == "NU") or (a == "NU" and b in ("AL", "HL")):  # LB23
        return False
    if (a == "PR" and b in ("ID", "EB", "EM")) or (a in ("ID", "EB", "EM") and b == "PO"):  # LB23a
        return False
    if (a in ("PR", "PO") and b in ("AL", "HL")) or (a in ("AL", "HL") and b in ("PR", "PO")):  # LB24
        return False
    # LB25: NU (SY|IS)* (CL|CP)? x (PO|PR), NU (SY|IS)* x NU, (PO|PR) x OP IS? NU,
    # (PO|PR|HY|IS) x NU.
    m = k - 2 if a in ("CL", "CP") else k - 1
    m = back(m, ("SY", "IS"))
    if m >= 0 and u[m][0] == "NU" and (b in ("PO", "PR") or (b == "NU" and a not in ("CL", "CP"))):
        return False
    if a in ("PO", "PR") and b == "OP" and \
            (cls(k + 1) == "NU" or (cls(k + 1) == "IS" and cls(k + 2) == "NU")):
        return False
    if a in ("PO", "PR", "HY", "IS") and b == "NU":
        return False
    if (a == "JL" and b in ("JL", "JV", "H2", "H3")) or (a in ("JV", "H2") and b in ("JV", "JT")) \
            or (a in ("JT", "H3") and b == "JT"):  # LB26
        return False
    if (a in ("JL", "JV", "JT", "H2", "H3") and b == "PO") or \
            (a == "PR" and b in ("JL", "JV", "JT", "H2", "H3")):  # LB27
        return False
    if a in ("AL", "HL") and b in ("AL", "HL"):  # LB28
        return False
    if (a == "AP" and ak(k)) or (ak(k - 1) and b in ("VF", "VI")) or \
            (a == "VI" and ak(k - 2) and (b == "AK" or u[k][1] == DOTTED_CIRCLE)) or \
            (ak(k - 1) and ak(k) and cls(k + 1) == "VF"):  # LB28a
        return False
    if a == "IS" and b in ("AL", "HL"):  # LB29
        return False
    if (a in ("AL", "HL", "NU") and b == "OP" and not ea(k)) or \
            (a == "CP" and not ea(k - 1) and b in ("AL", "HL", "NU")):  # LB30
        return False
    if a == "RI" and b == "RI" and ri[k - 1] % 2 == 1:  # LB30a
        return False
    if b == "EM" and (a == "EB" or _pict_unassigned(u[k - 1][1])):  # LB30b
        return False
    return True  # LB31


def line_breaks(s: str, lb=line_break_class) -> list:
    """Return (position, mandatory) for every break opportunity, in increasing order.

    Position p is between s[p-1] and s[p]. Position 0 is never a break (LB2) and
    position len(s) always is (LB3). lb maps a character to its Line_Break value.
    """
    n = len(s)
    if n == 0:
        return []
    c = [resolve(ch, lb) for ch in s]  # @line L1
    u, unit_of = units(s, c)  # @line L2
    ri = ri_runs(u)
    out = []  # @line L3
    for i in range(1, n):  # @line L4
        a, b = c[i - 1], c[i]
        if a in ("BK", "LF", "NL") or (a == "CR" and b != "LF"):  # @line L5
            out.append((i, True))
            continue
        if a == "CR" or b in HARD + ("SP", "ZW"):  # @line L6
            continue
        j = i - 1
        while j >= 0 and c[j] == "SP":
            j -= 1
        if j >= 0 and c[j] == "ZW":  # @line L7
            out.append((i, False))
            continue
        if a == "ZWJ" or unit_of[i] == unit_of[i - 1]:  # @line L8
            continue
        if rule_break(u, unit_of[i], ri):  # @line L9
            out.append((i, False))
    out.append((n, True))  # @line L10
    return out


def break_positions(s: str, lb=line_break_class) -> list:
    """The positions of all break opportunities, mandatory or not."""
    return [p for p, _ in line_breaks(s, lb)]


def segments(s: str, lb=line_break_class) -> list:
    """Split s at every break opportunity."""
    out, prev = [], 0
    for p in break_positions(s, lb):
        out.append(s[prev:p])
        prev = p
    return out
