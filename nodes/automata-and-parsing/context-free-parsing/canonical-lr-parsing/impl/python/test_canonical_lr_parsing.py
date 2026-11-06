# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/canonical-lr-parsing/. The authors are listed in prov/12M6QZ.jsonl.

import itertools
import random

from canonical_lr_parsing import END, build_tables, parse


def g(text):
    """'S -> C C | d ; C -> c' into (start, productions); 'ε' is the empty string."""
    prods, start = [], None
    for part in text.split(";"):
        lhs, rhs = part.split("->")
        lhs = lhs.strip()
        start = start or lhs
        for alt in rhs.split("|"):
            prods.append((lhs, tuple(x for x in alt.split() if x != "ε")))
    return start, prods


def derives(prods, w):
    """Oracle: the least fixpoint of {(X, i, j) : X =>* w[i:j]}, exact for every grammar."""
    n = len(w)
    t = {(w[i], i, i + 1) for i in range(n)}
    changed = True
    while changed:
        changed = False
        for a, rhs in prods:
            for i in range(n + 1):
                cur = {i}
                for x in rhs:
                    cur = {j for p in cur for j in range(p, n + 1) if (x, p, j) in t}
                for j in cur:
                    if (a, i, j) not in t:
                        t.add((a, i, j))
                        changed = True
    return t


def trees(start, prods, w, cap=2):
    """Oracle: the number of parse trees of w, capped at cap (a cycle counts as cap)."""
    t = derives(prods, w)
    nts = {a for a, _ in prods}
    memo, active = {}, set()

    def cnt(x, i, j):
        if x not in nts:
            return 1 if j == i + 1 and w[i] == x else 0
        if (x, i, j) not in t:
            return 0
        if (x, i, j) in memo:
            return memo[(x, i, j)]
        if (x, i, j) in active:
            return cap
        active.add((x, i, j))
        total = sum(seq(rhs, 0, i, j) for a, rhs in prods if a == x)
        active.discard((x, i, j))
        memo[(x, i, j)] = min(total, cap)
        return memo[(x, i, j)]

    def seq(rhs, k, i, j):
        if k == len(rhs):
            return 1 if i == j else 0
        return sum(cnt(rhs[k], i, m) * seq(rhs, k + 1, m, j) for m in range(i, j + 1) if cnt(rhs[k], i, m))

    return cnt(start, 0, len(w))


def replay(start, prods, reductions, w):
    """Read the reductions backwards as a rightmost derivation and return its yield."""
    nts = {a for a, _ in prods}
    form = [start]
    for k in reversed(reductions):
        a, rhs = prods[k]
        pos = max(i for i, x in enumerate(form) if x in nts)
        assert form[pos] == a
        form[pos:pos + 1] = list(rhs)
    assert all(x not in nts for x in form)
    return "".join(form)


def words(alphabet, max_len):
    for k in range(max_len + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def check(start, prods, alphabet, max_len):
    t = build_tables(start, prods)
    for w in words(alphabet, max_len):
        member = (start, 0, len(w)) in derives(prods, w)
        if t.conflicts:
            assert trees(start, prods, w) <= 2
            continue
        assert trees(start, prods, w) <= 1, "a conflict-free table proves the grammar unambiguous"
        out = parse(t, w)
        assert (out is not None) == member, (prods, w)
        if out is not None:
            assert replay(start, prods, out, w) == w
    return t


def test_dragon_book_example():
    start, prods = g("S -> C C ; C -> c C | d")
    t = check(start, prods, "cd", 7)
    assert len(t.states) == 10 and not t.conflicts
    # I3 = GOTO(I0, c) and I6 = GOTO(I2, c) have the same core but different lookaheads
    assert t.action[(0, "c")] == ("shift", 3) and t.action[(2, "c")] == ("shift", 6)
    assert t.action[(4, "c")] == ("reduce", 3) and t.action[(4, "d")] == ("reduce", 3)
    assert (4, END) not in t.action and t.action[(7, END)] == ("reduce", 3)
    assert t.goto[(0, "S")] == 1 and t.goto[(0, "C")] == 2 and t.goto[(6, "C")] == 9
    # cdd: shift c, shift d, C -> d, C -> c C, shift d, C -> d, S -> C C
    assert parse(t, "cdd") == [2, 1, 2, 0]
    assert parse(t, "cd") is None and parse(t, "ddd") is None


def test_expressions_left_recursion():
    start, prods = g("E -> E + T | T ; T -> T * F | F ; F -> ( E ) | i")
    t = check(start, prods, "i+*()", 5)
    assert len(t.states) == 22 and not t.conflicts
    out = parse(t, "i+i*i")
    assert [prods[k] for k in out] == [
        ("F", ("i",)), ("T", ("F",)), ("E", ("T",)), ("F", ("i",)), ("T", ("F",)),
        ("F", ("i",)), ("T", ("T", "*", "F")), ("E", ("E", "+", "T"))]


def test_lr1_not_lalr1():
    start, prods = g("S -> a A d | b B d | a B e | b A e ; A -> c ; B -> c")
    t = check(start, prods, "abcde", 4)
    assert not t.conflicts
    assert parse(t, "acd") == [4, 0] and parse(t, "ace") == [5, 2]


def test_ambiguous_grammars_conflict():
    for text in ["E -> E + E | a", "S -> i S | i S e S | a", "S -> S S | ( S ) | ε", "S -> A | B ; A -> a ; B -> a"]:
        start, prods = g(text)
        assert build_tables(start, prods).conflicts


def test_epsilon_and_empty_input():
    start, prods = g("S -> ε")
    t = check(start, prods, "a", 3)
    assert parse(t, "") == [0] and parse(t, "a") is None
    start, prods = g("S -> ( S ) S | ε")
    check(start, prods, "()", 8)
    start, prods = g("S -> A B ; A -> a A | ε ; B -> b B | ε")
    check(start, prods, "ab", 6)
    start, prods = g("S -> A ; A -> B ; B -> b")  # unit productions
    t = check(start, prods, "b", 3)
    assert parse(t, "b") == [2, 1, 0]


def test_long_input_no_recursion():
    start, prods = g("E -> E + T | T ; T -> i")
    t = build_tables(start, prods)
    n = 20000
    out = parse(t, "i" + "+i" * n)
    assert out is not None and len(out) == 1 + 2 * n + 1
    start, prods = g("E -> T + E | T ; T -> i")  # right recursion: the stack grows
    t = build_tables(start, prods)
    assert len(parse(t, "i" + "+i" * n)) == 2 * (n + 1)


def test_random_against_brute_force():
    rng = random.Random(1965)
    names = ["S", "A", "B"]
    conflict_free = 0
    for _ in range(700):
        k = rng.randint(1, 3)
        prods = []
        for a in names[:k]:
            for _ in range(rng.randint(1, 3)):
                rhs = tuple(rng.choice(names[:k] + ["a", "b"]) for _ in range(rng.randint(0, 3)))
                if (a, rhs) not in prods:
                    prods.append((a, rhs))
        t = check("S", prods, "ab", 5)
        conflict_free += not t.conflicts
    assert conflict_free > 100
