---
tag: G3HRJ9
kind: algorithm
slug: smith-waterman
name: Smith-Waterman algorithm
aliases:
- Smith-Waterman local alignment
area: biology/sequence-alignment
level: core
summary: Dynamic program that finds an optimal local alignment of two sequences in O(mn) time, with a floor of zero in each cell and a maximum over all cells.
solves: [local-alignment]
model: word-ram
complexity:
  vars: {m: the length of the first sequence, n: the length of the second sequence}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n), score_only: "Θ(min(m, n))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1981
  people: [Temple F. Smith, Michael S. Waterman]
  note: Smith and Waterman published the local alignment recurrence in 1981, with a general gap function. Gotoh (1982) gave the O(mn) form for affine gaps.
prereqs: [local-alignment, needleman-wunsch]
see_also: [needleman-wunsch, semi-global-dp, gotoh-algorithm, banded-smith-waterman, hirschberg-algorithm, blast, x-drop-extension, kadane-algorithm]
sources:
  - paper: doi:10.1016/0022-2836(81)90087-5
    title: Temple F. Smith and Michael S. Waterman, Identification of common molecular subsequences, Journal of Molecular Biology 147(1), 1981, 195-197
    locator: the recurrence with the zero term, the maximum over the matrix, and the traceback to a zero cell
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the O(mn) recurrences for affine gap weights, for global and local similarity
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3, Local alignment, Smith-Waterman algorithm (and the condition of a negative expected score)
  - paper: doi:10.1016/0022-2836(87)90478-5
    title: Michael S. Waterman and Mark Eggert, A new algorithm for best subsequence alignments with application to tRNA-rRNA comparisons, Journal of Molecular Biology 197(4), 1987, 723-728
    locator: the best non-overlapping local alignments after the first
---

The Smith-Waterman algorithm finds an optimal [local alignment](/local-alignment/) of two sequences: a substring of each and an alignment of the two substrings with the largest [alignment score](/alignment-score/). It fills the same table as [Needleman-Wunsch](/needleman-wunsch/), with two changes. Each cell takes the maximum with 0, which lets an alignment start anywhere for free. The answer is the largest cell of the whole table, not the last cell, which lets an alignment end anywhere. A [traceback](/traceback/) from that cell stops at the first cell with value 0. The time is $\Theta(mn)$ for lengths $m$ and $n$. This page uses a substitution score $s(a, b)$ and a linear gap penalty $d$ per gap symbol; the scheme must have a negative expected score on random letters.

## In plain words

You want the best matching pieces of two sequences, not the best match of the whole sequences. Use the grid of the global method: each box holds the best score of an alignment that ends at that pair of positions.

There is one new rule. If the best score for a box falls below zero, write zero instead. A negative score means that the alignment so far does more harm than good, so it is better to drop it and start fresh at the next pair. When the grid is full, find the box with the highest number in the whole grid; the best piece ends there. Walk back from that box, as in the global method, and stop when you reach a zero. That is where the best piece starts.

## The problem

**Input.** Sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$ (DNA, RNA or amino acids), a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$, and a gap penalty $d \ge 0$ per gap symbol.

**Output.** Substrings $x[i'..i]$ and $y[j'..j]$ and an alignment of them with the largest score over all pairs of substrings, and that score. The empty alignment, with score 0, is allowed. See [local alignment](/local-alignment/) for the full statement and the condition on the scoring scheme.

## The algorithm

Let $H(i, j)$ be the best score of an alignment of a suffix of $x_1 \cdots x_i$ with a suffix of $y_1 \cdots y_j$, the empty suffixes included. Such an alignment is empty, with score 0, or its last column is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$. So

$$H(i, j) = \max\{0,\; H(i - 1, j - 1) + s(x_i, y_j),\; H(i - 1, j) - d,\; H(i, j - 1) - d\},$$

and the best local score is the maximum of $H(i, j)$ over all cells.

```pseudo id=main
SMITH-WATERMAN(x[1 .. m], y[1 .. n], s, d)
L1  for i ← 0 to m do H[i, 0] ← 0
L2  for j ← 0 to n do H[0, j] ← 0
L3  best ← 0, (bi, bj) ← (0, 0)
L4  for i ← 1 to m do
L5      for j ← 1 to n do
L6          H[i, j] ← max(0, H[i − 1, j − 1] + s(x_i, y_j), H[i − 1, j] − d, H[i, j − 1] − d)
L7          if H[i, j] > best then best ← H[i, j], (bi, bj) ← (i, j)
L8  i ← bi, j ← bj, A ← empty list of columns
L9  while H[i, j] > 0 do
L10     if H[i, j] = H[i − 1, j − 1] + s(x_i, y_j) then put (x_i, y_j) in front of A, i ← i − 1, j ← j − 1
L11     else if H[i, j] = H[i − 1, j] − d then put (x_i, −) in front of A, i ← i − 1
L12     else put (−, y_j) in front of A, j ← j − 1
L13 return best, A, x[i + 1 .. bi], y[j + 1 .. bj]
```

Lines L1 and L2 set the border to 0: a suffix of a prefix against an empty string scores at best 0, with the empty alignment. Line L6 is the Needleman-Wunsch rule with the extra term 0. Line L7 keeps the largest cell; with the strict test, the first such cell in row-major order wins.

The traceback of lines L9 to L12 runs only while the cell is positive. A positive cell got its value from one of the three non-zero terms of line L6, so one of the tests finds a step. A border cell is 0, so the loop never reads outside the table. The loop stops at a cell with value 0: there the alignment starts, and the substrings of line L13 begin after that cell.

## Example

Toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$. Its expected score on uniform DNA is $-1/4$. Align $x = $ TCAGTTGCA and $y = $ GAGTGCAT.

Lines L1 to L7 fill this table. The cells of the traceback are in bold; the largest cell is $H(9, 7) = 10$.

| | $-$ | G | A | G | T | G | C | A | T |
|---|---|---|---|---|---|---|---|---|---|
| $-$ | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| T | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 |
| C | 0 | **0** | 0 | 0 | 0 | 1 | 2 | 0 | 0 |
| A | 0 | 0 | **2** | 0 | 0 | 0 | 0 | 4 | 2 |
| G | 0 | 2 | 0 | **4** | 2 | 2 | 0 | 2 | 3 |
| T | 0 | 0 | 1 | 2 | **6** | 4 | 2 | 0 | 4 |
| T | 0 | 0 | 0 | 0 | **4** | 5 | 3 | 1 | 2 |
| G | 0 | 2 | 0 | 2 | 2 | **6** | 4 | 2 | 0 |
| C | 0 | 0 | 1 | 0 | 1 | 4 | **8** | 6 | 4 |
| A | 0 | 0 | 2 | 0 | 0 | 2 | 6 | **10** | 8 |

The zero floor is at work in many cells. For example, $H(2, 1)$ for C against G would be $\max\{0 - 1, 0 - 2, 0 - 2\} = -1$ without the floor; with it, the cell is 0, and the alignment that ends at $(3, 2)$ starts fresh.

The traceback starts at $(9, 7)$:

| cell | value | line | column | reason |
|---|---|---|---|---|
| $(9, 7)$ | 10 | L10 | (A, A) | $H(8, 6) + 2 = 10$ |
| $(8, 6)$ | 8 | L10 | (C, C) | $H(7, 5) + 2 = 8$ |
| $(7, 5)$ | 6 | L10 | (G, G) | $H(6, 4) + 2 = 6$ |
| $(6, 4)$ | 4 | L11 | (T, $-$) | $H(5, 3) - 1 = 1$ fails; $H(5, 4) - 2 = 4$ |
| $(5, 4)$ | 6 | L10 | (T, T) | $H(4, 3) + 2 = 6$ |
| $(4, 3)$ | 4 | L10 | (G, G) | $H(3, 2) + 2 = 4$ |
| $(3, 2)$ | 2 | L10 | (A, A) | $H(2, 1) + 2 = 2$ |
| $(2, 1)$ | 0 | L9 | stop | |

The result is the score 10, the substrings $x[3..9] = $ AGTTGCA and $y[2..7] = $ AGTGCA, and the alignment

```
A G T T G C A
A G - T G C A
```

The best global alignment of the same two sequences scores only 5, because it must also align the flanks TC and T.

## Correctness

The key claim is that $H(i, j)$ is the best score of an alignment of a suffix of $x_1 \cdots x_i$ with a suffix of $y_1 \cdots y_j$. The proof is the induction of Needleman-Wunsch, with the empty alignment as a fourth case, which the term 0 covers. Every local alignment ends at some pair of positions $(i, j)$, so it is one of the alignments that $H(i, j)$ considers, and the maximum over all cells is the best local score. The traceback keeps the invariant that $H$ of the current cell plus the score of the columns built so far equals the best score; it stops at a cell with value 0, so the columns score exactly the best score. The full proof is below.

## Complexity

- **Time.** Lines L1 to L3 take $\Theta(m + n)$ time. Lines L4 to L7 fill $mn$ cells in $O(1)$ time each, if $s$ is a table lookup. The traceback takes at most $m + n$ steps. So the time is $\Theta(mn)$ in the best, the average and the worst case.
- **Space.** $\Theta(mn)$ words for the table.
- **Score only.** Line L6 reads only the current row and the row above, so two rows of the shorter sequence and the best cell are enough: $\Theta(\min(m, n))$ space. Database search tools work in this mode and compute the alignment only for the best hits.
- **Alignment in linear space.** One pass finds the end cell $(b_i, b_j)$. A second pass, over the reversed prefixes $x_1 \cdots x_{b_i}$ and $y_1 \cdots y_{b_j}$, finds the start cell. Then [Hirschberg's algorithm](/hirschberg-algorithm/) aligns the two substrings globally. The total is $\Theta(mn)$ time and $O(\min(m, n))$ space beside the output.

## Properties

- **Exact.** It returns an optimal local alignment for every integer $s$ and $d \ge 0$. The scoring condition (a negative expected score) is about the meaning of the result, not about its optimality.
- **Deterministic.** The strict test of line L7 reports the first best cell in row-major order, and the order of lines L10 to L12 picks one alignment that ends there.
- **Starts and ends with a pair.** With $d \ge 0$, the returned alignment never starts or ends with a gap column. The first column: a gap step from a cell of value 0 gives at most $0 - d \le 0$, but the traceback only leaves positive cells. The last column: if the best cell got its value only from a gap step, its neighbour above or to the left holds at least as much and comes first in row-major order, so line L7 would have kept the neighbour. In the example, the alignment starts and ends with (A, A).
- **Not online.** The best cell and the alignment are known only at the end.

## Variants and improvements

- **Affine gaps.** With three tables for the three kinds of last column, the [Gotoh algorithm](/gotoh-algorithm/) handles the gap penalty $d + (L - 1)e$ in $\Theta(mn)$ time. The 0 goes into the table of the pair columns. This is the form used in practice.
- **General gap function.** The 1981 recurrence allows any gap penalty $g(L)$, at the cost of trying every gap length, $O(mn(m + n))$ time.
- **Several alignments.** Waterman and Eggert (1987) find the next best local alignment that shares no pair with the ones already found, by a recomputation of the part of the table that the found alignment affects.
- **Banded and seeded.** [Banded Smith-Waterman](/banded-smith-waterman/) fills only a band around a diagonal. [X-drop extension](/x-drop-extension/) grows an alignment from a seed and stops where the score falls too far below the best so far. [BLAST](/blast/) and the [FASTA algorithm](/fasta-algorithm/) use such methods to avoid the full table.
- **Vector and parallel forms.** The cells of one anti-diagonal are independent, and so, with a correction pass, are the cells of one column. SIMD and GPU implementations use this to fill many cells per instruction; the striped layout of Farrar (2007) is a common one.
- **Ungapped.** Without gaps, the problem splits into the diagonals, and each diagonal is a [maximum subarray](/maximum-subarray-problem/) problem; Smith-Waterman on one diagonal is [Kadane's algorithm](/kadane-algorithm/).

## When to use it

Use Smith-Waterman when you need the best local alignment exactly: to align a query with a few candidate sequences, to check the hits of a heuristic search, or when the sequences are short. Use it when only a part of the sequences is related, for example a shared protein domain. For a search in a large database, the full table for every database sequence is often too slow, and a heuristic such as [BLAST](/blast/) is the standard first step. If the sequences are related over their whole length, use [Needleman-Wunsch](/needleman-wunsch/); if one end must be kept, use the [semi-global DP](/semi-global-dp/).

## Pitfalls

- **No zero floor.** Without the term 0 in line L6, a bad start is never dropped: every alignment must then start on the border of the table, and the result is not a local alignment. On TCAGTTGCA and GAGTGCAT it gives 9 instead of 10.
- **The last cell.** Returning $H[m, n]$ instead of the best cell of line L7 gives the best local alignment that ends at the last letters of both sequences. In the example, $H(9, 8) = 8$, not 10.
- **Tracing back to the border.** The loop of line L9 must stop at the first cell with value 0. A traceback that runs to $(0, 0)$, as in Needleman-Wunsch, adds columns of total score at most 0 and returns a longer alignment with a lower score.
- **A positive expected score.** If the scheme scores a random pair above 0 on average, for example with $s(a, b) = +1$ for mismatches, the code is still correct, but the best local alignment of two unrelated sequences covers almost all of both. Check the scheme before you trust a local score.

## Implementations

## History

Temple Smith and Michael Waterman published the algorithm in 1981 in a three-page note in the Journal of Molecular Biology, titled "Identification of common molecular subsequences". They took the dynamic program of Needleman and Wunsch and of Sellers, added the zero term so that an alignment may start at any pair, and took the best cell of the matrix as the end. Their recurrence allowed a general gap weight $g(L)$, so it took cubic time; Gotoh (1982) gave the $O(mn)$ form for affine gaps. Waterman and Eggert (1987) extended the method to the best non-overlapping alignments after the first. Today the name Smith-Waterman means the local recurrence with a linear or affine gap penalty, and it is the exact reference for the heuristics of database search.

## References
