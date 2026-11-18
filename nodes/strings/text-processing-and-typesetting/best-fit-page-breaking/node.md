---
tag: 81895S
kind: algorithm
slug: best-fit-page-breaking
name: Best-fit page breaking
aliases:
- TeX page builder
area: strings/text-processing-and-typesetting
level: core
summary: Add lines to the current page and break at the feasible break of least cost seen before the page overflows, without looking ahead.
solves: [page-breaking-problem]
model: word-ram
complexity:
  vars: {m: the number of items of the vertical list, k: the largest number of items scanned for one page}
  time: {worst: O(m k), best: Θ(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1984
  people: [Donald E. Knuth]
  note: Knuth described the page builder of TeX and its cost of a page break in The TeXbook in 1984, and gave its full code in TeX, The Program in 1986.
prereqs: [page-breaking-problem, widows-and-orphans, box-glue-penalty-model, typesetting-badness]
see_also: [optimal-pagination, greedy-line-breaking, knuth-plass-line-breaking, pagination-np-completeness, least-weight-subsequence, greedy-stays-ahead]
sources:
  - book: isbn:9780201134476
    title: Donald E. Knuth, The TeXbook, Addison-Wesley, 1984
    locator: "chapter 15, How TeX makes lines into pages: the page goal, the cost of a page break and the choice of the best break so far"
  - book: isbn:9780201134377
    title: Donald E. Knuth, TeX, The Program, Addison-Wesley, 1986
    locator: part 45, The page builder
---

Best-fit page breaking is the method that TeX uses to divide a long vertical list of lines into pages. It fills one page at a time: it moves lines onto the current page, gives each possible break a cost from how much the page must stretch or shrink and from the penalty at the break, and keeps the break of least cost seen so far. When the page is too full to take more, or a break is forced, it ends the page at the best break and starts the next page there. It never looks at later pages, so it is fast and simple, but it does not always find the breaking of least total cost; [optimal pagination](/optimal-pagination/) does that with dynamic programming.

## In plain words

Think of a person who fills pages with lines of text. They put lines on the page one by one. After each line, they ask: if the page ended here, how bad would it look? A page that is too empty must spread its lines apart, and some places are bad for a break, for example after the first line of a paragraph.

They remember the best place so far. When the next line does not fit at all, they cut the page at the best place they remember, and they start the next page with the lines after it.

They never think about the pages that come later. Sometimes a good cut now forces a bad page later.

## The problem

The input is a vertical list $x_0, \ldots, x_{m-1}$ in the [box, glue and penalty model](/box-glue-penalty-model/), as in the [page breaking problem](/page-breaking-problem/):

- a **box** is a line (or a display, a figure, a heading) of height $h \ge 0$ and depth $d \ge 0$;
- a **glue** is a space between lines of natural size $w \ge 0$, stretch $y \ge 0$ and shrink $z \ge 0$; the stretch can be of an infinite order (`fil`, `fill`), but the shrink is finite;
- a **penalty** $p$ marks a place where a break is good ($p < 0$), bad ($p > 0$), forbidden ($p \ge 10000$) or forced ($p \le -10000$). [Widow and club penalties](/widows-and-orphans/) are penalties of this kind.

A break may be at a penalty with $p < 10000$, or at a glue that comes right after a box. The last item is a forced penalty. The input also has the **page goal** $g$, the height of the text on a page, and a maximum depth $D$.

**The page total.** A page that starts at the box $s$ and ends at the break $b$ holds $x_s, \ldots, x_{b-1}$. Its total $t$ is the sum of the heights of its boxes, the sizes of its glue, and the depths of its boxes except the last one: the depth of the last box hangs below the page and counts only for its part above $D$. Its stretch $Y$ and shrink $Z$ are the sums over its glue.

**The badness of a page.** If $t < g$ and some glue has infinite stretch, the badness is $\beta = 0$. If $t < g$ otherwise, $\beta$ is the [badness](/typesetting-badness/) of TeX for stretching by $g - t$ with stretch $Y$, which is about $100 \bigl((g - t) / Y\bigr)^3$ and is capped at 10000. If $t - g > Z$, the page does not fit and $\beta = \infty$. Otherwise $\beta$ is the badness for shrinking by $t - g$ with shrink $Z$.

**The cost of a break.** With $\beta$ and the penalty $p$ of the break ($p = 0$ at a glue):

- $c = \infty$ if $\beta = \infty$;
- $c = p$ if $p \le -10000$ (a forced break on a page that fits);
- $c = \beta + p$ if $\beta < 10000$;
- $c = 100000$ if $\beta = 10000$.

In TeX, $c$ also adds a penalty $q$ for footnotes and other insertions that are split, and $c = \infty$ if $q \ge 10000$. This page leaves insertions out, so $q = 0$.

## The algorithm

```pseudo id=main
BEST-FIT-PAGES(x_0 .. x_{m−1}, g, D)
L1  breaks ← empty list; a ← −1
L2  loop
L3      s ← the first box after the break a
L4      if there is no such box then leave the loop
L5      least ← ∞; best ← none
L6      for b ← s + 1 to m − 1 do
L7          if b is not a legal break then continue
L8          (t, Y, Z) ← the page total, stretch and shrink of x_s .. x_{b−1}
L9          c ← the cost of the break b, from the badness of (t, Y, Z) against g
L10         if c ≤ least then
L11             least ← c; best ← b
L12         if c = ∞ or x_b is a forced penalty then leave the for loop
L13     append best to breaks
L14     a ← best
L15 return breaks
```

Line L3 drops the glue and penalties at the top of a page, as TeX does, so a page never starts with white space. Line L8 uses prefix sums of the sizes, stretches and shrinks, so it takes $O(1)$ time; it removes the depth of the last box when no glue follows it on the page. Line L10 uses $\le$, so a later break wins a tie, as in TeX. Line L12 stops at the first break where the page does not fit: the total can only grow when the page gets longer, so no later break can fit. If the first break already does not fit, its cost $\infty$ is still $\le least$, and the page is overfull, which is what TeX does. The items after the best break and up to the stopping break go back to the list and start the next page.

## Example

Take six lines of heights 10, 10, 10, 10, 20 and 20 (the last two could be displays), glue of size 2, stretch 8 and shrink 1 between them, the ending of plain TeX (glue with `fill` stretch and a forced break) and page goal $g = 44$. All depths are 0 and all penalties are 0.

| page | lines | total | badness | cost |
|---|---|---|---|---|
| 1 | 1 | 10 | 10000 (no stretch) | 100000 |
| 1 | 1 to 2 | 22 | 2073 | 2073 |
| 1 | 1 to 3 | 34 | 24 | 24 |
| 1 | 1 to 4 | 46 | 30 | 30 |
| 1 | 1 to 5 | 68 | $\infty$ | $\infty$, stop |
| 2 | 4 to 5 | 32 | 336 | 336 |
| 2 | 4 to 6 | 54 | $\infty$ | $\infty$, stop |
| 3 | 6 | 20 | 0 (`fill`) | forced |

On page 1 the break after line 3 costs 24 and the break after line 4 costs 30, so the builder ends page 1 after line 3. Page 2 then starts with a short line and two tall ones: lines 4 and 5 make 32 units, which must stretch by 12 with only 8 units of stretch, and lines 4 to 6 do not fit. The total cost of the unforced breaks is $24 + 336 = 360$. The breaking with lines 1 to 4 on page 1 (cost 30) and lines 5 and 6 on page 2 (total 42, at the forced break) costs 30. The builder saved 6 points on page 1 and paid 336 on page 2.

## Correctness

The builder is not exact for the total cost, as the example shows, so its correctness is that it does what TeX does. Two facts carry the proof. First, the prefix sums with the depth correction give, for each break, the same total that TeX keeps item by item with its separate page depth. Second, the scan of lines L6 to L12 sees exactly the legal breaks up to the first one where the page does not fit or a break is forced, and the test $c \le least$ keeps the last break of least cost among them. Each page ends after it starts, so the loop ends after at most $m$ pages. The full proof is in the proof file below.

## Complexity

Each break is tested in $O(1)$ time. A page scans the items from its first box to its stopping break, and the items after its best break are scanned again for the next page, so the time is $O(m + P k)$ for $P$ pages, where $k$ is the largest number of items scanned for one page. This is $O(m k)$ in the worst case. In practice a page holds about $k$ items, so $P k$ is about $m$ and the time is $\Theta(m)$. The prefix sums take $\Theta(m)$ extra space; TeX itself keeps only running totals for the current page.

## Properties

- **A heuristic.** It does not minimize the total cost of the breaks, and the example above loses by a factor of 12. The choices of the plain TeX values (for example `\clubpenalty=150` and `\widowpenalty=150`) are design choices, not results.
- **Online.** It needs only the current page and the next item, so TeX can ship out a page before it reads the rest of the document. This matters for page numbers and running heads that depend on the material.
- **Deterministic and iterative.** A later break wins a tie.
- **Overfull pages are possible.** When a single box is taller than the page goal plus the shrink, the page is overfull, and TeX reports it.

## Variants and improvements

- **Insertions.** TeX adds footnotes, floating figures and tables as insertions. Each one takes space from the page goal, and a split insertion adds the penalty $q$ to the cost.
- **Top skip and marks.** TeX puts the glue `\topskip` before the first box of a page so that the first baselines line up, and it keeps marks for running heads. Both leave the method the same.
- **Splitting a box.** The `\vsplit` operation of TeX uses the same cost to cut a box of a given height from a vertical list, for columns and for balancing.
- **Optimal breaking.** [Optimal pagination](/optimal-pagination/) chooses all page breaks together, as [Knuth-Plass line breaking](/knuth-plass-line-breaking/) does for lines. With floating figures, the general problem is hard; see [the NP-completeness of pagination](/pagination-np-completeness/).

## When to use it

Use it when pages must be produced one at a time, as in TeX, when the document is long, or when later material is not known yet. When the whole document is known and the cost of a bad page is high, as in books with many displays, use [optimal pagination](/optimal-pagination/), or run the builder and then fix the worst pages by hand.

## Pitfalls

- **The depth of the last box.** The depth of the last line hangs below the bottom of the page and does not count in the total, unless it is more than $D$. Counting it makes every page look fuller than it is.
- **Glue at the top.** The glue and penalties after a break are dropped. A forced penalty that comes at the top of a page is dropped too, so the list of breaks can end before the last item.
- **The cost 100000.** A page with badness 10000 costs 100000, not $10000 + p$. So when no break fits well, the builder takes the latest such break, which can end a page right before a heading.
- **It is not optimal.** Do not use it as a reference for tests of an optimal method. Test it against an item by item copy of the TeX rule instead.

## Implementations

## History

Knuth wrote the page builder for TeX and described its cost of a page break in The TeXbook in 1984, and its full code is in TeX, The Program of 1986. The method keeps only the current page in memory, so TeX can ship out each page before it reads the rest of the document. At about the same time, his student Michael Plass studied the optimal version of the problem with figures in his Stanford thesis of 1981, which led to [optimal pagination](/optimal-pagination/) and to the [hardness results](/pagination-np-completeness/).

## References
