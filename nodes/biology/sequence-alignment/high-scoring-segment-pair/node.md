---
tag: 7SVH0B
kind: concept
slug: high-scoring-segment-pair
name: High-scoring segment pair
aliases:
- HSP
- locally maximal segment pair
area: biology/sequence-alignment
level: core
summary: A pair of equal-length segments of two sequences, aligned with no gaps, whose score cannot be raised by moving either end. BLAST reports these local alignments.
prereqs: [local-alignment, substitution-matrix]
see_also: [blast, seed-and-extend, karlin-altschul-statistics, e-value, bit-score, maximum-subarray-problem, x-drop-extension, smith-waterman]
sources:
  - paper: doi:10.1016/S0022-2836(05)80360-2
    title: Stephen F. Altschul, Warren Gish, Webb Miller, Eugene W. Myers and David J. Lipman, Basic local alignment search tool, Journal of Molecular Biology 215(3), 1990
    locator: pages 403 to 410, Introduction and Methods (the maximal segment pair, locally maximal segment pairs after Sellers, and the HSPs found by word extension)
  - paper: doi:10.1073/pnas.87.6.2264
    title: Samuel Karlin and Stephen F. Altschul, Methods for assessing the statistical significance of molecular sequence features by using general scoring schemes, PNAS 87(6), 1990
    locator: pages 2264 to 2268 (the distribution of the maximal segment score and the number of high-scoring segments)
  - paper: "Peter H. Sellers, Pattern recognition in genetic sequences by mismatch density, Bulletin of Mathematical Biology 46(4), 1984, pages 501 to 514"
    title: Sellers 1984
    locator: the notion of a locally optimal (locally maximal) segment pair
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, the sections on heuristic alignment algorithms (BLAST) and on the significance of scores
---

A high-scoring segment pair (HSP) is a pair of segments of the same length, one from each of two sequences, aligned letter by letter with no gaps, whose score cannot be raised by extending or shortening the segments. The best HSP over all positions is the maximal segment pair (MSP). [BLAST](/blast/) finds HSPs by [seed and extend](/seed-and-extend/) and reports each one with a score, a [bit score](/bit-score/) and an [E-value](/e-value/). The [Karlin-Altschul statistics](/karlin-altschul-statistics/) give the number of HSPs above a score in random sequences.

## In plain words

Write one sequence above the other and slide it to some offset. At this offset each letter faces one letter of the other sequence. Each facing pair gets a score from a table: a high score for the same or a similar letter, a low score for a bad match. Now pick a stretch of the facing pairs and add up their scores.

An HSP is a stretch where the total is high and cannot get higher. If you make the stretch longer at either end, you add bad pairs. If you make it shorter, you remove good pairs. So the stretch is a peak. Many offsets have a few small peaks by chance. A long and high peak means that the two sequences share a real piece.

## The idea

**The model.** The two sequences are $q = q_1 \cdots q_m$ (the query) and $y = y_1 \cdots y_n$ (the subject) over an alphabet $\Sigma$: the four DNA bases or the 20 amino acids. A [substitution matrix](/substitution-matrix/) $s(a, b)$ gives an integer score to each pair of letters, for example [BLOSUM62](/blosum-matrix/) for proteins or $+1/-2$ (match $+1$, mismatch $-2$) for DNA. There is no gap model: an HSP has no gaps.

**Segment pairs.** A segment pair of length $L$ is $q_{i+1} \cdots q_{i+L}$ together with $y_{j+1} \cdots y_{j+L}$. Its score is

$$S = \sum_{t=1}^{L} s(q_{i+t}, y_{j+t}).$$

All letter pairs of the segment pair lie on one diagonal $d = j - i$ of the $m \times n$ [dot matrix](/dot-matrix-plot/). A segment pair is an ungapped [local alignment](/local-alignment/).

**Locally maximal.** Sellers (1984) and Altschul et al. (1990) call a segment pair *locally maximal* if no extension or shortening of the two segments gives a higher score. The 1990 BLAST paper defines the MSP as the highest scoring pair of segments of the same length, and calls a locally maximal segment pair with score at least a cutoff $S$ a high-scoring segment pair.

**A test on one diagonal.** Number the cells of diagonal $d$ as $1, \ldots, D$ and let $P_0 = 0$ and $P_t$ be the sum of the first $t$ cell scores. The segment of cells $a+1, \ldots, b$ has score $P_b - P_a$. Moving the left end changes only $P_a$, and moving the right end changes only $P_b$. So the segment is locally maximal if and only if

$$P_a = \min_{0 \le t \le b} P_t \quad \text{and} \quad P_b = \max_{a \le t \le D} P_t,$$

because a strictly smaller $P_{a'}$ with $a' < b$, or a strictly larger $P_{b'}$ with $b' > a$, would give a higher score. With $P_b > P_a$ the score is positive. This is the [maximum subarray problem](/maximum-subarray-problem/) for each diagonal, with all its local peaks kept.

**Properties that follow.** Each proper prefix and each proper suffix of an HSP has a score of at least 0, because otherwise cutting it off raises the score. Each stretch that touches an HSP on the same diagonal, on the left or on the right, has a score of at most 0. Two different HSPs on one diagonal can share cells only when their prefix sums tie at both ends ($P_a = P_{a'}$ and $P_b = P_{b'}$), so with no ties they are disjoint.

**The MSP.** The MSP is the HSP with the highest score. [Kadane's algorithm](/kadane-algorithm/) on each of the $m + n - 1$ diagonals finds it in $O(mn)$ time and $O(1)$ extra space. This is exact. BLAST does not compute it this way, because $mn$ is too large for a database.

**HSPs in BLAST output.** BLAST extends each word hit along its diagonal and stops with the X-drop rule (see [X-drop extension](/x-drop-extension/)). The reported segment is the best one that the extension saw. It is a true segment pair with a true score, but the X-drop stop can end it before a higher peak further along, so it is not always locally maximal in the strict sense above. Gapped BLAST (1997) starts its gapped extension from an HSP and reports gapped local alignments, which the BLAST output still calls HSPs. This page uses the strict ungapped meaning.

**MSP and HSP are not the same.** There is one MSP score per sequence pair, but there can be many HSPs. The alias "maximal segment pair" names the best HSP. The Karlin-Altschul theorem describes both: the MSP score has an extreme value distribution, and the number of HSPs with score at least $S$ is about Poisson with mean $K m n e^{-\lambda S}$.

## Examples

**One pair of DNA sequences.** Take $q = $ GATTACAGT and $y = $ CATTAGAGT, with match $+1$ and mismatch $-2$. On the main diagonal $d = 0$ the pairs are G/C, A/A, T/T, T/T, A/A, C/G, A/A, G/G and T/T, with scores $-2, 1, 1, 1, 1, -2, 1, 1, 1$. The prefix sums are

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $P_t$ | 0 | $-2$ | $-1$ | 0 | 1 | 2 | 0 | 1 | 2 | 3 |

The minimum is $P_1 = -2$ and the maximum after it is $P_9 = 3$, so cells 2 to 9 form an HSP with score $5$: ATTACAGT against ATTAGAGT. It has a mismatch inside it (C/G). The two parts ATTA (score 4) and AGT (score 3) are not HSPs, because joining them across the mismatch gives $4 - 2 + 3 = 5$, which is higher than each part.

Over all 17 diagonals, the strict test finds 14 locally maximal segment pairs with a positive score:

| score | count | segment pairs |
|---|---|---|
| 5 | 1 | ATTACAGT / ATTAGAGT on $d = 0$ (the MSP) |
| 2 | 3 | GA / GA ($q_1 q_2$ and $y_6 y_7$), CA / CA ($q_6 q_7$ and $y_1 y_2$), AG / AG ($q_7 q_8$ and $y_5 y_6$) |
| 1 | 10 | single matching letters |

With a cutoff $S = 3$ only the MSP is an HSP. With $S = 2$ there are four.

**A protein word.** With BLOSUM62, the segment pair PQG against PEG scores $7 + 2 + 6 = 15$. Extending it with one more pair on either side adds that pair's score, so whether it grows into a larger HSP depends on the letters next to it.

**Random sequences.** Two random sequences of length 500 and $10^9$ with uniform bases and $+1/-2$ scores have about $0.82$ HSPs of score 20 or more by chance (the [E-value](/e-value/) page gives the numbers). Real homologs give HSPs far above this.

## Where it is used

- **BLAST.** Each word hit is extended to an HSP, and HSPs with score at least $S$ are reported or passed to the gapped stage. See [BLAST](/blast/) and [seed and extend](/seed-and-extend/).
- **Statistics of local alignment.** The Karlin-Altschul theorem is a statement about MSP scores and HSP counts of random sequences. It defines $\lambda$, $K$, the [E-value](/e-value/) and the [bit score](/bit-score/).
- **Sum statistics.** BLAST can combine several HSPs of one sequence pair, which are consistent in order, into one significance value (Karlin and Altschul, 1993). This helps when gaps break a match into pieces.
- **Chaining.** Long-read and whole-genome aligners chain ungapped anchors into a longer match. See [seed chaining](/seed-chaining/).
- **Dot plots.** The diagonal runs in a [dot matrix plot](/dot-matrix-plot/) are HSPs seen by eye.

An HSP differs from a [Smith-Waterman](/smith-waterman/) alignment because it allows no gaps. Its score is at most the Smith-Waterman score of the same pair, with any gap penalty, since an HSP is one of the local alignments that the Smith-Waterman recurrence scores. On the problem side, the MSP of one diagonal is exactly the [maximum subarray problem](/maximum-subarray-problem/), which other areas cover.

## References
