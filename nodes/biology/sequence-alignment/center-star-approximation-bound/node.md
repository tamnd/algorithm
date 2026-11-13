---
tag: YAE5ER
kind: theorem
slug: center-star-approximation-bound
name: Center-star approximation bound
aliases:
- 2-approximation for sum-of-pairs
- Gusfield bound
area: biology/sequence-alignment
level: advanced
summary: For a metric cost, the center-star alignment of k sequences has sum-of-pairs cost at most 2 - 2/k times the optimum.
prereqs: [center-star-method, sum-of-pairs-score, triangle-inequality, approximation-ratio]
see_also: [multiple-sequence-alignment, msa-np-hardness, metric-space, edit-distance, steiner-tree-problem]
sources:
  - paper: doi:10.1007/BF02460299
    title: Dan Gusfield, Efficient methods for multiple sequence alignment with guaranteed error bounds, Bulletin of Mathematical Biology 55(1), 1993, pages 141 to 154
    locator: the theorem that the center star alignment has SP cost at most 2 - 2/k times optimal when the scores satisfy the triangle inequality
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14, Section 14.6.2 (bounded-error approximation for SP alignment) and Section 14.9
  - book: isbn:9780534952624
    title: João Setubal and João Meidanis, Introduction to Computational Molecular Biology, 1997
    locator: Chapter 3, Section 3.4.2, Star alignments
  - paper: "Vineet Bafna, Eugene L. Lawler and Pavel A. Pevzner, Approximation algorithms for multiple sequence alignment, Theoretical Computer Science 182(1-2), 1997, pages 233 to 244"
    locator: the ratio 2 - l/k for any fixed l < k
---

The center-star approximation bound states that the [center-star method](/center-star-method/) is a $(2 - 2/k)$-approximation for [multiple sequence alignment](/multiple-sequence-alignment/) under the [sum-of-pairs cost](/sum-of-pairs-score/), when the cost of two symbols is a metric. The proof uses only two facts: each sequence keeps its optimal alignment with the center, and the [triangle inequality](/triangle-inequality/) holds column by column. Dan Gusfield proved it in 1993. Because minimizing the sum-of-pairs cost is [NP-hard](/msa-np-hardness/), a polynomial-time method cannot be exact unless P = NP, so an approximation bound of this kind is what one can hope for.

## Statement

Let $\Sigma$ be an alphabet, $- \notin \Sigma$ the gap, and $\Sigma' = \Sigma \cup \{-\}$. Let $\delta : \Sigma' \times \Sigma' \to \mathbb{R}_{\ge 0}$ be a metric on $\Sigma'$: $\delta(x, y) = 0$ if and only if $x = y$, $\delta(x, y) = \delta(y, x)$, and $\delta(x, z) \le \delta(x, y) + \delta(y, z)$. In particular $\delta(-, -) = 0$. Let $S_1, \ldots, S_k$ be sequences over $\Sigma$, with $k \ge 2$.

For an alignment $A$ (rows $A_1, \ldots, A_k$ of equal length, row $A_i$ equal to $S_i$ when its gaps are removed), write $d_A(i, j) = \sum_p \delta(A_i[p], A_j[p])$ for the cost of the pair of rows $i, j$, and $\mathrm{SP}(A) = \sum_{i < j} d_A(i, j)$. Let $D(i, j)$ be the optimal cost of a pairwise alignment of $S_i$ and $S_j$, and $\mathrm{OPT}$ the smallest $\mathrm{SP}(A)$ over all alignments $A$.

**Theorem (Gusfield 1993).** Let $c$ be an index that minimizes $\sum_j D(c, j)$, and let $M$ be any alignment of $S_1, \ldots, S_k$ with $d_M(c, i) = D(c, i)$ for every $i$. Then

$$\mathrm{SP}(M) \le \Big(2 - \frac{2}{k}\Big)\, \mathrm{OPT}.$$

The [center-star method](/center-star-method/) returns such an alignment $M$, so it is a $(2 - 2/k)$-approximation algorithm.

## In plain words

The method picks the sequence that is closest, in total, to all the others, and lines up every other sequence with it as well as possible.

For two sequences that are not the center, their cost in this alignment is at most the cost of going from the first sequence to the center and then from the center to the second. This is the triangle inequality. Adding these detours over all pairs counts each distance to the center about twice.

On the other side, no alignment can make two sequences cost less than their best pairwise alignment. Since the center has the smallest total distance, the best alignment costs at least about half of what the detours count.

Together these two facts give a factor of at most two, and a little less when there are few sequences.

## Proof

Write $S = \sum_{j=1}^{k} D(c, j)$. Note $D(c, c) = 0$.

**Step 1: pairs of rows cost what their pairwise alignments cost.** For any alignment $A$ and rows $i \ne j$, remove the columns where both $A_i$ and $A_j$ have a gap. What is left is a pairwise alignment of $S_i$ and $S_j$, and it has the same cost $d_A(i, j)$, because $\delta(-, -) = 0$. Hence $d_A(i, j) \ge D(i, j)$, and $\mathrm{SP}(A) = \sum_{i<j} d_A(i, j)$ is a sum over pairs of rows.

**Step 2: upper bound.** For any column $p$ of $M$ and any $i, j$, the triangle inequality on $\Sigma'$ gives

$$\delta(M_i[p], M_j[p]) \le \delta(M_i[p], M_c[p]) + \delta(M_c[p], M_j[p]).$$

Summing over all columns $p$,

$$d_M(i, j) \le d_M(i, c) + d_M(c, j) = D(i, c) + D(c, j).$$

This also holds when $i = c$ or $j = c$, with $d_M(c, c) = 0$. Count each unordered pair twice:

$$2\,\mathrm{SP}(M) = \sum_{i=1}^{k} \sum_{j \ne i} d_M(i, j) \le \sum_{i=1}^{k} \sum_{j \ne i} \big(D(i, c) + D(c, j)\big).$$

For a fixed $i$, the inner sum of $D(i, c)$ is $(k - 1) D(i, c)$, so these terms add up to $(k-1) S$. For a fixed $i$, the inner sum of $D(c, j)$ over $j \ne i$ is $S - D(c, i)$, so these terms add up to $kS - S = (k-1) S$. Therefore

$$2\,\mathrm{SP}(M) \le 2(k - 1)\, S.$$

**Step 3: lower bound.** Let $A^{*}$ be an optimal alignment. By Step 1,

$$2\,\mathrm{OPT} = \sum_{i=1}^{k} \sum_{j \ne i} d_{A^{*}}(i, j) \ge \sum_{i=1}^{k} \sum_{j=1}^{k} D(i, j) \ge \sum_{i=1}^{k} S = kS,$$

where the last step uses that $c$ minimizes the row sum $\sum_j D(i, j)$.

**Step 4: the ratio.** If $S = 0$, Step 2 gives $\mathrm{SP}(M) = 0 \le (2 - 2/k)\,\mathrm{OPT}$. Otherwise Steps 2 and 3 give

$$\mathrm{SP}(M) \le (k - 1)\, S = \frac{2(k-1)}{k} \cdot \frac{kS}{2} \le \Big(2 - \frac{2}{k}\Big)\,\mathrm{OPT}. \qquad \blacksquare$$

The proof needs $d_M(c, i) = D(c, i)$ for each $i$. For the alignment that the center-star method builds, this is the projection property proved in the [correctness proof of the method](/center-star-method/).

## Consequences

- **A polynomial-time approximation.** The center-star method takes $O(k^2 n^2 + k^3 n)$ time, so the sum-of-pairs problem with a metric cost has a polynomial-time approximation algorithm with ratio below 2, while the exact problem is NP-hard.
- **A lower bound for exact search.** Step 3 gives $\mathrm{OPT} \ge \frac{1}{2} \sum_{i \ne j} D(i, j)$ for every instance, with no condition on the center. Exact methods such as the Carrillo-Lipman pruning use the pairwise costs as lower bounds of this kind, and the center-star cost as an upper bound.
- **Any star works for the upper bound.** Step 2 holds for any index $c$ and any alignment that keeps the optimal pairwise alignments with $c$: $\mathrm{SP}(M) \le (k - 1) \sum_j D(c, j)$. Only Step 3 needs the minimizing center.
- **Better ratios.** The same method of proof, with small groups of sequences aligned exactly to the center, gives the ratio $2 - 3/k$ of Pevzner (1992) and $2 - l/k$ for any fixed $l < k$ of Bafna, Lawler and Pevzner (1997).

## Tightness

The bound is reached for $k = 3$ with the unit cost (the [edit distance](/edit-distance/) cost, a metric). Take $S_1 = \texttt{A}$, $S_2 = \texttt{AC}$, $S_3 = \texttt{AA}$. All three pairwise distances are 1, so each row sum is 2 and any sequence can be the center. With $S_1$ as center, both

```
A-      -A
AC      AA
```

are optimal pairwise alignments with the center. If the method picks these two, the merged alignment is

```
-A-
-AC
AA-
```

with $d(1,2) = 1$, $d(1,3) = 1$ and $d(2,3) = 2$, so its cost is 4. The alignment `A-`, `AC`, `AA` costs 3, which is optimal, because Step 3 gives $\mathrm{OPT} \ge 3$. The ratio is $4/3 = 2 - 2/3$. The example shows that the bound holds for the worst choice among optimal pairwise alignments, and that a method with other tie rules can do better on the same input.

The two inequalities of the proof are both equalities only when every pair $i, j$ costs exactly $D(i, c) + D(c, j)$ in $M$, and when every row sum is equal to $S$ and the optimal alignment induces optimal pairwise alignments for all pairs. The bound also fails without the triangle inequality: for a cost that is not a metric, Step 2 does not hold, and the proof gives no bound.

## History

Gusfield gave the method and the bound in a technical report of the University of California, Davis, in 1991, and in the Bulletin of Mathematical Biology in 1993. Pevzner (1992) improved the ratio to $2 - 3/k$, and Bafna, Lawler and Pevzner (1994 conference, 1997 journal) reached $2 - l/k$ for any fixed $l$. Wang and Jiang proved in 1994 that the exact problem is NP-hard. Gusfield's 1997 book, Chapter 14, gives the proof in the form used here.

## References
