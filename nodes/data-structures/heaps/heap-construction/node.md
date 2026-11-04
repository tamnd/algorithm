---
tag: FPZBHW
kind: problem
slug: heap-construction
name: Heap construction
aliases:
- build-heap
- heapify problem
area: data-structures/heaps
level: intro
summary: Given n keys, arrange them into a valid heap.
model: comparison-model
complexity:
  vars: {n: the number of keys}
  time: {worst: Θ(n)}
prereqs: [heap, heap-property, complete-binary-tree]
see_also: [floyd-heap-construction, heap-construction-by-insertion, binary-heap, heapsort, sorting-problem, decision-tree-model]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.3 (Building a heap), BUILD-MAX-HEAP and its linear bound
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the heap creation phase of Algorithm H and its analysis
  - paper: "Robert W. Floyd, Algorithm 245: Treesort 3, Communications of the ACM 7(12), 1964"
    locator: page 701
  - paper: "Gaston H. Gonnet and J. Ian Munro, Heaps on heaps, SIAM Journal on Computing 15(4), 1986"
    locator: pages 964 to 971 (heap construction with about 1.625n comparisons)
  - paper: "Marek A. Suchenek, Elementary yet precise worst-case analysis of Floyd's heap-construction program, Fundamenta Informaticae 120(1), 2012"
    locator: the main theorem, the exact worst-case comparison count of Floyd's method
---

Heap construction is the problem of arranging $n$ given keys into a [heap](/heap/), most often a [binary heap](/binary-heap/) in an array. It is the first phase of [heapsort](/heapsort/) and the way to start a [priority queue](/priority-queue/) that has its items at the start. [Floyd's method](/floyd-heap-construction/) solves it in $\Theta(n)$ time and with fewer than $2n$ comparisons, so the problem is easier than [sorting](/sorting-problem/), which needs $\Theta(n \log n)$ comparisons. In the [comparison model](/comparison-model/), each method needs more than $1.36n$ comparisons on some input of large size.

## In plain words

You get a pile of numbers and must put them in a list so that each number is at most the two numbers at twice its position and twice its position plus one. A sorted list works, but sorting is more work than needed. The rule only asks each number to be small compared with the few numbers directly below it, not with all later numbers.

You can add the numbers one at a time and let each one climb to its place. That is simple, but each climb can be long. A faster way fixes the list from the bottom up: the bottom half needs no work, the row above it needs at most one step down for each number, and only the few numbers near the top can move far. In total the work is a small multiple of the number of items.

## Definition

**Input.** A sequence $B = (b_1, \ldots, b_n)$ of keys from a set with a [total order](/total-order/) $\le$, with $n \ge 0$.

**Output.** An array $A[1 \ldots n]$ such that

1. $A$ is a permutation of $B$: there is a bijection $\pi$ of $\{1, \ldots, n\}$ with $A[i] = b_{\pi(i)}$ for each $i$;
2. $A$ has the min-heap property of a binary heap: $A[\lfloor i/2 \rfloor] \le A[i]$ for each $i$ with $2 \le i \le n$.

The max-heap version asks for $A[\lfloor i/2 \rfloor] \ge A[i]$. Many outputs are valid for one input: for $n$ distinct keys there are exactly $n!/\prod_{v} s(v)$ valid outputs, where $s(v)$ is the size of the subtree of the node $v$ in the complete binary tree of $n$ nodes (see the [heap property](/heap-property/) page). Any of them is correct.

The *in-place* version asks for $A$ to be built in the array that holds $B$, with $O(1)$ extra cells.

## Variants

- **Max-heap or min-heap.** The same problem with the order reversed.
- **$d$-ary heaps.** The parent of $i$ is $\lfloor (i - 2)/d \rfloor + 1$, as in a [d-ary heap](/d-ary-heap/). Floyd's method works with $d$ comparisons per level and still runs in $O(n)$ time for fixed $d$.
- **Pointer-based heaps.** For a [binomial heap](/binomial-heap/) or a [leftist heap](/leftist-heap/), $n$ inserts or a sequence of pairwise melds take $O(n)$ time. For a [Fibonacci heap](/fibonacci-heap/), $n$ inserts take $O(n)$ time and build a forest of $n$ single nodes.
- **Online construction.** The keys arrive one at a time, and the array must be a heap after each arrival. Then each key must be inserted, see [heap construction by insertion](/heap-construction-by-insertion/).
- **Counting.** Count the valid outputs for $n$ distinct keys. The formula above answers it.

## Examples

- $B = (4, 1, 3, 2, 16, 9, 10, 14, 8, 7)$, max-heap version. Floyd's method gives $[16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$, the result of CLRS Section 6.3, with 14 comparisons and 7 swaps. Inserting the keys one by one in the given order gives $[16, 14, 10, 8, 7, 3, 9, 1, 4, 2]$, another valid max-heap, with 17 comparisons and 9 swaps.
- $B = (5, 3, 8, 1, 9, 2)$, min-heap version. Floyd's method gives $[1, 3, 2, 5, 9, 8]$.
- $B$ sorted in non-decreasing order is already a min-heap, and a correct output is $B$ itself. Floyd's method then does no swap.
- For $n = 3$ and the keys $1, 2, 3$, the valid min-heaps are $[1, 2, 3]$ and $[1, 3, 2]$. The formula gives $3!/(3 \cdot 1 \cdot 1) = 2$.
- For $n = 10$ and distinct keys, there are $10!/1080 = 3360$ valid min-heaps.

## Known algorithms

- [Floyd's heap construction](/floyd-heap-construction/): sift down each internal node from the last to the first. $\Theta(n)$ time in the worst case, at most $2n - 2s_2(n) - e_2(n)$ comparisons and at most $n - s_2(n)$ swaps, where $s_2(n)$ is the number of 1 bits of $n$ and $e_2(n)$ is the exponent of the largest power of 2 that divides $n$. In place.
- [Heap construction by insertion](/heap-construction-by-insertion/): insert the keys one by one with [sift-up](/sift-up/). $\Theta(n \log n)$ time in the worst case, $O(n)$ expected time on a random order. In place and online.
- The method of Gonnet and Munro (1986) builds a binary heap with about $1.625n$ comparisons in the worst case, with a more complex procedure.
- Sorting the keys with any $O(n \log n)$ sort also gives a heap, but it does more work than the problem needs.

## Bounds

**Upper bound.** $O(n)$ time and fewer than $2n$ comparisons, by Floyd's method. The exact worst-case comparison count of Floyd's method, $2n - 2s_2(n) - e_2(n)$, is the result of Suchenek (2012).

**A trivial lower bound.** Each output has a minimum at $A[1]$. Finding the minimum of $n$ keys needs $n - 1$ comparisons in the comparison model, because each key other than the minimum must lose a comparison. So heap construction needs at least $n - 1$ comparisons, and $\Omega(n)$ time. With Floyd's method, the problem is $\Theta(n)$.

**An information lower bound.** In the [decision tree model](/decision-tree-model/), consider a comparison algorithm for $n$ distinct keys. At a leaf of its decision tree, the algorithm outputs a fixed rearrangement $\pi$ of the input positions. Two different inputs that reach the same leaf give two different outputs $\pi(x) \ne \pi(y)$, and both are heaps on the same key set $\{1, \ldots, n\}$. So at most $H(n) = n!/\prod_v s(v)$ inputs reach one leaf, the tree has at least $n!/H(n) = \prod_v s(v)$ leaves, and its depth is at least

$$\left\lceil \lg \prod_{v} s(v) \right\rceil = \left\lceil \sum_{v} \lg s(v) \right\rceil.$$

For $n = 10$ this is $\lceil \lg 1080 \rceil = 11$. For $n = 10^6$ the sum is about $1.3644n$, so each method needs more than $1.36n$ comparisons on some input of this size.

**Compared with sorting.** Sorting needs $\lceil \lg(n!) \rceil = n \lg n - O(n)$ comparisons. So a heap is a much weaker order than a sorted array, and building it is cheaper by a factor of order $\log n$.

## Reductions

- **Heap construction reduces to sorting.** A sorted array is a min-heap, so a sort of cost $T(n)$ solves heap construction in $T(n)$.
- **Sorting reduces to heap construction plus $n$ extract-min operations.** This is [heapsort](/heapsort/). It costs $O(n)$ for the construction and $O(n \log n)$ for the extractions, so a faster heap construction alone cannot beat the sorting bound.
- **Selection of the $k$ smallest keys** reduces to heap construction plus $k$ extract-min operations, in $O(n + k \log n)$ time. See [top-k selection](/top-k-selection/).

## Applications

- The first phase of [heapsort](/heapsort/).
- Starting a priority queue with many items at once, for example the initial frontier of a search, the event list of an [event-driven simulation](/event-driven-simulation/), or the leaves of [Huffman coding](/huffman-coding/).
- [Top-k selection](/top-k-selection/) and the partial sorts of the [k-way merge](/k-way-merge/) of many sorted runs.
- Rebuilding a heap after many changes at once, which is cheaper than as many single updates when the number of changes is a constant fraction of $n$.

## References
