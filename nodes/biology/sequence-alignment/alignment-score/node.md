---
tag: 0GS6F6
kind: concept
slug: alignment-score
name: Alignment score
aliases:
- alignment cost
area: biology/sequence-alignment
level: intro
summary: The number a scoring scheme gives to an alignment of two sequences, the sum of the substitution scores of its aligned pairs minus the penalties of its gaps.
prereqs: [edit-operations]
see_also: [pairwise-sequence-alignment, substitution-matrix, gap-penalty, alignment-graph, edit-distance, weighted-edit-distance, longest-common-subsequence, karlin-altschul-statistics]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 (the scoring model, substitution scores as log-odds ratios, and the linear and affine gap penalties)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the sections on string similarity (the value of an alignment and its relation to weighted edit distance) and on gaps
  - paper: doi:10.1007/BF01733210
    title: Temple F. Smith, Michael S. Waterman and Walter M. Fitch, Comparative biosequence metrics, Journal of Molecular Evolution 18(1), 1981, 38-46
    locator: the comparison of the similarity measure of Needleman and Wunsch with the distance of Sellers, and the conditions under which they give the same optimal alignments
  - paper: doi:10.1137/0126070
    title: Peter H. Sellers, On the theory and computation of evolutionary distances, SIAM Journal on Applied Mathematics 26(4), 1974, 787-793
    locator: the evolutionary distance between two sequences as a minimum over alignments
---

The alignment score is the number that a scoring scheme gives to an [alignment](/pairwise-sequence-alignment/) of two sequences: the sum of the substitution scores of the aligned pairs of letters, minus a penalty for each gap. The scoring scheme has two parts, a [substitution matrix](/substitution-matrix/) $s(a, b)$ and a [gap penalty](/gap-penalty/) $g(L)$. Alignment algorithms look for the alignment with the largest score, so the score is the objective that every page of this area optimizes. It is the similarity form of the [edit distance](/edit-distance/): edit distance counts a cost and minimizes it, the score counts a reward and maximizes it, and for global alignment the two views give the same optimal alignments.

## In plain words

Write two DNA or protein sequences one above the other, and put gap symbols into them so that the two rows have the same length. Each column now holds two letters, or one letter and a gap. A table says how good each pair of letters is: the same letter scores well, a similar amino acid scores a little, and a very different one scores badly. Each gap costs a penalty, because an insertion or a deletion is a rare event in evolution.

Add the numbers of all the columns. That total is the score of the alignment. A high score says that the two rows line up letters that could share an ancestor. The same two sequences have a very large number of alignments, and the alignment algorithms find the one with the highest total without trying them all.

## The idea

### Alignments

Let $\Sigma$ be the alphabet: $\{A, C, G, T\}$ for DNA, $\{A, C, G, U\}$ for RNA, or the 20 amino acids. Let the gap symbol $-$ be outside $\Sigma$. An *alignment* of $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ is a pair of rows $(\bar x, \bar y)$ over $\Sigma \cup \{-\}$ with the same length $L$, such that

- deleting each $-$ from $\bar x$ gives $x$, and deleting each $-$ from $\bar y$ gives $y$;
- no column $k$ has $\bar x_k = \bar y_k = -$.

So $\max(m, n) \le L \le m + n$. A column is an *aligned pair* $(a, b)$ (a match if $a = b$, else a mismatch), a *deletion* $(a, -)$ or an *insertion* $(-, b)$. These are the three [edit operations](/edit-operations/), read as columns. A *gap* is a maximal run of consecutive columns that have $-$ in the same row; its length is the number of those columns.

### The score

A scoring scheme is a function $s : \Sigma \times \Sigma \to \mathbb{R}$ and a gap penalty $g : \{1, 2, \ldots\} \to \mathbb{R}_{\ge 0}$. The score of an alignment $A$ is

$$S(A) = \sum_{\text{pairs } (a, b) \text{ of } A} s(a, b) \; - \sum_{\text{gaps } G \text{ of } A} g(|G|).$$

Two gap models cover nearly all practice.

- **Linear gaps:** $g(L) = dL$ with $d \ge 0$. Then each gap column costs $d$, and $S(A)$ is a sum over the columns. This is what makes the plain dynamic programs ([Needleman-Wunsch](/needleman-wunsch/), [Smith-Waterman](/smith-waterman/)) work with one table. See [linear gap penalty](/linear-gap-penalty/).
- **Affine gaps:** $g(L) = d + (L - 1)e$ with $d \ge e \ge 0$, the convention of Durbin et al. Other books write $g(L) = o + Le$, so their opening cost $o$ is $d - e$ here; check the convention before you copy parameters. The score is no longer a sum over columns, because a gap column costs $d$ or $e$ depending on its left neighbour. See [affine gap penalty](/affine-gap-penalty/) and the [Gotoh algorithm](/gotoh-algorithm/).

For proteins, $s$ is usually a log-odds matrix such as BLOSUM62 or PAM250: $s(a, b)$ is proportional to $\log \frac{p_{ab}}{q_a q_b}$, where $p_{ab}$ is the frequency of the pair in trusted alignments of related proteins and $q_a$ is the background frequency of $a$. So the score of an ungapped alignment is the log of a likelihood ratio, related sequences against random ones. The [substitution matrix](/substitution-matrix/) page derives this.

### Similarity and distance

The [edit distance](/edit-distance/) view gives each column a cost and minimizes the sum. For global alignments the two views are the same up to a change of parameters.

**Claim.** Let $\delta(a, b) \ge 0$ be a substitution cost and $\gamma$ a cost per gap symbol, and let $D(A)$ be the total cost of an alignment $A$ of $x$ and $y$. Fix a constant $M$, and set $s(a, b) = M - \delta(a, b)$ and $d = \gamma - M/2$. Then $S(A) = \frac{M}{2}(m + n) - D(A)$ for each global alignment $A$ of $x$ and $y$.

*Proof.* Let $A$ have $p$ aligned pairs and $q$ gap columns. Each pair uses one letter of each sequence, and each gap column uses one letter, so $2p + q = m + n$. Then $S(A) = \sum (M - \delta(a, b)) - qd = pM - \sum \delta(a, b) - q\gamma + qM/2 = \frac{M}{2}(2p + q) - D(A)$. $\square$

The term $\frac{M}{2}(m + n)$ is the same for every global alignment of $x$ and $y$, so the alignments of largest score are exactly the alignments of least cost. Smith, Waterman and Fitch (1981) compared the similarity of Needleman and Wunsch with the distance of Sellers (1974) in this way. The claim fails for [local alignment](/local-alignment/), because there the aligned parts, and so $m + n$, change from one candidate to the next. That is why local alignment needs a similarity score.

### Special cases

- **[Longest common subsequence](/longest-common-subsequence/).** With $s(a, a) = 1$, $s(a, b) = 0$ for $a \ne b$ and $d = 0$, the score counts the match columns, and the best score is the length of an LCS.
- **Levenshtein distance.** With $s(a, a) = 0$, $s(a, b) = -1$ for $a \ne b$ and $d = 1$, the best score is minus the edit distance. A general $\delta$ gives the [weighted edit distance](/weighted-edit-distance/).

### Expected score of a random column

If the letters of both sequences are independent with frequencies $q_a$, the expected score of an aligned pair is $E = \sum_{a, b} q_a q_b \, s(a, b)$. Local alignment and the [Karlin-Altschul statistics](/karlin-altschul-statistics/) need $E < 0$ and at least one positive $s(a, b)$: otherwise a long random alignment gets a high score only because it is long. A raw score depends on the units of $s$; the [bit score](/bit-score/) rescales it so that scores from different matrices can be compared.

## Examples

All examples use the toy DNA scheme of the pages of this area: $s(a, a) = +2$, $s(a, b) = -1$ for $a \ne b$, and a linear gap penalty $d = 2$.

**Four alignments of ACGTC and AGTAC.** The table also gives the score under the LCS scheme and under the Levenshtein scheme of the previous section.

| alignment (top over bottom) | toy score | LCS score | Levenshtein score |
|---|---|---|---|
| `ACGT-C` over `A-GTAC` | $2 - 2 + 2 + 2 - 2 + 2 = 4$ | 4 | $-2$ |
| `ACGTC` over `AGTAC` | $2 - 1 - 1 - 1 + 2 = 1$ | 2 | $-3$ |
| `ACGTC-` over `A-GTAC` | $2 - 2 + 2 + 2 - 1 - 2 = 1$ | 3 | $-3$ |
| `-ACGTC` over `AGTAC-` | $-2 - 1 - 1 - 1 - 1 - 2 = -8$ | 0 | $-6$ |

The first alignment is optimal under all three schemes; the [Needleman-Wunsch](/needleman-wunsch/) page computes it. The two strings have 1683 alignments in total (see [alignment graph](/alignment-graph/) for the count).

**The distance view of the toy scheme.** Take $M = 2$. Then $s = M - \delta$ gives $\delta(a, a) = 0$ and $\delta(a, b) = 3$, and $d = \gamma - M/2$ gives $\gamma = 3$. So for two DNA strings of total length $m + n$, the best toy score is $(m + n)$ minus the least cost of an alignment in which each mismatch and each gap symbol costs 3. For ACGTC and AGTAC the best score is 4 and $m + n = 10$, so the least cost is 6: the two gap symbols of the first alignment.

**Linear and affine penalties.** Take an alignment with one gap of length 3. With $d = 2$ the gap costs 6. With the affine penalty $g(L) = 5 + (L - 1) \cdot 1$ it costs 7. Three separate gaps of length 1 cost 6 under the linear penalty and 15 under the affine one. The affine model prefers one long gap to many short ones, which fits the biology: one insertion event often adds several letters.

**Expected score.** For uniform DNA, $q_a = 1/4$, and the toy scheme gives $E = \frac{1}{4} \cdot 2 + \frac{3}{4} \cdot (-1) = -\frac{1}{4} < 0$. So the toy scheme is a valid scheme for local alignment. With a mismatch score of $+1$ instead, $E = 5/4 > 0$, and the best local alignment of two random sequences would cover most of both.

## Where it is used

- [Pairwise sequence alignment](/pairwise-sequence-alignment/) in its [global](/global-alignment/), [local](/local-alignment/) and [semi-global](/semi-global-alignment/) forms maximizes this score.
- The [alignment graph](/alignment-graph/) puts the column scores on the edges of a grid, so the best alignment is a heaviest path.
- [Multiple sequence alignment](/multiple-sequence-alignment/) adds the pairwise scores in the [sum-of-pairs score](/sum-of-pairs-score/).
- [BLAST](/blast/) reports a raw score, the [bit score](/bit-score/) and the [E-value](/e-value/), from [Karlin-Altschul statistics](/karlin-altschul-statistics/).
- A [pair HMM](/pair-hmm/) gives a probabilistic reading of the same score: the log-odds of an alignment under a model of related sequences against a model of random ones.

## References
