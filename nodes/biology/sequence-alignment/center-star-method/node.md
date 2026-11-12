---
tag: 3K9D30
kind: algorithm
slug: center-star-method
name: Center-star method
aliases:
- star alignment
- center star alignment
area: biology/sequence-alignment
level: core
summary: Align every sequence optimally to the one sequence that is closest to all others, then merge the pairwise alignments. Gives a (2 - 2/k)-approximation for sum-of-pairs cost.
solves: [multiple-sequence-alignment]
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence}
  time: {worst: "O(k^2 n^2 + k^3 n)"}
  space: {extra: "O(n^2 + k^2 n)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1993
  people: [Dan Gusfield]
  note: Gusfield gave the method and its error bound in a 1991 technical report, published in the Bulletin of Mathematical Biology in 1993.
prereqs: [multiple-sequence-alignment, sum-of-pairs-score, needleman-wunsch, edit-distance]
see_also: [center-star-approximation-bound, progressive-alignment, msa-np-hardness, approximation-ratio, global-alignment]
sources:
  - paper: doi:10.1007/BF02460299
    title: Dan Gusfield, Efficient methods for multiple sequence alignment with guaranteed error bounds, Bulletin of Mathematical Biology 55(1), 1993, pages 141 to 154
    locator: the center star alignment for the SP measure and its bound of 2 - 2/k
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14, Section 14.6.2 (alignments consistent with a tree, and Section 14.6.2.2, the center star method for SP alignment)
  - book: isbn:9780534952624
    title: João Setubal and João Meidanis, Introduction to Computational Molecular Biology, 1997
    locator: Chapter 3, Section 3.4.2, Star alignments
---

The center-star method builds a [multiple sequence alignment](/multiple-sequence-alignment/) of $k$ sequences from $k - 1$ optimal pairwise alignments. It picks as *center* the sequence whose total optimal pairwise cost to all the others is smallest, aligns each other sequence to the center with the [Needleman-Wunsch](/needleman-wunsch/) recurrence, and merges these pairwise alignments column by column. When the cost function is a metric, the [sum-of-pairs cost](/sum-of-pairs-score/) of the result is at most $2 - 2/k$ times the optimal cost; the [center-star approximation bound](/center-star-approximation-bound/) page proves this. Dan Gusfield published the method in 1993.

## In plain words

Exact multiple alignment is too slow for many sequences, but the alignment of two sequences is fast. The center-star method uses only pairwise alignments.

First it aligns every pair of sequences and writes down how far apart they are. The sequence with the smallest total distance to all the others becomes the center of a star. Each other sequence is a point of the star, connected only to the center.

Then it aligns each point to the center, one at a time, and adds it to the growing alignment. The center row is the common ruler. If the new pairwise alignment needs a gap in the center, a gap column is added to all rows that are already there. A gap that is in the alignment stays there. So each sequence keeps its best alignment to the center.

## The problem

The input is $k \ge 1$ sequences $S_1, \ldots, S_k$ over an alphabet $\Sigma$, for example DNA with $\Sigma = \{A, C, G, T\}$, each of length at most $n$. Write $\Sigma' = \Sigma \cup \{-\}$, where $-$ is the gap. The cost function $\delta : \Sigma' \times \Sigma' \to \mathbb{Z}_{\ge 0}$ is symmetric and has $\delta(-, -) = 0$. This is a linear gap model: each gap symbol against a letter costs $\delta(x, -)$, so a gap of length $L$ costs $L$ times that amount. The goal is an alignment $A$ (rows $A_1, \ldots, A_k$ of equal length, no column of gaps only, row $A_i$ equal to $S_i$ when its gaps are removed) of small cost

$$\mathrm{SP}(A) = \sum_{i < j} \sum_{p} \delta\big(A_i[p], A_j[p]\big).$$

$D(i, j)$ is the optimal cost of a pairwise alignment of $S_i$ and $S_j$, a weighted [edit distance](/edit-distance/). Minimizing $\mathrm{SP}$ exactly is [NP-hard](/msa-np-hardness/) when $k$ is part of the input, so the method gives up optimality for a bound.

## The algorithm

```pseudo id=main
CENTER-STAR(S[1..k], δ)
L1  for each pair i < j do D[i][j] ← D[j][i] ← optimal pairwise cost of S_i and S_j
L2  c ← the smallest index that minimizes Σ_j D[c][j]
L3  M ← the alignment with the one row S_c
L4  for each i ≠ c, in increasing order do
L5      (C′, T′) ← an optimal pairwise alignment of S_c (row C′) and S_i (row T′)
L6      M ← MERGE(M, C′, T′)
L7  return M, with its rows put in input order

MERGE(M, C′, T′)              ▷ row c of M and the row C′ both spell S_c with gaps
L8  p ← 0, q ← 0, N ← an empty alignment with one more row than M
L9  while p < |M| or q < |C′| do
L10     if p < |M|, q < |C′| and M[c][p], C′[q] are both letters or both gaps then
            add column M[·][p] with T′[q] below it to N, p ← p + 1, q ← q + 1
L11     else if p < |M| and M[c][p] = − then
            add column M[·][p] with − below it to N, p ← p + 1
L12     else                  ▷ C′[q] = −: S_i has a letter that the center does not have
            add a column of gaps with T′[q] below it to N, q ← q + 1
L13 return N
```

Line L1 runs the pairwise dynamic program for every pair. Line L2 picks the center. Lines L4 to L6 add the other sequences one at a time. MERGE walks along the center row of $M$ and the center row $C'$ of the new pairwise alignment. Both rows spell $S_c$, so when both show a letter it is the same letter of $S_c$, and the column is shared (line L10). A gap in the center of $M$ that $C'$ does not have gets a gap in the new row (line L11). A gap in $C'$ that $M$ does not have becomes a new column, with gaps in all old rows (line L12). This is the rule "once a gap, always a gap": MERGE never removes or moves a gap of $M$.

## Example

Take $k = 4$ DNA sequences and unit costs: $\delta(x, x) = 0$, and $\delta(x, y) = 1$ for $x \ne y$, gap included. This is the edit distance, and it is a metric.

$$S_1 = \texttt{ACGTAC},\quad S_2 = \texttt{ACGGTAC},\quad S_3 = \texttt{AGTAC},\quad S_4 = \texttt{CGTTAC}.$$

| $D$ | $S_1$ | $S_2$ | $S_3$ | $S_4$ | row sum |
|---|---|---|---|---|---|
| $S_1$ | 0 | 1 | 1 | 2 | **4** |
| $S_2$ | 1 | 0 | 2 | 2 | 5 |
| $S_3$ | 1 | 2 | 0 | 2 | 5 |
| $S_4$ | 2 | 2 | 2 | 0 | 6 |

The center is $S_1$. The pairwise alignments of line L5, and the alignment $M$ after each merge:

| step | pairwise alignment (center over $S_i$) | $M$ after MERGE |
|---|---|---|
| start | | `ACGTAC` |
| $i = 2$ | `AC-GTAC` over `ACGGTAC` | `AC-GTAC`, `ACGGTAC` |
| $i = 3$ | `ACGTAC` over `A-GTAC` | `AC-GTAC`, `ACGGTAC`, `A--GTAC` |
| $i = 4$ | `ACG-TAC` over `-CGTTAC` | `AC-G-TAC`, `ACGG-TAC`, `A--G-TAC`, `-C-GTTAC` |

In the last step, $C' = $ `ACG-TAC` has a gap after `G` that $M$ does not have, so line L12 adds a new column, with gaps in the three old rows. The final alignment is

```
S1  AC-G-TAC
S2  ACGG-TAC
S3  A--G-TAC
S4  -C-GTTAC
```

Its sum-of-pairs cost is 12. The optimal sum-of-pairs cost of these four sequences is 11, so the ratio is $12/11 \approx 1.09$, well under the bound $2 - 2/4 = 1.5$.

## Correctness

The output is a valid alignment of the input, and it keeps each pairwise alignment with the center: for each $i$, the rows $c$ and $i$ of the output, with their columns of two gaps removed, are exactly the pair $(C', T')$ that line L5 computed for $S_i$, so their cost is $D(c, i)$. The proof is an invariant of the MERGE loop: the columns of $N$ written so far, restricted to the old rows, are $M[\cdot][0 \ldots p-1]$, and restricted to rows $c$ and the new row they are $(C'[0 \ldots q-1], T'[0 \ldots q-1])$ with some columns of two gaps added. Later merges only add columns of gaps in old rows, which do not change a projection. The full proof is in the proof file. The cost bound $\mathrm{SP}(M) \le (2 - 2/k)\,\mathrm{OPT}$ for a metric $\delta$ follows from this property and the triangle inequality; it is proved on the [center-star approximation bound](/center-star-approximation-bound/) page.

## Complexity

The model is the word RAM, with one unit for each evaluation of $\delta$.

- **Line L1.** There are $\binom{k}{2}$ pairs. Each pairwise table has at most $(n+1)^2$ cells, with three terms in each cell. This is $O(k^2 n^2)$ time.
- **Line L2.** $O(k^2)$ time for the row sums.
- **Line L5.** $k - 1$ more tables, $O(k n^2)$ time. A program can keep the tracebacks of line L1 instead, at the cost of more space.
- **Lines L6 and L8 to L13.** MERGE writes each column of $N$ once, and a column has at most $k$ symbols. The center adds at most $n$ columns, and each other sequence adds at most $n$ columns in line L12, so $|M| \le kn$ at all times. The $k - 1$ merges take $O(k \cdot k \cdot kn) = O(k^3 n)$ time.

The total is $O(k^2 n^2 + k^3 n)$ time in the worst case. The extra space is $O(n^2)$ for one pairwise table and $O(k^2 n)$ for the alignment. A merge that first records, for each gap slot of the center, the largest number of letters that any sequence inserts there, and then writes each row once, takes $O(k^2 n)$ time in total, so the time becomes $O(k^2 n^2)$.

## Properties

- **Approximation ratio.** For a metric $\delta$ with $\delta(-,-) = 0$, $\mathrm{SP}(M) \le (2 - 2/k)\,\mathrm{OPT}$. For $k = 3$ the ratio $4/3$ is attained (see [the bound page](/center-star-approximation-bound/)).
- **Exact for two sequences.** For $k = 2$ the output is an optimal pairwise alignment.
- **Deterministic.** The tie rules of line L2 (smallest index) and of the pairwise traceback fix the output. A different optimal pairwise alignment in line L5 can change the sum-of-pairs cost, but not the bound.
- **Order of merges.** With the rule "once a gap, always a gap", the order of the loop in line L4 changes only the order of gap columns inside one gap slot of the center, never the projections onto the center.

## Variants and improvements

- **Better ratios.** Pevzner (1992) improved the ratio to $2 - 3/k$, and Bafna, Lawler and Pevzner (1997) to $2 - l/k$ for any fixed $l < k$, by aligning small groups of sequences exactly instead of single sequences to one center.
- **Tree alignments.** The center star is the special case of an alignment consistent with a tree, where the tree is a star. [Progressive alignment](/progressive-alignment/) merges along a guide tree instead, but without a proved bound.
- **Similarity scores.** With scores to maximize, such as [BLOSUM](/blosum-matrix/) entries, the bound does not hold, because the proof needs costs that obey the [triangle inequality](/triangle-inequality/).

## When to use it

Use the center-star method when you need a multiple alignment with a proved bound, or a quick upper bound on the optimal SP cost to prune an exact search such as the Carrillo-Lipman method. It suits sets of sequences that are all close to one of them. For sets with clear subfamilies, a [progressive](/progressive-alignment/) aligner such as [Clustal](/clustal/) or [MUSCLE](/muscle/) usually gives alignments that biologists prefer, although they have no worst-case bound.

## Pitfalls

- **Similarity scores in place of costs.** The bound holds only for a metric cost. With a similarity matrix, or with $\delta(x, x) > 0$, the proof fails, and the output has no guarantee.
- **Affine gaps.** With an [affine gap penalty](/affine-gap-penalty/), the cost of a pair of rows is not a sum over columns. The pairs with the center still cost $D(c, i)$, but the triangle inequality per column does not bound the other pairs, so the proof fails.
- **Moving old gaps in MERGE.** If line L10 accepted a letter of $C'$ against a gap of $M$, the old rows would shift, and the projection of an earlier sequence onto the center would change. Keep the three cases of lines L10 to L12.
- **Choosing the center by length.** The center must minimize $\sum_j D(c, j)$ in line L2. Another choice keeps the output valid, but the proof of the bound uses this minimum.

## Implementations

## History

Dan Gusfield described the method, with its bound $2 - 2/k$, in a 1991 technical report of the University of California, Davis, and in the Bulletin of Mathematical Biology in 1993. Pevzner and then Bafna, Lawler and Pevzner improved the ratio, and Wang and Jiang proved in 1994 that the exact problem is NP-hard.

## References
