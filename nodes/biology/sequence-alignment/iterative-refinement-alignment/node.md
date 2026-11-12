---
tag: 1TKX5V
kind: technique
slug: iterative-refinement-alignment
name: Iterative refinement alignment
aliases:
- alignment refinement
- iterative multiple alignment refinement
area: biology/sequence-alignment
level: advanced
summary: Improve a multiple alignment by splitting its rows into two groups, realigning the groups, and keeping the result only if the score improves.
prereqs: [progressive-alignment, multiple-sequence-alignment, sum-of-pairs-score, sequence-profile-alignment]
see_also: [muscle, mafft, probcons, local-search, hill-climbing, clustal]
sources:
  - paper: doi:10.1093/bioinformatics/7.4.479
    title: Marc P. Berger and Peter J. Munson, A novel randomized iterative strategy for aligning multiple protein sequences, Computer Applications in the Biosciences 7(4), 1991, pages 479 to 484
    locator: random division of the sequences into two subgroups, optimal alignment of the subgroups, repeated
  - paper: doi:10.1006/jmbi.1996.0679
    title: Osamu Gotoh, Significant improvement in accuracy of multiple protein sequence alignments by iterative refinement as assessed by reference to structural alignments, Journal of Molecular Biology 264(4), 1996, pages 823 to 838
    locator: the doubly nested randomized iterative method of the PRRP program, with weights from the guide tree
  - paper: doi:10.1093/nar/gkh340
    title: Robert C. Edgar, MUSCLE, multiple sequence alignment with high accuracy and high throughput, Nucleic Acids Research 32(5), 2004, pages 1792 to 1797
    locator: stage 3, refinement by tree-dependent restricted partitioning, accepting a new alignment only if the SP score improves
  - paper: "Iain M. Wallace, Orla O'Sullivan and Desmond G. Higgins, Evaluation of iterative alignment algorithms for multiple alignment, Bioinformatics 21(8), 2005, pages 1408 to 1414"
    locator: comparison of refinement strategies applied to the output of progressive aligners
---

Iterative refinement improves a [multiple sequence alignment](/multiple-sequence-alignment/) that already exists, usually the output of [progressive alignment](/progressive-alignment/). In each step it splits the rows into two groups, removes the columns that became gaps only, aligns the two groups again with a pairwise dynamic program, and keeps the new alignment only if it scores better than the old one. Because worse alignments are never accepted, the objective never decreases, and the method stops when no split improves it or after a fixed number of steps. It is a form of [local search](/local-search/), and it repairs some of the early errors that progressive alignment freezes. Berger and Munson used random splits in 1991; [MUSCLE](/muscle/) and [MAFFT](/mafft/) split along the edges of the guide tree.

## In plain words

A progressive aligner makes its choices early and never goes back. Iterative refinement goes back.

Take the finished alignment and divide the sequences into two groups. Pull the two groups apart, remove the columns that are now empty in a group, and align the two groups again, as two blocks. If the new alignment is better by the chosen score, keep it. If not, keep the old one.

Repeat this with other ways to divide the sequences. Each kept change makes the alignment better, so the score only goes up. Stop when no division helps, or when you run out of time.

## When it applies

- There is a starting alignment and an objective that can score any alignment, such as the [sum-of-pairs score](/sum-of-pairs-score/).
- Aligning two groups of rows is fast: a dynamic program on columns, $O(L_1 L_2)$ column scores for groups of lengths $L_1$ and $L_2$.
- There is time for more passes over the data. Each step costs about as much as one merge of progressive alignment, and a full pass over a tree with $k$ leaves has $2k - 3$ edges.
- The starting alignment has local errors. Refinement cannot fix a deep error that needs many rows to move at once in different ways.

## The template

```pseudo id=main
REFINE(A, T, score, maxPasses)       ▷ A: alignment of k rows, T: guide tree on the rows
L1  for pass ← 1 to maxPasses do
L2      improved ← false
L3      for each edge e of T, in a fixed order or in random order do
L4          (X, Y) ← the rows of A on the two sides of e
L5          remove from X and from Y every column of gaps only
L6          A′ ← ALIGN-GROUPS(X, Y)
L7          if score(A′) > score(A) then
L8              A ← A′, improved ← true
L9      if not improved then return A
L10 return A
```

ALIGN-GROUPS is the group-to-group dynamic program of [progressive alignment](/progressive-alignment/): each group keeps its internal alignment, and gaps are inserted as whole columns.

**The objective never decreases.** Line L7 accepts $A'$ only when its score is higher, so $\mathrm{score}(A)$ is nondecreasing over the run, and the returned alignment is at least as good as the input. The number of alignments of the input is finite, so with a strict increase at each accepted step the loop must end even without the limit $maxPasses$. In practice the limit, or a small number of passes without improvement, ends it much sooner.

**When the test of line L7 is not needed.** If the objective is the sum-of-pairs score with a linear gap penalty and gap against gap scored 0, and ALIGN-GROUPS maximizes the sum of the scores of the pairs that cross the two groups, then the old alignment, with its columns of gaps only in each group, is one of the candidates of the dynamic program. Pairs inside a group keep their score, because removing columns of two gaps changes nothing. So $\mathrm{score}(A') \ge \mathrm{score}(A)$ automatically. The test matters when the group score differs from the objective: MUSCLE aligns groups with a log-expectation score but accepts by SP, and with affine gaps the group program uses an approximate gap count.

**Choice of splits.**

- *Random bipartitions.* Berger and Munson (1991) divide the sequences into two random groups at each step.
- *Tree-dependent restricted partitioning.* Only the $2k - 3$ splits given by the edges of the guide tree are tried. Splits between closely related sequences rarely change much, so MUSCLE visits edges in order of decreasing distance from the root, and MAFFT's FFT-NS-i cycles over the tree edges.
- *One sequence against the rest.* Each sequence in turn is removed and aligned again to the profile of the others.
- *Doubly nested iteration.* Gotoh's PRRP program (1996) has an inner loop of group realignments and an outer loop that recomputes the guide tree and the sequence weights from the current alignment.

## Classic examples

- **Berger and Munson (1991).** Random division into two subgroups, optimal alignment of the subgroups, repeated many times.
- **Gotoh, PRRP (1996).** Doubly nested randomized iterative refinement with weights from the tree. Gotoh showed that the refinement improves accuracy against alignments from protein structures.
- **[MUSCLE](/muscle/) (2004), stage 3.** Tree-dependent restricted partitioning on the second guide tree, accepting a change only if the SP score improves, until no change is accepted or a pass limit is reached.
- **[MAFFT](/mafft/) (2002), FFT-NS-i.** The progressive FFT-NS-2 alignment followed by refinement on the tree edges, following Hirosawa and others (1995).
- **[ProbCons](/probcons/) (2005).** Repeated realignment of random bipartitions under its expected accuracy objective.

## Variations

- **Accept equal scores.** Accepting $\mathrm{score}(A') \ge \mathrm{score}(A)$ lets the search move across plateaus, but then the loop needs an explicit limit, since it can cycle.
- **Simulated annealing and genetic algorithms.** Accepting some worse alignments, with a probability that falls over time, can escape local optima. This gives up the property that the objective never decreases.
- **Refine with a different objective.** The group alignment can use consistency scores, as in T-Coffee or ProbCons, or posterior probabilities.
- **Refine a column range.** Realign only a window of columns, between two well-conserved blocks, to keep the cost down for long alignments.

## Pitfalls

- **Local optimum only.** A split that would help needs one group of rows to move as a block. Errors that need moves of several groups at once stay. The final alignment depends on the starting alignment and the order of splits.
- **Objective not the same as accuracy.** A higher SP score does not always mean an alignment closer to the true one. Wallace, O'Sullivan and Higgins (2005) compared refinement strategies on reference alignments; measure accuracy on references, not only the objective.
- **Forgetting to remove empty columns.** After the split, a group can have columns with gaps only. If they stay, the group program aligns them, and they can pull new gaps to odd places or break the score comparison.
- **Comparing scores of different kinds.** The test in line L7 must use one objective for $A$ and $A'$, computed the same way. Comparing the score of the group program with the objective of the whole alignment can accept a worse alignment.
- **Random splits without a seed.** Results then change from run to run. Use a seeded generator to make runs reproducible.

## References
