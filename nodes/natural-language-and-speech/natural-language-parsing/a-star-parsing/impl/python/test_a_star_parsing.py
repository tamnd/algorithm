# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/a-star-parsing/. The authors are listed in prov/MZTBB1.jsonl.

import math
import random

from a_star_parsing import a_star_parse, null_estimate, sx_estimate, tree_log_score
from nlslog import NEG_INF

MS = [
    ("S", ("NP", "VP"), 1.0),
    ("PP", ("P", "NP"), 1.0),
    ("VP", ("V", "NP"), 0.7),
    ("VP", ("VP", "PP"), 0.3),
    ("NP", ("NP", "PP"), 0.4),
    ("P", ("with",), 1.0),
    ("V", ("saw",), 1.0),
    ("NP", ("astronomers",), 0.1),
    ("NP", ("ears",), 0.18),
    ("NP", ("saw",), 0.04),
    ("NP", ("stars",), 0.18),
    ("NP", ("telescopes",), 0.1),
]
SENT = "astronomers saw stars with ears".split()


def leaves(t):
    out, stack = [], [t]
    while stack:
        u = stack.pop()
        if isinstance(u, str):
            out.append(u)
        else:
            stack.extend(reversed(u[1]))
    return out


def binary_trees(i, j):
    """All binary bracketings of the span (i, j), as nested pairs; a leaf is its index."""
    if j - i == 1:
        return [i]
    out = []
    for k in range(i + 1, j):
        for left in binary_trees(i, k):
            for right in binary_trees(k, j):
                out.append((left, right))
    return out


def brute_force(rules, start, w):
    """The best log score over all binary trees of w: enumerate every bracketing
    and find its best labeling by a max over the labels at each node."""
    lex, binr = {}, []
    for a, rhs, q in rules:
        if q <= 0:
            continue
        if len(rhs) == 1:
            lex.setdefault(rhs[0], []).append((a, math.log(q)))
        else:
            binr.append((a, rhs[0], rhs[1], math.log(q)))

    def label(shape):
        if isinstance(shape, int):
            d = {}
            for a, lq in lex.get(w[shape], ()):
                d[a] = max(d.get(a, NEG_INF), lq)
            return d
        left, right = label(shape[0]), label(shape[1])
        d = {}
        for a, b, c, lq in binr:
            if b in left and c in right:
                d[a] = max(d.get(a, NEG_INF), lq + left[b] + right[c])
        return d

    best, count = NEG_INF, 0
    for shape in binary_trees(0, len(w)):
        count += 1
        best = max(best, label(shape).get(start, NEG_INF))
    return best, count


def cky(rules, start, w):
    """Exhaustive Viterbi CKY over fencepost spans, in log space."""
    n = len(w)
    lex, binr = {}, []
    for a, rhs, q in rules:
        if q <= 0:
            continue
        if len(rhs) == 1:
            lex.setdefault(rhs[0], []).append((a, math.log(q)))
        else:
            binr.append((a, rhs[0], rhs[1], math.log(q)))
    ch = {}
    for i in range(n):
        for a, lq in lex.get(w[i], ()):
            ch[(a, i, i + 1)] = max(ch.get((a, i, i + 1), NEG_INF), lq)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            for k in range(i + 1, j):
                for a, b, c, lq in binr:
                    if (b, i, k) in ch and (c, k, j) in ch:
                        s = lq + ch[(b, i, k)] + ch[(c, k, j)]
                        if s > ch.get((a, i, j), NEG_INF):
                            ch[(a, i, j)] = s
    return ch.get((start, 0, n), NEG_INF), ch


def test_example() -> None:
    s, t, pops_null = a_star_parse(MS, "S", SENT)
    assert math.isclose(s, math.log(0.0009072), rel_tol=1e-12)
    pp = ("PP", (("P", ("with",)), ("NP", ("ears",))))
    obj = ("NP", (("NP", ("stars",)), pp))
    vp = ("VP", (("V", ("saw",)), obj))
    assert t == ("S", (("NP", ("astronomers",)), vp))
    s2, t2, pops_sx = a_star_parse(MS, "S", SENT, sx_estimate(MS, "S", len(SENT)))
    assert t2 == t and math.isclose(s2, s, rel_tol=1e-12)
    assert pops_sx < pops_null
    assert (pops_null, pops_sx) == (12, 10)


def test_inadmissible_estimate_fails() -> None:
    # An estimate that underestimates the outside score of (NP, 2, 5) is not
    # admissible. The parser then pops the goal by the other reading first.
    def bad(x, i, j):
        return -100.0 if (x, i, j) == ("NP", 2, 5) else 0.0

    s, t, _ = a_star_parse(MS, "S", SENT, bad)
    assert math.isclose(s, math.log(0.0006804), rel_tol=1e-12)
    assert t[1][1][1][0][0] == "VP"  # VP -> VP PP: the PP attaches to the verb


def test_no_parse_and_edges() -> None:
    assert a_star_parse(MS, "S", [])[:2] == (NEG_INF, None)
    assert a_star_parse(MS, "S", ["stars", "with"])[:2] == (NEG_INF, None)
    assert a_star_parse(MS, "S", ["unknown"])[:2] == (NEG_INF, None)
    s, t, _ = a_star_parse(MS, "NP", ["stars"])
    assert math.isclose(s, math.log(0.18)) and t == ("NP", ("stars",))
    for bad in ([("S", ("A", "B", "C"), 1.0), ("A", ("a",), 1.0)],
                [("S", ("x",), -0.5)]):
        try:
            a_star_parse(bad, "S", ["a"])
        except ValueError:
            continue
        raise AssertionError("bad grammar accepted")


def test_catalan_counts() -> None:
    # The grammar X -> X X, X -> a has one tree per binary bracketing.
    g = [("X", ("X", "X"), 0.5), ("X", ("a",), 0.5)]
    counts = [brute_force(g, "X", ["a"] * n)[1] for n in range(1, 8)]
    assert counts == [1, 1, 2, 5, 14, 42, 132]
    for n in range(1, 8):
        s, t, _ = a_star_parse(g, "X", ["a"] * n, sx_estimate(g, "X", n))
        assert math.isclose(s, (2 * n - 1) * math.log(0.5), rel_tol=1e-12)
        assert leaves(t) == ["a"] * n


def random_grammar(rng):
    nts = ["S", "A", "B"][: rng.randint(1, 3)]
    terms = ["x", "y", "z"]
    rules = []
    for a in nts:
        for b in nts:
            for c in nts:
                if rng.random() < 0.6:
                    rules.append((a, (b, c), rng.choice([0.1, 0.2, 0.3, 0.5, 0.9])))
        for t in terms:
            if rng.random() < 0.6:
                rules.append((a, (t,), rng.choice([0.05, 0.2, 0.4, 0.7])))
    return rules, terms


def test_random_against_brute_force_and_cky() -> None:
    rng = random.Random(2003)
    for trial in range(600):
        rules, terms = random_grammar(rng)
        n = rng.randint(1, 7 if trial % 10 == 0 else 5)
        w = [rng.choice(terms) for _ in range(n)]
        ref, ch = cky(rules, "S", w)
        if n <= 5 or trial % 30 == 0:
            bf, _ = brute_force(rules, "S", w)
            assert bf == ref or math.isclose(bf, ref, rel_tol=1e-12)
        s0, t0, p0 = a_star_parse(rules, "S", w)
        s1, t1, p1 = a_star_parse(rules, "S", w, sx_estimate(rules, "S", n))
        for s, t in ((s0, t0), (s1, t1)):
            if ref == NEG_INF:
                assert s == NEG_INF and t is None
            else:
                assert math.isclose(s, ref, rel_tol=1e-9, abs_tol=1e-12)
                assert leaves(t) == w and t[0] == "S"
                assert math.isclose(tree_log_score(rules, t), ref, rel_tol=1e-9, abs_tol=1e-12)


def test_sx_is_admissible() -> None:
    # The SX estimate is at least the true Viterbi outside score of every item.
    rng = random.Random(11)
    for _ in range(150):
        rules, terms = random_grammar(rng)
        n = rng.randint(1, 5)
        w = [rng.choice(terms) for _ in range(n)]
        _, inside = cky(rules, "S", w)
        est = sx_estimate(rules, "S", n)
        # Viterbi outside scores, top down
        out = {("S", 0, n): 0.0}
        binr = [(a, r[0], r[1], math.log(q)) for a, r, q in rules if len(r) == 2]
        for length in range(n, 1, -1):
            for i in range(n - length + 1):
                j = i + length
                for a, b, c, lq in binr:
                    if (a, i, j) not in out:
                        continue
                    for k in range(i + 1, j):
                        if (b, i, k) in inside and (c, k, j) in inside:
                            sb = out[(a, i, j)] + lq + inside[(c, k, j)]
                            sc = out[(a, i, j)] + lq + inside[(b, i, k)]
                            out[(b, i, k)] = max(out.get((b, i, k), NEG_INF), sb)
                            out[(c, k, j)] = max(out.get((c, k, j), NEG_INF), sc)
        for (x, i, j), o in out.items():
            assert est(x, i, j) >= o - 1e-9
        assert null_estimate("S", 0, n) == 0.0


def test_log_space_underflow() -> None:
    # 12 words with lexical probability 1e-30: the plain product underflows.
    n = 12
    g = [("X", ("X", "X"), 1.0), ("X", ("a",), 1e-30)]
    plain = 1.0
    for _ in range(n):
        plain *= 1e-30
    assert plain == 0.0
    s, t, _ = a_star_parse(g, "X", ["a"] * n, sx_estimate(g, "X", n))
    assert math.isclose(s, n * math.log(1e-30), rel_tol=1e-12)
    assert leaves(t) == ["a"] * n


def test_long_input_iterative() -> None:
    # A right-branching grammar on 300 words: the tree is built without recursion.
    n = 300
    g = [("X", ("A", "X"), 0.9), ("X", ("b",), 1.0), ("A", ("a",), 1.0)]
    w = ["a"] * (n - 1) + ["b"]
    s, t, pops = a_star_parse(g, "X", w)
    assert math.isclose(s, (n - 1) * math.log(0.9), rel_tol=1e-12)
    assert leaves(t) == w
