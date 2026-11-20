# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldstein-branch-cut/. The authors are listed in prov/5RF5DV.jsonl.
"""Goldstein branch cut phase unwrapping (Goldstein, Zebker and Werner 1988).

The input is a wrapped phase image psi[i][j] on an m x n grid of pixels. A
residue is a 2 x 2 square of pixels around which the wrapped differences sum to
2 pi q with q = +1 or -1. The method joins residues by branch cuts until every
group of joined residues has total charge zero or touches the border, and then
unwraps by a flood fill that never crosses a cut.

Geometry. Square (r, c) has the corners (r, c), (r, c+1), (r+1, c+1), (r+1, c).
Two neighbouring squares share one primal edge, and a cut that steps from one
square to the next blocks that edge:

    step (r, c) -> (r+1, c) blocks the edge ('h', r+1, c) between (r+1, c) and (r+1, c+1),
    step (r, c) -> (r, c+1) blocks the edge ('v', r, c+1) between (r, c+1) and (r+1, c+1).

A cut to the border leaves the grid through a boundary edge. ('h', i, j) is the
edge between (i, j) and (i, j+1); ('v', i, j) is the edge between (i, j) and (i+1, j).
"""

from collections import deque
import math

TWO_PI = 2.0 * math.pi


def wrap(x):
    """The value of x - 2 pi k in (-pi, pi]."""
    y = math.fmod(x + math.pi, TWO_PI)
    if y <= 0.0:
        y += TWO_PI
    return y - math.pi


def residues(psi):
    """Charges q[r][c] in {-1, 0, 1} of the (m-1) x (n-1) squares, counterclockwise in (row, column) order."""
    m, n = len(psi), len(psi[0])
    q = [[0] * (n - 1) for _ in range(m - 1)]
    for r in range(m - 1):
        for c in range(n - 1):
            s = (wrap(psi[r][c + 1] - psi[r][c]) + wrap(psi[r + 1][c + 1] - psi[r][c + 1])
                 + wrap(psi[r + 1][c] - psi[r + 1][c + 1]) + wrap(psi[r][c] - psi[r + 1][c]))
            q[r][c] = int(round(s / TWO_PI))
    return q


def _cut_between(blocked, a, b):
    """Block the edges crossed by a staircase path of squares from a to b (rows first, then columns)."""
    r, c = a
    r2, c2 = b
    while r != r2:
        step = 1 if r2 > r else -1
        blocked.add(('h', max(r, r + step), c))
        r += step
    while c != c2:
        step = 1 if c2 > c else -1
        blocked.add(('v', r, max(c, c + step)))
        c += step


def _cut_to_border(blocked, s, m, n):
    """Block a straight path from square s to the nearest side of the grid, including the boundary edge."""
    r, c = s
    options = [(r + 1, 'up'), (m - 1 - r, 'down'), (c + 1, 'left'), (n - 1 - c, 'right')]
    _, side = min(options)
    if side == 'up':
        for i in range(r, -1, -1):
            blocked.add(('h', i, c))
    elif side == 'down':
        for i in range(r + 1, m):
            blocked.add(('h', i, c))
    elif side == 'left':
        for j in range(c, -1, -1):
            blocked.add(('v', r, j))
    else:
        for j in range(c + 1, n):
            blocked.add(('v', r, j))


def branch_cuts(q, max_box=None):
    """Goldstein's cut placement. Returns the set of blocked primal edges.

    q is the residue map of an m x n image, so it has m - 1 rows and n - 1 columns.
    max_box is the largest box radius; None means large enough to reach any border.
    """
    rows, cols = len(q), len(q[0])
    m, n = rows + 1, cols + 1
    if max_box is None:
        max_box = max(rows, cols)
    blocked = set()
    in_tree = [[False] * cols for _ in range(rows)]
    for r0 in range(rows):
        for c0 in range(cols):
            if q[r0][c0] == 0 or in_tree[r0][c0]:
                continue
            tree = [(r0, c0)]  # @line L2
            in_tree[r0][c0] = True
            charge = q[r0][c0]  # @line L3
            k = 1
            while charge != 0 and k <= max_box:  # @line L4
                t_idx = 0
                while charge != 0 and t_idx < len(tree):
                    tr, tc = tree[t_idx]
                    for r in range(max(0, tr - k), min(rows, tr + k + 1)):
                        for c in range(max(0, tc - k), min(cols, tc + k + 1)):
                            if charge != 0 and q[r][c] != 0 and not in_tree[r][c]:  # @line L5
                                _cut_between(blocked, (tr, tc), (r, c))  # @line L6
                                in_tree[r][c] = True
                                tree.append((r, c))
                                charge += q[r][c]
                    if charge != 0 and (tr - k < 0 or tc - k < 0 or tr + k >= rows or tc + k >= cols):
                        _cut_to_border(blocked, (tr, tc), m, n)  # @line L7
                        charge = 0
                    t_idx += 1
                k += 1  # @line L8
            if charge != 0:
                _cut_to_border(blocked, (r0, c0), m, n)  # @line L9
    return blocked


def _neighbours(i, j, m, n, blocked):
    """The pixels joined to (i, j) by an edge that is not blocked."""
    out = []
    if j + 1 < n and ('h', i, j) not in blocked:
        out.append((i, j + 1))
    if j > 0 and ('h', i, j - 1) not in blocked:
        out.append((i, j - 1))
    if i + 1 < m and ('v', i, j) not in blocked:
        out.append((i + 1, j))
    if i > 0 and ('v', i - 1, j) not in blocked:
        out.append((i - 1, j))
    return out


def flood_fill_unwrap(psi, blocked, seeds=None):
    """Unwrap psi by breadth first search over the edges that are not blocked.

    Each region of pixels connected by free edges starts from its first pixel in
    the order of seeds (default: raster order), whose value is psi itself.
    Returns (phi, region) where region[i][j] is the index of the region of (i, j).
    """
    m, n = len(psi), len(psi[0])
    phi = [[0.0] * n for _ in range(m)]
    region = [[-1] * n for _ in range(m)]
    order = seeds if seeds is not None else [(i, j) for i in range(m) for j in range(n)]
    label = 0
    for si, sj in order:
        if region[si][sj] >= 0:
            continue
        phi[si][sj] = psi[si][sj]
        region[si][sj] = label
        queue = deque([(si, sj)])
        while queue:
            i, j = queue.popleft()
            for a, b in _neighbours(i, j, m, n, blocked):
                if region[a][b] < 0:
                    phi[a][b] = phi[i][j] + wrap(psi[a][b] - psi[i][j])  # @line L10
                    region[a][b] = label
                    queue.append((a, b))
        label += 1
    return phi, region


def goldstein_unwrap(psi, max_box=None):
    """Return (phi, blocked edges, region labels) for the wrapped image psi."""
    q = residues(psi)  # @line L1
    blocked = branch_cuts(q, max_box)
    phi, region = flood_fill_unwrap(psi, blocked)
    return phi, blocked, region  # @line L11


def cut_components(q, blocked):
    """Group the squares into components joined by blocked edges between them.

    Returns a list of (total charge, touches_border, squares) for the
    components that contain at least one residue.
    """
    rows, cols = len(q), len(q[0])
    m, n = rows + 1, cols + 1
    seen = [[False] * cols for _ in range(rows)]
    out = []
    for r0 in range(rows):
        for c0 in range(cols):
            if seen[r0][c0]:
                continue
            seen[r0][c0] = True
            stack, squares, border = [(r0, c0)], [], False
            while stack:
                r, c = stack.pop()
                squares.append((r, c))
                if (r == 0 and ('h', 0, c) in blocked) or (r == rows - 1 and ('h', m - 1, c) in blocked):
                    border = True
                if (c == 0 and ('v', r, 0) in blocked) or (c == cols - 1 and ('v', r, n - 1) in blocked):
                    border = True
                steps = [((r + 1, c), ('h', r + 1, c)), ((r - 1, c), ('h', r, c)),
                         ((r, c + 1), ('v', r, c + 1)), ((r, c - 1), ('v', r, c))]
                for (a, b), e in steps:
                    if 0 <= a < rows and 0 <= b < cols and not seen[a][b] and e in blocked:
                        seen[a][b] = True
                        stack.append((a, b))
            charge = sum(q[r][c] for r, c in squares)
            if any(q[r][c] != 0 for r, c in squares):
                out.append((charge, border, squares))
    return out


def l0_cost(phi, psi):
    """The number of edges where the unwrapped difference is not the wrapped difference."""
    m, n = len(psi), len(psi[0])
    cost = 0
    for i in range(m):
        for j in range(n):
            if j + 1 < n and abs(phi[i][j + 1] - phi[i][j] - wrap(psi[i][j + 1] - psi[i][j])) > 1e-9:
                cost += 1
            if i + 1 < m and abs(phi[i + 1][j] - phi[i][j] - wrap(psi[i + 1][j] - psi[i][j])) > 1e-9:
                cost += 1
    return cost
