# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ovsf-codes/. The authors are listed in prov/MV4CVC.jsonl.

"""Orthogonal variable spreading factor (OVSF) codes, in integers.

The code C(SF, k), for SF a power of two and 0 <= k < SF, is a list of SF
values +1 or -1, with the 3GPP numbering:
    C(1, 0) = (1),
    C(2N, 2k) = (C(N, k), C(N, k)),
    C(2N, 2k + 1) = (C(N, k), -C(N, k)).
The parent of C(SF, k) is C(SF / 2, k // 2).
"""


def _check(sf: int, k: int) -> None:
    if sf < 1 or sf & (sf - 1) or not 0 <= k < sf:
        raise ValueError("need SF a power of two and 0 <= k < SF")


def ovsf(sf: int, k: int) -> list[int]:
    """The code C(SF, k) as a list of +1 and -1."""
    _check(sf, k)
    if sf == 1:  # @line L1
        return [1]
    p = ovsf(sf // 2, k // 2)  # @line L2
    if k % 2 == 0:  # @line L3
        return p + p
    return p + [-v for v in p]  # @line L4


def is_ancestor(sf1: int, k1: int, sf2: int, k2: int) -> bool:
    """True if C(sf1, k1) lies on the path from the root to C(sf2, k2) (a code is its own ancestor)."""
    _check(sf1, k1)
    _check(sf2, k2)
    if sf1 > sf2:
        return False
    return k2 // (sf2 // sf1) == k1


def orthogonal(sf1: int, k1: int, sf2: int, k2: int) -> bool:
    """True if two codes stay orthogonal for any data: neither is an ancestor of the other."""
    return not is_ancestor(sf1, k1, sf2, k2) and not is_ancestor(sf2, k2, sf1, k1)  # @line L5


def spread(symbols: list[int], code: list[int]) -> list[int]:
    """Each symbol times the whole code, one after another."""
    return [s * c for s in symbols for c in code]


def despread(chips: list[int], code: list[int]) -> list[int]:
    """Correlate each block of len(code) chips with the code."""
    n = len(code)
    return [sum(chips[i + j] * code[j] for j in range(n)) for i in range(0, len(chips), n)]


def sylvester_row(sf: int, i: int) -> list[int]:
    """Row i of the Sylvester-Hadamard matrix of order SF: (-1)^popcount(i AND j)."""
    return [1 - 2 * (bin(i & j).count("1") % 2) for j in range(sf)]


def bit_reverse(k: int, bits: int) -> int:
    out = 0
    for _ in range(bits):
        out = (out << 1) | (k & 1)
        k >>= 1
    return out


def valid_assignment(codes: list[tuple[int, int]]) -> bool:
    """True if no assigned code is an ancestor of another."""
    for i, (sa, ka) in enumerate(codes):
        for sb, kb in codes[i + 1:]:
            if not orthogonal(sa, ka, sb, kb):
                return False
    return True


def allocate(used: list[tuple[int, int]], sf: int) -> tuple[int, int] | None:
    """The leftmost code of spreading factor SF that is orthogonal to every used code, or None."""
    for k in range(sf):
        if all(orthogonal(sf, k, su, ku) for su, ku in used):
            return (sf, k)
    return None
