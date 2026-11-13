---
tag: 7PW24F
kind: concept
slug: sum-of-pairs-score
name: Sum-of-pairs score
aliases:
- SP score
- SP cost
area: biology/sequence-alignment
level: core
summary: The score of a multiple alignment as the sum, over all pairs of rows, of the pairwise scores of each column, with gap against gap scored 0.
prereqs: [alignment-score, pairwise-sequence-alignment, scoring-matrix]
see_also: [multiple-sequence-alignment, center-star-method, center-star-approximation-bound, msa-np-hardness, progressive-alignment, muscle, t-coffee, affine-gap-penalty]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14, Section 14.5.1 (how to score multiple alignments) and Section 14.6 (the sum-of-pairs objective)
  - book: isbn:9780534952624
    title: João Setubal and João Meidanis, Introduction to Computational Molecular Biology, 1997
    locator: Chapter 3, Section 3.4.1, The SP measure
  - paper: doi:10.1137/0148063
    title: Humberto Carrillo and David Lipman, The multiple sequence alignment problem in biology, SIAM Journal on Applied Mathematics 48(5), 1988, pages 1073 to 1082
    locator: the sum-of-pairs objective and the bound that each pair of rows costs at least its optimal pairwise alignment
  - paper: "Stephen F. Altschul, Gap costs for multiple sequence alignment, Journal of Theoretical Biology 138(3), 1989, pages 297 to 309"
    locator: gap costs of a multiple alignment defined through its pairwise projections
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 6 (scoring a multiple alignment, and the weak points of the sum-of-pairs score)
---

The sum-of-pairs score, or SP score, gives one number to a [multiple sequence alignment](/multiple-sequence-alignment/). For each column it adds the pairwise scores of all pairs of symbols in the column, from a [scoring matrix](/scoring-matrix/) and a gap score, and it adds these column scores over the alignment. A column where both rows of a pair have a gap adds 0. With this rule, the SP score is also the sum of the scores of the $\binom{k}{2}$ pairwise alignments that the multiple alignment induces. It is the most common objective for exact and approximate multiple alignment, and minimizing it is [NP-hard](/msa-np-hardness/).

## In plain words

A multiple alignment puts many sequences in rows, one above the other, with gaps added so that related letters are in the same column.

To score it, look at each pair of rows on its own. Give the pair the score it would get as a normal two-sequence alignment: points for matching letters, a penalty for mismatches and for a letter against a gap. A place where both rows of the pair have a gap is not part of their pairwise alignment, so it counts nothing.

Then add up the scores of all pairs of rows. For three sequences there are three pairs; for ten sequences there are 45.

## The idea

Let $A$ be an alignment of $k$ sequences $S_1, \ldots, S_k$ over an alphabet $\Sigma$. It has rows $A_1, \ldots, A_k$ of equal length $L$ over $\Sigma' = \Sigma \cup \{-\}$, row $A_i$ spells $S_i$ when its gaps are removed, and no column has gaps only. Let $s : \Sigma' \times \Sigma' \to \mathbb{R}$ be a symmetric pair score with $s(-, -) = 0$. The SP score is

$$\mathrm{SP}(A) = \sum_{p=1}^{L} \sum_{1 \le i < j \le k} s\big(A_i[p], A_j[p]\big).$$

**Costs or scores.** With a cost $\delta$ (0 for a match, positive for a change, as in [edit distance](/edit-distance/)), the goal is to minimize $\mathrm{SP}$. With a similarity score such as a [BLOSUM](/blosum-matrix/) or [PAM](/pam-matrix/) entry and a negative gap score, the goal is to maximize it. The approximation results, such as the [center-star bound](/center-star-approximation-bound/), need costs that form a metric.

**Why gap against gap scores 0.** The *projection* $\pi_{i,j}(A)$ is the pair of rows $A_i, A_j$ with every column removed in which both have a gap. It is a pairwise alignment of $S_i$ and $S_j$. Because $s(-, -) = 0$,

$$\mathrm{SP}(A) = \sum_{i < j} \mathrm{score}\big(\pi_{i,j}(A)\big).$$

So each pair of rows is scored exactly as an ordinary [pairwise alignment](/pairwise-sequence-alignment/), and the columns that another sequence adds do not change it. Two consequences follow. First, each term is at most (for scores) or at least (for costs) the optimal pairwise value, which gives the bound used by exact methods: the optimal SP cost is at least $\sum_{i<j} D(i, j)$, where $D$ is the optimal pairwise cost. Second, a nonzero $s(-, -)$ would make the score depend on gap columns that have nothing to do with the pair.

**Column additivity.** With a linear gap score, $\mathrm{SP}$ is a sum over columns, so a dynamic program over the $k$-dimensional lattice of prefixes finds the optimum in $O(k^2 2^k n^k)$ time for $k$ sequences of length $n$ (each cell has $2^k - 1$ predecessors, and the score of a column sums $O(k^2)$ pairs). With an [affine gap penalty](/affine-gap-penalty/), the natural definition charges each projection its own gap openings, as Altschul (1989) proposed. Then the cost of a column depends on earlier columns, and exact programs use approximate gap counts.

**Weighted SP.** A weight $w_{ij} \ge 0$ per pair gives $\sum_{i<j} w_{ij}\, \mathrm{score}(\pi_{i,j}(A))$. Aligners such as [Clustal](/clustal/) use weights to lower the influence of groups of near-identical sequences.

## Examples

**A three-row alignment.** Take unit costs: $\delta(x, x) = 0$ and $\delta(x, y) = 1$ for $x \ne y$, with a gap against a letter costing 1 and $\delta(-, -) = 0$.

```
S1  AC-GT
S2  A--GT
S3  ACCGT
```

| column | symbols | pairs (1,2), (1,3), (2,3) | cost |
|---|---|---|---|
| 1 | A, A, A | 0, 0, 0 | 0 |
| 2 | C, -, C | 1, 0, 1 | 2 |
| 3 | -, -, C | 0, 1, 1 | 2 |
| 4 | G, G, G | 0, 0, 0 | 0 |
| 5 | T, T, T | 0, 0, 0 | 0 |

The SP cost is 4. Per pair: the projection of rows 1 and 2 drops column 3 and leaves `ACGT` over `A-GT`, cost 1; rows 1 and 3 cost 1; rows 2 and 3 cost 2. The sum is again 4. If gap against gap cost 1, column 3 would cost 3 and the total 5, although no pair of sequences has changed.

**Counting one event many times.** Take $k$ copies of the same sequence, and change one letter in one copy. In the best alignment, the changed column costs $k - 1$ under unit costs, because the changed letter is compared with each of the other $k - 1$ rows. A single substitution in a tree of $k$ sequences is counted $k - 1$ times, while the same substitution shared by half of the rows is counted about $k^2/4$ times. Durbin et al. use this kind of example to show that the SP score has no clear probabilistic basis: it compares every sequence with every other one, as if each had evolved from all the others, and not from a common ancestor in a tree.

## Where it is used

- **Exact alignment.** The $k$-dimensional dynamic program and the Carrillo-Lipman pruning, implemented in the MSA program of Lipman, Altschul and Kececioglu (1989), optimize the SP score.
- **Approximation.** The [center-star method](/center-star-method/) has a [proved ratio](/center-star-approximation-bound/) of $2 - 2/k$ for SP costs that form a metric.
- **Hardness.** [Wang and Jiang](/msa-np-hardness/) proved in 1994 that minimizing the SP cost is NP-hard.
- **Heuristic aligners.** [Progressive alignment](/progressive-alignment/) aligns profiles with column scores that are averages of pair scores, which is the SP score between two groups. The refinement stage of [MUSCLE](/muscle/) accepts a new alignment only if its SP score improves. The objective of [T-Coffee](/t-coffee/) is a weighted sum over pairs of residues, with weights from a library instead of a matrix.
- **A different meaning in benchmarks.** Benchmark suites such as BAliBASE also report an "SP score": the fraction of residue pairs of a reference alignment that a test alignment reproduces. It is a measure of accuracy against a reference, not the objective defined on this page.

## References
