# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kinematic-fixture-analysis/. The authors are listed in prov/E79S9A.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations, product

from kinematic_fixture_analysis import (
    analyze,
    apply,
    cross,
    detach_twist,
    dot,
    error_twist,
    jacobian,
    rank,
)

# Faces of the box [0, 2]^3: (axis, value, inward normal).
FACES = [
    (0, 0, (1, 0, 0)),
    (0, 2, (-1, 0, 0)),
    (1, 0, (0, 1, 0)),
    (1, 2, (0, -1, 0)),
    (2, 0, (0, 0, 1)),
    (2, 2, (0, 0, -1)),
]

EZ, EY, EX = (0, 0, 1), (0, 1, 0), (1, 0, 0)
BLOCK = [
    ((20, 10, 0), EZ),
    ((80, 10, 0), EZ),
    ((50, 50, 0), EZ),
    ((20, 0, 20), EY),
    ((80, 0, 20), EY),
    ((0, 30, 20), EX),
]
CLAMPS = [((100, 30, 20), (-1, 0, 0)), ((50, 60, 20), (0, -1, 0)), ((50, 30, 40), (0, 0, -1))]


def box_contact(rng):
    axis, value, n = rng.choice(FACES)
    p = [rng.randint(0, 2) for _ in range(3)]
    p[axis] = value
    return (tuple(p), n)


def det(m):
    """Determinant by Laplace expansion along the first row."""
    if len(m) == 1:
        return m[0][0]
    total = 0
    for j in range(len(m)):
        if m[0][j] == 0:
            continue
        minor = [row[:j] + row[j + 1 :] for row in m[1:]]
        total += (-1) ** j * m[0][j] * det(minor)
    return total


def rank_by_minors(rows):
    """The largest k with a nonzero k x k minor."""
    for k in range(min(len(rows), 6), 0, -1):
        for rs in combinations(range(len(rows)), k):
            for cs in combinations(range(6), k):
                if det([[rows[r][c] for c in cs] for r in rs]) != 0:
                    return k
    return 0


def cayley(w):
    """The exact rational rotation (I - C)^-1 (I + C) with C = [w / 2]x."""
    c = [Fraction(v) / 2 for v in w]
    s = 2 / (1 + dot(c, c))
    cm = [[0, -c[2], c[1]], [c[2], 0, -c[0]], [-c[1], c[0], 0]]
    c2 = [[sum(cm[i][k] * cm[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return [[int(i == j) + s * (cm[i][j] + c2[i][j]) for j in range(3)] for i in range(3)]


def mat_vec(r, v):
    return [sum(r[i][k] * v[k] for k in range(3)) for i in range(3)]


def finite_gaps(contacts, xi, t):
    """The gaps after the finite rigid motion R = cayley(t w), d = t delta.

    The part surface at contact i is the plane through p_i with normal n_i.
    After the motion it is the plane through R p_i + d with normal R n_i,
    and the gap is the signed distance of the fixed locator p_i from it,
    times |n_i|.
    """
    delta = [t * v for v in xi[:3]]
    r = cayley([t * v for v in xi[3:]])
    gaps = []
    for p, n in contacts:
        moved = mat_vec(r, p)
        rn = mat_vec(r, n)
        gaps.append(dot(rn, [moved[k] + delta[k] - p[k] for k in range(3)]))
    return gaps


def in_cone(rows, target, r):
    """Is target a nonnegative combination of rows? (Caratheodory: try every
    basis of r rows of the span; target is assumed to lie in the span.)"""
    for subset in combinations(range(len(rows)), r):
        cols = [rows[i] for i in subset]
        aug = [[cols[j][k] for j in range(r)] + [target[k]] for k in range(6)]
        coeffs = _solve_consistent(aug, r)
        if coeffs is not None and all(c >= 0 for c in coeffs):
            return True
    return False


def _solve_consistent(aug, r):
    """Solve a 6 x r system with full column rank, or None if the columns are dependent."""
    a = [list(row) for row in aug]
    row = 0
    for c in range(r):
        piv = next((i for i in range(row, 6) if a[i][c] != 0), None)
        if piv is None:
            return None
        a[row], a[piv] = a[piv], a[row]
        a[row] = [v / a[row][c] for v in a[row]]
        for i in range(6):
            if i != row and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[row])]
        row += 1
    return [a[i][r] for i in range(r)]


def positively_spans_its_span(rows):
    r = rank(rows)
    return all(in_cone(rows, [-v for v in w], r) for w in rows)


class TestWorkedBlock(unittest.TestCase):
    def test_rank_and_det(self):
        j = jacobian(BLOCK)
        self.assertEqual(j[0], [0, 0, 1, 10, -20, 0])
        self.assertEqual(rank(j), 6)
        self.assertEqual(abs(det(j)), 144000)  # 2 * area 1200 * spacing 60

    def test_locating_is_not_holding(self):
        rep = analyze(BLOCK)
        self.assertTrue(rep.deterministic)
        self.assertFalse(rep.form_closure)
        g = apply(jacobian(BLOCK), rep.detach_twist)
        self.assertTrue(all(v >= 0 for v in g) and any(v > 0 for v in g))
        self.assertEqual(error_twist(BLOCK, [1] * 6), [1, 1, 1, 0, 0, 0])

    def test_error_amplification(self):
        xi = error_twist(BLOCK, [0, 0, 0, 0, Fraction(1, 100), 0])
        self.assertEqual(xi[5], Fraction(1, 6000))  # 0.01 / 60

    def test_clamps(self):
        self.assertFalse(analyze(BLOCK + CLAMPS[2:]).form_closure)
        self.assertTrue(analyze(BLOCK + CLAMPS).form_closure)

    def test_degenerate_layouts(self):
        collinear = list(BLOCK)
        collinear[2] = ((50, 10, 0), EZ)
        rep = analyze(collinear)
        self.assertEqual(rep.rank, 5)
        self.assertEqual(rep.null_twists, [[0, 20, -10, 1, 0, 0]])
        stacked = list(BLOCK)
        stacked[4] = ((20, 0, 30), EY)
        rep = analyze(stacked)
        self.assertEqual(rep.rank, 5)
        self.assertEqual(rep.null_twists, [[30, -20, 0, 0, 0, 1]])


class TestVBlock(unittest.TestCase):
    def test_cylinder_turns_about_its_axis(self):
        a, b = Fraction(3, 5), Fraction(4, 5)
        vee = [
            ((0, a, -b), (0, -a, b)),
            ((0, -a, -b), (0, a, b)),
            ((4, a, -b), (0, -a, b)),
            ((4, -a, -b), (0, a, b)),
            ((0, Fraction(1, 5), 0), (1, 0, 0)),
        ]
        rep = analyze(vee)
        self.assertEqual(rep.rank, 5)
        self.assertEqual(rep.null_twists, [[0, 0, 0, 1, 0, 0]])
        flat = ((2, Fraction(1, 2), b), (0, 0, -1))
        self.assertEqual(analyze(vee + [flat]).rank, 6)


class TestAgainstBruteForce(unittest.TestCase):
    def test_rank_matches_minors(self):
        rng = random.Random(7)
        for _ in range(60):
            contacts = [box_contact(rng) for _ in range(rng.randint(1, 7))]
            j = jacobian(contacts)
            self.assertEqual(rank(j), rank_by_minors(j))

    def test_first_order_gaps(self):
        """The finite motion of size t changes gap i by t J_i xi + O(t^2)."""
        rng = random.Random(11)
        t = Fraction(1, 10**6)
        for _ in range(40):
            contacts = [box_contact(rng) for _ in range(6)]
            xi = [rng.randint(-3, 3) for _ in range(6)]
            first = apply(jacobian(contacts), xi)
            for g, f in zip(finite_gaps(contacts, xi, t), first):
                self.assertLess(abs(g / t - f), Fraction(1, 1000))

    def test_null_twists_move_no_gap(self):
        rng = random.Random(3)
        t = Fraction(1, 10**6)
        seen = 0
        for _ in range(60):
            contacts = [box_contact(rng) for _ in range(rng.randint(3, 7))]
            rep = analyze(contacts)
            self.assertEqual(rep.deterministic, rep.rank == 6)
            self.assertEqual(len(rep.null_twists), 6 - rep.rank)
            for xi in rep.null_twists:
                seen += 1
                self.assertTrue(any(v != 0 for v in xi))
                for g in finite_gaps(contacts, xi, t):
                    self.assertLess(abs(g / t), Fraction(1, 1000))
        self.assertGreater(seen, 20)

    def test_full_rank_has_no_grid_null_twist(self):
        """Search all twists in {-1, 0, 1}^6 with exact finite motions."""
        rng = random.Random(5)
        t = Fraction(1, 10**6)
        grid = [xi for xi in product((-1, 0, 1), repeat=6) if any(xi)]
        done = 0
        while done < 4:
            contacts = [box_contact(rng) for _ in range(6)]
            j = jacobian(contacts)
            if rank(j) != 6:
                continue
            done += 1
            for xi in grid:
                if all(v == 0 for v in apply(j, xi)):
                    self.fail("full rank but a null twist")
            xi = grid[rng.randrange(len(grid))]
            gaps = finite_gaps(contacts, xi, t)
            self.assertTrue(any(abs(g / t) > Fraction(1, 2) for g in gaps))

    def test_detach_matches_positive_span(self):
        """Stiemke: no detaching twist exactly when the rows positively span their span."""
        rng = random.Random(13)
        closed = 0
        for trial in range(80):
            contacts = [box_contact(rng) for _ in range(rng.randint(2, 8))]
            if trial % 2:
                # Pair some contacts with the point straight across the box:
                # the two rows are opposite, so the cone holds a line.
                for p, n in contacts[: rng.randint(1, 4)]:
                    axis = [abs(v) for v in n].index(1)
                    q = list(p)
                    q[axis] = 2 - q[axis]
                    contacts.append((tuple(q), tuple(-v for v in n)))
            j = jacobian(contacts)
            d = detach_twist(j)
            if d is not None:
                g = apply(j, d)
                self.assertTrue(all(v >= 0 for v in g) and any(v > 0 for v in g))
            self.assertEqual(d is None, positively_spans_its_span(j))
            closed += d is None
        self.assertGreater(closed, 0)
        for contacts, expect in ((BLOCK + CLAMPS, True), (BLOCK + CLAMPS[2:], False)):
            j = jacobian(contacts)
            self.assertEqual(positively_spans_its_span(j), expect)
            self.assertEqual(detach_twist(j) is None, expect)

    def test_six_contacts_never_close(self):
        rng = random.Random(17)
        for _ in range(40):
            contacts = [box_contact(rng) for _ in range(6)]
            self.assertFalse(analyze(contacts).form_closure)

    def test_positive_scaling_and_order(self):
        rng = random.Random(19)
        for _ in range(20):
            contacts = [box_contact(rng) for _ in range(rng.randint(4, 8))]
            rep = analyze(contacts)
            scaled = [(p, tuple(3 * v for v in n)) for p, n in contacts]
            shuffled = list(contacts)
            rng.shuffle(shuffled)
            for other in (scaled, shuffled):
                rep2 = analyze(other)
                self.assertEqual(rep.rank, rep2.rank)
                self.assertEqual(rep.form_closure, rep2.form_closure)
                self.assertEqual(rep.detach_twist is None, rep2.detach_twist is None)

    def test_cross_product_rows(self):
        p, n = (1, 2, 0), (0, 0, 1)
        self.assertEqual(cross(p, n), (2, -1, 0))
        self.assertEqual(jacobian([(p, n)])[0], [0, 0, 1, 2, -1, 0])


if __name__ == "__main__":
    unittest.main()
