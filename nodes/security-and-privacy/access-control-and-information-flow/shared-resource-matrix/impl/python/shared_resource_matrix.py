# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-resource-matrix/. The authors are listed in prov/3Z77T4.jsonl.

from collections.abc import Mapping, Sequence

Table = Mapping[str, Mapping[str, str]]


def from_rows(rows: Table) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Turn a matrix given by rows into the reference and modify sets of each primitive.

    rows[a][p] is a string that holds "R" when primitive p references attribute a
    and "M" when p modifies a, for example "R", "M" or "R/M". A missing entry is
    blank. Cost: O(number of entries).
    """
    refs: dict[str, set[str]] = {}
    mods: dict[str, set[str]] = {}
    for a, row in rows.items():
        for p, entry in row.items():
            refs.setdefault(p, set())
            mods.setdefault(p, set())
            if "R" in entry:
                refs[p].add(a)
            if "M" in entry:
                mods[p].add(a)
    return refs, mods


def shared_resource_matrix(
    attributes: Sequence[str],
    refs: Mapping[str, set[str]],
    mods: Mapping[str, set[str]],
) -> tuple[dict[str, set[str]], list[tuple[str, list[str], list[str]]]]:
    """Close the shared resource matrix and list the candidate attributes.

    Precondition: every attribute named in refs or mods is in attributes, and
    refs and mods have the same keys (the primitives). The closure follows the
    rule of Kemmerer: if p references a and q modifies a, then p also references
    every attribute that q references. The result is the closed reference set of
    each primitive, and for each attribute that some primitive modifies and some
    primitive references after the closure, the triple (attribute, modifiers,
    sensors) in the order of attributes. These are candidates for a channel, not
    proved channels. Cost: O(m n^2) time and O(n^2 + m n) space for n attributes
    and m primitives.
    """
    edges: dict[str, set[str]] = {a: set() for a in attributes}  # @line L1
    for q in refs:  # @line L2
        for a in mods[q]:  # @line L3
            edges[a] |= refs[q]  # @line L4
    closed: dict[str, set[str]] = {}
    for p in refs:  # @line L5
        seen = set(refs[p])  # @line L6
        stack = list(refs[p])
        while stack:  # @line L7
            a = stack.pop()  # @line L8
            for b in edges[a]:  # @line L9
                if b not in seen:
                    seen.add(b)  # @line L10
                    stack.append(b)
        closed[p] = seen
    candidates: list[tuple[str, list[str], list[str]]] = []  # @line L11
    for a in attributes:  # @line L12
        modifiers = [p for p in refs if a in mods[p]]  # @line L13
        sensors = [p for p in refs if a in closed[p]]
        if modifiers and sensors:
            candidates.append((a, modifiers, sensors))
    return closed, candidates  # @line L14
