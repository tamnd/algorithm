---
tag: 1QSFAS
kind: problem
slug: simultaneous-alignment-and-folding
name: Simultaneous alignment and folding of RNA
aliases:
- RNA structural alignment
area: biology/structure-prediction
level: advanced
summary: "Align several RNA sequences and fold them into one common structure at the same time, with one score for both. Exact for k sequences in O(n^(3k)) time; tools add limits to cut the cost."
prereqs: [rna-secondary-structure, global-alignment]
see_also: [sankoff-rna-algorithm, nussinov-algorithm, mccaskill-algorithm, multiple-sequence-alignment, progressive-alignment, banded-alignment, covariance-model, rna-homology-search]
sources:
  - paper: doi:10.1137/0145048
    title: David Sankoff, Simultaneous solution of the RNA folding, alignment and protosequence problems, SIAM Journal on Applied Mathematics 45(5), 1985, pages 810 to 825
    locator: the joint objective of alignment and folding, and the dynamic program with O(n^(3k)) time for k sequences
  - paper: doi:10.1093/nar/25.18.3724
    title: Jan Gorodkin, Laurie J. Heyer and Gary D. Stormo, Finding the most significant common sequence and structure motifs in a set of RNA sequences, Nucleic Acids Research 25(18), 1997, pages 3724 to 3732
    locator: Foldalign, a local and simplified form of the Sankoff algorithm for pairs of sequences, and multiple alignments built from pairwise ones by a greedy progressive method
  - paper: doi:10.1006/jmbi.2001.5351
    title: David H. Mathews and Douglas H. Turner, Dynalign, an algorithm for finding the secondary structure common to two RNA sequences, Journal of Molecular Biology 317(2), 2002, pages 191 to 203
    locator: the free energy objective for two sequences, the limit M on the distance between aligned nucleotides, and the running time of about O(M^3 N^3)
  - paper: doi:10.1371/journal.pcbi.0030065
    title: Sebastian Will, Kristin Reiche, Ivo L. Hofacker, Peter F. Stadler and Rolf Backofen, Inferring noncoding RNA families and classes by means of genome-scale structure-based clustering, PLoS Computational Biology 3(4), 2007, e65
    locator: LocARNA, a local variant of the Sankoff algorithm on base pair probabilities, its time and memory in terms of the number of significant base pairs, and its use to cluster thousands of candidate sequences
---

Simultaneous alignment and folding is the problem of finding, for a set of RNA sequences, an alignment and one common secondary structure that together get the best score. The score adds a sequence part, as in [sequence alignment](/global-alignment/), and a structure part, such as a free energy or a count of base pairs, and a base pair of the common structure must join aligned positions in every sequence. Sankoff solved it exactly in 1985 with a dynamic program that costs $O(n^{3k})$ time for $k$ sequences of length $n$, which is $O(n^6)$ already for two. So all practical tools limit the problem: they align two sequences at a time, bound how far aligned positions can shift, or keep only likely base pairs.

## In plain words

Two RNA molecules from related species often fold into the same shape, even when many of their letters differ. To compare them well, you want to line up the letters and find the shared shape.

If you line up the letters first, you may put the gaps in places that break the shape. If you fold each molecule first, each fold may be a little wrong, and the two wrong folds may not match. Doing both at the same time avoids both problems: the shape tells where the gaps should go, and the line-up tells which pairs the two molecules share.

The price is time. The exact method looks at every part of one molecule against every part of the other, and that grows very fast with length and with the number of molecules.

## Definition

**Input.** $k$ RNA sequences $x^1, \ldots, x^k$ over A, C, G and U, of length at most $n$, and a scoring scheme.

**Output.** A pair $(A, S)$ of:

- an alignment $A$ of the sequences, a matrix of $k$ rows and $c$ columns in which each row is one sequence with gaps added, and
- a consensus structure $S$, a set of pairs of columns $(p, q)$ with $p < q$. The pairs are nested: no two pairs $(p, q)$ and $(p', q')$ have $p < p' < q < q'$, so there are no [pseudoknots](/pseudoknot/). Each column is in at most one pair.

For each sequence $x^r$, the pairs of $S$ whose two columns both hold a base of $x^r$ give a structure of $x^r$ on its own.

**Objective.** Maximise $\mathrm{score}(A, S) = \mathrm{align}(A) + \mathrm{fold}(A, S)$. Typical choices are:

- $\mathrm{align}(A)$ is a [sum-of-pairs score](/sum-of-pairs-score/) with a [linear](/linear-gap-penalty/) or affine gap penalty;
- $\mathrm{fold}(A, S)$ is a sum over sequences of the structure score of each induced structure, for example minus its free energy in the [nearest-neighbor model](/nearest-neighbor-model/), a bonus for each pair as in the [Nussinov algorithm](/nussinov-algorithm/), or a sum of terms from base pair probabilities computed by the [McCaskill algorithm](/mccaskill-algorithm/).

Most schemes allow a pair in a sequence only if its two bases are Watson-Crick (A-U, C-G) or G-U and the loop it closes has at least a minimum number of unpaired bases. The weight between the two parts is a choice of the scheme, and the best $(A, S)$ depends on it.

## Variants

- **Two sequences or many.** For $k = 2$ the problem is the pairwise one that most tools solve. For $k > 2$, tools build a multiple alignment from pairwise ones by a [progressive](/progressive-alignment/) method.
- **Global or local.** A global solution aligns the whole sequences. A local solution finds the best pair of subsequences, as [local alignment](/local-alignment/) does, which finds a common structured motif inside longer sequences.
- **Energy or probabilities.** Dynalign scores the structure by free energy. Tools on base pair probabilities, such as LocARNA, first run the McCaskill algorithm on each sequence and then align the two probability matrices.
- **Structure known for one side.** When one side is a family with a known consensus structure, the problem becomes the alignment of a sequence to a [covariance model](/covariance-model/), which costs about $n^3$ instead of $n^6$.
- **With pseudoknots.** Crossing pairs make even the folding of one sequence NP-hard in common energy models ([pseudoknot hardness](/pseudoknot-np-hardness/)), so they are left out here.

## Examples

Take $x = $ `GCAAGC` and $y = $ `CGAACG`, a match score of 1, a mismatch score of $-1$, a gap cost of 1 for each gap position, and a bonus of 3 for each consensus pair whose bases pair in both sequences, with at least one unpaired column inside each pair.

**Align first, then fold.** With the bonus set to 0, the best alignment scores 0, for example

```
GC-AAGC-
-CGAA-CG
```

In it, no two columns hold pairs in both rows, so no consensus pair can be added, and the joint score stays 0.

**Align and fold at once.** The best joint solution is

```
GCAAGC
CGAACG
((..))
```

It has four mismatches ($-4$), two matches ($+2$) and two consensus pairs ($+6$): G-C with C-G and C-G with G-C. Its score is 4. The alignment has no gaps and four mismatches, which a sequence-only aligner would never choose, but it is the alignment that puts the two stems on top of each other. The [Sankoff algorithm](/sankoff-rna-algorithm/) page computes this example step by step.

## Known algorithms

| method | scope | structure score | cost |
|---|---|---|---|
| [Sankoff](/sankoff-rna-algorithm/) (1985) | $k$ sequences, exact | energy or pair score | $O(n^{3k})$ time, $O(n^{2k})$ memory; $O(n^6)$ and $O(n^4)$ for $k = 2$ |
| Foldalign (Gorodkin, Heyer and Stormo 1997) | two sequences, local; many by greedy progressive steps | sequence and structure conservation | a simplified Sankoff recursion |
| Dynalign (Mathews and Turner 2002) | two sequences, global | free energy of the common structure | about $O(M^3 N^3)$, with $N$ the length of the shorter sequence and $M$ the largest allowed distance between aligned nucleotides |
| LocARNA (Will et al. 2007) | two sequences, local; many by progressive steps | base pair probabilities | $O(n^2 (n^2 + m^2))$ time and $O(n^2 + m^2)$ memory, with $m$ the number of significant base pairs |

**Banding.** Dynalign aligns position $i$ of one sequence only with positions $k$ of the other with $|i - k| \le M$. This is the same idea as [banded alignment](/banded-alignment/) for sequences: for each index in one sequence, the matching index in the other has $O(M)$ choices instead of $n$. It is exact when the best solution stays in the band.

**Sparse pairs.** LocARNA keeps only the base pairs whose probability in the McCaskill ensemble of each sequence is above a cutoff. With a bounded number of significant pairs for each base, $m = O(n)$, and the cost becomes $O(n^4)$ time and $O(n^2)$ memory, against $O(n^6)$ and $O(n^4)$ for the full problem. The answer is exact only for the reduced set of pairs.

**Constraints.** Other limits used by tools of this kind are a largest length of a local motif, a largest loop size, and anchor columns given by the user or by a fast sequence alignment. Each removes parts of the table; none changes the worst case of the unrestricted problem.

## Bounds

- **Upper bound.** For a fixed $k$ the problem is solvable exactly in $O(n^{3k})$ time and $O(n^{2k})$ memory by the Sankoff recursion.
- **Number of sequences.** With the structure score set to 0 the problem is multiple alignment under the sum-of-pairs score, which is [NP-hard](/msa-np-hardness/) when $k$ is part of the input. So no algorithm polynomial in both $n$ and $k$ is expected.
- **Restricted versions.** The costs of the banded and sparse methods above are upper bounds for their restricted problems, not for the full one. How close their answers come to the exact optimum is measured on benchmarks, not proved.

## Reductions

- **From multiple sequence alignment.** As above, a zero structure score gives the [multiple sequence alignment](/multiple-sequence-alignment/) problem, so the problem is at least as hard.
- **From single sequence folding.** For $k = 1$ there is nothing to align, and the problem is folding one sequence, by the Nussinov or [Zuker](/zuker-algorithm/) recursion, depending on the structure score.
- **To alignment against a model.** If the structure of one side is fixed, the problem reduces to aligning a sequence to a structure, which a covariance model does, and which is the core step of [RNA structural homology search](/rna-homology-search/).

## Applications

- **Comparative structure prediction.** Folding several related sequences together gives better structures than folding one alone. Mathews and Turner report that Dynalign found 86.1% of the known base pairs of their tRNA test set, against 59.7% for free energy minimisation of single sequences.
- **Clustering of non-coding RNAs.** Will et al. used LocARNA to cluster thousands of candidate structured RNAs by structure and to find families and classes that sequence similarity does not show.
- **Seeds for family models.** A structural alignment of a few members is the input from which a covariance model of the family is built.

## References
