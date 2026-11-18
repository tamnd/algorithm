---
tag: 7WJTT8
kind: algorithm
slug: tex-math-layout
name: TeX math layout algorithm
aliases:
- TeX Appendix G algorithm
area: strings/text-processing-and-typesetting
level: advanced
summary: Lay out a formula by turning a math list into boxes recursively, with styles that shrink sub and superscripts and font parameters for their shifts.
model: word-ram
complexity:
  vars: {n: the number of nodes of the formula}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: true, exact: true}
history:
  year: 1984
  people: [Donald E. Knuth]
  note: Knuth gave the rules that turn a formula into boxes in appendix G of The TeXbook in 1984, and their code in TeX, The Program in 1986.
prereqs: [box-glue-penalty-model]
see_also: [text-shaping, kerning, box-glue-penalty-model, knuth-plass-line-breaking, best-fit-page-breaking, unicode-code-point]
sources:
  - book: isbn:9780201134476
    title: Donald E. Knuth, The TeXbook, Addison-Wesley, 1984
    locator: "appendix G, Generating boxes from formulas: rule 15 for fractions and rule 18 for sub and superscripts; chapter 17 for the styles"
  - book: isbn:9780201134377
    title: Donald E. Knuth, TeX, The Program, Addison-Wesley, 1986
    locator: part 35, Subroutines for math mode, and part 36, Typesetting math formulas (make_fraction and make_scripts)
---

The math layout algorithm of TeX turns a formula, given as a tree of atoms, into a box of a known width, height and depth. It works from the inside out: it sets the parts of a fraction or the scripts of a symbol first, in a smaller **style**, and then places them with shifts that come from **font parameters**, such as the height of a superscript or the gap above a fraction bar. Each rule moves the parts apart until fixed clearances hold, so that a superscript never touches a subscript and a numerator never touches the bar. TeX uses its own rules and the parameters of its math fonts, not the shaping rules of OpenType or the Unicode text algorithms; see [text shaping](/text-shaping/) for that other model.

## In plain words

A formula is built from small pieces. For $x^2$, the 2 is printed smaller and higher than the x. For a fraction, the top part goes above a bar and the bottom part below it.

The algorithm builds the inner pieces first, so it knows how big they are. Then it decides how far up or down to move each piece. The font gives the normal distances. If two pieces would come too close, the algorithm pushes them apart.

Pieces inside other pieces get smaller, but only down to a smallest size, so that they stay readable.

## The problem

A formula here is a tree with four kinds of nodes:

- a **character**, with a width, height and depth from the font;
- a **row**, a sequence of formulas set side by side;
- a **fraction** with a numerator, a denominator and a rule thickness $\theta$ (the default thickness $\xi_8$ of the font, or 0 for `\atop`);
- **scripts**: a nucleus with a superscript, a subscript or both.

The **style** is one of $D, T, S, SS$ (display, text, script and scriptscript), each in a normal and a **cramped** form ($D'$, $T'$, $S'$, $SS'$). Cramped styles raise superscripts less; they are used under a bar and in subscripts. With the styles numbered $D = 0$, $D' = 1$, $T = 2$ up to $SS' = 7$, TeX computes the style of each part with integer arithmetic:

| part | style | example |
|---|---|---|
| superscript | $2 \lfloor s/4 \rfloor + 4 + (s \bmod 2)$ | $T \to S$, $T' \to S'$, $S \to SS$ |
| subscript | $2 \lfloor s/4 \rfloor + 5$ | $T \to S'$, $S \to SS'$ |
| numerator | $s + 2 - 2 \lfloor s/6 \rfloor$ | $D \to T$, $T \to S$, $SS \to SS$ |
| denominator | $2 \lfloor s/2 \rfloor + 3 - 2 \lfloor s/6 \rfloor$ | $D \to T'$, $T \to S'$ |

$D$ and $T$ use the text size of the font, $S$ the script size and $SS$ the scriptscript size. The font gives, for each size, the parameters named $\sigma_5$ (x-height), $\sigma_8$ to $\sigma_{12}$ (`num1`, `num2`, `num3`, `denom1`, `denom2`), $\sigma_{13}$ to $\sigma_{17}$ (`sup1`, `sup2`, `sup3`, `sub1`, `sub2`), $\sigma_{18}$ and $\sigma_{19}$ (`sup_drop`, `sub_drop`) and $\sigma_{22}$ (the axis height, the height of the fraction bar), and the rule thickness $\xi_8$. The output is a box with its width, height and depth, and the shift up $u$ of the numerator or superscript and the shift down $v$ of the denominator or subscript.

## The algorithm

The layout of a character is its box, and the layout of a row puts the boxes of its parts side by side. Scripts use rule 18 of appendix G (lines L1 to L12) and fractions use rule 15 (lines L13 to L20), each after the layout of its parts in their styles. Here $\sigma$ means the parameter at the size of the current style $s$.

```pseudo id=main
SCRIPTS(nucleus box z, superscript, subscript, style s)
L1  if the nucleus is a single character then u ← 0; v ← 0
L2  else t ← the size of the scripts; u ← h(z) − sup_drop(t); v ← d(z) + sub_drop(t)
L3  if there is no superscript then
L4      x ← the subscript set in sub(s), plus the script space
L5      v ← max(v, sub1, h(x) − 4σ5/5); return z followed by x lowered by v
L6  x ← the superscript set in sup(s), plus the script space
L7  u ← max(u, sup3 if s is cramped, else sup1 if s = D, else sup2, d(x) + σ5/4)
L8  if there is no subscript then return z followed by x raised by u
L9  y ← the subscript set in sub(s), plus the script space; v ← max(v, sub2)
L10 c ← 4ξ8 − ((u − d(x)) − (h(y) − v))
L11 if c > 0 then v ← v + c; c ← 4σ5/5 − (u − d(x)); if c > 0 then u ← u + c; v ← v − c
L12 return z followed by x raised by u over y lowered by v

FRACTION(numerator, denominator, θ, style s)
L13 if θ is the default then θ ← ξ8
L14 x ← the numerator set in num(s); z ← the denominator set in denom(s); center the narrower one
L15 if s is D or D' then u ← num1; v ← denom1 else v ← denom2; u ← num2 if θ ≠ 0, else num3
L16 if θ = 0 then c ← 7ξ8 if s is D or D', else 3ξ8; δ ← half(c − ((u − d(x)) − (h(z) − v))); if δ > 0 then u ← u + δ; v ← v + δ
L17 else c ← 3θ if s is D or D', else θ; δ ← half(θ)
L18     δ1 ← c − ((u − d(x)) − (σ22 + δ)); if δ1 > 0 then u ← u + δ1
L19     δ2 ← c − ((σ22 − δ) − (h(z) − v)); if δ2 > 0 then v ← v + δ2
L20 return x raised by u, a rule of thickness θ on the axis, z lowered by v, with null delimiters on both sides
```

Line L2 hangs the scripts of a big nucleus, such as a fraction, from its top and bottom, instead of from the baseline. Lines L10 and L11 keep at least $4\xi_8$ between the superscript and the subscript, and they push the subscript down first, since a high superscript looks worse. Lines L18 and L19 keep a clearance between each part and the bar, and the bar is centered on the axis, so fractions line up with the minus sign and the plus sign. Here half$(x)$ is $x/2$ rounded up for odd $x$, as in TeX.

## Example

The font of this example is a toy font with made-up values in units of 0.1 point, loosely in the range of a 10 point font: x-height 43, `sup1` 41, `sup2` 36, `sup3` 29, `sub1` 15, `sub2` 25, $\xi_8 = 4$, and script space 5. The characters x, 1 and 2 have heights 43, 64 and 64 at text size, and the script size is 7/10 of that, so a script 1 or 2 has height 44.

| formula | style | first $u$, $v$ | gap $(u - d_x) - (h_y - v)$ | final $u$, $v$ |
|---|---|---|---|---|
| $x^2$ | $T$ | $u = \max(0, 36, 10) = 36$ | | 36 |
| $x^2$ | $T'$ | $u = 29$ (`sup3`) | | 29 |
| $x_1$ | $T$ | $v = \max(0, 15, 44 - 34) = 15$ | | 15 |
| $x_1^2$ | $T$ | 36, 25 | $36 - 19 = 17 \ge 16$ | 36, 25 |
| $x_1^2$ | $T'$ | 29, 25 | $29 - 19 = 10 < 16$ | 34, 26 |

In the last row, line L11 first moves the subscript down by 6, to $v = 31$. The bottom of the superscript is then at 29, below $4 \cdot 43 / 5 = 34$, so both scripts move up by 5: $u = 34$ and $v = 26$. The gap stays 16. In the text style $T$ the superscript is high enough already.

For $\frac{1}{2}$ in style $T$, with `num2` 39, `denom2` 34, axis height 25 and $\theta = 4$: the clearances to the bar are $(39 - 0) - (25 + 2) = 12$ and $(25 - 2) - (44 - 34) = 13$, both at least $\theta$, so $u = 39$ and $v = 34$, and the box has height $39 + 44 = 83$ and depth 34. In style $D$ the same fraction uses `num1` and `denom1` and its parts are set in $T$ and $T'$ at text size, so it is much taller.

## Correctness

The style formulas give the table of The TeXbook, which can be checked on all eight styles. The box of a script stack has height $h(x) + u$ and depth $d(y) + v$, because the kern between the scripts is chosen to make the gap exact; this is the box that TeX builds. Each correction step only adds to a gap: line L11 adds the missing amount to the gap between the scripts and then moves both scripts by the same amount, and lines L16, L18 and L19 add the missing amount (or twice half of it) to a gap to the bar. So the clearances hold at the end. The recursion is on proper subformulas, so it ends. The full proof is in the proof file below.

## Complexity

Each node is laid out once by its parent, with $O(1)$ work per fraction and per script node and $O(k)$ for a row of $k$ parts. So the time is $\Theta(n)$ for a formula with $n$ nodes. The extra space is the depth of the recursion, $O(n)$ in the worst case and the nesting depth of the formula in general.

## Properties

- **Bottom-up.** A part is set before its parent, so the parent knows its size.
- **Local.** The shifts of one node depend only on its parts and the font, not on the rest of the line. This is why a formula can be broken across lines only at its top level.
- **Driven by parameters.** The rules are fixed and a font designer tunes the layout through the parameters. The plain TeX values of `\scriptspace` and `\nulldelimiterspace` are design choices.
- **Three sizes only.** Scripts of scripts stay at scriptscript size, so deep nesting does not make text unreadably small.

## Variants and improvements

- **The full appendix G.** TeX also has rules for the spacing between atoms by class (ordinary, operator, binary, relation, and others), large operators with limits, radicals, accents, delimiters that grow with their content, and italic corrections. This page leaves them out.
- **The MATH table of OpenType.** OpenType fonts can carry a table of math constants and glyph variants that plays the role of the TeX parameters, so that systems such as LuaTeX, XeTeX and word processors can lay out math with any font that has it.
- **MathML.** Browsers that render MathML use layout rules that follow the same ideas: styles that shrink, shifts from font constants, and minimum gaps.

## When to use it

Use it to set formulas in a typesetting system, or to compute the size of a formula before you place it in a line. With an OpenType math font, read the parameters from its MATH table; with a TeX font, read them from the font metric files. For plain text with occasional exponents, the superscript feature of the font is simpler.

## Pitfalls

- **The size of the parameters.** Most parameters come from the size of the current style, but `sup_drop` and `sub_drop` come from the size of the scripts. Mixing them up moves scripts on fractions and parenthesized groups.
- **A character nucleus.** Scripts on a single character are placed from the baseline, not from its top and bottom; only a box nucleus uses the drops.
- **Cramped styles.** Forgetting to cramp the denominator and the subscripts makes exponents in denominators too high.
- **Rounding.** TeX computes in integer scaled points with its own half and div. Floating point can give results that differ from TeX by one unit.

## Implementations

## History

Knuth designed the math layout of TeX in the late 1970s and gave its final form in appendix G of The TeXbook in 1984, with the code in TeX, The Program in 1986. Later systems, among them the MATH table of OpenType and MathML renderers, kept the same scheme of styles, font parameters and clearances.

## References
