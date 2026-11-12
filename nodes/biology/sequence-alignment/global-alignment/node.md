---
tag: CA686H
kind: problem
slug: global-alignment
name: Global alignment
aliases:
- end-to-end alignment
area: biology/sequence-alignment
level: intro
summary: Align two whole sequences from end to end so that the alignment score is largest; gaps at the two ends cost the same as gaps inside.
prereqs: [pairwise-sequence-alignment]
see_also: [needleman-wunsch, hirschberg-algorithm, local-alignment, semi-global-alignment, alignment-graph, affine-gap-alignment, edit-distance, longest-common-subsequence]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3 (global alignment, Needleman-Wunsch algorithm)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the sections on edit distance, edit graphs and string similarity
  - paper: doi:10.1016/0022-2836(70)90057-4
    title: Saul B. Needleman and Christian D. Wunsch, A general method applicable to the search for similarities in the amino acid sequence of two proteins, Journal of Molecular Biology 48(3), 1970, 443-453
    locator: the method, which compares the two complete sequences
  - paper: doi:10.1137/0126070
    title: Peter H. Sellers, On the theory and computation of evolutionary distances, SIAM Journal on Applied Mathematics 26(4), 1974, 787-793
    locator: the distance between two sequences as a minimum over alignments and its O(mn) computation
---

Global alignment is the form of [pairwise sequence alignment](/pairwise-sequence-alignment/) that aligns every letter of both sequences: the alignment starts at the first letters and ends at the last letters, and gaps at the ends are charged like gaps inside. The goal is the largest [alignment score](/alignment-score/). It suits two sequences of about the same length that are related over their whole length, such as one protein in two species. The [Needleman-Wunsch algorithm](/needleman-wunsch/) solves it in $O(mn)$ time for lengths $m$ and $n$, and [Hirschberg's algorithm](/hirschberg-algorithm/) does it in linear space.

## In plain words

You have two sequences that should match from start to end, for example the same gene in a human and in a mouse. You write one above the other, and you may put gaps into either of them, but you must use every letter of both. Each column gets a score: a good pair of letters earns points, a bad pair or a gap loses points.

The task is to choose where the gaps go so that the total is as high as possible. A gap at the start or the end is not free; it costs the same as a gap in the middle. So the answer always covers both sequences completely, even where they do not look alike. If only a part of them is related, the other forms of alignment, local or semi-global, fit better.

## Definition

**Model.** The alphabet $\Sigma$ is DNA, RNA or the 20 amino acids. The input is $x \in \Sigma^m$, $y \in \Sigma^n$, a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$ and a gap penalty. The gap penalty is linear, $d$ per gap symbol with $d \ge 0$, unless a variant says otherwise. The costs below are in the [word RAM](/word-ram/) model.

An alignment of $x$ and $y$ is a pair of rows over $\Sigma \cup \{-\}$ of the same length, with no column $(-, -)$, that give $x$ and $y$ when the gap symbols are removed (see [alignment score](/alignment-score/)). Its score is

$$S(A) = \sum_{\text{pair columns } (a, b)} s(a, b) \; - \; d \cdot (\text{number of gap columns}).$$

**Output.** An alignment $A^*$ with $S(A^*) = \operatorname{OPT}(x, y) = \max_A S(A)$, or only the value $\operatorname{OPT}(x, y)$.

**Recurrence.** Let $F(i, j) = \operatorname{OPT}(x_1 \cdots x_i, \, y_1 \cdots y_j)$. The last column of an optimal alignment of the two prefixes is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$, so

$$F(i, j) = \max\{F(i - 1, j - 1) + s(x_i, y_j),\; F(i - 1, j) - d,\; F(i, j - 1) - d\},$$

with $F(0, 0) = 0$, $F(i, 0) = -id$ and $F(0, j) = -jd$. The answer is $F(m, n)$.

## Variants

- **Distance form.** Minimize a sum of costs. This is the [weighted edit distance](/weighted-edit-distance/), and the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) is the same table. For global alignment, a similarity score and a distance give the same optimal alignments after a change of parameters (see [alignment score](/alignment-score/)).
- **Affine gaps.** A gap of length $L$ costs $d + (L - 1)e$. This is [affine-gap alignment](/affine-gap-alignment/), solved in $O(mn)$ time by the [Gotoh algorithm](/gotoh-algorithm/).
- **General gap function.** A gap of length $L$ costs $g(L)$ for an arbitrary $g$. The recurrence must try every gap length, which takes $O(mn(m + n))$ time. Needleman and Wunsch allowed this in 1970.
- **Free end gaps.** Drop the charge for the gaps at some ends: [semi-global alignment](/semi-global-alignment/).
- **Band.** Only alignments whose path stays within $k$ diagonals of the main one: [banded alignment](/banded-alignment/), in $O(k \max(m, n))$ time.
- **Value only.** The score alone needs two rows of the table, so $O(\min(m, n))$ space.

## Examples

All examples use the toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$.

**ACGTC and AGTAC** ($m = n = 5$). The optimal alignment is unique:

```
A C G T - C
A - G T A C
```

Its score is $2 - 2 + 2 + 2 - 2 + 2 = 4$. The alignment without gaps, ACGTC over AGTAC, scores only $2 - 1 - 1 - 1 + 2 = 1$. The [Needleman-Wunsch](/needleman-wunsch/) page fills the table for this pair.

**Global against local.** For TCAGTTGCA and GAGTGCAT, the best global score is 5, but the best [local alignment](/local-alignment/), AGTTGCA over AG-TGCA, scores 10. The global alignment must also align the flanks TC and T, and they cost 5 points.

**End gaps are charged.** For TTCAGTAC and AGTACGGA, the five letters AGTAC overlap, but the global optimum is $-2$. An alignment that puts the overlap in one column block needs three gap symbols at each end, which cost $6 \cdot 2 = 12$ against the $10$ points of the overlap. [Semi-global alignment](/semi-global-alignment/) makes those end gaps free and scores 10.

**Special cases.** With $s(a, a) = 1$, $s(a, b) = 0$ and $d = 0$, $\operatorname{OPT}$ is the length of a [longest common subsequence](/longest-common-subsequence/); for ACGTC and AGTAC it is 4 (AGTC). With $s(a, a) = 0$, $s(a, b) = -1$ and $d = 1$, $\operatorname{OPT}$ is minus the Levenshtein [edit distance](/edit-distance/); for the same pair it is $-2$.

## Known algorithms

| algorithm | gaps | time (worst case) | space |
|---|---|---|---|
| [Needleman-Wunsch](/needleman-wunsch/) (quadratic form) | linear | $\Theta(mn)$ | $\Theta(mn)$ for the alignment, $\Theta(\min(m, n))$ for the score |
| Needleman and Wunsch (1970 form) | general $g$ | $O(mn(m + n))$ | $\Theta(mn)$ |
| [Gotoh](/gotoh-algorithm/) | affine | $\Theta(mn)$ | $\Theta(mn)$ |
| [Hirschberg](/hirschberg-algorithm/) | linear (affine with Myers and Miller) | $\Theta(mn)$, about twice the cells | $O(\min(m, n))$ plus the output |
| [Banded alignment](/banded-alignment/) | linear or affine | $O(k \max(m, n))$ | $O(k \max(m, n))$ |

For two strings of length $n$ over a constant alphabet, Crochemore, Landau and Ziv-Ukelson (2003) compute the score with an arbitrary scoring matrix in $O(n^2 / \log n)$ time. The [Four Russians method](/four-russians-method/) gives the same bound for edit distance with bounded integer costs.

## Bounds

- **Upper.** $O(mn)$ time for linear and affine gaps, and $O(n^2 / \log n)$ over a constant alphabet with an arbitrary scoring matrix.
- **Lower, trivial.** $\Omega(m + n)$: the algorithm must read every letter.
- **Lower, conditional.** LCS and Levenshtein distance are special cases, so under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) no algorithm runs in $O(n^{2 - \varepsilon})$ time for strings of length $n$ (see [edit distance hardness](/edit-distance-hardness/) and the [Backurs-Indyk LCS lower bound](/backurs-indyk-lcs-lower-bound/)).

## Reductions

- **To a longest path.** Global alignment is the heaviest path from the corner $(0, 0)$ to the corner $(m, n)$ in the [alignment graph](/alignment-graph/), a grid DAG. The recurrence above is [longest path in a DAG](/dag-longest-path/) in row-major topological order.
- **From LCS and edit distance.** Both are global alignment with a fixed scheme, as in the examples.
- **From semi-global alignment.** Semi-global alignment with linear gaps reduces to global alignment by a change of the first row, the first column and the end cell of the table, not by a change of the input; the [semi-global DP](/semi-global-dp/) page gives the details.

## Applications

- Comparison of orthologous genes or proteins of about equal length, for example to count the substitutions between two species.
- The pairwise step of progressive [multiple sequence alignment](/multiple-sequence-alignment/), and the pairwise distances that build a guide tree.
- Comparison of two assemblies or two versions of a short sequence, such as a plasmid or a gene before and after editing.
- In text processing, the same problem with unit costs is the diff of two strings ([edit distance](/edit-distance/)).

## References
