---
tag: 2E8VG6
kind: problem
slug: local-alignment
name: Local alignment
aliases:
- local sequence alignment
- best-scoring substring alignment
area: biology/sequence-alignment
level: core
summary: Find a substring of each of two sequences whose global alignment has the largest score; the poorly matching flanks are left out at no cost.
prereqs: [global-alignment]
see_also: [smith-waterman, global-alignment, semi-global-alignment, maximum-subarray-problem, karlin-altschul-statistics, blast, high-scoring-segment-pair, longest-common-substring]
sources:
  - paper: doi:10.1016/0022-2836(81)90087-5
    title: Temple F. Smith and Michael S. Waterman, Identification of common molecular subsequences, Journal of Molecular Biology 147(1), 1981, 195-197
    locator: the definition of the maximally similar pair of segments and the algorithm that finds it
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.3 (local alignment, the condition of a negative expected score, and repeated matches)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the section on local alignment
  - paper: doi:10.1016/0022-2836(87)90478-5
    title: Michael S. Waterman and Mark Eggert, A new algorithm for best subsequence alignments with application to tRNA-rRNA comparisons, Journal of Molecular Biology 197(4), 1987, 723-728
    locator: the computation of the best local alignments that do not share a pair
  - paper: doi:10.1214/aoap/1177005208
    title: Richard Arratia and Michael S. Waterman, A phase transition for the score in matching random sequences allowing deletions, Annals of Applied Probability 4(1), 1994, 200-225
    locator: the linear and the logarithmic growth of the best local score, depending on the scoring parameters
---

Local alignment is the form of [pairwise sequence alignment](/pairwise-sequence-alignment/) that looks for the best-matching parts of two sequences. It chooses a substring of each sequence and an alignment of the two substrings, so that the [alignment score](/alignment-score/) is as large as possible. The letters outside the chosen substrings cost nothing. This is the right question when two sequences share only a domain, a motif or a conserved region inside unrelated flanks. The [Smith-Waterman algorithm](/smith-waterman/) solves it in $O(mn)$ time for lengths $m$ and $n$. The score must have a negative expected value on random letters; otherwise the best local alignment of two random sequences is nearly global.

## In plain words

Two proteins can be very different overall but share one part that does the same job. If you force an alignment of the whole sequences, the unrelated parts add many bad columns, and the shared part is hidden in a low total.

Local alignment lets you choose where to start and where to stop in each sequence. Only the chosen pieces are scored, and everything outside them is ignored. You look for the pair of pieces that gives the highest score. If the two sequences share nothing, the best choice is to take nothing, with a score of zero. For this to work, a random pair of letters must score below zero on average; otherwise longer pieces always look better, even when they are not related.

## Definition

**Model.** The alphabet $\Sigma$ is DNA, RNA or the 20 amino acids. The input is $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a substitution score $s : \Sigma \times \Sigma \to \mathbb{Z}$ and a linear gap penalty $d \ge 0$ per gap symbol, unless a variant says otherwise. The costs are in the [word RAM](/word-ram/) model.

Write $x[i..i']$ for the substring $x_i \cdots x_{i'}$, empty if $i' < i$, and $\operatorname{OPT}_{\mathrm{glob}}(u, v)$ for the best global alignment score of $u$ and $v$ (see [global alignment](/global-alignment/)).

**Output.** Substrings $u = x[i..i']$ and $v = y[j..j']$ and an optimal global alignment of $u$ and $v$, such that

$$\operatorname{OPT}_{\mathrm{loc}}(x, y) = \max_{u \text{ substring of } x,\ v \text{ substring of } y} \operatorname{OPT}_{\mathrm{glob}}(u, v)$$

is attained. The empty substrings give the score 0, so $\operatorname{OPT}_{\mathrm{loc}} \ge 0$.

**The scoring condition.** Let $q_a$ be the background frequency of the letter $a$. The definition makes sense for every $s$ and $d$, but it finds related regions only if the expected score of a random pair is negative, $\sum_{a, b} q_a q_b \, s(a, b) < 0$, and some $s(a, a) > 0$. Durbin et al. state this condition for local alignment. Arratia and Waterman (1994) proved that, for random sequences, the best local score grows linearly with the length for some scoring parameters and logarithmically for others, with a sharp change between the two regimes. Only in the logarithmic regime does a high local score point to a real similarity.

## Variants

- **Affine gaps.** A gap of length $L$ costs $d + (L - 1)e$. The [Gotoh algorithm](/gotoh-algorithm/) with a floor of 0 solves it in $O(mn)$ time; this is the form that [BLAST](/blast/) and most protein search tools use.
- **Ungapped local alignment.** Without gaps, a local alignment lies on one diagonal of the [alignment graph](/alignment-graph/), and the best one on a diagonal is a [maximum subarray](/maximum-subarray-problem/) of the scores $s(x_i, y_{i + c})$. This is a [high-scoring segment pair](/high-scoring-segment-pair/), and its score has the exact statistics of [Karlin and Altschul](/karlin-altschul-statistics/).
- **Several local alignments.** Find the best $k$ local alignments that share no aligned pair (Waterman and Eggert, 1987), or all the local alignments above a threshold (the repeated matches of Durbin et al.).
- **Fitting and overlap.** If one end of the alignment is fixed to the end of a sequence, the problem is [semi-global alignment](/semi-global-alignment/).
- **Banded or seeded.** Search only near a diagonal or around a seed hit: [banded Smith-Waterman](/banded-smith-waterman/), [X-drop extension](/x-drop-extension/) and [seed-and-extend](/seed-and-extend/).
- **Probabilistic form.** A local [pair HMM](/pair-hmm/) adds random flanking states, and the sum over its paths scores the relation of the two sequences without choosing one alignment.

## Examples

All examples use the toy DNA scheme: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, $d = 2$. Its expected score on uniform DNA is $\frac{1}{4} \cdot 2 - \frac{3}{4} \cdot 1 = -\frac{1}{4} < 0$, so the condition holds.

| $x$ | $y$ | global | local | local alignment |
|---|---|---|---|---|
| TCAGTTGCA | GAGTGCAT | 5 | 10 | `AGTTGCA` over `AG-TGCA`, $x[3..9]$ and $y[2..7]$ |
| TTCAGTAC | AGTACGGA | $-2$ | 10 | `AGTAC` over `AGTAC`, $x[4..8]$ and $y[1..5]$ |
| CAGGTACT | TAGTAC | 5 | 8 | `GTAC` over `GTAC`, $x[4..7]$ and $y[3..6]$ |
| ACGTC | AGTAC | 4 | 4 | `AC` over `AC`, $x[1..2]$ and $y[4..5]$ |
| AAAA | CCCC | $-4$ | 0 | the empty alignment |

In the first row, the local alignment keeps one gap, because the two matches AG before the gap earn 4 and the gap costs only 2. In the last row, every pair of letters mismatches, so the best choice is to align nothing.

The fourth row shows that the local optimum need not be unique: for ACGTC and AGTAC, the alignment `ACGT-C` over `A-GTAC` of the whole strings also scores 4. [Smith-Waterman](/smith-waterman/) returns one of the optimal alignments, by its rule for ties.

**A positive expected score.** With $s(a, a) = +2$, $s(a, b) = +1$ and $d = 2$, every pair scores well, and the best local alignment of two random DNA sequences of length $n$ covers almost all of both. The score then says little about relation, and the local form fails.

## Known algorithms

| algorithm | gaps | time (worst case) | space |
|---|---|---|---|
| Brute force over the pairs of substrings | any | $O(m^2 n^2)$ global problems | |
| [Smith-Waterman](/smith-waterman/) | linear | $\Theta(mn)$ | $\Theta(mn)$, or $\Theta(\min(m, n))$ for the score |
| Smith-Waterman with the [Gotoh](/gotoh-algorithm/) recurrences | affine | $\Theta(mn)$ | $\Theta(mn)$ |
| Smith-Waterman for the end cell, then [Hirschberg](/hirschberg-algorithm/) between the ends | linear or affine | $\Theta(mn)$ | $O(\min(m, n))$ plus the output |
| [Banded Smith-Waterman](/banded-smith-waterman/) | linear or affine | $O(k \max(m, n))$ for a band of width $k$ | |
| Crochemore, Landau and Ziv-Ukelson (2003) | linear, constant alphabet | $O(n^2 / \log n)$ for $m = n$ | |

Heuristics for database search, [BLAST](/blast/), the [FASTA algorithm](/fasta-algorithm/) and [seed-and-extend](/seed-and-extend/) in general, run much faster, but they can miss an optimal local alignment that contains no exact seed.

## Bounds

- **Upper.** $O(mn)$ time with linear or affine gaps, and $O(n^2 / \log n)$ over a constant alphabet with an arbitrary scoring matrix.
- **Lower, conditional.** With $s(a, a) = 1$, $s(a, b) = 0$ and $d = 0$, no column has a negative score, so extending an alignment to the whole strings never lowers it, and $\operatorname{OPT}_{\mathrm{loc}}$ equals the length of a [longest common subsequence](/longest-common-subsequence/). So local alignment with this fixed scheme is as hard as LCS, and under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/) it has no $O(n^{2 - \varepsilon})$ algorithm (see the [Backurs-Indyk LCS lower bound](/backurs-indyk-lcs-lower-bound/)). This scheme breaks the scoring condition, so the argument says nothing about the schemes used in practice.
- **Lower, trivial.** $\Omega(m + n)$ to read the input.

## Reductions

- **To global alignment.** $\operatorname{OPT}_{\mathrm{loc}}$ is the maximum of $O(m^2 n^2)$ global problems, one per pair of substrings. The Smith-Waterman recurrence removes this factor: a floor of 0 in each cell starts a new alignment for free.
- **To a longest path.** Add a source with an edge of weight 0 to each vertex of the [alignment graph](/alignment-graph/) and an edge of weight 0 from each vertex to a sink. A heaviest source-to-sink path is an optimal local alignment, so [longest path in a DAG](/dag-longest-path/) solves the problem in $\Theta(mn)$ time.
- **Ungapped form and the maximum subarray problem.** Without gaps, the best local alignment on one diagonal is a [maximum subarray](/maximum-subarray-problem/) of the column scores, which [Kadane's algorithm](/kadane-algorithm/) finds in linear time. In the other direction, take numbers $a_1, \ldots, a_n$, let $x = y = 1 2 \cdots n$ over the alphabet $\{1, \ldots, n\}$, set $s(i, i) = a_i$, and give each mismatch the score $-C$ and each gap symbol the penalty $C$, for $C$ larger than $\sum |a_i|$. Then no optimal local alignment has a mismatch or a gap, and its score is the maximum subarray sum (0 for the empty subarray).
- **From the longest common substring.** With $s(a, a) = 1$, a very negative mismatch score and a very large $d$, the best local alignment is a [longest common substring](/longest-common-substring/). That problem has a linear-time solution with a [suffix tree](/suffix-tree/), so this special case is easier than the general one.

## Applications

- Database search: [BLAST](/blast/) and [FASTA](/fasta-algorithm/) report local alignments of a query with each database sequence, ranked by [E-value](/e-value/) under [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- Protein domains: two multi-domain proteins that share one domain align well only in that domain.
- [Read mapping](/read-mapping/): a local alignment of a read can clip its ends, for example adapter sequence or a low-quality tail.
- Repeats and motifs: the best local alignments of a sequence with itself, off the main diagonal, are its repeats.

## References
