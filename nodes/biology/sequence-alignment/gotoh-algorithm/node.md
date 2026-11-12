---
tag: GKC398
kind: algorithm
slug: gotoh-algorithm
name: Gotoh algorithm
aliases:
- Gotoh affine-gap alignment
- Gotoh-Smith-Waterman
area: biology/sequence-alignment
level: core
summary: Computes an optimal alignment under the affine gap penalty d + (L-1)e in O(mn) time, with three DP tables for the three kinds of last column.
solves: [affine-gap-alignment]
model: word-ram
complexity:
  vars: {m: the length of x, n: the length of y}
  time: {worst: Θ(m n)}
  space: {extra: Θ(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1982
  people: [Osamu Gotoh]
  note: Gotoh reduced alignment with the gap weight w_k = uk + v from the cubic time of the general gap recurrence to O(mn); Altschul and Erickson corrected the traceback in 1986.
prereqs: [affine-gap-alignment, needleman-wunsch]
see_also: [smith-waterman, affine-gap-penalty, hirschberg-algorithm, banded-smith-waterman, x-drop-extension, pair-hmm, alignment-graph]
sources:
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the recurrences with the auxiliary quantities for gaps ending in each sequence, and the O(mn) bound
  - paper: doi:10.1007/BF02462326
    title: Stephen F. Altschul and Bruce W. Erickson, Optimal sequence alignment using affine gap costs, Bulletin of Mathematical Biology 48(5/6), 1986, 603-616
    locator: the observation that Gotoh's traceback does not always yield an optimal alignment, and the corrected traceback for all optimal alignments
  - paper: doi:10.1101/031500
    title: Tomáš Flouri, Kassian Kobert, Torbjørn Rognes and Alexandros Stamatakis, Are all global alignment algorithms and implementations correct?, bioRxiv preprint, 2015
    locator: the initialization error for global alignment in Gotoh's paper and in later textbooks and programs
  - paper: doi:10.1093/bioinformatics/4.1.11
    title: Eugene W. Myers and Webb Miller, Optimal alignments in linear space, CABIOS 4(1), 1988, 11-17
    locator: the affine recurrences in linear space
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.4 (the three-state recurrences for affine gaps)
---

The Gotoh algorithm computes an optimal [alignment with affine gap penalties](/affine-gap-alignment/), where a gap of length $L$ costs $d + (L-1)e$, in $O(mn)$ time for sequences of lengths $m$ and $n$. It keeps three [dynamic programming](/dynamic-programming/) tables, one for each kind of last column: a pair, a letter of $x$ over a space, or a space over a letter of $y$. The general gap recurrence needs $O(mn(m+n))$ time, so Gotoh's 1982 paper made affine gaps as cheap as the [linear gap penalty](/linear-gap-penalty/) of [Needleman-Wunsch](/needleman-wunsch/). With a floor of zero it is the standard local aligner, often called Gotoh-Smith-Waterman.

## In plain words

To line up two sequences, a program fills a grid. Each cell holds the best score for lining up a start of one sequence with a start of the other.

With affine gaps, a dash costs a lot when it starts a gap and a little when it extends one. One number per cell does not say whether the best alignment there ends inside a gap, so the program cannot price the next dash. Gotoh keeps three numbers per cell: the best score that ends with a pair of letters, the best that ends with a dash in the lower row, and the best that ends with a dash in the upper row. Each cell takes constant work.

To read off the alignment, the program walks back through the grid and remembers which of the three numbers it is following.

## The problem

The input is $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a [scoring matrix](/scoring-matrix/) $s$, and gap parameters $d \ge e \ge 0$. The output is the maximum of

$$S(A) = \sum_{\text{pair columns } (a, b)} s(a, b) \; - \sum_{\text{gaps}} \bigl(d + (L - 1)e\bigr)$$

over all global alignments $A$ of $x$ and $y$, and one alignment that reaches it. A gap is a maximal run of columns with a space in the same row; a space in one row next to a space in the other row starts a new gap. Some sources write the penalty as $o + Le$; then $d = o + e$. See [affine gap penalty](/affine-gap-penalty/).

## The algorithm

For $0 \le i \le m$ and $0 \le j \le n$, among the alignments of $x_1 \cdots x_i$ with $y_1 \cdots y_j$, let

- $M(i, j)$ be the best score of one that ends with the pair column $(x_i, y_j)$,
- $X(i, j)$ be the best score of one that ends with the column $(x_i, -)$,
- $Y(i, j)$ be the best score of one that ends with the column $(-, y_j)$,
- $H(i, j) = \max\{M(i, j), X(i, j), Y(i, j)\}$, with $H(0, 0) = 0$,

where the maximum of an empty set is $-\infty$. A column $(x_i, -)$ either opens a new gap, at cost $d$, after an alignment that ends in any other way, or extends a gap in the same row, at cost $e$. Opening after an alignment that already ends with $(x_{i-1}, -)$ would count one gap as two. Since $d \ge e$, that only gives a lower value, so it does no harm, and the recurrence may use $H$ for the opening term.

```pseudo id=main
GOTOH(x, y, s, d, e)                              ▷ |x| = m, |y| = n, d ≥ e ≥ 0
L1  fill M, X, Y, H with −∞; M[0][0] ← 0; H[0][0] ← 0
L2  for i ← 0 to m do
L3      for j ← 0 to n do
L4          if i = 0 and j = 0 then continue
L5          if i > 0 and j > 0 then M[i][j] ← H[i−1][j−1] + s(x_i, y_j)
L6          if i > 0 then X[i][j] ← max(H[i−1][j] − d, X[i−1][j] − e)     ▷ x_i over a space
L7          if j > 0 then Y[i][j] ← max(H[i][j−1] − d, Y[i][j−1] − e)     ▷ a space over y_j
L8          H[i][j] ← max(M[i][j], X[i][j], Y[i][j])
L9  (i, j, state) ← (m, n, any); start two empty rows
L10 while i > 0 or j > 0 do
L11     if state = any then state ← the first of M, X, Y whose value at (i, j) equals H[i][j]
L12     if state = M then prepend (x_i, y_j); (i, j, state) ← (i−1, j−1, any)
L13     else if state = X then prepend (x_i, −)
L14         if X[i][j] = X[i−1][j] − e then state ← X else state ← any; i ← i − 1
L15     else prepend (−, y_j); if Y[i][j] = Y[i][j−1] − e then state ← Y else state ← any; j ← j − 1
L16 return H[m][n] and the two rows
```

Line L1 is the whole border initialization. The border cells then follow from lines L6 and L7: $X(i, 0) = -(d + (i-1)e)$ for $i \ge 1$, $Y(0, j) = -(d + (j-1)e)$ for $j \ge 1$, and $X(0, j) = Y(i, 0) = M(i, 0) = M(0, j) = -\infty$. Lines L9 to L15 trace back. The variable $state$ names the table whose value the walk is following; inside a gap the walk stays in $X$ or $Y$ as long as the extension term produced the value.

## Example

Let $x = \texttt{ACGTTA}$, $y = \texttt{ACTA}$, match $+2$, mismatch $-1$, $d = 3$, $e = 1$. The table $H$ is

| | $-$ | A | C | T | A |
|---|---|---|---|---|---|
| $-$ | 0 | -3 | -4 | -5 | -6 |
| A | -3 | **2** | -1 | -2 | -3 |
| C | -4 | -1 | **4** | 1 | 0 |
| G | -5 | -2 | **1** | 3 | 0 |
| T | -6 | -3 | **0** | 3 | 2 |
| T | -7 | -4 | -1 | **2** | 2 |
| A | -8 | -5 | -2 | -1 | **4** |

The last rows of the other tables are $M(6, \cdot) = -\infty, -5, -5, -2, 4$, $X(6, \cdot) = -8, -5, -2, -1, -1$ and $Y(6, \cdot) = -\infty, -11, -8, -5, -4$. The traceback, in bold:

| cell | state | value | reason | column |
|---|---|---|---|---|
| $(6, 4)$ | $M$ | 4 | $H(5, 3) + 2$ | (A, A) |
| $(5, 3)$ | $M$ | 2 | $H(4, 2) + 2$ | (T, T) |
| $(4, 2)$ | $X$ | 0 | $X(3, 2) - 1$, stay in $X$ | (T, $-$) |
| $(3, 2)$ | $X$ | 1 | $H(2, 2) - 3$, leave $X$ | (G, $-$) |
| $(2, 2)$ | $M$ | 4 | $H(1, 1) + 2$ | (C, C) |
| $(1, 1)$ | $M$ | 2 | $H(0, 0) + 2$ | (A, A) |

The result is $\texttt{ACGTTA}$ over $\texttt{AC--TA}$, score $8 - 4 = 4$. At $(4, 2)$ the opening term is $H(3, 2) - 3 = -2$, smaller than the extension term $0$: the alignment that deletes $\texttt{GT}$ as one gap wins over any that opens a second gap.

## Correctness

By induction over the cells in the order of lines L2 and L3, each of $M, X, Y$ equals the best score of its class of alignments. For $X(i, j)$, the alignment without its last column ends in a pair, in $(x_{i-1}, -)$, or in $(-, y_j)$, or is empty. Removing the last column changes the score by $-e$ in the second case and by $-d$ in the others, so the best value is $\max\{M(i-1, j) - d, X(i-1, j) - e, Y(i-1, j) - d\}$. Line L6 uses $H(i-1, j) - d$ in place of the two $-d$ terms, which adds the term $X(i-1, j) - d$; since $d \ge e$ it is at most $X(i-1, j) - e$ and does not change the maximum. The traceback keeps its state, so each column it emits has the cost that the table value assumed, and the emitted alignment scores exactly $H(m, n)$. The full proof is in the proofs file.

## Complexity

- **Time.** Lines L5 to L8 cost $O(1)$ for each of the $(m+1)(n+1)$ cells, and the traceback emits at most $m + n$ columns. The total is $\Theta(mn)$.
- **Space.** Four tables of $(m+1)(n+1)$ cells for the traceback, $\Theta(mn)$. $H$ can be computed on the fly, and the traceback needs only $M$, $X$ and $Y$, or two bits per cell and table with pointers.
- **Score only.** Each row reads only the row above, so two rows of each table suffice: $O(n)$ space. Myers and Miller (1988) recover the alignment in $O(m + n)$ space and $O(mn)$ time.

## Properties

- **Exact.** It returns the true optimum of the affine score for every $d \ge e \ge 0$.
- **Same order as Needleman-Wunsch.** The time differs from the one-table [linear gap penalty](/linear-gap-penalty/) version only by a constant factor of about three.
- **One column of memory.** It works because the cost of a column depends only on the column before it. Penalties that are not affine, such as concave ones, need more state.
- **Ties.** Line L11 prefers $M$, then $X$, then $Y$, and line L14 prefers to stay in a gap. Other orders give other optimal alignments with the same score.

## Variants and improvements

- **Local alignment.** Use $H(i, j) = \max\{0, M(i, j), X(i, j), Y(i, j)\}$, keep the largest $H$ over all cells, and stop the traceback at a cell with $H = 0$. This is the affine [Smith-Waterman](/smith-waterman/) algorithm, also called Gotoh-Smith-Waterman.
- **Free end gaps.** Set the border cells to $0$ for the free sequence, and take the maximum over the last row or column, as in [semi-global alignment](/semi-global-alignment/).
- **Linear space.** Myers and Miller combine the recurrences with [Hirschberg's](/hirschberg-algorithm/) divide and conquer; the split must allow a gap that crosses the middle row, whose opening is then charged only once.
- **Bands and drops.** The [banded Smith-Waterman](/banded-smith-waterman/) computes the same recurrences inside a diagonal band, and gapped [X-drop extension](/x-drop-extension/) skips cells whose score has fallen too far below the best.
- **SIMD.** Farrar's striped method (2007) runs the local recurrences on vectors of cells along the query.
- **Two-piece affine.** With two pairs $(d_1, e_1)$ and $(d_2, e_2)$, keep two gap tables per row and take the better; the cost per cell stays constant.

## When to use it

Use it for any pairwise alignment with affine gaps when $mn$ cells fit in the time budget: protein against protein, a read against a short reference window, or the final alignment after a heuristic search. For long sequences, combine it with a band, an X-drop rule or a linear-space method. If gaps should cost the same per space, the one-table [Needleman-Wunsch](/needleman-wunsch/) recurrence is simpler.

## Pitfalls

- **Border cells of the gap tables (line L1).** Initializing the gap table for one row with the border of the other, for example $X(0, j) = H(0, j)$, lets a gap in the bottom row and a gap in the top row share one opening charge. Flouri et al. (2015) report this mistake in Gotoh's paper, in textbooks, and in several programs. With $x = \texttt{A}$, $y = \texttt{C}$, mismatch $-5$, $d = 3$, $e = 1$, the correct score is $-5$, but the wrong border gives $-4$, from a space over $\texttt{C}$ followed by $\texttt{A}$ over a space with only one opening charge.
- **Traceback without a state (lines L11 to L15).** Choosing at each cell the table equal to $H$, without remembering that the walk is inside a gap, can return an alignment whose score is below $H(m, n)$. With $x = \texttt{AAG}$, $y = \texttt{A}$, match $+2$, mismatch $-1$, $d = 3$, $e = 1$, the optimum is $\texttt{AAG}$ over $\texttt{A--}$, score $-2$. At cell $(2, 1)$ both $M$ and $X$ equal $H = -1$, and a walk without state takes $M$ and returns $\texttt{AAG}$ over $\texttt{-A-}$, which scores $-4$. Altschul and Erickson (1986) pointed out this kind of error in Gotoh's traceback.
- **$d < e$ (lines L6 and L7).** With $d < e$ the opening term $H(i-1, j) - d$ restarts a gap at a lower cost than extending it, and the tables overestimate the optimum. Check the parameters before running.
- **Mixed conventions.** A tool option "open 10, extend 1" is $d = 10$ or $d = 11$ depending on the tool. Mixing them shifts every gap by one extension.

## Implementations

## History

Before 1982, alignment with a general gap weight used the recurrence of Waterman, Smith and Beyer, in $O(mn(m+n))$ time. Osamu Gotoh, in "An improved algorithm for matching biological sequences" (Journal of Molecular Biology, 1982), observed that for the gap weight $w_k = uk + v$ the best gap ending at a cell can be updated from its neighbour in constant time, which gave $O(mn)$. Altschul and Erickson (1986) showed that Gotoh's traceback does not always yield an optimal alignment and gave a correct procedure. Myers and Miller (1988) brought the space to linear. In 2015 Flouri, Kobert, Rognes and Stamatakis found an initialization error in the original paper that had been copied into textbooks and software.

## References
