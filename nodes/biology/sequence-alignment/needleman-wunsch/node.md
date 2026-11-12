---
tag: 2FKWQD
kind: algorithm
slug: needleman-wunsch
name: Needleman-Wunsch algorithm
aliases:
- Needleman-Wunsch-Sellers algorithm
area: biology/sequence-alignment
level: intro
summary: Dynamic program that finds an optimal global alignment of two sequences in O(mn) time by filling a table of prefix scores and tracing back.
solves: [global-alignment]
model: word-ram
complexity:
  vars: {m: the length of the first sequence, n: the length of the second sequence}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n), score_only: "Θ(min(m, n))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1970
  people: [Saul B. Needleman, Christian D. Wunsch]
  note: Needleman and Wunsch published a dynamic program for the comparison of two protein sequences in 1970. The O(mn) form with a linear gap penalty that is now taught under their name came with Sankoff (1972) and Sellers (1974).
prereqs: [global-alignment, alignment-graph, tabulation]
see_also: [smith-waterman, semi-global-dp, hirschberg-algorithm, gotoh-algorithm, wagner-fischer-algorithm, lcs-dynamic-programming, banded-alignment, traceback]
sources:
  - paper: doi:10.1016/0022-2836(70)90057-4
    title: Saul B. Needleman and Christian D. Wunsch, A general method applicable to the search for similarities in the amino acid sequence of two proteins, Journal of Molecular Biology 48(3), 1970, 443-453
    locator: the method of the paper (the matrix of the two sequences, the maximum match and the penalty for gaps)
  - paper: doi:10.1073/pnas.69.1.4
    title: David Sankoff, Matching sequences under deletion/insertion constraints, Proceedings of the National Academy of Sciences of the USA 69(1), 1972, 4-6
    locator: the quadratic algorithm for the largest number of matches
  - paper: doi:10.1137/0126070
    title: Peter H. Sellers, On the theory and computation of evolutionary distances, SIAM Journal on Applied Mathematics 26(4), 1974, 787-793
    locator: the O(mn) computation of the distance between two sequences
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the introduction, which names the Needleman-Wunsch-Sellers algorithm and its cost with a general gap function
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3, Global alignment, Needleman-Wunsch algorithm
---

The Needleman-Wunsch algorithm finds an optimal [global alignment](/global-alignment/) of two sequences. It fills a table whose cell $(i, j)$ holds the best [alignment score](/alignment-score/) of the first $i$ letters of one sequence against the first $j$ letters of the other. Each cell is the largest of three neighbours plus a score, so the $(m + 1)(n + 1)$ cells take $\Theta(mn)$ time. A [traceback](/traceback/) from the last cell gives the alignment. This page uses a substitution score $s(a, b)$ and a linear gap penalty $d$ per gap symbol; it is the similarity form of the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/).

## In plain words

You want to line up two whole sequences with gaps so that the total score is as high as possible. Make a grid with one sequence along the side and the other along the top. Each box answers a small question: what is the best score for the first few letters of one sequence against the first few letters of the other?

You fill the boxes from the top left corner. A box has only three ways to end its alignment: pair the two last letters, or put one of them against a gap. Each way uses a box that you already filled. So you take the best of three and move on. The bottom right box holds the best score for the whole sequences. To get the alignment itself, walk back from that box and repeat each choice that gave the best value.

## The problem

**Input.** Sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$ (DNA, RNA or amino acids), a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$, and a gap penalty $d \ge 0$ per gap symbol (the linear model $g(L) = dL$).

**Output.** An alignment $A$ of $x$ and $y$ that maximizes $S(A) = \sum s(a, b) - d \cdot (\text{number of gap columns})$, and its score. See [global alignment](/global-alignment/) for the full statement.

## The algorithm

Let $F(i, j)$ be the best score of an alignment of $x_1 \cdots x_i$ and $y_1 \cdots y_j$. The last column of such an alignment is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$, and the rest is an alignment of shorter prefixes. So

$$F(i, j) = \max\{F(i - 1, j - 1) + s(x_i, y_j),\; F(i - 1, j) - d,\; F(i, j - 1) - d\}.$$

```pseudo id=main
NEEDLEMAN-WUNSCH(x[1 .. m], y[1 .. n], s, d)
L1  F[0, 0] ← 0
L2  for i ← 1 to m do F[i, 0] ← −i · d            ▷ x_1 .. x_i against gaps
L3  for j ← 1 to n do F[0, j] ← −j · d            ▷ gaps against y_1 .. y_j
L4  for i ← 1 to m do
L5      for j ← 1 to n do
L6          F[i, j] ← max(F[i − 1, j − 1] + s(x_i, y_j), F[i − 1, j] − d, F[i, j − 1] − d)
L7  i ← m, j ← n, A ← empty list of columns
L8  while i > 0 or j > 0 do
L9      if i > 0 and j > 0 and F[i, j] = F[i − 1, j − 1] + s(x_i, y_j) then put (x_i, y_j) in front of A, i ← i − 1, j ← j − 1
L10     else if i > 0 and F[i, j] = F[i − 1, j] − d then put (x_i, −) in front of A, i ← i − 1
L11     else put (−, y_j) in front of A, j ← j − 1
L12 return F[m, n], A
```

Lines L1 to L3 fill the border. An empty prefix against $j$ letters has only one alignment, all gaps, with score $-jd$. Lines L4 to L6 fill the rest row by row. When line L6 runs, the three cells it reads are already filled: they are in the row above or to the left in the same row.

Lines L7 to L11 are the traceback. At each cell, they find a step that gives the value of the cell, and they put the column of that step in front of the alignment. Line L11 needs no test: if lines L9 and L10 fail, then $j > 0$ and the third term of line L6 is the one that gave $F[i, j]$. When two steps tie, the order of the tests chooses one: the diagonal, then a gap in $y$, then a gap in $x$. Each choice gives an optimal alignment.

## Example

Toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$. Align $x = $ ACGTC and $y = $ AGTAC.

Lines L1 to L6 fill this table. The rows are the prefixes of $x$, the columns the prefixes of $y$. The cells of the traceback path are in bold.

| | $-$ | A | G | T | A | C |
|---|---|---|---|---|---|---|
| $-$ | **0** | $-2$ | $-4$ | $-6$ | $-8$ | $-10$ |
| A | $-2$ | **2** | 0 | $-2$ | $-4$ | $-6$ |
| C | $-4$ | **0** | 1 | $-1$ | $-3$ | $-2$ |
| G | $-6$ | $-2$ | **2** | 0 | $-2$ | $-4$ |
| T | $-8$ | $-4$ | 0 | **4** | **2** | 0 |
| C | $-10$ | $-6$ | $-2$ | 2 | 3 | **4** |

For example, $F(4, 3) = \max\{F(3, 2) + s(T, T), F(3, 3) - 2, F(4, 2) - 2\} = \max\{4, -2, -2\} = 4$.

The traceback starts at $(5, 5)$ with the value 4.

| cell | value | test that holds | column | reason |
|---|---|---|---|---|
| $(5, 5)$ | 4 | L9 | (C, C) | $F(4, 4) + 2 = 4$ |
| $(4, 4)$ | 2 | L11 | ($-$, A) | $F(3, 3) - 1 = -1$ and $F(3, 4) - 2 = -4$ fail; $F(4, 3) - 2 = 2$ |
| $(4, 3)$ | 4 | L9 | (T, T) | $F(3, 2) + 2 = 4$ |
| $(3, 2)$ | 2 | L9 | (G, G) | $F(2, 1) + 2 = 2$ |
| $(2, 1)$ | 0 | L10 | (C, $-$) | $F(1, 0) - 1 = -3$ fails; $F(1, 1) - 2 = 0$ |
| $(1, 1)$ | 2 | L9 | (A, A) | $F(0, 0) + 2 = 2$ |

The result is the score 4 and the alignment

```
A C G T - C
A - G T A C
```

## Correctness

The proof is an induction over the cells in the order of lines L4 and L5. The claim is that $F[i, j]$ is the best score of an alignment of $x_1 \cdots x_i$ and $y_1 \cdots y_j$. The border is right because an empty prefix has only one alignment. For an inner cell, the last column of an optimal alignment is one of three kinds, and removing it leaves an alignment of smaller prefixes, which by induction scores at most the neighbour cell. Line L6 takes the best of the three cases. The traceback keeps the invariant that $F[i, j]$ plus the score of the columns built so far equals $F[m, n]$, so it ends with an alignment of score $F[m, n]$. The full proof is below.

## Complexity

- **Time.** Lines L1 to L3 take $\Theta(m + n)$ time. Lines L4 to L6 fill $mn$ cells, each with three additions and two comparisons in $O(1)$ time, if $s$ is a table lookup. The traceback takes one step per column, at most $m + n$ steps. So the time is $\Theta(mn)$ in the best, the average and the worst case, because each cell is filled whatever the input.
- **Space.** The table holds $(m + 1)(n + 1)$ integers, $\Theta(mn)$ words.
- **Score only.** Line L6 reads only the current row and the row above. If you need $F[m, n]$ and not the alignment, keep two rows of the shorter sequence ([rolling-array space reduction](/rolling-array-space-reduction/)): $\Theta(\min(m, n))$ space.
- **Alignment in linear space.** [Hirschberg's algorithm](/hirschberg-algorithm/) finds the alignment in $O(\min(m, n))$ space and $\Theta(mn)$ time, with about twice the cell computations.

Under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), no algorithm solves the problem in $O(n^{2 - \varepsilon})$ time for $m = n$ (see [global alignment](/global-alignment/)), so the quadratic time is close to optimal for general inputs.

## Properties

- **Exact.** It returns an optimal alignment for each scoring scheme, also for negative or asymmetric $s$ and for $d = 0$.
- **Deterministic.** The fixed order of the tests in lines L9 to L11 picks one optimal alignment among ties.
- **Not online.** The traceback needs the whole table, so the alignment is known only at the end. The score of each pair of prefixes is known as soon as its cell is filled.
- **Data independent.** It does the same work for every input of lengths $m$ and $n$; similar sequences do not make it faster. Banded and cutoff methods use similarity to save work.

## Variants and improvements

- **Affine gaps.** Three tables instead of one give the [Gotoh algorithm](/gotoh-algorithm/), still $\Theta(mn)$ time.
- **General gap function.** With a gap penalty $g(L)$ of any shape, a cell must consider every gap length that ends at it, which takes $O(mn(m + n))$ time. This is the form of the 1970 paper.
- **Local and semi-global forms.** A floor of 0 in line L6 and a maximum over all cells give [Smith-Waterman](/smith-waterman/). A border of zeros in lines L2 and L3 and a maximum over the last row or column give the [semi-global DP](/semi-global-dp/).
- **Banded.** Fill only the cells within $k$ diagonals of the main one: [banded alignment](/banded-alignment/), $O(k \max(m, n))$ time. It is exact if an optimal alignment stays in the band.
- **Linear space.** [Hirschberg's algorithm](/hirschberg-algorithm/) for linear gaps, and Myers and Miller (1988) for affine gaps.
- **Parallel and vector forms.** The cells of one anti-diagonal are independent, so they can be filled at the same time by vector instructions or by GPU threads.
- **Unit costs.** For LCS and edit distance, the [Four Russians method](/four-russians-method/) and the [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) are faster.

## When to use it

Use Needleman-Wunsch when the two sequences are related over their whole length and are short enough that $mn$ cells fit in memory, for example two proteins or two genes of a few thousand letters. For the score alone, keep two rows. For long sequences that are similar, use a banded alignment; for long sequences in general, use Hirschberg's algorithm. If only a part of the sequences is related, use [Smith-Waterman](/smith-waterman/) or the [semi-global DP](/semi-global-dp/) instead, because the global form charges the unrelated ends.

## Pitfalls

- **A zero border.** If lines L2 and L3 set the border to 0, end gaps become free, and the result is a semi-global alignment, not a global one. The border must be $-i \cdot d$ and $-j \cdot d$.
- **Missing bounds in the traceback.** Line L10 must test $i > 0$ and line L9 must test $i > 0$ and $j > 0$. Without the tests, the traceback reads $F[-1, j]$ on the border, and in Python a negative index reads the last row of the table without an error.
- **Transposed scores.** For an asymmetric matrix, lines L6 and L9 must both use $s(x_i, y_j)$. If one of them uses $s(y_j, x_i)$, the test of line L9 can fail where it should hold, and line L11, which has no test, then takes a step that does not give the value of the cell. The returned alignment is then not optimal, or it does not use all the letters.
- **Floating-point scores.** The tests of lines L9 and L10 compare for equality. With floating-point scores, rounding can make both tests fail, with the same wrong step at line L11. Use integer scores, or store the choice of line L6 in a second table.

## Implementations

## History

Saul Needleman and Christian Wunsch published their method in 1970 to compare the amino acid sequences of two proteins. They filled a matrix of the two sequences and allowed a gap penalty of a general form, and in that form each cell looks at every possible gap length, so the method takes cubic time. Sankoff (1972) gave a quadratic algorithm for the largest number of matches, and Sellers (1974) gave the $O(mn)$ computation of an evolutionary distance with costs per letter. The same table was found several times in those years, also for edit distance by Wagner and Fischer (1974). Gotoh (1982) calls the quadratic form the Needleman-Wunsch-Sellers algorithm, and extended it to affine gaps. Today the name Needleman-Wunsch means the quadratic program with a linear or affine gap penalty.

## References
