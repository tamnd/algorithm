---
tag: 6FEAF1
kind: technique
slug: banded-alignment
name: Banded alignment
aliases:
- banded dynamic programming
- k-band alignment
area: biology/sequence-alignment
level: core
summary: Fill only the cells of the alignment DP table on diagonals lo <= j - i <= hi; exact when an optimal path stays in the band, and exact for edit distance with band doubling.
prereqs: [needleman-wunsch, edit-distance]
see_also: [banded-smith-waterman, x-drop-extension, k-differences-problem, ukkonen-cutoff-algorithm, landau-vishkin-algorithm, fasta-algorithm, minimap2, myers-diff]
sources:
  - paper: doi:10.1093/nar/12.1Part1.175
    title: James W. Fickett, Fast optimal alignment, Nucleic Acids Research 12(1 Part 1), 1984, 175-179
    locator: computing only the part of the matrix that can hold an alignment within a cost bound, and raising the bound when needed
  - paper: doi:10.1016/S0019-9958(85)80046-2
    title: Esko Ukkonen, Algorithms for approximate string matching, Information and Control 64, 1985, 100-118
    locator: the band of diagonals for edit distance at most a threshold, and the doubling of the threshold
  - paper: doi:10.1093/bioinformatics/8.5.481
    title: Kun-Mao Chao, William R. Pearson and Webb Miller, Aligning two sequences within a specified diagonal band, CABIOS 8(5), 1992, 481-487
    locator: global and local alignment inside a band in O(NW) time and O(N) space
  - paper: doi:10.1073/pnas.85.8.2444
    title: William R. Pearson and David J. Lipman, Improved tools for biological sequence comparison, Proceedings of the National Academy of Sciences USA 85(8), 1988, 2444-2448
    locator: the final optimization step of FASTA, a dynamic program in a band around the best initial region
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 12, Section 12.2 (k-difference global alignment in a band)
---

Banded alignment is a technique that speeds up an alignment dynamic program by filling only the cells near one diagonal. Cell $(i, j)$ of the table lies on diagonal $t = j - i$, and the band is the set of diagonals $lo \le t \le hi$. A band of $w = hi - lo + 1$ diagonals has at most $w(m+1)$ cells, so [Needleman-Wunsch](/needleman-wunsch/), [Smith-Waterman](/smith-waterman/) and their affine versions run in $O(wm)$ time instead of $O(mn)$. The result is the best alignment inside the band, which is the true optimum only when some optimal path stays inside. For unit-cost [edit distance](/edit-distance/), doubling the band until the distance fits it gives an exact method in $O((D+1)\min(m, n))$ time, where $D$ is the distance.

## In plain words

To align two sequences, a program fills a grid with one row per letter of the first sequence and one column per letter of the second. The best alignment is a path through the grid from the top left to the bottom right. For similar sequences this path stays near the main diagonal, because a step off the diagonal means an inserted or deleted letter.

So the program fills only a strip of cells around the diagonal. A strip of width 20 in a grid of 10,000 by 10,000 cells is 500 times less work.

The risk is that the best path leaves the strip. Then the answer can be worse than the true best. For edit distance there is a safe test: if the answer is small compared with the strip width, no path outside can beat it.

## When it applies

- The scoring has a dynamic program over an $(m+1) \times (n+1)$ table in which each cell reads its left, upper and upper-left neighbours: [global](/global-alignment/), [local](/local-alignment/) and [semi-global alignment](/semi-global-alignment/), with linear or [affine gap penalties](/affine-gap-alignment/), and edit distance.
- The caller knows a diagonal near which a good alignment lies: the two sequences have about the same length and are similar, or a seed hit, a chain of hits or a previous alignment gives a diagonal, as in [seed-and-extend](/seed-and-extend/).
- For an exact result, there is a bound on how far an optimal path can stray. With unit costs and distance at most $k$, every optimal path stays within $k$ diagonals of both diagonal $0$ and diagonal $n - m$, the band of the [k-differences problem](/k-differences-problem/).
- The band must contain the start and end cells: for global alignment, $lo \le \min(0, n - m)$ and $hi \ge \max(0, n - m)$.

## The template

Let $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$. The holes are CELL, the recurrence of the underlying dynamic program, and the band $[lo, hi]$. A neighbour outside the band, or outside the table, reads as $-\infty$ for a score and $+\infty$ for a cost.

```pseudo id=main
BANDED-DP(x, y, lo, hi, CELL)                      ▷ band of diagonals lo ≤ j − i ≤ hi
L1  require lo ≤ min(0, n − m) and hi ≥ max(0, n − m)
L2  for i ← 0 to m do
L3      for j ← max(0, i + lo) to min(n, i + hi) do
L4          V[i][j] ← CELL(i, j), reading V only at cells inside the band
L5  return V[m][n]                                 ▷ the best value over paths inside the band
```

Row $i$ has at most $w = hi - lo + 1$ cells, at columns $i + lo$ to $i + hi$. Storing row $i$ in an array of length $w$ indexed by $j - i - lo$ gives $O(w)$ memory per row: the upper neighbour $(i - 1, j)$ is at offset $j - i - lo + 1$ of the previous row, the diagonal neighbour $(i - 1, j - 1)$ at the same offset $j - i - lo$, and the left neighbour at offset $j - i - lo - 1$ of the current row.

**What the template computes.** By induction over the cells, $V[i][j]$ is the best value of a path from $(0, 0)$ to $(i, j)$ that uses only band cells: CELL takes the best over the last step, and a missing neighbour removes exactly the paths through it. So line L5 returns the optimum over in-band alignments. Every in-band alignment is an alignment, so for a score this is a lower bound on the true optimum, and for a cost an upper bound.

**Band doubling for edit distance.** Let $\delta = n - m$. A path that touches diagonal $t$ goes from diagonal $0$ to $t$ and from $t$ to $\delta$, and each insertion or deletion moves it by one diagonal, so it has at least $|t| + |\delta - t|$ insertions and deletions and costs at least that much. For a threshold $T \ge |\delta|$, the diagonals with $|t| + |\delta - t| \le T$ form the band

$$lo = \min(0, \delta) - \lfloor (T - |\delta|)/2 \rfloor, \qquad hi = \max(0, \delta) + \lfloor (T - |\delta|)/2 \rfloor.$$

Every path that leaves this band costs more than $T$. So if the banded value $v$ is at most $T$, it is the edit distance: it is the cost of a real alignment, and every other alignment either lies in the band, and costs at least $v$, or leaves it, and costs more than $T \ge v$. If $v > T$, double $T$ and repeat, starting from $T = \max(1, |\delta|)$.

```pseudo id=doubling
BAND-DOUBLING(x, y)                                ▷ unit-cost edit distance
D1  δ ← n − m; T ← max(1, |δ|)
D2  loop
D3      lo ← min(0, δ) − ⌊(T − |δ|)/2⌋; hi ← max(0, δ) + ⌊(T − |δ|)/2⌋
D4      v ← BANDED-DP(x, y, lo, hi, the edit distance recurrence)
D5      if v ≤ T then return v
D6      T ← 2T
```

Once $T \ge D$, an optimal path lies in the band, so $v = D \le T$ and the loop stops. Each round costs $O((T + 1)(\min(m, n) + 1))$, because the band has about $T + 1$ diagonals and each diagonal has at most $\min(m, n) + 1$ cells. The thresholds grow geometrically and the last one is below $2\max(D, 1)$, so the total is $O((D + 1)(\min(m, n) + 1))$.

**Example.** Let $x = \texttt{ACGTACGTACGTACGTACGT}$ and $y = \texttt{ACGTACGTTACGTACGACGT}$, both of length 20, so $\delta = 0$.

| round | $T$ | band | cells | banded distance | result |
|---|---|---|---|---|---|
| 1 | 1 | $[0, 0]$ | 21 | 8 | $8 > 1$, double |
| 2 | 2 | $[-1, 1]$ | 61 | 2 | $2 \le 2$, return 2 |

The band $[0, 0]$ allows no insertion or deletion, so it gives the Hamming distance, 8. The band $[-1, 1]$ finds the true distance 2: $y$ has an extra $\texttt{T}$ at position 9, and the $\texttt{T}$ at position 16 of $x$ has no partner in $y$. The two rounds fill 82 cells; the full table has $21 \cdot 21 = 441$.

## Classic examples

- **FASTA.** After it finds the best ungapped regions, [FASTA](/fasta-algorithm/) runs a Smith-Waterman alignment in a band of fixed width centred on the diagonal of the best initial region. Pearson and Lipman described this as the optimization step.
- **Bounded edit distance.** For the [k-differences problem](/k-differences-problem/) between two strings, a band of $2k + 1$ diagonals around the main diagonal decides whether the distance is at most $k$ in $O(kn)$ time. The [Ukkonen cutoff algorithm](/ukkonen-cutoff-algorithm/) and the [Landau-Vishkin algorithm](/landau-vishkin-algorithm/) refine the same diagonal argument.
- **Diff.** The [Myers diff](/myers-diff/) algorithm finds a shortest edit script with only insertions and deletions in $O((m + n)D)$ time by exploring diagonals outward from the main one, a band that grows as needed.
- **Banded local alignment.** The [banded Smith-Waterman](/banded-smith-waterman/) aligns the region around a seed in a band, in seed-and-extend tools for proteins and DNA.
- **Read mapping.** [Minimap2](/minimap2/) and [BWA](/bwa/) align the gaps between anchors and the read ends with affine-gap dynamic programming inside a band whose width the user can set.

## Variations

- **Doubling, Fickett and Ukkonen.** Fickett (1984) computed only the part of the matrix that can contain an alignment with cost below a bound, and raised the bound when the result did not fit. Ukkonen (1985) gave the band and the doubling for edit distance with a proof of the $O(D \cdot \min(m, n))$ bound.
- **Linear space.** Chao, Pearson and Miller (1992) align within a band in $O(NW)$ time and $O(N)$ space, for $N$ the length of the shorter sequence and $W$ the band width, by combining the band with the divide and conquer of the [Hirschberg algorithm](/hirschberg-algorithm/). For local alignment they first find the start and end of the best local alignment in the band, then align that region globally.
- **Affine gaps.** The three tables of the [Gotoh algorithm](/gotoh-algorithm/) are banded in the same way, with the same offsets.
- **Adaptive bands.** Some aligners do not fix the band. They move a band of constant width along the table, shifting it toward the best cell of the last anti-diagonal, so that the band follows a drifting path. This is a heuristic.
- **Score drop instead of a band.** [X-drop extension](/x-drop-extension/) keeps the cells whose score is within $X$ of the best score so far; the region it explores can wander over many diagonals.

## Pitfalls

- **A narrow band without a check gives a wrong answer silently.** In the example above, the fixed band $[0, 0]$ returns 8 for a pair at distance 2. Use a bound proof, band doubling, or a test such as $v \le T$ before calling the result optimal.
- **The band misses the corner.** For global alignment with $n \ne m$, a band centred on diagonal $0$ with $hi < n - m$ does not contain $(m, n)$ at all. Line L1 checks this.
- **Indices in compressed rows.** Rows stored by offset $j - i - lo$ shift by one position from row to row. Reading the upper neighbour at the same offset reads the diagonal neighbour instead, and the program still runs, with wrong values.
- **Cells just outside the band.** The first and last cells of each row have neighbours outside the band. These must read as $-\infty$ for a score or $+\infty$ for a cost, not as $0$ or as a value left over from an earlier row.
- **The doubling test needs unit costs.** The bound "a path through diagonal $t$ costs at least $|t| + |\delta - t|$" uses a cost of at least 1 per insertion and deletion. With general scores, derive the band from the actual minimum gap cost, or use a fixed band as a heuristic.

## Exercises

1. Show that the band $|t| + |\delta - t| \le T$ is exactly the interval $[lo, hi]$ given in the template.
2. Prove that band doubling computes $O((D + 1)(\min(m, n) + 1))$ cells, and give the constant for the case $m = n$.
3. Adapt the doubling test to the cost model with substitution cost 1 and insertion and deletion cost $c \ge 1$.
4. Give two sequences and a band of width 3 around diagonal $0$ for which the banded global alignment score with match $+1$, mismatch $-1$ and gap $-1$ is lower than the true optimum.

## References
