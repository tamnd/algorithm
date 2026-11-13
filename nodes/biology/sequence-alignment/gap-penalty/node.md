---
tag: MT7P16
kind: concept
slug: gap-penalty
name: Gap penalty
aliases:
- indel penalty
- gap cost function
area: biology/sequence-alignment
level: intro
summary: The cost g(L) that an alignment score charges for each gap, a maximal run of L spaces in one row; linear and affine are the common models.
prereqs: [weighted-edit-distance]
see_also: [linear-gap-penalty, affine-gap-penalty, affine-gap-alignment, gotoh-algorithm, scoring-matrix, pairwise-sequence-alignment, needleman-wunsch, edit-distance]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (the scoring model and gap penalties) and Section 2.4 (dynamic programming with more complex models, general and affine gap functions)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, Section 11.8 (gaps and gap weight models) and Chapter 12, Section 12.6 (convex gap weights)
  - paper: doi:10.1016/0022-2836(82)90398-9
    title: Osamu Gotoh, An improved algorithm for matching biological sequences, Journal of Molecular Biology 162(3), 1982, 705-708
    locator: the gap weight w_k = uk + v and the O(mn) recurrence for it
  - paper: doi:10.1093/nar/25.17.3389
    title: Stephen F. Altschul, Thomas L. Madden, Alejandro A. Schäffer, Jinghui Zhang, Zheng Zhang, Webb Miller and David J. Lipman, Gapped BLAST and PSI-BLAST, Nucleic Acids Research 25(17), 1997, 3389-3402
    locator: the gap costs 10 + k for a gap of length k, used with BLOSUM-62 throughout the paper
---

A gap penalty is the cost that an alignment score charges for each gap, a maximal run of consecutive spaces in one row of a [pairwise alignment](/pairwise-sequence-alignment/). It is a function $g(L)$ of the gap length $L$. The score of an alignment is the sum of the [scoring matrix](/scoring-matrix/) values of its aligned pairs, minus $g(L)$ for each gap. The two common models are the [linear gap penalty](/linear-gap-penalty/) $g(L) = dL$ and the [affine gap penalty](/affine-gap-penalty/) $g(L) = d + (L-1)e$. The model decides which alignments are optimal and which dynamic program computes them.

## In plain words

When you line up two DNA or protein sequences, some letters of one sequence have no partner in the other. You show this with a dash, a space. A run of dashes next to each other in the same row is one gap. Biologically, one gap is often one event: a piece of sequence was inserted into one sequence, or deleted from the other.

A gap penalty says how many points a gap costs. If gaps cost nothing, the best alignment puts dashes everywhere to avoid each mismatch. If gaps cost too much, the best alignment never uses them, even where an insertion really happened. The simplest rule charges the same for each dash. A better rule charges a large amount to start a gap and a small amount for each extra dash, because one long insertion is more likely than many short ones.

## The idea

**Alignments and gaps.** Let $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ be sequences over an alphabet $\Sigma$, for example the four DNA bases or the 20 amino acids. An alignment of $x$ and $y$ is a pair of rows of equal length over $\Sigma \cup \{-\}$ such that deleting the spaces from the first row gives $x$, deleting them from the second row gives $y$, and no column holds two spaces. A *gap* is a maximal run of consecutive columns that all have a space in the same row. A run of spaces in the top row that is directly followed by a run of spaces in the bottom row is two gaps, not one.

**The score.** Fix a scoring matrix $s : \Sigma \times \Sigma \to \mathbb{R}$ and a gap penalty $g : \{1, 2, \ldots\} \to \mathbb{R}_{\ge 0}$. The score of an alignment $A$ is

$$S(A) = \sum_{\text{columns } (a, b) \text{ of } A,\ a, b \in \Sigma} s(a, b) \; - \sum_{\text{gaps of } A} g(\text{length of the gap}).$$

[Global alignment](/global-alignment/) asks for an alignment of maximum score. This page uses a score to maximize and a penalty to subtract. Books that minimize a distance use the same $g$ with the opposite sign of $s$, as in the [weighted edit distance](/weighted-edit-distance/).

**The common models.** All four below have $g(L) \ge 0$ and are non-decreasing in $L$.

| model | $g(L)$ | parameters | time of the best known dynamic program |
|---|---|---|---|
| linear | $dL$ | $d > 0$ | $O(mn)$, one table |
| affine | $d + (L-1)e$ | $d \ge e \ge 0$ | $O(mn)$, three tables ([Gotoh](/gotoh-algorithm/)) |
| concave | each extra space costs at most as much as the one before | for example $d + e \log_2 L$ | $O(mn)$ times a logarithmic factor (Gusfield, Section 12.6) |
| general | any function | a table of $g(1), g(2), \ldots$ | $O(mn(m+n))$ |

The concave case is called *convex gap weights* in part of the literature, including Gusfield. The function itself is concave: its increments $g(L+1) - g(L)$ do not grow.

**Conventions differ by one extension.** This encyclopedia writes the affine penalty as $g(L) = d + (L - 1)e$, as Durbin et al. do: $d$ is the cost of the first space and $e$ the cost of each further space. Other sources write $g(L) = o + Le$, so that the opening charge $o$ comes on top of an extension charge for every space. The two forms are the same function when $d = o + e$. Gotoh writes $w_k = uk + v$ with $v = o$ and $u = e$, Gusfield writes $W_g + L\,W_s$ with $W_g = o$ and $W_s = e$, and Altschul et al. charge a gap of length $k$ a cost $a + bk$ with $a = o$ and $b = e$. A program option "gap open 10, gap extend 1" means $d = 10$ or $d = 11$, depending on which form the program uses.

**The general recurrence.** Let $H(i, j)$ be the best score of an alignment of $x_1 \cdots x_i$ with $y_1 \cdots y_j$. The last block of such an alignment is a pair column or a gap of some length $k$ in one row, so

$$H(i, j) = \max\Bigl\{ H(i-1, j-1) + s(x_i, y_j),\ \max_{1 \le k \le i} \bigl(H(i-k, j) - g(k)\bigr),\ \max_{1 \le k \le j} \bigl(H(i, j-k) - g(k)\bigr) \Bigr\},$$

with $H(0, 0) = 0$ and the terms with an index below 0 left out. Cell $(i, j)$ looks at $i + j + 1$ earlier cells, so the table costs $O(mn(m+n))$ time. This recurrence is exact only when $g$ is *subadditive*, $g(a + b) \le g(a) + g(b)$ for all $a, b \ge 1$. The reason: the term $H(i-k, j) - g(k)$ also covers an alignment of the prefixes that already ends with a gap in the same row. That alignment then has one gap of length $k' + k$, but the recurrence charges it $g(k') + g(k)$. When $g$ is subadditive, this charge is at least the true charge, so the maximum is still the true optimum. Linear penalties, affine penalties with $d \ge e$, and concave penalties that stay concave when $g(0) = 0$ is added are subadditive. For the affine case, $g(a) + g(b) - g(a + b) = d - e$. The linear and affine models are worth a page each because they bring the cost down from $O(mn(m+n))$ to $O(mn)$.

## Examples

**Linear and affine disagree.** Align $x = \texttt{ACGTTA}$ with $y = \texttt{ACTA}$, with match score $+2$ and mismatch score $-1$. Two candidate alignments are

```
A1:  ACGTTA        A2:  ACGTTA
     AC--TA             AC-T-A
```

Both have four matches, worth $8$. Alignment A1 has one gap of length 2, and A2 has two gaps of length 1.

| penalty | $S(A_1)$ | $S(A_2)$ |
|---|---|---|
| linear, $d = 2$ | $8 - 4 = 4$ | $8 - 2 - 2 = 4$ |
| affine, $d = 3$, $e = 1$ | $8 - 4 = 4$ | $8 - 3 - 3 = 2$ |

The linear penalty cannot tell the two apart. The affine penalty prefers the single gap, which is the more likely history: one deletion of $\texttt{GT}$. The optimum under both penalties is $4$.

**Two gaps, not one.** In the alignment

```
AC-GT
A-GGT
```

column 2 has a space in the bottom row and column 3 has a space in the top row. These are two gaps of length 1, and each one pays the full opening charge. With the scores above and the affine penalty $d = 3$, $e = 1$, the alignment scores $6 - 3 - 3 = 0$. The gap-free alignment of $\texttt{ACGT}$ with $\texttt{AGGT}$ scores $2 - 1 + 2 + 2 = 5$. A program that joins the two spaces into one gap of length 2 would wrongly score the first alignment $6 - 4 = 2$.

**A penalty that breaks the recurrence.** Take $g(L) = L^2$, which is not subadditive: $g(2) = 4 > g(1) + g(1) = 2$. Align $x = \texttt{AAAA}$ with $y = \texttt{A}$, match $+2$. The best alignment matches one $\texttt{A}$ and puts the other three under spaces in two gaps, of lengths 1 and 2, for a score of $2 - 1 - 4 = -3$. The general recurrence returns $-1$, because it charges three adjacent spaces as three gaps of length 1. No alignment has score $-1$.

**Edit distance as a special case.** With $s(a, a) = 0$, $s(a, b) = -1$ for $a \ne b$ and the linear penalty $g(L) = L$, the best score is minus the Levenshtein [edit distance](/edit-distance/). For $\texttt{kitten}$ and $\texttt{sitting}$ it is $-3$.

## Where it is used

- Every pairwise alignment score has a gap penalty: [Needleman-Wunsch](/needleman-wunsch/) for global alignment, [Smith-Waterman](/smith-waterman/) for [local alignment](/local-alignment/), and [semi-global alignment](/semi-global-alignment/), which leaves end gaps free.
- The affine model is the default of protein and DNA search tools. [BLAST](/blast/) charges a gap of length $k$ the cost $a + bk$. Altschul et al. used $10 + k$ with BLOSUM-62 in the 1997 paper on gapped BLAST.
- The [affine gap alignment](/affine-gap-alignment/) problem and the [Gotoh algorithm](/gotoh-algorithm/) exist only because of the affine model. In a [pair HMM](/pair-hmm/), the affine penalty is the log-probability of a gap state that is entered once and then repeated, so the gap length has a geometric distribution.
- Gap penalties and the [scoring matrix](/scoring-matrix/) must be chosen together. The statistics of local alignment scores in [Karlin-Altschul statistics](/karlin-altschul-statistics/) are proved for ungapped alignments, and for gapped alignments the parameters are fitted for each pair of matrix and gap costs.

## References
