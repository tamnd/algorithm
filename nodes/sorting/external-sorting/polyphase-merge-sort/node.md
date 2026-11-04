---
tag: VP4CSM
kind: algorithm
slug: polyphase-merge-sort
name: Polyphase merge sort
aliases:
- polyphase merge
- polyphase merging
area: sorting/external-sorting
level: advanced
summary: Distribute runs unevenly across tapes so that each merge phase keeps all but one input tape busy.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {N: the number of items, S: the number of initial runs, T: the number of tapes}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [balanced-merge-sort, k-way-merge, sorted-run]
see_also: [cascade-merge-sort, oscillating-sort, external-merge-sort, replacement-selection, fibonacci-numbers]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.2, The Polyphase Merge (Algorithm D, the perfect distributions, the dummy runs, and the comparison with the balanced merge)
  - paper: doi:10.1145/1460512.1460524
    title: R. L. Gilstad, Polyphase merge sorting, an advanced technique, Proceedings of the Eastern Joint Computer Conference, 1960
    locator: the whole paper, the first description of the method
  - book: isbn:9780201416077
    title: Gaston H. Gonnet and Ricardo Baeza-Yates, Handbook of Algorithms and Data Structures, second edition
    locator: Section 4.4, External sorting (polyphase merge sort)
---

Polyphase merge sort is a tape sort that merges from $T - 1$ tapes onto one tape in each phase, instead of from half of the tapes onto the other half as the [balanced merge sort](/balanced-merge-sort/) does. To make this work, it puts unequal numbers of [sorted runs](/sorted-run/) on the tapes, in a *perfect distribution* related to the [Fibonacci numbers](/fibonacci-numbers/). Each phase then empties exactly one input tape, which becomes the output tape of the next phase. With few tapes it reads and writes the data fewer times than a balanced merge.

## In plain words

You have three tapes. A balanced merge would need four tapes: two to read from and two to write to. With three tapes, you can read from two and write to one, but after one round all the merged pieces are on one tape, and you must copy half of them to another tape before the next round. That copy is wasted work.

The polyphase merge avoids the copy. It puts more pieces on one tape than on the other, in a careful ratio. You merge pairs of pieces until the shorter tape is empty. Now the longer tape still has some pieces, the output tape has the merged ones, and the empty tape is ready for the next output. You repeat. If the numbers at the start are right, this goes on until one piece holds everything.

## The problem

The input is a file $F$ of $N$ items with a total order, a memory of $M$ items, and $T \ge 3$ tapes that are read and written only in sequence. The output is a tape with the items of $F$ in non-decreasing order. This is the [sorting problem](/sorting-problem/) on sequential devices.

## The algorithm

Let $P = T - 1$. The perfect distribution of level 0 is $(1, 0, \ldots, 0)$, with $P$ entries. If $(a_1, \ldots, a_P)$ is the perfect distribution of level $\ell$, with $a_1 \ge \cdots \ge a_P$, the one of level $\ell + 1$ is $(a_1 + a_2, a_1 + a_3, \ldots, a_1 + a_P, a_1)$. For $T = 3$ the totals are the Fibonacci numbers 1, 2, 3, 5, 8, 13, and for $T = 4$ they are 1, 3, 5, 9, 17, 31, 57.

```pseudo id=main
POLYPHASE-MERGE-SORT(F, M, T)           ▷ T ≥ 3 tapes, memory for M items
L1  cut F into S runs of M items and sort each run
L2  find the smallest level ℓ whose perfect distribution (a₁, …, a_P), P = T − 1, has a₁ + ⋯ + a_P ≥ S
L3  tape d must get a_d runs; a₁ + ⋯ + a_P − S of them are dummy runs, which are empty
L4  for each run, put it on the tape with the most runs still missing
L5  put the missing runs of each tape as dummy runs at its front
L6  tape T is the output tape; the others are the input tapes
L7  while the tapes hold more than one run in total do
L8      k ← the smallest number of runs on an input tape
L9      repeat k times
L10         merge the next run of each input tape, and write the result to the output tape
L11     rewind; the input tape that is now empty becomes the output tape, and the old output tape an input tape
L12 return the single run
```

Lines L2 to L5 make the perfect distribution of level $\ell$ with the $S$ real runs and some dummy runs. Line L10 is a [k-way merge](/k-way-merge/) of $P$ runs, in which a dummy run takes part as an empty run. A phase of lines L8 to L11 takes $a_P$ runs from each input tape and reverses one step of the rule above, so the counts go back to the perfect distribution of level $\ell - 1$. After $\ell$ phases, one run is left.

## Example

Sort the 14 items $F = (12, 3, 8, 1, 14, 6, 2, 11, 9, 5, 13, 4, 10, 7)$ with $M = 2$ and $T = 4$. Line L1 gives the 7 runs $R_1 = (3, 12)$, $R_2 = (1, 8)$, $R_3 = (6, 14)$, $R_4 = (2, 11)$, $R_5 = (5, 9)$, $R_6 = (4, 13)$ and $R_7 = (7, 10)$. The smallest perfect distribution with at least 7 runs is $(4, 3, 2)$, of level 3, so there are 2 dummy runs, written $\varnothing$. We write $R_{236}$ for the merge of $R_2$, $R_3$ and $R_6$, and so on.

| after | tape 1 | tape 2 | tape 3 | tape 4 | items moved |
|---|---|---|---|---|---|
| distribution | $R_1, R_2, R_4, R_7$ | $\varnothing, R_3, R_5$ | $\varnothing, R_6$ | empty | 14 |
| phase 1 | $R_4, R_7$ | $R_5$ | empty | $R_1$, $R_{236} = (1, 4, 6, 8, 13, 14)$ | 8 |
| phase 2 | $R_7$ | empty | $R_{451} = (2, 3, 5, 9, 11, 12)$ | $R_{236}$ | 6 |
| phase 3 | empty | $(1, 2, \ldots, 14)$ | empty | empty | 14 |

Phase 1 merges twice, because tape 3 holds 2 runs. Its first merge has $R_1$ and two dummy runs, so it only copies $R_1$. The three phases move 28 items, two times the file. The [balanced merge sort](/balanced-merge-sort/) of the same file on 4 tapes needs 3 passes, which move 42 items.

## Correctness

The two facts are: each phase turns the counts of a perfect distribution of level $j$ into those of level $j - 1$, and each merge keeps the runs sorted and keeps all items. A perfect distribution of level $j \ge 1$ has its smallest entry $a_P = b_1$, where $b_1$ is the first entry of level $j - 1$; taking $b_1$ runs from each input tape leaves the other entries of level $j - 1$, and the output tape gets $b_1$. The totals grow strictly with the level, so the loop stops after exactly $\ell$ phases with one sorted run of all items. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Phases.** The number of phases is the level $\ell$, the smallest with $t_\ell \ge S$. The totals grow by a factor that tends to the root of $x^P = x^{P-1} + \cdots + x + 1$: about 1.618 for $T = 3$, 1.839 for $T = 4$, and close to 2 for many tapes. So $\ell \approx \log S / \log \lambda_P$.
- **Data moved.** A phase does not move all of the data, so the useful measure is the number of items moved divided by $N$. For $S = 1000$ runs and the dummy placement of line L4, it is 10.67 with 3 tapes, 6.92 with 4 tapes, 5.33 with 6 tapes and 4.71 with 8 tapes. The [balanced merge sort](/balanced-merge-sort/) needs 10 passes with 4 tapes, 7 with 6 tapes and 5 with 8 tapes.
- **Reduction per pass.** For large $S$, the number of runs falls by a factor of about 1.94 for each pass over the data with 3 tapes, and about 2.68 with 4 tapes. A balanced merge gives a factor of $\sqrt 2 \approx 1.41$ with 3 tapes, because it must copy half the runs after each merge, and 2 with 4 tapes. Near 8 tapes the two methods are about equal, and with more tapes the balanced merge is better.
- **Time in memory.** $O(N \log M)$ for line L1 and $O(\log P)$ per item moved with a heap, so $O(N \log N)$ in total.

## Properties

- **Not stable.** Equal keys can leave in a different order, as the proof page shows with three equal keys and 3 tapes.
- **Not in place.** The data moves from tape to tape.
- **Sequential access.** Each tape is written from start to end and read after a rewind.
- **Fixed plan.** The level $\ell$, and the number of merges in each phase, depend only on $S$ and $T$.

## Variants and improvements

- **Better dummy runs.** Knuth's Algorithm D distributes the runs level by level, so that it need not know $S$ in advance, and it puts the dummy runs where they save the most work: a merge in which all inputs but one are dummy runs is a copy, and a merge of dummy runs only costs nothing.
- **Reading backward.** On tapes that can read backward, the output of a phase can be read in the next phase without a rewind, if each tape alternates the direction of its runs.
- **Cascade merge.** The [cascade merge sort](/cascade-merge-sort/) uses merges of order $T - 1$, $T - 2$, …, 1 in one pass and has another perfect distribution. With many tapes, it moves less data than polyphase.
- **Longer runs.** [Replacement selection](/replacement-selection/) in line L1 halves $S$ on random input, which saves about $\log 2 / \log \lambda_P$ phases.

## When to use it

Use a polyphase merge when the storage is sequential and there are few devices, from 3 to about 7. It was the standard tape sort for this reason. With 8 or more tapes, use a [balanced merge sort](/balanced-merge-sort/) or a [cascade merge sort](/cascade-merge-sort/). On disks, use an [external merge sort](/external-merge-sort/) with the full fan-in, which does not need a perfect distribution.

## Pitfalls

- **No dummy runs.** If line L3 uses only real runs when $S$ is not a perfect total, some phase finds two tapes empty or none, and the plan breaks.
- **Dummy runs at the end.** If line L5 puts the dummy runs at the end of the tapes, they are merged in the last phases, where each merge is large, and the sort copies more data than necessary.
- **The wrong merge count.** Line L8 must take the smallest count on an input tape. A phase that merges more than that reads past the end of a tape.
- **The wrong output tape.** Line L11 must make the tape that is now empty the output. Any other choice leaves a tape with runs that are never merged in time.
- **Counting phases as passes.** A phase is not a pass over the data. Compare methods by the items moved, not by the number of phases.

## Implementations

## History

Gilstad described the polyphase merge in 1960. Knuth's Section 5.4.2 gives the theory of the perfect distributions, Algorithm D with its placement of dummy runs, and the tables that compare polyphase with the balanced merge; it also tells the earlier history of the method. Gonnet and Baeza-Yates give the method and its cost in Section 4.4 of their Handbook.

## References
