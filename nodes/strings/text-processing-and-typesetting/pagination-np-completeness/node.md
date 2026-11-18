---
tag: 56PSG7
kind: theorem
slug: pagination-np-completeness
name: NP-completeness of pagination with figures
aliases:
- Plass pagination hardness
area: strings/text-processing-and-typesetting
level: advanced
summary: Pagination with figures that may change order is strongly NP-complete for the total distance from figures to their references, by reduction from 3-partition.
prereqs: [page-breaking-problem, np-complete, three-partition, strong-np-hardness, polynomial-time-reduction]
see_also: [optimal-pagination, best-fit-page-breaking, widows-and-orphans, bin-packing-np-hardness, partition-problem, table-layout-problem]
sources:
  - paper: "Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Department of Computer Science, Stanford University, 1981"
    title: Michael F. Plass, Optimal Pagination Techniques for Automatic Typesetting Systems, PhD thesis, Stanford University, 1981
    locator: the abstract (two simple badness functions for which optimal pagination is NP-complete)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: 3-PARTITION and strong NP-completeness
---

When figures may float to any page after their reference and may change their order, finding a pagination with a small total distance from the figures to their references is NP-complete. The hard part is not the text but the packing of the figures into the space that the pages leave, which is a form of bin packing. The reduction below is from [3-partition](/three-partition/), so the problem is NP-complete in the strong sense: it stays hard when all heights are small integers. When the figures must keep their order, [optimal pagination](/optimal-pagination/) solves the problem in polynomial time by dynamic programming.

## Statement

**Pagination with free figures (decision form).** The input is $n$ text lines with heights $h_1, \ldots, h_n$, $m$ figures with heights $f_1, \ldots, f_m$, for each figure $t$ the line $r_t$ that refers to it, a page height $H$ and a bound $K$, all nonnegative integers. A pagination is a sequence of nonempty pages, where each page holds a block of consecutive lines (possibly empty) and any set of figures, such that:

- the lines appear in their order, each on one page, and each figure is on one page;
- the total height of the lines and figures on each page is at most $H$;
- figure $t$ is on the page of line $r_t$ or on a later page.

Write $p(t)$ for the page number of figure $t$ and $q(i)$ for the page number of line $i$. The question is whether there is a pagination with
$$\sum_{t=1}^{m} \bigl(p(t) - q(r_t)\bigr) \le K.$$

**Theorem.** Pagination with free figures is strongly NP-complete.

## In plain words

Suppose a page of text mentions many pictures, and all of them must come after it. Each later page has room for only a few pictures, and a picture costs more the further it is from the text.

To keep the cost low, the first pages after the text must be packed full of pictures with no gap. Deciding whether the pictures can be grouped to fill pages exactly is a hard puzzle, the same as splitting numbers into groups with equal sums. So no fast method is known for the whole problem.

## Proof

**Membership in NP.** A certificate is the page number of every line and every figure. In polynomial time we can check that the pages are nonempty, that the line pages do not decrease, that each page fits, that each figure comes on or after the page of its reference, and that the sum is at most $K$. The number of pages is at most $n + m$, since each page is nonempty.

**Hardness.** We reduce from 3-PARTITION: given $3q$ positive integers $a_1, \ldots, a_{3q}$ and an integer $B$ with $B/4 < a_i < B/2$ for every $i$ and $\sum_i a_i = qB$, can the numbers be split into $q$ triples that each sum to $B$? This problem is NP-complete in the strong sense (Garey and Johnson). Build the instance with:

- one line of height $h_1 = B$;
- $3q$ figures with heights $f_i = a_i$, all referred to by line 1;
- page height $H = B$ and bound $K = 3 \cdot (1 + 2 + \cdots + q) = \frac{3q(q+1)}{2}$.

All numbers are at most $\max(B, K)$, so the instance has size polynomial in the size of the 3-PARTITION instance, and its numbers are bounded by a polynomial in the numbers and the length of that instance.

*Facts about any pagination of the instance.* Every figure is on the page of line 1 or later, and pages are nonempty, so line 1 is on page 1. Page 1 has the line of height $B = H$, so it has no room for a figure, as each $a_i > 0$. Four figures have total height more than $4 \cdot B/4 = B$, so each page holds at most 3 figures. List the figures in the order of their pages, with ties in any order. The first three figures are on page 2 or later, and in general the $j$-th figure is on page $1 + \lceil j/3 \rceil$ or later, because pages $2, \ldots, \lceil j/3 \rceil$ hold at most $3 (\lceil j/3 \rceil - 1) < j$ figures. Since $q(1) = 1$, the cost is
$$\sum_{t} \bigl(p(t) - 1\bigr) \ \ge\ \sum_{j=1}^{3q} \Bigl\lceil \frac{j}{3} \Bigr\rceil = 3 \sum_{k=1}^{q} k = K.$$

*If the numbers have a 3-partition, the pagination instance is a yes instance.* Put the line on page 1 and the $k$-th triple on page $k + 1$, for $k = 1, \ldots, q$. Each page has height $B = H$, every figure comes after line 1, and the cost is $\sum_{k=1}^{q} 3k = K$.

*If there is a pagination of cost at most $K$, the numbers have a 3-partition.* By the bound above, the cost is exactly $K$, so every inequality $p(t) - 1 \ge \lceil j/3 \rceil$ holds with equality: the figures with $j = 3k - 2, 3k - 1, 3k$ are on page $k + 1$. So pages $2, \ldots, q + 1$ each hold exactly three figures. Each of these pages has height at most $B$, and their total height is $\sum_i a_i = qB$, so each has height exactly $B$. The triples of the pages form a 3-partition.

The reduction is computed in polynomial time and keeps the numbers polynomially bounded. Since 3-PARTITION is NP-complete in the strong sense, pagination with free figures is strongly NP-complete. $\square$

## Consequences

- No polynomial algorithm solves pagination with free figures unless P = NP, and since the hardness is strong, no pseudo-polynomial algorithm does either, so even small integer heights do not help.
- The hardness holds with a single line of text, so it comes from packing the figures, not from breaking the text. Rules that keep the figures in a fixed order, as LaTeX does for floats of one kind, remove it.
- Practical systems use heuristics for floats, for example the rules of LaTeX on top of the [best-fit page builder](/best-fit-page-breaking/).

## Tightness

- **Figures in order.** If the figures must appear in the order of their references, the [optimal pagination](/optimal-pagination/) dynamic program finds the optimum in $O(n^2 m^2)$ time; drop its white-space term to get exactly the cost of this page. So the freedom to reorder figures is what makes the problem hard.
- **Few figures.** For a fixed number $m$ of figures, the in-order dynamic program, with the check that every figure on a page is referred to on that page or before, can be run on each of the $m!$ orders. Any pagination lists its figures in some order with each page holding a consecutive block, so this finds the optimum in time $O(m!\, n^2 m^2)$, which is polynomial in $n$.
- **Strength of the reduction.** The bounds $B/4 < a_i < B/2$ are what limit each page to three figures. With the weaker problem [partition](/partition-problem/), the same idea gives only weak NP-hardness, which would leave room for a pseudo-polynomial algorithm.

## History

Michael Plass studied optimal pagination in his Stanford PhD thesis of 1981, which shows that pagination with figures is NP-complete for two simple badness functions. The proof on this page is a short one in a simple model, with the total distance to references as the cost; it follows the pattern of the proof that [bin packing is strongly NP-hard](/bin-packing-np-hardness/), and it is not the proof of the thesis.

## References
