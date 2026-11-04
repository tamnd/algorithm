---
tag: CSPR1S
kind: algorithm
slug: heapsort
name: Heapsort
aliases:
- heap sort
area: sorting/comparison-sorts
level: core
summary: Builds a max-heap and repeatedly extracts the maximum; Theta(n log n) worst case and in place.
solves: [sorting-problem]
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
history:
  year: 1964
  people: [J. W. J. Williams, Robert W. Floyd]
  note: Williams published heapsort in 1964 as Algorithm 232 of the Communications of the ACM. Floyd published the linear-time heap construction in the same year as Algorithm 245, Treesort 3.
prereqs: [binary-heap, heap-property, sift-down, loop-invariant, asymptotic-notation]
see_also: [floyd-heap-construction, priority-queue, selection-sort, introsort, smoothsort, weak-heapsort, merge-sort, quicksort]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Sections 6.1 to 6.4 (heaps, MAX-HEAPIFY, BUILD-MAX-HEAP and its O(n) bound, HEAPSORT)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3, Sorting by selection (Algorithm H, heapsort, and its analysis)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4, Priority queues (heapsort, sink-based heap construction and the bound of fewer than 2N lg N + 2N compares)
  - paper: "J. W. J. Williams, Algorithm 232: Heapsort, Communications of the ACM 7(6) (1964)"
    locator: pp. 347 to 348
  - paper: "Robert W. Floyd, Algorithm 245: Treesort 3, Communications of the ACM 7(12) (1964)"
    locator: p. 701
  - paper: "Russel Schaffer and Robert Sedgewick, The analysis of heapsort, Journal of Algorithms 15(1) (1993)"
    locator: pp. 76 to 100 (the best case and the average case of heapsort)
  - paper: "Ingo Wegener, Bottom-up heapsort, a new variant of heapsort beating, on an average, quicksort (if n is not very small), Theoretical Computer Science 118(1) (1993)"
    locator: pp. 81 to 98
---

Heapsort sorts an array in place by turning it into a max-[heap](/binary-heap/) and then taking the maximum out $n - 1$ times. It solves the [sorting problem](/sorting-problem/) with $O(n \log n)$ comparisons in the worst case and $O(1)$ extra space, which no other simple sort achieves together. It is not stable, and its scattered memory access makes it slower in practice than a good [quicksort](/quicksort/). [Introsort](/introsort/) uses it as a fallback that guarantees the $O(n \log n)$ bound.

## In plain words

Think of the array as a family tree. The item at place 0 is the root, and the item at place $i$ has two children, at places $2i + 1$ and $2i + 2$. The array is a *heap* when each parent is at least as large as its children. Then the largest item is at the root.

Heapsort first rearranges the array into a heap. Then it swaps the root, the largest item, with the last item of the heap. The largest item is now at its final place at the end, and the heap is one item shorter. The new root may be too small, so it sinks down: it swaps with its larger child until both children are smaller. Then the heap is repaired, and the step repeats until one item is left.

## The problem

The input is an array $A[0 \ldots n-1]$ of items with a total order. The output is the same array, with its items in non-decreasing order. This is the [sorting problem](/sorting-problem/). The algorithm changes the array in place.

## The algorithm

In a heap of size $m$, stored in $A[0 \ldots m-1]$, the children of index $i$ are $2i + 1$ and $2i + 2$ when they are less than $m$. The [heap property](/heap-property/) says that $A[\lfloor (c-1)/2 \rfloor] \ge A[c]$ for each $c$ with $1 \le c < m$.

```pseudo id=main
HEAPSORT(A)                                ▷ n = |A|
L1  for i ← ⌊n/2⌋ − 1 downto 0 do SIFT-DOWN(A, i, n)     ▷ build the max-heap
L2  for end ← n − 1 downto 1 do
L3      exchange A[0] and A[end]           ▷ the maximum goes to its place
L4      SIFT-DOWN(A, 0, end)               ▷ repair the heap A[0 .. end − 1]

SIFT-DOWN(A, i, m)                         ▷ the subtrees of the children of i are heaps
L5  while 2i + 1 < m do
L6      c ← 2i + 1                         ▷ the left child
L7      if c + 1 < m and A[c + 1] > A[c] then c ← c + 1
L8      if A[i] ≥ A[c] then return
L9      exchange A[i] and A[c]
L10     i ← c
```

Line L1 is [Floyd's heap construction](/floyd-heap-construction/). The indices $\lfloor n/2 \rfloor$ to $n - 1$ are leaves, which are heaps of one item. The loop calls [SIFT-DOWN](/sift-down/) on each inner node, from the last one back to the root. When SIFT-DOWN runs on $i$, the subtrees of both children of $i$ are already heaps. Lines L5 to L10 move the item at $i$ down along the path of larger children until it is at least as large as each child. Lines L2 to L4 are the selection phase: each step puts the largest item of the heap at the end of the heap, shrinks the heap by one, and repairs it.

## Example

Sort $A = [6, 5, 3, 1, 8, 7, 2, 4]$, with $n = 8$. The build phase calls SIFT-DOWN for $i = 3, 2, 1, 0$.

| step | the array after the step |
|---|---|
| start | 6 5 3 1 8 7 2 4 |
| sift $i = 3$ | 6 5 3 4 8 7 2 1 |
| sift $i = 2$ | 6 5 7 4 8 3 2 1 |
| sift $i = 1$ | 6 8 7 4 5 3 2 1 |
| sift $i = 0$ | 8 6 7 4 5 3 2 1 |

Now $A$ is a max-heap. In the last row, the item 6 moved from the root to index 1, because 8 is the larger child of the root, and then it stopped, because its children 4 and 5 are smaller. The selection phase follows. The bar separates the heap from the sorted part.

| end | the array after lines L3 and L4 |
|---|---|
| 7 | 7 6 3 4 5 1 2 \| 8 |
| 6 | 6 5 3 4 2 1 \| 7 8 |
| 5 | 5 4 3 1 2 \| 6 7 8 |
| 4 | 4 2 3 1 \| 5 6 7 8 |
| 3 | 3 2 1 \| 4 5 6 7 8 |
| 2 | 2 1 \| 3 4 5 6 7 8 |
| 1 | 1 \| 2 3 4 5 6 7 8 |

The run makes 9 comparisons in the build phase and 27 in total. The lower bound for 8 items is $\lceil \lg(8!) \rceil = 16$.

## Correctness

SIFT-DOWN keeps this [loop invariant](/loop-invariant/): each parent and child pair in $A[0 \ldots m-1]$ satisfies the heap order, except perhaps the pairs of $i$ with its children, and the parent of $i$ is at least each child of $i$. When the loop stops, $i$ has no larger child, so $A[0 \ldots m-1]$ is a heap. HEAPSORT keeps this invariant for the loop of line L2:

> Before the step for $end$, $A[0 \ldots end]$ is a max-heap, $A[end+1 \ldots n-1]$ holds the $n - 1 - end$ largest items in sorted order, and each item of the heap is at most each item of the sorted part.

Line L3 moves the maximum of the heap to place $end$, and line L4 repairs the shorter heap. When the loop stops, $end = 0$, so $A[1 \ldots n-1]$ is sorted and $A[0]$ is a smallest item. The full proof is below.

## Complexity

**Build phase.** A node at height $h$ (the length of the longest path from it down to a leaf) costs at most $h$ steps of the loop of line L5, and each step makes at most 2 comparisons. The sum of the heights of all nodes of a heap of $n$ items is $n - \nu(n)$, where $\nu(n)$ is the number of 1 bits of $n$. So the build phase makes at most $2(n - \nu(n)) < 2n$ comparisons and takes $\Theta(n)$ time. The simpler bound uses at most $\lceil n/2^{h+1} \rceil$ nodes of height $h$, and $\sum_{h \ge 0} h/2^{h} = 2$.

**Selection phase.** The heap in line L4 has $end \le n - 1$ items, so its height is $\lfloor \lg end \rfloor$. Each call of SIFT-DOWN makes at most $2 \lfloor \lg end \rfloor$ comparisons. The sum over $end = 1, \ldots, n-1$ is at most $2 n \lg n$.

- **Worst case.** At most $2 n \lg n + 2n$ comparisons, so $O(n \log n)$ time. The [comparison sort lower bound](/comparison-sort-lower-bound/) makes it $\Theta(n \log n)$.
- **Average case.** On a random permutation, the root item sinks almost to the bottom in most steps, because it came from the bottom. The number of comparisons is about $2 n \lg n$. For $n = 10{,}000$ the mean over five random inputs was about 235,400, against $2 n \lg n \approx 265{,}800$.
- **Best case.** On distinct keys the time is also $\Theta(n \log n)$ in the best case (Schaffer and Sedgewick, 1993). If all keys are equal, line L8 returns at once in each call, and the time is $\Theta(n)$.
- **Space.** $\Theta(1)$ extra: a few indices. SIFT-DOWN is a loop, so there is no recursion stack.

For small $n$, the greatest number of comparisons over all $n!$ inputs is 7 for $n = 4$, 12 for $n = 5$ and 29 for $n = 8$, against the lower bounds 5, 7 and 16. Heapsort is far from optimal in comparisons by a constant factor of about 2.

## Properties

- **Not stable.** The exchange of line L3 moves an item over all the items of the heap. For the input $[1_a, 1_b]$ the output is $[1_b, 1_a]$.
- **In place.** It uses $O(1)$ extra space. It is an [in-place algorithm](/in-place-algorithm/) in the strict sense.
- **Not adaptive.** A sorted input still costs $\Theta(n \log n)$. [Smoothsort](/smoothsort/) is a heapsort variant that takes $O(n)$ time on sorted input.
- **Not online.** The build phase needs all items.
- **Poor locality.** The children of $i$ are at $2i + 1$ and $2i + 2$, so for large heaps each level of SIFT-DOWN touches a different part of memory. This is the main reason that heapsort is slower than quicksort and merge sort in practice.

## Variants and improvements

- **Bottom-up heapsort.** In SIFT-DOWN, first follow the path of larger children down to a leaf, with one comparison per level. Then climb back up to the place of the item. This saves most of the comparisons of line L8, because the item usually belongs near the bottom. Wegener (1993) proved a worst case of at most $1.5 n \lg n + O(n)$ comparisons.
- **[Weak-heapsort](/weak-heapsort/).** Use a weak heap, which needs one extra bit per item. It makes $n \lg n + O(n)$ comparisons in the worst case, close to the lower bound.
- **[d-ary heaps](/d-ary-heap/).** Use $d$ children per node. The tree is lower, so there are fewer levels and fewer cache misses, at the cost of $d$ comparisons per level.
- **[Smoothsort](/smoothsort/).** Use a forest of Leonardo heaps. It is adaptive, with $O(n)$ time on sorted input, and still $O(n \log n)$ in the worst case.
- **[Introsort](/introsort/).** Run quicksort, and switch to heapsort when the recursion is too deep. This gives the speed of quicksort and the worst case of heapsort.
- **Partial sort.** Stop the loop of line L2 after $k$ steps. The $k$ largest items are then sorted at the end, in $O(n + k \log n)$ time. See [heap select](/heap-select/).

## When to use it

Use heapsort when you need a worst case of $O(n \log n)$ and $O(1)$ extra space, and stability is not necessary, for example in an embedded system or in a kernel with a fixed memory budget. It is also the standard fallback inside introsort. Use quicksort or introsort when the average speed matters, [merge sort](/merge-sort/) or [Timsort](/timsort/) when the sort must be stable, and [insertion sort](/insertion-sort/) for small arrays.

## Pitfalls

- **Building the heap from the top.** A loop $i \leftarrow 0$ to $\lfloor n/2 \rfloor - 1$ in line L1 does not build a heap, because SIFT-DOWN needs both subtrees to be heaps already. The loop must go down from $\lfloor n/2 \rfloor - 1$ to 0.
- **The wrong heap size.** Line L4 must pass $end$, not $end + 1$ or $n$. With $end + 1$, SIFT-DOWN can pull the item that was just placed at $A[end]$ back into the heap.
- **Forgetting the right child bound.** Line L7 tests $c + 1 < m$ before it reads $A[c + 1]$. Without the test, the last parent of an even-sized heap reads an item outside the heap.
- **Strict test in line L8.** With $A[i] > A[c]$ instead of $\ge$, SIFT-DOWN still works, but it swaps equal items down for no gain. On all-equal keys the time becomes $\Theta(n \log n)$ instead of $\Theta(n)$.
- **One-based formulas in zero-based code.** The children $2i$ and $2i + 1$ are correct when the root is at index 1. With the root at index 0 they are $2i + 1$ and $2i + 2$.

## Implementations

## History

J. W. J. Williams published heapsort as Algorithm 232 in the Communications of the ACM in June 1964, together with the heap as a data structure for a [priority queue](/priority-queue/). His version built the heap by inserting the items one by one, in $O(n \log n)$ time. Robert W. Floyd published Algorithm 245, Treesort 3, in December 1964. It builds the heap from the bottom up in $O(n)$ time, as in line L1, and this is the form of heapsort in the textbooks.

## References
