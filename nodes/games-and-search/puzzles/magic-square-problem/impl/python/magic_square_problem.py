# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magic-square-problem/. The authors are listed in prov/DGVTGW.jsonl.
"""Normal magic squares: construction for every order n >= 3, and counting.

A normal magic square of order n holds 1..n^2 once each, and every row,
every column and both main diagonals sum to the magic constant
n(n^2 + 1)/2.

Construction: the Siamese method for odd n, the complement method for
n divisible by 4, and Conway's LUX method for n = 4m + 2.
Counting: brute force over all permutations for n <= 3, and a search with
forced cells for n = 4.
"""

from itertools import permutations


def magic_constant(n):
    return n * (n * n + 1) // 2


def is_magic(square):
    """True if the square is a normal magic square."""
    n = len(square)
    if any(len(row) != n for row in square):
        return False
    if sorted(v for row in square for v in row) != list(range(1, n * n + 1)):
        return False
    m = magic_constant(n)
    lines = [list(row) for row in square] + [[square[r][c] for r in range(n)] for c in range(n)]
    lines.append([square[i][i] for i in range(n)])
    lines.append([square[i][n - 1 - i] for i in range(n)])
    return all(sum(line) == m for line in lines)


def siamese(n):
    """De la Loubère's method for odd n."""
    sq = [[0] * n for _ in range(n)]
    i, j = 0, n // 2
    for v in range(1, n * n + 1):
        sq[i][j] = v
        if sq[(i - 1) % n][(j + 1) % n]:
            i = (i + 1) % n
        else:
            i, j = (i - 1) % n, (j + 1) % n
    return sq


def complement(n):
    """For n divisible by 4: write 1..n^2 in order, then complement the cells
    on the diagonals of each 4 by 4 block."""
    sq = [[r * n + c + 1 for c in range(n)] for r in range(n)]  # @line L3
    for r in range(n):
        for c in range(n):
            if (r % 4 in (0, 3)) == (c % 4 in (0, 3)):  # @line L4
                sq[r][c] = n * n + 1 - sq[r][c]
    return sq


# Order of 1..4 inside the 2 by 2 block, by letter.
_PATTERN = {"L": ((4, 1), (2, 3)), "U": ((1, 4), (2, 3)), "X": ((1, 4), (3, 2))}


def lux(n):
    """Conway's LUX method for n = 4m + 2 with m >= 1."""
    m = (n - 2) // 4
    k = 2 * m + 1
    small = siamese(k)  # @line L6
    letter = [["L"] * k for _ in range(m + 1)] + [["U"] * k] + [["X"] * k for _ in range(m - 1)]
    letter[m][m], letter[m + 1][m] = "U", "L"
    sq = [[0] * n for _ in range(n)]
    for r in range(k):
        for c in range(k):
            base = 4 * (small[r][c] - 1)
            pat = _PATTERN[letter[r][c]]
            for dr in range(2):
                for dc in range(2):
                    sq[2 * r + dr][2 * c + dc] = base + pat[dr][dc]  # @line L7
    return sq


def magic_square(n):
    """A normal magic square of order n, or None for n = 2."""
    if n == 2:
        return None
    if n % 2 == 1:
        return siamese(n)  # @line L1
    if n % 4 == 0:  # @line L2
        return complement(n)
    sq = lux(n)  # @line L5
    return sq  # @line L8


def symmetries(square):
    """The 8 images of the square under rotations and reflections."""
    out = []
    sq = [list(row) for row in square]
    for _ in range(4):
        sq = [list(row) for row in zip(*sq[::-1])]
        out.append(sq)
        out.append([row[::-1] for row in sq])
    return out


def normal_form(square):
    """Frénicle's standard form: the image with the smallest corner at the top
    left and its right neighbor smaller than the cell below it."""
    return min(symmetries(square))


def count_brute_force(n):
    """All normal magic squares of order n, by listing every arrangement of
    1..n^2 (use only for n <= 3)."""
    found = []
    m = magic_constant(n)
    for perm in permutations(range(1, n * n + 1)):
        if sum(perm[:n]) != m:
            continue
        sq = [list(perm[r * n:(r + 1) * n]) for r in range(n)]
        if is_magic(sq):
            found.append(sq)
    return found


def count_order_four():
    """Magic squares of order 4 up to rotation and reflection.

    Frénicle's form fixes the symmetry: the top left corner a is the smallest
    corner, and the cell right of it is smaller than the cell below it. Eight
    cells are chosen; the other eight are forced by the line sums.
    """
    s = 34
    full = frozenset(range(1, 17))
    count = 0
    for a in range(1, 17):
        for b in full - {a}:
            for c in full - {a, b}:
                d = s - a - b - c  # row 0
                if not a < d <= 16 or d in (b, c):
                    continue
                u1 = {a, b, c, d}
                for e in full - u1:
                    if e < b:
                        continue
                    for i in full - u1 - {e}:
                        m = s - a - e - i  # column 0
                        if not a < m <= 16 or m in u1 or m in (e, i):
                            continue
                        u3 = u1 | {e, i, m}
                        for f in full - u3:
                            for k in full - u3 - {f}:
                                p = s - a - f - k  # main diagonal
                                if not a < p <= 16 or p in u3 or p in (f, k):
                                    continue
                                u5 = u3 | {f, k, p}
                                for g in full - u5:
                                    j = s - d - g - m  # other diagonal
                                    h = s - e - f - g  # row 1
                                    if not (0 < j <= 16 and 0 < h <= 16) or len({g, j, h}) < 3:
                                        continue
                                    if j in u5 or h in u5:
                                        continue
                                    l = s - i - j - k  # row 2
                                    n = s - b - f - j  # column 1
                                    o = s - c - g - k  # column 2
                                    rest = full - u5 - {g, j, h}
                                    if (len({l, n, o}) == 3 and {l, n, o} <= rest
                                            and d + h + l + p == s and m + n + o + p == s):
                                        count += 1
    return count
