# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feautrier-array-dataflow/. The authors are listed in prov/61C0MP.jsonl.
"""Tests: the symbolic source of every read must match a brute-force search
for the last writer, at every instance, for several values of N."""

import random
import unittest

from feautrier_array_dataflow import (
    F, Program, Stmt, brute_sources, diagonal, eval_quast, even_writes, lexmax,
    matvec, source, form,
)


def check(test, prog, ns, box=None):
    """Compare the quast of every read with the brute-force last writer."""
    quasts = {}
    for T in prog.stmts:
        for r, ref in enumerate(T.reads):
            quasts[(T.name, r)] = source(prog, T, ref)
    count = 0
    for n in ns:
        env = {"N": n}
        brute = brute_sources(prog, env, box if box is not None else 2 * n + 2)
        for (name, r, point), want in brute.items():
            e = dict(env)
            e.update({f"t{k}": x for k, x in enumerate(point)})
            got = eval_quast(quasts[(name, r)], e)
            test.assertEqual(got, want, f"{name} read {r} at {point}, N={n}")
            count += 1
    return quasts, count


class Examples(unittest.TestCase):
    def test_matvec(self):
        quasts, count = check(self, matvec(), range(1, 6))
        self.assertGreater(count, 50)
        # the source of y[i] in S2(i, j) never depends on N
        self.assertNotIn("'N'", repr(quasts[("S2", 0)]))

    def test_even_writes_needs_a_new_parameter(self):
        quasts, _ = check(self, even_writes(), range(0, 6))
        self.assertIn("div", repr(quasts[("S2", 0)]))

    def test_diagonal(self):
        check(self, diagonal(), range(0, 5))

    def test_lexmax_matches_enumeration(self):
        # lexmax of (s0, s1) with 0 <= s0, s1 <= N, 3*s0 + 2*s1 <= t
        cons = [F(s0=1), F(s1=1), F(N=1, s0=-1), F(N=1, s1=-1), F(t=1, s0=-3, s1=-2)]
        quast = lexmax(["s0", "s1"], cons, [F(N=1), F(t=1)])
        for n in range(0, 5):
            for t in range(0, 20):
                pts = [(a, b) for a in range(n + 1) for b in range(n + 1) if 3 * a + 2 * b <= t]
                got = eval_quast(_tag(quast), {"N": n, "t": t})
                self.assertEqual(got, ("x", max(pts)))


def _tag(t):
    if t[0] == "leaf":
        return t if t[1] is None else ("leaf", ("x", t[1]))
    if t[0] == "if":
        return ("if", t[1], _tag(t[2]), _tag(t[3]))
    return ("div", t[1], t[2], t[3], _tag(t[4]))


def random_program(rng):
    """One or two outer i loops; each holds statements at depth 1 or inner
    j loops. All statements touch one array A with affine subscripts."""
    stmts, k = [], 0
    for b0 in range(rng.randint(1, 2)):
        for b1 in range(rng.randint(1, 2)):
            dom_i = [F(i=1), F(N=1, i=-1)]
            if rng.random() < 0.5:
                iters, betas, dom = ["i"], [b0, b1], dom_i
            else:
                lo, hi = rng.choice([(F(j=1), F(N=1, j=-1)), (F(j=1), F(i=1, j=-1)),
                                     (F(j=1, i=-1), F(N=1, j=-1))])
                iters, betas, dom = ["i", "j"], [b0, b1, 0], dom_i + [lo, hi]

            def sub():
                d = {"i": rng.choice([0, 1, 1, 2, -1])}
                if "j" in iters:
                    d["j"] = rng.choice([0, 1, 1, 2, -1])
                if rng.random() < 0.2:
                    d["N"] = 1
                return form(d, rng.choice([-1, 0, 0, 1]))
            reads = [("A", [sub()]) for _ in range(rng.randint(1, 2))]
            stmts.append(Stmt(f"S{k}", iters, betas, dom, ("A", [sub()]), reads))
            k += 1
    return Program(["N"], [F(N=1)], stmts)


class RandomPrograms(unittest.TestCase):
    def test_random(self):
        rng = random.Random(1988)
        total = 0
        for _ in range(14):
            prog = random_program(rng)
            _, count = check(self, prog, range(0, 4))
            total += count
        self.assertGreater(total, 500)


if __name__ == "__main__":
    unittest.main()
