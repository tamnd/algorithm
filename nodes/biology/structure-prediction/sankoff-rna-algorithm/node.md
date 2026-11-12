---
tag: XKWWEX
kind: algorithm
slug: sankoff-rna-algorithm
name: Sankoff's RNA algorithm
aliases:
- Sankoff simultaneous alignment and folding
area: biology/structure-prediction
level: research
summary: "Dynamic program that aligns two RNA sequences and folds them into one common nested structure at the same time. Theta(m^3 n^3) time and Theta(m^2 n^2) space; O(n^(3k)) time for k sequences."
solves: [simultaneous-alignment-and-folding]
model: word-ram
complexity:
  vars: {m: the length of the first sequence, n: the length of the second sequence}
  time: {worst: Θ(m^3 n^3), average: Θ(m^3 n^3), best: Θ(m^3 n^2)}
  space: {extra: Θ(m^2 n^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1985
  people: [David Sankoff]
  note: Sankoff gave the joint dynamic program for folding, alignment and ancestral sequences of k RNA sequences on a tree, with O(n^(3k)) time.
prereqs: [simultaneous-alignment-and-folding, nussinov-algorithm, needleman-wunsch]
see_also: [covariance-model, mccaskill-algorithm, zuker-algorithm, banded-alignment, progressive-alignment, interval-dp, traceback, rna-homology-search]
sources:
  - paper: doi:10.1137/0145048
    title: David Sankoff, Simultaneous solution of the RNA folding, alignment and protosequence problems, SIAM Journal on Applied Mathematics 45(5), 1985, pages 810 to 825
    locator: the joint objective, the dynamic program over pairs of subsequences, and its O(n^(3k)) time for k sequences
  - paper: doi:10.1371/journal.pcbi.0030065
    title: Sebastian Will, Kristin Reiche, Ivo L. Hofacker, Peter F. Stadler and Rolf Backofen, Inferring noncoding RNA families and classes by means of genome-scale structure-based clustering, PLoS Computational Biology 3(4), 2007, e65
    locator: the statement that the full Sankoff problem for two sequences needs O(n^6) time and O(n^4) memory, and the sparse variant LocARNA
  - paper: doi:10.1006/jmbi.2001.5351
    title: David H. Mathews and Douglas H. Turner, Dynalign, an algorithm for finding the secondary structure common to two RNA sequences, Journal of Molecular Biology 317(2), 2002, pages 191 to 203
    locator: a banded energy-based form of the Sankoff recursion for two sequences
  - paper: doi:10.1093/nar/25.18.3724
    title: Jan Gorodkin, Laurie J. Heyer and Gary D. Stormo, Finding the most significant common sequence and structure motifs in a set of RNA sequences, Nucleic Acids Research 25(18), 1997, pages 3724 to 3732
    locator: Foldalign, a local and simplified form of the Sankoff recursion
---

The Sankoff algorithm is a dynamic program that solves [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) exactly: it finds an alignment of two RNA sequences and one nested structure on the aligned columns that together get the best score. It runs the [Nussinov](/nussinov-algorithm/) interval recursion on both sequences at once, so a table cell is a pair of intervals, one in each sequence, and the cost is $\Theta(m^2 n^2)$ cells and $\Theta(m^3 n^3)$ time for lengths $m$ and $n$, which is $O(n^6)$ for two sequences of length $n$. David Sankoff gave it in 1985 for $k$ sequences on a tree, at $O(n^{3k})$ time. It is not the [Sankoff algorithm for weighted small parsimony](/sankoff-algorithm/) on a phylogenetic tree, an older method by the same author.

## In plain words

You have two RNA molecules that should fold into the same shape. You want to line them up letter by letter and, at the same time, find the shape they share.

The method works on a piece of each molecule at a time and decides what to do with the two first letters. Either one of them faces a gap, or they face each other and stay unpaired, or they face each other and both pair with letters further on, which also face each other. In the last case the pieces split into the part inside the pair and the part after it.

The best answer for each pair of pieces goes into a table. The table is large: it has one entry for each piece of the first molecule and each piece of the second.

## The problem

**Input.** Two RNA sequences $x = x_0 \cdots x_{m-1}$ and $y = y_0 \cdots y_{n-1}$ over A, C, G and U.

**Model of the structure.**

- Allowed base pairs are the Watson-Crick pairs A-U and C-G and the wobble pair G-U, in either order.
- A pair must close a hairpin of at least $h_{\min}$ unpaired bases in each sequence: a pair of $x_i$ with $x_h$ needs $h - i - 1 \ge h_{\min}$, and the same for $y$. The toy scheme on this page uses $h_{\min} = 1$.
- Pairs are nested; there are no [pseudoknots](/pseudoknot/).
- The structure score is a pair count, as in the Nussinov algorithm, not a free energy.

**Score.** A solution is an alignment of $x$ and $y$ with a set of consensus pairs of columns. A consensus pair joins two match columns $(x_i, y_k)$ and $(x_h, y_q)$ such that $x_i x_h$ and $y_k y_q$ are both allowed pairs that meet the hairpin rule. Its score is

$$\sum_{\text{match columns}} \sigma(x_i, y_k) \;-\; d \cdot \#\text{gap columns} \;+\; \beta \cdot \#\text{consensus pairs},$$

with $\sigma(a, b) = 1$ for $a = b$ and $-1$ otherwise in the examples, a [linear gap penalty](/linear-gap-penalty/) $d = 1$, and a pair bonus $\beta = 3$.

**Output.** The best score, and a solution that reaches it.

## The algorithm

Let $D[i, j, k, l]$ be the best score of a solution for the two subsequences $x[i:j)$ and $y[k:l)$, with half-open intervals. If one interval is empty, the only solution puts the other one against gaps. Otherwise look at the first column. It is $x_i$ against a gap, a gap against $y_k$, $x_i$ against $y_k$ and unpaired, or $x_i$ against $y_k$ and paired with a later match column $(x_h, y_q)$. In the last case the columns between the two paired columns align $x[i+1:h)$ with $y[k+1:q)$, and the columns after them align $x[h+1:j)$ with $y[q+1:l)$.

```pseudo id=main
SANKOFF(x, y)                              ▷ |x| = m, |y| = n; D[i, j, k, l] scores x[i:j) against y[k:l)
L1  for s ← 0 to m do                      ▷ s = j − i
L2      for t ← 0 to n do                  ▷ t = l − k
L3          for i ← 0 to m − s and k ← 0 to n − t do
L4              j ← i + s; l ← k + t
L5              if s = 0 or t = 0 then D[i, j, k, l] ← −d · (s + t); continue
L6              best ← D[i + 1, j, k, l] − d                          ▷ x_i against a gap
L7              best ← max(best, D[i, j, k + 1, l] − d)               ▷ a gap against y_k
L8              best ← max(best, σ(x_i, y_k) + D[i + 1, j, k + 1, l]) ▷ unpaired match column
L9              for h ← i + h_min + 1 to j − 1 such that x_i x_h is an allowed pair do
L10                 for q ← k + h_min + 1 to l − 1 such that y_k y_q is an allowed pair do
L11                     best ← max(best, σ(x_i, y_k) + σ(x_h, y_q) + β + D[i + 1, h, k + 1, q] + D[h + 1, j, q + 1, l])
L12             D[i, j, k, l] ← best
L13 return D[0, m, 0, n]
```

Every cell read in lines L6 to L11 has a shorter interval in $x$, or the same interval in $x$ and a shorter one in $y$, so the loop order of lines L1 and L2 fills it first. A [traceback](/traceback/) from $D[0, m, 0, n]$ that repeats the choice of each cell, with a stack of pending pairs of intervals, gives the alignment and the structure.

The case split is the one of the Nussinov recursion that pairs the first base or leaves it unpaired, here applied to a column of two bases. Sankoff's paper writes the recursion in a different but equivalent form, with a separate bifurcation case that splits both intervals at once, and for a general additive loop score instead of a pair count.

## Example

Take $x = $ `GCAAGC` and $y = $ `CGAACG` with the scores above. Sequence alignment alone, with $\beta = 0$, gives score 0, for example `GC-AAGC-` against `-CGAA-CG`, and that alignment has no column pairs that pair in both rows.

With $\beta = 3$, some cells of the table are:

| cell | subsequences | value | best choice |
|---|---|---|---|
| $D[2, 4, 2, 4]$ | `AA` against `AA` | 2 | two unpaired match columns |
| $D[1, 5, 1, 5]$ | `CAAG` against `GAAC` | 3 | pair $x_1 x_4$ = C-G with $y_1 y_4$ = G-C: $-1 - 1 + 3 + D[2, 4, 2, 4] + D[5, 5, 5, 5]$ |
| $D[1, 6, 1, 6]$ | `CAAGC` against `GAACG` | 2 | |
| $D[0, 6, 0, 6]$ | `GCAAGC` against `CGAACG` | 4 | pair $x_0 x_5$ = G-C with $y_0 y_5$ = C-G: $-1 - 1 + 3 + D[1, 5, 1, 5] + D[6, 6, 6, 6]$ |

At the top cell, the other choices give $D[1, 6, 0, 6] - 1 = 3$, $D[0, 6, 1, 6] - 1 = 3$ and $\sigma(\mathtt{G}, \mathtt{C}) + D[1, 6, 1, 6] = 1$, so the pair wins. The result is

```
GCAAGC
CGAACG
((..))
```

with score 4: two matches, four mismatches and two consensus pairs. The two stems are made of different bases in the two sequences, so an aligner that sees only letters avoids putting them together. The table has $\binom{8}{2}^2 = 784$ cells with $i \le j$ and $k \le l$.

In a second example, `CAGAAACUG` against `GAGAACUC`, the best alignment is the same with and without pairs, `CAGAAACUG` over `GAG-AACUC`, and the pairs add three consensus pairs, `(((...)))`, which raise the score from 3 to 12.

## Correctness

By induction on $(j - i) + (l - k)$, $D[i, j, k, l]$ is the best score over all solutions for $x[i:j)$ and $y[k:l)$. The base case is a pair with an empty interval, which has one solution. In the step, the first column of every solution falls in exactly one of the cases of lines L6 to L11. In the paired case, nesting means that no pair crosses the paired column $(x_h, y_q)$, so the columns before and after it are independent solutions of the two smaller subproblems, the hairpin rule is checked on the new pair only, and the score adds. Every combination that the lines form is a valid solution, so the maximum is the optimum. The [full proof](proofs/correctness.md) gives the details.

## Complexity

- **Cells.** There are $\binom{m+2}{2} \binom{n+2}{2}$ cells with $i \le j$ and $k \le l$, so $\Theta(m^2 n^2)$ space.
- **Time.** A cell with $s = j - i$ and $t = l - k$ runs the loop of line L9 over $O(s)$ values of $h$, and the loop of line L10 over $O(t)$ values of $q$ for each $h$ that pairs with $x_i$. Summed over all cells this is $\Theta(m^3 n^3)$ in the worst case, for example when $x$ is `G` repeated $m/2$ times followed by `C` repeated $m/2$ times, and $y$ is built the same way. When no base of $x$ can pair with a later base, the loop of line L10 never runs and the time is $\Theta(m^3 n^2)$, the best case of the code as written. For random sequences with independent uniform letters, a fixed base pairs with a random base with probability $3/8$, so the expected time is $\Theta(m^3 n^3)$.
- **Two sequences of length $n$.** $\Theta(n^6)$ time and $\Theta(n^4)$ space, which limits the plain algorithm to short sequences.
- **$k$ sequences.** A cell becomes a choice of an interval in each sequence, so $O(n^{2k})$ cells and $O(n^{3k})$ time, as Sankoff stated.

## Properties

- **Exact.** For the given scores, the result is an optimal solution, not an approximation.
- **Score dependent.** The answer depends on the weight $\beta$ against $\sigma$ and $d$. With $\beta = 0$ the algorithm is [Needleman-Wunsch](/needleman-wunsch/) alignment run on a much larger table. With $y$ empty there are no match columns and so no pairs; the algorithm does not reduce to folding one sequence alone.
- **Pairs on match columns only.** A base of one sequence that pairs while its partner column holds a gap in the other sequence is not allowed. This is a choice of the model; energy-based versions score the structure of each sequence and allow it.
- **Deterministic and offline.** The whole input is needed before the table is filled.

## Variants and improvements

- **Energy scores.** Replace the pair bonus by the free energy of loops in the [nearest-neighbor model](/nearest-neighbor-model/), as in Sankoff's general form and in Dynalign. The cases then follow the loop types of the [Zuker algorithm](/zuker-algorithm/).
- **Affine gaps.** Keep separate tables for a column that opens a gap and one that extends it, as for sequences.
- **Banding.** Dynalign allows only alignments in which aligned positions differ by at most $M$, which cuts the time to about $O(M^3 N^3)$.
- **Sparse pairs.** LocARNA keeps only base pairs with a high probability in the [McCaskill](/mccaskill-algorithm/) ensemble of each sequence, for $O(n^4)$ time and $O(n^2)$ memory when each base has a bounded number of such pairs.
- **Local and progressive.** Foldalign finds the best local motif of two sequences, and builds multiple alignments by [progressive](/progressive-alignment/) steps. The problem page lists these tools with their costs.
- **One side fixed.** If one side has a known consensus structure, aligning to a [covariance model](/covariance-model/) costs about $n^3$.

## When to use it

- For short RNAs, or short windows of longer ones, when an exact joint optimum under a stated score is needed, for example to test a faster heuristic.
- When the sequences are too different for a sequence aligner to place the stems, but their structures are conserved.
- Not for long sequences or many sequences: use a banded or sparse variant, or fold one sequence and align to a model.

## Pitfalls

- **Memory.** The table has about $m^2 n^2 / 4$ cells, which is about $2.5 \cdot 10^7$ for $m = n = 100$. A four-dimensional array of that size is easy to run out of.
- **Hairpin rule in both sequences.** The rule $h - i - 1 \ge h_{\min}$ must hold in $x$ and in $y$; checking only one lets a pair close an empty loop in the other.
- **Score of the pair columns.** The two paired columns are also match columns, so line L11 adds their two $\sigma$ terms as well as $\beta$. Leaving them out gives a different objective.
- **Base cases.** Two empty intervals score 0, and an interval of length $s$ against an empty one scores $-d s$; with $D[i, i, k, l]$ wrong, every cell above it is wrong.

## Implementations

## History

Sankoff published the method in 1985 in the SIAM Journal on Applied Mathematics. The paper treats $k$ sequences on a known tree and solves three problems at once: the folding of each sequence, their alignment, and the ancestral sequences at the inner nodes of the tree, which the title calls protosequences. Its cost of $O(n^{3k})$ time kept it a reference method. From 1997 on, Foldalign, Dynalign, LocARNA and other tools made limited forms of it practical, and the [simultaneous alignment and folding](/simultaneous-alignment-and-folding/) page describes them.

## References
