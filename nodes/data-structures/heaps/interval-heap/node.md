---
tag: XN8WFN
kind: data-structure
slug: interval-heap
name: Interval heap
aliases:
- interval heaps
area: data-structures/heaps
level: advanced
summary: Double-ended heap in which each node holds an interval of two keys.
implements: [double-ended-priority-queue]
model: comparison-model
prereqs: [double-ended-priority-queue, binary-heap, heap-property, sift-up, sift-down]
see_also: [double-ended-priority-queue, deap, min-max-heap, binary-heap, heap-delete, floyd-heap-construction, comparison-sort-lower-bound, priority-queue]
sources:
  - paper: "Jan van Leeuwen and Derick Wood, Interval heaps, The Computer Journal 36(3), 1993"
    locator: the definition, the insert and delete algorithms, and the linear-time build
  - book: isbn:9781584884354
    title: Dinesh P. Mehta and Sartaj Sahni (editors), Handbook of Data Structures and Applications
    locator: the chapter Double-ended priority queues, by Sartaj Sahni, the section on interval heaps
---

An interval heap is an array structure for the [double-ended priority queue](/double-ended-priority-queue/). It is a complete binary tree stored level by level, like a [binary heap](/binary-heap/), but each node holds two keys, a low key and a high key, so it describes the interval from low to high. The last node may hold one key. The rule is that the interval of each node contains the keys of its children: low of the parent $\le$ every key of the child $\le$ high of the parent. So the low keys form a min-heap, the high keys form a max-heap, and the root holds the minimum and the maximum. Find-min and find-max take $O(1)$ time, insert, extract-min and extract-max take $O(\log n)$ time, and the structure uses no extra space. It was introduced by van Leeuwen and Wood in 1993 and is often called the simplest of the array DEPQs.

## In plain words

Put the keys in pairs, and put each pair, smaller key first, in a node of a binary tree. Think of each pair as a range of numbers. The rule is that every range sits inside the range of the node above it.

Then the top node has the smallest and the largest key, because every other key lies inside its range. The small ends of all ranges behave like a min-heap, and the large ends behave like a max-heap. To add a key, put it at the end and move it up along the side where it does not fit. To remove the smallest key, move a key from the end to the top and move it down along the small side, as in a normal heap.

## The abstract type

An interval heap implements the [double-ended priority queue](/double-ended-priority-queue/): INSERT, FIND-MIN, FIND-MAX, EXTRACT-MIN and EXTRACT-MAX on a multiset of keys from a [total order](/total-order/). Like a binary heap, it has no fast meld and no search.

## Representation

The keys are in an array $A[0 \ldots n - 1]$. The node $j$, for $0 \le j < \lceil n/2 \rceil$, holds $A[2j]$, its low key $\mathrm{LO}(j)$, and $A[2j + 1]$, its high key $\mathrm{HI}(j)$, if $2j + 1 < n$; else the node holds one key, and we let $\mathrm{HI}(j) = \mathrm{LO}(j) = A[2j]$. The parent of the node $j \ge 1$ is $P(j) = \lfloor (j - 1)/2 \rfloor$, and its children are $2j + 1$ and $2j + 2$.

The invariants:

- **(N)** $\mathrm{LO}(j) \le \mathrm{HI}(j)$ for each node $j$.
- **(I)** for each node $j \ge 1$, $\mathrm{LO}(P(j)) \le \mathrm{LO}(j)$ and $\mathrm{HI}(j) \le \mathrm{HI}(P(j))$.

With (N), (I) says that both keys of $j$ lie in the interval $[\mathrm{LO}(P(j)), \mathrm{HI}(P(j))]$. By induction along the path to the root, every key lies in $[A[0], A[1]]$. The tree has $\lceil n/2 \rceil$ nodes, so its height is $\lfloor \lg \lceil n/2 \rceil \rfloor$, about $\lg n - 1$.

## Operations

```pseudo id=main
INSERT(x)
L1  append x to A; k ← n − 1; j ← ⌊k/2⌋              ▷ x is in the last node j
L2  if k is odd and A[k] < A[k − 1] then swap A[k] and A[k − 1]
L3  SIFT-UP-MIN(j); SIFT-UP-MAX(j)

SIFT-UP-MIN(j)
L4  while j > 0 and LO(j) < LO(P(j)) do
L5      swap LO(j) and LO(P(j)); j ← P(j)

SIFT-UP-MAX(j)
L6  while j > 0 and HI(P(j)) < HI(j) do
L7      swap HI(j) and HI(P(j)); j ← P(j)

EXTRACT-MIN()
L8  if n = 0 then error "underflow"
L9  r ← A[0]; x ← remove the last key of A; if n = 0 then return r
L10 A[0] ← x; j ← 0
L11 loop: c ← the child of j with the smaller LO; if j has no child then return r
L12     if not LO(c) < LO(j) then return r
L13     swap LO(j) and LO(c); if HI(c) < LO(c) then swap them
L14     j ← c

EXTRACT-MAX()
L15 if n = 0 then error "underflow"
L16 if n ≤ 2 then return the last key of A, removed
L17 r ← A[1]; A[1] ← remove the last key of A; j ← 0
L18 loop: c ← the child of j with the larger HI; if j has no child then return r
L19     if not HI(j) < HI(c) then return r
L20     swap HI(j) and HI(c); if HI(c) < LO(c) then swap them
L21     j ← c
```

**Insert.** The new key goes into the last node. If that node now has two keys, line L2 puts them in order. The old key of the node lies in the parent's interval, so at most one of the two sifts of line L3 moves anything: SIFT-UP-MIN if the new key is below the parent's interval, SIFT-UP-MAX if it is above.

**Extract-min.** The minimum is $A[0]$. The last key $x$ goes into the low slot of the root, and it sifts down the min-heap of low keys, as in [sift-down](/sift-down/). When it enters a child $c$, it may be larger than $\mathrm{HI}(c)$; then line L13 swaps the two keys of $c$, so $x$ stays as the high key of $c$ and the old high key goes on down as the low key. EXTRACT-MAX is the mirror image.

**Build.** $n$ keys can also be arranged bottom-up, as in [Floyd's heap construction](/floyd-heap-construction/), in $O(n)$ time; the Python code builds by inserts.

## Example

Insert 5, 2, 8, 6, 1, 9, 3, 7 in this order. The nodes are listed in array order, as (low, high).

| step | nodes | what happens |
|---|---|---|
| insert 5, 2 | (2, 5) | line L2 orders the root pair |
| insert 8 | (2, 8), (5) | 8 is the single key of node 1; it is above 5, the root's high key, so SIFT-UP-MAX swaps the two |
| insert 6 | (2, 8), (5, 6) | 6 fits in [2, 8] |
| insert 1 | (1, 8), (5, 6), (2) | 1 is below 2, so SIFT-UP-MIN swaps it to the root |
| insert 9 | (1, 9), (5, 6), (2, 8) | the pair (2, 9) at node 2; 9 is above 8, so it swaps with the root's high key |
| insert 3 | (1, 9), (3, 6), (2, 8), (5) | 3 at node 3 is below 5, the low key of node 1, and swaps with it |
| insert 7 | (1, 9), (3, 7), (2, 8), (5, 6) | the pair (5, 7); 7 is above 6, and swaps with it |
| extract-min | (2, 9), (3, 7), (6, 8), (5) | returns 1; the last key 6 goes to the root's low slot, then swaps with 2, the smaller low key of the children |
| extract-max | (2, 8), (3, 7), (5, 6) | returns 9; the last key 5 goes to the root's high slot, swaps with 8 at node 2, and line L20 orders (6, 5) to (5, 6) |

## Correctness

Each operation keeps (N) and (I). In INSERT, the invariants fail at most at the edge from the last node to its parent, on one side only, and SIFT-UP-MIN or SIFT-UP-MAX is the sift-up of a binary heap on the low keys or on the high keys. In EXTRACT-MIN, after line L10 only the edges from the root to its children can fail on the low side, and each step of the loop either stops or moves the failure one level down, with line L13 keeping (N) at the child. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| FIND-MIN, FIND-MAX | $O(1)$ |
| INSERT | $O(\log n)$, at most $h + 3$ comparisons for the height $h$ |
| EXTRACT-MIN, EXTRACT-MAX | $O(\log n)$, at most 3 comparisons per level |
| build from $n$ keys | $O(n)$ bottom-up, $O(n \log n)$ by inserts |

Each loop moves one level per iteration, and the tree of $\lceil n/2 \rceil$ nodes has height $\lfloor \lg \lceil n/2 \rceil \rfloor$. An iteration of EXTRACT-MIN compares the low keys of the two children, then the smaller with $\mathrm{LO}(j)$, then the keys of $c$, so 3 comparisons. INSERT does one comparison in line L2, one per level and one to stop in the sift that runs, and one in the sift that does not. The space is the array, with no extra fields.

## Variants

- **Delete of any key.** Given the position of a key, replace it with the last key and repair upward or downward, as in [heap delete](/heap-delete/).
- **Meld.** No fast meld is known for the array form; two interval heaps are merged by inserting the smaller one or by a new build.
- **Other array DEPQs.** The [deap](/deap/) keeps a min-heap and a max-heap side by side under an empty root, and the [min-max heap](/min-max-heap/) alternates min levels and max levels. All three have the same asymptotic costs.
- **External memory.** Each node can hold a block of keys in place of two, which gives an external interval heap for data on disk.

## When to use it

Use an interval heap when a program needs both the minimum and the maximum of a changing set and nothing else: a bounded buffer of the best $k$ candidates, the middle part of an external quicksort that keeps a run of keys in memory, or a scheduler that serves urgent and stale jobs. When search or delete by key is also needed, a balanced search tree is the better choice.

## Pitfalls

- **The single last node.** When $n$ is odd, the last node has one key, which acts as both its low and its high key. Code that reads $A[2j + 1]$ without a check reads past the end.
- **Forgetting line L13.** When the moved key enters a child, it may be larger than the child's high key. Without the swap, (N) fails, and a later find-max can be wrong.
- **Choosing the child.** EXTRACT-MIN must pick the child with the smaller low key, and EXTRACT-MAX the child with the larger high key, where a single-key child uses its one key.
- **Both sifts in insert.** The new key may break the interval on either side. Testing only the min side misses keys larger than the parent's high key.

## Implementations

The Python class `IntervalHeap` keeps the keys in one list `a`, with the node $j$ at `a[2*j]` and `a[2*j + 1]`. `insert`, `extract_min` and `extract_max` follow the pseudocode, `find_min` and `find_max` read the root, `nodes()` lists the pairs, and `check_invariant` checks (N) and (I). Keys need only the operation "<".

## History

Van Leeuwen and Wood published interval heaps in The Computer Journal in 1993, after the min-max heap of Atkinson, Sack, Santoro and Strothotte (1986) and the deap of Carlsson (1987). The same structure also appears in the literature under the names twin heap and diamond deque. Sahni's textbooks and handbook chapter made it the standard teaching example of a DEPQ.

## References
