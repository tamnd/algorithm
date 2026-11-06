# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-algorithm/. The authors are listed in prov/44TRAH.jsonl.

import itertools
import random

import pytest

from valiant_algorithm import Valiant, bmm_rows, is_cnf, recognize, to_cnf


def grammar(text):
    prods = []
    for rule in text.split(";"):
        a, rhs = rule.split("->")
        for alt in rhs.split("|"):
            prods.append((a.strip(), tuple(x for x in alt.split() if x != "eps")))
    return prods


def spans(prods, w):
    """Oracle for any grammar: all (X, i, j) with X =>* w[i:j], by a least fixpoint
    that tries every split of every right side."""
    nts = {a for a, _ in prods}
    n, known = len(w), set()

    def fits(rhs, i, j):
        if not rhs:
            return i == j
        for cut in itertools.combinations_with_replacement(range(i, j + 1), len(rhs) - 1):
            b = (i, *cut, j)
            ok = True
            for t, x in enumerate(rhs):
                if x in nts:
                    ok = (x, b[t], b[t + 1]) in known
                else:
                    ok = b[t + 1] == b[t] + 1 and w[b[t]] == x
                if not ok:
                    break
            if ok:
                return True
        return False

    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                for j in range(i, n + 1):
                    if (a, i, j) not in known and fits(rhs, i, j):
                        known.add((a, i, j))
                        changed = True
    return known


def cyk_table(prods, w):
    """Plain CYK on a CNF grammar: all (A, i, j) with i < j and A =>* w[i:j]."""
    n = len(w)
    t = {}
    for i, c in enumerate(w):
        t[(i, i + 1)] = {a for a, r in prods if r == (c,)}
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            cell = set()
            for k in range(i + 1, j):
                for a, r in prods:
                    if len(r) == 2 and r[0] in t[(i, k)] and r[1] in t[(k, j)]:
                        cell.add(a)
            t[(i, j)] = cell
    return {(a, i, j) for (i, j), cell in t.items() for a in cell}


def random_cnf(rng):
    names = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = set()
    for _ in range(rng.randint(2, 9)):
        a = rng.choice(names)
        if rng.random() < 0.6:
            prods.add((a, (rng.choice(names), rng.choice(names))))
        else:
            prods.add((a, (rng.choice("ab"),)))
    # a name with no production would be a terminal; drop the binary rules that use one
    while True:
        lhs = {a for a, _ in prods}
        keep = {(a, r) for a, r in prods if len(r) == 1 or set(r) <= lhs}
        if keep == prods:
            return sorted(prods)
        prods = keep


def random_grammar(rng):
    """Any shape: empty right sides, unit productions, left recursion, long right sides."""
    names = ["S", "A", "B", "C"][: rng.randint(1, 4)]
    prods = set()
    for _ in range(rng.randint(2, 7)):
        a = rng.choice(names)
        k = rng.choice([0, 1, 1, 2, 2, 3])
        prods.add((a, tuple(rng.choice(names + ["a", "b"]) for _ in range(k))))
    prods.add(("S", tuple(rng.choice(names + ["a", "b"]) for _ in range(rng.randint(1, 3)))))
    return sorted(prods)


def words(maxn):
    for n in range(maxn + 1):
        for t in itertools.product("ab", repeat=n):
            yield "".join(t)


HMU = grammar("S -> A B | B C ; A -> B A | a ; B -> C C | b ; C -> A B | a")


def test_hmu_example_table():
    v = Valiant(HMU, "S", "baaba")
    assert v.N == 8
    assert v.accepts()
    # the CYK table of the page, row by row (0-based spans)
    expect = {
        (0, 1): "B", (1, 2): "AC", (2, 3): "AC", (3, 4): "B", (4, 5): "AC",
        (0, 2): "AS", (1, 3): "B", (2, 4): "CS", (3, 5): "AS",
        (0, 3): "", (1, 4): "B", (2, 5): "B",
        (0, 4): "", (1, 5): "ACS",
        (0, 5): "ACS",
    }
    got = v.table()
    for (i, j), cell in expect.items():
        assert {a for a in "ABCS" if (a, i, j) in got} == set(cell)
    assert got == cyk_table(HMU, "baaba")
    # 28 cells above the diagonal of the 8 x 8 matrix, 7 of them terminal cells
    assert v.cells == 21
    assert v.products == {1: 24, 2: 4}


def test_cell_order_trace():
    """The order in which line L9 finishes the cells of the 8 x 8 example."""
    order = []

    class Traced(Valiant):
        def complete(self, l, m, l2, m2):
            if m - l == 1 and l2 > l + 1:
                order.append((l, l2))
            super().complete(l, m, l2, m2)

    Traced(HMU, "S", "baaba")
    assert order == [(0, 2), (1, 3), (0, 3), (4, 6), (5, 7), (4, 7), (2, 4), (3, 5), (2, 5),
                     (1, 4), (0, 4), (1, 5), (0, 5), (3, 6), (2, 6), (3, 7), (2, 7),
                     (1, 6), (0, 6), (1, 7), (0, 7)]


def test_products_for_cell_0_5():
    log = []

    class Logged(Valiant):
        def _add_product(self, r0, r1, k0, k1, c0, c1):
            if r0 <= 0 < r1 and c0 <= 5 < c1:
                log.append((r0, r1, k0, k1, c0, c1))
            super()._add_product(r0, r1, k0, k1, c0, c1)

    v = Logged(HMU, "S", "baaba")
    # k = 2, 3 by one 2 x 2 block product, then k = 1 and k = 4 by 1 x 1 products
    assert log == [(0, 2, 2, 4, 4, 6), (0, 1, 1, 2, 5, 6), (0, 1, 4, 5, 5, 6)]
    pairs = {bc for bc in v.pairs if v.prod[bc][0] >> 5 & 1}
    # the pairs that are right sides of productions: (B, A) and (B, C) from k = 1, (A, B) from k = 2
    assert pairs == {("B", "A"), ("B", "C"), ("A", "B")}
    assert v.calls == 15


def test_invariant_every_split_is_known_when_a_cell_is_finished():
    rng = random.Random(7)
    checked = 0

    class Checked(Valiant):
        def complete(self, l, m, l2, m2):
            if m - l == 1 and l2 > l + 1:
                i, j = l, l2
                need = set()
                for k in range(i + 1, j):
                    for b, c in self.pairs:
                        if self.rows[b][i] >> k & 1 and self.rows[c][k] >> j & 1:
                            need.add((b, c))
                have = {bc for bc in self.pairs if self.prod[bc][i] >> j & 1}
                assert have == need
                nonlocal checked
                checked += 1
            super().complete(l, m, l2, m2)

    for _ in range(60):
        g = random_cnf(rng)
        w = "".join(rng.choice("ab") for _ in range(rng.randint(2, 20)))
        Checked(g, "S", w)
    assert checked > 3000


def test_random_cnf_tables_against_cyk_and_fixpoint():
    rng = random.Random(2024)
    compared, accepted = 0, 0
    for _ in range(400):
        g = random_cnf(rng)
        w = "".join(rng.choice("ab") for _ in range(rng.randint(0, 12)))
        v = Valiant(g, "S", w)
        got = v.table()
        assert got == cyk_table(g, w)
        assert got == {(a, i, j) for a, i, j in spans(g, w) if i < j}
        compared += 1
        accepted += v.accepts()
    assert compared >= 400 and accepted >= 50


def test_random_general_grammars_through_cnf():
    """Empty and unit productions, left recursion, ambiguity and the empty input,
    against the fixpoint oracle on the original grammar."""
    rng = random.Random(99)
    compared, accepted, empty_accepted = 0, 0, 0
    for _ in range(250):
        g = random_grammar(rng)
        cnf, s0 = to_cnf(g, "S")
        assert is_cnf(cnf, s0)
        for w in words(5):
            want = ("S", 0, len(w)) in spans(g, w)
            assert recognize(cnf, s0, w) == want, (g, w)
            compared += 1
            accepted += want
            empty_accepted += want and w == ""
    assert compared >= 15000
    assert accepted >= 500 and empty_accepted >= 10


def test_named_grammars():
    cases = [
        ("E -> E + E | E * E | ( E ) | x", "E", ["x", "x+x*x", "(x+x)*x", "((x))"], ["", "x+", "()", "x x"]),
        ("S -> S S | ( S ) | eps", "S", ["", "()", "(()())", "()()(())"], ["(", ")(", "(()"]),
        ("S -> A ; A -> B ; B -> S | a", "S", ["a"], ["", "aa"]),
        ("S -> a S b | eps", "S", ["", "ab", "aaabbb"], ["a", "ba", "aab"]),
        ("S -> S a | a", "S", ["a", "aaaa"], ["", "b"]),
    ]
    for text, start, yes, no in cases:
        g = grammar(text)
        cnf, s0 = to_cnf(g, start)
        for w in yes:
            assert recognize(cnf, s0, list(w)), (text, w)
        for w in no:
            assert not recognize(cnf, s0, list(w)), (text, w)


def test_pluggable_multiplication():
    calls = []

    def cell_by_cell(x, y):
        calls.append((len(x), len(y)))
        out = []
        for row in x:
            acc = 0
            for t in range(len(y)):
                if row >> t & 1:
                    acc |= y[t]
            out.append(acc)
        return out

    rng = random.Random(5)
    for _ in range(80):
        g = random_cnf(rng)
        w = "".join(rng.choice("ab") for _ in range(rng.randint(0, 15)))
        v1 = Valiant(g, "S", w)
        v2 = Valiant(g, "S", w, bmm=cell_by_cell)
        assert v1.table() == v2.table()
        assert v1.calls == v2.calls
    assert calls and all(r == k for r, k in calls)
    assert bmm_rows([0b011, 0b100], [0b01, 0b10, 0b11]) == [0b11, 0b11]


def test_product_counts_follow_the_recurrence():
    def expected(size):
        # products of each block size made by COMPUTE(0, size)
        def comp(s):
            out = {}
            if s >= 2:
                for _ in range(4):
                    out[s // 2] = out.get(s // 2, 0) + 1
                for _ in range(4):
                    for t, c in comp(s // 2).items():
                        out[t] = out.get(t, 0) + c
            return out

        def compute(s):
            out = {}
            if s >= 2:
                for part in (compute(s // 2), compute(s // 2), comp(s // 2)):
                    for t, c in part.items():
                        out[t] = out.get(t, 0) + c
            return out

        return compute(size)

    for n in (1, 3, 7, 15, 31, 40):
        v = Valiant(HMU, "S", "ab" * (n // 2) + "a" * (n % 2))
        assert v.products == expected(v.N)
        for t, c in v.products.items():
            # the closed form of the page: (N / t) (N / (2 t) - 1) products of size t
            assert c == (v.N // t) * (v.N // (2 * t) - 1)


def test_rejects_non_cnf():
    with pytest.raises(ValueError):
        Valiant(grammar("S -> a S b | eps"), "S", "ab")
    with pytest.raises(ValueError):
        Valiant(grammar("S -> A ; A -> a"), "S", "a")
    with pytest.raises(ValueError):
        Valiant(grammar("S -> S S | eps"), "S", "")


def test_empty_input():
    assert recognize([("S", ()), ("S", ("a",))], "S", "")
    assert not recognize([("S", ("a",))], "S", "")
    v = Valiant([("S", ("a",))], "S", "")
    assert v.N == 1 and v.table() == set()


def test_long_input():
    # Dyck words in CNF: S -> S S | L R | L X, X -> S R
    g = grammar("S -> S S | L R | L X ; X -> S R ; L -> ( ; R -> )")
    rng = random.Random(11)
    w = []
    depth = 0
    while len(w) < 250:
        if depth and (rng.random() < 0.5 or depth > 40):
            w.append(")")
            depth -= 1
        else:
            w.append("(")
            depth += 1
    w += [")"] * depth
    v = Valiant(g, "S", w)
    assert v.accepts()
    assert v.N == 512
    assert v.table() == cyk_table(g, w)
    assert not recognize(g, "S", w[:-1])
    deep = ["("] * 150 + [")"] * 150
    assert recognize(g, "S", deep)
