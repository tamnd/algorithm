# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flood-fill/. The authors are listed in prov/M5TTW9.jsonl.


def flood_fill(grid: list[list[int]], row: int, col: int, color: int) -> int:
    """Recolor, in place, the 4-connected region of the seed cell (row, col) with color.

    The region is the set of cells that have the seed's old color and that the seed
    reaches by steps up, down, left and right through such cells. A cell is recolored
    when it is pushed, so it is never pushed twice. Returns the number of recolored
    cells. Time O(k) for a region of k cells, extra space O(k).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if not (0 <= row < rows and 0 <= col < cols):
        raise IndexError("seed cell is outside the grid")
    old = grid[row][col]  # @line L1
    if old == color:  # @line L2
        return 0
    grid[row][col] = color  # @line L3
    stack = [(row, col)]  # @line L4
    count = 1
    while stack:  # @line L5
        r, c = stack.pop()  # @line L6
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):  # @line L7
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == old:  # @line L8
                grid[nr][nc] = color  # @line L9
                stack.append((nr, nc))  # @line L10
                count += 1
    return count  # @line L11
