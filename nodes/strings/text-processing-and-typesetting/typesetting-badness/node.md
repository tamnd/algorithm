---
tag: 4N5WKK
kind: definition
slug: typesetting-badness
name: Badness of a line
aliases:
- adjustment ratio
- line badness
area: strings/text-processing-and-typesetting
level: core
summary: A measure of how far a line's glue must stretch or shrink, about 100 times the cube of the adjustment ratio, used in the cost of a line break.
prereqs: [box-glue-penalty-model]
see_also: [knuth-plass-line-breaking, greedy-line-breaking, printing-neatly, best-fit-page-breaking, least-weight-subsequence, convex-function]
sources:
  - paper: doi:10.1002/spe.4380111102
    title: "Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software: Practice and Experience 11(11), 1119-1184, 1981"
    locator: "the definition of the adjustment ratio, the badness 100 |r|^3, feasible lines and fitness classes"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Chapter 14, How TeX breaks paragraphs into lines (badness, tolerance and demerits)"
  - book: isbn:0201134373
    title: "Donald E. Knuth, TeX: The Program, Computers and Typesetting volume B, Addison-Wesley, 1986"
    locator: "the badness function in the part on basic arithmetic, and its use in the line breaker"
---

The badness of a line tells how much the spaces of a justified line must change from their natural widths to make the line exactly as long as the column. It is about 100 times the cube of the ratio of the change to the amount the spaces can change, and it is capped at 10000. A line set at its natural width has badness 0, a line whose spaces stretch or shrink by their full allowed amount has badness 100, and a line whose spaces would have to shrink more than allowed has no finite badness. Knuth and Plass defined it for TeX, where it is the main part of the cost of a line in [Knuth-Plass line breaking](/knuth-plass-line-breaking/).

## Definition

Work in the [box, glue and penalty model](/box-glue-penalty-model/). A line has a natural width $L$, a total stretchability $Y$ and a total shrinkability $Z$ (sums over its glue), and it must be set to the length $l$. Its adjustment ratio is

$$r = \frac{l - L}{Y} \text{ if } L < l, \qquad r = \frac{l - L}{Z} \text{ if } L > l, \qquad r = 0 \text{ if } L = l,$$

with $r = \infty$ when $L < l$ and $Y = 0$, and $r = -\infty$ when $L > l$ and $Z = 0$. Each glue $i$ is then set to width $w_i + r y_i$ (if $r \ge 0$) or $w_i + r z_i$ (if $r < 0$).

**Real badness.** The badness of the line is

$$\beta(r) = \begin{cases} \min(100 |r|^3, 10000) & \text{if } r \ge -1, \\ \infty & \text{if } r < -1 \text{ (the line is overfull).} \end{cases}$$

If the line stretches or shrinks glue of an infinite order (fil, fill or filll), only that glue moves and $\beta = 0$.

**The integer badness of TeX.** TeX computes the badness in integers, from the amount $t \ge 0$ that the line must stretch or shrink and the total $s$ of the stretch or shrink, both in scaled points (units of $2^{-16}$ point):

- $\mathrm{badness}(0, s) = 0$, and $\mathrm{badness}(t, s) = 10000$ if $t > 0$ and $s \le 0$;
- otherwise let $q = \lfloor 297 t / s \rfloor$ (TeX uses another order of operations for very large $t$, to avoid an overflow);
- if $q > 1290$ the badness is 10000, else it is $\lfloor (q^3 + 2^{17}) / 2^{18} \rfloor$.

Since $297^3 \approx 100 \cdot 2^{18}$, this is $100 (t/s)^3$ rounded, with an error of a few units. The value 10000 means "infinitely bad", and the line breaker gives an overfull line a value above it, so it loses to every line that fits.

A line is *feasible* for a tolerance $\rho$ when $r \ge -1$ and $\beta \le \rho$.

## Examples and non-examples

| $t/s$ | real badness | TeX badness | note |
|---|---|---|---|
| 0 | 0 | 0 | natural width |
| 1/3 | 3.70 | 4 | $\mathrm{badness}(1, 3)$ |
| 3/10 | 2.7 | 3 | $\mathrm{badness}(3, 10)$ |
| 1/2 | 12.5 | 12 | $\mathrm{badness}(1, 2)$ |
| 1 | 100 | 100 | full stretch or full shrink |
| 2 | 800 | 800 | $\mathrm{badness}(2, 1)$; only for stretch, since shrink stops at 1 |
| 3 | 2700 | 2698 | |
| 9/2 | 9112.5 | 10000 | TeX caps already above $q = 1290$ |

- **Stretch and shrink are symmetric.** A line 1 unit too long with shrink 3 and a line 1 unit too short with stretch 3 both have $r = \pm 1/3$ and badness 3.70 (4 in TeX).
- **The cap in TeX comes early.** The largest finite value of the integer form is 8189, at $q = 1290$, that is $t/s$ just under 4.35. From there on TeX gives 10000, while the real form reaches 10000 only at $t/s = 10^{2/3} \approx 4.64$. So the two forms can disagree on which of two very loose lines is worse.
- **A line that cannot stretch.** A line with one word and no glue, shorter than $l$, has $Y = 0$, so $r = \infty$ and the badness is 10000. In TeX it is an underfull box. It is still allowed if the tolerance is 10000.
- **A line that is too long.** A line with $L = 20$, $Z = 3$ and $l = 15$ has $r = -5/3 < -1$. It is overfull, and its badness is not 10000 but infinite: no tolerance makes it feasible.
- **The last line.** The last line of a TeX paragraph holds the glue \parfillskip with stretch 1fil, so its badness is 0 however short it is.
- **Not the adjustment ratio.** The ratio $r$ and the badness are different numbers: $r = 1/2$ gives badness 12.5. The badness is a cubic function of $r$, so it grows slowly near 0 and fast beyond 1.
- **Not the slack.** The cost of [printing neatly](/printing-neatly/) is the cube of the empty space at the end of a line, which does not depend on the number of spaces. The badness divides by the stretch first, so the same empty space costs less in a line with more spaces.

## Related definitions

- **Adjustment ratio.** The number $r$ above; it gives the widths of the glue.
- **Demerits.** The cost of a line in the Knuth-Plass algorithm, about $(\lambda + \beta)^2 + p^2$ for the line penalty $\lambda$ and the penalty $p$ at the break, with extra terms for hyphens and fitness classes. The square of the badness makes one very bad line cost more than several slightly bad ones.
- **Fitness class.** Knuth and Plass put a line into one of four classes by $r$: tight ($r < -1/2$), decent ($-1/2 \le r \le 1/2$), loose ($1/2 < r \le 1$) and very loose ($r > 1$). The bounds $1/2$ and $1$ are the badness values 12.5 and 100, and TeX tests its integer badness against 12 and 99.
- **Tolerance.** The largest badness of a feasible line; plain TeX uses 100 for its first try without hyphens (\pretolerance) and 200 for the second (\tolerance).
- **Page badness.** The page builder of TeX uses the same function for the glue of a page, as in [best-fit page breaking](/best-fit-page-breaking/).
- **Line cost in least weight subsequence.** With rigid spaces and a cost that is a [convex function](/convex-function/) of the width of the line, line breaking is a [least weight subsequence](/least-weight-subsequence/) problem with the quadrangle inequality. The badness is not of this form, because it divides by the stretch of the line, which changes from line to line.

## References
