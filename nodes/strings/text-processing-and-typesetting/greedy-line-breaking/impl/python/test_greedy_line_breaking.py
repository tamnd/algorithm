# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-line-breaking/. The authors are listed in prov/HF8Z28.jsonl.

import math
import random
from fractions import Fraction

from boxglue import (
    FIL,
    FILL,
    INF_BAD,
    INF_PENALTY,
    Box,
    Glue,
    Measures,
    Penalty,
    adjustment_ratio,
    all_breakings,
    badness,
    is_forced,
    is_legal_break,
    is_overfull,
    legal_breakpoints,
    paragraph,
    render,
    tex_badness,
    tex_line_badness,
)

# ---------------------------------------------------------------- the helper


def direct_line(items, a, b):
    """Measures of the line a..b by a direct scan, without prefix sums."""
    i = 0 if a < 0 else a + 1
    if a >= 0:
        while i < b and not isinstance(items[i], Box):
            i += 1
    L = 0
    Y = [0, 0, 0, 0]
    Z = [0, 0, 0, 0]
    for x in items[i:b]:
        if isinstance(x, Box):
            L += x.width
        elif isinstance(x, Glue):
            L += x.width
            Y[x.stretch_order] += x.stretch
            Z[x.shrink_order] += x.shrink
    if isinstance(items[b], Penalty):
        L += items[b].width
    return L, tuple(Y), tuple(Z)


def random_items(rng, n_words):
    words = []
    for _ in range(n_words):
        k = rng.randint(1, 3)
        words.append([rng.randint(1, 6) for _ in range(k)])
    space = Glue(rng.randint(1, 3), rng.randint(0, 2), rng.randint(0, 1))
    items = paragraph(words, space=space, hyphen_width=1, hyphen_penalty=50)
    # put a few extra items in, to test the discard rule and the orders
    j = rng.randrange(len(items) - 3)
    items.insert(j, Glue(2, 1, 1, stretch_order=rng.choice([0, FIL, FILL])))
    items.insert(j, Penalty(0, rng.choice([0, 100, INF_PENALTY, -INF_PENALTY])))
    return items


def test_paragraph_builder():
    items = paragraph([3, ["ab", "c"], Fraction(5, 2)], space=Glue(1, 1, 1))
    assert items[0] == Box(3)
    assert items[1] == Glue(1, 1, 1)
    assert items[2] == Box(2, text="ab")
    assert items[3] == Penalty(1, 50, True)
    assert items[4] == Box(1, text="c")
    assert items[6] == Box(Fraction(5, 2))
    assert items[-3:] == [Penalty(0, INF_PENALTY), Glue(0, 1, 0, stretch_order=FIL), Penalty(0, -INF_PENALTY)]
    assert is_forced(items[-1]) and not is_forced(items[-3])


def test_legal_breakpoints():
    items = paragraph([2, [1, 1], 3])
    # 0 box, 1 glue, 2 box, 3 hyphen, 4 box, 5 glue, 6 box, 7 pen 10000, 8 fil glue, 9 pen -10000
    assert legal_breakpoints(items) == [1, 3, 5, 9]
    assert not is_legal_break(items, 7) and not is_legal_break(items, 8)
    glue_after_glue = [Box(1), Glue(1), Glue(1), Box(1)]
    assert legal_breakpoints(glue_after_glue) == [1]


def test_measures_against_direct_scan():
    rng = random.Random(7)
    for _ in range(200):
        items = random_items(rng, rng.randint(1, 6))
        meas = Measures(items)
        legal = legal_breakpoints(items)
        for a in [-1] + legal:
            for b in legal:
                if b > a:
                    assert meas.line(a, b) == direct_line(items, a, b)


def test_vertical_measures():
    items = [Box(5, height=10, depth=2), Glue(3, 1, 1), Box(5, height=8, depth=1), Penalty(4, 0)]
    meas = Measures(items, vertical=True)
    assert meas.line(-1, 3) == (10 + 2 + 3 + 8 + 1, (1, 0, 0, 0), (1, 0, 0, 0))


def test_adjustment_ratio():
    assert adjustment_ratio(19, 19, 3, 3) == (0, 0)
    assert adjustment_ratio(19, 18, 3, 3) == (Fraction(1, 3), 0)
    assert adjustment_ratio(19, 20, 3, 3) == (Fraction(-1, 3), 0)
    assert adjustment_ratio(10, 4, 0, 0) == (math.inf, 0)
    assert adjustment_ratio(10, 14, 2, 0) == (-math.inf, 0)
    assert adjustment_ratio(10, 4, (3, 2, 0, 0), 0) == (Fraction(3), FIL)
    r, o = adjustment_ratio(10, 16, 3, 3)
    assert r == -2 and is_overfull(r, o)
    assert not is_overfull(Fraction(-1), 0) and not is_overfull(-5, FIL)


def test_real_badness():
    assert badness(Fraction(1, 3)) == Fraction(100, 27)
    assert badness(Fraction(-1, 3)) == Fraction(100, 27)
    assert badness(Fraction(1)) == 100
    assert badness(Fraction(-1)) == 100
    assert badness(Fraction(5)) == INF_BAD
    assert badness(math.inf) == INF_BAD
    assert badness(Fraction(-3, 2)) == math.inf
    assert badness(Fraction(7), FIL) == 0


def test_tex_badness_check_values():
    assert tex_badness(1, 3) == 4
    assert tex_badness(1, 1) == 100
    assert tex_badness(1, 2) == 12
    assert tex_badness(2, 1) == 800
    assert tex_badness(3, 10) == 3
    assert tex_badness(0, 0) == 0
    assert tex_badness(5, 0) == INF_BAD
    assert tex_badness(1000, 1) == INF_BAD


def test_tex_badness_monotone_and_close():
    # the integer badness of TeX grows with t and falls with s: badness(t+1, s) >= badness(t, s) >= badness(t, s+1)
    for s in range(1, 60):
        for t in range(0, 150):
            b = tex_badness(t, s)
            assert tex_badness(t + 1, s) >= b >= tex_badness(t, s + 1)
    rng = random.Random(3)
    for _ in range(2000):
        s = rng.randint(65536, 20 * 65536)
        t = rng.randint(0, 2 * s)
        exact = Fraction(100 * t**3, s**3)
        b = tex_badness(t, s)
        if exact < 1000:
            # the integer form is within 1 plus 2 percent of the real form here
            assert abs(b - exact) <= 1 + exact / 50


def test_tex_line_badness():
    pt = 65536
    assert tex_line_badness(19 * pt, 18 * pt, 3 * pt, 3 * pt) == 4
    assert tex_line_badness(19 * pt, 20 * pt, 3 * pt, 3 * pt) == 4
    assert tex_line_badness(19 * pt, 23 * pt, 3 * pt, 3 * pt) == INF_BAD + 1
    assert tex_line_badness(19 * pt, 2 * pt, (0, 1, 0, 0), 0) == 0
    assert tex_line_badness(19 * pt, 19 * pt, 0, 0) == 0


def test_all_breakings():
    items = paragraph([2, [1, 1], 3, 4])
    optional = [b for b in legal_breakpoints(items) if b != len(items) - 1]
    got = list(all_breakings(items))
    assert len(got) == 2 ** len(optional)
    assert len(set(got)) == len(got)
    for br in got:
        assert br[-1] == len(items) - 1
        assert list(br) == sorted(br)
        assert all(is_legal_break(items, b) for b in br)
    forced_inside = [Box(1), Glue(1), Box(1), Penalty(0, -INF_PENALTY), Box(1), Glue(1), Box(1), Penalty(0, -INF_PENALTY)]
    got = list(all_breakings(forced_inside))
    assert got == [(3, 7), (3, 5, 7), (1, 3, 7), (1, 3, 5, 7)]


def test_render():
    items = paragraph(["hyph", "en", ["ex", "am", "ple"], "go"])
    br = (1, 7, len(items) - 1)  # after hyph, at the hyphen after am, at the end
    assert items[7] == Penalty(1, 50, True)
    assert render(items, br) == ["hyph", "en exam-", "ple go"]


# ---------------------------------------------------------------- greedy line breaking

from greedy_line_breaking import fits, greedy_line_breaks  # noqa: E402


def all_lines_fit(items, br, l):
    meas = Measures(items)
    a = -1
    for b in br:
        if not fits(meas, a, b, l):
            return False
        a = b
    return True


def line_badness(items, br, l):
    meas = Measures(items)
    out, a = [], -1
    for b in br:
        L, Y, Z = meas.line(a, b)
        r, order = adjustment_ratio(l, L, Y, Z)
        out.append(badness(r, order))
        a = b
    return out


def fixed_space_items(rng):
    """Random words with hyphenation points; glue that cannot stretch, and shrink <= width."""
    n_words = rng.randint(1, 9)
    words = []
    for _ in range(n_words):
        k = 1 if rng.random() < 0.7 else 2
        words.append([rng.randint(1, 5) for _ in range(k)])
    w = rng.randint(1, 2)
    space = Glue(w, 0, rng.randint(0, w))
    items = paragraph(words, space=space, hyphen_width=1, hyphen_penalty=50)
    return items, max(max(p) for p in words) + 1


def test_greedy_example_of_the_page():
    words = "the quick brown fox jumps over the lazy dog".split()
    items = paragraph(words, space=Glue(1, 0, 0))
    br = greedy_line_breaks(items, 15)
    assert render(items, br) == ["the quick brown", "fox jumps over", "the lazy dog"]


def test_greedy_fewest_lines_against_brute_force():
    rng = random.Random(7)
    for _ in range(250):
        items, wmin = fixed_space_items(rng)
        l = rng.randint(wmin, wmin + 12)
        g = greedy_line_breaks(items, l)
        assert all_lines_fit(items, g, l)
        feasible = [br for br in all_breakings(items) if all_lines_fit(items, br, l)]
        assert feasible
        assert len(g) == min(len(br) for br in feasible)
        # greedy stays ahead: its k-th break is at least the k-th break of any feasible breaking
        for br in feasible:
            for k in range(len(g)):
                assert g[k] >= br[k]


def test_greedy_takes_the_farthest_break_with_varying_lengths():
    rng = random.Random(11)
    for _ in range(200):
        items, wmin = fixed_space_items(rng)
        lengths = [rng.randint(wmin, wmin + 8) for _ in range(3)]
        g = greedy_line_breaks(items, lengths)
        meas = Measures(items)
        legal = legal_breakpoints(items)
        a = -1
        for j, b in enumerate(g):
            l = lengths[min(j, 2)]
            assert fits(meas, a, b, l)
            later = [c for c in legal if c > b]
            assert all(not fits(meas, a, c, l) for c in later)
            a = b


def test_stretch_model_greedy_fails():
    # Glue 2 with stretch 1 and shrink 1, lines of length 8, tolerance 200 as in plain TeX.
    words = ["ab", "abc", "a", "abcd", "abcd"]
    items = paragraph(words, space=Glue(2, 1, 1))
    g = greedy_line_breaks(items, 8)
    assert render(items, g) == ["ab abc a", "abcd", "abcd"]
    assert line_badness(items, g, 8) == [100, 10000, 0]
    good = [br for br in all_breakings(items) if all(x <= 200 for x in line_badness(items, br, 8))]
    assert [render(items, br) for br in good] == [["ab abc", "a abcd", "abcd"]]
    assert line_badness(items, good[0], 8) == [100, 100, 0]
    # the least total badness over all breakings (the total-fit choice) is 200, greedy gives 10100
    best = min(sum(line_badness(items, br, 8)) for br in all_breakings(items))
    assert best == 200 and sum(line_badness(items, g, 8)) == 10100


def test_overfull_word_and_forced_break():
    items = paragraph(["abcdefghij", "ab"], space=Glue(1, 0, 0))
    g = greedy_line_breaks(items, 5)
    assert render(items, g) == ["abcdefghij", "ab"]
    assert not all_lines_fit(items, g, 5)
    forced = [Box(1), Glue(1), Box(1), Penalty(0, -INF_PENALTY), Box(1), Glue(1), Box(1), Penalty(0, -INF_PENALTY)]
    assert greedy_line_breaks(forced, 100) == [3, 7]


def test_greedy_measures_a_linear_number_of_lines():
    rng = random.Random(3)
    words = [rng.randint(1, 6) for _ in range(2000)]
    items = paragraph(words, space=Glue(1, 0, 0))
    stats = {}
    greedy_line_breaks(items, 30, stats)
    assert stats["tests"] <= 2 * len(items)
