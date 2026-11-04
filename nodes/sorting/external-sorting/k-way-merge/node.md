---
tag: 04PNZQ
kind: algorithm
slug: k-way-merge
name: K-way merge
aliases:
- multiway merge
- k-way merging
area: sorting/external-sorting
level: core
summary: Merge k sorted input streams into one output stream, using a heap or tournament tree to pick the minimum.
model: comparison-model
complexity:
  vars: {n: the total number of items, k: the number of runs}
  time: {worst: O(k + n log k), average: O(k + n log k), best: O(k + n log k)}
  space: {extra: Θ(k)}
properties: {stable: true, in_place: false, adaptive: false, online: true, deterministic: true, comparison: true, recursive: false}
prereqs: [merging-sorted-lists, binary-heap, sorted-run]
see_also: [tournament-tree, external-merge-sort, merge-sort, priority-queue, optimal-merge-pattern, merging-lower-bound, funnelsort, multinomial-coefficient]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.4.1, Multiway Merging and Replacement Selection (trees of winners and trees of losers)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Heapsort (Section 6.5, priority queues, and its exercise on merging k sorted lists in O(n lg k) time)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Priority Queues (the multiway merge client of the index priority queue)
---

A k-way merge combines $k$ [sorted runs](/sorted-run/) into one sorted sequence. It keeps the first item of each run in a [binary heap](/binary-heap/) or a [tournament tree](/tournament-tree/), outputs the smallest one, and replaces it with the next item of the same run. With $n$ items in total it takes $O(k + n \log k)$ time, which is optimal for comparison merges when the runs have equal lengths. It is the inner step of [external merge sort](/external-merge-sort/), where $k$ is as large as memory allows.

## In plain words

You have several sorted lists, and you want one sorted list with all their items. The smallest item of all is at the front of one of the lists. So you look only at the front item of each list, take the smallest one, and move it to the output. Then that list has a new front item, and you do the same again.

With many lists, it takes long to find the smallest of the front items each time. So you keep the front items in a heap, a structure that gives the smallest item fast and accepts a new item fast. Each step then costs a few comparisons, about as many as the number of times you can halve the number of lists. The lists are read from front to back only, so they can be files or streams.

## The problem

The input is $k \ge 0$ sequences $S_1, \ldots, S_k$, each sorted in non-decreasing order, with $n = |S_1| + \cdots + |S_k|$ items in total. The output is one sequence that holds all the items, in non-decreasing order. For $k = 2$ this is the problem of [merging sorted lists](/merging-sorted-lists/). We also ask for stability: equal items come out in the order of their runs, and in their order inside a run.

## The algorithm

```pseudo id=main
K-WAY-MERGE(S₁, …, S_k)                 ▷ each S_i is sorted
L1  H ← an empty min-heap of pairs (x, i), ordered by x, then by i
L2  for i ← 1 to k do
L3      if S_i is not empty then add (the head of S_i, i) to H
L4  O ← an empty sequence
L5  while H is not empty do
L6      (x, i) ← the minimum of H
L7      append x to O, and remove x from the front of S_i
L8      if S_i is not empty then replace the minimum of H by (the head of S_i, i)
L9      else delete the minimum of H
L10 return O
```

The heap holds one pair for each run that still has items: its head and its number. Lines L2 and L3 put the first item of each run in the heap. The implementation builds the heap with one call of heapify, in $O(k)$ time. Line L6 reads the minimum without a removal. Line L8 overwrites the root with the next item of the same run and restores the heap with one [sift-down](/sift-down/). This is cheaper than a delete and an insert, which take two passes over the height of the heap. Line L9 removes a run that is empty, so the heap shrinks. The order of pairs by $x$ and then by $i$ makes the merge stable.

## Example

Merge $S_1 = (3, 17, 25)$, $S_2 = (8, 9)$, $S_3 = (1, 12, 30)$ and $S_4 = (4, 4, 20)$. The table shows the pairs in $H$, in sorted order, at line L6 of each step.

| step | the pairs in H | output |
|---|---|---|
| 1 | (1,3) (3,1) (4,4) (8,2) | 1 |
| 2 | (3,1) (4,4) (8,2) (12,3) | 3 |
| 3 | (4,4) (8,2) (12,3) (17,1) | 4 |
| 4 | (4,4) (8,2) (12,3) (17,1) | 4 |
| 5 | (8,2) (12,3) (17,1) (20,4) | 8 |
| 6 | (9,2) (12,3) (17,1) (20,4) | 9 |
| 7 | (12,3) (17,1) (20,4) | 12 |
| 8 | (17,1) (20,4) (30,3) | 17 |
| 9 | (20,4) (25,1) (30,3) | 20 |
| 10 | (25,1) (30,3) | 25 |
| 11 | (30,3) | 30 |

At step 3 the second 4 of $S_4$ replaces the first, so the heap has the same pairs at step 4. At step 6, $S_2$ becomes empty, so line L9 deletes its pair and the heap has 3 pairs. The output is $(1, 3, 4, 4, 8, 9, 12, 17, 20, 25, 30)$.

## Correctness

The invariant of line L5 is: $O$ is the stable sort of the items that were removed from the runs; $H$ holds exactly one pair (head of $S_i$, $i$) for each run $S_i$ that is not empty; and each item in $O$ is at most each item that is still in a run. Because each run is sorted, the smallest remaining item is the head of some run, so it is the minimum of $H$, and line L7 keeps $O$ sorted. The tie rule on $i$ keeps it stable. Each step removes one item from the runs, so the loop stops after exactly $n$ steps with all items in $O$. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

The heap has at most $k$ pairs. Building it takes $O(k)$ time. Each of the $n$ steps does one sift-down or one delete, and each costs at most $2 \lfloor \lg k \rfloor$ comparisons of pairs. So the merge takes $O(k + n \log k)$ time, and the extra space is the heap, $\Theta(k)$. A tree of losers, a form of the [tournament tree](/tournament-tree/), needs only $\lceil \lg k \rceil$ comparisons per step, because each step compares the new item with one stored loser at each level.

**Lower bound.** Take runs of lengths $n_1, \ldots, n_k$. A comparison merge must tell apart all ways to interleave the runs, and there are $\binom{n}{n_1, \ldots, n_k}$ of them, the [multinomial coefficient](/multinomial-coefficient/). By the [information-theoretic bound](/information-theoretic-bound/), some input needs at least $\lg \binom{n}{n_1, \ldots, n_k}$ comparisons. For runs of equal length $n/k$, this is at least $n \lg k - (k - 1) \lg(n + 1)$. To see it, sum the multinomial coefficients over all $\binom{n+k-1}{k-1} \le (n+1)^{k-1}$ choices of the lengths: the sum is $k^n$ by the multinomial theorem, and the term with equal lengths is the largest, because when $n_a \ge n_b + 2$, a move of one item from run $a$ to run $b$ multiplies the coefficient by $n_a/(n_b + 1) > 1$. So the loser tree is optimal up to the lower-order term, and the binary heap is within a factor of 2. For four runs of lengths 3, 2, 3 and 3, as in the example, there are $92400$ interleavings, so some input needs at least 17 comparisons.

In the [external memory model](/external-memory-model/), the merge holds one block of $B$ items of each run and one output block. If the runs have $n$ items in total, it does at most $\lceil n_1/B \rceil + \cdots + \lceil n_k/B \rceil$ reads and $\lceil n/B \rceil$ writes, with $k + 1 \le M/B$.

## Properties

- **Stable.** Pairs with equal keys are ordered by the run number $i$ in line L1.
- **Online and sequential.** Each run is read from front to back, and the output is made from front to back. The merge can start before the runs are complete, if it can wait for the next item of a run.
- **Not adaptive.** The cost does not drop when the runs do not overlap. A check of the last item of each run against the first item of the next can detect this case first.

## Variants and improvements

- **Tree of losers.** A [tournament tree](/tournament-tree/) stores the loser of each match at the inner nodes. A step replays only the path from the leaf of the used run to the root: $\lceil \lg k \rceil$ comparisons, with no comparison of siblings. Knuth gives this form for tape and disk merges.
- **A tree of two-way merges.** Merge the runs in pairs, then the results in pairs, and so on. This also takes $O(n \log k)$ time, but it writes $\lceil \lg k \rceil$ intermediate sequences, so it is not good for external data.
- **Runs of different lengths.** If the runs are merged two at a time, merge the two shortest runs first. This is the [optimal merge pattern](/optimal-merge-pattern/), the same greedy rule as Huffman coding.
- **Sentinels.** Append an item $+\infty$ to each run. Then line L9 is not necessary: an empty run stays in the heap with key $+\infty$, and the loop stops after $n$ outputs.
- **Block buffers and forecasting.** In external memory each run has a buffer of one block, or two with [double buffering](/double-buffering/). Forecasting reads next the block of the run whose buffer will become empty first, which is the run with the smallest last key in its buffer.
- **No parameters.** The $k$-merger of [funnelsort](/funnelsort/) merges $k$ runs with $O\big(k + \frac{k^3}{B}(1 + \log_M k)\big)$ cache misses for an output of $k^3$ items, without knowledge of $M$ and $B$.

## When to use it

Use a k-way merge when you have more than two sorted sequences: the runs of an [external merge sort](/external-merge-sort/), sorted files or sorted index lists, the levels of a [log-structured merge tree](/log-structured-merge-tree/), or the sorted outputs of several machines. For two runs, a plain two-way merge with one comparison per item is faster.

## Pitfalls

- **Ties by key only.** If line L1 orders the pairs only by $x$, equal items from different runs come out in any order, and the merge is not stable. In Python, a tuple $(x, i)$ compares $x$ for equality first, so items that have only a less-than test need an explicit comparison of $x$ and then of $i$.
- **A pop and a push.** If line L8 deletes the minimum and then inserts the next head, each step does two passes over the heap instead of one.
- **Empty runs.** If line L3 adds a pair for an empty run, the merge reads a head that does not exist.
- **A merge in sequence.** Merging $S_1$ with $S_2$, then the result with $S_3$, and so on, takes $\Theta(nk)$ time for runs of equal length, because the first items are copied $k - 1$ times.
- **A sentinel that is a real key.** If a run can hold the largest value of its type, a sentinel of that value is not larger than all real items.

## Implementations

## History

Knuth's Section 5.4.1 describes the multiway merge for tape and disk sorts, with the tree of winners and the tree of losers, and its use with replacement selection. The merge of $k$ lists with a heap in $O(n \lg k)$ time is a standard exercise in textbooks, for example in CLRS Chapter 6.

## References
