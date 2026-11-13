---
tag: V7ZEFS
kind: problem
slug: pairwise-sequence-alignment
name: Pairwise sequence alignment
aliases:
- two-sequence alignment
area: biology/sequence-alignment
level: intro
summary: Given two DNA, RNA or protein sequences and a scoring scheme, find an alignment of largest score, in the global, local or semi-global form.
prereqs: [alignment-score]
see_also: [global-alignment, local-alignment, semi-global-alignment, alignment-graph, needleman-wunsch, smith-waterman, edit-distance, multiple-sequence-alignment]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Pairwise alignment (Section 2.3 for the global, local, repeated and overlap forms, Section 2.4 for affine gaps, Section 2.6 for linear space)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (edit distance, similarity, local alignment, end-space free alignment and gaps) and Chapter 12 (linear space and faster methods)
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6 (global and local sequence alignment, scoring, gap penalties) and Chapter 7, Section 7.2 (space-efficient alignment)
  - paper: doi:10.1137/S0097539702402007
    title: Maxime Crochemore, Gad M. Landau and Michal Ziv-Ukelson, A subquadratic sequence alignment algorithm for unrestricted scoring matrices, SIAM Journal on Computing 32(6), 2003, 1654-1673
    locator: the O(n^2 / log n) algorithm for global and local alignment with an arbitrary scoring matrix over a constant alphabet
  - paper: "Alfred V. Aho, Daniel S. Hirschberg and Jeffrey D. Ullman, Bounds on the complexity of the longest common subsequence problem, Journal of the ACM 23(1), 1976, 1-12"
    locator: the lower bound of order mn comparisons in the model of equal and unequal tests
---

Pairwise sequence alignment is the problem of lining up two DNA, RNA or protein sequences so that the [alignment score](/alignment-score/) is as large as possible. The input is the two sequences and a scoring scheme, a [substitution matrix](/substitution-matrix/) and a [gap penalty](/gap-penalty/). The problem has three main forms: [global alignment](/global-alignment/) of the whole sequences, [local alignment](/local-alignment/) of the best pair of substrings, and [semi-global alignment](/semi-global-alignment/) with free end gaps. Each form is a heaviest path in the [alignment graph](/alignment-graph/), and a dynamic program solves it in $O(mn)$ time for lengths $m$ and $n$.

## In plain words

Two genes or proteins that come from a common ancestor still look alike, but evolution has changed some letters and has inserted or deleted others. To compare them, you write one sequence above the other and add gaps, so that letters with a common origin stand in the same column.

A scoring scheme rates each column, and the problem is to find the arrangement with the best total. Sometimes you want to line up the two sequences from end to end. Sometimes you want only the best matching piece of each, for example one shared domain in two large proteins. Sometimes one sequence should fit inside the other, or the end of one should overlap the start of the other. The number of possible arrangements grows very fast, so a program cannot try them all, but a table of partial answers finds the best one quickly.

## Definition

**Model.** The alphabet $\Sigma$ is DNA ($\{A, C, G, T\}$), RNA ($\{A, C, G, U\}$) or the 20 amino acids. The input is $x \in \Sigma^m$ and $y \in \Sigma^n$, a substitution score $s : \Sigma \times \Sigma \to \mathbb{R}$ and a gap penalty $g$. The default gap model is linear, $g(L) = dL$; the affine model is $g(L) = d + (L - 1)e$. Scores are integers in the [word RAM](/word-ram/) model.

An alignment $A$ of $x$ and $y$ and its score $S(A)$ are defined on the [alignment score](/alignment-score/) page. Write $\mathcal{A}(u, v)$ for the set of alignments of $u$ and $v$.

**Global.** Find $A \in \mathcal{A}(x, y)$ that maximizes $S(A)$. The value is $\operatorname{OPT}_{\mathrm{glob}}(x, y) = \max_{A \in \mathcal{A}(x, y)} S(A)$.

**Local.** Find substrings $u$ of $x$ and $v$ of $y$, and $A \in \mathcal{A}(u, v)$, that maximize $S(A)$. The empty substrings are allowed, so the value is at least 0.

**Semi-global.** Find $A \in \mathcal{A}(x, y)$ that maximizes $S(A)$, where the gap columns at a chosen subset of the four ends (before or after the letters of $x$, before or after the letters of $y$) cost nothing.

The output is the alignment, or only its score if the question asks for the value.

## Variants

- **The form.** Global, local or semi-global, as above. Semi-global covers *overlap* alignment (a suffix of one sequence against a prefix of the other) and *fitting* alignment (all of one sequence against a substring of the other).
- **The gap model.** Linear gaps, affine gaps ([affine-gap alignment](/affine-gap-alignment/)), or a general function $g$. A general $g$ costs $O(mn(m + n))$ time with the original recurrences of Needleman and Wunsch and of Smith and Waterman, because a cell must look at every gap length.
- **Value or alignment.** The score alone needs only two rows of the table, $O(\min(m, n))$ space. The alignment needs a [traceback](/traceback/), or [Hirschberg's algorithm](/hirschberg-algorithm/) to keep linear space.
- **Distance form.** Minimize a cost instead of maximizing a score. For global alignment this is the [weighted edit distance](/weighted-edit-distance/), and it gives the same optimal alignments after a change of parameters (see [alignment score](/alignment-score/)).
- **Restricted alignments.** Only alignments inside a diagonal band ([banded alignment](/banded-alignment/)), or only alignments with at most $k$ differences ([k-differences problem](/k-differences-problem/)).
- **Many sequences or a graph.** Three or more sequences give [multiple sequence alignment](/multiple-sequence-alignment/). A sequence against a graph of sequences gives [sequence-to-graph alignment](/sequence-to-graph-alignment/).
- **Probabilistic form.** A [pair HMM](/pair-hmm/) defines a probability for each alignment; the most probable alignment is the Viterbi path, and the sum over all alignments measures how related the sequences are.

## Examples

All examples use the toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, and $d = 2$ per gap symbol.

| $x$ | $y$ | global | local | semi-global |
|---|---|---|---|---|
| ACGTC | AGTAC | 4: `ACGT-C` over `A-GTAC` | 4 | 4 |
| TCAGTTGCA | GAGTGCAT | 5 | 10: `AGTTGCA` over `AG-TGCA` | |
| TTCAGTAC | AGTACGGA | $-2$ | 10: `AGTAC` over `AGTAC` | overlap, 10: `TTCAGTAC---` over `---AGTACGGA` |
| CAGGTACT | TAGTAC | 5 | 8: `GTAC` over `GTAC` | fitting of $y$ in $x$, 7: `CAGGTACT` over `TA-GTAC-` |

The rows show how the forms differ. In the second row, the flanks TC and T of the two sequences pull the global score down, and local alignment drops them. In the third row, the sequences share only an overlap of five letters, and the overlap form scores it without a penalty for the six unaligned end letters. In the last row, the fitting form must keep the first letter T of $y$, at a cost, so it scores less than the local form, which may drop that letter.

Even two strings of length 5 have 1683 alignments, and two of length 10 have 8097453; the [alignment graph](/alignment-graph/) page counts them.

## Known algorithms

| algorithm | form | gaps | time | space |
|---|---|---|---|---|
| [Needleman-Wunsch](/needleman-wunsch/) | global | linear | $\Theta(mn)$ | $\Theta(mn)$ |
| [Smith-Waterman](/smith-waterman/) | local | linear | $\Theta(mn)$ | $\Theta(mn)$ |
| [Semi-global DP](/semi-global-dp/) | semi-global | linear | $\Theta(mn)$ | $\Theta(mn)$ |
| [Gotoh](/gotoh-algorithm/) | all forms | affine | $\Theta(mn)$ | $\Theta(mn)$ |
| [Hirschberg](/hirschberg-algorithm/) | global (and the others with a first pass) | linear, affine with Myers and Miller | $\Theta(mn)$ | $O(\min(m, n))$ plus the output |
| [Banded alignment](/banded-alignment/) | global, inside a band of width $k$ | linear or affine | $O(k \max(m, n))$ | $O(k \max(m, n))$ |

For unit costs, the [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) and the [Ukkonen cutoff](/ukkonen-cutoff-algorithm/) are faster in practice and in some cases in theory. For database search, [BLAST](/blast/), the [FASTA algorithm](/fasta-algorithm/) and other [seed-and-extend](/seed-and-extend/) methods are heuristics: they run much faster on real data, but they can miss an optimal local alignment that has no exact seed.

## Bounds

- **Upper bound.** $O(mn)$ time for each form with linear or affine gaps. For a constant alphabet and an arbitrary scoring matrix, Crochemore, Landau and Ziv-Ukelson (2003) gave $O(n^2 / \log n)$ time for two sequences of length $n$, for global and local alignment. The [Four Russians method](/four-russians-method/) gives the same bound for edit distance with bounded integer costs.
- **Conditional lower bound.** The Levenshtein distance and the longest common subsequence are special cases of global alignment with a fixed scoring scheme. So, unless the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) fails, no algorithm solves global alignment in $O(n^{2 - \varepsilon})$ time for a constant $\varepsilon > 0$. See [edit distance hardness](/edit-distance-hardness/) and the [SETH lower bound for LCS](/lcs-seth-lower-bound/).
- **Comparison lower bound.** In a model where the letters can only be tested for equality, Aho, Hirschberg and Ullman (1976) proved a lower bound of order $mn$ comparisons for the longest common subsequence, so for global alignment in that model.
- **Space.** The score needs $O(\min(m, n))$ words beside the input, and so does the alignment, with [Hirschberg's algorithm](/hirschberg-algorithm/), beside the output.

## Reductions

- **To a longest path.** Each form is a heaviest source-to-sink path in a [directed acyclic graph](/directed-acyclic-graph/) with $(m + 1)(n + 1)$ grid vertices, the [alignment graph](/alignment-graph/), plus a source and a sink for the local and semi-global forms. [Longest path in a DAG](/dag-longest-path/) takes time linear in the size of the graph, which is $\Theta(mn)$.
- **From LCS and edit distance.** The [longest common subsequence](/longest-common-subsequence/) is global alignment with $s(a, a) = 1$, $s(a, b) = 0$ and $d = 0$. The Levenshtein [edit distance](/edit-distance/) is minus the global score with $s(a, a) = 0$, $s(a, b) = -1$ and $d = 1$. Both reductions take $O(1)$ time.
- **From approximate string matching.** Finding a substring of a text close to a pattern is the fitting form with unit costs; [Sellers' algorithm](/sellers-algorithm/) is the semi-global table for it.
- **Local to global.** The best local alignment is the best global alignment of some pair of substrings, so $O(m^2 n^2)$ global problems solve it; the zero floor of [Smith-Waterman](/smith-waterman/) removes this factor.

## Applications

- Database search for homologous genes and proteins: [BLAST](/blast/) and [FASTA](/fasta-algorithm/) report local alignments, with [E-values](/e-value/) from [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- [Read mapping](/read-mapping/): after a seed finds a candidate place, a banded semi-global or local alignment gives the final position and the differences.
- Genome assembly: [overlap detection](/overlap-detection/) between reads is overlap alignment.
- Phylogenetics and protein structure: pairwise alignments are the input of [multiple sequence alignment](/multiple-sequence-alignment/) and of distance-based tree methods.

## References
