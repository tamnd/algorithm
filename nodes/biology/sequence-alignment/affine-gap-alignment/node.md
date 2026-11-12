---
tag: RF65QZ
kind: problem
slug: affine-gap-alignment
name: Alignment with affine gap penalties
aliases:
- gotoh alignment problem
- affine gap alignment
area: biology/sequence-alignment
level: core
summary: Find a maximum-score alignment of two sequences when a gap of length L costs d + (L-1)e; solved in O(mn) time by the Gotoh algorithm.
prereqs: [affine-gap-penalty, scoring-matrix]
see_also: [gotoh-algorithm, needleman-wunsch, smith-waterman, global-alignment, local-alignment, alignment-graph, pair-hmm, edit-distance-hardness]
sources:
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the O(mn) algorithm for the gap weight w_k = uk + v
  - paper: doi:10.1007/BF02462326
    title: Stephen F. Altschul and Bruce W. Erickson, Optimal sequence alignment using affine gap costs, Bulletin of Mathematical Biology 48(5/6), 1986, 603-616
    locator: the traceback of Gotoh's method and a correct procedure for all optimal alignments
  - paper: doi:10.1093/bioinformatics/4.1.11
    title: Eugene W. Myers and Webb Miller, Optimal alignments in linear space, CABIOS 4(1), 1988, 11-17
    locator: affine gap alignment in O(mn) time and O(m + n) space
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.4 (alignment with affine gap scores) and Chapter 4 (the same problem as a pair HMM)
  - paper: doi:10.1137/15M1053128
    title: Arturs Backurs and Piotr Indyk, Edit distance cannot be computed in strongly subquadratic time (unless SETH is false), SIAM Journal on Computing 47(3), 2018, 1087-1097
    locator: the conditional quadratic lower bound for edit distance
---

Alignment with affine gap penalties asks for a maximum-score [alignment](/pairwise-sequence-alignment/) of two sequences when the score adds a [scoring matrix](/scoring-matrix/) value for each aligned pair and subtracts $d + (L-1)e$ for each gap of length $L$. It is the [global alignment](/global-alignment/) or [local alignment](/local-alignment/) problem under the [affine gap penalty](/affine-gap-penalty/), the model used by almost every practical aligner. The [Gotoh algorithm](/gotoh-algorithm/) solves it in $O(mn)$ time with three tables, and no algorithm that is faster by a polynomial factor is expected.

## In plain words

You have two sequences and want to line them up so that similar letters stand in the same column. Some letters get no partner, and you mark them with dashes. A run of dashes is a gap.

The score rewards good pairs of letters and punishes gaps. Here a gap has two prices: a large one to start it and a small one for each extra dash. The task is to find the arrangement with the highest score.

This sounds like the ordinary alignment task, and it nearly is. The difference is that a dash now costs more or less depending on whether the dash before it is in the same row. A program must remember which kind of column came last, and that is why the standard solution keeps three tables instead of one.

## Definition

**Input.** Two sequences $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$, a scoring matrix $s : \Sigma \times \Sigma \to \mathbb{R}$, and gap parameters $d \ge e \ge 0$.

**Alignments.** An alignment of $x$ and $y$ is a pair of rows of equal length over $\Sigma \cup \{-\}$ that give $x$ and $y$ when the spaces are deleted, with no column of two spaces. A gap is a maximal run of columns with a space in the same row.

**Score.**

$$S(A) = \sum_{\text{pair columns } (a, b)} s(a, b) \; - \sum_{\text{gaps}} \bigl(d + (L - 1)e\bigr),$$

where $L$ is the length of the gap.

**Output.** The global version asks for $\max_A S(A)$ over all alignments of $x$ and $y$, and for one alignment that reaches it. The local version asks for the maximum of $S(A)$ over all alignments of a substring of $x$ with a substring of $y$, where the empty alignment scores $0$.

The number of alignments is the Delannoy number $\sum_k \binom{m}{k}\binom{n}{k}2^k$, which grows exponentially, so enumeration is not an option. For $m = 6$ and $n = 4$ it is already $1289$.

## Variants

- **Global, local and semi-global.** The global version is [Needleman-Wunsch](/needleman-wunsch/) with affine gaps, the local version is [Smith-Waterman](/smith-waterman/) with affine gaps, and the [semi-global](/semi-global-alignment/) version charges nothing for gaps at the ends of one or both sequences.
- **Score only.** Only $\max_A S(A)$ is wanted. Database search computes millions of these and needs $O(n)$ memory.
- **All optimal alignments.** Every alignment of maximum score is wanted, or a count of them. Altschul and Erickson (1986) showed how to do this correctly with affine gaps.
- **Restricted region.** The alignment must stay in a diagonal band, as in [banded alignment](/banded-alignment/) and the [banded Smith-Waterman](/banded-smith-waterman/), or the search stops when the score drops too far, as in [X-drop extension](/x-drop-extension/). These are not the same problem; they return the optimum of a restricted set.
- **Other gap models.** Two-piece affine penalties take the minimum of two affine functions; the [linear gap penalty](/linear-gap-penalty/) is the case $d = e$.

## Examples

**A gap of two beats two gaps of one.** Let $x = \texttt{ACGTTA}$, $y = \texttt{ACTA}$, match $+2$, mismatch $-1$, $d = 3$, $e = 1$. The optimal global score is $4$, reached by

```
ACGTTA
AC--TA
```

four matches, $8$, minus one gap of length 2, $3 + 1 = 4$. The alignment $\texttt{ACGTTA}$ over $\texttt{AC-T-A}$ has the same four matches but two gaps, and scores $8 - 6 = 2$. Under the linear penalty $d = e = 3$ the best score drops to $2$; under $d = e = 1$ it rises to $6$. The [Gotoh algorithm](/gotoh-algorithm/) page shows the three tables for this pair.

**Opposite rows are two gaps.** Let $x = \texttt{ACGT}$ and $y = \texttt{AGGT}$, with the same scores. The alignment

```
AC-GT
A-GGT
```

has a space in the bottom row, then a space in the top row. These are two gaps, cost $3 + 3$, and the score is $6 - 6 = 0$. The optimum is the gap-free alignment, $2 - 1 + 2 + 2 = 5$.

**A local example.** Let $x = \texttt{TTGACCTGAAT}$, $y = \texttt{CCGACCTTGAAG}$, match $+2$, mismatch $-3$, $d = 5$, $e = 2$. The best local alignment is

```
GACC-TGAA
GACCTTGAA
```

eight matches and one gap of length 1: $16 - 5 = 11$.

## Known algorithms

| algorithm | time | space | notes |
|---|---|---|---|
| general gap recurrence | $O(mn(m+n))$ | $O(mn)$ | works for any subadditive $g$; see [gap penalty](/gap-penalty/) |
| [Gotoh algorithm](/gotoh-algorithm/) (1982) | $O(mn)$ | $O(mn)$, or $O(n)$ for the score | three tables; the published traceback was corrected by Altschul and Erickson (1986) |
| Myers and Miller (1988) | $O(mn)$ | $O(m + n)$ | divide and conquer in the style of the [Hirschberg algorithm](/hirschberg-algorithm/), with care at the split row for gaps that cross it |
| [banded Smith-Waterman](/banded-smith-waterman/), banded global alignment | $O(kn)$ for band width $k$ | $O(kn)$ | exact only for alignments inside the band |
| [X-drop extension](/x-drop-extension/) | depends on the input | | heuristic; used by [BLAST](/blast/) |

Practical implementations run the three-table recurrence with vector instructions, for example Farrar's striped Smith-Waterman (2007), and the work per cell stays constant.

## Bounds

- **Upper bound.** $O(mn)$ time by the Gotoh algorithm, with $O(m + n)$ space by Myers and Miller.
- **Conditional lower bound.** Unit-cost [edit distance](/edit-distance/) is a special case: match $0$, mismatch $-1$, $d = e = 1$ gives minus the edit distance. Backurs and Indyk proved that edit distance has no $O(n^{2-\varepsilon})$ algorithm for any $\varepsilon > 0$ unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails; see [edit distance hardness](/edit-distance-hardness/). So affine gap alignment has no strongly subquadratic algorithm under the same hypothesis.
- **No unconditional quadratic lower bound** is known for general models of computation.

## Reductions

- **From linear gap alignment.** Set $e = d$. Every [linear gap penalty](/linear-gap-penalty/) instance, and so edit distance and the [longest common subsequence](/longest-common-subsequence/), is an affine instance.
- **To a longest path in a DAG.** Build an [alignment graph](/alignment-graph/) with three nodes $M_{ij}, X_{ij}, Y_{ij}$ for each cell. Add an edge of weight $s(x_i, y_j)$ from each of the three nodes of cell $(i-1, j-1)$ to $M_{ij}$. Add edges of weight $-d$ from $M_{i-1,j}$ and $Y_{i-1,j}$ to $X_{ij}$, and of weight $-e$ from $X_{i-1,j}$ to $X_{ij}$; and the same for $Y_{ij}$ with $(i, j-1)$. Paths from the source to the sink correspond one to one with alignments, with path weight equal to the score. A [longest path in a DAG](/dag-longest-path/) then solves the problem in time linear in the $O(mn)$ edges, which is the Gotoh algorithm.
- **To pair HMM decoding.** In a [pair HMM](/pair-hmm/) with a match state and two gap states, the most probable state path under the Viterbi algorithm is an optimal affine gap alignment, with $d$ and $e$ the negative logs of the gap open and gap repeat probabilities.

## Applications

- Protein and DNA database search: [BLAST](/blast/) extends seeds with gapped affine alignment, and Smith-Waterman search tools compute the full affine local score against each database sequence.
- Read mapping and long-read alignment in [BWA](/bwa/) and [minimap2](/minimap2/), which align inside a band around a seed chain.
- [Progressive alignment](/progressive-alignment/) in [multiple sequence alignment](/multiple-sequence-alignment/), which aligns profiles with affine gap costs at each step.

## References
