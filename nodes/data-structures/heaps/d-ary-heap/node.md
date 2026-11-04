---
tag: Y99BAR
kind: data-structure
slug: d-ary-heap
name: d-ary heap
aliases:
- k-ary heap
- d-heap
area: data-structures/heaps
level: core
summary: Generalization of the binary heap with d children per node, trading insert speed for extract cost.
implements: [priority-queue]
model: comparison-model
prereqs: [binary-heap, heap-property, sift-up, sift-down]
see_also: [binary-heap, heap, dijkstra, prim, decrease-key, floyd-heap-construction, indexed-priority-queue, heapsort]
sources:
  - paper: "Donald B. Johnson, Priority queues with update and finding minimum spanning trees, Information Processing Letters 4(3), 1975"
    locator: pages 53 to 57 (d-heaps and the choice of d for shortest paths and spanning trees)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Problem 6-2 (Analysis of d-ary heaps)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the exercises on heaps with more than two children per node
  - paper: "Anthony LaMarca and Richard E. Ladner, The influence of caches on the performance of heaps, ACM Journal of Experimental Algorithmics 1, 1996"
    locator: the experiments with cache-aligned d-heaps
---

A $d$-ary heap is a [binary heap](/binary-heap/) in which each node has up to $d$ children instead of two, for a fixed $d \ge 2$. It is a complete $d$-ary tree, stored level by level in an array, with the [heap property](/heap-property/). The tree has height about $\log_d n$, so insert and [decrease-key](/decrease-key/) take $O(\log_d n)$ time, but extract-min must compare $d$ children at each level and takes $O(d \log_d n)$ time. Johnson (1975) used this trade to speed up [Dijkstra's algorithm](/dijkstra/) and [Prim's algorithm](/prim/), which do many more decrease-keys than extract-mins: with $d \approx m/n$ they run in $O(m \log_{m/n} n)$ time. In practice, $d = 4$ is a common choice, because the tree is shallower and the children of a node share cache lines.

## In plain words

A binary heap is a family tree where each parent has at most two children and is smaller than them. Now let each parent have up to $d$ children, for example four. The tree gets much flatter: with four children per node, a million items fit in about ten levels instead of twenty.

Moving an item up is now faster, because there are fewer levels to climb, and at each level you compare only with one parent. Moving an item down is slower per level, because you must look at all $d$ children to find the smallest. So a larger $d$ helps when items mostly move up, and hurts when items mostly move down.

## The abstract type

A $d$-ary heap implements the [priority queue](/priority-queue/): INSERT, FIND-MIN, EXTRACT-MIN, DECREASE-KEY at an index, and BUILD from $n$ keys. Keys come from a [total order](/total-order/). Like the binary heap, it does not support a fast meld or a search for a key.

## Representation

The keys are in $A[1 \ldots n]$. In the 1-based form, the parent of $i \ge 2$ is $\lfloor (i - 2)/d \rfloor + 1$, and the children of $i$ are $d(i - 1) + 2, \ldots, di + 1$, those of them that are at most $n$. With $d = 2$ these are the usual formulas $\lfloor i/2 \rfloor$, $2i$ and $2i + 1$. In the 0-based form, the parent of $i \ge 1$ is $\lfloor (i - 1)/d \rfloor$ and the children are $di + 1, \ldots, di + d$.

The invariant is the min-heap property

$$A[\mathrm{parent}(i)] \le A[i] \quad \text{for each } 2 \le i \le n.$$

Level $t$ of the tree holds the indices from $(d^t - 1)/(d - 1) + 1$ to $(d^{t+1} - 1)/(d - 1)$, so the height $h$ of a tree of $n \ge 1$ nodes is the least $h$ with $(d^{h+1} - 1)/(d - 1) \ge n$. That is $h = \lceil \log_d((d - 1)n + 1) \rceil - 1$, and $h < \log_d n + 1$.

## Operations

```pseudo id=main
PARENT(i)                                  ▷ 2 ≤ i
L1  return ⌊(i − 2)/d⌋ + 1

CHILD(i, j)                                ▷ the j-th child of i, 1 ≤ j ≤ d
L2  return d(i − 1) + j + 1

SIFT-UP(A, i)
L3  while i > 1 and A[i] < A[PARENT(i)] do
L4      swap A[i] and A[PARENT(i)]
L5      i ← PARENT(i)

SIFT-DOWN(A, n, i)
L6  while true do
L7      m ← i
L8      for j ← 1 to d do
L9          c ← CHILD(i, j)
L10         if c ≤ n and A[c] < A[m] then m ← c
L11     if m = i then return
L12     swap A[i] and A[m], i ← m

INSERT(H, k)
L13 H.n ← H.n + 1, A[H.n] ← k
L14 SIFT-UP(A, H.n)

EXTRACT-MIN(H)
L15 if H.n = 0 then error "heap underflow"
L16 min ← A[1], A[1] ← A[H.n], H.n ← H.n − 1
L17 SIFT-DOWN(A, H.n, 1)
L18 return min

DECREASE-KEY(H, i, k)
L19 if k > A[i] then error "new key is larger than the current key"
L20 A[i] ← k, SIFT-UP(A, i)

BUILD(H, B[1 .. n])
L21 A[1 .. n] ← B[1 .. n], H.n ← n
L22 for i ← PARENT(n) downto 1 do SIFT-DOWN(A, n, i)
```

**Sift-up** (lines L3 to L5) is the same as in a binary heap, with the new parent formula. It does one comparison per level.

**Sift-down** (lines L6 to L12) finds the smallest of the key and its up to $d$ children (lines L8 to L10), which takes up to $d$ comparisons, and swaps with that child if it is smaller.

**Insert, extract-min and decrease-key** (lines L13 to L20) are the binary heap operations with these two sifts. **Build** (lines L21 and L22) is [Floyd's method](/floyd-heap-construction/): it sifts down each internal node, from the last one, PARENT$(n)$, to the root.

## Example

Take $d = 3$, so the children of 1 are 2, 3, 4, the children of 2 are 5, 6, 7, and the children of 3 are 8, 9, 10. BUILD on $B = [5, 3, 8, 1, 9, 2, 7, 6, 4]$, with $n = 9$, runs line L22 for $i = $ PARENT$(9) = 3$, then 2, then 1.

| step | what happens | array |
|---|---|---|
| start | $B$ copied | [5, 3, 8, 1, 9, 2, 7, 6, 4] |
| SIFT-DOWN at 3 | 8 has the children 6 and 4; swap with 4 | [5, 3, 4, 1, 9, 2, 7, 6, 8] |
| SIFT-DOWN at 2 | 3 has the children 9, 2, 7; swap with 2 | [5, 2, 4, 1, 9, 3, 7, 6, 8] |
| SIFT-DOWN at 1 | 5 has the children 2, 4, 1; swap with 1; cell 4 has no children | [1, 2, 4, 5, 9, 3, 7, 6, 8] |
| INSERT 0 | 0 at cell 10, its parent is 3; swap with 4, then with 1 | [0, 2, 1, 5, 9, 3, 7, 6, 8, 4] |
| EXTRACT-MIN | returns 0; 4 goes to the root; children 2, 1, 5; swap with 1; the children 6 and 8 of cell 3 are larger | [1, 2, 4, 5, 9, 3, 7, 6, 8] |
| DECREASE-KEY at 8 to 0 | the parent of 8 is 3; swap with 4, then with 1 | [0, 2, 1, 5, 9, 3, 7, 4, 8] |

The tree has 2 levels below the root for 9 or 10 keys, against 3 for a binary heap.

## Correctness

The proof is the one for the binary heap, with "each child" in place of "both children". Sift-up is correct when the only edge that may fail is the edge into $i$ and the parent of $i$ is at most each child of $i$. Sift-down is correct when the only edges that may fail are the edges out of $i$ and the parent of $i$ is at most each child of $i$; lines L8 to L10 find a smallest child among all $d$. Build keeps the claim that each subtree with a root after $i$ is a heap. See [the correctness proof](proofs/correctness.md).

## Complexity

Let $h$ be the height, so $h < \log_d n + 1$.

- **Insert and decrease-key.** Sift-up does at most $h$ swaps and $h$ comparisons, so $O(\log_d n) = O(\log n / \log d)$.
- **Extract-min.** Sift-down does at most $h$ swaps and at most $d$ comparisons per level, so at most $d\,h$ comparisons and $O(d \log_d n)$ time.
- **Build.** A sift-down from a node of height $t$ costs at most $d\,t$ comparisons, and the heights of all nodes add up to at most $(n - 1)/(d - 1) + h$. So build does fewer than $d(n - 1)/(d - 1) + d\,h < 2n + d(\log_d n + 1)$ comparisons, which is $O(n)$.
- **Find-min.** $O(1)$. **Space.** $n$ cells, no pointers.

The proofs are in [the complexity proof](proofs/complexity.md).

| operation | time |
|---|---|
| insert | $O(\log_d n)$ |
| find-min | $O(1)$ |
| extract-min | $O(d \log_d n)$ |
| decrease-key | $O(\log_d n)$ |
| build | $O(n)$ |

**Choosing $d$.** The function $d / \ln d$ is smallest at $d = e$ among real numbers, and $d = 3$ gives slightly fewer comparisons than $d = 2$ for extract-min alone: $d \log_d n = (d/\lg d) \lg n$, which is $2 \lg n$ for $d = 2$, about $1.89 \lg n$ for $d = 3$, and $2 \lg n$ again for $d = 4$. For a mix of operations, the best $d$ balances the two costs. Dijkstra's algorithm on a graph with $n$ vertices and $m$ edges does $n$ extract-mins and up to $m$ decrease-keys, for a total of

$$O(n\,d \log_d n + m \log_d n).$$

With $d = \max(2, \lceil m/n \rceil)$, both terms are $O(m \log_d n)$, so the time is $O(m \log_{2 + m/n} n)$. On a dense graph with $m = n^{1 + \varepsilon}$, this is $O(m/\varepsilon)$, linear in $m$ for a fixed $\varepsilon > 0$.

## Variants

- **Max-heap.** Reverse each comparison.
- **Cache-aligned layout.** LaMarca and Ladner (1996) padded the array so that the $d$ children of each node lie in one cache line, which makes the $d$ comparisons of a sift-down cheap. A 4-ary heap is a common result of such tuning.
- **Indexed form.** A position map gives decrease-key by item name, as in the [indexed priority queue](/indexed-priority-queue/).
- **Heapsort with $d$ children.** [Heapsort](/heapsort/) works with any $d$; ternary heapsort is a known variant.

## When to use it

Use a $d$-ary heap in place of a binary heap when decrease-key or insert is much more common than extract-min, as in Dijkstra's and Prim's algorithms on dense graphs, or when the cost of memory access dominates and a shallow tree helps. It keeps the simple array layout, so it is often faster in practice than a [Fibonacci heap](/fibonacci-heap/), whose better bound comes with pointers and large constants. For a graph with few edges per vertex, $d = 2$ or $d = 4$ is usual.

## Pitfalls

- **Wrong index formulas.** The 1-based parent is $\lfloor (i - 2)/d \rfloor + 1$, not $\lfloor i/d \rfloor$; the latter is right only for $d = 2$. Mixing the 1-based and 0-based formulas breaks the tree.
- **A sift-down that stops at the first smaller child.** It must find the smallest of all $d$ children; swapping with any smaller child can put a larger key above a smaller sibling.
- **The last child.** Only the last internal node can have fewer than $d$ children. The loop must stop at the first child index beyond $n$, as the test $c \le n$ in line L10 does.
- **Too large a $d$.** With $d$ close to $n$, the heap is a root with a list of children, and extract-min scans almost all keys. Keep $d$ a small constant or about $m/n$.

## Implementations

The Python class `DaryHeap(d)` is a 0-based min-heap of keys, with `d = 4` by default. It follows the main block with the 0-based formulas. Its sift-down breaks out of the loop over children at the first child index beyond the end, since the later children are beyond it too. `decrease_key` takes a 0-based index.

## History

Donald B. Johnson introduced $d$-heaps in 1975, in a paper in Information Processing Letters on priority queues with update, and used them for shortest paths and minimum spanning trees with $d$ chosen from the density of the graph. The binary case is the heap of Williams (1964). CLRS gives the analysis of $d$-ary heaps as Problem 6-2.

## References
