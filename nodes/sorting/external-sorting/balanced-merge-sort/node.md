---
tag: K6SD9E
kind: algorithm
slug: balanced-merge-sort
name: Balanced multiway merge sort
aliases:
- balanced merge
- balanced k-way merge sort
area: sorting/external-sorting
level: core
summary: Merge runs in passes over a fixed set of tapes or files, with the same number of inputs and outputs in each pass.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {N: the number of items, S: the number of initial runs, P: "the merge order, half the number of tapes"}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [sorted-run, k-way-merge, external-merge-sort]
see_also: [polyphase-merge-sort, cascade-merge-sort, oscillating-sort, replacement-selection, natural-merge-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4, External Sorting (the balanced merge on tapes), and Section 5.4.2 (comparison with the polyphase merge)
  - book: isbn:9780201416077
    title: Gaston H. Gonnet and Ricardo Baeza-Yates, Handbook of Algorithms and Data Structures, second edition
    locator: Section 4.4, External sorting (balanced merge sort)
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (passes of R-way merges)
---

Balanced multiway merge sort is the [external merge sort](/external-merge-sort/) for tapes, or for files that can only be read and written from start to end. It uses $T \ge 4$ tapes in two equal sets of $P = \lfloor T/2 \rfloor$. It writes the initial [sorted runs](/sorted-run/) in turn onto the first set, then merges one run from each tape of the first set onto the tapes of the second set, in turn, and swaps the two sets after each pass. With $S$ initial runs it makes $\lceil \log_P S \rceil$ merge passes, each over all the data.

## In plain words

You have a long list on a tape, and a few more empty tapes. A tape can only be read or written from start to end, so you cannot jump to a place on it.

First you cut the list into pieces that fit in memory, sort each piece, and write the sorted pieces onto half of the tapes, one tape after the other in turn. Then you rewind. You read the first piece of each of these tapes, merge them into one longer piece, and write it onto the first tape of the other half. The next merged piece goes onto the next tape of the other half, and so on in turn. When the input tapes are empty, the two halves change roles. Each round makes the pieces as many times longer as there are input tapes. You stop when one piece holds all the items.

## The problem

The input is a file $F$ of $N$ items with a total order. Memory holds $M$ items. There are $T \ge 4$ tapes, each read and written only in sequence. The output is a tape with the items of $F$ in non-decreasing order. This is the [sorting problem](/sorting-problem/) on sequential devices.

## The algorithm

```pseudo id=main
BALANCED-MERGE-SORT(F, M, T)            ▷ T ≥ 4 tapes, memory for M items
L1  P ← ⌊T/2⌋; the tapes A₀ … A_{P−1} are the inputs, B₀ … B_{P−1} the outputs
L2  j ← 0
L3  while F has items do
L4      read the next M items, sort them, write them as a run to A_{j mod P}; j ← j + 1
L5  while the tapes A hold more than one run in total do
L6      rewind all tapes; i ← 0
L7      while some tape A_d has a run left do
L8          merge the next run of each tape A_d that has one, and write it to B_{i mod P}; i ← i + 1
L9      swap the names A and B, and erase the new tapes B
L10 return the single run, which is on A₀
```

Lines L3 and L4 are run formation and distribution in one step: run $j$ goes to tape $A_{j \bmod P}$, so the tapes get equal numbers of runs, up to one. Line L8 is a [k-way merge](/k-way-merge/) with $k \le P$: it reads one run from the front of each input tape. Each pass puts its merged runs in turn on the output tapes, so the next pass again finds the runs spread evenly. In the last pass, the only merged run has $i = 0$, so it is on $B_0$, which line L9 names $A_0$. The merge takes the tape with the smaller index on equal keys, which keeps the sort stable.

## Example

Sort the 14 items $F = (12, 3, 8, 1, 14, 6, 2, 11, 9, 5, 13, 4, 10, 7)$ with $M = 2$ and $T = 4$, so $P = 2$. Run formation gives the 7 runs $R_1 = (3, 12)$, $R_2 = (1, 8)$, $R_3 = (6, 14)$, $R_4 = (2, 11)$, $R_5 = (5, 9)$, $R_6 = (4, 13)$ and $R_7 = (7, 10)$. We write $R_{12}$ for the merge of $R_1$ and $R_2$, and so on.

| after | first input tape | second input tape |
|---|---|---|
| distribution | $R_1, R_3, R_5, R_7$ | $R_2, R_4, R_6$ |
| pass 1 | $R_{12} = (1, 3, 8, 12)$, $R_{56} = (4, 5, 9, 13)$ | $R_{34} = (2, 6, 11, 14)$, $R_7 = (7, 10)$ |
| pass 2 | $R_{1234} = (1, 2, 3, 6, 8, 11, 12, 14)$ | $R_{567} = (4, 5, 7, 9, 10, 13)$ |
| pass 3 | $R_{1 \ldots 7} = (1, 2, \ldots, 14)$ | empty |

The table shows the tapes that are the inputs of the next pass. In pass 1, $R_7$ has no partner, so line L8 copies it alone. There are $\lceil \log_2 7 \rceil = 3$ passes.

For a larger file with $S = 1000$ initial runs, 4 tapes give 10 passes, 6 tapes give 7 passes, and 8 or 10 tapes give 5 passes.

## Correctness

Number the initial runs $R_0, R_1, \ldots$ in the order of line L4. The invariant of line L5 is: the runs on the tapes $A$ are the stable sorts of consecutive blocks of initial runs, and the $i$-th run of tape $A_d$ is block number $iP + d$, so reading the tapes in the order of $i$, then $d$, gives the blocks in order. Line L4 makes this true with blocks of one run. In a pass, line L8 merges the blocks $iP, \ldots, iP + P - 1$, which are consecutive, and writes the result as run $\lfloor i/P \rfloor$ of tape $B_{i \bmod P}$, which is again block number $i$ in the order of the invariant. Each pass reduces $s \ge 2$ runs to $\lceil s/P \rceil \le s - 1$, so the loop stops. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **Passes.** After pass $q$ there are $\lceil S/P^q \rceil$ runs, so there are $\lceil \log_P S \rceil$ merge passes when $S \ge 1$. Run formation is one more pass.
- **Data moved.** Each pass reads and writes all $N$ items, so the sort moves $N(1 + \lceil \log_P S \rceil)$ items from tape and to tape.
- **Time in memory.** Run formation takes $O(N \log M)$ comparisons. A pass takes $O(N \log P)$ comparisons with a heap. In total, $O(N \log N)$.
- **Memory.** One block buffer for each of the $P$ input tapes and one for the output tape, plus the memory for run formation.

The pass count compares with the other tape sorts by the factor by which one pass divides the number of runs: $P = T/2$ here. The [polyphase merge sort](/polyphase-merge-sort/) uses $T - 1$ inputs in each merge, and it needs fewer passes over the data when $T$ is less than about 8. For many tapes the balanced merge is better, because it reads all of the data in each pass, while the polyphase merge spreads its work over phases that each read only part of it.

## Properties

- **Stable.** The runs of a merge are consecutive blocks of the input, and the merge takes the tape with the smaller index on equal keys.
- **Not in place.** The data is copied from one set of tapes to the other in each pass.
- **Not adaptive.** With runs of a fixed size, a sorted input costs the same. With [replacement selection](/replacement-selection/) for run formation, a sorted input gives one run and no merge pass.
- **Sequential access only.** Each tape is written from start to end and read from start to end after a rewind.

## Variants and improvements

- **Longer runs.** [Replacement selection](/replacement-selection/) in line L4 makes runs of about $2M$ items on random input. This halves $S$ and can save one pass.
- **Odd number of tapes.** With $T$ odd, line L1 leaves one tape unused. One can give the inputs $\lceil T/2 \rceil$ tapes and the outputs $\lfloor T/2 \rfloor$, and alternate the two merge orders.
- **Fewer tapes per pass.** The [polyphase merge sort](/polyphase-merge-sort/) and the [cascade merge sort](/cascade-merge-sort/) keep one tape empty at a time and use the others as inputs, with an uneven distribution of runs.
- **No rewinds.** Tapes that can be read backward allow the merge to read a run in the other direction without a rewind. The [oscillating sort](/oscillating-sort/) builds on this.
- **Files on disk.** With files on disk, the restriction to $P$ input files and $P$ output files is not necessary. The [external merge sort](/external-merge-sort/) merges $M/B - 1$ runs at a time and keeps the runs on one disk.

## When to use it

Use a balanced merge when the storage can only be read and written in sequence, and there are many devices, about 8 or more. It is simple, it is stable, and its passes are easy to restart after a failure, because each pass is a complete copy. With few tapes, polyphase merging needs fewer passes. On disks, use an [external merge sort](/external-merge-sort/) with the full fan-in.

## Pitfalls

- **All runs on one tape.** If line L4 writes the runs to one tape, a pass cannot merge them, because the merge needs its inputs on different tapes.
- **The wrong output tape.** If line L8 writes all merged runs to $B_0$, the next pass has its runs on one tape. The outputs must go in turn to all $P$ output tapes.
- **Using all T tapes as inputs.** Line L1 must keep $P$ tapes free for the output. With $T - 1$ inputs and one output, the next pass has all runs on one tape, which needs a redistribution; this is the problem that polyphase merging solves.
- **Counting passes on the run size.** The number of passes is $\lceil \log_P S \rceil$ with $S$ the number of runs, not $\log_P N$. Longer initial runs reduce $S$.

## Implementations

## History

Knuth's Section 5.4 describes the balanced merge as the basic tape sort and uses it as the point of comparison for the polyphase, cascade and oscillating sorts of Sections 5.4.2 to 5.4.5. The Handbook of Gonnet and Baeza-Yates gives the balanced merge sort with its pass count in Section 4.4.

## References
