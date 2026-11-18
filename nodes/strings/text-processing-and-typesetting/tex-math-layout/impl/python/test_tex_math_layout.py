# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tex-math-layout/. The authors are listed in prov/7WJTT8.jsonl.

import random

from tex_math_layout import (
    CHARS,
    D,
    D_,
    PARAMS,
    RULE_THICKNESS,
    S,
    S_,
    SS,
    SS_,
    T,
    T_,
    Char,
    Frac,
    Row,
    Scripts,
    cramped,
    denom_style,
    half,
    layout,
    num_style,
    parse,
    size_of,
    sub_style,
    sup_style,
)


def test_style_tables():
    # The TeXbook, chapter 17: the styles of superscripts, subscripts, numerators and denominators.
    assert [sup_style(s) for s in range(8)] == [S, S_, S, S_, SS, SS_, SS, SS_]
    assert [sub_style(s) for s in range(8)] == [S_, S_, S_, S_, SS_, SS_, SS_, SS_]
    assert [num_style(s) for s in range(8)] == [T, T_, S, S_, SS, SS_, SS, SS_]
    assert [denom_style(s) for s in range(8)] == [T_, T_, S_, S_, SS_, SS_, SS_, SS_]
    assert [size_of(s) for s in range(8)] == [0, 0, 0, 0, 1, 1, 2, 2]
    for s in range(8):
        assert cramped(sub_style(s)) and cramped(denom_style(s))
        assert cramped(sup_style(s)) == cramped(s)


def test_half_matches_tex():
    assert [half(x) for x in (-4, -3, -2, -1, 0, 1, 2, 3, 4)] == [-2, -1, -1, 0, 0, 1, 1, 2, 2]


def test_toy_font_sizes():
    assert CHARS[0]["2"] == (50, 64, 0)
    assert CHARS[1]["2"] == (35, 44, 0)
    assert CHARS[1]["y"] == (34, 30, 13)
    assert PARAMS[1]["sup_drop"] == 27 and PARAMS[1]["sub_drop"] == 3


def dims(b):
    return (b.width, b.height, b.depth)


def test_superscript_on_a_character():
    b = layout(parse("x^2"), T)
    assert b.info["u"] == 36  # sup2, since T is neither display nor cramped
    assert dims(b) == (57 + 35 + 5, 44 + 36, 0)
    assert layout(parse("x^2"), D).info["u"] == 41  # sup1
    assert layout(parse("x^2"), T_).info["u"] == 29  # sup3


def test_subscript_alone():
    b = layout(parse("x_1"), T)
    assert b.info["v"] == 15  # sub1 beats 44 - 4 * 43 / 5 = 10
    assert dims(b) == (97, 43, 15)


def test_both_scripts_without_and_with_the_gap_rule():
    b = layout(parse("x_1^2"), T)
    assert (b.info["u"], b.info["v"]) == (36, 25)  # the gap 17 is at least 4 * theta = 16
    assert dims(b) == (97, 80, 25)
    b = layout(parse("x_b^2"), T)
    assert (b.info["u"], b.info["v"]) == (36, 28)  # gap 13: the subscript moves down by 3
    b = layout(parse("x_1^2"), T_)
    # gap 10: v = 31; then the bottom of the superscript is 29 < 34, so both move up by 5
    assert (b.info["u"], b.info["v"]) == (34, 26)


def test_scripts_on_a_box_use_the_drops():
    b = layout(parse("{xy}^2"), T)
    assert b.info["u"] == 36  # 43 - 27 = 16 is less than sup2
    b = layout(parse("\\frac{1}{2}^2"), T)
    assert b.info["u"] == 83 - 27  # the height of the fraction minus sup_drop at script size
    assert b.height == 44 + 56
    b = layout(parse("{xy}_1"), T)
    assert b.info["v"] == 19 + 3  # the depth of y plus sub_drop at script size


def test_fraction_in_text_and_display():
    b = layout(parse("\\frac{1}{2}"), T)
    assert (b.info["u"], b.info["v"]) == (39, 34)  # num2 and denom2, no correction
    assert dims(b) == (35 + 24, 83, 34)
    b = layout(parse("\\frac{1}{2}"), D)
    assert (b.info["u"], b.info["v"]) == (68, 69)  # num1 and denom1
    assert dims(b) == (50 + 24, 132, 69)
    b = layout(parse("\\frac{y}{2}"), T)
    assert b.info["u"] == 44  # the depth of y leaves a gap of -1 to the rule: raise by 5
    b = layout(parse("\\atop{1}{2}"), T)
    assert (b.info["u"], b.info["v"]) == (44, 34)  # num3, no rule


def test_narrower_part_is_centered_and_width_is_the_wider():
    b = layout(parse("\\frac{xy}{2}"), T)
    assert b.width == CHARS[1]["x"][0] + CHARS[1]["y"][0] + 24


def random_formula(rng, depth):
    k = rng.random()
    if depth == 0 or k < 0.35:
        return Char(rng.choice("xyabn12"))
    if k < 0.55:
        return Row(tuple(random_formula(rng, depth - 1) for _ in range(rng.randint(1, 3))))
    if k < 0.75:
        return Frac(random_formula(rng, depth - 1), random_formula(rng, depth - 1), rng.choice([None, None, 0, 2, 7]))
    sup = random_formula(rng, depth - 1) if rng.random() < 0.7 else None
    sub = random_formula(rng, depth - 1) if sup is None or rng.random() < 0.5 else None
    return Scripts(random_formula(rng, depth - 1), sup, sub)


def test_invariants_on_random_formulas():
    rng = random.Random(1)
    for _ in range(600):
        f = random_formula(rng, 3)
        s = rng.randrange(8)
        b = layout(f, s)
        assert b.width >= 0 and b.height + b.depth >= 0
        if isinstance(f, Scripts) and f.sup is not None and f.sub is not None:
            x, y = layout(f.sup, sup_style(s)), layout(f.sub, sub_style(s))
            assert (b.info["u"] - x.depth) - (y.height - b.info["v"]) >= 4 * RULE_THICKNESS
        if isinstance(f, Frac):
            x, z = layout(f.num, num_style(s)), layout(f.den, denom_style(s))
            u, v, th = b.info["u"], b.info["v"], b.info["theta"]
            p = PARAMS[size_of(s)]
            if th == 0:
                clr = (7 if s < T else 3) * RULE_THICKNESS
                assert (u - x.depth) - (z.height - v) >= clr
            else:
                clr = 3 * th if s < T else th
                d = half(th)
                assert (u - x.depth) - (p["axis_height"] + d) >= clr
                assert (p["axis_height"] - d) - (z.height - v) >= clr


def test_scripts_shrink_with_the_style():
    for s in range(8):
        b = layout(Scripts(Char("x"), Char("2")), s)
        x = CHARS[size_of(sup_style(s))]["2"]
        assert b.width == CHARS[size_of(s)]["x"][0] + x[0] + 5
    assert layout(parse("x^{x^{x^2}}"), T).width == 57 + (39 + 5) + (28 + 5) + (25 + 5)


def test_parser():
    assert parse("x") == Char("x")
    assert parse("x_1^2") == Scripts(Char("x"), Char("2"), Char("1"))
    assert parse("\\frac{a}{b}") == Frac(Char("a"), Char("b"))
    assert parse("{xy}^2") == Scripts(Row((Char("x"), Char("y"))), Char("2"), None)
    assert parse("ab") == Row((Char("a"), Char("b")))
