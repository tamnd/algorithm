# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-localization/. The authors are listed in prov/599C1C.jsonl.

"""Markov localization on a grid map with four headings.

The map m is a list of strings: '#' is a wall and '.' is free.
A pose is (r, c, h): the row r, the column c of a free cell, and the heading
h in 0, 1, 2, 3 for north, east, south and west. Row 0 is the top row.

Motion model p(x_t | u_t, x_(t-1), m), for the controls:
  'F'  move one cell ahead with probability p_move; the robot stays where
       it is with probability 1 - p_move, and also when the cell ahead is a wall;
  'L', 'R'  turn by 90 degrees to the left or to the right (no error).
Measurement model p(z_t | x_t, m): the robot measures the number d of free
cells ahead of it before the first wall. The reading z in 0..z_max is
  (1 - w_rand) * K(z | d) + w_rand / (z_max + 1),
where K puts 3/5 on d and 1/5 on d - 1 and d + 1, clamped to 0..z_max.

The arithmetic is generic: with fractions.Fraction parameters the belief is
exact. A belief is a dict from pose to probability.
"""

from fractions import Fraction

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # north, east, south, west


def free_cells(m):
    return [(r, c) for r, row in enumerate(m) for c, ch in enumerate(row) if ch == "."]


def poses(m):
    """Return all poses of the map, in a fixed order."""
    return [(r, c, h) for (r, c) in free_cells(m) for h in range(4)]


def is_free(m, r, c):
    return 0 <= r < len(m) and 0 <= c < len(m[r]) and m[r][c] == "."


def motion_model(m, x_prev, u, p_move):
    """Return the list of (x_t, probability) with a positive probability."""
    r, c, h = x_prev
    if u == "L":
        return [((r, c, (h + 3) % 4), 1)]
    if u == "R":
        return [((r, c, (h + 1) % 4), 1)]
    if u != "F":
        raise ValueError("unknown control")
    dr, dc = DIRS[h]
    if not is_free(m, r + dr, c + dc):
        return [(x_prev, 1)]
    return [((r + dr, c + dc, h), p_move), (x_prev, 1 - p_move)]


def expected_range(m, x):
    """Return the number of free cells ahead of the pose x before a wall."""
    r, c, h = x
    dr, dc = DIRS[h]
    d = 0
    while is_free(m, r + dr * (d + 1), c + dc * (d + 1)):
        d += 1
    return d


def measurement_model(z, d, z_max, w_rand):
    """Return p(z | d) for a reading z in 0..z_max and a true range d."""
    if not 0 <= z <= z_max:
        return 0 * w_rand
    hit = 0 * w_rand
    for dz, w in ((-1, Fraction(1, 5)), (0, Fraction(3, 5)), (1, Fraction(1, 5))):
        if min(max(d + dz, 0), z_max) == z:
            hit += w
    return (1 - w_rand) * hit + w_rand / (z_max + 1)


def markov_localization(bel, u, z, m, p_move, z_max, w_rand):
    """Return bel(x_t) from bel(x_(t-1)), the control u and the reading z.

    u = None skips the prediction and z = None skips the correction.
    """
    if u is None:
        bel_bar = dict(bel)
    else:
        bel_bar = {x: 0 * p_move for x in bel}  # @line L1
        for x_prev, b in bel.items():  # @line L2
            if b == 0:
                continue
            for x, pr in motion_model(m, x_prev, u, p_move):  # @line L3
                bel_bar[x] += pr * b  # @line L4
    if z is None:
        return bel_bar
    q = {x: measurement_model(z, expected_range(m, x), z_max, w_rand) * b for x, b in bel_bar.items()}  # @line L5
    total = sum(q.values())
    if total == 0:
        raise ValueError("the reading has probability zero under the predicted belief")
    eta = 1 / total  # @line L6
    return {x: eta * v for x, v in q.items()}  # @line L7


def uniform_belief(m, one=Fraction(1)):
    ps = poses(m)
    return {x: one / len(ps) for x in ps}
