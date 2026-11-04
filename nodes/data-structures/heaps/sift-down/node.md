---
tag: MFM3MX
kind: algorithm
slug: sift-down
name: Sift-down
aliases:
- percolate-down
- bubble-down
- heapify-down
- max-heapify
area: data-structures/heaps
level: intro
summary: Moves a key downward, swapping with its smaller (or larger) child, until the heap property holds.
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [heap-property, complete-binary-tree, loop-invariant]
see_also: [sift-up, sift-down-sink, binary-heap, floyd-heap-construction, heapsort, heap-extract-max, d-ary-heap, priority-queue]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.2 (Maintaining the heap property, MAX-HEAPIFY) and Section 6.3 (Building a heap)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), Algorithm H (heapsort) and the sift-down loop in its steps H3 to H8
  - paper: Robert W. Floyd, Algorithm 245, Treesort 3, Communications of the ACM 7(12), 1964
    locator: the procedure siftup, which moves an item down the tree in the paper's terms
  - paper: Ingo Wegener, Bottom-up heapsort, a new variant of heapsort beating, on an average, quicksort (if n is not very small), Theoretical Computer Science 118(1), 1993
    locator: the bottom-up form of sift-down and its comparison bounds
---

Sift-down moves one item of a [binary heap](/binary-heap/) away from the root, by swaps with its smaller child, until no child is smaller than it. It restores the [heap property](/heap-property/) at a node whose two subtrees are heaps but whose own item may be too large. It does at most two comparisons per level, so it takes $O(\log n)$ time. It is the core of extract-min, of [Floyd's heap construction](/floyd-heap-construction/) in $\Theta(n)$ time and of [heapsort](/heapsort/); the mirror operation is [sift-up](/sift-up/). This page uses a min-heap with the root at index 0. The max-heap form with the root at index 1, as `sink` in Sedgewick and Wayne, is on the page [sink](/sift-down-sink/).

## In plain words

Think of a company chart in which each boss must earn less than each person below them. The boss at some place leaves, and a person who earns too much takes the empty seat. That person looks at the two people right below. If one of them earns less, the two change places, and the lower earner of the two moves up. Then the person looks down again, and so on, until nobody right below earns less, or there is nobody below.

The person must change places with the lower earner of the two, not with any one of them. Only then is the one who moves up a good boss for both people below. The chart is a balanced tree, so the trip to the bottom is short.

## The problem

The input is an array $A$ with a heap size $n$, and an index $i$ with $0 \le i < n$. The layout is the usual one: the children of $j$ are $2j+1$ and $2j+2$ when they are less than $n$, and the parent of $j \ge 1$ is $\lfloor (j-1)/2 \rfloor$. Let $T(i)$ be the set of indices in the subtree of $i$. An edge $(q, c)$, with $q$ the parent of $c$, is *right* when $A[q] \le A[c]$.

The precondition is that the subtree of $i$ is a heap *except at $i$*: each edge of $T(i)$ whose parent is not $i$ is right. In other words, the subtrees of the two children of $i$ are min-heaps. The output is a permutation of the items of $T(i)$ inside $T(i)$ such that all edges of $T(i)$ are right. No cell outside $T(i)$ changes.

For a max-heap, reverse each comparison and pick the *larger* child. This is MAX-HEAPIFY of CLRS.

## The algorithm

```pseudo id=main
SIFT-DOWN(A, i, n)                     ▷ the subtree of i is a min-heap except at i
L1  loop
L2      l ← 2i + 1                     ▷ the left child
L3      if l ≥ n then return i         ▷ i is a leaf
L4      c ← l
L5      if l + 1 < n and A[l + 1] < A[l] then c ← l + 1    ▷ c is the smaller child
L6      if A[i] ≤ A[c] then return i
L7      swap A[i] and A[c]
L8      i ← c

EXTRACT-MIN(A)                         ▷ A[0 .. n − 1] is a min-heap with n ≥ 1
L9  x ← A[0]
L10 move A[n − 1] to A[0] and remove the last cell, so n ← n − 1
L11 if n > 0 then SIFT-DOWN(A, 0, n)
L12 return x
```

Lines L4 and L5 find the smaller child $c$. Line L6 stops when the item is not larger than that child, so it is not larger than either child. Else line L7 moves the smaller child up into the cell of $i$, where it is at most its old sibling, and the item goes down one level. EXTRACT-MIN takes the root, moves the last item into the root, which keeps the tree a [complete binary tree](/complete-binary-tree/), and sifts it down.

## Example

**Extract-min.** Start with the min-heap $A = [1, 2, 3, 4, 9, 5, 8, 7]$ and call EXTRACT-MIN$(A)$. Line L10 moves the last item 7 to the root.

| step | $i$ | children | smaller child $c$ | $A[i]$ vs. $A[c]$ | action | $A$ after |
|---|---|---|---|---|---|---|
| L10 | | | | | 7 to the root | [7, 2, 3, 4, 9, 5, 8] |
| 1 | 0 | 2, 3 | 1 | 7 > 2 | swap | [2, 7, 3, 4, 9, 5, 8] |
| 2 | 1 | 4, 9 | 3 | 7 > 4 | swap | [2, 4, 3, 7, 9, 5, 8] |
| 3 | 3 | none | | | leaf | return 3 |

The result is 1, and the heap is $[2, 4, 3, 7, 9, 5, 8]$. The item 7 went down 2 levels with 4 comparisons.

**Building a heap.** Floyd's method calls SIFT-DOWN$(A, i, n)$ for $i = \lfloor n/2 \rfloor - 1$ down to 0. On $A = [9, 4, 7, 1, 8, 2, 6, 3, 5]$, with $n = 9$:

| call | moves | $A$ after |
|---|---|---|
| $i = 3$ | 1 is not larger than 3 and 5, no move | [9, 4, 7, 1, 8, 2, 6, 3, 5] |
| $i = 2$ | 7 down to index 5 | [9, 4, 2, 1, 8, 7, 6, 3, 5] |
| $i = 1$ | 4 down to index 3, then to index 7 | [9, 1, 2, 3, 8, 7, 6, 4, 5] |
| $i = 0$ | 9 down to index 1, 3, then 7 | [1, 3, 2, 4, 8, 7, 6, 9, 5] |

The four calls do 14 comparisons. This is exactly the bound $2(n - \nu(n)) = 2(9 - 2)$ of the Complexity section, where $\nu(n)$ is the number of ones in the binary form of $n$.

## Correctness

The loop keeps this [loop invariant](/loop-invariant/) at line L2, where $i_0$ is the input index: (D1) each edge of $T(i_0)$ whose parent is not $i$ is right, and (D2) if $i \ne i_0$, the parent of $i$ is at most each child of $i$. At the start, (D1) is the precondition and (D2) says nothing. If $i$ is a leaf, or if $A[i] \le A[c]$ at line L6, the edges from $i$ are right too, and the subtree is a heap. Else line L7 puts the smaller child $c$ at $i$. It is at most its sibling, and at most the parent of $i$ by (D2), so the edges into and out of $i$ become right, and (D2) holds for $c$, because the old $A[c]$ was at most the children of $c$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let the *height* of index $i$ in a heap of $n$ items be $h(i) = \lfloor \lg(n/(i+1)) \rfloor$: the largest $k$ with $(i+1) 2^k \le n$, which is the number of levels below $i$. Each iteration that does not return moves $i$ to a child, one level down. So SIFT-DOWN runs at most $h(i)$ full iterations, with at most two comparisons each, plus a final iteration with at most two comparisons only if $i$ is not then a leaf. The count of comparisons is at most $2h(i)$: a final iteration that compares means $i$ still has a child, and then the full iterations before it were fewer than $h(i)$.

- **Worst case.** For the root, $h(0) = \lfloor \lg n \rfloor$, so at most $2 \lfloor \lg n \rfloor$ comparisons and $\lfloor \lg n \rfloor$ swaps. EXTRACT-MIN usually reaches this bound, because the item moved from the last cell is a large one. So the time is $\Theta(\log n)$ in the worst case.
- **Best case.** One or two comparisons, when the item is not larger than its children: $\Theta(1)$.
- **Space.** $\Theta(1)$ extra.

**Floyd's construction in linear time.** The construction calls SIFT-DOWN once for each internal node, so it does at most $2 \sum_i h(i)$ comparisons. The number of indices with $h(i) \ge k$ is the number of $i$ with $i + 1 \le n/2^k$, which is $\lfloor n/2^k \rfloor$. So

$$\sum_{i=0}^{n-1} h(i) = \sum_{k \ge 1} \left\lfloor \frac{n}{2^k} \right\rfloor = n - \nu(n),$$

where the last step is Legendre's formula for the power of 2 in $n!$. Hence the construction does fewer than $2n$ comparisons and fewer than $n$ swaps, and it takes $\Theta(n)$ time. For $n = 100$ the bound is $2 \cdot 97 = 194$ comparisons; for $n = 1000$ it is $2 \cdot 994 = 1988$.

**Heapsort.** Heapsort builds a max-heap and then does $n - 1$ extractions, each with one sift-down from the root. So it does at most $2n \lfloor \lg n \rfloor + 2n$ comparisons and runs in $\Theta(n \log n)$ time.

## Properties

- **In place.** It moves items inside the array and uses $O(1)$ extra space.
- **Local.** Only the cells on one path from $i$ down to a node of $T(i)$ change.
- **Two comparisons per level.** One comparison picks the smaller child, the other compares it with the item. Sift-up needs only one per level.
- **Not stable.** Equal keys can change their relative order.

## Variants and improvements

- **A hole instead of swaps.** Save the item, move each smaller child up into the hole, and write the item once at the end. This does one write per level instead of three.
- **Bottom-up sift-down.** First follow the path of smaller children all the way to a leaf, with one comparison per level. Then climb back up this path to the first key that is not larger than the item, and shift the path up by one. The item from the last cell of a heap is usually large, so the climb is short. Wegener showed that heapsort with this form, called bottom-up heapsort, does at most $1.5 n \lg n + O(n)$ comparisons, and about $n \lg n + O(n)$ on average. Python's `heapq` uses this form in `heappop`.
- **d-ary heaps.** In a [d-ary heap](/d-ary-heap/), the item compares with $d$ children per level, so a sift-down costs $O(d \log_d n)$.
- **Sink.** The max-heap form with the root at index 1, written with the helpers `less` and `exch`, is [sink](/sift-down-sink/) in Sedgewick and Wayne. The two compute the same thing.
- **Weak heaps.** A [weak heap](/weak-heap/) relaxes the order so that the sift-down of heapsort needs only about one comparison per level.

## When to use it

Use sift-down each time the item at a node may be larger than one of its children: after the root is replaced in extract-min or in a `replace` operation, after a key grows in a min-heap, and at each internal node when you build a heap from an array. When a key moves toward the root, use [sift-up](/sift-up/) instead. To delete an item at index $i$, move the last item to $i$ and call both: at most one of them moves it.

## Pitfalls

- **Swapping with the wrong child.** Line L5 must pick the *smaller* child. A swap with the larger child puts a large item above its smaller sibling and breaks the heap.
- **A missing right child.** The test $l + 1 < n$ of line L5 is needed. Without it, the code reads a cell past the heap, which in heapsort holds an item that is already sorted.
- **The heap size in heapsort.** The call must use the current heap size $n$, not the length of the array. Else the sorted tail is pulled back into the heap.
- **Calling it on a node whose subtrees are not heaps.** SIFT-DOWN fixes one node. To build a heap, the calls must go from the last internal node to the root, so that both subtrees are heaps when a node is sifted. A loop from the root down does not give a heap.
- **Strict test for the stop.** Line L6 stops when $A[i] \le A[c]$. A test $A[i] < A[c]$ still gives a heap but swaps equal keys for no gain.

## Implementations

## History

Robert W. Floyd published Treesort 3 in 1964, as Algorithm 245 of the Communications of the ACM. It improved the heapsort of J. W. J. Williams from the same year. It builds the heap by sifting down each internal node from the last to the first, which takes linear time, and Floyd's paper calls this step `siftup`, in the sense of moving larger items up. Knuth's Algorithm H in Section 5.2.3 gives the same loop. Wegener analyzed the bottom-up form in 1993. The names vary: CLRS writes MAX-HEAPIFY, Sedgewick and Wayne write `sink`, and other texts say percolate-down, heapify-down or bubble-down.

## References
