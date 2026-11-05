# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/state-elimination/. The authors are listed in prov/GVY1JV.jsonl.

import itertools
import random

from state_elimination import EMPTY, EPS, eliminate, size, to_string

# Brute-force references, for short words only.


def nfa_accepts(n, start, accepting, moves, w):
    """Direct simulation of the NFA with ε-closure."""

    def close(S):
        S = set(S)
        todo = list(S)
        while todo:
            p = todo.pop()
            for x, a, q in moves:
                if x == p and a == "" and q not in S:
                    S.add(q)
                    todo.append(q)
        return S

    cur = close({start})
    for c in w:
        cur = close({q for p, a, q in moves if p in cur and a == c})
    return bool(cur & set(accepting))


def spans(r, w):
    """The set of pairs (i, j) such that w[i:j] is in L(r), bottom-up."""
    memo = {}
    order, stack, seen = [], [(r, False)], set()
    while stack:  # iterative post-order over the shared nodes
        x, done = stack.pop()
        if done:
            order.append(x)
            continue
        if id(x) in seen:
            continue
        seen.add(id(x))
        stack.append((x, True))
        stack.extend((y, False) for y in x[1:] if isinstance(y, tuple))
    n = len(w)
    for x in order:
        k = x[0]
        if k == "empty":
            S = set()
        elif k == "eps":
            S = {(i, i) for i in range(n + 1)}
        elif k == "sym":
            S = {(i, i + 1) for i in range(n) if w[i] == x[1]}
        elif k == "alt":
            S = memo[id(x[1])] | memo[id(x[2])]
        elif k == "cat":
            A, B = memo[id(x[1])], memo[id(x[2])]
            S = {(i, l) for i, j in A for j2, l in B if j == j2}
        else:
            A = memo[id(x[1])]
            S = {(i, i) for i in range(n + 1)}
            while True:
                T = S | {(i, l) for i, j in S for j2, l in A if j == j2}
                if T == S:
                    break
                S = T
        memo[id(x)] = S
    return memo[id(r)]


def re_accepts(r, w):
    return (0, len(w)) in spans(r, w)


def parse(p):
    """A small recursive parser for short test patterns (same syntax)."""
    i = 0

    def alt():
        nonlocal i
        r = cat()
        while i < len(p) and p[i] == "|":
            i += 1
            r = ("alt", r, cat())
        return r

    def cat():
        r = None
        while i < len(p) and p[i] not in "|)":
            x = atom()
            r = x if r is None else ("cat", r, x)
        return EPS if r is None else r

    def atom():
        nonlocal i
        c = p[i]
        i += 1
        if c == "(":
            x = alt()
            i += 1
        elif c == "ε":
            x = EPS
        elif c == "∅":
            x = EMPTY
        else:
            x = ("sym", c)
        while i < len(p) and p[i] == "*":
            i += 1
            x = ("star", x)
        return x

    return alt()


def words(alpha, L):
    for k in range(L + 1):
        for t in itertools.product(alpha, repeat=k):
            yield "".join(t)


def random_nfa(rng, alpha):
    n = rng.randint(1, 5)
    moves = []
    for _ in range(rng.randint(0, 3 * n)):
        a = rng.choice(list(alpha) + [""])
        moves.append((rng.randrange(n), a, rng.randrange(n)))
    acc = [q for q in range(n) if rng.random() < 0.4]
    return n, rng.randrange(n), acc, moves


def thompson_tree(r, moves, counter):
    """A Thompson NFA for a test expression (recursive; tests use small trees)."""
    s, f = counter[0], counter[0] + 1
    counter[0] += 2
    k = r[0]
    if k == "sym":
        moves.append((s, r[1], f))
    elif k == "eps":
        moves.append((s, "", f))
    elif k in ("alt", "cat"):
        s1, f1 = thompson_tree(r[1], moves, counter)
        s2, f2 = thompson_tree(r[2], moves, counter)
        if k == "alt":
            moves += [(s, "", s1), (s, "", s2), (f1, "", f), (f2, "", f)]
        else:
            moves += [(s, "", s1), (f1, "", s2), (f2, "", f)]
    elif k == "star":
        s1, f1 = thompson_tree(r[1], moves, counter)
        moves += [(s, "", s1), (s, "", f), (f1, "", s1), (f1, "", f)]
    return s, f


def rand_re(rng, alpha, d):
    if d == 0 or rng.random() < 0.25:
        return rng.choice([("sym", a) for a in alpha] + [EPS, EMPTY])
    k = rng.choice(["alt", "cat", "star", "star"])
    if k == "star":
        return ("star", rand_re(rng, alpha, d - 1))
    return (k, rand_re(rng, alpha, d - 1), rand_re(rng, alpha, d - 1))


def test_divisible_by_three():
    mv = [(r, str(b), (2 * r + b) % 3) for r in range(3) for b in (0, 1)]
    e = eliminate(3, 0, [0], mv, [2, 1, 0])
    assert to_string(e) == "(0|1(01*0)*1)*"
    assert size(e) == 14
    assert to_string(eliminate(3, 0, [0], mv, [1, 2, 0])) == "(0|11|10(1|00)*01)*"
    for order in itertools.permutations(range(3)):
        e = eliminate(3, 0, [0], mv, list(order))
        for w in words("01", 9):
            assert re_accepts(e, w) == (w != "" and int(w, 2) % 3 == 0 or w == "")


def test_edges():
    assert eliminate(1, 0, [], []) is EMPTY
    assert eliminate(1, 0, [0], []) is EPS
    assert to_string(eliminate(1, 0, [0], [(0, "a", 0)])) == "a*"
    assert to_string(eliminate(2, 0, [1], [(0, "a", 1), (1, "", 0)])) == "aa*"
    assert to_string(eliminate(2, 0, [1], [(0, "", 1), (1, "", 0)])) == "ε"
    assert to_string(eliminate(2, 0, [0], [(1, "a", 1)])) == "ε"  # state 1 unreachable


def test_random_nfas():
    rng = random.Random(7)
    for alpha in ("ab", "abc"):
        L = 6 if alpha == "ab" else 4
        for _ in range(600):
            n, q0, acc, mv = random_nfa(rng, alpha)
            order = list(range(n))
            rng.shuffle(order)
            e = eliminate(n, q0, acc, mv, order)
            # the printed form parses back to the same language
            e2 = parse(to_string(e))
            for w in words(alpha, L):
                want = nfa_accepts(n, q0, acc, mv, w)
                assert re_accepts(e, w) == want
                assert re_accepts(e2, w) == want


def test_round_trip_through_thompson():
    rng = random.Random(11)
    for alpha in ("ab", "abc"):
        L = 6 if alpha == "ab" else 4
        for _ in range(400):
            r = rand_re(rng, alpha, 4)
            mv, counter = [], [0]
            s, f = thompson_tree(r, mv, counter)
            e = eliminate(counter[0], s, [f], mv)
            for w in words(alpha, L):
                assert re_accepts(e, w) == re_accepts(r, w)


def test_nested_stars_and_constants():
    for p in ["∅", "ε", "∅*", "(a*)*", "((a|ε)*b*)*", "(a∅)*b", "(ε|a)(ε|b)"]:
        r = parse(p)
        mv, counter = [], [0]
        s, f = thompson_tree(r, mv, counter)
        e = eliminate(counter[0], s, [f], mv)
        for w in words("ab", 6):
            assert re_accepts(e, w) == re_accepts(r, w)


def test_long_chain_no_recursion():
    n = 5000
    mv = [(i, "ab"[i % 2], i + 1) for i in range(n - 1)] + [(n - 1, "a", 0)]
    e = eliminate(n, 0, [0], mv)
    assert size(e) > n
    u = "".join("ab"[i % 2] for i in range(n - 1))
    assert to_string(e) == "ε|" + u + "(a" + u + ")*a"
