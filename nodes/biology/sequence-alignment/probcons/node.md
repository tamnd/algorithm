---
tag: VPNKKD
kind: algorithm
slug: probcons
name: ProbCons
aliases:
- probabilistic consistency
- probabilistic consistency transformation
area: biology/sequence-alignment
level: research
summary: A progressive multiple aligner that scores residue pairs by pair-HMM posterior probabilities, made consistent through third sequences, and aligns for maximum expected accuracy.
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence, L: the length of the alignment, R: the number of refinement rounds}
  time: {worst: "O(k^3 n^3 + R k^2 L^2)"}
  space: {extra: "O(k^2 n^2 + L^2)"}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2005
  people: [Chuong B. Do, Mahathi S. P. Mahabhashyam, Michael Brudno, Serafim Batzoglou]
  note: ProbCons combined three ideas, posterior probabilities from a pair-HMM, maximum expected accuracy alignment, and the consistency of T-Coffee, and was the most accurate aligner on the BAliBASE, SABmark and PREFAB benchmarks in its paper.
prereqs: [progressive-alignment, pair-hmm, forward-backward-algorithm, t-coffee]
see_also: [multiple-sequence-alignment, iterative-refinement-alignment, sum-of-pairs-score, hidden-markov-model, profile-hmm, mafft, muscle, clustal]
sources:
  - paper: doi:10.1101/gr.2821705
    title: Chuong B. Do, Mahathi S. P. Mahabhashyam, Michael Brudno and Serafim Batzoglou, ProbCons, probabilistic consistency-based multiple sequence alignment, Genome Research 15(2), 2005, pages 330 to 340
    locator: the three-state pair-HMM, Steps 1 to 5 (posteriors, expected accuracies, the consistency transformation applied twice, the guide tree, progressive alignment), 100 rounds of iterative refinement, and the sparse product with threshold 0.01
  - paper: doi:10.1006/jmbi.2000.4042
    title: Cédric Notredame, Desmond G. Higgins and Jaap Heringa, T-Coffee, a novel method for fast and accurate multiple sequence alignment, Journal of Molecular Biology 302(1), 2000, pages 205 to 217
    locator: library extension, the consistency idea that ProbCons makes probabilistic
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 4, pair HMMs, the forward and backward algorithms, and posterior probabilities of aligned residue pairs
---

ProbCons is a method for [multiple sequence alignment](/multiple-sequence-alignment/) by Chuong Do, Mahathi Mahabhashyam, Michael Brudno and Serafim Batzoglou, published in 2005. It is a [progressive aligner](/progressive-alignment/) built on a [pair hidden Markov model](/pair-hmm/). For every pair of sequences it computes the posterior probability that residue $i$ of one is aligned with residue $j$ of the other. It then applies the *probabilistic consistency transformation*: the probability for $x_i$ and $y_j$ is re-estimated as an average, over all sequences $z$, of the chance to go from $x_i$ to a residue of $z$ and on to $y_j$. Groups are aligned to maximize the expected number of correctly aligned residue pairs, with no gap penalties, and the result is improved by random two-way splits and realignment. It applies the consistency idea of [T-Coffee](/t-coffee/) in a probabilistic form.

## In plain words

For two sequences, a probabilistic model can say how likely each pair of letters is to belong in the same column, by averaging over all ways to align the two. These numbers are better guides than a single best alignment, because they show how sure the model is.

ProbCons computes these numbers for every pair of sequences. Then it lets the other sequences vote. If letter x is likely paired with some letter of a third sequence, and that letter is likely paired with letter y, then x and y gain support. Pairs that no third sequence supports lose weight.

Then the sequences are aligned along a tree, so that the total of these numbers in the columns is as large as possible. Finally the sequences are split at random into two groups and realigned many times.

## The problem

The input is $k$ sequences $S_1, \ldots, S_k$ and a pair-HMM. The output is a multiple alignment: rows of equal length, row $i$ spelling $S_i$ with gaps added, and no column of gaps only. The goal is an alignment with many correct residue pairs. ProbCons measures an alignment by its *expected accuracy*: the sum, over pairs of rows and over columns, of the posterior probability of the residue pair in the column. This is a [sum-of-pairs score](/sum-of-pairs-score/) in which the pair score of two residues is a posterior probability and gaps score 0. Each step optimizes this score for a pair of groups; the whole alignment is not proved optimal.

## The algorithm

```pseudo id=main
PROBCONS(S[1..k], R)
L1  for each pair x, y do P_xy(i, j) ← Pr(x_i is aligned with y_j | x, y), by the forward and backward algorithms on the pair-HMM
L2  for each pair x, y do E(x, y) ← (largest sum of P_xy(i, j) over the matched pairs of an alignment of x and y) / min(|x|, |y|)
L3  repeat 2 times: for each pair x, y do P′_xy ← (1/k) Σ over all sequences z of P_xz P_zy, with P_xx the identity matrix
L4  G ← join the two clusters with the largest E, set E(xy, z) ← E(x, y) (E(x, z) + E(y, z)) / 2, and repeat
L5  A ← PROGRESSIVE(G, S), where two columns score Σ P′_xy(i, j) over their residue pairs and gaps score 0
L6  repeat R times
L7      split the rows of A at random into two groups, and remove the columns of gaps only in each group
L8      A ← the best block alignment of the two groups under the same column score
L9  return A
```

**The pair-HMM (line L1).** The model has a match state that emits two aligned letters and two insert states that emit a letter of one sequence against a gap. The forward value $f_M(i, j)$ is the total probability of all paths that emit $x_1 \ldots x_i$ and $y_1 \ldots y_j$ and end with $x_i$ matched to $y_j$; the backward value $b_M(i, j)$ is the probability of emitting the rest from there. Then $P_{xy}(i, j) = f_M(i, j)\, b_M(i, j) / \Pr(x, y)$. The paper trains the transition and emission parameters by expectation maximization; the implementation uses fixed values.

**Maximum expected accuracy (lines L2, L5 and L8).** The alignment of two sequences that maximizes the expected number of correct residue pairs is found by the [Needleman-Wunsch](/needleman-wunsch/) recurrence with $P_{xy}(i, j)$ as the score of a match and 0 for a gap. The paper defines the expected accuracy $E(x, y)$ as this maximum divided by the length of the shorter sequence. For two groups, a column pair scores the sum of $P'_{xy}(i, j)$ over the residue pairs of the two columns.

**Consistency (line L3).** In matrix form $P'_{xy} = \frac{1}{k} \sum_z P_{xz} P_{zy}$, where $z$ runs over all $k$ sequences, including $x$ and $y$, for which $P_{xx}$ and $P_{yy}$ are identity matrices; so the direct estimate $P_{xy}$ is one of the $k$ terms. The paper applies the transformation twice by default and keeps only entries above 0.01, so the products are sparse.

**Guide tree and refinement (lines L4 and L6 to L8).** The tree joins the most similar clusters first, with the similarity update of line L4. Refinement splits the sequences into two random groups, of possibly unequal size, and realigns them. Because there are no gap penalties, the current alignment of the two groups is one of the block alignments considered, so the score cannot go down. The paper uses 100 rounds.

## Example

The implementation uses a DNA pair-HMM with gap open probability 0.2, gap extend probability 0.4, emission 0.2 for each identical pair and $0.2/12$ for each different pair in the match state, and 0.25 per letter in the insert states. Take

$$S_1 = \texttt{GGAG},\quad S_2 = \texttt{GTGAG},\quad S_3 = \texttt{GTAG}.$$

The expected accuracies are about 0.911 for $S_1, S_2$, 0.850 for $S_1, S_3$ and 0.918 for $S_2, S_3$, so the tree joins $S_2$ and $S_3$ first, which gives `GTGAG` over `GT-AG`. The question is where the second `G` of $S_1$ goes when $S_1$ is added: under the `G` of $S_2$ in column 3, or under the two `T`s in column 2.

| posterior of the second `G` of $S_1$ with | before consistency | after two passes |
|---|---|---|
| the `G` at position 3 of $S_2$ | 0.84 | 0.44 |
| the `T` at position 2 of $S_2$ | 0.07 | 0.28 |
| the `T` at position 2 of $S_3$ | 0.73 | 0.45 |

Before consistency, column 3 scores 0.84 and column 2 scores $0.07 + 0.73 = 0.80$, so the merge puts the `G` in column 3. After consistency, column 3 scores 0.44 and column 2 scores about 0.74. The evidence moved through $S_3$: the `G` of $S_1$ is likely aligned with the `T` of $S_3$, which is very likely aligned with the `T` of $S_2$. The result is

```
S1  GG-AG
S2  GTGAG
S3  GT-AG
```

Under the scores $+1$ for a match, $-1$ for a mismatch and $-2$ for a letter against a gap, this alignment has sum-of-pairs score 4, the optimum found by exact dynamic programming. Without consistency the same tree gives `G-GAG` for $S_1$ and score 3. The 100 refinement rounds do not change the alignment.

## Correctness

The output is a valid multiple alignment, each merge and each refinement step maximizes the expected accuracy between its two groups, refinement never lowers the expected accuracy, and for two sequences the output is the maximum expected accuracy alignment under the transformed posteriors.

The forward and backward algorithms compute sums over all paths of the pair-HMM, so $f_M(i, j)\, b_M(i, j)$ is the total probability of the paths that match $x_i$ with $y_j$, and dividing by $\Pr(x, y)$ gives the posterior. The merge is the global alignment recurrence on columns with gap score 0; as for [Needleman-Wunsch](/needleman-wunsch/), it returns a block alignment of the two groups with the largest total column score, and a block alignment of two valid groups is valid. In refinement, removing gap-only columns does not change the score, the current alignment of the two groups is one of the candidates, and the score within each group is fixed, so the total cannot decrease. The proof file has the details.

## Complexity

The model is the word RAM, with one unit per arithmetic operation. $L$ is the length of the final alignment, $n \le L \le kn$, and $R$ is the number of refinement rounds.

- **Lines L1 and L2.** For each of $\binom{k}{2}$ pairs, forward, backward and the MEA program fill $O(n^2)$ cells, so $O(k^2 n^2)$ time.
- **Line L3.** One pass computes, for each of the $O(k^2)$ pairs, $k$ matrix products of size $n$. With dense matrices this is $O(k^3 n^3)$ time. With sparse matrices of about $c$ nonzero entries per row, one product costs $O(c^2 n)$, which is how the paper makes the step fast.
- **Line L4.** $O(k^3)$ time with the simple method.
- **Line L5.** A merge of groups with $a$ and $b$ rows fills $O(L^2)$ cells with column scores of $O(ab)$ terms; the sum of $ab$ over all merges is $\binom{k}{2}$, so $O(k^2 L^2)$.
- **Lines L6 to L8.** Each round aligns two groups with $ab \le k^2/4$, so $O(k^2 L^2)$ per round.

The total is $O(k^2 n^2 + k^3 n^3 + R k^2 L^2)$ time, which is $O(k^3 n^3 + R k^2 L^2)$, with dense matrices. The posterior matrices take $O(k^2 n^2)$ space, and one table $O(L^2)$.

## Properties

- **Deterministic** for a fixed random seed. The refinement splits are random.
- **No gap penalties at alignment time.** The gap model lives in the pair-HMM, through the posteriors.
- **Monotone refinement.** Each round keeps or improves the expected accuracy.
- **Exact for two sequences** with respect to its expected accuracy, and a heuristic for three or more.
- **Consistency mixes in the direct estimate.** With $z = x$ or $z = y$ the sum includes $P_{xy}$ itself, so a pair that no third sequence supports keeps part of its weight.

## Variants and improvements

- **ProbCons-ext** adds a second pair of insert states to the pair-HMM, to model long or terminal insertions.
- **More consistency passes or more refinement rounds** trade time for accuracy; the paper's defaults are 2 and 100.
- **T-Coffee** uses identity-weighted pairs from global and local alignments and a min-based extension in place of posteriors and matrix products. See [T-Coffee](/t-coffee/).
- **MAFFT** L-INS-i and G-INS-i add a consistency score to a weighted sum-of-pairs objective. See [MAFFT](/mafft/).

## When to use it

Use ProbCons for up to a few hundred protein sequences when accuracy is the main goal. The posterior and consistency steps grow with the square and the cube of the number of sequences, so for thousands of sequences use [MAFFT](/mafft/), [MUSCLE](/muscle/) or [Clustal](/clustal/) Omega instead.

## Pitfalls

- **Cubic cost in $k$.** The consistency step needs every triple of sequences.
- **Model parameters.** The pair-HMM is trained for proteins; DNA or very different data need other parameters.
- **Expected accuracy is not the sum-of-pairs score with a substitution matrix.** A good ProbCons alignment can have a lower classical SP score than another aligner's output, and the reverse.
- **Random refinement.** Different seeds can give different alignments; fix the seed for reproducible results.
- **Underflow.** Forward and backward values are products of many probabilities; real implementations work with logarithms or scaling.

## Implementations

## History

Chuong Do, Mahathi Mahabhashyam, Michael Brudno and Serafim Batzoglou published ProbCons in Genome Research in 2005. Posterior probabilities from pair HMMs were known, and T-Coffee had shown in 2000 that consistency through third sequences improves progressive alignment. ProbCons joined the two ideas: it replaced T-Coffee's weights with posterior probabilities and its extension with a product of probability matrices, and used maximum expected accuracy alignment in place of the single most probable alignment. In the paper it gave higher accuracy than the leading aligners of the time on the BAliBASE, SABmark and PREFAB benchmarks.

## References
