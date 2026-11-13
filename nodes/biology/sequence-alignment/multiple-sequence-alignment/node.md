---
tag: QR2355
kind: problem
slug: multiple-sequence-alignment
name: Multiple sequence alignment
aliases:
- MSA
- multiple alignment
area: biology/sequence-alignment
level: core
summary: Align three or more sequences at once, by adding gaps so that related residues share a column, to optimize a score such as sum-of-pairs.
prereqs: [pairwise-sequence-alignment, global-alignment, scoring-matrix, gap-penalty]
see_also: [sum-of-pairs-score, msa-np-hardness, center-star-method, progressive-alignment, profile-hmm, consensus-sequence, shortest-common-supersequence, phylogenetic-tree]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14 (multiple string comparison), Sections 14.5 and 14.6 (scoring and the sum-of-pairs objective), Section 14.10 (common multiple alignment methods)
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 6, Multiple sequence alignment methods
  - paper: doi:10.1137/0148063
    title: Humberto Carrillo and David Lipman, The multiple sequence alignment problem in biology, SIAM Journal on Applied Mathematics 48(5), 1988, pages 1073 to 1082
    locator: the exact dynamic program over k dimensions and the pruning by pairwise bounds
  - paper: "David J. Lipman, Stephen F. Altschul and John D. Kececioglu, A tool for multiple sequence alignment, Proceedings of the National Academy of Sciences USA 86(12), 1989, pages 4412 to 4415"
    locator: the MSA program, an implementation of the Carrillo-Lipman method
  - paper: doi:10.1089/cmb.1994.1.337
    title: Lusheng Wang and Tao Jiang, On the complexity of multiple sequence alignment, Journal of Computational Biology 1(4), 1994, pages 337 to 348
    locator: NP-completeness of the sum-of-pairs problem
  - book: isbn:9780534952624
    title: João Setubal and João Meidanis, Introduction to Computational Molecular Biology, 1997
    locator: Chapter 3, Section 3.4, Comparing multiple sequences
---

Multiple sequence alignment (MSA) is the problem of aligning three or more sequences at once. Gaps are added to each sequence so that all rows have the same length and residues that are believed to share an origin, a structural role or a function stand in the same column. The quality of an alignment is measured by an objective, most often the [sum-of-pairs score](/sum-of-pairs-score/). For a fixed number of sequences, dynamic programming solves the problem exactly, but the time grows exponentially with the number of sequences, and the problem is [NP-hard](/msa-np-hardness/) when the number is unbounded. Most practical aligners are therefore heuristics.

## In plain words

You have several DNA or protein sequences that you believe are related, for example the same gene in ten species. You want to write them one below the other so that matching parts line up. To do this you insert gap symbols into the sequences, never change or reorder their letters, and make all rows the same length.

A good multiple alignment shows which positions stay the same in all sequences and where insertions and deletions happened. It is the input for many later steps, such as building family trees of genes or finding important sites in a protein.

The hard part is that each sequence affects where the gaps go in all the others.

## Definition

Let $\Sigma$ be an alphabet, $-$ the gap symbol, and $\Sigma' = \Sigma \cup \{-\}$. The input is $k \ge 2$ sequences $S_1, \ldots, S_k$ over $\Sigma$, of lengths $n_1, \ldots, n_k$, and a scoring scheme.

An **alignment** is a $k \times L$ matrix $A$ over $\Sigma'$ such that:

- row $A_i$, with its gaps removed, equals $S_i$;
- no column consists of gaps only.

Then $\max_i n_i \le L \le \sum_i n_i$.

The **objective** most used in theory is the sum-of-pairs score. For a symmetric pair score $s$ on $\Sigma'$ with $s(-, -) = 0$,

$$\mathrm{SP}(A) = \sum_{p=1}^{L} \sum_{1 \le i < j \le k} s\big(A_i[p], A_j[p]\big).$$

**Optimization problem.** Find an alignment that maximizes $\mathrm{SP}(A)$ for a similarity score, or minimizes it for a cost.

**Decision problem.** Given also a bound $C$, decide if some alignment has cost at most $C$.

For $k = 2$ this is [global alignment](/global-alignment/), solved by [Needleman-Wunsch](/needleman-wunsch/).

## Variants

- **Objective.** Besides sum of pairs, there are the *star* objective (the cost of all rows against one given row), the *tree* objective (sequences at the leaves of a given [phylogenetic tree](/phylogenetic-tree/), with ancestral sequences to be chosen at internal nodes, and the sum of edge costs to minimize), and the *consensus* objective (the total cost of all rows against a [consensus sequence](/consensus-sequence/)). *Weighted* SP gives each pair of rows a weight.
- **Gap model.** With a [linear gap penalty](/linear-gap-penalty/) the SP score is a sum over columns. With an [affine gap penalty](/affine-gap-penalty/), each pair of rows is charged its own gap openings after columns of two gaps are removed, and the cost of a column depends on the previous columns.
- **Probabilistic objectives.** A [profile HMM](/profile-hmm/) defines a probability for each alignment column, and aligners such as [ProbCons](/probcons/) maximize the expected number of correctly aligned residue pairs.
- **Consistency objectives.** [T-Coffee](/t-coffee/) maximizes agreement with a library of pairwise alignments.
- **Local multiple alignment.** Find conserved regions, such as motifs, in only part of each sequence.
- **Graph output.** [Partial order alignment](/partial-order-alignment/) represents the alignment as a directed acyclic graph instead of a matrix.

## Examples

Take $S_1 = \texttt{ACGT}$, $S_2 = \texttt{AGT}$, $S_3 = \texttt{ACCGT}$ with unit costs: 0 for a match, 1 for a mismatch or for a letter against a gap, and 0 for a gap against a gap.

```
S1  AC-GT
S2  A--GT
S3  ACCGT
```

Columns 2 and 3 each cost 2, the other columns cost 0, so the SP cost is 4. This is optimal: the optimal pairwise costs are $D(1,2) = 1$, $D(1,3) = 1$ and $D(2,3) = 2$, each pair of rows of any alignment costs at least its optimal pairwise cost, so no alignment costs less than $1 + 1 + 2 = 4$.

Here the optimal multiple alignment induces an optimal pairwise alignment for every pair. This is not true in general: when the pairwise optima disagree, the multiple alignment must give up some of them, and the objective decides which.

## Known algorithms

| method | type | time | guarantee |
|---|---|---|---|
| dynamic program over the $k$-dimensional lattice | exact | $O(k^2 2^k n^k)$ | optimal SP |
| Carrillo-Lipman pruning (1988), the MSA program (1989) | exact | exponential in $k$ in the worst case | optimal SP |
| [center-star method](/center-star-method/) | approximation | $O(k^2 n^2 + k^3 n)$ | $2 - 2/k$ for a metric cost |
| Bafna, Lawler and Pevzner (1997) | approximation | polynomial for fixed $l$ | $2 - l/k$ for a metric cost |
| [progressive alignment](/progressive-alignment/), e.g. [Clustal](/clustal/) | heuristic | about $O(k^2 n^2)$ | none |
| [iterative refinement](/iterative-refinement-alignment/), e.g. [MUSCLE](/muscle/), [MAFFT](/mafft/) | heuristic | progressive time plus refinement passes | the objective never gets worse |
| consistency, e.g. [T-Coffee](/t-coffee/), [ProbCons](/probcons/) | heuristic | about $O(k^3 n^2)$ | none |
| [partial order alignment](/partial-order-alignment/) | heuristic | about $O(k\, n\, E)$ for a graph with $E$ edges | none |

Here $n$ is the length of the longest sequence. The exact program fills one cell for each tuple of prefix lengths, $\prod_i (n_i + 1) \le (n+1)^k$ cells, and each cell takes the best of $2^k - 1$ predecessors, one for each nonempty set of rows that receive a letter in the last column, and the SP score of that column takes $O(k^2)$ time.

## Bounds

- **Hardness.** The SP problem is NP-hard when $k$ is part of the input ([Wang and Jiang 1994](/msa-np-hardness/)), for a fixed alphabet and a fixed cost table, and later results extend this to every metric cost.
- **Lower bound on the optimum.** Each pair of rows of an alignment is a pairwise alignment, so $\mathrm{OPT} \ge \sum_{i<j} D(i, j)$ for costs, where $D(i, j)$ is the optimal pairwise cost. Carrillo and Lipman use this bound, with an upper bound from any heuristic alignment, to limit the lattice cells that the exact program visits.
- **Size of the search space.** The number of alignments grows exponentially in both $k$ and $n$, so enumeration is useless beyond tiny cases.

## Reductions

- **From shortest common supersequence.** The [NP-hardness proof](/msa-np-hardness/) maps binary strings and a length $m$ to an alignment instance with one or two extra ruler rows; a cheap alignment exists exactly when a common [supersequence](/shortest-common-supersequence/) of length $m$ exists.
- **To shortest paths.** The exact program is a shortest path in a directed acyclic graph whose vertices are the tuples of prefix lengths. [A* search](/a-star-search/) with the sum of pairwise costs as heuristic is one way to explore only part of it.
- **Of two groups to pairwise alignment.** Aligning two alignments under SP, keeping each group fixed, is a pairwise dynamic program on columns, the basic step of progressive methods ([sequence-profile alignment](/sequence-profile-alignment/) is the case of one group of size one).

## Applications

- **Phylogenetics.** Tree-building methods such as [neighbor joining](/neighbor-joining/) and maximum likelihood take an MSA as input, one column per homologous site.
- **Protein families.** [Profile HMMs](/profile-hmm/) and [position-specific scoring matrices](/position-specific-scoring-matrix/) are built from multiple alignments, and search tools such as [HMMER](/hmmer/) use them to find new members of a family.
- **Conserved sites.** Columns with little variation point to residues that matter for structure or function, shown by a [consensus sequence](/consensus-sequence/) or a [sequence logo](/sequence-logo/).
- **Structure prediction.** Pairs of columns that change together suggest residues in contact.
- **Genome assembly and sequencing.** Aligning many reads of one region, often with [partial order alignment](/partial-order-alignment/), gives a consensus that corrects sequencing errors.

## References
