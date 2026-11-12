---
tag: HNEF8P
kind: algorithm
slug: banded-smith-waterman
name: Banded Smith-Waterman
aliases:
- banded local alignment
area: biology/sequence-alignment
level: core
summary: Smith-Waterman local alignment with affine gaps restricted to the diagonals lo <= j - i <= hi, in O(wm) time for a band of w diagonals; used to extend seed hits.
solves: [local-alignment]
model: word-ram
complexity:
  vars: {m: the length of x, n: the length of y, w: the number of diagonals in the band}
  time: {worst: O(w m)}
  space: {extra: O(w m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1992
  people: [Kun-Mao Chao, William R. Pearson, Webb Miller]
  note: FASTA (1988) already ran Smith-Waterman in a band around its best diagonal; Chao, Pearson and Miller gave banded global and local alignment in linear space in 1992.
prereqs: [smith-waterman, banded-alignment, gotoh-algorithm]
see_also: [x-drop-extension, seed-and-extend, fasta-algorithm, blast, affine-gap-alignment, local-alignment, minimap2]
sources:
  - paper: doi:10.1093/bioinformatics/8.5.481
    title: Kun-Mao Chao, William R. Pearson and Webb Miller, Aligning two sequences within a specified diagonal band, CABIOS 8(5), 1992, 481-487
    locator: local alignment within a band, in O(NW) time and O(N) space
  - paper: doi:10.1073/pnas.85.8.2444
    title: William R. Pearson and David J. Lipman, Improved tools for biological sequence comparison, Proceedings of the National Academy of Sciences USA 85(8), 1988, 2444-2448
    locator: the optimized score of FASTA, computed by dynamic programming in a band around the best initial region
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the affine gap recurrences used in each cell
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 12, Section 12.2 (alignment in a band)
---

The banded Smith-Waterman algorithm computes the best [local alignment](/local-alignment/) of two sequences among the alignments whose path stays inside a diagonal band, the cells $(i, j)$ with $lo \le j - i \le hi$. It runs the affine [Smith-Waterman](/smith-waterman/) recurrences of the [Gotoh algorithm](/gotoh-algorithm/) on the band only, so a band of $w$ diagonals costs $O(wm)$ time instead of $O(mn)$. Seed-based search tools use it to extend a hit: the seed fixes a diagonal, and the band allows a few insertions and deletions around it. The result is exact for the band and can miss the true best local alignment when that alignment leaves the band.

## In plain words

Local alignment looks for the best-matching pair of pieces of two sequences. The full method fills a grid with a cell for every pair of positions, which is too slow when one sequence is a genome or a large database.

A search tool first finds a short exact match, a seed. Around the seed, the best local alignment probably follows the same diagonal of the grid, with only a few small steps to the side for inserted or deleted letters. So the tool fills only a strip of cells along that diagonal, a few cells wide.

The answer is the best local alignment that stays in the strip. If the true best alignment has a long gap, it steps out of the strip, and the banded method cannot see it.

## The problem

The input is $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a [scoring matrix](/scoring-matrix/) $s$, [affine gap penalties](/affine-gap-penalty/) $d \ge e \ge 0$ (a gap of length $L$ costs $d + (L - 1)e$), and a band $lo \le hi$. A local alignment of a substring $x_{i_0 + 1} \cdots x_i$ with $y_{j_0 + 1} \cdots y_j$ is a path in the alignment grid from cell $(i_0, j_0)$ to cell $(i, j)$, one cell per column. It is *in the band* when every cell of the path, including the start, satisfies $lo \le j - i \le hi$. The output is the maximum score of an in-band local alignment, with $0$ for the empty one, an alignment that reaches it, and its end cell.

## The algorithm

The tables are those of the Gotoh algorithm, restricted to band cells, with a floor of $0$ in $H$ for a fresh start. Any table entry outside the band, outside the grid, or not yet set reads as $-\infty$.

```pseudo id=main
BANDED-SW(x, y, s, d, e, lo, hi)                    ▷ cells with lo ≤ j − i ≤ hi; d ≥ e ≥ 0
L1  best ← 0; (bi, bj) ← (0, 0); all table entries read −∞ until set
L2  for i ← 0 to m do
L3      for j ← max(0, i + lo) to min(n, i + hi) do
L4          if i > 0 and j > 0 then M[i][j] ← H[i−1][j−1] + s(x_i, y_j)
L5          X[i][j] ← max(H[i−1][j] − d, X[i−1][j] − e)          ▷ x_i over a space
L6          Y[i][j] ← max(H[i][j−1] − d, Y[i][j−1] − e)          ▷ a space over y_j
L7          H[i][j] ← max(0, M[i][j], X[i][j], Y[i][j])
L8          if H[i][j] > best then best ← H[i][j]; (bi, bj) ← (i, j)
L9  if best = 0 then return the empty alignment; (i, j, state) ← (bi, bj, any)
L10 loop
L11     if state = any then (if H[i][j] = 0 then exit the loop); state ← the first of M, X, Y equal to H[i][j]
L12     if state = M then prepend (x_i, y_j); (i, j, state) ← (i−1, j−1, any)
L13     else if state = X then prepend (x_i, −); state ← X if X[i][j] = X[i−1][j] − e, else any; i ← i − 1
L14     else prepend (−, y_j); state ← Y if Y[i][j] = Y[i][j−1] − e, else any; j ← j − 1
L15 return best, the two rows, and the end cell (bi, bj)
```

Row $i$ holds at most $w = hi - lo + 1$ cells, so each table is stored as $m + 1$ arrays of length $w$, with cell $(i, j)$ at offset $j - i - lo$. Line L11 stops at a cell whose value is the $0$ of line L7, the start of the alignment.

## Example

Let $x = \texttt{TTGACCTGAAT}$ and $y = \texttt{CCGACCTTGAAG}$, match $+2$, mismatch $-3$, $d = 5$, $e = 2$. The best local alignment without any band is

```
GACC-TGAA
GACCTTGAA
```

with eight matches and one gap, $16 - 5 = 11$. It starts at cell $(2, 2)$, on diagonal $0$, and after the gap it runs on diagonal $1$ up to its end cell $(10, 11)$. Different bands give:

| band $[lo, hi]$ | best score | alignment | end cell |
|---|---|---|---|
| all diagonals | 11 | $\texttt{GACC-TGAA}$ over $\texttt{GACCTTGAA}$ | $(10, 11)$ |
| $[-1, 1]$ | 11 | the same | $(10, 11)$ |
| $[0, 0]$ | 10 | $\texttt{GACCT}$ over $\texttt{GACCT}$ | $(7, 7)$ |
| $[1, 3]$ | 8 | $\texttt{TGAA}$ over $\texttt{TGAA}$ | $(10, 11)$ |

The band $[0, 0]$ forbids every gap, so it finds only the gap-free part before the gap. The band $[1, 3]$ excludes the start of the best alignment and finds only the part after the gap. The band $[-1, 1]$ contains the whole path and gives the true optimum, with $35$ band cells against $12 \cdot 13 = 156$ for the full table.

## Correctness

For each band cell, $M$, $X$ and $Y$ hold the best score of an in-band alignment ending at that cell with a pair column, an $x$ letter over a space, or a space over a $y$ letter, where the alignment may start at any in-band cell, and $H$ is the maximum of these and $0$. The proof is the induction of the [Gotoh algorithm](/gotoh-algorithm/) with two changes: the $0$ in line L7 stands for the empty alignment that starts at the cell, and a neighbour outside the band reads $-\infty$, which removes exactly the alignments that would pass through it. The traceback follows the stored values back to a cell with value $0$ and emits an alignment of score $best$. The full proof is in the proofs file.

## Complexity

- **Time.** Each row has at most $w$ band cells and each costs $O(1)$, so the fill takes $O(w(m + 1))$ time, and never more than $O((m + 1)(n + 1))$. The traceback emits at most $m + n$ columns. For a band of fixed width around a seed diagonal, the time is linear in the length of the extended region.
- **Space.** Four tables of $w(m + 1)$ entries, $O(wm)$, for the traceback. The score and the end cell alone need two rows, $O(w)$. Chao, Pearson and Miller (1992) also recover the alignment in $O(m + n)$ space, by finding the start and the end of the best local alignment in the band and then aligning that region globally in linear space.

## Properties

- **Monotone in the band.** A wider band contains more alignments, so the score never decreases as the band grows, and with $lo \le -m$ and $hi \ge n$ it is the Smith-Waterman score.
- **Exact for the band, heuristic for the problem.** The answer is optimal among in-band alignments. As an answer to local alignment it is a lower bound.
- **A band is not a window.** The alignment can start and end anywhere in the band, so a band of 3 diagonals can still return an alignment of thousands of columns.

## Variants and improvements

- **Global and semi-global bands.** The same band restriction applied to [Needleman-Wunsch](/needleman-wunsch/) or to [semi-global alignment](/semi-global-alignment/) gives [banded alignment](/banded-alignment/) for whole sequences, where the band must contain the corners.
- **Extension from a seed.** In seed-and-extend tools, the alignment is anchored at the seed and extended in each direction separately. The band is centred on the seed diagonal, and the extension also stops when the score falls far below its best, a combination of a band and [X-drop extension](/x-drop-extension/).
- **Linear space.** Chao, Pearson and Miller (1992) give $O(NW)$ time and $O(N)$ space, for $N$ the length of the shorter sequence and $W$ the band width.
- **Vector instructions.** The cells of one anti-diagonal of the band do not depend on each other, so they can be computed together with SIMD instructions; read mappers such as [minimap2](/minimap2/) do this.

## When to use it

Use it when a seed, a chain of seeds or a previous alignment tells you the diagonal of the alignment, and the expected number of insertions and deletions is small compared with the band width: protein search after [FASTA](/fasta-algorithm/) style diagonal scoring, extension of seeds in [seed-and-extend](/seed-and-extend/) tools, or realignment of reads near a known position. When long gaps are possible, use a wider band, an X-drop rule that can wander off the diagonal, or the full Smith-Waterman algorithm.

## Pitfalls

- **The optimum leaves the band (lines L3 to L6).** With $x = \texttt{ACGTACGTAC}$, $y = \texttt{ACGTAGGGCGTAC}$, match $+2$, mismatch $-3$, $d = 3$, $e = 1$, the best local alignment is $\texttt{ACGTA---CGTAC}$ over $\texttt{ACGTAGGGCGTAC}$, score $20 - 5 = 15$. Its gap of length 3 moves it from diagonal $0$ to diagonal $3$. The band $[-1, 1]$ returns only $10$, for $\texttt{ACGTA}$; the band $[0, 3]$ returns $15$. Nothing in the output warns that the band was too narrow.
- **Stale values at the band edge (lines L5 and L6).** In row-offset storage, the upper neighbour of the last cell of a row lies outside the band. If the code reads the previous row's array past its end, or reuses an array without resetting it, line L5 reads an old value instead of $-\infty$.
- **Stopping the traceback (line L11).** The traceback must stop only at a cell where the walk is in state "any" and $H = 0$. Stopping at the first cell where $M$ or $X$ happens to be $0$ inside a gap cuts the alignment and returns rows whose score is not $best$.
- **The start must be in the band.** A path that starts outside the band and enters it is not an in-band alignment under this definition, and the algorithm does not find it. Tests that compare with a brute force must use the same definition.

## Implementations

## History

Pearson and Lipman's FASTA (1988) computed its final optimized score with a dynamic program restricted to a band around the best diagonal region found by its word search. Chao, Pearson and Miller published the general method for global and local alignment within a specified diagonal band in 1992, with linear space. Banded affine local alignment around seeds is now the inner loop of many mappers and search tools.

## References
