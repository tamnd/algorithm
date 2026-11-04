---
tag: 9J3JJD
kind: algorithm
slug: sift-up
name: Sift-up
aliases:
- percolate-up
- bubble-up
- heap-insert
area: data-structures/heaps
level: intro
summary: Moves a newly inserted or decreased key upward until the heap property holds.
model: comparison-model
complexity:
  vars: {n: the number of items in the heap, i: the index of the item that moves}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [heap-property, complete-binary-tree, loop-invariant]
see_also: [sift-down, sift-down-sink, binary-heap, heap-increase-key, decrease-key, heap-construction-by-insertion, priority-queue, d-ary-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (Priority queues), the procedures MAX-HEAP-INCREASE-KEY and MAX-HEAP-INSERT
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), bottom-up reheapify (swim)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), heaps and the insertion of a new item into a heap
  - paper: J. W. J. Williams, Algorithm 232, Heapsort, Communications of the ACM 7(6), 1964
    locator: the procedure INHEAP
  - paper: Ryan Hayward and Colin McDiarmid, Average case analysis of heap building by repeated insertion, Journal of Algorithms 12(1), 1991
    locator: the average number of exchanges when a heap is built by repeated insertion
---

Sift-up moves one item of a [binary heap](/binary-heap/) toward the root, by swaps with its parent, until its parent is not larger than it. It restores the [heap property](/heap-property/) after a new item is placed in the last cell of the array, and after the key of an item is decreased in a min-heap. It does at most one comparison and one swap per level, so it takes $O(\log n)$ time. It is the core of `insert` and of [decrease-key](/decrease-key/) in a heap-based [priority queue](/priority-queue/), and the mirror image of [sift-down](/sift-down/).

## In plain words

Think of a company chart in which each boss must earn less than each person below them. A new person joins at the bottom. If the new person earns less than their boss, the two change places. Then the new person compares with the next boss up, and so on. The new person stops when their boss earns less, or when they reach the top.

Each change of places fixes the order between the new person and the boss, and does not break the order anywhere else. The other people in the chart do not move, except the bosses that step down by one place. The chart is a balanced tree, so the trip to the top is short: about the number of times you can halve the number of people.

## The problem

The input is an array $A[0 \ldots n-1]$ and an index $i$ with $0 \le i < n$. The array is a *binary min-heap* in the usual layout: the parent of index $j \ge 1$ is $\lfloor (j-1)/2 \rfloor$, and the children of $j$ are $2j+1$ and $2j+2$ when they are less than $n$. The heap property is $A[\lfloor (j-1)/2 \rfloor] \le A[j]$ for each $j \ge 1$.

The precondition is that $A$ is a heap *except at $i$*:

- **(H1)** $A[\lfloor (c-1)/2 \rfloor] \le A[c]$ for each $c \ge 1$ with $c \ne i$, and
- **(H2)** if $i \ge 1$, then the parent of $i$ is at most each child of $i$.

The output is a permutation of $A$ that is a min-heap. Only the items on the path from $i$ to the root move. Two cases meet the precondition: a heap of $n - 1$ items with a new item appended at $i = n - 1$, which has no children, and a heap in which the key at $i$ was made smaller.

For a max-heap, reverse each comparison. Then sift-up restores the heap after an insert or after an increase of a key, which is MAX-HEAP-INCREASE-KEY in CLRS and `swim` in Sedgewick and Wayne.

## The algorithm

```pseudo id=main
SIFT-UP(A, i)                          ▷ A is a min-heap except at i
L1  while i > 0 do
L2      p ← ⌊(i − 1) / 2⌋              ▷ the parent of i
L3      if A[p] ≤ A[i] then return i
L4      swap A[i] and A[p]
L5      i ← p
L6  return i

HEAP-INSERT(A, x)                      ▷ A[0 .. n − 1] is a min-heap
L7  append x to A, so that x is at index n and A has n + 1 items
L8  return SIFT-UP(A, n)
```

Line L3 stops at the first ancestor that is not larger than the moving item. Line L4 moves the parent down one level, into the old cell of the item, and moves the item up. The return value is the final index of the item, which an [indexed priority queue](/indexed-priority-queue/) uses to update its handle. HEAP-INSERT places the new item in the first free cell, which keeps the tree a [complete binary tree](/complete-binary-tree/), and then calls SIFT-UP.

## Example

Start with the min-heap $A = [2, 4, 3, 7, 9, 5, 8]$ and call HEAP-INSERT$(A, 1)$, then HEAP-INSERT$(A, 3)$.

| step | $i$ | $p$ | $A[p]$ vs. moving item | action | $A$ after |
|---|---|---|---|---|---|
| L7 | 7 | | | append 1 | [2, 4, 3, 7, 9, 5, 8, 1] |
| 1 | 7 | 3 | 7 > 1 | swap | [2, 4, 3, 1, 9, 5, 8, 7] |
| 2 | 3 | 1 | 4 > 1 | swap | [2, 1, 3, 4, 9, 5, 8, 7] |
| 3 | 1 | 0 | 2 > 1 | swap | [1, 2, 3, 4, 9, 5, 8, 7] |
| L1 | 0 | | | at the root | return 0 |
| L7 | 8 | | | append 3 | [1, 2, 3, 4, 9, 5, 8, 7, 3] |
| 1 | 8 | 3 | 4 > 3 | swap | [1, 2, 3, 3, 9, 5, 8, 7, 4] |
| 2 | 3 | 1 | 2 ≤ 3 | stop | return 3 |

The first insert is a new minimum, so it climbs all $\lfloor \lg 8 \rfloor = 3$ levels with 3 comparisons. The second stops after 2 comparisons and 1 swap. In both runs, the items off the path from the new leaf to the root do not move.

## Correctness

The loop keeps this [loop invariant](/loop-invariant/) before each test of line L1: (H1) and (H2) hold for the current $i$, and $A$ is a permutation of the input. At the start this is the precondition. If line L3 finds $A[p] \le A[i]$, the one edge that (H1) leaves out also holds, so $A$ is a heap. If not, the swap of line L4 makes the edge $(p, i)$ right, and the new item at $i$, the old parent, is at most the children of $i$ by (H2). The old item of $i$ is smaller than the old parent, so it is also at most the sibling of $i$. This gives (H1) and (H2) for the new index $p$. When $i = 0$, no edge ends at the root, so (H1) says that $A$ is a heap. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The index $i$ goes to its parent in each iteration, and the parent of $j \ge 1$ has depth one less than $j$. The depth of index $i$ is $\lfloor \lg(i+1) \rfloor$. So the loop runs at most $\lfloor \lg(i+1) \rfloor$ times, with one comparison and at most one swap in each.

- **Worst case.** For HEAP-INSERT into a heap of $n$ items, $i = n$, so at most $\lfloor \lg(n+1) \rfloor$ comparisons and swaps. The bound is reached when the new item is smaller than all others. So the time is $\Theta(\log n)$ in the worst case.
- **Best case.** One comparison, when the new item is not smaller than its parent: $\Theta(1)$.
- **Average case.** When a heap is built by inserting the items of a uniformly random permutation one at a time, the mean number of swaps per insert stays bounded by a constant as $n$ grows, which Hayward and McDiarmid analyze. Most new items stop near the bottom, because half of the cells of a heap are leaves.
- **Space.** $\Theta(1)$ extra: the indices $i$ and $p$.

So building a heap by $n$ inserts costs $\Theta(n \log n)$ in the worst case, for example when the keys arrive in decreasing order, and $\Theta(n)$ on average. [Floyd's construction](/floyd-heap-construction/) by sift-down takes $\Theta(n)$ in the worst case; see [heap construction by insertion](/heap-construction-by-insertion/) for the comparison.

## Properties

- **In place.** It moves items inside the array and uses $O(1)$ extra space.
- **Local.** It changes only the cells on the path from $i$ to the root. Each other cell keeps its item.
- **Fewer comparisons than sift-down.** It does one comparison per level, against the parent. Sift-down needs two per level, because it must first find the smaller child.
- **Not stable.** Equal keys can change their relative order, as in each heap.

## Variants and improvements

- **A hole instead of swaps.** Save the moving item $x$, then shift each larger parent down into the hole, and write $x$ once at the end. This does one write per level instead of the three of a swap. `heapq` of Python and most library heaps use this form.
- **Binary search on the path.** The keys on the path from $i$ to the root are sorted, so the final place of $x$ can be found with a [binary search](/binary-search/) in $O(\log \log n)$ comparisons. The moves are still $O(\log n)$. This saves comparisons when they are expensive.
- **d-ary heaps.** In a [d-ary heap](/d-ary-heap/), the parent of $j$ is $\lfloor (j-1)/d \rfloor$, and sift-up takes $O(\log_d n)$ steps. A large $d$ makes insert and decrease-key cheaper and extract-min dearer, which is the trade-off of Dijkstra's algorithm on dense graphs.
- **Max-heaps and other orders.** The same code with $\ge$ restores a max-heap after an insert or an increase of a key, as in [heap-increase-key](/heap-increase-key/).

## When to use it

Use sift-up each time a key in a binary heap moves toward the root: a new item at the end of the array, or a lowered key in a min-heap. When a key grows in a min-heap, use [sift-down](/sift-down/) instead. When the key at $i$ is changed to an unknown new value, call both: at most one of them moves the item. To build a heap from $n$ items that are all known at the start, do not insert them one by one; use Floyd's bottom-up construction, which takes $\Theta(n)$ time.

## Pitfalls

- **The parent formula of the wrong layout.** With the root at index 0, the parent is $\lfloor (i-1)/2 \rfloor$ (line L2). The formula $\lfloor i/2 \rfloor$ is for the layout with the root at index 1. Mixing them breaks the heap without an error.
- **Strict test for the stop.** Line L3 stops when $A[p] \le A[i]$. A test $A[p] < A[i]$ also gives a heap, but it swaps equal keys up to the root for no gain.
- **Losing the handle.** In an indexed heap, each swap of line L4 moves two items. The index table of both items must change, not only that of the moving item.
- **Sift-up after an increase.** If a key in a min-heap grows, sift-up stops at once at line L3 and leaves the heap broken below $i$. That case needs sift-down.

## Implementations

## History

J. W. J. Williams published the binary heap in 1964 as Algorithm 232 of the Communications of the ACM, with the heapsort algorithm. His procedure INHEAP adds an item at the end of the heap and moves it up toward the root, which is sift-up. The names vary: CLRS writes MAX-HEAP-INCREASE-KEY, Sedgewick and Wayne call it `swim`, and other texts say percolate-up or bubble-up.

## References
