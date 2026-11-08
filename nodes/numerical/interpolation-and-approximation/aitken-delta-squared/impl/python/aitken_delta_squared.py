# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aitken-delta-squared/. The authors are listed in prov/3C5CRR.jsonl.

"""Aitken's delta-squared process for accelerating sequences."""

from typing import Any, List, Optional, Sequence


def aitken(s: Sequence[Any]) -> List[Optional[Any]]:
    """Return t_0 .. t_{N-2} for s_0 .. s_N, with t_k = s_{k+2} - (Δs_{k+1})^2 / Δ²s_k.

    Where the second difference is zero, t_k is s_{k+2} if the sequence is locally
    constant and None (undefined) otherwise. Cost: 6 operations per output.
    """
    out: List[Optional[Any]] = []
    for k in range(len(s) - 2):  # @line L1
        a = s[k + 1] - s[k]  # @line L2
        b = s[k + 2] - s[k + 1]  # @line L3
        d = b - a  # @line L4
        if d == 0:  # @line L5
            out.append(s[k + 2] if b == 0 else None)
        else:
            out.append(s[k + 2] - b * b / d)  # @line L6
    return out


def aitken_table(s: Sequence[Any]) -> List[List[Any]]:
    """Iterated Aitken: column 0 is s, column j + 1 is aitken(column j).

    Stops when a column would have fewer than one entry or an undefined entry.
    """
    cols: List[List[Any]] = [list(s)]
    while len(cols[-1]) >= 3:
        nxt = aitken(cols[-1])
        if any(v is None for v in nxt):
            break
        cols.append(nxt)
    return cols
