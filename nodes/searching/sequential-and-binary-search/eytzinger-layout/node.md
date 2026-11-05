---
tag: Q8TG36
kind: data-structure
slug: eytzinger-layout
name: Eytzinger layout
aliases:
- BFS-order implicit search tree layout
area: searching/sequential-and-binary-search
level: advanced
summary: Store a sorted array in breadth-first order of its implicit binary search tree to make binary search cache-friendly.
model: comparison-model
complexity:
  vars: {n: the number of items}
  time: {build: Θ(n), search: Θ(log n)}
  space: {total: Θ(n)}
prereqs: [binary-search, complete-binary-tree, lower-bound-query]
see_also: [binary-heap, binary-search-tree, van-emde-boas-layout, b-tree, branchless-binary-search, prefetching, cache-oblivious-model, level-order-traversal]
sources:
  - paper: doi:10.1145/3053370
    title: Paul-Virak Khuong and Pat Morin, Array layouts for comparison-based searching, ACM Journal of Experimental Algorithmics 22 (2017)
    locator: Article 1.3 (the Eytzinger layout, its branch-free search with prefetching, and comparisons with sorted, B-tree and van Emde Boas layouts)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.1 (binary search trees stored implicitly in an array)
---

The Eytzinger layout stores $n$ sorted items in an array in the breadth-first order of a [complete binary tree](/complete-binary-tree/) that is a [binary search tree](/binary-search-tree/) for them. Slot 1 holds the root, the median; slot $k$ has its children in slots $2k$ and $2k + 1$, as in a [binary heap](/binary-heap/); and an in-order walk of the slots gives the sorted order. A search for $x$ starts at slot 1 and steps $k \gets 2k + [B[k] < x]$ until $k > n$, then removes the trailing 1 bits and one more bit of $k$ to get the slot of the [lower bound](/lower-bound-query/). It makes the same $\lfloor \lg(n+1) \rfloor$ or $\lceil \lg(n+1) \rceil$ comparisons as [binary search](/binary-search/), but the first probes of every search are at the start of the array, where they stay in cache, and the descendants of a slot at depth 4 lie in 16 consecutive slots, so one [prefetch](/prefetching/) gets them all. Khuong and Morin found it the fastest of the simple layouts for large arrays in memory.

## In plain words

A plain sorted array keeps the middle item in the middle. Every search looks at it first, then at the item a quarter of the way in or three quarters of the way in, and so on. These first looks are far apart in memory, and each one can cost a slow trip to main memory.

The Eytzinger layout puts the items in the order in which a binary search would meet them: first the middle item, then the two quarter items, then the four eighth items, and so on. The items that all searches look at first now sit together at the front of the array, where the processor keeps them close at hand. Moving to the next item is a simple step: double the position, and add one if you go right.

## The abstract type

A static ordered set, or multiset, of $n$ items from a [total order](/total-order/), with these operations:

- **Build** from a sorted array.
- **Lower bound** of a key $x$: the first item $\ge x$, or NONE, and its rank $\ell$, the number of items $< x$.
- **Find**: the rank of the first copy of $x$, or NIL.
- **Iterate** in sorted order.

The set does not change after the build. To insert or delete, build again, or use a [B-tree](/b-tree/).

## Representation

An array $B[1 \ldots n]$; slot 0 is unused or holds padding. The implicit tree has root 1, and slot $k$ has the left child $2k$ and the right child $2k + 1$ when these are at most $n$. Its parent is $\lfloor k/2 \rfloor$. Because the slots are $1, \ldots, n$ with no gaps, the tree is a complete binary tree: all levels are full except the last, which is filled from the left.

**Invariant.** The in-order walk of the tree (left subtree, node, right subtree) visits the slots in an order $k_0, k_1, \ldots, k_{n-1}$ with $B[k_0] \le B[k_1] \le \cdots \le B[k_{n-1}]$. The sorted rank of slot $k$ is its position in this walk. An optional array $R[1 \ldots n]$ stores these ranks, to turn a slot into an index of the sorted order.

The bits of a slot number are the path to it: after the leading 1, a 0 means "go left" and a 1 means "go right".

## Operations

```pseudo id=main
EYTZINGER-BUILD(A)                 ▷ A[0 .. n − 1] sorted
L1  i ← 0
L2  FILL(1)
L3  return B
FILL(k)                            ▷ in-order walk of the subtree at slot k
L4  if k ≤ n then
L5      FILL(2k)
L6      B[k] ← A[i], R[k] ← i, i ← i + 1
L7      FILL(2k + 1)
EYTZINGER-LOWER-BOUND(B, x)        ▷ the slot of the first item ≥ x, or 0
L8  k ← 1
L9  while k ≤ n do
L10     k ← 2k + [B[k] < x]       ▷ [true] = 1, [false] = 0
L11 k ← k >> (t + 1)               ▷ t is the number of trailing 1 bits of k
L12 return k
```

Lines L1 to L7 copy the sorted items into the slots in in-order, so the invariant holds by construction. The recursion depth is the height of the tree, $\lfloor \lg n \rfloor + 1$; the implementation uses an explicit stack.

Lines L8 to L10 walk down from the root, left when $B[k] \ge x$ and right when $B[k] < x$, until $k$ leaves the tree. The last node where the walk went left holds the lower bound. The walk wrote one bit per step into $k$, so that node is $k$ with its trailing 1 bits removed (the steps right after it) and then the 0 bit of the step left. Line L11 does this in one shift. If the walk never went left, $k$ is all 1 bits and the shift gives 0: every item is less than $x$.

The rank of the lower bound is $R[k]$, or $n$ when $k = 0$. **Find** tests $k \ne 0$ and $B[k] = x$. In code, the shift of line L11 is `k >> (ffs(~k))` in C, or `k >> (k ^ (k + 1)).bit_length()` in Python.

## Example

The sorted array $A = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]$ has $n = 10$. The build gives:

| slot $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $B[k]$ | 14 | 8 | 18 | 4 | 12 | 16 | 20 | 2 | 6 | 10 |
| rank $R[k]$ | 6 | 3 | 8 | 1 | 5 | 7 | 9 | 0 | 2 | 4 |

The root is 14, not the middle item 10 or 12, because the last level is filled from the left: the left subtree of the root has 6 nodes and the right one has 3.

Search for $x = 13$:

| step | $k$ | $B[k]$ | $B[k] < 13$ | new $k$ |
|---|---|---|---|---|
| 1 | 1 | 14 | false | 2 |
| 2 | 2 | 8 | true | 5 |
| 3 | 5 | 12 | true | 11 |

Now $k = 11 = 1011_2 > n$. It has $t = 2$ trailing 1 bits, so line L11 gives $1011_2 >> 3 = 1$. Slot 1 holds 14, with rank 6: the lower bound of 13 is 14 at sorted index 6. For $x = 21$ the walk goes right at 14, 18 and 20 and ends at $k = 15 = 1111_2$, which gives 0: all items are less than 21, and the rank is $n = 10$. For $x = 1$ the walk goes left four times, to $k = 16 = 10000_2$, and line L11 gives slot 8, which holds 2 with rank 0.

## Correctness

Each node $k_t$ on the walk with $B[k_t] < x$ comes, in in-order, after its left subtree, and so do all items there, which are therefore $< x$ too. Each node with $B[k_t] \ge x$ comes before its right subtree, which is therefore $\ge x$. Every node is on the walk or in the subtree on the side the walk did not take. So the items $\ge x$ are the left-turn nodes and their right subtrees, and the first of them in in-order is the last left-turn node, since every later part of the walk lies in its left subtree. The bit argument of line L11 identifies that node. The full proof is below.

## Complexity

- **Build.** Each slot is filled once: $\Theta(n)$ time.
- **Search.** The walk visits one node per level and stops below a leaf. The tree has $n$ nodes and is complete, so the external positions are at depth $\lfloor \lg(n+1) \rfloor$ or $\lceil \lg(n+1) \rceil$, and the walk makes that many comparisons: the same as the best binary search, and $\Theta(\log n)$. Line L11 is $O(1)$ with a bit instruction.
- **Space.** $n + 1$ slots, and $n$ more for the rank array if the sorted indices are needed. The layout can replace the sorted array, so no extra space is needed when only the items matter.
- **Memory traffic.** With $w$ items per cache line, $w$ a power of 2, the descendants of a slot $k$ that lie $\lg w$ levels below it occupy the slots $wk, \ldots, wk + w - 1$, which is one cache line when the array is aligned. A search can prefetch the line of slot $wk$ when it is at slot $k$, about $\lg w$ steps before it needs it; with 4-byte keys and 64-byte lines, $w = 16$. The first levels of the tree are read by every search and stay in cache. In the external-memory model the search still reads $\Theta(\log(n/B))$ blocks, not the $\Theta(\log_B n)$ of a B-tree, but each block read is predicted early.

## Variants

- **Prefetching search.** Add a prefetch of $B[16k]$ (or $B[wk]$) at the top of the loop. Khuong and Morin report that this makes the layout faster than a plain sorted array for large $n$.
- **Branchless search.** Line L10 is already free of data-dependent branches, so the walk is a [branchless binary search](/branchless-binary-search/) with a fixed number of passes for each depth.
- **0-based slots.** Use children $2k + 1$ and $2k + 2$. The shift of line L11 then works on $k + 1$.
- **B-tree layout.** Group $w$ keys per node and store the nodes in breadth-first order; each step reads one cache line and makes $\lg(w+1)$ levels of progress. This is the static [B-tree](/b-tree/), also called an S-tree.
- **[Van Emde Boas layout](/van-emde-boas-layout/).** Store the top half of the levels, then each bottom subtree, recursively. It is [cache-oblivious](/cache-oblivious-model/): $O(\log_B n)$ block reads for every block size $B$.
- **Padding to a full tree.** Pad $n$ up to $2^h - 1$ with $+\infty$ so that every search makes exactly $h$ steps.

## When to use it

Use the Eytzinger layout for a static sorted set in memory that is searched very often and is larger than the processor cache, such as a sorted index of millions of numbers. It keeps the code of binary search and makes each search faster through better use of caches and prefetching. For small sets that fit in cache, a plain sorted array with a branchless search is as good and keeps the sorted order for range scans. For sets that change, or for data on disk, use a [B-tree](/b-tree/).

## Pitfalls

- **Forgetting that the order is not sorted.** A range scan over the array does not give the items in order. Iterate by an in-order walk, or keep the rank array.
- **Off by one in the slots.** The formulas $2k$, $2k + 1$ and the shift of line L11 need 1-based slots. With 0-based slots, use $2k + 1$, $2k + 2$ and apply the shift to $k + 1$.
- **Shift for $k = 0$ result.** When every item is less than $x$ the result is 0, not a slot. Test it before reading $B[k]$.
- **Building in the wrong order.** Copying $A$ in breadth-first order of the indices, $B[k] = A[k - 1]$, gives a heap order, not a search tree. The build must follow the in-order walk.
- **Alignment.** The cache-line claim needs slot $wk$ at the start of a line. Allocate the array aligned, and place slot 0, the unused one, so that slot $w$ starts a line.

## Implementations

## History

The numbering, with a person at 1 and the parents of person $k$ at $2k$ and $2k + 1$, is the genealogical system named after Michael Eytzinger, who used it in the sixteenth century. The same numbering stores a [binary heap](/binary-heap/) in an array. As a layout for searching sorted data in memory it was studied in experiments on array layouts, and Khuong and Morin showed in 2017 that, with prefetching and a branch-free loop, it beats both the sorted order and the B-tree and van Emde Boas layouts on large arrays.

## References
