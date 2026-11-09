# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algorithm-x/. The authors are listed in prov/0R5E65.jsonl.

from collections.abc import Hashable, Iterator, Sequence


def algorithm_x(
    primary: Sequence[Hashable],
    options: Sequence[Sequence[Hashable]],
    secondary: Sequence[Hashable] = (),
) -> Iterator[list[int]]:
    """Yield every exact cover, as a list of option indices in the order chosen.

    Each primary item must be covered exactly once, and each secondary item
    at most once. Each option must contain at least one primary item. Option j is the set of items options[j]. The search always
    branches on an active primary item with the fewest active options, the
    first such item in the order of `primary` when there is a tie, and it
    tries the options of that item in increasing index order. The recursion
    depth is at most the number of primary items.
    """
    prim = list(primary)
    sec = list(secondary)
    if len(set(prim) | set(sec)) != len(prim) + len(sec):
        raise ValueError("items must be distinct")
    known = set(prim) | set(sec)
    rows: list[list[Hashable]] = []
    for opt in options:
        row = list(opt)
        if len(set(row)) != len(row) or not set(row) <= known:
            raise ValueError("an option repeats an item or uses an unknown item")
        if not set(row) & set(prim):
            raise ValueError("each option must contain a primary item")
        rows.append(row)

    # cols[i] is the set of active options that contain item i.
    cols: dict[Hashable, set[int]] = {i: set() for i in prim + sec}
    for j, row in enumerate(rows):
        for i in row:
            cols[i].add(j)
    active_primary = list(prim)  # the order breaks ties in line L4
    alive = set(prim)
    prim_set = set(prim)
    solution: list[int] = []

    def cover(i: Hashable) -> None:
        # Remove item i and every option that contains it from the other lists.
        for j in cols[i]:
            for k in rows[j]:
                if k != i:
                    cols[k].discard(j)
        alive.discard(i)

    def uncover(i: Hashable) -> None:
        for j in cols[i]:
            for k in rows[j]:
                if k != i:
                    cols[k].add(j)
        if i in prim_set:
            alive.add(i)

    def search() -> Iterator[list[int]]:
        if not alive:  # @line L1
            yield list(solution)  # @line L2
            return  # @line L3
        best = None  # @line L4
        for i in active_primary:
            if i in alive and (best is None or len(cols[i]) < len(cols[best])):
                best = i
        cover(best)  # @line L5
        for j in sorted(cols[best]):  # @line L6
            solution.append(j)  # @line L7
            others = [k for k in rows[j] if k != best]
            for k in others:  # @line L8
                cover(k)
            yield from search()  # @line L9
            for k in reversed(others):  # @line L10
                uncover(k)
            solution.pop()  # @line L11
        uncover(best)  # @line L12

    yield from search()


def count_exact_covers(
    primary: Sequence[Hashable],
    options: Sequence[Sequence[Hashable]],
    secondary: Sequence[Hashable] = (),
) -> int:
    """Return the number of exact covers."""
    return sum(1 for _ in algorithm_x(primary, options, secondary))


def first_exact_cover(
    primary: Sequence[Hashable],
    options: Sequence[Sequence[Hashable]],
    secondary: Sequence[Hashable] = (),
) -> list[int] | None:
    """Return the first exact cover found, as sorted option indices, or None."""
    for s in algorithm_x(primary, options, secondary):
        return sorted(s)
    return None
