---
tag: D5CP96
kind: definition
slug: kerning
name: Kerning
aliases:
- pair kerning
area: strings/text-processing-and-typesetting
level: intro
summary: An adjustment of the space between a specific pair of glyphs, such as A and V, read from a pair table or class table of the font.
prereqs: [unicode-code-point]
see_also: [text-shaping, tex-math-layout, greedy-line-breaking, knuth-plass-line-breaking, box-glue-penalty-model]
sources:
  - url: https://learn.microsoft.com/en-us/typography/opentype/spec/gpos
    title: OpenType specification, GPOS, the Glyph Positioning Table
    locator: lookup type 2, pair adjustment positioning (format 1 for pairs of glyphs, format 2 for pairs of glyph classes)
  - url: https://learn.microsoft.com/en-us/typography/opentype/spec/chapter2
    title: OpenType specification, OpenType Layout Common Table Formats
    locator: Features and lookups, the lookup table (subtables are tried in order and the first match is used)
---

Kerning is a change of the space between two particular glyphs that stand next to each other, so that the gap looks the same as between other letters. In "AV" or "To", the shapes leave a large empty area between the glyphs, so the font moves them closer; in a few pairs it moves them apart. The font gives these changes as a table of pairs, or as a table of pairs of glyph classes, and the text shaper reads it when it positions the glyphs.

## Definition

A font gives each glyph $g$ an **advance** $\mathrm{adv}(g)$, the distance the pen moves after the glyph. A **kerning function** gives a number $k(g, h)$ for each ordered pair of glyphs, and $k(g, h) = 0$ for most pairs. For a line of glyphs $g_1, \ldots, g_n$, the pen positions are
$$x_1 = 0, \qquad x_{i+1} = x_i + \mathrm{adv}(g_i) + k(g_i, g_{i+1}),$$
and the width of the line is $\sum_i \mathrm{adv}(g_i) + \sum_{i < n} k(g_i, g_{i+1})$. A negative kern moves the second glyph closer.

Kerning is applied to each pair of neighbors in turn, so "AVA" gets the kern of (A, V) and the kern of (V, A).

**Pair kerning and class kerning.** A font can give $k$ in two ways, which are the two formats of the pair adjustment lookup in the GPOS table of OpenType:

- a **pair table** (format 1) lists single pairs of glyphs, each with its value;
- a **class table** (format 2) puts glyphs into classes, $c_1(g)$ for the first glyph and $c_2(h)$ for the second, and gives a matrix $K$ so that $k(g, h) = K[c_1(g)][c_2(h)]$. Class 0 holds all glyphs that are not in another class.

A class table is small, since A, À and Á can share one class. A pair table gives **exceptions** to it. The subtables of one lookup are tried in order and the first one that matches the pair is used, so a font that lists the pair table first can give one pair a value that its classes do not.

## Examples and non-examples

The numbers below are made up, in units of 1/1000 of the font size.

- The advances of A and V are 667 each and $k(\mathrm{A}, \mathrm{V}) = -80$. Without kerning "AV" is 1334 wide; with kerning it is 1254.
- A class table puts A, À and Á in one class and V, W in another, with the value $-80$. Then "ÁW" also gets $-80$ without a pair of its own.
- An exception: the pair table gives (A, W) the value $-60$. With the pair table first, "AW" gets $-60$ and "ÀW" still gets $-80$ from the classes.
- **Not kerning: tracking.** Letter spacing adds the same amount after every glyph of a text. It does not depend on the pair.
- **Not kerning: ligatures.** Joining f and i into one glyph fi is a substitution, not a change of position.
- **Not kerning: mark positioning.** Placing an accent on a letter moves the accent by an offset from anchor points; it is a different lookup type of GPOS.

## Related definitions

- [Text shaping](/text-shaping/) applies kerning as one of its positioning steps, after the substitutions.
- In TeX, a font gives kerns in its lig/kern program, and TeX puts a kern item into the list between the two characters. In the [box, glue and penalty model](/box-glue-penalty-model/) a kern is a fixed space that cannot stretch or shrink.
- Line breaking needs the widths of words, so it uses the kerned widths; see [greedy line breaking](/greedy-line-breaking/).

## References
