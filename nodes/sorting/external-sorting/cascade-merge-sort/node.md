---
tag: KG5YAF
kind: algorithm
slug: cascade-merge-sort
name: Cascade merge sort
aliases:
- cascade merge
area: sorting/external-sorting
level: advanced
summary: A tape-based merge scheme in which each merge phase cascades runs into the next tape, reducing rewinds.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {N: the number of items, S: the number of initial runs, T: the number of tapes}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [polyphase-merge-sort, k-way-merge, sorted-run]
see_also: [balanced-merge-sort, oscillating-sort, external-merge-sort, replacement-selection]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.3, The Cascade Merge (the cascade distributions, and the comparison with the polyphase merge)
  - book: isbn:9780201416077
    title: Gaston H. Gonnet and Ricardo Baeza-Yates, Handbook of Algorithms and Data Structures, second edition
    locator: Section 4.4, External sorting (cascade merge sort)
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (merge passes, and why disks remove the need for tape distributions)
---

Cascade merge sort is a tape sort in which one pass is a *cascade* of merges of decreasing order: a merge of $T - 1$ tapes onto the empty tape, until the shortest input tape is empty; then a merge of the remaining $T - 2$ tapes onto that tape, until the next one is empty; and so on, down to a merge of two tapes. Like the [polyphase merge sort](/polyphase-merge-sort/), it needs an uneven *perfect distribution* of the initial [sorted runs](/sorted-run/), but each pass moves almost all of the data. With many tapes it moves less data than the polyphase merge.

## In plain words

You have several tapes with sorted pieces on them, and one empty tape. Merge one piece from each tape onto the empty tape, again and again, until one tape runs out. That tape is now empty, so it becomes the next place to write. Merge the pieces of the tapes that still have some onto it, until the next tape runs out, and go on in this way. Each merge uses one tape fewer than the one before, like water that falls down a row of steps.

At the end of the round, one tape still has pieces that were not merged. They stay where they are. If the numbers of pieces at the start were right, the counts after each round have the same pattern as before, only smaller, until one piece is left.

## The problem

The input is a file $F$ of $N$ items with a total order, a memory of $M$ items, and $T \ge 3$ tapes that are read and written only in sequence. The output is a tape with the items of $F$ in non-decreasing order. This is the [sorting problem](/sorting-problem/) on sequential devices.

## The algorithm

Let $P = T - 1$. The cascade distribution of level 0 is $(1, 0, \ldots, 0)$. If $(a_1, \ldots, a_P)$ is the one of level $\ell$, the one of level $\ell + 1$ is $(a_1 + \cdots + a_P,\ a_1 + \cdots + a_{P-1},\ \ldots,\ a_1 + a_2,\ a_1)$. For $T = 6$ the totals are 1, 5, 15, 55, 190, 671. For $T = 3$ the rule is the same as for the polyphase merge.

```pseudo id=main
CASCADE-MERGE-SORT(F, M, T)             ▷ T ≥ 3 tapes, memory for M items
L1  cut F into S runs of M items and sort each run
L2  find the smallest level ℓ whose cascade distribution (a₁, …, a_P), P = T − 1, has a₁ + ⋯ + a_P ≥ S
L3  for each run, put it on the tape with the most runs still missing
L4  put the missing runs of each tape as dummy runs, which are empty, at its front
L5  tape T is the output tape
L6  while the tapes hold more than one run in total do
L7      the active tapes are all tapes except the output tape
L8      while there are at least two active tapes do
L9          k ← the smallest number of runs on an active tape
L10         repeat k times
L11             merge the next run of each active tape, and write the result to the output tape
L12         remove the tape that is now empty from the active tapes, and make it the output tape
L13     rewind all tapes                ▷ one pass is complete
L14 return the single run
```

Lines L8 to L12 are one pass. The first step of a pass is a [k-way merge](/k-way-merge/) of order $P$, the next of order $P - 1$, and the last of order 2. The runs left on the last active tape are not copied; this is the "merge of order 1" of the cascade, and it costs nothing. At the end of the pass, the counts are those of the cascade distribution of the level below.

## Example

Sort the 12 items $F = (12, 3, 8, 1, 6, 2, 11, 9, 5, 4, 10, 7)$ with $M = 2$ and $T = 4$. Line L1 gives the 6 runs $R_1 = (3, 12)$, $R_2 = (1, 8)$, $R_3 = (2, 6)$, $R_4 = (9, 11)$, $R_5 = (4, 5)$ and $R_6 = (7, 10)$. The cascade distributions for $T = 4$ have the totals 1, 3, 6, 14, so $S = 6$ is perfect: $(3, 2, 1)$, of level 2, with no dummy runs.

| after | tape 1 | tape 2 | tape 3 | tape 4 | items moved |
|---|---|---|---|---|---|
| distribution | $R_1, R_2, R_4$ | $R_3, R_5$ | $R_6$ | empty | 12 |
| pass 1, merge of order 3 | $R_2, R_4$ | $R_5$ | empty | $R_{136} = (2, 3, 6, 7, 10, 12)$ | 6 |
| pass 1, merge of order 2 | $R_4$ | empty | $R_{25} = (1, 4, 5, 8)$ | $R_{136}$ | 4 |
| pass 2, merge of order 3 | empty | $(1, 2, \ldots, 12)$ | empty | empty | 12 |

Pass 1 leaves $R_4$ on tape 1 without a copy, so it moves 10 of the 12 items. The two passes move 22 items. The [balanced merge sort](/balanced-merge-sort/) on 4 tapes needs $\lceil \log_2 6 \rceil = 3$ passes, which move 36 items.

## Correctness

At the start of a pass, the $P$ input tapes hold the counts $c_i = b_1 + \cdots + b_{P-i+1}$ of a cascade distribution, where $(b_1, \ldots, b_P)$ is the distribution of the level below. Step $r$ of the pass merges $b_r$ times and empties exactly one tape, so after the step of order 2 the tapes hold $b_1, \ldots, b_P$. Each merge keeps the runs sorted and keeps all items, and the totals of the distributions decrease strictly to 1, so after $\ell$ passes one sorted run of all items is left. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Passes.** The number of passes is the level $\ell$, the smallest with a total of at least $S$. The totals grow by a factor that tends to $1/(2\sin(\pi/(4P + 2)))$ per level: about 2.25 for $T = 4$, about 3.51 for $T = 6$, and about $(2P + 1)/\pi$ for large $T$.
- **Data moved.** Each pass moves all items except those on the tape that the last step leaves alone. The table gives the number of items moved divided by $N$, with the dummy placement of line L3 and unit runs, for this method and for the polyphase merge.

| tapes | cascade, $S = 1000$ | polyphase, $S = 1000$ | cascade, $S = 20000$ | polyphase, $S = 20000$ |
|---|---|---|---|---|
| 4 | 7.93 | 6.92 | 10.74 | 9.98 |
| 6 | 5.81 | 5.33 | 7.72 | 7.67 |
| 8 | 4.92 | 4.71 | 6.89 | 6.94 |
| 10 | 3.96 | 4.55 | 5.95 | 6.61 |

With few tapes, the polyphase merge moves less data; with about 8 or more, the cascade merge does. The exact crossover depends on the placement of the dummy runs.

- **Time in memory.** $O(N \log M)$ for line L1 and $O(\log P)$ per item moved, so $O(N \log N)$ in total.

## Properties

- **Not stable.** As with the polyphase merge, the tapes do not keep the runs in the order of $F$, and a merge breaks ties by tape, not by position in $F$.
- **Not in place.** The data moves from tape to tape.
- **Sequential access.** Each tape is written from start to end and read after a rewind.
- **Fixed plan.** The level $\ell$ and all merge counts depend only on $S$ and $T$.

## Variants and improvements

- **Rewind overlap.** In a pass, the tapes become empty one at a time. A tape that is empty can be rewound while the merges of lower order go on, so the rewind time overlaps the work. Knuth's Section 5.4.3 discusses this.
- **Reading backward.** With tapes that read backward, a tape can be read without a rewind, if the directions of the runs alternate. The [oscillating sort](/oscillating-sort/) takes this further.
- **Polyphase merge.** The [polyphase merge sort](/polyphase-merge-sort/) uses only the merge of order $P$ and moves part of the data in each phase.
- **Longer runs.** [Replacement selection](/replacement-selection/) in line L1 halves $S$ on random input.

## When to use it

Use a cascade merge on sequential devices with many tapes, about 8 or more, when the time of the rewinds also matters. With fewer tapes, the [polyphase merge sort](/polyphase-merge-sort/) moves less data. On disks, use an [external merge sort](/external-merge-sort/) with the full fan-in, which needs no perfect distribution.

## Pitfalls

- **A perfect distribution of the wrong kind.** Line L2 must use the cascade rule. A polyphase distribution leaves the tapes in counts that the cascade cannot reduce to the level below.
- **Copying the last tape.** The runs left on the last active tape after line L12 must stay where they are. A copy of them moves data for nothing.
- **The wrong output tape.** Line L12 must write the next step to the tape that has just become empty, not to the output of the step before, which still holds runs for the next pass.
- **Including the output in the merge.** The tape that receives the runs of a step is not active in the later steps of the same pass. If line L11 reads from it, the counts break.

## Implementations

## History

Knuth's Section 5.4.3 describes the cascade merge, derives its perfect distributions and compares it with the polyphase merge for different numbers of tapes. He credits the method to B. K. Betz and W. C. Carter (1959). Gonnet and Baeza-Yates give it with its cost in Section 4.4 of their Handbook. With disks, which allow a merge of all runs from one device, the tape distributions lost their use; Vitter's survey treats only the multiway merge with full fan-in.

## References
