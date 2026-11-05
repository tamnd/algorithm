# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pike-vm/. The authors are listed in prov/VF24KJ.jsonl.

import itertools
import random
import re

from pike_vm import compile_regex, fullmatch, pike_vm, search


EMPTY = ("empty",)
EPS = ("eps",)


def parse(text):
    """Parse | , concatenation, *, parentheses, ε and ∅ into the tuple form."""
    pos = 0

    def peek():
        return text[pos] if pos < len(text) else None

    def p_alt():
        nonlocal pos
        r = p_cat()
        while peek() == "|":
            pos += 1
            r = ("alt", r, p_cat())
        return r

    def p_cat():
        items = []
        while peek() is not None and peek() not in "|)":
            items.append(p_rep())
        if not items:
            return EPS
        r = items[0]
        for x in items[1:]:
            r = ("cat", r, x)
        return r

    def p_rep():
        nonlocal pos
        r = p_atom()
        while peek() == "*":
            pos += 1
            r = ("star", r)
        return r

    def p_atom():
        nonlocal pos
        c = peek()
        pos += 1
        if c == "(":
            r = p_alt()
            assert peek() == ")"
            pos += 1
            return r
        if c == "ε":
            return EPS
        if c == "∅":
            return EMPTY
        return ("sym", c)

    r = p_alt()
    assert pos == len(text)
    return r


def language(r, bound):
    """All strings of L(r) of length at most bound, by enumeration."""
    t = r[0]
    if t == "empty":
        return set()
    if t == "eps":
        return {""}
    if t == "sym":
        return {r[1]} if bound >= 1 else set()
    if t == "alt":
        return language(r[1], bound) | language(r[2], bound)
    if t == "cat":
        a, b = language(r[1], bound), language(r[2], bound)
        return {x + y for x in a for y in b if len(x) + len(y) <= bound}
    body = language(r[1], bound) - {""}
    result, frontier = {""}, {""}
    while frontier:
        frontier = {x + y for x in frontier for y in body if len(x) + len(y) <= bound} - result
        result |= frontier
    return result


def words(alphabet, bound):
    for k in range(bound + 1):
        for t in itertools.product(alphabet, repeat=k):
            yield "".join(t)


def random_regex(rng, alphabet, depth):
    if depth == 0 or rng.random() < 0.25:
        x = rng.random()
        if x < 0.08:
            return EMPTY
        if x < 0.18:
            return EPS
        return ("sym", rng.choice(alphabet))
    k = rng.random()
    if k < 0.35:
        return ("alt", random_regex(rng, alphabet, depth - 1), random_regex(rng, alphabet, depth - 1))
    if k < 0.75:
        return ("cat", random_regex(rng, alphabet, depth - 1), random_regex(rng, alphabet, depth - 1))
    return ("star", random_regex(rng, alphabet, depth - 1))


def decorate(rng, r):
    """Turn some nodes into groups and some stars into lazy stars."""
    t = r[0]
    if t in ("alt", "cat"):
        r = (t, decorate(rng, r[1]), decorate(rng, r[2]))
    elif t == "star":
        r = ("lazy" if rng.random() < 0.3 else "star", decorate(rng, r[1]))
    if rng.random() < 0.3:
        r = ("group", r)
    return r


def plain(r):
    """Drop groups and laziness, which do not change the language."""
    t = r[0]
    if t == "group":
        return plain(r[1])
    if t in ("star", "lazy"):
        return ("star", plain(r[1]))
    if t in ("alt", "cat"):
        return (t, plain(r[1]), plain(r[2]))
    return r


def to_python(r):
    t = r[0]
    if t == "empty":
        return "(?!)"
    if t == "eps":
        return "(?:)"
    if t == "sym":
        return r[1]
    if t == "alt":
        return "(?:" + to_python(r[1]) + "|" + to_python(r[2]) + ")"
    if t == "cat":
        return "(?:" + to_python(r[1]) + ")(?:" + to_python(r[2]) + ")"
    if t == "star":
        return "(?:" + to_python(r[1]) + ")*"
    if t == "lazy":
        return "(?:" + to_python(r[1]) + ")*?"
    return "(" + to_python(r[1]) + ")"


def nullable(r):
    return "" in language(plain(r), 0)


def has_nullable_star_body(r):
    t = r[0]
    if t in ("star", "lazy"):
        return nullable(r[1]) or has_nullable_star_body(r[1])
    if t in ("alt", "cat"):
        return has_nullable_star_body(r[1]) or has_nullable_star_body(r[2])
    if t == "group":
        return has_nullable_star_body(r[1])
    return False


def bitstate(prog, ngroups, text, full=False):
    """Backtracking in priority order that never visits a (pc, position) pair twice."""
    n = len(text)
    visited = set()
    for start in range(n + 1) if not full else [0]:
        stack = [(0, start, (-1,) * (2 * ngroups))]
        while stack:
            pc, i, caps = stack.pop()
            if (pc, i) in visited:
                continue
            visited.add((pc, i))
            ins = prog[pc]
            op = ins[0]
            if op == "char":
                if i < n and text[i] == ins[1]:
                    stack.append((pc + 1, i + 1, caps))
            elif op == "jmp":
                stack.append((ins[1], i, caps))
            elif op == "split":
                stack.append((ins[2], i, caps))
                stack.append((ins[1], i, caps))
            elif op == "save":
                k = ins[1]
                stack.append((pc + 1, i, caps[:k] + (i,) + caps[k + 1 :]))
            elif op == "match":
                if not full or i == n:
                    return [(caps[2 * k], caps[2 * k + 1]) if caps[2 * k] >= 0 and caps[2 * k + 1] >= 0 else None for k in range(ngroups)]
    return None


def python_spans(r, text):
    m = re.search(to_python(r), text)
    if m is None:
        return None
    return [m.span(k) if m.span(k) != (-1, -1) else None for k in range((m.re.groups) + 1)]


def random_text(rng, alphabet):
    return "".join(rng.choice(alphabet) for _ in range(rng.randrange(0, 9)))


def test_example_ambiguous_submatch():
    r = parse_groups("(a|ab)(c|bcd)(d*)")
    assert search(r, "abcd") == [(0, 4), (0, 1), (1, 4), (4, 4)]
    assert fullmatch(r, "abcd") == [(0, 4), (0, 1), (1, 4), (4, 4)]
    assert search(r, "xabcdd") == [(1, 6), (1, 2), (2, 5), (5, 6)]


def parse_groups(text):
    """Like parse, but ( ) makes a capture group and *? a lazy star."""
    pos = 0

    def peek():
        return text[pos] if pos < len(text) else None

    def p_alt():
        nonlocal pos
        r = p_cat()
        while peek() == "|":
            pos += 1
            r = ("alt", r, p_cat())
        return r

    def p_cat():
        items = []
        while peek() is not None and peek() not in "|)":
            items.append(p_rep())
        if not items:
            return EPS
        r = items[0]
        for x in items[1:]:
            r = ("cat", r, x)
        return r

    def p_rep():
        nonlocal pos
        r = p_atom()
        while peek() == "*":
            pos += 1
            if peek() == "?":
                pos += 1
                r = ("lazy", r)
            else:
                r = ("star", r)
        return r

    def p_atom():
        nonlocal pos
        c = peek()
        pos += 1
        if c == "(":
            r = p_alt()
            assert peek() == ")"
            pos += 1
            return ("group", r)
        if c == "ε":
            return EPS
        if c == "∅":
            return EMPTY
        return ("sym", c)

    r = p_alt()
    assert pos == len(text)
    return r


def test_greedy_lazy_and_groups():
    assert search(parse_groups("(a*)(a*)"), "aaa") == [(0, 3), (0, 3), (3, 3)]
    assert search(parse_groups("(a*?)(a*)"), "aaa") == [(0, 3), (0, 0), (0, 3)]
    assert search(parse_groups("(a*?)b"), "aab") == [(0, 3), (0, 2)]
    assert search(parse_groups("((a)|b)*"), "ab") == [(0, 2), (1, 2), (0, 1)]
    assert search(parse_groups("(a|b)*c"), "ababc") == [(0, 5), (3, 4)]
    assert search(parse_groups("b"), "aab") == [(2, 3)]
    assert search(parse_groups("ab|b"), "bab") == [(0, 1)]


def test_edge_cases():
    assert search(EMPTY, "") is None
    assert search(EMPTY, "ab") is None
    assert search(EPS, "") == [(0, 0)]
    assert search(EPS, "ab") == [(0, 0)]
    assert fullmatch(EPS, "a") is None
    assert search(parse_groups("a"), "") is None
    assert search(parse_groups("(∅)|b"), "b") == [(0, 1), None]
    # An empty iteration that would revisit the star's split is cut, so these
    # differ from Python's re, which reports (0, 0), (0, 0), (2, 2) and (2, 2).
    assert search(parse_groups("(a*)*"), "") == [(0, 0), None]
    assert search(parse_groups("(a*)*"), "b") == [(0, 0), None]
    assert search(parse_groups("(a*)*"), "aa") == [(0, 2), (0, 2)]
    assert search(parse_groups("(a|ε)*b"), "aab") == [(0, 3), (1, 2)]
    assert fullmatch(parse_groups("((a*)*b*)*"), "abab") == bitstate(*compile_regex(parse_groups("((a*)*b*)*")), "abab", True)


def test_deep_inputs():
    n = 3000
    r = ("sym", "a")
    for _ in range(n - 1):
        r = ("cat", r, ("sym", "a"))
    assert fullmatch(r, "a" * n) == [(0, n)]
    assert fullmatch(r, "a" * (n - 1)) is None
    s = ("sym", "b")
    for _ in range(1500):
        s = ("star", ("group", s))
    spans = search(s, "b" * 50)
    assert spans[0] == (0, 50)
    assert search(("cat", s, ("sym", "c")), "b" * 40) is None


def test_random_against_backtracker_and_language():
    rng = random.Random(2026_11_06)
    for trial in range(1500):
        alphabet = "ab" if trial % 2 == 0 else "abc"
        r = decorate(rng, random_regex(rng, alphabet, 4))
        prog, ngroups = compile_regex(r)
        lang = language(plain(r), 6 if alphabet == "ab" else 4)
        for w in words(alphabet, 6 if alphabet == "ab" else 4):
            got = pike_vm(prog, ngroups, w, full=True)
            assert (got is not None) == (w in lang), (r, w)
            assert got == bitstate(prog, ngroups, w, True), (r, w)
        for _ in range(4):
            t = random_text(rng, alphabet)
            got = pike_vm(prog, ngroups, t)
            assert got == bitstate(prog, ngroups, t), (r, t)
            subs = [t[j:k] for j in range(len(t) + 1) for k in range(j, len(t) + 1)]
            big = language(plain(r), len(t))
            assert (got is not None) == any(x in big for x in subs), (r, t)
            if got is not None:
                s0, s1 = got[0]
                assert t[s0:s1] in big
                for sp in got[1:]:
                    if sp is not None:
                        assert s0 <= sp[0] <= sp[1] <= s1


def test_random_against_python_re():
    rng = random.Random(7)
    compared = 0
    while compared < 800:
        alphabet = "ab" if compared % 2 == 0 else "abc"
        r = decorate(rng, random_regex(rng, alphabet, 4))
        if has_nullable_star_body(r):
            continue
        compared += 1
        for _ in range(5):
            t = random_text(rng, alphabet)
            assert search(r, t) == python_spans(r, t), (r, to_python(r), t)


def test_nested_stars_against_backtracker():
    for text in ["(a*)*", "((a*)*b)*", "(a*b*)*", "((ε|a)*)*", "(∅|a*)*b", "((a*?)*)*", "(a|ab)*(b*)"]:
        r = parse_groups(text)
        prog, ngroups = compile_regex(r)
        for w in words("ab", 6):
            assert pike_vm(prog, ngroups, w) == bitstate(prog, ngroups, w), (text, w)
            assert pike_vm(prog, ngroups, w, True) == bitstate(prog, ngroups, w, True), (text, w)
