---
tag: E0N3BW
kind: problem
slug: page-breaking-problem
name: Page breaking
aliases:
- pagination problem
area: strings/text-processing-and-typesetting
level: core
summary: Split a sequence of lines, figures and footnotes into pages to minimize a cost of underfull pages, widows, orphans and distance from figure references.
model: word-ram
complexity:
  vars: {n: the number of lines, k: the largest number of lines on one page}
  time: {worst: O(n k)}
prereqs: [widows-and-orphans, box-glue-penalty-model, typesetting-badness, least-weight-subsequence]
see_also: [best-fit-page-breaking, optimal-pagination, pagination-np-completeness, knuth-plass-line-breaking, greedy-line-breaking, printing-neatly, dp-on-dag, table-layout-problem]
sources:
  - book: isbn:9780201134476
    title: Donald E. Knuth, The TeXbook, Addison-Wesley, 1984
    locator: the chapter on how TeX makes lines into pages (the page builder, \vsize, insertions and the cost of a page break)
  - paper: "Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Department of Computer Science, Stanford University, 1981"
    title: Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Stanford University, 1981
    locator: the models of pagination with text and figures, and the badness functions for which the problem is NP-complete
  - url: https://drafts.csswg.org/css-break-3/
    title: CSS Fragmentation Module Level 3, W3C
    locator: "section 3.3, Breaks Between Lines: orphans, widows"
---

Page breaking is the problem of splitting a document, already broken into lines, into pages of a fixed height. A good split fills each page, avoids [widow and orphan lines](/widows-and-orphans/), and puts each figure and footnote near the line that refers to it. With text only, the problem is a shortest path over the possible breaks and dynamic programming solves it fast; with figures that keep their order it is still polynomial, and with figures that may change order it becomes NP-complete.

## In plain words

A long text is first cut into lines. Then the lines must go onto pages, and each page has room for only so many lines.

A page that is half empty looks bad. A paragraph that leaves one line alone at the top or the bottom of a page looks bad too. A picture should be close to the text that talks about it.

So each way to cut the pages gets a score, and we want the cut with the best total score. Filling each page as much as we can is simple, but it can force a bad page later.

## Definition

**Input.** A sequence of items $x_1, \ldots, x_n$, each a line with a height, the possible break points between them, a cost $\pi_i$ for a break after item $i$, and a page height $H$. Optionally, a set of figures (or footnotes), each with a height and the index of the line that refers to it.

**Output.** A pagination: a sequence of pages that holds every line and every figure once, with the lines in their order, where the content of each page fits in $H$ and each figure is on the page of its reference or later.

**Objective.** Minimize the total cost: the sum over the pages of a cost for the white space of the page (for example $(H - u)^2$ for a page of height $u$, or the [badness](/typesetting-badness/) of the stretch or shrink of its glue), plus the break costs $\pi_i$ of the breaks used, plus a cost for each figure that grows with its distance from its reference. The last page is often free, since it can end with white space.

With text only and a cost that is a sum of page costs, where the cost of a page depends only on its first and last line, this is a [least-weight subsequence](/least-weight-subsequence/) problem over the break points.

## Variants

- **Text only.** The pages hold consecutive blocks of lines. This is the problem that [Knuth-Plass line breaking](/knuth-plass-line-breaking/) solves for lines, with lines in place of words and pages in place of lines.
- **Online, one page at a time.** The program must decide each page before it sees the text after the next break. TeX works this way, with its [best-fit page builder](/best-fit-page-breaking/), so it needs to keep only the current page in memory.
- **Figures in order.** Figures float, but each keeps its order relative to the other figures, as the floats of LaTeX do within a class. [Optimal pagination](/optimal-pagination/) solves this by dynamic programming.
- **Figures in any order.** The figures may be placed in any order. The problem is then [NP-complete](/pagination-np-completeness/), even with very simple costs.
- **Footnotes.** A footnote must start on the page of its reference, and a long footnote may be split and continued on the next page. TeX handles both with insertions.
- **Hard rules.** Systems such as CSS give a minimum number of lines that must stay before and after a break (the `orphans` and `widows` properties), and forbid breaks inside some boxes, instead of costs.
- **Facing pages.** Two pages that face each other should end at the same height, which links the breaks of neighboring pages.

## Examples

**A widow.** One paragraph of 5 lines of height 1, $H = 4$, a page cost of $(H - u)^2$ on each page but the last, and a widow penalty of 150 for the break after line 4. Filling the first page gives pages of 4 and 1 lines, with cost $0 + 150 = 150$. Pages of 3 and 2 lines cost $(4 - 3)^2 = 1$, so they are optimal.

**A figure.** Eight lines of height 1, a figure of height 3 referenced from line 4, $H = 5$, and a cost of 5 for each page that the figure floats away from its reference. Filling page 1 with lines 1 to 5 leaves no room for the figure, so it goes to page 2 with lines 6 and 7, and the cost is 5. Putting only lines 1 to 3 on page 1 (white space 2, cost 4) and lines 4 and 5 with the figure on page 2 costs 4, which is optimal. The [optimal pagination](/optimal-pagination/) page works this example in full.

## Known algorithms

| algorithm | model | time | result |
|---|---|---|---|
| fill each page (first fit) | text and figures | $O(n + m)$ | fast, can be far from optimal |
| [best-fit page builder](/best-fit-page-breaking/) of TeX | text, glue, penalties, insertions | $O(n k)$ | best break for each page alone |
| dynamic programming over break points | text only | $O(n k)$ | optimal |
| [optimal pagination](/optimal-pagination/) | text and $m$ figures in order | $O(n^2 m^2)$ | optimal |

Here $k$ is the largest number of lines on a page, so $k \le n$. The dynamic program over break points computes, for each break $j$, the least cost of the pages that end at $j$, from the at most $k$ breaks $i$ such that lines $i + 1$ to $j$ fit on one page; it is a [shortest path in a DAG](/dag-shortest-paths/). [Prefix sums](/prefix-sums/) of the heights give the height of each candidate page in $O(1)$ time.

## Bounds

- Text only: $O(n k)$ time by dynamic programming, and $\Omega(n)$ since every line must be read.
- Figures in order: polynomial, $O(n^2 m^2)$ with the simple model of the optimal pagination page.
- Figures in any order: strongly NP-complete for the total distance from figures to their references, by a reduction from 3-partition; see [the NP-completeness of pagination](/pagination-np-completeness/). So no polynomial algorithm is expected, and no pseudo-polynomial algorithm either, unless P = NP.
- A one-page-at-a-time method cannot be optimal in general: the best-fit page builder pays 360 where the optimum pays 30 on the example of its page.

## Reductions

- Text-only page breaking is a least-weight subsequence problem, the same as optimal line breaking and [printing neatly](/printing-neatly/).
- 3-partition reduces to pagination with figures in any order: the figures play the numbers and the pages play the bins, as in the proof of [bin packing hardness](/bin-packing-np-hardness/).
- Laying out each page is itself a small packing problem when a page holds several floats or columns; the [table layout problem](/table-layout-problem/) is a related layout problem that is NP-complete.

## Applications

- TeX and LaTeX break pages with the best-fit page builder, and LaTeX places floats by rules on top of it.
- Browsers and e-book readers break pages and columns by the rules of CSS Fragmentation, with the `orphans` and `widows` properties.
- Word processors and desktop publishing programs break pages with widow and orphan control and keep-with-next rules.
- Batch systems for books and documentation use optimal methods, since they can see the whole document.

## References
