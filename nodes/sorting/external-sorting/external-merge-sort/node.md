---
tag: V917JH
kind: algorithm
slug: external-merge-sort
name: External merge sort
aliases:
- external mergesort
- k-way merge sort
- two-phase external sort
area: sorting/external-sorting
level: intro
summary: Form sorted runs that fit in memory, then repeatedly merge them until one sorted file remains.
solves: [sorting-problem]
model: external-memory-model
complexity:
  vars: {N: the number of items, M: the number of items that fit in memory, B: the number of items in a disk block, n: the number of blocks N/B, m: the number of blocks M/B}
  time: {worst: O(N log N), average: O(N log N), best: O(N log N)}
  space: {extra: Θ(N)}
  io:
    worst: "O(n log_m n)"
    average: "O(n log_m n)"
    best: "O(n log_m n)"
properties: {stable: true, in_place: false, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [merge-sort, sorted-run, k-way-merge, external-memory-model]
see_also: [replacement-selection, external-sorting-lower-bound, external-sorting-io-lower-bound, polyphase-merge-sort, double-buffering, funnelsort, external-samplesort, sort-merge-join]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4 (External Sorting) and Section 5.4.1 (Multiway Merging and Replacement Selection)
  - paper: doi:10.1145/48529.48535
    title: Alok Aggarwal and Jeffrey Scott Vitter, The input/output complexity of sorting and related problems, Communications of the ACM 31(9), 1988, pages 1116 to 1127
    locator: the model, the merge sort upper bound and the lower bound for sorting
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging, and Theorem 5.1
---

External merge sort sorts a file that is too large for main memory. It reads the file one memoryload at a time, sorts each load in memory and writes it back as a [sorted run](/sorted-run/), then merges $k$ runs at a time with a [k-way merge](/k-way-merge/) until one run is left. In the [external memory model](/external-memory-model/) it does $O\big(\frac NB \log_{M/B} \frac NB\big)$ block transfers, which matches the [I/O lower bound for sorting](/external-sorting-lower-bound/). It is the sort that databases and command-line tools use for data on disk.

## In plain words

You must sort a pile of papers that is much larger than your desk. First you take as many papers as fit on the desk, sort them, and put them on the floor as one sorted stack. You do this until all the papers are in sorted stacks.

Then you merge the stacks. You put the top sheet of a few stacks on the desk, leave room for one output stack, and always move the smallest top sheet to the output. When a stack is empty, it is finished. Each merge makes fewer, longer stacks. You repeat until one stack holds all the papers.

The slow part is to walk to the floor and back, not the work on the desk. So the method moves papers in large bundles and merges as many stacks at a time as the desk allows. Then each paper makes only a few trips.

## The problem

The input is a file $F$ of $N$ items with a total order, stored on disk in blocks of $B$ items. Main memory holds $M$ items. The output is a file with the same items in non-decreasing order. This is the [sorting problem](/sorting-problem/) in the [external memory model](/external-memory-model/): the cost is the number of block reads and block writes, and work in memory is free. We assume $M \ge 3B$ and that $B$ divides $M$.

## The algorithm

```pseudo id=main
EXTERNAL-MERGE-SORT(F, M, B)            ▷ F has N items on disk, M ≥ 3B
L1  k ← M/B − 1                         ▷ k input buffers and one output buffer
L2  R ← an empty list of runs
L3  for each piece of M consecutive items of F, from left to right do
L4      read the piece into memory
L5      sort it in memory with a stable sort, write it as a run, and append it to R
L6  while |R| > 1 do
L7      R′ ← an empty list of runs
L8      for each group G of k consecutive runs of R, from left to right do
L9          if |G| = 1 then append the run of G to R′          ▷ no I/O
L10         else merge the runs of G into one run, and append it to R′
L11     R ← R′
L12 return the single run of R, or an empty file if N = 0
```

Lines L3 to L5 are the run formation phase. Each piece fills memory, so each run has $M$ items, except the last run. Lines L6 to L11 are the merge phase. One iteration of line L6 is a *pass*. Line L10 is a [k-way merge](/k-way-merge/): memory holds one block of each input run and one output block. When the block of a run is used up, the merge reads the next block of that run. When the output block is full, the merge writes it. A [tournament tree](/tournament-tree/) or a [binary heap](/binary-heap/) finds the smallest head. For equal heads, the merge takes the head of the run that comes first in $G$. Line L9 keeps a last group of one run as it is, because a merge of one run only copies it.

## Example

Sort 18 items with $M = 6$ and $B = 2$, so the fan-in is $k = 6/2 - 1 = 2$:

$$F = [41, 7, 63, 18, 90, 2, 55, 34, 12, 77, 29, 5, 68, 23, 81, 46, 9, 60].$$

The file has 9 blocks.

| step | the runs | block I/Os |
|---|---|---|
| run formation | [2 7 18 41 63 90] [5 12 29 34 55 77] [9 23 46 60 68 81] | 9 reads, 9 writes |
| pass 1 | [2 5 7 12 18 29 34 41 55 63 77 90] [9 23 46 60 68 81] | 6 reads, 6 writes |
| pass 2 | [2 5 7 9 12 18 23 29 34 41 46 55 60 63 68 77 81 90] | 9 reads, 9 writes |

In pass 1, the groups are the first two runs and the third run alone. Line L10 merges the first two runs. Line L9 keeps the third run, with no I/O. Pass 2 merges the two remaining runs. The total is $18 + 12 + 18 = 48$ block I/Os. The bound below gives $2 \cdot 9 \cdot (1 + 2) = 54$.

A large example: $N = 10^{10}$ items, $M = 10^6$ and $B = 10^4$. Then $\lceil N/B \rceil = 10^6$ blocks, run formation makes $10^4$ runs, and $k = 99$. The passes reduce the number of runs from $10^4$ to 102, then to 2, then to 1. That is 3 passes and $2 \cdot 10^6 \cdot 4 = 8 \cdot 10^6$ block I/Os. With $M = 8 \cdot 10^7$, there are 125 runs and $k = 7999$, so one pass is sufficient and the sort does $4 \cdot 10^6$ block I/Os: it reads and writes the file two times.

## Correctness

Number the pieces of line L3 from left to right. The invariant of line L6 is: the runs of $R$, in order, are the stable sorts of consecutive parts $F_1, F_2, \ldots$ of $F$, whose concatenation is $F$. Line L5 makes this true. A stable merge of consecutive runs, which takes the earlier run first on a tie, gives the stable sort of the union of their parts, so line L10 keeps the invariant. Each pass reduces $|R| = r \ge 2$ to $\lceil r/k \rceil \le r - 1$, so the loop stops, and then the one run is the stable sort of $F$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

Let $n = \lceil N/B \rceil$, the number of blocks of the file, and $r_0 = \lceil N/M \rceil$, the number of runs.

- **Run formation.** Each block is read one time and written one time: $2n$ I/Os.
- **One pass.** Each run in a merged group is read one time and written one time. All runs except the last have a length that is a multiple of $B$, so each pass costs at most $2n$ I/Os.
- **The number of passes.** After pass $i$ there are $\lceil r_0 / k^i \rceil$ runs. So the number of passes is $p = \lceil \log_k r_0 \rceil$ when $r_0 \ge 1$.

The total is at most

$$2 \left\lceil \frac NB \right\rceil \left(1 + \left\lceil \log_{M/B - 1} \left\lceil \frac NM \right\rceil \right\rceil\right)$$

block I/Os. The [external memory model](/external-memory-model/) page shows that this is at most $8 \lceil N/B \rceil \log_{M/B} (N/B)$ when $N > M$, which is $O\big(\frac NB \log_{M/B} \frac NB\big)$. The [external sorting lower bound](/external-sorting-lower-bound/) shows that each comparison sort needs $\Omega\big(\frac NB \log_{M/B} \frac NB\big)$ I/Os for $N \ge e^2 B$ and $B \le M/2$. So external merge sort is optimal in this model, up to a constant factor. The bound for $D$ parallel disks is on the page [external sorting I/O lower bound](/external-sorting-io-lower-bound/).

The work in memory is $O(N \log M)$ comparisons for run formation and $O(N \log k)$ comparisons per pass with a heap, which is $O(N \log N)$ in total. The disk space is $2N$ items, because each pass reads the old runs and writes the new runs.

## Properties

- **Stable.** Line L5 uses a stable sort, and line L10 takes the earlier run on a tie.
- **Not in place.** Each pass writes a new copy of the data. The disk space of a run can be freed after the merge has read it, but the file still needs $N$ items of free space in the worst case.
- **Not adaptive.** A sorted input costs the same number of I/Os. Run formation with [replacement selection](/replacement-selection/) makes one run from a sorted input.
- **Sequential access.** Each run is read and written from left to right. This is why the method works on tapes and on disks, where sequential access is much faster than random access.

## Variants and improvements

- **Longer runs.** [Replacement selection](/replacement-selection/) makes runs of about $2M$ items on random input, so there are about half as many runs.
- **Overlap of I/O and work.** [Double buffering](/double-buffering/) gives each run two buffers, so the merge works on one buffer while the disk fills the other. The fan-in drops to about $M/(2B)$.
- **Several disks.** [Disk striping](/disk-striping/) treats $D$ disks as one disk with blocks of $DB$ items. It is simple, but it is not optimal when $D$ is large. Randomized cycling and [balance sort](/balance-sort/) reach the optimal bound for $D$ disks.
- **Tapes.** With tapes, a run must be on a separate tape to be merged. [Balanced merge sort](/balanced-merge-sort/), [polyphase merge sort](/polyphase-merge-sort/), [cascade merge sort](/cascade-merge-sort/) and [oscillating sort](/oscillating-sort/) arrange the runs on a small number of tapes.
- **Distribution instead of merging.** [External samplesort](/external-samplesort/) splits the file into buckets by splitters and sorts each bucket. It has the same I/O bound.
- **No parameters.** [Funnelsort](/funnelsort/) has the same bound in the [cache-oblivious model](/cache-oblivious-model/), where the algorithm does not know $M$ and $B$.
- **Sort keys, then move records.** For large records, sort pairs of a key and a record number, then move the records. This second step is [external permuting](/external-permuting/).

## When to use it

Use external merge sort when the data does not fit in memory, for example to sort a log file, to build an index, or for a [sort-merge join](/sort-merge-join/). One merge pass is sufficient when the file has at most $(M/B - 1)M$ items. With $M = 10^9$ items and $B = 10^5$ items, that is about $10^{13}$ items. If the data fits in memory, an in-memory sort such as [merge sort](/merge-sort/) is faster. If only a small number of distinct keys is present, or if you need only a group by key, a [hash join](/hash-join/) or a hash partition can avoid the sort.

## Pitfalls

- **No room for the output buffer.** Line L1 must set $k = M/B - 1$, not $M/B$. With $M/B$ input buffers, the output block does not fit in memory.
- **Binary merges.** If line L10 merges only two runs at a time, the number of passes is $\lceil \lg r_0 \rceil$ instead of $\lceil \log_k r_0 \rceil$. For $10^4$ runs, that is 14 passes instead of 2 with $k = 999$.
- **Ties without the run number.** If the heap of line L10 compares only keys, equal keys from different runs can come out in either order, and the sort is not stable.
- **Small blocks.** If $B$ is small, for example one record, each I/O pays the full seek time. Use blocks of many kilobytes, even if this makes $k$ smaller.
- **Copying a lone run.** If line L9 merges a group of one run, the pass copies it for no gain.

## Implementations

## History

Knuth's Section 5.4 describes merge sorts for tapes and disks from the early years of computing, and Section 5.4.1 gives replacement selection and the k-way merge with a tree of losers. Aggarwal and Vitter in 1988 defined the external memory model with $M$ and $B$, showed that the k-way merge sort does $O\big(\frac NB \log_{M/B} \frac NB\big)$ I/Os, and proved a matching lower bound. Vitter's survey of 2008 gives the variants for parallel disks.

## References
