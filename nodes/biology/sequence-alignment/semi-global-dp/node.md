---
tag: GQAPYM
kind: algorithm
slug: semi-global-dp
name: Semi-global dynamic programming
aliases:
- overlap alignment algorithm
- fitting alignment algorithm
- free-end-gap dynamic program
area: biology/sequence-alignment
level: core
summary: Needleman-Wunsch with a zero border at the free starts and a maximum over the last row or column at the free ends; O(mn) time for overlap and fitting alignment.
solves: [semi-global-alignment]
model: word-ram
complexity:
  vars: {m: the length of the first sequence, n: the length of the second sequence}
  time: {worst: Θ(m n), average: Θ(m n), best: Θ(m n)}
  space: {extra: Θ(m n), score_only: "Θ(min(m, n))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1980
  people: [Peter H. Sellers]
  note: Sellers (1980) used a zero first row to find the substrings of a text closest to a pattern, the fitting case with costs. The free end gaps of overlap alignment became a standard option of the global dynamic program in the following years.
prereqs: [semi-global-alignment, needleman-wunsch]
see_also: [needleman-wunsch, smith-waterman, sellers-algorithm, semi-global-alignment, overlap-detection, read-mapping, gotoh-algorithm, banded-alignment]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the section on end-space free alignment (the changed base conditions and the maximum over the last row and column)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3, Overlap matches
  - paper: "Peter H. Sellers, The theory and computation of evolutionary distances: pattern recognition, Journal of Algorithms 1(4), 1980, 359-373"
    locator: the dynamic program for the substrings of a text that are closest to a pattern
---

The semi-global DP solves [semi-global alignment](/semi-global-alignment/): an alignment of two whole sequences in which the gaps at chosen ends are free. It is the [Needleman-Wunsch](/needleman-wunsch/) table with two changes. A free start sets the first column or the first row to 0 instead of $-i \cdot d$ or $-j \cdot d$, so the alignment may skip a prefix of that sequence. A free end takes the best cell of the last column or the last row instead of the corner, so the alignment may skip a suffix. Overlap alignment and fitting alignment are two settings of these switches. The time is $\Theta(mn)$ for lengths $m$ and $n$. This page uses a substitution score $s(a, b)$ and a linear gap penalty $d$ per gap symbol.

## In plain words

You want to align two whole sequences, but you have declared some ends free: the part of a sequence that sticks out at that end costs nothing. The method is the grid of the global method with small changes at the edges.

If a sequence may skip its first letters for free, the boxes along its side of the grid start at zero instead of growing penalties: the alignment can start at any of those boxes for nothing. If a sequence may skip its last letters for free, you do not have to finish in the bottom right box. You may finish anywhere along the bottom row or the right column, and you take the best box there. From that box you walk back as usual.

## The problem

**Input.** Sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$ (DNA, RNA or amino acids), a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$, a gap penalty $d \ge 0$ per gap symbol, and four flags:

- $P_x$: the gaps opposite a prefix of $x$ (before the first letter of $y$) are free;
- $S_x$: the gaps opposite a suffix of $x$ (after the last letter of $y$) are free;
- $P_y$ and $S_y$: the same for a prefix and a suffix of $y$.

**Output.** An alignment of $x$ and $y$ with the largest semi-global score, and that score. Overlap alignment of a suffix of $x$ with a prefix of $y$ is $P_x$ and $S_y$; fitting $y$ into $x$ is $P_x$ and $S_x$. See [semi-global alignment](/semi-global-alignment/) for the exact score.

## The algorithm

The recurrence for the inner cells is that of Needleman-Wunsch:

$$F(i, j) = \max\{F(i - 1, j - 1) + s(x_i, y_j),\; F(i - 1, j) - d,\; F(i, j - 1) - d\}.$$

```pseudo id=main
SEMI-GLOBAL-DP(x[1 .. m], y[1 .. n], s, d, Px, Sx, Py, Sy)
L1  F[0, 0] ← 0
L2  for i ← 1 to m do F[i, 0] ← (0 if Px else −i · d)      ▷ a prefix of x against gaps
L3  for j ← 1 to n do F[0, j] ← (0 if Py else −j · d)      ▷ gaps against a prefix of y
L4  for i ← 1 to m do
L5      for j ← 1 to n do
L6          F[i, j] ← max(F[i − 1, j − 1] + s(x_i, y_j), F[i − 1, j] − d, F[i, j − 1] − d)
L7  E ← {(m, n)} ∪ {(i, n) : 0 ≤ i ≤ m, if Sx} ∪ {(m, j) : 0 ≤ j ≤ n, if Sy}
L8  (i, j) ← the first cell of E with the largest F; (ei, ej) ← (i, j); A ← the columns (x_{i+1} .. x_m against gaps) and (gaps against y_{j+1} .. y_n)
L9  while i > 0 and j > 0 do
L10     if F[i, j] = F[i − 1, j − 1] + s(x_i, y_j) then put (x_i, y_j) in front of A, i ← i − 1, j ← j − 1
L11     else if F[i, j] = F[i − 1, j] − d then put (x_i, −) in front of A, i ← i − 1
L12     else put (−, y_j) in front of A, j ← j − 1
L13 put the columns (x_1 .. x_i against gaps) and (gaps against y_1 .. y_j) in front of A
L14 return F[ei, ej], A
```

Lines L2 and L3 hold the free starts. With $P_x$, the cell $(i, 0)$ is 0: the letters $x_1 \cdots x_i$ go against gaps before the first letter of $y$, and these gaps are free. Lines L4 to L6 are Needleman-Wunsch without a change.

Lines L7 and L8 hold the free ends. With $S_x$, the alignment may end at any cell $(i, n)$ of the last column: all of $y$ is used, and the letters $x_{i+1} \cdots x_m$ go against free gaps after it. With $S_y$, it may end at any cell $(m, j)$ of the last row. Line L8 puts these free tail columns into $A$; at most one of the two parts is not empty, because $i = m$ or $j = n$.

The traceback of lines L9 to L12 is that of Needleman-Wunsch. It stops at the border, where $i = 0$ or $j = 0$. Line L13 adds the head: the rest of one sequence against gaps. Its cost is already in the border value of line L2 or L3, whether it is free or not.

## Example

Toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$. Fit $y = $ TAGTAC into $x = $ CAGGTACT, so $P_x$ and $S_x$ hold and $P_y$ and $S_y$ do not.

Line L2 sets the first column to 0, and line L3 sets the first row to $-2j$. Lines L4 to L6 fill this table; the cells of the traceback are in bold.

| | $-$ | T | A | G | T | A | C |
|---|---|---|---|---|---|---|---|
| $-$ | **0** | $-2$ | $-4$ | $-6$ | $-8$ | $-10$ | $-12$ |
| C | 0 | **$-1$** | $-3$ | $-5$ | $-7$ | $-9$ | $-8$ |
| A | 0 | $-1$ | **1** | $-1$ | $-3$ | $-5$ | $-7$ |
| G | 0 | $-1$ | **$-1$** | 3 | 1 | $-1$ | $-3$ |
| G | 0 | $-1$ | $-2$ | **1** | 2 | 0 | $-2$ |
| T | 0 | 2 | 0 | $-1$ | **3** | 1 | $-1$ |
| A | 0 | 0 | 4 | 2 | 1 | **5** | 3 |
| C | 0 | $-1$ | 2 | 3 | 1 | 3 | **7** |
| T | 0 | 2 | 0 | 1 | 5 | 3 | 5 |

With $S_x$, line L7 allows every cell of the last column. Its largest value is $F(7, 6) = 7$, so line L8 starts at $(7, 6)$ and puts the free tail column (T, $-$) for $x_8$ into $A$. The corner $F(8, 6) = 5$ is the global-style end.

| cell | value | line | column | reason |
|---|---|---|---|---|
| $(7, 6)$ | 7 | L10 | (C, C) | $F(6, 5) + 2 = 7$ |
| $(6, 5)$ | 5 | L10 | (A, A) | $F(5, 4) + 2 = 5$ |
| $(5, 4)$ | 3 | L10 | (T, T) | $F(4, 3) + 2 = 3$ |
| $(4, 3)$ | 1 | L10 | (G, G) | $F(3, 2) + 2 = 1$ |
| $(3, 2)$ | $-1$ | L11 | (G, $-$) | $F(2, 1) - 1 = -2$ fails; $F(2, 2) - 2 = -1$ |
| $(2, 2)$ | 1 | L10 | (A, A) | $F(1, 1) + 2 = 1$ |
| $(1, 1)$ | $-1$ | L10 | (C, T) | $F(0, 0) - 1 = -1$ |
| $(0, 0)$ | 0 | L13 | no head | |

The result is the score 7 and the alignment

```
C A G G T A C T
T A - G T A C -
```

The last column is free. All of $y$ is aligned, and the mismatch (C, T) at the start is kept, because $y$ may not lose its first letter: the flag $P_y$ is off. A local alignment would drop it and score 8.

**Overlap.** For $x = $ TTCAGTAC and $y = $ AGTACGGA with $P_x$ and $S_y$, the first column is 0, and the last row of the table is $0, 0, 1, 2, 6, 10, 8, 6, 4$. Its largest value is $F(8, 5) = 10$, so the alignment ends after AGTAC of $y$, and GGA goes against free gaps. The traceback runs down the diagonal to $(3, 0)$, and line L13 puts TTC against free gaps in front: `TTCAGTAC---` over `---AGTACGGA`, score 10.

## Correctness

Define the score of an alignment of the prefixes $x_1 \cdots x_i$ and $y_1 \cdots y_j$ with only the leading gaps free, as allowed by $P_x$ and $P_y$. The Needleman-Wunsch induction shows that $F(i, j)$ is the best such score: the border is right by lines L2 and L3, and the last column of a prefix alignment with $i, j \ge 1$ is never a leading gap, so it is always charged, as line L6 assumes. A full alignment is a prefix alignment that ends at some cell plus a tail of gap columns, and the tail is free exactly when the end cell is in the set $E$ of line L7. So the best cell of $E$ holds the optimum. The traceback is that of Needleman-Wunsch. The full proof is below.

## Complexity

- **Time.** Lines L1 to L3 take $\Theta(m + n)$ time, lines L4 to L6 take $\Theta(mn)$, line L8 looks at $O(m + n)$ cells, and the traceback and lines L13 and L8 add $O(m + n)$ columns. So the time is $\Theta(mn)$ in the best, the average and the worst case, as for Needleman-Wunsch.
- **Space.** $\Theta(mn)$ words for the table.
- **Score only.** Two rows of the table are enough for the score. With $S_x$, keep the best value of the last column as the rows go by; with $S_y$, the last row is the final row. So $\Theta(\min(m, n))$ space, if the rows run over the shorter sequence.
- **Alignment in linear space.** A score-only pass finds the end cell, a pass over the reversed sequences finds the start cell, and [Hirschberg's algorithm](/hirschberg-algorithm/) aligns the part between them: $\Theta(mn)$ time and $O(\min(m, n))$ space beside the output.

## Properties

- **Exact.** It returns an optimal semi-global alignment for every integer $s$ and $d \ge 0$ and every setting of the four flags.
- **A superset of Needleman-Wunsch.** With all four flags off, lines L2 and L3 are the Needleman-Wunsch border and $E = \{(m, n)\}$, so the program is Needleman-Wunsch.
- **Deterministic.** Line L8 takes the first best cell in the order of line L7, and the traceback has the fixed order of tests of Needleman-Wunsch.
- **No zero floor.** Unlike [Smith-Waterman](/smith-waterman/), no cell is set to 0 in the inside of the table. So the alignment cannot skip letters in the middle, and a bad letter at a non-free end is charged.

## Variants and improvements

- **Affine gaps.** The same border and end rules apply to the three tables of the [Gotoh algorithm](/gotoh-algorithm/); a free end gap then costs neither the opening nor the extension.
- **Unit costs and a text.** With costs instead of scores and $P_y$, $S_y$ for a pattern $x$ in a text $y$, the table is [Sellers' algorithm](/sellers-algorithm/) for [approximate string matching](/approximate-string-matching/). Each cell of the last row whose cost is at most $k$ ends an occurrence with at most $k$ differences.
- **Banded.** [Banded alignment](/banded-alignment/) with free ends fills only a band around the expected diagonal, for example the diagonal of a seed hit in [read mapping](/read-mapping/) or of a k-mer match in [overlap detection](/overlap-detection/).
- **Bit-parallel.** For unit costs, the [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) computes the fitting case one machine word of cells at a time.

## When to use it

Use the semi-global DP when both sequences must be aligned in full except at known ends: to find the overlap of two reads in assembly, to place a whole read on a part of a reference, or to find a primer or an adapter in a read. If letters may also be dropped at the other ends, or the related part is somewhere in the middle of both sequences, use [Smith-Waterman](/smith-waterman/). If no end may stick out, use [Needleman-Wunsch](/needleman-wunsch/).

## Pitfalls

- **Free start without a free border.** The flag $P_x$ must change the first column in line L2; a program that only changes the end rule of lines L7 and L8 still charges the leading gaps. On the overlap example it returns 4, not 10, because the three gaps under TTC cost 6.
- **The wrong row or column.** A free suffix of $x$ means the end may be any cell of the last column, $(i, n)$, in line L7; a free suffix of $y$ means the last row, $(m, j)$. Exchanging the two sets answers a different question: on the overlap example, ending in the last column instead of the last row gives 4, not 10.
- **A traceback to the corner.** The traceback must start at the cell chosen in line L8, not at $(m, n)$, and line L8 must add the free tail columns. Without them, the returned rows do not contain all of $x$ and $y$.
- **A zero floor inside the table.** Adding the term 0 of Smith-Waterman to line L6 turns the program into a different one: the alignment may then skip letters at ends that are not free.

## Implementations

## History

The parts of the method are older than its name. Sellers (1980) set the first row of the distance table to 0 to find the substrings of a text that are closest to a pattern, which is the fitting case with costs. Smith and Waterman (1981) used a zero border and a maximum over the matrix for the local case. Durbin et al. (1998) describe the overlap case with a zero border and a maximum over the last row and column, and Gusfield (1997) the general form with end spaces free. Today most alignment libraries offer the four free ends as options of one global routine.

## References
