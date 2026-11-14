# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/line-probe-routing/. The authors are listed in prov/CEQKHV.jsonl.

from typing import Optional, Sequence

Cell = tuple[int, int]

H, V = 0, 1  # orientation of a probe line: horizontal (along a row) or vertical


def is_free(grid: Sequence[str], cell: Cell) -> bool:
    r, c = cell
    return 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#"


def probe_line(grid: Sequence[str], b: Cell, o: int) -> list[Cell]:
    """The cells of the longest free horizontal (o = H) or vertical (o = V) segment through b."""
    dr, dc = (0, 1) if o == H else (1, 0)
    lo = b
    while is_free(grid, (lo[0] - dr, lo[1] - dc)):
        lo = (lo[0] - dr, lo[1] - dc)
    cells = []
    cur = lo
    while is_free(grid, cur):
        cells.append(cur)
        cur = (cur[0] + dr, cur[1] + dc)
    return cells


def chain(base: dict[Cell, Cell], c: Cell) -> list[Cell]:
    """Cells from c back to the origin of its side, following each line to its base point."""
    out = [c]
    cur = c
    while base[cur] != cur:
        b = base[cur]
        dr = (b[0] > cur[0]) - (b[0] < cur[0])
        dc = (b[1] > cur[1]) - (b[1] < cur[1])
        while cur != b:
            cur = (cur[0] + dr, cur[1] + dc)
            out.append(cur)
    return out


def remove_loops(path: list[Cell]) -> list[Cell]:
    """Cut out every closed loop, so that no cell repeats."""
    out: list[Cell] = []
    pos: dict[Cell, int] = {}
    for c in path:
        if c in pos:
            k = pos[c]
            for d in out[k + 1:]:
                del pos[d]
            del out[k + 1:]
        else:
            pos[c] = len(out)
            out.append(c)
    return out


def line_probe_search(grid: Sequence[str], s: Cell, t: Cell) -> tuple[Optional[Cell], list[dict[Cell, Cell]], list[list[tuple[int, Cell, int]]]]:
    """Mikami-Tabuchi line probes from s and t, level by level.

    Returns the meeting cell (or None), the base point of each covered cell for
    each side, and for each level the lines drawn as (side, base point, orientation).
    """
    base: list[dict[Cell, Cell]] = [{s: s}, {t: t}]
    covered: list[list[set[Cell]]] = [[set(), set()], [set(), set()]]
    levels: list[list[tuple[int, Cell, int]]] = []
    if s == t:
        return s, base, levels
    todo: list[list[tuple[Cell, int]]] = [[(s, H), (s, V)], [(t, H), (t, V)]]  # @line L1
    while todo[0] or todo[1]:  # @line L2
        drawn: list[tuple[int, Cell, int]] = []
        new_todo: list[list[tuple[Cell, int]]] = [[], []]  # @line L4
        for side in (0, 1):  # @line L3
            for b, o in todo[side]:  # @line L5
                if b in covered[side][o]:  # @line L6
                    continue
                drawn.append((side, b, o))
                for c in probe_line(grid, b, o):  # @line L7
                    covered[side][o].add(c)
                    if c in base[side]:  # @line L8
                        continue
                    base[side][c] = b  # @line L9
                    if c in base[1 - side]:  # @line L10
                        levels.append(drawn)
                        return c, base, levels
                    new_todo[side].append((c, 1 - o))  # @line L11
        levels.append(drawn)
        todo = new_todo  # @line L12
    return None, base, levels  # @line L13


def line_probe_routing(grid: Sequence[str], s: Cell, t: Cell) -> Optional[list[Cell]]:
    """Return a path of cells from s to t found by Mikami-Tabuchi line probes, or None.

    grid is a list of equal-length strings, '#' marks a blocked cell. A path is
    found whenever one exists. It need not be shortest.
    """
    if not is_free(grid, s) or not is_free(grid, t):
        return None
    meet, base, _ = line_probe_search(grid, s, t)
    if meet is None:
        return None
    from_s = chain(base[0], meet)
    from_s.reverse()
    to_t = chain(base[1], meet)
    return remove_loops(from_s + to_t[1:])
