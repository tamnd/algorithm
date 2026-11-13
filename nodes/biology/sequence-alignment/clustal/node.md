---
tag: CZRQ68
kind: algorithm
slug: clustal
name: Clustal
aliases:
- ClustalW
- ClustalΩ
- Clustal Omega
area: biology/sequence-alignment
level: core
summary: A family of progressive multiple aligners. ClustalW aligns weighted profiles along a neighbor-joining guide tree; Clustal Omega aligns profile HMMs.
model: word-ram
complexity:
  vars: {k: the number of sequences, n: the length of the longest sequence, L: the length of the alignment}
  time: {worst: "O(k^2 n^2 + k^3 + k^2 L^2)"}
  space: {extra: "O(k^2 + n^2 + k L + L^2)"}
properties: {deterministic: true, recursive: true, online: false}
history:
  year: 1994
  people: [Julie D. Thompson, Desmond G. Higgins, Toby J. Gibson]
  note: The first CLUSTAL program is from Higgins and Sharp in 1988. ClustalW (1994) added sequence weights and position-specific gap penalties, and Clustal Omega (2011) uses profile HMMs and fast guide trees.
prereqs: [progressive-alignment, needleman-wunsch, neighbor-joining, sequence-profile-alignment]
see_also: [multiple-sequence-alignment, sum-of-pairs-score, midpoint-rooting, upgma, muscle, mafft, t-coffee, profile-hmm]
sources:
  - paper: doi:10.1093/nar/22.22.4673
    title: Julie D. Thompson, Desmond G. Higgins and Toby J. Gibson, CLUSTAL W, improving the sensitivity of progressive multiple sequence alignment through sequence weighting, position-specific gap penalties and weight matrix choice, Nucleic Acids Research 22(22), 1994, pages 4673 to 4680
    locator: the progressive method, the sequence weights, the choice of substitution matrix by divergence, and the gap penalty rules
  - paper: doi:10.1038/msb.2011.75
    title: Fabian Sievers and others, Fast, scalable generation of high-quality protein multiple sequence alignments using Clustal Omega, Molecular Systems Biology 7, 2011, article 539
    locator: mBed guide trees in O(N log N) time and profile HMM alignment with HHalign
  - paper: doi:10.1016/0378-1119(88)90330-7
    title: Desmond G. Higgins and Paul M. Sharp, CLUSTAL, a package for performing multiple sequence alignment on a microcomputer, Gene 73(1), 1988, pages 237 to 244
    locator: the first Clustal program
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 6, Section 6.4 (progressive alignment methods, including ClustalW)
---

Clustal is a family of programs for [multiple sequence alignment](/multiple-sequence-alignment/) by [progressive alignment](/progressive-alignment/). The best known version, ClustalW, from Thompson, Higgins and Gibson in 1994, computes a distance for every pair of sequences, builds a [neighbor-joining](/neighbor-joining/) guide tree, roots it at its midpoint, gives each sequence a weight from the branch lengths, and then aligns weighted groups of sequences, called profiles, from the leaves of the tree to the root. Clustal Omega, from 2011, keeps the progressive scheme but builds the guide tree from embedded distances and aligns profile hidden Markov models. Like every progressive method, Clustal is a heuristic: it is fast and usually good, but it does not optimize a global objective.

## In plain words

Clustal first measures how alike each pair of sequences is, by aligning the pair and counting identical letters. From these numbers it draws a tree in which similar sequences sit on nearby branches.

Then it aligns along the tree, closest sequences first. Two aligned groups are joined as two blocks. Gaps go in as whole columns, so a group that is already aligned stays aligned.

Two details make it better than a plain progressive aligner. Sequences on long, lonely branches get more weight, so ten copies of nearly the same sequence do not outvote one different sequence. And gap penalties change with the place: a gap is cheaper where other sequences already have gaps.

## The problem

The input is $k$ sequences over an alphabet $\Sigma$, of lengths at most $n$, a pair score $s$ on $\Sigma \cup \{-\}$ (a substitution score, a gap score, and $s(-, -) = 0$), and the output is a multiple alignment: rows of equal length, row $i$ spelling the $i$-th sequence with gaps added, and no column of gaps only. Clustal does not promise the best value of any objective. Each merge is optimal for its own two profiles under a weighted average of pair scores, which is a weighted [sum-of-pairs score](/sum-of-pairs-score/) of the pairs that cross the two groups.

This page describes the ClustalW pipeline with a linear gap penalty. The position-specific gap rules of ClustalW are described in the text and left out of the pseudocode.

## The algorithm

```pseudo id=main
CLUSTAL(S[1..k], s)
L1  for each pair i < j do
        (A, B) ← an optimal global alignment of S_i and S_j
        D[i][j] ← 1 − (number of identical letter pairs in (A, B)) / (number of letter pairs in (A, B))
L2  U ← NEIGHBOR-JOINING(D), an unrooted tree with branch lengths
L3  T ← U rooted at the midpoint of its longest leaf-to-leaf path
L4  for each leaf x: w[x] ← Σ over edges e on the path from x to the root of len(e) / (number of leaves below e)
L5  for each leaf v of T do P[v] ← the alignment with one row, the sequence of v
L6  for each internal node v of T in postorder, with children u and u′ do
L7      P[v] ← PROFILE-ALIGN(P[u], P[u′], w)
L8  return P[root of T], with its rows in input order
```

PROFILE-ALIGN is the global alignment recurrence on columns. A column $x$ of the first profile and a column $y$ of the second score

$$\mathrm{col}(x, y) = \frac{\sum_{a \in x} \sum_{b \in y} w_a\, w_b\, s(a, b)}{\big(\sum_{a \in x} w_a\big)\big(\sum_{b \in y} w_b\big)},$$

the weighted average of the pair scores between the two groups, where a gap of the column scores $s(-, b)$ against a letter $b$. A column of either profile can also face a column of gaps that is inserted into the other profile. The traceback inserts these gap columns, so each profile moves as a block.

Line L1 gives distances: ClustalW uses either full dynamic programming, as here, or a fast approximate method based on short exact matches. Line L2 builds the tree with the [neighbor-joining](/neighbor-joining/) method of Saitou and Nei. Line L3 is [midpoint rooting](/midpoint-rooting/). Line L4 shares the length of each edge equally among the sequences below it, so sequences on long branches of their own get large weights and near-identical sequences share small ones.

**ClustalW refinements left out of the pseudocode.** The abstract of the 1994 paper lists them: the substitution matrix is chosen at each merge according to the divergence of the sequences being aligned; gap opening penalties depend on the residue type; gap penalties are lowered in runs of hydrophilic residues, which are likely to be loops; and positions where earlier merges opened gaps get lower gap opening penalties, so new gaps join old ones. ClustalW also delays very divergent sequences, which are added only after the others are aligned.

**Clustal Omega.** Line L1 and line L2 cost $O(k^2)$ pairwise comparisons, too many for very large $k$. Clustal Omega embeds each sequence as a vector of distances to a small set of seed sequences (the mBed method) and clusters the vectors, which builds the guide tree in $O(k \log k)$ time. Line L7 aligns profile hidden Markov models with HHalign instead of weighted profiles.

## Example

Take $k = 4$ DNA sequences and the score $+1$ for a match, $-1$ for a mismatch, and $-2$ for a letter against a gap:

$$S_1 = \texttt{ACGTTGCA},\quad S_2 = \texttt{ACGTGCA},\quad S_3 = \texttt{AGGTTGCA},\quad S_4 = \texttt{ACTTGA}.$$

Line L1 gives these optimal pairwise alignments and distances:

| pair | alignment | identity distance |
|---|---|---|
| $S_1, S_2$ | `ACGTTGCA` / `ACG-TGCA` | 0 |
| $S_1, S_3$ | `ACGTTGCA` / `AGGTTGCA` | 1/8 |
| $S_1, S_4$ | `ACGTTGCA` / `AC-TTG-A` | 0 |
| $S_2, S_3$ | `ACG-TGCA` / `AGGTTGCA` | 1/7 |
| $S_2, S_4$ | `ACGTGCA` / `ACTTG-A` | 1/6 |
| $S_3, S_4$ | `AGGTTGCA` / `A-CTTG-A` | 1/6 |

Gaps do not count in the identity, so $S_1$ and $S_4$ have distance 0 although $S_4$ is two letters shorter. Neighbor joining joins $S_1$ with $S_4$, with a negative branch length $-5/96$ for $S_1$ that is set to 0, then that pair with $S_2$, and midpoint rooting puts $S_3$ alone on one side of the root. The weights of line L4 are about 0.023 for $S_1$, 0.041 for $S_2$, 0.099 for $S_3$ and 0.075 for $S_4$.

The merges, in postorder:

| step | profiles | result |
|---|---|---|
| 1 | $S_1$ with $S_4$ | `ACGTTGCA`, `AC-TTG-A` |
| 2 | $S_2$ with the profile of step 1 | `AC-GTGCA`, `ACGTTGCA`, `AC-TTG-A` |
| 3 | $S_3$ with the profile of step 2 | `AGGTTGCA`, `AC-GTGCA`, `ACGTTGCA`, `AC-TTG-A` |

In step 2, $S_2$ has one letter fewer than $S_1$, and its gap can go in column 3 or in column 4. Column 3 lines the gap up with the gap of $S_4$, and $S_4$ has a larger weight than $S_1$, so the profile score prefers column 3. In step 3 that choice is frozen. The final alignment, in input order,

```
S1  ACGTTGCA
S2  AC-GTGCA
S3  AGGTTGCA
S4  AC-TTG-A
```

has sum-of-pairs score 14. The alignment with the gap of $S_2$ in column 4 (`ACG-TGCA`) scores 15, which is optimal: the `G` of $S_2$ then matches the `G` of $S_3$. This is the typical error of progressive alignment: a tie, or a near tie, decided before all sequences are present.

## Correctness

The output is a valid multiple alignment of the input, and with $k = 2$ it is an optimal global alignment of the two sequences.

The proof is by induction over the postorder of line L6. A leaf profile is the one-row alignment of its sequence. If $P[u]$ and $P[u']$ are valid alignments of the sequences below $u$ and $u'$, PROFILE-ALIGN returns rows that are the rows of $P[u]$ and $P[u']$ with whole gap columns inserted, and each column of the result holds a column of $P[u]$ or of $P[u']$, which has a letter. So $P[v]$ is valid for the sequences below $v$. For each merge, the dynamic program returns an alignment of the two profiles with the largest total of $\mathrm{col}$, by the same argument as for [Needleman-Wunsch](/needleman-wunsch/) with columns as symbols. With two single sequences, $\mathrm{col}(x, y) = s(x, y)$, so the result is an optimal pairwise alignment. The proof file has the details.

No statement of global optimality is possible: the example above shows a suboptimal sum-of-pairs score, and the problem is [NP-hard](/msa-np-hardness/).

## Complexity

The model is the word RAM, with one unit per evaluation of $s$ and per arithmetic operation. $L$ is the length of the final alignment, $n \le L \le kn$.

- **Line L1.** $\binom{k}{2}$ pairwise alignments, $O(k^2 n^2)$ time and $O(n^2)$ space for one table.
- **Line L2.** Neighbor joining on $k$ leaves takes $O(k^3)$ time and $O(k^2)$ space.
- **Lines L3 and L4.** $O(k^2)$ time on a tree with $2k - 2$ nodes.
- **Lines L6 and L7.** A merge of profiles with $a$ and $b$ rows fills a table of at most $(L + 1)^2$ cells, and a column score sums $ab$ pairs, so it takes $O(ab\, L^2)$ time. Each pair of sequences is split across one merge only, at their lowest common ancestor, so the sum of $ab$ over all merges is $\binom{k}{2}$. All merges take $O(k^2 L^2)$ time.

The total is $O(k^2 n^2 + k^3 + k^2 L^2)$ time. With residue counts per column, a column score takes $O(|\Sigma|^2)$ time, and the merges take $O(k\, |\Sigma|^2 L^2)$. The space is $O(k^2)$ for the distances, $O(L^2)$ for a table and $O(kL)$ for the profiles.

## Properties

- **Deterministic.** Ties in neighbor joining, rooting and traceback are broken by fixed rules.
- **Exact for two sequences**, and not exact for three or more.
- **Order-dependent.** The guide tree decides which gaps are frozen first. Different trees give different alignments.
- **Weights.** A sequence alone on a long branch gets a large weight; a sequence inside a tight cluster shares its branches and gets a small one. Identical sequences on branches of length 0 get weight 0 from line L4 and contribute only through their group.
- **Linear gap model here.** With ClustalW's affine and position-specific gaps, the merge program needs three states, as in the [Gotoh](/gotoh-algorithm/) recurrence.

## Variants and improvements

- **CLUSTAL (1988) to Clustal V.** The first versions by Higgins and Sharp ran on microcomputers.
- **ClustalW (1994)** added the weights, the matrix choice by divergence, and the position-specific gap rules. ClustalX gave it a graphical interface.
- **Clustal Omega (2011)** uses mBed guide trees and HHalign profile HMM alignment.
- **Other progressive aligners** replace parts of the pipeline: [MUSCLE](/muscle/) uses k-mer distances, UPGMA and refinement; [MAFFT](/mafft/) uses FFT-based segment matching; [T-Coffee](/t-coffee/) replaces the substitution matrix with a consistency library.

## When to use it

Use ClustalW-style alignment for a few hundred related sequences when a standard, well-understood method is wanted. Use Clustal Omega for large protein families. For the highest accuracy on hard, divergent sets, consistency-based tools such as [T-Coffee](/t-coffee/) or [ProbCons](/probcons/), or iterative tools such as [MAFFT](/mafft/) in its iterative modes, usually do better at a higher cost.

## Pitfalls

- **Reading the guide tree as a phylogeny.** The tree comes from crude distances and only orders the merges.
- **Identity distances ignore gaps.** Two sequences that differ only by a long insertion get distance 0, as $S_1$ and $S_4$ do in the example.
- **Frozen gaps.** Errors of early merges stay, as in the example. Inspect or refine the result for important work.
- **Zero weights.** Identical sequences can get weight 0. If a whole profile has weight 0, the weighted average divides by zero; an implementation must fall back to equal weights.
- **Similarity versus cost.** The pseudocode maximizes a similarity score. With a cost, change max to min and negate the comparisons.

## Implementations

## History

Desmond Higgins and Paul Sharp published CLUSTAL in Gene in 1988, a progressive aligner that ran on personal computers. Julie Thompson, Desmond Higgins and Toby Gibson published ClustalW in Nucleic Acids Research in 1994, with sequence weights, a choice of substitution matrix by divergence, and position-specific gap penalties. It became one of the most used tools in bioinformatics. Fabian Sievers and others published Clustal Omega in Molecular Systems Biology in 2011, to align much larger sets of protein sequences.

## References
