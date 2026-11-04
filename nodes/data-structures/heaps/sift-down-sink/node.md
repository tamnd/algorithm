---
tag: RCFB8N
kind: algorithm
slug: sift-down-sink
name: Sink (sift-down) operation
aliases:
- Sink
area: data-structures/heaps
level: intro
summary: Restores heap order by exchanging a node with its larger child repeatedly until the node is no smaller than its children.
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [sift-down, heap-property, loop-invariant]
see_also: [sift-down, sift-up, heapsort, binary-heap, floyd-heap-construction, heap-extract-max, priority-queue]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), top-down reheapify (sink), the class MaxPQ, and the subsection on heapsort with its cost propositions
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Sections 6.2 to 6.4 (MAX-HEAPIFY, BUILD-MAX-HEAP and HEAPSORT)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), Algorithm H (heapsort)
---

Sink is the form of [sift-down](/sift-down/) in a max-heap stored at positions 1 to $n$ of an array, written with two helpers: `less(i, j)`, which compares the items at positions $i$ and $j$, and `exch(i, j)`, which swaps them. It moves the item at position $k$ down, by exchanges with its *larger* child, until it is not smaller than its children. It is the name and the code of Sedgewick and Wayne, where `sink` serves `delMax` of the priority queue `MaxPQ` and both phases of [heapsort](/heapsort/). This page treats that formulation and heapsort built on it; the general operation, its min-heap form with the root at index 0, and the bottom-up variant are on the [sift-down](/sift-down/) page.

## In plain words

Picture a sports ladder drawn as a tree, where each player must be at least as strong as the two players right below. A weak player is placed at some spot. The player looks at the two below, picks the stronger one, and if that one is stronger, the two change places. Then the weak player looks down again. This stops when nobody below is stronger.

Heapsort uses this step twice. First it fixes every spot of an unsorted list from the bottom up, so that the strongest player is at the top. Then it takes the top player out, puts the last player at the top, sinks that player, and takes the next top player out, until the list is sorted.

## The problem

The heap occupies positions $1, \ldots, n$. The children of position $k$ are $2k$ and $2k + 1$ when they are at most $n$, and the parent of $k \ge 2$ is $\lfloor k/2 \rfloor$. The array is a *max-heap* when each item is not smaller than its children: $\neg\,\text{less}(\lfloor j/2 \rfloor, j)$ for each $2 \le j \le n$. This 1-based layout makes the index arithmetic short, and the tree is the same [complete binary tree](/complete-binary-tree/) as in the 0-based layout.

The input of SINK is a position $k$ such that the subtrees of $2k$ and $2k + 1$ are max-heaps. The output is a permutation of the items of the subtree of $k$, inside that subtree, such that the subtree is a max-heap. The helpers make the code the same for each item type and for each place where the items live. Heapsort uses this: its positions $1, \ldots, n$ are the cells $0, \ldots, n-1$ of a 0-based array, and only `less` and `exch` know it.

## The algorithm

```pseudo id=main
SINK(k, n)                              ▷ the subtrees of 2k and 2k + 1 are max-heaps
L1  while 2k ≤ n do
L2      j ← 2k
L3      if j < n and less(j, j + 1) then j ← j + 1     ▷ j is the larger child
L4      if not less(k, j) then break
L5      exch(k, j)
L6      k ← j

DEL-MAX()                               ▷ pq[1 .. n] is a max-heap with n ≥ 1
L7  max ← pq[1]
L8  exch(1, n); n ← n − 1
L9  SINK(1, n)
L10 pq[n + 1] ← null                    ▷ do not keep a reference to the old maximum
L11 return max

HEAPSORT(a[1 .. n])
L12 for k ← ⌊n/2⌋ downto 1 do SINK(k, n)                ▷ heap construction
L13 while n > 1 do                                      ▷ sortdown
L14     exch(1, n); n ← n − 1
L15     SINK(1, n)
```

Line L1 runs while $k$ has a left child. Line L3 moves $j$ to the right child when it exists and is larger. Line L4 stops when the item at $k$ is not smaller than the larger child. DEL-MAX swaps the root with the last item, shrinks the heap, and sinks the new root. Line L10 clears the old cell, so that a language with garbage collection can free the item. HEAPSORT first makes a max-heap with sink at each internal position from right to left. Then each round of the sortdown moves the maximum of the heap to the end of the heap, where it stays, and sinks the new root.

## Example

Heapsort on $a = [5, 1, 9, 3, 7, 6, 2, 8, 4]$, with positions 1 to 9.

**Construction.** The calls go from $k = 4$ down to $k = 1$.

| call | larger child | moves | $a$ after | compares |
|---|---|---|---|---|
| SINK(4, 9) | 8 at position 8 | 3 down to 8 | [5, 1, 9, 8, 7, 6, 2, 3, 4] | 2 |
| SINK(3, 9) | 6 at position 6 | none, 9 is larger | [5, 1, 9, 8, 7, 6, 2, 3, 4] | 2 |
| SINK(2, 9) | 8, then 4 | 1 down to 4, then to 9 | [5, 8, 9, 4, 7, 6, 2, 3, 1] | 4 |
| SINK(1, 9) | 9, then 6 | 5 down to 3, then to 6 | [9, 8, 6, 4, 7, 5, 2, 3, 1] | 4 |

The construction does 12 compares, fewer than $2n = 18$.

**Sortdown.** Each row swaps the root with the last item of the heap, then sinks the new root. The sorted tail is on the right.

| heap size after | heap | sorted tail | compares |
|---|---|---|---|
| 8 | [8, 7, 6, 4, 1, 5, 2, 3] | [9] | 4 |
| 7 | [7, 4, 6, 3, 1, 5, 2] | [8, 9] | 4 |
| 6 | [6, 4, 5, 3, 1, 2] | [7, 8, 9] | 3 |
| 5 | [5, 4, 2, 3, 1] | [6, 7, 8, 9] | 2 |
| 4 | [4, 3, 2, 1] | [5, 6, 7, 8, 9] | 3 |
| 3 | [3, 1, 2] | [4, 5, 6, 7, 8, 9] | 2 |
| 2 | [2, 1] | [3, 4, 5, 6, 7, 8, 9] | 1 |
| 1 | [1] | [2, 3, 4, 5, 6, 7, 8, 9] | 0 |

The whole sort does $12 + 19 = 31$ compares. The first row is also one DEL-MAX on the heap after the construction: it returns 9 and leaves $[8, 7, 6, 4, 1, 5, 2, 3]$.

## Correctness

SINK keeps this [loop invariant](/loop-invariant/) at line L1, with $k_0$ the input position: each parent-child pair in the subtree of $k_0$ whose parent is not $k$ is in heap order, and if $k \ne k_0$, the parent of $k$ is at least each child of $k$. An exchange at line L5 puts the larger child $j$ at $k$, which is at least its sibling and at most the parent of $k$, and then the invariant holds for $j$. At the end, $k$ is a leaf or not smaller than its larger child, so the whole subtree is a max-heap. Heapsort is correct by a second invariant of the loop of line L13: $a[1 \ldots n]$ is a max-heap, and $a[n+1 \ldots]$ holds the largest items in sorted order, each at least each item of the heap. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The number of levels below position $k$ in a heap of $n$ items is $\lfloor \lg(n/k) \rfloor$. Each pass of the loop that does not stop goes down one level and calls `less` at most twice. So SINK$(k, n)$ makes at most $2 \lfloor \lg(n/k) \rfloor$ compares and $\lfloor \lg(n/k) \rfloor$ exchanges.

- **DEL-MAX.** At most $2 \lfloor \lg n \rfloor$ compares and $\lfloor \lg n \rfloor + 1$ exchanges, with the one of line L8: $\Theta(\log n)$ time in the worst case.
- **Heap construction.** The calls of line L12 make at most $2 \sum_{k=1}^{n} \lfloor \lg(n/k) \rfloor = 2(n - \nu(n))$ compares, where $\nu(n)$ is the number of ones in the binary form of $n$. The sum is derived on the [sift-down](/sift-down/) page. So the construction uses fewer than $2n$ compares and fewer than $n$ exchanges.
- **Heapsort.** The sortdown makes $n - 1$ calls of SINK$(1, m)$ for $m < n$, each with at most $2 \lfloor \lg n \rfloor$ compares. With the construction, heapsort uses fewer than $2n \lg n + 2n$ compares and at most half as many exchanges, plus the $n - 1$ exchanges of line L14. It runs in $\Theta(n \log n)$ time in the worst case and $O(1)$ extra space.
- **Best case of SINK.** One or two compares, when the item is not smaller than its children.

These are the bounds that Sedgewick and Wayne prove in Section 2.4. Heapsort does about twice as many compares as [merge sort](/merge-sort/), and it accesses memory far apart, so in practice it is slower than a good quicksort or merge sort. It is the sort with an $O(n \log n)$ worst case and $O(1)$ extra space.

## Properties

- **In place.** Heapsort with sink needs no array besides the input.
- **Not stable.** The exchange of line L14 jumps over many items, so equal keys can change their order.
- **Generic.** All access to the items goes through `less` and `exch`. The same code sorts any type, and it can count compares or animate the sort by wrapping the helpers.
- **Not adaptive.** A sorted input still costs $\Theta(n \log n)$: the construction moves the largest item to the front.

## Variants and improvements

- **Sink to the bottom.** In the sortdown, the item placed at the root comes from the bottom, so it almost always sinks to the bottom again. Floyd's idea, used in bottom-up heapsort, goes down the path of larger children without comparing the item, then climbs back up. This nearly halves the compares. See [sift-down](/sift-down/).
- **0-based layout.** With the root at index 0, the children of $k$ are $2k + 1$ and $2k + 2$. The `less` and `exch` helpers of heapsort hide this shift instead.
- **Min-heap.** Reverse `less` to get a min-heap, for `delMin` of a `MinPQ`, as used by the [top M](/top-m-problem/) client.
- **Indexed priority queue.** In an [indexed priority queue](/indexed-priority-queue/), `exch` also updates the table from items to positions. Sink is otherwise the same.

## When to use it

Use this form when a heap stores its items at positions 1 to $n$, or when the code must be generic over the item type and the storage, as in a textbook library. Use heapsort when the sort must run in $O(n \log n)$ in the worst case with $O(1)$ extra memory, for example in an embedded system or as the fallback of [introsort](/introsort/). When stability or speed on real data matters more, use [merge sort](/merge-sort/) or Timsort.

## Pitfalls

- **The bound of the loop.** The test of line L1 is $2k \le n$, not $2k < n$. With $<$, a node whose only child is at position $n$ is never compared with that child.
- **The right child past the heap.** Line L3 needs $j < n$. Without it, the code compares with position $n + 1$, which in heapsort holds a sorted item, and pulls it back into the heap.
- **Exchanging with the smaller child.** Line L3 must pick the *larger* child in a max-heap. An exchange with the smaller child leaves a larger item below a smaller one.
- **The heap size in the sortdown.** Line L15 must use the size after line L14 decreased it. Using the old $n$ undoes the last step.
- **Off by one in the helpers.** In heapsort on a 0-based array, `less(i, j)` must compare $a[i - 1]$ and $a[j - 1]$. Forgetting the shift in one helper but not in the other breaks the sort only on some inputs.

## Implementations

## History

The operation comes from the heapsort papers of 1964: J. W. J. Williams introduced the heap, and Robert W. Floyd gave the linear-time construction that sinks each internal node from the last to the first. The name `sink`, the companion `swim` for [sift-up](/sift-up/), and the style with the helpers `less` and `exch` are those of the textbooks of Robert Sedgewick, in the fourth edition with Kevin Wayne.

## References
