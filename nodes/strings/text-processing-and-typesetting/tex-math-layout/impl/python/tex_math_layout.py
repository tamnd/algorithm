# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tex-math-layout/. The authors are listed in prov/7WJTT8.jsonl.

"""Two rules of the math layout of TeX: scripts (rule 18) and fractions (rule 15).

This follows The TeXbook, appendix G, and TeX: The Program, parts 35 and
36 (make_scripts and make_fraction), for a small part of math: single
characters, horizontal lists of atoms, fractions with null delimiters,
and sub and superscripts. It leaves out the spacing between atoms
(rule 20), italic corrections (taken as 0), large operators, radicals,
accents and delimiters of variable size.

The font is a toy font. Its character sizes and its parameters are made
up for this page, loosely in the range of a 10 point font in units of
0.1 pt; they are not the values of any real font. All sizes are ints, and
// stands for the div of Pascal, which agrees with it on the values used
here (the only signed division is half, written to match TeX).
"""

from dataclasses import dataclass, field
from typing import Optional, Union

# ----------------------------------------------------------------- styles

D, D_, T, T_, S, S_, SS, SS_ = range(8)  # display, text, script, scriptscript; _ is cramped
STYLE_NAMES = ["D", "D'", "T", "T'", "S", "S'", "SS", "SS'"]
TEXT_SIZE, SCRIPT_SIZE, SCRIPT_SCRIPT_SIZE = 0, 1, 2


def cramped(s: int) -> bool:
    return s % 2 == 1


def size_of(s: int) -> int:
    """The font size of a style: D and T use text size, S script size, SS scriptscript size."""
    return max(0, s // 2 - 1)


def sub_style(s: int) -> int:
    return 2 * (s // 4) + S + 1


def sup_style(s: int) -> int:
    return 2 * (s // 4) + S + (s % 2)


def num_style(s: int) -> int:
    return s + 2 - 2 * (s // 6)


def denom_style(s: int) -> int:
    return 2 * (s // 2) + 1 + 2 - 2 * (s // 6)


def half(x: int) -> int:
    """half of TeX: (x + 1) div 2 for odd x, x div 2 for even x."""
    return (x + 1) // 2


# ------------------------------------------------------------- the toy font

_TEXT_CHARS = {  # made up: (width, height, depth) at text size
    "x": (57, 43, 0),
    "y": (49, 43, 19),
    "a": (53, 43, 0),
    "b": (43, 69, 0),
    "n": (60, 43, 0),
    "1": (50, 64, 0),
    "2": (50, 64, 0),
}
_TEXT_PARAMS = {  # made up, named as in TeX: sigma 5 and sigma 8 to sigma 22
    "x_height": 43,
    "num1": 68,
    "num2": 39,
    "num3": 44,
    "denom1": 69,
    "denom2": 34,
    "sup1": 41,
    "sup2": 36,
    "sup3": 29,
    "sub1": 15,
    "sub2": 25,
    "sup_drop": 39,
    "sub_drop": 5,
    "axis_height": 25,
}
_SCALE = [(1, 1), (7, 10), (5, 10)]  # text, script and scriptscript sizes


def _scaled(v: int, size: int) -> int:
    a, b = _SCALE[size]
    return v * a // b


CHARS = [{c: tuple(_scaled(v, z) for v in dims) for c, dims in _TEXT_CHARS.items()} for z in range(3)]
PARAMS = [{k: _scaled(v, z) for k, v in _TEXT_PARAMS.items()} for z in range(3)]
RULE_THICKNESS = 4  # xi 8, default_rule_thickness, the same at all sizes here
SCRIPT_SPACE = 5  # \scriptspace
NULL_DELIMITER_SPACE = 12  # \nulldelimiterspace


# ------------------------------------------------------------ formulas and boxes


@dataclass(frozen=True)
class Char:
    c: str


@dataclass(frozen=True)
class Row:
    """A horizontal list of atoms, set side by side with no spacing."""

    items: tuple


@dataclass(frozen=True)
class Frac:
    num: object
    den: object
    thickness: Optional[int] = None  # None is the default rule thickness, 0 is \atop


@dataclass(frozen=True)
class Scripts:
    nucleus: object
    sup: object = None
    sub: object = None


Formula = Union[Char, Row, Frac, Scripts]


@dataclass
class Box:
    """A box with its width, height and depth. info keeps the shifts u and v."""

    width: int
    height: int
    depth: int
    info: dict = field(default_factory=dict)


def layout(f: Formula, s: int) -> Box:
    """The box of the formula f set in the style s."""
    if isinstance(f, Char):
        w, h, d = CHARS[size_of(s)][f.c]
        return Box(w, h, d)
    if isinstance(f, Row):
        boxes = [layout(g, s) for g in f.items]
        return Box(sum(b.width for b in boxes), max((b.height for b in boxes), default=0), max((b.depth for b in boxes), default=0))
    if isinstance(f, Frac):
        return make_fraction(f, s)
    if isinstance(f, Scripts):
        return make_scripts(f, s)
    raise TypeError("not a formula")


def make_scripts(f: Scripts, s: int) -> Box:
    """Rule 18: attach a superscript, a subscript or both to the nucleus."""
    z = layout(f.nucleus, s)
    p = PARAMS[size_of(s)]
    if f.sup is None and f.sub is None:
        return z
    if isinstance(f.nucleus, Char):  # @line L1
        u = v = 0
    else:  # @line L2
        t = SCRIPT_SIZE if s < S else SCRIPT_SCRIPT_SIZE
        u = z.height - PARAMS[t]["sup_drop"]
        v = z.depth + PARAMS[t]["sub_drop"]
    if f.sup is None:  # @line L3
        x = layout(f.sub, sub_style(s))  # @line L4
        x.width += SCRIPT_SPACE
        v = max(v, p["sub1"], x.height - abs(p["x_height"] * 4) // 5)  # @line L5
        return Box(z.width + x.width, max(z.height, x.height - v), max(z.depth, x.depth + v), {"u": None, "v": v})
    x = layout(f.sup, sup_style(s))  # @line L6
    x.width += SCRIPT_SPACE
    if cramped(s):  # @line L7
        clr = p["sup3"]
    elif s == D:
        clr = p["sup1"]
    else:
        clr = p["sup2"]
    u = max(u, clr, x.depth + abs(p["x_height"]) // 4)
    if f.sub is None:  # @line L8
        return Box(z.width + x.width, max(z.height, x.height + u), max(z.depth, x.depth - u), {"u": u, "v": None})
    y = layout(f.sub, sub_style(s))  # @line L9
    y.width += SCRIPT_SPACE
    v = max(v, p["sub2"])
    clr = 4 * RULE_THICKNESS - ((u - x.depth) - (y.height - v))  # @line L10
    if clr > 0:  # @line L11
        v += clr
        clr = abs(p["x_height"] * 4) // 5 - (u - x.depth)
        if clr > 0:
            u += clr
            v -= clr
    w = max(x.width, y.width)  # @line L12
    return Box(z.width + w, max(z.height, x.height + u), max(z.depth, y.depth + v), {"u": u, "v": v})


def make_fraction(f: Frac, s: int) -> Box:
    """Rule 15: a fraction with a rule of thickness theta and null delimiters."""
    p = PARAMS[size_of(s)]
    theta = RULE_THICKNESS if f.thickness is None else f.thickness  # @line L13
    x = layout(f.num, num_style(s))  # @line L14
    z = layout(f.den, denom_style(s))
    w = max(x.width, z.width)
    display = s < T
    if display:  # @line L15
        u, v = p["num1"], p["denom1"]
    else:
        v = p["denom2"]
        u = p["num2"] if theta != 0 else p["num3"]
    axis = p["axis_height"]
    if theta == 0:  # @line L16
        clr = 7 * RULE_THICKNESS if display else 3 * RULE_THICKNESS
        delta = half(clr - ((u - x.depth) - (z.height - v)))
        if delta > 0:
            u += delta
            v += delta
    else:  # @line L17
        clr = 3 * theta if display else theta
        delta = half(theta)
        delta1 = clr - ((u - x.depth) - (axis + delta))  # @line L18
        if delta1 > 0:
            u += delta1
        delta2 = clr - ((axis - delta) - (z.height - v))  # @line L19
        if delta2 > 0:
            v += delta2
    # The null delimiters are empty boxes on the axis: they add width, and the
    # height axis and the depth -axis, which rarely matter.
    height = max(x.height + u, axis)  # @line L20
    depth = max(z.depth + v, -axis)
    return Box(w + 2 * NULL_DELIMITER_SPACE, height, depth, {"u": u, "v": v, "theta": theta, "delta": delta})


def parse(text: str) -> Formula:
    """A tiny parser for tests and examples: characters, {groups}, ^, _ and \\frac{a}{b}."""
    pos = 0

    def atom():
        nonlocal pos
        if text.startswith("\\frac", pos):
            pos += 5
            a = group()
            b = group()
            return Frac(a, b)
        if text.startswith("\\atop", pos):
            pos += 5
            a = group()
            b = group()
            return Frac(a, b, 0)
        if text[pos] == "{":
            return group()
        c = text[pos]
        pos += 1
        return Char(c)

    def group():
        nonlocal pos
        if text[pos] != "{":
            return atom()
        pos += 1
        items = []
        while text[pos] != "}":
            items.append(scripted())
        pos += 1
        return items[0] if len(items) == 1 else Row(tuple(items))

    def scripted():
        nonlocal pos
        nuc = atom()
        sup = sub = None
        while pos < len(text) and text[pos] in "^_":
            op = text[pos]
            pos += 1
            arg = atom()
            if op == "^":
                sup = arg
            else:
                sub = arg
        return Scripts(nuc, sup, sub) if sup is not None or sub is not None else nuc

    items = []
    while pos < len(text):
        items.append(scripted())
    return items[0] if len(items) == 1 else Row(tuple(items))
