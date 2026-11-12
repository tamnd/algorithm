---
tag: A56BPK
kind: technique
slug: progressive-alignment
name: Progressive alignment
aliases:
- Feng-Doolittle progressive alignment
- guide-tree alignment
area: biology/sequence-alignment
level: core
summary: Build a guide tree from pairwise distances, then align sequences and groups of sequences in tree order, keeping every gap once it is placed.
prereqs: [multiple-sequence-alignment, needleman-wunsch, sequence-profile-alignment]
see_also: [upgma, neighbor-joining, clustal, muscle, mafft, t-coffee, iterative-refinement-alignment, center-star-method]
sources:
  - paper: doi:10.1007/BF02603120
    title: Da-Fei Feng and Russell F. Doolittle, Progressive sequence alignment as a prerequisite to correct phylogenetic trees, Journal of Molecular Evolution 25(4), 1987, pages 351 to 360
    locator: the progressive method, the guide tree from pairwise scores, and the rule that a gap once placed is kept
  - book: isbn:9780521629713
    title: Richard Durbin, Sean Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, 1998
    locator: Chapter 6, Section 6.4, Progressive alignment methods (Feng-Doolittle and profile alignment)
  - paper: doi:10.1093/nar/22.22.4673
    title: Julie D. Thompson, Desmond G. Higgins and Toby J. Gibson, CLUSTAL W, Nucleic Acids Research 22(22), 1994, pages 4673 to 4680
    locator: progressive profile alignment along a neighbor-joining guide tree, with sequence weights
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, 1997
    locator: Chapter 14, Section 14.10 (common multiple alignment methods)
---

Progressive alignment builds a [multiple sequence alignment](/multiple-sequence-alignment/) from a series of pairwise alignments. It first computes a distance for every pair of sequences, then builds a *guide tree* from these distances, and then walks the tree from the leaves to the root: at each internal node it aligns the two alignments of its children with a pairwise dynamic program and keeps the result. Gaps placed at one step are never removed later, which Feng and Doolittle (1987) called "once a gap, always a gap". The method is fast and is the core of [Clustal](/clustal/), [MUSCLE](/muscle/), [MAFFT](/mafft/) and [T-Coffee](/t-coffee/), but it has no guarantee: an error made early stays in the final alignment.

## In plain words

Aligning many sequences at once is too slow. Aligning two at a time is fast. Progressive alignment does many two-at-a-time steps in a good order.

First, measure how similar each pair of sequences is. Then build a tree that joins the most similar sequences first, like a family tree.

Now follow the tree. Align the two closest sequences. Then add the next sequence, or join two small groups that were aligned before, and align them as two blocks. A group is treated as one long sequence with a column of letters in each position. When a gap is needed in a group, the whole group gets a gap column.

The closest sequences are aligned first, because their alignment is the most reliable. Gaps found then stay in place.

## When it applies

- The sequences are related along their whole length, so a global alignment makes sense.
- The number of sequences $k$ is too large for exact methods, which take time exponential in $k$.
- A distance between two sequences can be computed fast, from a pairwise alignment or from shared short words.
- The sequences fall into groups of closely related members, which a tree describes well. When all sequences are equally distant, the guide tree carries little information and the order of merges is close to arbitrary.

## The template

```pseudo id=main
PROGRESSIVE(S[1..k])
L1  for each pair i < j do D[i][j] ← distance of S_i and S_j
L2  T ← a rooted binary guide tree built from D
L3  for each leaf v of T do P[v] ← the alignment with one row, the sequence of v
L4  for each internal node v of T in postorder, with children u and w do
L5      P[v] ← ALIGN-GROUPS(P[u], P[w])
L6  return P[root of T]

ALIGN-GROUPS(X, Y)            ▷ X has rows of length m, Y rows of length n
L7  fill a table F[0..m][0..n] with the global alignment recurrence on columns:
        F[i][j] = max of F[i-1][j-1] + col(X[i], Y[j]),
                         F[i-1][j] + gapcol(X[i]), F[i][j-1] + gapcol(Y[j])
L8  trace back from F[m][n]; a step on X alone adds a column of gaps to all rows of Y,
        a step on Y alone adds a column of gaps to all rows of X
L9  return the rows of X and Y with these gap columns, kept in column order
```

Line L1 is the costly part for long sequences: $\binom{k}{2}$ pairwise alignments of length $n$ take $O(k^2 n^2)$ time. Fast tools replace it with counts of shared [k-mers](/kmer-index/). Line L2 uses a clustering method such as [UPGMA](/upgma/), which gives a rooted tree directly, or [neighbor joining](/neighbor-joining/), whose unrooted tree is rooted, for example at its [midpoint](/midpoint-rooting/).

Line L7 is the [sequence-profile](/sequence-profile-alignment/) recurrence, generalized to two groups. The usual column score is the average of the pair scores between the two groups:

$$\mathrm{col}(x, y) = \frac{1}{|X|\,|Y|} \sum_{a \in x} \sum_{b \in y} s(a, b),$$

where $x$ and $y$ are columns of $X$ and $Y$, and $s$ scores a gap against a letter and gives 0 to a gap against a gap. This is the [sum-of-pairs score](/sum-of-pairs-score/) of the pairs that cross the two groups, divided by the number of such pairs. The pairs inside $X$ and inside $Y$ do not change, because the alignment of each group is fixed. Weights per sequence turn the average into a weighted average.

Line L8 is where "once a gap, always a gap" comes from: the rows of each group move only as a block, so the gaps already in a group stay, and new gaps are added only as whole columns.

**Cost.** Line L5 runs $k - 1$ times. Each run takes time proportional to the product of the two alignment lengths times the cost of one column score, which is $O(k)$ with residue counts per column. With alignments of length $O(n)$, the merges take $O(k^2 n^2)$ in the worst case, and the whole method $O(k^2 n^2)$ plus the cost of the tree.

**The Feng-Doolittle method.** The original method differs from the profile template in its scores. It converts each pairwise alignment score into a distance, normalized against the scores of shuffled sequences, and builds the tree with the [Fitch-Margoliash](/fitch-margoliash/) method. To add a sequence to a group, or to join two groups, it uses the best-scoring pairwise alignment between one sequence of each side, and it inserts gaps in the whole group according to that alignment. Gaps in a finished group are then replaced by a neutral symbol that scores 0 against everything, so that later steps prefer to put new gaps where gaps already are.

## Classic examples

- **Feng and Doolittle (1987)** introduced the method for building phylogenetic trees from protein families.
- **[Clustal](/clustal/)** (ClustalW, 1994) uses a [neighbor-joining](/neighbor-joining/) guide tree, weights each sequence by its branch lengths, and changes the substitution matrix and the gap penalties with the distance between groups and the residues near a gap. Clustal Omega aligns profile HMMs along the tree.
- **[MUSCLE](/muscle/)** (2004) builds a first tree from k-mer distances with [UPGMA](/upgma/), aligns progressively with a log-expectation column score, rebuilds the tree from the first alignment, and then refines.
- **[MAFFT](/mafft/)** (2002) uses a tree from shared 6-tuples and speeds up each group alignment with the [fast Fourier transform](/fast-fourier-transform/) to find matching segments.
- **[T-Coffee](/t-coffee/)** (2000) uses the same progressive scheme, but its column score comes from a library of pairwise alignments, extended through third sequences.
- **[ProbCons](/probcons/)** (2005) aligns groups progressively with posterior probabilities of residue pairs from a pair-HMM.

## Variations

- **Profile against sequence only.** Some methods add one sequence at a time to a single growing group, along a ladder-shaped tree. The [center-star method](/center-star-method/) is the case where every sequence is added through its pairwise alignment with one center sequence, and it has a proved error bound.
- **Two passes.** A first guide tree from a crude distance gives a first alignment; distances measured on that alignment give a better tree and a second progressive pass. MUSCLE and the FFT-NS-2 strategy of MAFFT do this.
- **Refinement after the progressive pass.** [Iterative refinement](/iterative-refinement-alignment/) cuts the tree at an edge, realigns the two groups, and keeps the change if the score improves. This repairs some early errors.
- **Consistency.** T-Coffee and ProbCons change the scores, not the order: the score of a residue pair already includes evidence from all other sequences, so early merges make fewer errors.
- **Graph groups.** [Partial order alignment](/partial-order-alignment/) keeps each group as a directed acyclic graph and aligns a new sequence to the graph.

## Pitfalls

- **Frozen errors.** A misplaced gap in an early merge cannot be moved later, even when the rest of the sequences show that it is wrong. Refinement or consistency scores reduce this, but do not remove it.
- **The guide tree is not a phylogeny.** The tree only decides the order of merges. It is built from crude distances and is often wrong as a species tree. Do not report it as a phylogeny without a proper tree method on the final alignment.
- **No objective is optimized.** Each merge is optimal for its own two groups, but the result is not optimal for the sum-of-pairs score or any other global objective, and nothing bounds the error.
- **Gap placement in groups.** With a column score that charges gaps against gaps, or with affine gaps computed per group, new gaps are drawn away from existing gap columns, so gaps scatter. Tools lower the gap penalty where a group already has gaps for this reason.
- **Overrepresented subfamilies.** With an unweighted average, a large group of near-identical sequences decides the column scores. Use sequence weights.
- **Order of children.** The result can depend on how ties in the tree and in the traceback are broken. Fix the rules if results must be reproducible.

## References
