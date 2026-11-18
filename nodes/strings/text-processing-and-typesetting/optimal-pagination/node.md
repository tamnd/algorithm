---
tag: VBW9VJ
kind: algorithm
slug: optimal-pagination
name: Optimal pagination by dynamic programming
aliases:
- Plass optimal pagination
area: strings/text-processing-and-typesetting
level: advanced
summary: Choose all page breaks of a document at once by dynamic programming over break points, with figures placed in order on or after their first reference.
solves: [page-breaking-problem]
model: word-ram
complexity:
  vars: {n: the number of text lines, m: the number of figures}
  time: {worst: O(n^2 m^2)}
  space: {extra: Θ(n m)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1981
  people: [Michael F. Plass]
  note: Plass studied the optimal pagination of text with figures in his Stanford PhD thesis of 1981, and showed that some simple cost functions make the problem NP-complete.
prereqs: [page-breaking-problem, widows-and-orphans, dp-on-dag, prefix-sums]
see_also: [best-fit-page-breaking, pagination-np-completeness, knuth-plass-line-breaking, dag-shortest-paths, least-weight-subsequence, cut-and-paste-argument]
sources:
  - paper: "Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Department of Computer Science, Stanford University, 1981"
    title: Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Stanford University, 1981
    locator: the optimal pagination of text with figures, and the badness functions for which the problem is NP-complete
  - paper: doi:10.1002/spe.4380111102
    title: Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software, Practice and Experience 11(11), 1119-1184, 1981
    locator: the total-fit method for lines, which optimal pagination carries over to pages
---

Optimal pagination chooses all the page breaks of a document together, so that the sum of the costs of the pages is as small as possible. A page has a cost for its white space, for a bad break such as a widow line, and for each figure that floats away from the line that refers to it. When the text lines and the figures each keep their order, the state after a page is just the pair (lines placed, figures placed), and a shortest path over these pairs gives the optimum. This is the page version of the total-fit method of [Knuth-Plass line breaking](/knuth-plass-line-breaking/), and it can beat the [best-fit page builder](/best-fit-page-breaking/) of TeX, which fills one page at a time.

## In plain words

A book has lines of text and some figures. Each figure must come on the page where the text first mentions it, or on a later page. Each page has a fixed height.

We want pages that are well filled, with no bad breaks, and with each figure close to where it is mentioned. A choice that is good for one page can be bad for the next one, so we must look at all pages together.

After some pages are done, all that matters for the rest is how many lines and how many figures are used. So we find the best way to reach each such pair, from small pairs to large ones, as in a shortest path search.

## The problem

There are $n$ text lines with heights $h_1, \ldots, h_n$ and $m$ figures with heights $f_1, \ldots, f_m$, all $\ge 0$. Figure $t$ is referenced from line $r_t$, with $1 \le r_1 \le \cdots \le r_m \le n$. The page height is $H$. This page uses a simple model of the [page breaking problem](/page-breaking-problem/):

- A page holds a block of consecutive lines and a block of consecutive figures; one of the blocks can be empty, but not both. So the lines keep their order, and the figures keep their order.
- The total height $u$ of a page is at most $H$. There is no glue: the white space of a page is $H - u$.
- Figure $t$ is on the page of line $r_t$ or on a later page.

The cost of a pagination adds, for every page except the last one:

- $(H - u)^2$, the white space, squared;
- $\pi_i$ if the page holds lines and its last line $i$ is not line $n$; this is the cost of a break after line $i$, for example a [widow or club penalty](/widows-and-orphans/);
- $\alpha w$, where $w$ is the number of figures referenced on this page or earlier that are not placed yet, and $\alpha \ge 0$ is a weight.

The sum of the terms $w$ over all pages is the sum over the figures of the page of the figure minus the page of its reference. So the last term charges $\alpha$ for each page that a figure floats away from its reference. The last page is free, as in TeX, where it ends with glue that can stretch without limit.

## The algorithm

Let $R(i)$ be the number of figures referenced from lines $1, \ldots, i$. A state $(i, j)$ means that the first $i$ lines and the first $j$ figures are on finished pages. A page from $(i, j)$ to $(i', j')$ is allowed when it fits and $j' \le R(i')$: every figure on it is referenced on this page or earlier. Its cost depends only on $i$, $i'$, $j'$ and the height $u$, so it is an edge weight in a DAG over the states. Prefix sums of the heights give $u$ in $O(1)$ time.

```pseudo id=main
OPTIMAL-PAGES(h_1 .. h_n, f_1 .. f_m, r_1 .. r_m, H, α, π)
L1  C[0][0] ← 0; C[i][j] ← ∞ for every other state
L2  for i ← 0 to n do
L3      for j ← 0 to m do
L4          if C[i][j] = ∞ then continue
L5          for i' ← i to n, while the lines i+1 .. i' fit in H do
L6              for j' ← j to m, while j' ≤ R(i') and the page fits in H do
L7                  if (i', j') = (i, j) then continue
L8                  d ← C[i][j] + the cost of the page from (i, j) to (i', j'), or 0 if (i', j') = (n, m)
L9                  if d < C[i'][j'] then C[i'][j'] ← d; P[i'][j'] ← (i, j)
L10 if C[n][m] = ∞ then return failure
L11 follow P back from (n, m), and return C[n][m] and the states of the pages
```

Every page goes from a state to a state that is later in the lexicographic order, so lines L2 and L3 visit the states in a topological order. The loops of lines L5 and L6 stop early, because a longer block can only be taller and $R(i')$ is fixed for a fixed $i'$.

## Example

Take eight lines of height 1, one figure of height 3 referenced from line 4, page height $H = 5$, $\alpha = 5$ and no break penalties.

| pagination | page 1 | page 2 | page 3 | cost |
|---|---|---|---|---|
| fill each page | lines 1 to 5 | figure, lines 6 and 7 | line 8 | $0 + 5 = 5$ |
| optimal | lines 1 to 3 | lines 4 and 5, figure | lines 6 to 8 | $2^2 = 4$ |
| | lines 1 to 4 | figure, line 5 ... | | $1 + 5 = 6$ or more |

Filling each page puts lines 1 to 5 on page 1. The figure is referenced there, does not fit, and floats to page 2, which costs $\alpha = 5$. The optimum leaves two units of white space on page 1, which costs 4, so that line 4 starts page 2 and the figure sits on the same page as its reference. The DP finds this, and a search over all paginations confirms it.

## Correctness

Two facts make the DP exact. First, the condition that each figure comes on or after the page of its reference can be checked page by page: it holds exactly when $j' \le R(i')$ after each page. Second, the cost splits over the pages: a figure that floats $d$ pages from its reference is counted once at each of the $d$ page breaks between them, and at each break the number of such figures is $R(i') - j'$. So the valid paginations are the paths from $(0, 0)$ to $(n, m)$ in a DAG, the cost of a pagination is the weight of its path, and the DP is a [shortest path in a DAG](/dag-shortest-paths/). An optimal pagination to a state can be cut and pasted into any optimal pagination through it (the [cut-and-paste argument](/cut-and-paste-argument/)). The full proof is in the proof file below.

## Complexity

There are $(n + 1)(m + 1)$ states, each with at most $(n + 1)(m + 1)$ pages leaving it, and each page costs $O(1)$ time. So the time is $O(n^2 m^2)$ and the extra space is $\Theta(n m)$ for the table and the links. If a page holds at most $a$ lines and $b$ figures, as when every height is at least 1, the time is $O(n m a b)$, which is linear in $n m$ for a fixed page size. When $m = 0$, the method is a [least weight subsequence](/least-weight-subsequence/) problem over the lines, in $O(n a)$ time.

## Properties

- **Exact for its model.** It returns a pagination of least total cost among the valid ones.
- **Offline.** It needs the whole document before it can fix the first page, unlike the page builder of TeX.
- **The model matters.** The DP works because the lines and the figures each keep their order and the cost splits over page breaks. If figures can change order, the problem is NP-complete; see [the NP-completeness of pagination](/pagination-np-completeness/).
- **Ties.** Line L9 keeps the first best path found, so the result is deterministic.

## Variants and improvements

- **Page-dependent costs.** If the cost of a page depends on its page number (for example, a figure must be on the same spread, so odd and even pages differ), the state needs the page number too, $(i, j, k)$, and the time grows by a factor of the number of pages.
- **Other figure costs.** A cost that is a convex function of the distance, such as its square, does not split over page breaks with the state $(i, j)$ alone, so it needs a larger state or another method.
- **Glue between lines.** With stretchable glue between the lines, the white space term becomes the [badness](/typesetting-badness/) of the page, as in the TeX cost, and the DP is the same.
- **Several kinds of floats.** With figures and tables in two separate streams, the state is a triple, one count per stream.

## When to use it

Use it when the whole document is known and page quality matters: books with many figures, reports with tables, documents for print. For long documents where the first pages must come out before the rest is known, or where the layout changes often, the [best-fit page builder](/best-fit-page-breaking/) is cheaper.

## Pitfalls

- **The last page.** The last page must be free, or the DP will try to fill it. A cost for its white space is a common error.
- **Figures before their reference.** The test $j' \le R(i')$ uses the last line of the new page, not the first line.
- **A figure term that does not split.** Summing a convex function of the distance does not fit the state $(i, j)$, and a DP that does it anyway is not exact.
- **Equal references.** Two figures referenced from the same line must still keep their order; sort them by number, not by height.

## Implementations

## History

Michael Plass, a student of Donald Knuth, studied the pagination of text with figures in his Stanford PhD thesis of 1981. He showed that the problem is NP-complete for two simple badness functions, so a fast exact method needs a restricted model such as the one on this page. In the same year, Knuth and Plass published the total-fit method for lines, which this method carries over to pages. TeX itself kept the simpler [best-fit page builder](/best-fit-page-breaking/).

## References
