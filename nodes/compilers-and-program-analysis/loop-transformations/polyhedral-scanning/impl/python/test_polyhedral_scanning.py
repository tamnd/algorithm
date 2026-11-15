# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyhedral-scanning/. The authors are listed in prov/19214B.jsonl.
"""Tests: for small parameter values, the generated loops must visit every
integer point of every statement domain exactly once, in lexicographic order
of (schedule, iteration vector, statement). Running the statements in that
order on small arrays must give the same memory as the original program
whenever a brute-force check finds the schedule legal."""

import random
import unittest

from polyhedral_scanning import (
    Scop, clean, eliminate, execute, feasible, implied, instance_of, scan, separate,
    show, skewed_stencil, triangle, two_ranges,
)


def value(aff, env):
    return sum(c * (env[v] if v else 1) for v, c in aff.items())


def brute(scop, env, box):
    """All (point, s) with the iteration vector in the box and the domain."""
    out = []
    for s, S in enumerate(scop.stmts):
        d = len(S["iters"])

        def rec(prefix):
            if len(prefix) == d:
                e = dict(env)
                e.update(zip(S["iters"], prefix))
                if all(value(c, e) >= 0 for c in S["domain"]):
                    sched = [value(th, e) for th in S["schedule"]]
                    sched += [0] * (scop.m - len(sched))
                    out.append((tuple(sched) + tuple(prefix) + (0,) * (scop.d - d), s))
                return
            for x in range(-box, box + 1):
                rec(prefix + [x])
        rec([])
    return sorted(out)


def scanned(scop, ast, env):
    seen = []
    execute(ast, scop, env, lambda s, p: seen.append((p, s)))
    return seen


def check_scan(test, scop, ns):
    ast = scan(scop)
    for n in ns:
        env = {"N": n}
        got, want = scanned(scop, ast, env), brute(scop, env, 2 * n + 4)
        # equal to the sorted list of all points: each point once, in order
        test.assertEqual(got, want, f"N={n}\n" + "\n".join(show(ast, scop)))
    return ast


class Pieces(unittest.TestCase):
    def test_simplex_tests(self):
        # x >= 0, y >= 0, x + y <= 2 in two variables
        rows = [[1, 0, 0], [0, 1, 0], [-1, -1, 2]]
        self.assertTrue(feasible(rows, 2))
        self.assertFalse(feasible(rows + [[1, 1, -3]], 2))
        self.assertTrue(implied(rows, [-1, 0, 2], 2))
        self.assertFalse(implied(rows, [-1, 0, 1], 2))

    def test_fourier_motzkin(self):
        # 0 <= j <= i <= N gives 0 <= i <= N after eliminating j
        rows = [[0, 1, 0, 0], [1, -1, 0, 0], [-1, 0, 1, 0]]
        self.assertEqual(sorted(eliminate(rows, 1)), sorted([[1, 0, 0, 0], [-1, 0, 1, 0]]))
        # i = 2 j with 0 <= i <= 3: the shadow is the rational one, odd i included
        rows = [[-1, 2, 0], [1, -2, 0], [1, 0, 0], [-1, 0, 3]]
        self.assertEqual(sorted(eliminate(rows, 1)), sorted([[1, 0, 0], [-1, 0, 3]]))
        # 2 i + 1 >= 0 has the same integer points as i >= 0
        self.assertEqual(clean([[2, 1]]), [[1, 0]])

    def test_separation_is_disjoint_and_covers(self):
        # [0, 5] and [3, 8] on one line
        a, b = [[1, 0], [-1, 5]], [[1, -3], [-1, 8]]
        pieces = separate([(a, frozenset("a")), (b, frozenset("b"))], 1)
        for x in range(-2, 11):
            hit = [lab for rows, lab in pieces if all(r[0] * x + r[1] >= 0 for r in rows)]
            want = frozenset(c for c, (lo, hi) in [("a", (0, 5)), ("b", (3, 8))] if lo <= x <= hi)
            self.assertEqual(hit, [want] if want else [], x)


class Examples(unittest.TestCase):
    def test_triangle(self):
        check_scan(self, triangle("ij"), range(0, 5))
        ast = check_scan(self, triangle("ji"), range(0, 5))
        self.assertEqual(show(ast, triangle("ji"))[:2], ["for t1 = 0 to N:", "  for t2 = t1 to N:"])

    def test_two_ranges_split_in_three_loops(self):
        scop = two_ranges()
        ast = check_scan(self, scop, range(0, 6))
        self.assertEqual(len(ast), 3)
        self.assertEqual(show(ast, scop)[0], "for t1 = 0 to min(N, 1):")

    def test_skewed_stencil(self):
        check_scan(self, skewed_stencil(), range(0, 5))

    def test_guarded_union_fallback(self):
        # force the path used when the pieces cannot be sorted
        import polyhedral_scanning as ps
        saved = ps.sort_pieces
        ps.sort_pieces = lambda pieces, k, nv: None
        try:
            ast = check_scan(self, two_ranges(), range(0, 6))
            self.assertIn("union", ast[0])
            check_scan(self, random_scop(random.Random(7), False), range(0, 4))
        finally:
            ps.sort_pieces = saved

    def test_stride(self):
        # the schedule 2 i leaves holes: odd t1 values have no point
        S = {"name": "S", "iters": ["i"], "domain": [{"i": 1}, {"N": 1, "i": -1}],
             "schedule": [{"i": 2}]}
        check_scan(self, Scop(["N"], [{"N": 1}], [S]), range(0, 5))


# ------------------------------------------------------- random programs

DOMS_J = [({"j": 1}, {"N": 1, "j": -1}), ({"j": 1}, {"i": 1, "j": -1}),
          ({"j": 1, "i": -1}, {"N": 1, "j": -1})]
DOMS_I = [({"i": 1}, {"N": 1, "i": -1}), ({"i": 1, "": -1}, {"N": 1, "i": -1, "": 1}),
          ({"i": 1, "": -2}, {"N": 1, "i": -1})]
LINEAR = [[{"i": 1}, {"j": 1}], [{"j": 1}, {"i": 1}], [{"i": 1}, {"i": 1, "j": 1}],
          [{"i": 1, "j": 1}, {"i": 1}], [{"i": 1, "j": 1}, {"j": 1}]]


def random_scop(rng, original):
    """One or two outer loops with up to three statements of depth 1 or 2.
    Each statement has its original schedule vector (b0, i, b1, j, b2) and,
    unless `original`, a random schedule of the same shape. The fields
    'write', 'reads' and 'omega' are used by the tests only."""
    stmts, k = [], 0
    for b0 in range(rng.randint(1, 2)):
        lo_i, hi_i = rng.choice(DOMS_I)
        for b1 in range(rng.randint(1, 2)):
            if k == 3:
                break
            if rng.random() < 0.5:
                iters, dom = ["i"], [lo_i, hi_i]
                omega = [{"": b0}, {"i": 1}, {"": b1}, {}, {}]
                lin = [{"i": rng.choice([1, 1, 2])}, {}]
            else:
                iters, dom = ["i", "j"], [lo_i, hi_i] + list(rng.choice(DOMS_J))
                omega = [{"": b0}, {"i": 1}, {"": b1}, {"j": 1}, {}]
                lin = rng.choice(LINEAR)
            sched = omega if original else [{"": b0}, lin[0], {"": b1}, lin[1], {}]

            def sub():
                d = {"i": rng.choice([0, 1, 1, -1])}
                if "j" in iters:
                    d["j"] = rng.choice([0, 1, -1])
                return d, rng.choice([-1, 0, 0, 1])
            reads = [(rng.choice("AB"), sub()) for _ in range(rng.randint(1, 2))]
            stmts.append({"name": f"S{k}", "iters": iters, "domain": dom, "schedule": sched,
                          "omega": omega, "write": (rng.choice("AB"), sub()), "reads": reads})
            k += 1
    return Scop(["N"], [{"N": 1}], stmts)


def cell(acc, env):
    arr, (d, c) = acc
    return arr, value(d, env) + c


def instances(scop, env, box):
    """(omega vector, s, iteration vector) of every instance."""
    out = []
    for point, s in brute(scop, env, box):
        S = scop.stmts[s]
        it = instance_of(scop, s, point)
        e = dict(env)
        e.update(zip(S["iters"], it))
        out.append((tuple(value(o, e) for o in S["omega"]), s, it))
    return sorted(out)


def run(scop, env, order):
    mem = {}
    for s, it in order:
        S = scop.stmts[s]
        e = dict(env)
        e.update(zip(S["iters"], it))
        args = [mem.get(cell(r, e), 1) for r in S["reads"]]
        mem[cell(S["write"], e)] = (sum(args) * 31 + 7 * s + 1) % 1000003
    return mem


def legal(scop, env, inst, pos):
    """Every pair of instances that touch one cell, with a write, keeps its
    order. pos maps (s, it) to the place in the new order."""
    touched = {}
    for _, s, it in inst:
        S = scop.stmts[s]
        e = dict(env)
        e.update(zip(S["iters"], it))
        touched[(s, it)] = ({cell(S["write"], e)}, {cell(r, e) for r in S["reads"]})
    for x in range(len(inst)):
        a = inst[x][1:]
        wa, ra = touched[a]
        for y in range(x + 1, len(inst)):
            b = inst[y][1:]
            wb, rb = touched[b]
            if (wa & (wb | rb) or ra & wb) and pos[b] < pos[a]:
                return False
    return True


class RandomPrograms(unittest.TestCase):
    def test_original_schedule_gives_original_order(self):
        rng = random.Random(2000)
        for _ in range(12):
            scop = random_scop(rng, True)
            ast = check_scan(self, scop, range(0, 4))
            for n in range(0, 4):
                env = {"N": n}
                order = [(s, instance_of(scop, s, p)) for p, s in scanned(scop, ast, env)]
                self.assertEqual(order, [(s, it) for _, s, it in instances(scop, env, 2 * n + 4)])

    def test_random_schedules(self):
        rng = random.Random(1991)
        runs = 0
        for _ in range(16):
            scop = random_scop(rng, False)
            ast = check_scan(self, scop, range(0, 4))
            for n in range(0, 4):
                env = {"N": n}
                inst = instances(scop, env, 2 * n + 4)
                order = [(s, instance_of(scop, s, p)) for p, s in scanned(scop, ast, env)]
                pos = {x: t for t, x in enumerate(order)}
                if legal(scop, env, inst, pos):
                    want = run(scop, env, [(s, it) for _, s, it in inst])
                    self.assertEqual(run(scop, env, order), want)
                    runs += 1
        self.assertGreater(runs, 20)


if __name__ == "__main__":
    unittest.main()
