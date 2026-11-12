---
tag: HKPH6N
kind: technique
slug: x-drop-extension
name: X-drop extension
aliases:
- X-drop heuristic
- X-drop rule
area: biology/sequence-alignment
level: advanced
summary: Extend an alignment outward from a seed and stop when the score falls more than X below the best score seen so far; fast, but it can miss a better alignment.
prereqs: [seed-and-extend, smith-waterman]
see_also: [blast, high-scoring-segment-pair, banded-smith-waterman, minimap2, kadane-algorithm, maximum-subarray-problem, karlin-altschul-statistics, banded-alignment]
sources:
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990, 403-410
    locator: the extension of word hits without gaps, stopped when the score falls a fixed distance below the best score of shorter extensions
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schaffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, a new generation of protein database search programs, Nucleic Acids Research 25(17), 1997, 3389-3402
    locator: the two-hit method, and the gapped extension by dynamic programming that drops cells whose score falls more than X_g below the best score
  - paper: doi:10.1089/10665270050081478
    title: Zheng Zhang, Scott Schwartz, Lukas Wagner and Webb Miller, A greedy algorithm for aligning DNA sequences, Journal of Computational Biology 7(1-2), 2000, 203-214
    locator: the X-drop condition for gapped alignment, its dynamic programming form, and the greedy algorithm of MegaBLAST
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018, 3094-3100
    locator: the Z-drop rule, an X-drop variant that does not count a long gap against the drop
---

X-drop extension is a technique for extending an alignment from a seed: it adds columns outward from the seed and stops as soon as the running score falls more than a fixed amount $X$ below the best score seen so far, then keeps the extension that reached that best score. [BLAST](/blast/) introduced it in 1990 for ungapped extension of word hits, and Gapped BLAST (1997) applied it to dynamic programming, where cells that fall more than $X$ below the best are dropped. The work then depends on the length of the similar region, not on the length of the sequences. The rule is a heuristic: an alignment that must pass through a low-scoring stretch deeper than $X$ is cut off, even when the region beyond it would score higher.

## In plain words

A search tool has found a short exact match between two sequences, the seed. The true similar region is probably longer, so the tool grows the match outward, one letter pair at a time, and keeps a running score.

Inside a similar region the score mostly goes up. After the region ends, the letters are unrelated and the score mostly goes down. The tool remembers the highest score so far. When the score has dropped more than a chosen amount below that high point, the tool assumes that the region has ended, stops, and cuts the match back to the high point.

This is fast, because the tool looks only a little past the end of the region. The price is that a short bad stretch inside a long good region can stop the growth too early.

## When it applies

- A seed or an anchor is known, and the goal is the best extension from it, not the best alignment anywhere in the two sequences.
- The scores are such that random letter pairs have a negative expected score, as for any [substitution matrix](/substitution-matrix/) used in search. Then the score of an extension past the end of the true region drifts downward, and the drop happens soon.
- A good alignment is not expected to contain long stretches with a negative total. The rule cuts off any extension that needs to cross such a stretch whose loss exceeds $X$.
- The extension is done separately in each direction from the seed; the left extension uses the reversed prefixes.

## The template

Both procedures extend to the right from the end of a seed. The sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ are the parts after the seed, $s$ is the scoring matrix, and $X \ge 0$. The gapped version uses a [linear gap penalty](/linear-gap-penalty/) $g$ per space to keep it short; the affine version keeps the three tables of the [Gotoh algorithm](/gotoh-algorithm/) and applies the same rule to them.

```pseudo id=main
UNGAPPED-X-DROP(x, y, s, X)                    ▷ extends along one diagonal
L1  t ← 0; best ← 0; ℓ ← 0; k ← 0
L2  while k < m and k < n do
L3      k ← k + 1; t ← t + s(x_k, y_k)
L4      if t > best then best ← t; ℓ ← k
L5      else if t < best − X then exit the loop
L6  return best, ℓ                             ▷ the extension is x_1..x_ℓ over y_1..y_ℓ

GAPPED-X-DROP(x, y, s, g, X)                   ▷ dynamic programming with pruning
L7  best ← 0; (bi, bj) ← (0, 0); every entry of S reads −∞ until set
L8  for i ← 0 to m do
L9      a ← 0 if i = 0, else the first live column of row i − 1; b ← −1 if i = 0, else the last live column of row i − 1
L10     for j ← a to n do
L11         S[i][j] ← 0 if i = j = 0, else max(S[i−1][j−1] + s(x_i, y_j), S[i−1][j] − g, S[i][j−1] − g)
L12         if S[i][j] < best − X then S[i][j] ← −∞                   ▷ the cell is dead
L13         else if S[i][j] > best then best ← S[i][j]; (bi, bj) ← (i, j)
L14         if j > b and S[i][j] = −∞ then exit the inner loop
L15     if row i has no live cell then exit the outer loop
L16 return best, (bi, bj)                      ▷ trace back from (bi, bj) for the alignment
```

A cell is *live* when its value is finite. A cell left of the first live column of the row above has dead neighbours above, on the diagonal and to the left, so line L10 starts at $a$. A cell right of the last live column of the row above can only be reached from its left neighbour, so after one dead cell there, all cells to its right are dead too, which justifies line L14. Line L15 ends the extension when a whole row is dead.

**What the rule guarantees.** The values that the procedures keep are scores of real extensions, so $best$ never exceeds the optimal extension score $OPT$. Let $P$ be an optimal extension path. If every prefix of $P$ scores at least $OPT - X$, then each cell of $P$ holds at least the score of its prefix, by induction along $P$; that value is at least $OPT - X \ge best - X$, so line L5 or L12 never fires on $P$, and the procedure returns $OPT$. With $X = \infty$ nothing is dropped: the ungapped version returns the maximum prefix sum, and the gapped version returns the best score of an alignment of $x_1 \cdots x_i$ with $y_1 \cdots y_j$ over all $(i, j)$. Without this condition the result can be lower than $OPT$.

**Cost.** The ungapped version takes $O(\ell + r)$ time, where $r$ is the number of steps after the best point before the drop. For a random continuation with negative expected score per column, $r$ is about $X$ divided by the expected loss per column. The gapped version computes only the live cells and their immediate neighbours, about the area of a band around the alignment whose width depends on $X$ and the gap penalty. With $X = \infty$ it computes all $(m + 1)(n + 1)$ cells.

**Example where it misses (ungapped).** Let $x = \texttt{ACGGACGTACGTAC}$ and $y = \texttt{ACTTACGTACGTAC}$, match $+1$, mismatch $-3$. The column scores are $1, 1, -3, -3$, then ten times $1$, and the running sums are $1, 2, -1, -4, -3, -2, \ldots, 6$. The best full extension has score $6$ at length $14$. With $X = 5$, the sum $-4$ after column 4 is below $best - X = 2 - 5 = -3$, so the loop stops and returns score $2$ at length $2$. With $X = 6$ the sum $-4$ is not below $-4$, the loop continues, and it returns $6$ at length $14$.

**Example (gapped).** Let $x = \texttt{ACGTACGTAC}$, $y = \texttt{ACGTAGGGCGTAC}$, match $+2$, mismatch $-3$, $g = 2$. The best extension is $\texttt{ACGTA---CGTAC}$ over $\texttt{ACGTAGGGCGTAC}$, score $20 - 6 = 14$, and its prefix score falls from $10$ to $4$ in the gap. With $X = 5$ the procedure returns $10$ at cell $(5, 5)$ after 57 cells. With $X = 6$ it returns $14$ at cell $(10, 13)$ after 87 cells. The full table has $11 \cdot 14 = 154$ cells.

## Classic examples

- **BLAST, 1990.** Each word hit is extended without gaps in both directions, stopping when the score falls more than $X$ below the best; the result is a [high-scoring segment pair](/high-scoring-segment-pair/). The X-drop stop can miss part of a segment pair, and the paper accepts this for speed.
- **Gapped BLAST, 1997.** Two hits on the same diagonal within a short distance trigger an ungapped X-drop extension. If it scores high enough, a gapped extension by dynamic programming starts from a point inside it, in both directions, and drops every cell whose score falls more than $X_g$ below the best. The score is then judged with [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- **MegaBLAST.** Zhang, Schwartz, Wagner and Miller (2000) gave a greedy algorithm for DNA that visits cells in order of their distance in edits and applies the X-drop condition. For scores of a certain form it returns the same result as the dynamic programming X-drop, and it is much faster on similar sequences.
- **Read and genome aligners.** Many seed-and-extend tools, including LASTZ and the extension in [minimap2](/minimap2/), run a banded or pruned alignment with an X-drop style stop; see [seed-and-extend](/seed-and-extend/).

## Variations

- **Affine gaps.** Keep the tables $M$, $X$, $Y$ of the Gotoh algorithm and call a cell dead when all three are below $best - X$.
- **Anti-diagonal order.** Process the cells by anti-diagonal $i + j$ instead of by row. The cells of one anti-diagonal do not depend on each other, which suits vector instructions, and the live range on each anti-diagonal stays short.
- **Z-drop.** Minimap2 stops when the score at $(i, j)$ falls more than $Z + e \cdot |(i - i') - (j - j')|$ below the best score at $(i', j')$, where $e$ is the gap extension score. A long gap shifts the diagonal and raises the allowed drop, so the extension can cross a long deletion that X-drop would cut, while a stretch of mismatches on one diagonal still stops it.
- **Band plus X-drop.** The [banded Smith-Waterman](/banded-smith-waterman/) and the X-drop rule are often combined: the band limits the diagonals, and the drop limits the length.
- **Choosing X.** The drop is usually given in bits and converted to raw score with the $\lambda$ of the scoring system, so the same setting means the same thing for different matrices. The ungapped drop is set small and the gapped drop larger.

## Pitfalls

- **Missing a better alignment.** A drop deeper than $X$ inside a true region cuts it, as in the ungapped example: two mismatches under $+1/-3$ scoring cost 6 and lose the remaining 8 matches. The procedure gives no sign that it stopped early. Increase $X$, or check the result with the full [Smith-Waterman](/smith-waterman/) algorithm when the answer matters.
- **Strict or weak comparison.** Line L5 tests $t < best - X$. Some programs stop when $t \le best - X$. The two differ exactly at a drop of $X$, as in the example with $X = 6$, so results of two programs can differ by one setting.
- **Returning the stop point.** The extension ends at the best point $\ell$, not at the point $k$ where the loop stopped. Returning $k$ adds a tail with a negative score.
- **Stale entries.** In the gapped version, an entry from an earlier row that was not recomputed must read $-\infty$. Reusing a row array without clearing the cells that the current row does not compute lets old values come back as live cells.
- **Pruning by the current best inside a row.** In the gapped version, $best$ can rise during a row, so the same cell can be live or dead depending on the order in which cells are processed. Tools that process by anti-diagonal and update $best$ once per anti-diagonal give slightly different results. Both are heuristics; compare tools only with the same order.

## Exercises

1. Show that with $X = \infty$ the ungapped procedure computes the maximum prefix sum of the column scores, and relate it to [Kadane's algorithm](/kadane-algorithm/) for the [maximum subarray problem](/maximum-subarray-problem/).
2. Give, for every $X$, a pair of sequences under $+1/-3$ scoring on which the ungapped procedure returns less than half of the best extension score.
3. Prove the statement after the template: if every prefix of an optimal path scores at least $OPT - X$, the gapped procedure returns $OPT$.
4. For column scores that are independent with mean $\mu < 0$ after the end of the true region, estimate the expected number of extra columns read before the drop.
5. Write the affine version of lines L11 to L13 with three tables, and decide which of the three values must be below $best - X$ for the cell to be dead.

## References
