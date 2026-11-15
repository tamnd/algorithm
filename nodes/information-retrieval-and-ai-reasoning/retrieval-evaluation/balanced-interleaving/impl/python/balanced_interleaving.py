# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-interleaving/. The authors are listed in prov/8GEA8G.jsonl.

from typing import Collection, Hashable, Sequence


def interleave(a: Sequence[Hashable], b: Sequence[Hashable], a_first: bool) -> list[Hashable]:
    """Return the balanced interleaving of rankings a and b.

    Precondition: a and b have no repeated documents. a_first is the coin that
    breaks the tie when both pointers are equal. Each loop step advances one
    pointer, so there are at most len(a) + len(b) steps, each O(1) with a hash set:
    O(len(a) + len(b)) time and space.
    """
    out: list[Hashable] = []
    shown: set[Hashable] = set()
    ka, kb = 0, 0  # @line L1
    while ka < len(a) and kb < len(b):  # @line L2
        if ka < kb or (ka == kb and a_first):  # @line L3
            if a[ka] not in shown:  # @line L4
                out.append(a[ka])
                shown.add(a[ka])
            ka += 1  # @line L5
        else:  # @line L6
            if b[kb] not in shown:  # @line L7
                out.append(b[kb])
                shown.add(b[kb])
            kb += 1  # @line L8
    return out  # @line L9


def credit(
    a: Sequence[Hashable], b: Sequence[Hashable], shown: Sequence[Hashable], clicked: Collection[Hashable]
) -> int:
    """Return 1 if the clicks prefer a, -1 if they prefer b, and 0 for no preference.

    Precondition: shown is the interleaved list built from a and b, and clicked is a
    set of documents of shown. The cost is O(len(a) + len(b) + len(shown)) time.
    """
    if not clicked:  # @line L10
        return 0
    pos = {d: i for i, d in enumerate(shown)}
    low = max(clicked, key=lambda d: pos[d])  # @line L11
    inf = len(a) + len(b) + 1
    ra = a.index(low) + 1 if low in a else inf
    rb = b.index(low) + 1 if low in b else inf
    k = min(ra, rb)  # @line L12
    ha = sum(1 for d in a[:k] if d in clicked)  # @line L13
    hb = sum(1 for d in b[:k] if d in clicked)
    return (ha > hb) - (ha < hb)  # @line L14
