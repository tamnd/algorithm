# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ephemeron/. The authors are listed in prov/DGVSB7.jsonl.

"""Marking with ephemerons (Hayes 1997).

The heap: objects 0 .. n-1, strong edges edges[x], and a map eph from an
ephemeron object e to its pair (key, value). An ephemeron keeps its value
alive only while the ephemeron itself and its key are both alive. The live
set is the least set that holds the roots and is closed under the strong
edges and this rule. One traversal finds it: an ephemeron whose key is not
yet marked waits on a list of that key, and marking the key releases it.
"""


def mark_with_ephemerons(
    edges: dict[int, list[int]],
    eph: dict[int, tuple[int, int]],
    roots: list[int],
) -> tuple[set[int], list[int]]:
    """Return the live set and the ephemerons to clear (live, with a dead key)."""
    marked: set[int] = set()
    stack: list[int] = []
    waiting: dict[int, list[int]] = {}

    def mark(y: int) -> None:
        if y not in marked:
            marked.add(y)
            stack.append(y)

    for r in roots:
        mark(r)
    while stack:
        x = stack.pop()
        for e in waiting.pop(x, []):  # x is a key that ephemerons wait for
            mark(eph[e][1])
        if x in eph:
            k, v = eph[x]
            if k in marked:
                mark(v)
            else:
                waiting.setdefault(k, []).append(x)
        for y in edges.get(x, []):
            mark(y)
    cleared = sorted(e for e in eph if e in marked and eph[e][0] not in marked)
    return marked, cleared


def mark_with_weak_pairs(
    edges: dict[int, list[int]],
    eph: dict[int, tuple[int, int]],
    roots: list[int],
) -> set[int]:
    """The weak pair rule for contrast: the key is weak, the value is strong."""
    seen, stack = set(roots), list(roots)
    while stack:
        x = stack.pop()
        succ = list(edges.get(x, []))
        if x in eph:
            succ.append(eph[x][1])
        for y in succ:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return seen
