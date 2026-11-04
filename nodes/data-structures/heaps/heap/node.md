---
tag: 45YARP
kind: definition
slug: heap
name: Heap
aliases:
- heap-ordered tree
area: data-structures/heaps
level: intro
summary: Tree-based structure whose nodes satisfy the heap property; the family behind most priority queues.
prereqs: [heap-property, rooted-tree]
see_also: [priority-queue, binary-heap, d-ary-heap, binomial-heap, fibonacci-heap, pairing-heap, heapsort, meldable-priority-queue]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6 (Heapsort), Sections 6.1 and 6.5
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), heaps and Algorithm H, and the part on priority queues and merging in the same section
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues)
  - paper: "J. W. J. Williams, Algorithm 232: Heapsort, Communications of the ACM 7(6), 1964"
    locator: pages 347 to 348
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Section 1 (the operations of a heap and their use in network algorithms)
---

A heap is a data structure that stores a set of items with keys in one or more [heap-ordered](/heap-property/) trees, so that a smallest key (or a largest key) is always at a root. It is the usual way to implement a [priority queue](/priority-queue/): insert an item, find the minimum, delete the minimum, and in many heaps also decrease a key and meld two heaps. The many kinds of heap differ in the shape rule of their trees and in how they link and cut trees, and so in the cost of each operation. The first heap was the array-based [binary heap](/binary-heap/) of Williams (1964).

## Definition

Let $(K, \le)$ be a set with a [total order](/total-order/). A *min-heap* over $K$ is a finite [forest](/rooted-tree/) $F$ of rooted trees, a key $\mathrm{key}(v) \in K$ at each node $v$, and an item at each node, such that

1. **(order)** each tree of $F$ has the min-heap property: $\mathrm{key}(p(v)) \le \mathrm{key}(v)$ for each node $v$ with a parent $p(v)$;
2. **(shape)** $F$ meets the shape rule of the kind of heap, for example "one [complete binary tree](/complete-binary-tree/)" for a binary heap, or "at most one binomial tree of each order" for a [binomial heap](/binomial-heap/);
3. **(access)** the structure can reach the root of each tree, and a pointer or an index names a root of minimum key, or such a root can be found among the roots.

The items of the heap are the items of the nodes, so the heap stores a multiset of keys of size $n = |V(F)|$. A *max-heap* is the same with $\ge$ in place of $\le$.

By the global form of the [heap property](/heap-property/), each key is at least the key of the root of its tree. So

$$\min_{v \in V(F)} \mathrm{key}(v) = \min_{r \text{ a root of } F} \mathrm{key}(r),$$

and a minimum is found among the roots alone. With one tree, it is the root. This identity is the reason that heaps work: the minimum is cheap to find, and the rest of the set is only partly ordered, which is cheap to keep.

**The operations.** A heap implements the [priority queue](/priority-queue/) type. The common operations of a min-heap $H$ are:

| operation | effect |
|---|---|
| `make-heap()` | return an empty heap |
| `insert(H, x, k)` | add the item $x$ with key $k$ |
| `find-min(H)` | return an item of minimum key |
| `delete-min(H)` | remove and return an item of minimum key |
| `decrease-key(H, x, k)` | lower the key of the item $x$ to $k \le \mathrm{key}(x)$, see [decrease-key](/decrease-key/) |
| `delete(H, x)` | remove the item $x$ |
| `meld(H_1, H_2)` | return one heap with the items of both, see [meldable priority queue](/meldable-priority-queue/) |

For `decrease-key` and `delete`, the caller must name the item by a *handle*: a pointer to its node, or an index into a position map, as in an [indexed priority queue](/indexed-priority-queue/). A heap cannot search for a key fast, because the heap property gives no order between two subtrees.

**The costs of the main kinds.** The table gives the bounds for a heap of $n$ items. "am." marks an amortized bound; the others are worst-case bounds.

| heap | insert | find-min | delete-min | decrease-key | meld |
|---|---|---|---|---|---|
| [binary heap](/binary-heap/) | $O(\log n)$ | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| [d-ary heap](/d-ary-heap/) | $O(\log_d n)$ | $O(1)$ | $O(d \log_d n)$ | $O(\log_d n)$ | $O(n)$ |
| [binomial heap](/binomial-heap/) | $O(\log n)$, $O(1)$ am. | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ |
| [Fibonacci heap](/fibonacci-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ am. | $O(1)$ am. | $O(1)$ |
| [hollow heap](/hollow-heap/) | $O(1)$ | $O(1)$ | $O(\log n)$ am. | $O(1)$ | $O(1)$ |
| [Brodal queue](/brodal-queue/) | $O(1)$ | $O(1)$ | $O(\log n)$ | $O(1)$ | $O(1)$ |

The binomial heap reaches $O(1)$ for find-min when it keeps a pointer to the minimum root. The [leftist heap](/leftist-heap/), the [pairing heap](/pairing-heap/) and the [skew heap](/skew-heap/) meld in $O(\log n)$ time, worst case or amortized, with simple code; their pages give the exact results.

**A lower bound.** In the [comparison model](/comparison-model/), $n$ inserts followed by $n$ delete-mins output the items in sorted order. Sorting needs $\lceil \lg(n!) \rceil = n \lg n - O(n)$ comparisons in the worst case (see the [comparison sort lower bound](/comparison-sort-lower-bound/)). So, for each comparison-based heap, the cost of one insert plus one delete-min is $\Omega(\log n)$, worst case or amortized. A heap can make insert, find-min, meld and decrease-key $O(1)$, but then delete-min is $\Omega(\log n)$.

## Examples and non-examples

- **A binary min-heap.** The array $[1, 3, 2, 7, 4, 5]$ stores one complete binary tree: the root 1 has the children 3 and 2, the node 3 has the children 7 and 4, and the node 2 has the child 5. The minimum is at index 1.
- **A binomial heap of 6 items.** Since $6 = 110_2$, the forest has one binomial tree of order 1 (2 nodes) and one of order 2 (4 nodes). With the keys $8, 12$ in the first tree and $3, 5, 9, 4$ in the second (root 3, children 5 and 4, and 9 under 5), the minimum 3 is the smaller of the two roots 8 and 3.
- **A Fibonacci heap after some inserts.** After the inserts of 7, 2 and 9 and no other operation, a Fibonacci heap is three trees with one node each, and the minimum pointer is at 2. Its shape rule is only a bound on the degrees, so a heap of three single nodes is legal.
- **Non-example, a sorted list.** A sorted linked list has the minimum at its head and is heap-ordered as a path. It is a valid heap with the shape rule "a path", but insert then costs $\Theta(n)$. It is a priority queue, and it is seldom called a heap.
- **Non-example, a binary search tree.** A [binary search tree](/binary-search-tree/) can find the minimum in $O(h)$, but it is not heap-ordered: the root is in the middle of the keys.
- **Non-example, the memory heap.** The "heap" of a language runtime, from which `malloc` and `new` take memory, is a different use of the word. It is not ordered by keys, and it has no relation to this definition.

## Related definitions

- The [heap property](/heap-property/) is the order rule of item 1.
- The [priority queue](/priority-queue/) is the abstract type that a heap implements, and the [meldable priority queue](/meldable-priority-queue/) adds `meld`. The [double-ended priority queue](/double-ended-priority-queue/) adds `delete-max`, and the [min-max heap](/min-max-heap/), the [deap](/deap/) and the [interval heap](/interval-heap/) implement it.
- [Heap construction](/heap-construction/) is the problem of building a heap from $n$ items at once. [Floyd's method](/floyd-heap-construction/) does it in $O(n)$ time for a binary heap.
- [Heapsort](/heapsort/) sorts by building a binary max-heap and deleting the maximum $n$ times.
- A [bucket queue](/bucket-queue/) and a [radix heap](/radix-heap/) are priority queues for small integer keys. They are not heap-ordered trees, but the literature often lists them with the heaps.

### History

Williams introduced the binary heap in 1964, as the data structure of heapsort, in Algorithm 232 of the Communications of the ACM. Floyd gave the linear-time construction in the same year. Vuillemin defined the binomial queue in 1978, and Fredman and Tarjan defined the Fibonacci heap in their paper of 1987.

## References
