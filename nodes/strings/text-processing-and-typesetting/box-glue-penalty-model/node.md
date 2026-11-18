---
tag: FHCB1D
kind: model
slug: box-glue-penalty-model
name: Box, glue and penalty model
aliases:
- boxes and glue
area: strings/text-processing-and-typesetting
level: core
summary: A paragraph as a sequence of rigid boxes, stretchable and shrinkable glue, and penalties that mark optional breaks, used by optimal line breaking.
prereqs: [prefix-sums]
see_also: [knuth-plass-line-breaking, greedy-line-breaking, typesetting-badness, least-weight-subsequence, printing-neatly, best-fit-page-breaking, unicode-line-breaking-algorithm, hyphenation-problem]
sources:
  - paper: doi:10.1002/spe.4380111102
    title: "Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software: Practice and Experience 11(11), 1119-1184, 1981"
    locator: "the definition of boxes, glue and penalties, the legal breakpoints, the adjustment ratio, badness and demerits, and the encodings of ragged-right and centered text"
  - book: isbn:1575860104
    title: "Donald E. Knuth, Digital Typography, CSLI Publications, 1999"
    locator: "Chapter 3, the reprint of Breaking paragraphs into lines"
  - book: isbn:0201134470
    title: "Donald E. Knuth, The TeXbook, Computers and Typesetting volume A, Addison-Wesley"
    locator: "Chapter 12 (glue and its infinite orders), Chapter 14 (how TeX breaks paragraphs into lines) and Chapter 15 (how TeX makes lines into pages)"
  - book: isbn:0201134373
    title: "Donald E. Knuth, TeX: The Program, Computers and Typesetting volume B, Addison-Wesley, 1986"
    locator: "the parts on the badness function, the line breaker and the page builder"
---

The box, glue and penalty model describes a paragraph as a sequence of three kinds of items. A *box* is something rigid with a width, such as a letter or a word. *Glue* is a space with a natural width that can stretch and shrink by given amounts. A *penalty* is a place where a line may end, with a cost for ending there. A choice of breaks cuts the sequence into lines, each line is set to its length by stretching or shrinking its glue, and the model gives each choice a cost from how far the glue moved and which penalties were used. Donald Knuth and Michael Plass defined it in 1981 for TeX, and the same items describe a page as a vertical sequence of lines and spaces. Line breaking and page breaking in this model are optimization problems, so the model is a machine for algorithms rather than an algorithm.

## The machine

**Items.** A paragraph is a sequence $x_0, \ldots, x_{m-1}$. Each item is one of:

- a box with width $w_i$;
- a glue with natural width $w_i$, stretchability $y_i \ge 0$ and shrinkability $z_i \ge 0$;
- a penalty with width $w_i$, cost $p_i$ and a flag $f_i$ (set for a hyphen).

A penalty $p_i \ge 10000$ forbids a break and $p_i \le -10000$ forces one; TeX treats 10000 as infinity. The stretch and shrink of a glue can also be infinite, in one of three orders (fil, fill and filll in TeX), where any amount of a higher order hides all amounts of the lower orders.

**Legal breakpoints.** A line may end only at:

- a penalty $x_b$ with $p_b < 10000$;
- a glue $x_b$ that directly follows a box.

So a break is never inside a box, and a space made of several glues breaks only at its first one. A *breaking* is a sequence of legal breakpoints $b_1 < \cdots < b_k = m - 1$ that holds every forced break.

**Lines.** The line from a break $a$ to the next break $b$ holds the items after $a$ and before $b$, except that the glue and penalties right after $a$, before the first box, are discarded. A glue at a break disappears; a penalty at a break adds its width $w_b$ to the line, which is the width of the hyphen. Line $j$ has a length $l_j$; usually all lengths are the same, but they can change, for example around a figure.

**Setting a line.** The line has natural width $L$ (the sum of the widths of its boxes and glues, plus $w_b$ at a penalty), total stretch $Y$ and total shrink $Z$. If $L < l$, each glue $i$ gets the width $w_i + r y_i$ with $r = (l - L)/Y$; if $L > l$, it gets $w_i + r z_i$ with $r = (l - L)/Z$, which is negative. The number $r$ is the adjustment ratio. The glue may not shrink below $w_i - z_i$, so $r < -1$ means the line is overfull and does not fit. When $Y$ or $Z$ has a part of an infinite order, only the glue of the highest order present moves, and the other glue keeps its natural width.

**Cost of a line.** With prefix sums of the widths, stretches and shrinks, each line is measured in $O(1)$ time after $O(m)$ work, for any pair of breaks.

**The ending of a paragraph.** TeX ends each paragraph with a penalty 10000 (no break), a glue of width 0 with stretch 1fil (\parfillskip) and a forced penalty $-10000$. The last line can then be short: the fil glue takes all the space, and its badness is 0.

**Encodings.** Many layouts are sequences of these items:

- *Justified text.* A box per word, an interword glue between words, and a flagged penalty at each hyphenation point, with the width of the hyphen and a cost (\hyphenpenalty, 50 in plain TeX). The points come from a method for the [hyphenation problem](/hyphenation-problem/).
- *Ragged right.* Between words put a glue of width 0 and stretch $S$, a penalty 0, and a glue of width $w$ and stretch $-S$. If the line ends at the penalty, the first glue stays at the end of the line and the next two items are discarded, so the line has stretch $S$ at its end. If it does not, the two glues are both in the line, their stretch cancels, and the space has the fixed width $w$. So the spaces in a line stay equal and only the right margin moves. Knuth and Plass give this and an encoding for centered lines.
- *Pages.* A vertical list holds the lines as boxes (their size is height plus depth), the glue between lines and paragraphs, and penalties such as \clubpenalty and \widowpenalty (150 in plain TeX), which make a break after the first line or before the last line of a paragraph cost more ([widows and orphans](/widows-and-orphans/)).

**Example of setting a line.** Take the words "glue can stretch" as boxes of widths 4, 3 and 7, with two glues of width 2, stretch 1 and shrink 1, and the length $l = 19$. Then $L = 14 + 4 = 18$, $Y = 2$ and $r = (19 - 18)/2 = 1/2$, so each glue is set to width 2.5. With $l = 17$, $r = (17 - 18)/2 = -1/2$ and each glue gets width 1.5. With $l = 15$, $r = -3/2 < -1$: the line is overfull.

## What it counts

**Badness.** The cost of a line is a function of $r$, its [badness](/typesetting-badness/), about $100 |r|^3$ and at most 10000. The cube makes small changes cheap and large ones very expensive. In the example above, $r = 1/2$ gives badness 12.5 in the real form and 12 in the integer form that TeX computes. An overfull line has no finite badness and is not allowed, except as a last resort.

**Feasible lines.** A line is feasible when $r \ge -1$ and its badness is at most a tolerance $\rho$. TeX first tries the paragraph without hyphenation, with the tolerance \pretolerance (100 in plain TeX), and if that fails, it tries again with hyphenation and \tolerance (200 in plain TeX).

**Demerits.** The cost of a breaking is the sum of the demerits of its lines. A line with badness $\beta$ that ends at a penalty $p$ gets about $(\lambda + \beta)^2 + p^2$, where $\lambda$ is the line penalty (\linepenalty, 10 in plain TeX), with extra demerits for two hyphens in a row (\doublehyphendemerits, 10000), for a hyphen in the last full line (\finalhyphendemerits, 5000) and for a tight line next to a loose one (\adjdemerits, 10000). The exact formula is on the page on the [Knuth-Plass algorithm](/knuth-plass-line-breaking/). These numbers are design choices of plain TeX, not results, and other values give other layouts.

**Pages.** For a vertical list, the page builder of TeX computes a badness for a page from its glue in the same way, and adds the penalty at the break and the costs of insertions such as footnotes. It chooses the break of least cost seen so far, which is [best-fit page breaking](/best-fit-page-breaking/), not a total optimum.

**Cost of the computation.** The time of a line breaking method is counted in line measurements and comparisons in the [word RAM](/word-ram/), where each measurement costs $O(1)$ by prefix sums. A paragraph with $q$ optional breakpoints has $2^q$ breakings, so a method must not look at all of them.

## Relation to other models

- **Fixed-width text.** [Printing neatly](/printing-neatly/) is the special case with words as boxes, rigid spaces ($y_i = z_i = 0$), no hyphens and a cost that depends only on the empty space at the end of each line. It is the ragged-right encoding with the cost of a line set to the cube of its slack.
- **Least weight subsequence.** If the cost of a line depends only on its two breaks, the best breaking is a [least weight subsequence](/least-weight-subsequence/) problem over the legal breakpoints, which is a shortest path in a DAG ([DP on a DAG](/dp-on-dag/)). The flags and the classes of tight and loose lines in the demerits of TeX depend on the line before, so the full model needs a state per break and does not fit this problem directly.
- **Break opportunities.** The [Unicode line breaking algorithm](/unicode-line-breaking-algorithm/) decides where a break is allowed in text of any script. It gives the legal breakpoints, which can become penalties of this model, but it gives no cost.
- **Pages and paragraphs.** The vertical list uses the same items, and the [page breaking problem](/page-breaking-problem/) and [optimal pagination](/optimal-pagination/) ask the same question for pages that line breaking asks for lines.

## Known results in the model

- **Total fit.** The [Knuth-Plass algorithm](/knuth-plass-line-breaking/) finds a breaking of least total demerits with all lines feasible, in $O(m A)$ time for $A$ active breakpoints, by dynamic programming over the breaks.
- **First fit.** [Greedy line breaking](/greedy-line-breaking/) ends each line at the farthest break that fits. With rigid spaces, or spaces that can only shrink, it gives the fewest lines. With stretchable spaces it can make a line that must stretch far, even when a breaking with all lines within the tolerance exists.
- **Fast methods for simple costs.** When the cost of a line is a convex function of its natural width $S_b - S_a$ alone, the weight satisfies the quadrangle inequality, and the [Hirschberg-Larmore algorithm](/hirschberg-larmore-algorithm/) ($O(m \log m)$) and [Wilber's algorithm](/wilber-algorithm/) ($O(m)$) apply.
- **Integer badness.** TeX computes the badness in integers from the amount $t$ to stretch or shrink and the total $s$, with results such as badness 4 for $t/s = 1/3$, where the real form gives 3.70.
- **Pages.** TeX breaks pages by best fit, and optimal page breaking with floats and footnotes is studied as [optimal pagination](/optimal-pagination/).

### Pitfalls

- **Counting the glue at a break.** The glue at a break belongs to no line, and the glue and penalties after a break are discarded up to the next box. Counting them gives wrong widths.
- **Infinite shrink.** A glue with infinite shrink lets a line be as short as needed, so no line is ever overfull. TeX reports it as an error in a paragraph.
- **Treating 10000 as a number.** A penalty of 10000 means "never" and $-10000$ means "always". A program that adds them like other costs gets lines that should not exist.
- **Breaking at glue after glue.** Only a glue that follows a box is a legal break. Allowing a break at a later glue of a space gives lines that start with a space.

## References
