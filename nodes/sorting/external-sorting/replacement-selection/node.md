---
tag: H4VBFM
kind: algorithm
slug: replacement-selection
name: Replacement selection
aliases:
- snowplow method
- run formation by replacement selection
area: sorting/external-sorting
level: core
summary: Form runs using a heap of fixed size so that runs are on average about twice the memory size.
model: comparison-model
complexity:
  vars: {n: the number of items, P: the number of items that the heap holds}
  time: {worst: O(n log P), average: O(n log P), best: O(n log P)}
  space: {extra: Θ(P)}
properties: {stable: true, in_place: false, adaptive: true, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [sorted-run, binary-heap, priority-queue]
see_also: [replacement-selection-run-length, external-merge-sort, k-way-merge, tournament-tree, tournament-sort, polyphase-merge-sort, double-buffering]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1, Multiway Merging and Replacement Selection (Algorithm R, the snowplow argument)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition
    locator: Chapter 13, External Sorting (minimizing the number of runs)
  - paper: doi:10.1561/0400000014
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4), 2008
    locator: Section 5.2, Sorting by Merging (runs of 2M items on average by replacement selection)
---

Replacement selection is the run formation step of an [external merge sort](/external-merge-sort/) that makes [sorted runs](/sorted-run/) longer than memory. It keeps $P$ items in a [priority queue](/priority-queue/), writes the smallest item that can still extend the current run, and reads the next input item into its place. On random input the runs have an expected length of about $2P$, so there are about half as many runs as with a sort of each memoryload. It reads its input as a stream and needs $O(\log P)$ time per item.

## In plain words

Memory holds a fixed number of items. You fill it from the input. Then you repeat one step: write the smallest item in memory to the end of the current run, and read the next input item into the free place.

The new item can go in the current run only if it is not smaller than the item you just wrote, because the run must stay in order. If it is smaller, you mark it for the next run and keep it in memory. Marked items wait. When all items in memory are marked, the current run ends, and the marked items start the next run.

On random input, about half of the new items still fit in the current run, so each run gets about two memoryloads of items. On sorted input, every item fits, and the whole input becomes one run.

## The problem

The input is a stream $F$ of $n$ items with a total order. Memory holds $P \ge 1$ items. The output is a list of sorted runs whose items, together, are the items of $F$. The goal is few runs, because the merge phase of an [external merge sort](/external-merge-sort/) makes $\lceil \log_k r \rceil$ passes over $r$ runs.

## The algorithm

Each item in the heap has a run number $r$ and its input position $s$. The heap orders items by $r$, then by key, then by $s$.

```pseudo id=main
REPLACEMENT-SELECTION(F, P)             ▷ P ≥ 1 items fit in memory
L1  H ← an empty min-heap of triples (r, x, s), ordered by r, then x, then s
L2  read up to P items of F into H, each with run number 1
L3  R ← an empty list of runs
L4  while H is not empty do
L5      (r, x, s) ← the minimum of H
L6      if r > |R| then append a new empty run to R
L7      append x to run r of R
L8      if F has a next item y then
L9          if y ≥ x then t ← r else t ← r + 1
L10         replace the minimum of H by (t, y, the position of y)
L11     else delete the minimum of H
L12 return R
```

Line L5 picks the item with the smallest run number, and the smallest key among those. Line L6 starts a new run when the smallest run number in the heap is larger than the number of the current run, that is, when all items in the heap belong to the next run. Line L9 is the rule of the method: the new item $y$ can join the current run only if it is not smaller than $x$, the item that was just written. Line L10 does one [sift-down](/sift-down/). When the input is empty, line L11 shrinks the heap, and the last runs are written from memory. The position $s$ makes the order of equal items the input order.

## Example

Take $F = (5, 1, 9, 3, 7, 2, 8, 6, 4, 10, 0, 11)$ and $P = 3$. The table writes an item $x$ with run number $r$ as $x/r$, and lists the heap in its order at line L5.

| step | the heap | output | next input |
|---|---|---|---|
| 1 | 1/1 5/1 9/1 | 1 to run 1 | 3, run 1 |
| 2 | 3/1 5/1 9/1 | 3 to run 1 | 7, run 1 |
| 3 | 5/1 7/1 9/1 | 5 to run 1 | 2, run 2 |
| 4 | 7/1 9/1 2/2 | 7 to run 1 | 8, run 1 |
| 5 | 8/1 9/1 2/2 | 8 to run 1 | 6, run 2 |
| 6 | 9/1 2/2 6/2 | 9 to run 1 | 4, run 2 |
| 7 | 2/2 4/2 6/2 | 2 to run 2 | 10, run 2 |
| 8 | 4/2 6/2 10/2 | 4 to run 2 | 0, run 3 |
| 9 | 6/2 10/2 0/3 | 6 to run 2 | 11, run 2 |
| 10 | 10/2 11/2 0/3 | 10 to run 2 | none |
| 11 | 11/2 0/3 | 11 to run 2 | none |
| 12 | 0/3 | 0 to run 3 | none |

At step 3, the item 2 is smaller than the output 5, so it waits for run 2. At step 7 all items in the heap have run number 2, so run 1 ends. The runs are $(1, 3, 5, 7, 8, 9)$, $(2, 4, 6, 10, 11)$ and $(0)$. A sort of each memoryload gives 4 runs of 3 items.

On a larger input, the gain is close to a factor of 2. A random input of $10^6$ items with $P = 1000$ is cut into 501 runs, with a mean length of 1996. A sort of each memoryload gives 1000 runs.

## Correctness

Let $c$ be the number of runs in $R$, so run $c$ is the current run, and let $x$ be the last item written. The invariant of line L4 is: each run of $R$ is sorted; each item in $H$ has run number $c$ or $c + 1$; and each item in $H$ with run number $c$ is at least $x$. Line L5 takes the smallest item of run $c$ if there is one, which is at least $x$, so run $c$ stays sorted. Else all items have number $c + 1$, and line L6 starts a new run with the smallest of them. Line L9 gives the new item the number $c$ only if it is at least the item just written. Each step writes one item, so the loop stops after $n$ steps. The full proof, with the proof that each run except the last has at least $P$ items, is in [the proof page](proofs/correctness.md).

## Complexity

- **Time.** Line L2 builds the heap in $O(P)$ time. Each of the $n$ steps does one sift-down or one delete, with at most $2 \lfloor \lg P \rfloor$ comparisons of triples. The time is $O(P + n \log P)$, which is $O(n \log P)$ for $n \ge P$.
- **Space.** The heap holds $P$ items. Input and output buffers are extra.
- **I/O.** Each item is read one time and written one time. With buffers of $B$ items, run formation does about $2n/B$ block transfers, the same as a sort of each memoryload.
- **The number of runs.** Every run except the last has at least $P$ items, so there are at most $\lceil n/P \rceil$ runs: replacement selection never makes more runs than a sort of each memoryload. A reversed input gives runs of exactly $P$ items, except the last. A sorted input gives one run. For random input, the expected number of runs is $\frac{n}{2P} + O(1)$; the proof is on the page [replacement selection run length](/replacement-selection-run-length/).

## Properties

- **Stable, in a sense that a merge can use.** Equal items in one run are in input order, because of the position $s$. An item never goes to an earlier run than an equal item read before it. So a merge that takes the earlier run on equal keys gives a stable sort.
- **Online.** The method reads the input once, as a stream, and writes the runs as streams. It needs no knowledge of $n$.
- **Adaptive.** Order in the input gives longer runs. An input that is sorted, except that each item is fewer than $P$ places from its sorted place, gives one run.
- **Not in place.** The runs are new files.

## Variants and improvements

- **A tree of losers.** Knuth's Algorithm R keeps the $P$ items at the leaves of a [tournament tree](/tournament-tree/) of losers. Each step then costs $\lceil \lg P \rceil$ comparisons.
- **Natural selection.** The items for the next run go to a reservoir on disk instead of staying in memory. The current run then continues longer, at the cost of extra I/O for the reservoir. Knuth's Section 5.4.1 analyzes it.
- **Records of different sizes.** When records have different lengths, a new record may not fit into the place of the old one, and memory becomes fragmented. Implementations then manage memory in blocks, or switch to the load, sort and store method.
- **Join with the merge.** At the end of the input, the last runs are still in memory. A sort can keep them there and merge them in the first merge pass, which saves one write and one read of them.

## When to use it

Use replacement selection for run formation when the input may be partly sorted, or when the input arrives as a stream and the sort must start before the input ends. On partly sorted data it can make one run where a sort of each memoryload makes many. When memory is large, a single merge pass is often sufficient with either method, and a fast in-memory sort of each memoryload, which works well with caches, can be the better choice.

## Pitfalls

- **A strict test.** If line L9 uses $y > x$ instead of $y \ge x$, an item equal to the last output waits for the next run. On the input $(7, 7, 7, 7, 7, 7)$ with $P = 2$, this gives 3 runs instead of 1.
- **No run number in the heap.** If line L1 orders the heap only by key, line L5 can write an item of the next run into the current run, and the run is not sorted.
- **A test against the wrong item.** Line L9 must compare $y$ with $x$, the item just written. A test against the new minimum of the heap puts items into a run where they do not fit.
- **The memory for buffers.** $P$ is the number of items in the heap, not the size of memory. The input buffer and the output buffer need memory too.

## Implementations

## History

Knuth's Section 5.4.1 gives replacement selection as Algorithm R, with a tree of losers, and explains the run length of about $2P$ with the picture of a snowplow that clears a circular road during a steady snowfall. The same section gives the early history of the method. Vitter's survey lists it as the usual way to get runs of $2M$ items in an external merge sort.

## References
