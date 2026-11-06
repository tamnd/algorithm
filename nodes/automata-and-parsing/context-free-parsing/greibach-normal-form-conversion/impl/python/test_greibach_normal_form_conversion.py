# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greibach-normal-form-conversion/. The authors are listed in prov/0QNXET.jsonl.

import itertools
import random

from greibach_normal_form_conversion import is_gnf, to_gnf


def language(productions, start, max_len):
    """Independent oracle: least fixed point of the sets of terminal strings
    of length at most max_len derived by each nonterminal. Handles empty,
    unit and cyclic productions directly."""
    nts = {a for a, _ in productions}
    lang = {a: set() for a in nts}
    changed = True
    while changed:
        changed = False
        for a, rhs in productions:
            cur = {()}
            for x in rhs:
                part = lang[x] if x in nts else {(x,)}
                cur = {u + v for u in cur for v in part if len(u) + len(v) <= max_len}
            if not cur <= lang[a]:
                lang[a] |= cur
                changed = True
    return lang.get(start, set())


def gnf_derives(productions, start, w):
    """Membership for a grammar in Greibach normal form: each step reads one
    terminal, so a set of stacks of nonterminals is enough."""
    if not w:
        return (start, ()) in productions
    by = {}
    for a, r in productions:
        if r:
            by.setdefault((a, r[0]), []).append(r[1:])
    stacks = {(start,)}
    for x in w:
        nxt = set()
        for st in stacks:
            if st:
                for tail in by.get((st[0], x), []):
                    if len(tail) + len(st) - 1 <= len(w):
                        nxt.add(tuple(tail) + st[1:])
        stacks = nxt
    return () in stacks


def random_grammar(rng, nts, maxlen, eps=0.15):
    names = ["S", "A", "B"][:nts]
    prods = []
    for a in names:
        for _ in range(rng.randint(1, 3)):
            if rng.random() < eps:
                prods.append((a, ()))
            else:
                prods.append((a, tuple(rng.choice(names + ["a", "b"]) for _ in range(rng.randint(1, maxlen)))))
    return list(dict.fromkeys(prods))


def words(max_len):
    for m in range(max_len + 1):
        yield from itertools.product("ab", repeat=m)


def check(g, start, max_len, self_check=False):
    out, s0 = to_gnf(g, start)
    assert is_gnf(out, s0)
    ref = language(g, start, max_len)
    if self_check:  # the GNF membership test against the general oracle
        assert language(out, s0, max_len) == ref
    count = 0
    for w in words(max_len):
        assert (w in ref) == gnf_derives(out, s0, w), (g, w)
        count += 1
    return count


def test_hopcroft_ullman_example():
    g = [("A1", ("A2", "A3")), ("A2", ("A3", "A1")), ("A2", ("b",)), ("A3", ("A1", "A2")), ("A3", ("a",))]
    out, s0 = to_gnf(g, "A1")
    assert s0 == "A1" and is_gnf(out, s0)
    counts = {}
    for a, _ in out:
        counts[a] = counts.get(a, 0) + 1
    assert counts == {"A1": 5, "A2": 5, "A3": 4, "A3_rec": 10}
    assert ("A3", ("b", "A3", "A2", "A3_rec")) in out
    check(g, "A1", 9, self_check=True)
    assert {w for w in language(g, "A1", 5)} == {tuple("ba"), tuple("abaa"), tuple("bbab")}


def test_empty_string_and_edges():
    out, s0 = to_gnf([("S", ())], "S")
    assert out == [(s0, ())] and s0 != "S"
    out, s0 = to_gnf([("S", ("S",))], "S")
    assert out == []
    for g in (
        [("S", ("a", "S", "b")), ("S", ())],
        [("S", ("S", "S")), ("S", ("a",)), ("S", ())],
        [("S", ("A",)), ("A", ("B",)), ("B", ("S",)), ("B", ("a",))],
        [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("a",))],
    ):
        out, s0 = to_gnf(g, g[0][0])
        assert is_gnf(out, s0)
        ref = language(g, g[0][0], 6)
        assert language(out, s0, 6) == ref
        for w in words(6):
            assert (w in ref) == gnf_derives(out, s0, w)
    g = [("E", ("E", "+", "T")), ("E", ("T",)), ("T", ("a",))]
    out, s0 = to_gnf(g, "E")
    assert gnf_derives(out, s0, tuple("a+a+a+a"))
    assert not gnf_derives(out, s0, tuple("a++a"))


def test_exponential_family():
    for m in range(2, 8):
        g = [(f"A{m}", (f"A{m-1}", x)) for x in "ab"]
        g += [("A1", ("a",)), ("A1", ("b",))]
        g += [(f"A{i}", (f"A{i-1}", x)) for i in range(2, m) for x in "ab"]
        out, s0 = to_gnf(g, f"A{m}")
        assert len(out) == 2 ** (m + 1)


def test_random_against_oracle():
    rng = random.Random(20261106)
    total = 0
    for nts, maxlen in ((1, 3), (2, 3), (3, 2)):
        for _ in range(250):
            g = random_grammar(rng, nts, maxlen)
            total += check(g, "S", 5, self_check=True)
    assert total >= 500
