---
tag: RYMMF1
kind: algorithm
slug: t-coffee
name: T-Coffee
aliases:
- Tree-based Consistency Objective Function for alignment Evaluation
area: biology/sequence-alignment
level: advanced
summary: A progressive multiple aligner that scores residue pairs from a library of global and local pairwise alignments, made consistent by extension through third sequences.
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence, L: the length of the alignment}
  time: {worst: "O(k^3 n^2 + k^2 L^2)"}
  space: {extra: "O(k^2 n^2 + L^2)"}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 2000
  people: [Cédric Notredame, Desmond G. Higgins, Jaap Heringa]
  note: T-Coffee builds on the COFFEE objective function of Notredame, Holm and Higgins (1998), which scores an alignment by its agreement with a library of pairwise alignments.
prereqs: [progressive-alignment, needleman-wunsch, smith-waterman, neighbor-joining]
see_also: [multiple-sequence-alignment, sum-of-pairs-score, local-alignment, probcons, clustal, muscle, mafft, iterative-refinement-alignment]
sources:
  - paper: doi:10.1006/jmbi.2000.4042
    title: Cédric Notredame, Desmond G. Higgins and Jaap Heringa, T-Coffee, a novel method for fast and accurate multiple sequence alignment, Journal of Molecular Biology 302(1), 2000, pages 205 to 217
    locator: the primary library from ClustalW and Lalign, the percent identity weights, the combination of libraries, the library extension with its GARFIELD example, the O(N^3 L^2) worst case, and the progressive strategy with zero gap penalties
  - paper: doi:10.1093/bioinformatics/14.5.407
    title: Cédric Notredame, Liisa Holm and Desmond G. Higgins, COFFEE, an objective function for multiple sequence alignments, Bioinformatics 14(5), 1998, pages 407 to 422
    locator: the COFFEE score, the agreement of an alignment with a library of weighted pairwise alignments
  - paper: doi:10.1093/nar/gkl091
    title: Iain M. Wallace, Orla O'Sullivan, Desmond G. Higgins and Cédric Notredame, M-Coffee, combining multiple sequence alignment methods with T-Coffee, Nucleic Acids Research 34(6), 2006, pages 1692 to 1699
    locator: a library built from the outputs of several multiple aligners
---

T-Coffee is a method for [multiple sequence alignment](/multiple-sequence-alignment/) by Cédric Notredame, Desmond Higgins and Jaap Heringa, published in 2000. It is a [progressive aligner](/progressive-alignment/), but it does not score residue pairs with a substitution matrix. It first aligns every pair of sequences, globally and locally, and collects the aligned residue pairs in a *library*, each weighted by the identity of the alignment it came from. Then it *extends* the library: a residue pair gains weight for every third sequence that aligns well with both residues. Progressive alignment with these position-specific weights, and no gap penalties, avoids many of the early errors of a plain progressive aligner, because each merge already sees information from all the sequences.

## In plain words

First align each pair of sequences, in two ways: end to end, and only on the best matching piece. Each time two letters end up in the same column, write the pair down with a weight: the share of identical letters in that alignment.

Then check the pairs against the other sequences. If letter x of one sequence pairs with letter z of a third sequence, and z pairs with letter y of a second one, that is a vote for pairing x with y. Add the votes to the weight of the pair.

Finally align the sequences in the order of a guide tree, as usual, but score each column by these weights. A pair that many sequences agree on wins, even when two sequences alone would choose differently.

## The problem

The input is $k$ sequences $S_1, \ldots, S_k$, and the output is a multiple alignment: rows of equal length, row $i$ spelling $S_i$ with gaps added, and no column of gaps only. A residue is a position $(i, p)$ of a sequence. A *library* is a weight $W(x, y) \ge 0$ for pairs of residues of different sequences. The objective in the background is the COFFEE score of Notredame, Holm and Higgins (1998): the total weight of the residue pairs that an alignment places in the same column. Finding the alignment with the largest total weight is the maximum weight trace problem, which Kececioglu showed NP-complete, so T-Coffee does not solve it exactly. It aligns progressively with the extended weights.

## The algorithm

```pseudo id=main
T-COFFEE(S[1..k])
L1  W ← for each pair i < j, the residue pairs of a global and of a local alignment of S_i and S_j, each with the percent identity of its alignment as weight; the weights of a pair found twice are added
L2  for each pair x, y of residues of different sequences do W′(x, y) ← W(x, y) + Σ over residues z of the other sequences of min(W(x, z), W(z, y))
L3  D[i][j] ← 1 − (percent identity of the global alignment of S_i and S_j) / 100, for each pair i < j
L4  G ← NEIGHBOR-JOINING(D), rooted at its last join
L5  A ← PROGRESSIVE(G, S), with GROUP-ALIGN at each internal node
L6  return A, with its rows in input order

GROUP-ALIGN(X, Y)
L7  col(a, b) ← (1 / (|X| |Y|)) Σ W′(x, y) over the residues x in column a of X and y in column b of Y
L8  F[i][j] ← max(F[i−1][j−1] + col(i, j), F[i−1][j], F[i][j−1]), with F[i][0] = F[0][j] = 0
L9  return the block alignment found by the traceback of F
```

**Primary library (line L1).** The paper aligns each pair globally with ClustalW and locally with Lalign, which gives the ten best local alignments that do not intersect. Each aligned residue pair gets the percent identity of the alignment it comes from. The two libraries are pooled: a pair present in both gets the sum of the two weights, and pairs never aligned have weight 0. The library format accepts any source of pairwise alignments, including several alignments of the same pair. The implementation uses one optimal global alignment and one best local alignment per pair, with the scores $+1$, $-1$ and $-2$ for match, mismatch and gap.

**Extension (line L2).** In the paper's example, residue G of sequence A is aligned with G of sequence B with weight 88. Through sequence C the two are also linked, with weights 77 (A to C) and 100 (C to B), so the pair gains $\min(77, 100) = 77$ and gets weight 165. A pair that no intermediate sequence supports keeps only its direct weight; a pair that was never aligned directly can gain weight through third sequences.

**Progressive phase (lines L3 to L9).** As in ClustalW, the pairwise alignments give distances and neighbor joining gives the guide tree. Two groups are aligned by dynamic programming in which two columns score the average extended weight over their residue pairs. The paper sets the gap opening and gap extension penalties to zero: the weights already come from alignments made with gap penalties, and consistent segments get weights large enough to resist gaps. Gaps, once placed, stay, as in every progressive method.

## Example

Take three DNA sequences:

$$S_1 = \texttt{AGGC},\quad S_2 = \texttt{AGC},\quad S_3 = \texttt{AGCC}.$$

**Library.** The global alignment of $S_1$ and $S_2$ is `AGGC` over `A-GC` (identity 100), and their best local alignment is `AG` over `AG` (identity 100). So the second G of $S_1$ is paired with the G of $S_2$ with weight 100, and the first G of $S_1$ is also paired with it with weight 100: the two sources disagree. The pairs between $S_1$ and $S_3$, and between $S_2$ and $S_3$, all place the G of each sequence at position 2.

**Extension.** Through $S_3$, the first G of $S_1$ is paired with the G of $S_3$ (weight 175, from both sources) and that G with the G of $S_2$ (weight 200), so the pair (first G of $S_1$, G of $S_2$) gains 175 and reaches 275. The pair (second G of $S_1$, G of $S_2$) gets no support from $S_3$ and stays at 100.

**Progressive phase.** The distances are 0 for $S_1, S_2$, $1/4$ for $S_1, S_3$ and 0 for $S_2, S_3$; with three sequences every join has the same neighbor-joining criterion, and the tie goes to $S_1$ and $S_2$. Their merge now prefers the first G, and adding $S_3$ gives

```
S1  AGGC
S2  AG-C
S3  AGCC
```

with sum-of-pairs score 4 under the same $+1$, $-1$, $-2$ scores, which is the optimum. A plain progressive aligner with the same scores and the same tree takes the tie in the merge of $S_1$ and $S_2$ the other way, gets `A-GC` for $S_2$, cannot move the gap later, and ends at score 2.

## Correctness

The output is a valid multiple alignment. For two sequences it has the largest total extended weight among all their alignments.

GROUP-ALIGN is the global alignment recurrence on columns, with column score col and gap score 0. By the argument of [Needleman-Wunsch](/needleman-wunsch/), with columns in place of letters, it returns a block alignment of the two groups with the largest total of col: rows keep their symbols in order, gaps come in as whole columns, and each output column holds a column of one group, so it has a letter. By induction over the guide tree, the alignment at the root is valid for all $k$ sequences. For $k = 2$, col of two residues is their extended weight, so the merge maximizes the library score. For $k \ge 3$ no optimality holds: the maximum weight trace problem is NP-complete. The proof file has the details.

## Complexity

The model is the word RAM, with one unit per arithmetic operation and per dictionary access. $L$ is the length of the final alignment, $n \le L \le kn$.

- **Line L1.** $\binom{k}{2}$ pairs, each with two $O(n^2)$ dynamic programs, so $O(k^2 n^2)$ time. The library has $O(k^2 n)$ entries per alignment source.
- **Line L2.** Each pairwise alignment gives a residue at most one partner, so a residue has $O(1)$ library partners in each other sequence for a fixed number of alignment sources. For each of $O(k^2 n^2)$ residue pairs the sum then has $O(k)$ terms, so the step takes $O(k^3 n^2)$ time. The paper states this worst case as $O(N^3 L^2)$ for $N$ sequences of average length $L$, and reports a cost closer to $O(N^3 L)$ on its data, where most residue pairs have weight zero.
- **Lines L3 and L4.** Neighbor joining on $k$ leaves takes $O(k^3)$ time.
- **Lines L5 to L9.** A merge of groups with $a$ and $b$ rows fills an $O(L^2)$ table with column scores of $O(ab)$ terms. The sum of $ab$ over all merges is $\binom{k}{2}$, so $O(k^2 L^2)$ time in total.

The total is $O(k^3 n^2 + k^2 L^2)$ time. The extended library can have up to $O(k^2 n^2)$ entries, the main cost in space.

## Properties

- **Deterministic.** Ties in the pairwise alignments, in neighbor joining and in the traceback are broken by fixed rules.
- **Exact for two sequences** with respect to its own library score, and a heuristic for three or more.
- **No gap penalties in the progressive phase.** The pairwise alignments that build the library carry the gap model.
- **Order-dependent.** Gaps are frozen as in any progressive method, but the extended weights make the early merges agree with the other sequences.
- **Flexible input.** Any pairwise or multiple alignments, from sequence, structure or other methods, can feed the library.

## Variants and improvements

- **COFFEE (1998)** optimized the library score with the genetic algorithm SAGA. T-Coffee replaced the slow search with extension and progressive alignment.
- **M-Coffee (2006)** builds the library from the outputs of several multiple aligners and combines them into one alignment.
- **Structure and homology extensions.** Later versions add libraries from structural alignments and from profiles of database homologs.
- **[ProbCons](/probcons/)** uses the same consistency idea with posterior probabilities from a pair hidden Markov model in place of identity weights.
- **[MAFFT](/mafft/)** L-INS-i and G-INS-i add a consistency score to their objective.

## When to use it

Use T-Coffee for up to a few hundred sequences when accuracy matters more than time, and especially when other data, such as structures or the outputs of other aligners, should be combined. For thousands of sequences, the cubic cost of extension is too high; use [MAFFT](/mafft/), [MUSCLE](/muscle/) or [Clustal](/clustal/) Omega.

## Pitfalls

- **Cubic cost.** The extension step grows with $k^3$. Doubling the number of sequences multiplies its time by about eight.
- **Identity weights are rough.** The paper uses percent identity because it is a reasonable indicator of accuracy for sequences with more than 30 percent identity. For more distant sequences the weights say less about which pairs are correct.
- **Frozen gaps remain.** Consistency reduces early errors but does not remove them.
- **No gap penalty does not mean no gaps cost.** With zero gap penalties, an alignment can spread residues with no library support over many columns; the result can be longer than with a gap-penalized method.

## Implementations

## History

Cédric Notredame, Liisa Holm and Desmond Higgins proposed the COFFEE objective function in 1998: score a multiple alignment by its agreement with a library of weighted pairwise alignments. Notredame, Higgins and Jaap Heringa published T-Coffee in the Journal of Molecular Biology in 2000, replacing the genetic algorithm with library extension and progressive alignment, and tested it on the 141 alignments of BAliBASE. The consistency idea was then used in ProbCons, MAFFT and many later aligners.

## References
