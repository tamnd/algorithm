---
tag: XDPBX8
kind: definition
slug: widows-and-orphans
name: Widows and orphans
aliases:
- widow and orphan lines
area: strings/text-processing-and-typesetting
level: intro
summary: "Lines of a paragraph left alone by a page break: the last line at the top of a page and the first line at the bottom. Names vary; TeX calls the first line a club line."
prereqs: [box-glue-penalty-model]
see_also: [page-breaking-problem, best-fit-page-breaking, optimal-pagination, knuth-plass-line-breaking, greedy-line-breaking]
sources:
  - book: isbn:9780201134476
    title: Donald E. Knuth, The TeXbook, Addison-Wesley, 1984
    locator: the parameters \clubpenalty, \widowpenalty, \displaywidowpenalty and \brokenpenalty, and their values in the plain format of appendix B
  - book: isbn:9780201134377
    title: Donald E. Knuth, TeX, The Program, Addison-Wesley, 1986
    locator: part 39, Breaking paragraphs into lines, continued (the penalty put between two lines of a paragraph)
  - url: https://drafts.csswg.org/css-break-3/
    title: CSS Fragmentation Module Level 3, W3C
    locator: "section 3.3, Breaks Between Lines: orphans, widows"
---

Widows and orphans are lines of a paragraph that a page break leaves alone: the last line of a paragraph at the top of a new page, or the first line of a paragraph at the bottom of a page. Both look bad, because the eye loses the paragraph at the break. Page breaking methods avoid them with a penalty on the breaks that make them, or with a hard rule on the number of lines that must stay together. The names are not used the same way in all style guides, so a program should state which line it means.

## Definition

Take a paragraph of $\ell \ge 2$ lines, numbered $1, \ldots, \ell$, and a page break between line $i$ and line $i + 1$, with $1 \le i < \ell$.

- The break leaves a **widow** when $i = \ell - 1$: the last line of the paragraph is alone at the top of the next page. This is the common meaning in typography, in TeX (the `\widowpenalty`) and in CSS.
- The break leaves an **orphan** when $i = 1$: the first line of the paragraph is alone at the bottom of the page. TeX calls this line a **club line** and its penalty `\clubpenalty`; CSS calls it an orphan.

Some guides swap the two words, and some use "widow" for a very short last line of a paragraph (one word alone on its line, also called a runt), with no page break at all. The definitions above are the ones used on this site.

**The rule with $k$ lines.** CSS generalizes the idea: the property `orphans` is the least number of lines of a block that must stay on a page before a break, and `widows` is the least number that must go to the next page. Both have the initial value 2. A break after line $i$ is allowed only if $i \ge$ `orphans` and $\ell - i \ge$ `widows`. With both values 2, this forbids exactly the breaks after line 1 and after line $\ell - 1$.

**The penalty model.** TeX puts a penalty between each pair of lines of a paragraph, in the [box, glue and penalty model](/box-glue-penalty-model/). The penalty after line $i$ is `\interlinepenalty`, plus `\clubpenalty` if $i = 1$, plus `\widowpenalty` if $i = \ell - 1$ (or `\displaywidowpenalty` if the paragraph goes on after a display), plus `\brokenpenalty` if line $i$ ends with a hyphen. A one-line paragraph gets none of these. Plain TeX sets `\clubpenalty=150`, `\widowpenalty=150`, `\displaywidowpenalty=50`, `\brokenpenalty=100` and `\interlinepenalty=0`; these are design choices, not results. A value of 10000 forbids the break, which gives the hard rule.

## Examples and non-examples

- A paragraph of five lines broken after line 4: line 5 starts the next page alone. This is a widow. In plain TeX the break costs 150 more than a break in the middle of the paragraph.
- The same paragraph broken after line 1: line 1 ends the page alone. This is an orphan, or a club line in TeX.
- Broken after line 2 or line 3: neither. At least two lines stay on each side.
- A two-line paragraph broken after line 1: $i = 1$ and $i = \ell - 1$, so the break makes both, and TeX adds both penalties, $150 + 150 = 300$.
- A paragraph whose last line holds one short word, with no page break: not a widow in the sense of this page, though some guides call it one.
- A heading at the bottom of a page with its text on the next page: not a widow or an orphan, but a similar fault. TeX and CSS handle it with a penalty or a rule that keeps the heading with the next line.

## Related definitions

- The [page breaking problem](/page-breaking-problem/) uses these penalties as part of the cost of a page break.
- The [best-fit page builder](/best-fit-page-breaking/) of TeX adds the penalty at a break to the badness of the page, and [optimal pagination](/optimal-pagination/) adds it to the total cost.
- In line breaking, the same model of penalties marks hyphens and forbidden breaks; see [Knuth-Plass line breaking](/knuth-plass-line-breaking/).

## References
