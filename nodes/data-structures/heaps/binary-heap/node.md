---
tag: 1QKQ6A
kind: data-structure
slug: binary-heap
name: Binary heap
aliases:
- array heap
- implicit binary heap
- min-heap
- max-heap
area: data-structures/heaps
level: intro
summary: Complete binary tree stored in an array that supports insert and extract-min in O(log n).
implements: [priority-queue]
model: comparison-model
prereqs: [heap, heap-property, complete-binary-tree, priority-queue]
see_also: [d-ary-heap, floyd-heap-construction, heapsort, indexed-priority-queue, binomial-heap, fibonacci-heap, sift-up, sift-down]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Sections 6.1 (Heaps), 6.2 (Maintaining the heap property), 6.3 (Building a heap) and 6.5 (Priority queues)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues), Algorithm 2.6 (heap priority queue), swim and sink
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), heaps, Algorithm H and the history of heapsort
  - paper: "J. W. J. Williams, Algorithm 232: Heapsort, Communications of the ACM 7(6), 1964"
    locator: pages 347 to 348
  - paper: "Robert W. Floyd, Algorithm 245: Treesort 3, Communications of the ACM 7(12), 1964"
    locator: page 701
---

A binary heap is a [complete binary tree](/complete-binary-tree/) that is stored in an array, level by level, and that has the [heap property](/heap-property/): each key is at most the keys of its children (a min-heap) or at least them (a max-heap). It implements the [priority queue](/priority-queue/) with insert, extract-min and decrease-key in $O(\log n)$ worst-case time, find-min in $O(1)$, and build in $O(n)$. It needs no pointers: the parent of index $i$ is $\lfloor i/2 \rfloor$, and its children are $2i$ and $2i + 1$. It is the heap of [heapsort](/heapsort/), of the priority queues of most standard libraries, and of the usual code of [Dijkstra's algorithm](/dijkstra/).

## In plain words

Think of a company chart where each boss earns less than each person directly under them. Then the top person earns the least. In a binary heap, each person has at most two people under them, and each row of the chart is full before the next row starts.

Because the rows are full, the chart fits in a plain list, row after row. To find the people under a person, double their position.

To add a person, put them at the end of the last row and let them move up past each boss who earns more. To remove the top person, move the last person to the top and let them move down past the cheaper of their two helpers, until both helpers earn more. Each move goes one row, and there are few rows: about as many as the times you can halve the list.

## The abstract type

A binary heap implements the [priority queue](/priority-queue/) over keys with a [total order](/total-order/): `insert(H, k)`, `find-min(H)`, `extract-min(H)`, `decrease-key(H, i, k)` and `build(H, B)`. The handle of `decrease-key` is the index $i$ of the key in the array; code that must find a key by an item name adds a position map, as in an [indexed priority queue](/indexed-priority-queue/). The structure compares keys only, so its bounds hold in the [comparison model](/comparison-model/). A max-heap is the same with each comparison reversed. It gives `extract-max` and `increase-key`, see [heap extract-max](/heap-extract-max/) and [heap increase-key](/heap-increase-key/).

## Representation

The heap $H$ has an array $A[1 \ldots N]$ and a size $H.n$ with $0 \le H.n \le N$. The keys are $A[1 \ldots H.n]$. The tree is implicit:

$$\mathrm{parent}(i) = \lfloor i/2 \rfloor, \qquad \mathrm{left}(i) = 2i, \qquad \mathrm{right}(i) = 2i + 1,$$

and a child index larger than $H.n$ means that the child does not exist. So the nodes $1$ to $H.n$ fill the levels of a complete binary tree from the top, each level from the left. Level $d$ holds the indices $2^d$ to $2^{d+1} - 1$.

**Invariant (H).** For each $i$ with $2 \le i \le H.n$: $A[\lfloor i/2 \rfloor] \le A[i]$.

By the [heap property](/heap-property/), (H) puts a minimum key at $A[1]$. Some facts about the shape, for $n = H.n \ge 1$:

- The height is $\lfloor \lg n \rfloor$. The deepest index $n$ is on level $\lfloor \lg n \rfloor$, because $2^{\lfloor \lg n \rfloor} \le n < 2^{\lfloor \lg n \rfloor + 1}$.
- The leaves are the indices $\lfloor n/2 \rfloor + 1$ to $n$, since $i$ has a child exactly when $2i \le n$.
- The node $i$ has height $\max\{h : 2^h i \le n\}$, because its leftmost descendant at depth $h$ below it is $2^h i$. So exactly $\lfloor n/2^h \rfloor$ nodes have height at least $h$.

When the array is full, an implementation doubles it, as a [dynamic array](/dynamic-array/) does. This makes the cost of insert amortized; with a fixed capacity $N$ it is worst case.

## Operations

```pseudo id=main
SIFT-UP(A, i)                                 ▷ move A[i] up to its place
L1  while i > 1 and A[⌊i/2⌋] > A[i] do
L2      swap A[i] and A[⌊i/2⌋]
L3      i ← ⌊i/2⌋

SIFT-DOWN(A, n, i)                            ▷ move A[i] down to its place in A[1 .. n]
L4  while true do
L5      m ← i
L6      if 2i ≤ n and A[2i] < A[m] then m ← 2i
L7      if 2i + 1 ≤ n and A[2i + 1] < A[m] then m ← 2i + 1
L8      if m = i then return
L9      swap A[i] and A[m]
L10     i ← m

INSERT(H, k)
L11 H.n ← H.n + 1
L12 A[H.n] ← k
L13 SIFT-UP(A, H.n)

FIND-MIN(H)
L14 if H.n = 0 then error "heap underflow"
L15 return A[1]

EXTRACT-MIN(H)
L16 if H.n = 0 then error "heap underflow"
L17 min ← A[1]
L18 A[1] ← A[H.n]
L19 H.n ← H.n − 1
L20 SIFT-DOWN(A, H.n, 1)
L21 return min

DECREASE-KEY(H, i, k)                         ▷ 1 ≤ i ≤ H.n
L22 if k > A[i] then error "new key is larger than the current key"
L23 A[i] ← k
L24 SIFT-UP(A, i)

BUILD(H, B[1 .. n])
L25 A[1 .. n] ← B[1 .. n]; H.n ← n
L26 for i ← ⌊n/2⌋ downto 1 do SIFT-DOWN(A, n, i)
```

**Sift-up** (lines L1 to L3) repairs a key that may be too small for its place. While the key is smaller than its parent, it swaps with the parent. Each step moves one level up, so it does at most $\lfloor \lg i \rfloor$ swaps and as many comparisons plus one. The page [sift-up](/sift-up/) has more on it.

**Sift-down** (lines L4 to L10) repairs a key that may be too large for its place. It finds the smallest of the key and its children (lines L6 and L7, two comparisons). If the key is the smallest, it stops; else it swaps with that child and goes on from there. It does at most $\lfloor \lg(n/i) \rfloor$ swaps and at most $2\lfloor \lg(n/i) \rfloor + 2$ comparisons. See [sift-down](/sift-down/).

**Insert** (lines L11 to L13) puts the new key in the first free cell, which is the next leaf of the complete tree, and sifts it up. The cost is $O(\log n)$.

**Find-min** (lines L14 and L15) reads the root. The cost is $O(1)$.

**Extract-min** (lines L16 to L21) saves the root, moves the last key into the root, shrinks the heap by one and sifts the root down. Only the last cell can be removed without a hole in the complete tree, which is why the last key fills the root. The cost is $O(\log n)$.

**Decrease-key** (lines L22 to L24) lowers $A[i]$ and sifts it up. A smaller key can only be too small for its place, never too large, so sift-up is enough. The cost is $O(\log n)$. A general `change-key` that may raise the key calls sift-down in that case.

**Build** (lines L25 and L26) is [Floyd's heap construction](/floyd-heap-construction/). It sifts down each internal node, from the last one to the root. The cost is $O(n)$, not $O(n \log n)$, see the complexity section.

## Example

Start with BUILD on $B = [5, 3, 8, 1, 9, 2]$, so $n = 6$ and line L26 runs for $i = 3, 2, 1$. Then run five operations. The table shows the array after each step.

| step | what happens | array |
|---|---|---|
| start | $B$ copied | [5, 3, 8, 1, 9, 2] |
| SIFT-DOWN at 3 | 8 has the child 2, swap | [5, 3, 2, 1, 9, 8] |
| SIFT-DOWN at 2 | 3 has the children 1 and 9, swap with 1 | [5, 1, 2, 3, 9, 8] |
| SIFT-DOWN at 1 | 5 swaps with 1, then with 3 | [1, 3, 2, 5, 9, 8] |
| INSERT 4 | 4 at index 7, its parent 2 is smaller, stop | [1, 3, 2, 5, 9, 8, 4] |
| INSERT 0 | 0 at index 8, swaps with 5, 3 and 1 | [0, 1, 2, 3, 9, 8, 4, 5] |
| EXTRACT-MIN | returns 0; 5 goes to the root, swaps with 1 and 3 | [1, 3, 2, 5, 9, 8, 4] |
| DECREASE-KEY at 5 to 0 | 0 swaps with 3, then with 1 | [0, 1, 2, 5, 3, 8, 4] |
| EXTRACT-MIN | returns 0; 4 goes to the root, swaps with 1 and 3 | [1, 3, 2, 5, 4, 8] |

The tree of the last array has the root 1, the children 3 and 2, then 5 and 4 under 3, and 8 under 2.

## Correctness

Each operation keeps the invariant (H) and the multiset of keys that the priority queue must hold. The key facts are two lemmas. Sift-up is correct when the only possible violation of (H) is the edge from $A[i]$ to its parent, and the parent of $i$ is at most each child of $i$. Sift-down is correct when the only possible violations are the edges from $A[i]$ to its children, and the parent of $i$ is at most each child of $i$. Each swap moves the one possible violation one level, and the loop stops at the root, at a leaf, or when no violation is left. Insert, decrease-key and extract-min each set up the condition of one lemma. Build sifts down the nodes in decreasing index order, so the two subtrees of $i$ are heaps when $i$ is processed. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n = H.n$. Each operation costs $O(1)$ outside the sift loops, and each loop iteration costs $O(1)$ and moves one level. The tree has height $\lfloor \lg n \rfloor$.

**Insert and decrease-key.** Sift-up from index $i$ runs at most $\lfloor \lg i \rfloor \le \lfloor \lg n \rfloor$ iterations. Inserting the keys $n, n-1, \ldots, 1$ in this order makes each new key go up to the root, so the worst case is $\Theta(\log n)$.

**Extract-min.** Sift-down from the root runs at most $\lfloor \lg n \rfloor$ iterations, with 2 comparisons each, so extract-min does at most $2\lfloor \lg n \rfloor$ comparisons plus 2 for the last test. On the heap $[1, 2, \ldots, n]$, which is sorted and so satisfies (H), the last key $n$ is the largest; it moves to the root and sinks to a leaf, at depth at least $\lfloor \lg(n-1) \rfloor - 1$. So the worst case is $\Theta(\log n)$.

**Build.** SIFT-DOWN at a node of height $h$ costs $O(h + 1)$. Exactly $\lfloor n/2^h \rfloor$ nodes have height at least $h$, so the sum of the heights of all nodes is

$$\sum_{h \ge 1} \left\lfloor \frac{n}{2^h} \right\rfloor = n - s_2(n) < n,$$

where $s_2(n)$ is the number of 1 bits of $n$ ([Legendre's formula](/legendre-formula/) for the power of 2 in $n!$). So BUILD does at most $n - s_2(n)$ swaps and runs in $\Theta(n)$ time. The page [Floyd's heap construction](/floyd-heap-construction/) proves this and gives the exact comparison count.

| operation | time |
|---|---|
| insert | $\Theta(\log n)$ worst case; amortized if the array doubles |
| find-min | $\Theta(1)$ |
| extract-min | $\Theta(\log n)$ worst case |
| decrease-key (with the index) | $\Theta(\log n)$ worst case |
| build from $n$ keys | $\Theta(n)$ worst case |
| meld of two heaps of total size $n$ | $\Theta(n)$, by a build on the joined array |
| search for a key | $\Theta(n)$ |
| space | $n$ cells, no pointers |

In the [comparison model](/comparison-model/), insert and extract-min cannot both be $o(\log n)$, even amortized, because $n$ of each sort $n$ keys (see the [heap](/heap/) page). Heaps such as the [Fibonacci heap](/fibonacci-heap/) make insert and decrease-key $O(1)$ amortized, but extract-min stays $\Omega(\log n)$.

## Variants

- **Max-heap.** Reverse each comparison. [Heapsort](/heapsort/) uses a max-heap so that the sorted output fills the array from the end.
- **0-based arrays.** With $A[0 \ldots n-1]$, the parent of $i$ is $\lfloor (i-1)/2 \rfloor$ and the children are $2i + 1$ and $2i + 2$. The Python code of this page uses this form.
- **[d-ary heap](/d-ary-heap/).** Each node has $d$ children. Insert and decrease-key take $O(\log_d n)$ and extract-min takes $O(d \log_d n)$. With $d = 4$ it is often faster in practice, because of fewer levels and better cache use.
- **[Indexed priority queue](/indexed-priority-queue/).** A position map from items to indices gives decrease-key and delete by item name.
- **Bottom-up sift-down.** Walk down the path of smaller children to a leaf with one comparison per level, then go back up to the right place. When the moved key belongs near the bottom, as it does in heapsort, this uses about $\lg n$ comparisons instead of about $2 \lg n$.
- **Delete of any index.** Move the last key into the hole, then sift up or down, see [heap delete](/heap-delete/).
- **[Min-max heap](/min-max-heap/), [interval heap](/interval-heap/) and [deap](/deap/).** These give both the minimum and the maximum, for a [double-ended priority queue](/double-ended-priority-queue/).
- **[Weak heap](/weak-heap/).** A relaxed order that saves comparisons in sorting.

## When to use it

Use a binary heap as the default priority queue: it is short, it uses no pointers, and its array access is fast. Use it for [heapsort](/heapsort/), for [top-k selection](/top-k-selection/), for a [k-way merge](/k-way-merge/) and for [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/) on sparse graphs, where it gives $O((n + m) \log n)$ time. On dense graphs, a [Fibonacci heap](/fibonacci-heap/) gives $O(m + n \log n)$ in theory, but a binary heap or a [d-ary heap](/d-ary-heap/) is often faster at practical sizes. Use a [binomial heap](/binomial-heap/) or a [leftist heap](/leftist-heap/) when heaps must meld fast. Use a [bucket queue](/bucket-queue/) when the keys are small integers.

## Pitfalls

- **Off-by-one in the index formulas.** Mixing the 1-based formulas with a 0-based array makes the root's "children" $0$ and $1$, so the root is its own child and the tree is wrong. With a 0-based array, use $2i + 1$, $2i + 2$ and $\lfloor (i-1)/2 \rfloor$.
- **Comparing only with the left child.** A sift-down that swaps with the left child when it is smaller than the parent, without comparing the two children, breaks (H) between the new parent and the right child. Line L7 must compare with the current smallest, $A[m]$, not with $A[i]$.
- **Missing right child.** The test $2i + 1 \le n$ in line L7 is needed; without it, sift-down reads a stale key beyond the end of the heap. After an extract-min, that cell still holds the key that moved to the root.
- **Sift-up after a key increase.** Decrease-key calls sift-up. If the new key may be larger, sift-up does nothing and (H) breaks below the node. Check the direction (line L22) or call sift-down.
- **A build by $n$ inserts.** It is correct, but it costs $\Theta(n \log n)$ in the worst case, see [heap construction by insertion](/heap-construction-by-insertion/). Use line L26.
- **Stale handles.** An index into the array changes at each swap. A caller that keeps an index for decrease-key must get it updated, which is what the position map of an indexed priority queue does.

## Implementations

The Python class is a 0-based min-heap of keys. It follows the main block line by line, with the index formulas of the 0-based variant, and it grows the list as a dynamic array. `decrease_key` takes the 0-based index.

## History

Williams introduced the binary heap in 1964 in the Communications of the ACM, as Algorithm 232, Heapsort, with the insert and the extract operations in an array. In the same year Floyd published Treesort 3, Algorithm 245, which builds the heap bottom-up in linear time. Knuth gives this history in Section 5.2.3 of Volume 3. The use of the heap as a general priority queue, with decrease-key, is the form that textbooks such as CLRS give in Chapter 6.

## References
