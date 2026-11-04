---
tag: HGEHQG
kind: data-structure
slug: min-max-heap
name: Min-max heap
aliases:
- min-max heaps
area: data-structures/heaps
level: core
summary: Binary tree whose levels alternate min and max layers, giving both extremes in O(1) to find.
implements: [double-ended-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(log n)}
  space: {extra: O(1)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [heap-property, complete-binary-tree, sift-up, sift-down]
see_also: [double-ended-priority-queue, interval-heap, deap, binary-heap, floyd-heap-construction, priority-queue, sliding-window-median, heap]
sources:
  - paper: M. D. Atkinson, J.-R. Sack, N. Santoro and Th. Strothotte, Min-max heaps and generalized priority queues, Communications of the ACM 29(10), 1986
    locator: pages 996 to 1000 (the definition, the TrickleDown and BubbleUp procedures, the linear-time construction, and the generalization to order-statistic queues)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), heaps and their array layout, which the min-max heap extends
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6 (Heapsort), the array layout of a heap and the analysis of building a heap in linear time
---

A min-max heap is a [double-ended priority queue](/double-ended-priority-queue/) stored in one array, in the shape of a [complete binary tree](/complete-binary-tree/) like a [binary heap](/binary-heap/). The levels of the tree alternate: a node on an even level (the root is level 0) is at most every key below it, and a node on an odd level is at least every key below it. So the minimum is at the root and the maximum is one of its two children, and both are found in $O(1)$ time. Insert, delete-min and delete-max take $O(\log n)$ time, and a heap is built from $n$ keys in $O(n)$ time. Atkinson, Sack, Santoro and Strothotte introduced it in 1986.

## In plain words

A normal heap is a family tree where each person is smaller than everyone below them, so the smallest is at the top. It gives the smallest item fast, but finding the largest means searching the whole bottom row.

A min-max heap takes turns by generation. The top person is the smallest of everyone. Their children are each the largest in their own family branch. The grandchildren are again the smallest in their branches, and so on. So the smallest item is at the top, and the largest is one of the two people just below it. When an item is added or removed, it moves up or down by jumps of two generations, past the people of its own kind, which keeps the work short.

## The abstract type

A min-max heap implements the [double-ended priority queue](/double-ended-priority-queue/) on a multiset of keys from a total order: `insert(x)`, `find-min()`, `find-max()`, `delete-min()` and `delete-max()`, plus `build(A)` from an array. It does not support meld in less than linear time, and decrease-key needs an index of positions, as for a binary heap.

## Representation

The items are in an array $A[0 \dots n-1]$, in level order, as in a binary heap with 0-based indices: the children of $i$ are $2i + 1$ and $2i + 2$, the parent of $i > 0$ is $\lfloor (i - 1)/2 \rfloor$, and the grandparent of $i \ge 3$ is $\lfloor (i - 3)/4 \rfloor$. The level of $i$ is $\lfloor \lg(i + 1) \rfloor$. A node on an even level is a *min node*, and a node on an odd level is a *max node*.

**Invariant (min-max order).** For every node $i$ and every descendant $j$ of $i$:

- if $i$ is a min node, then $A[i] \le A[j]$;
- if $i$ is a max node, then $A[i] \ge A[j]$.

Two consequences follow. The min nodes on any path from the root form a nondecreasing sequence, and the max nodes form a nonincreasing sequence. The root $A[0]$ is a smallest key, and a largest key is $A[0]$ if $n = 1$, else the larger of $A[1]$ and $A[2]$ (only $A[1]$ if $n = 2$). Each max node is at least its descendants, so the largest key of the whole tree, which is in the subtree of node 1 or node 2 if $n \ge 2$, is at that node.

For a node $i$, say that $x$ is *better than* $y$ for the level of $i$ if $x < y$ and $i$ is a min node, or $x > y$ and $i$ is a max node.

## Operations

```pseudo id=main
PUSH-DOWN(A, i, n)                      ▷ the subtree of i is in order except at i
L1  while 2i + 1 < n do                 ▷ i has a child
L2      m ← the child or grandchild of i with the best key for the level of i
L3      if m is a child of i then
L4          if A[m] is better than A[i] for the level of i then swap A[m] and A[i]
L5          return
L6      if A[m] is not better than A[i] for the level of i then return
L7      swap A[m] and A[i]
L8      p ← parent(m); if A[p] is better than A[m] for the level of i then swap A[m] and A[p]
L9      i ← m

PUSH-UP(A, i)                           ▷ A[i] is a new leaf
L10 if i = 0 then return
L11 p ← parent(i)
L12 if A[i] is better than A[p] for the level of p then
L13     swap A[i] and A[p]; i ← p
L14 while i has a grandparent g and A[i] is better than A[g] for the level of i do
L15     swap A[i] and A[g]; i ← g

DELETE-MIN(A, n)                        ▷ n ≥ 1
L16 x ← A[0]; A[0] ← A[n − 1]; n ← n − 1; PUSH-DOWN(A, 0, n)
L17 return x

DELETE-MAX(A, n)                        ▷ n ≥ 1
L18 m ← 0 if n = 1, else 1 if n = 2, else the index of the larger of A[1] and A[2]
L19 x ← A[m]; A[m] ← A[n − 1]; n ← n − 1; if m < n then PUSH-DOWN(A, m, n); return x

INSERT(A, n, x)
L20 A[n] ← x; n ← n + 1; PUSH-UP(A, n − 1)
```

**PUSH-DOWN** (lines L1 to L9), called TrickleDown by Atkinson et al., moves a key down two levels at a time. At a min node $i$, it finds the smallest key among the children and grandchildren of $i$. If that key is at a grandchild $m$ and is smaller than $A[i]$, the two swap. The old $A[i]$ is now at $m$, below the max node $p = \mathrm{parent}(m)$, so line L8 swaps it with $A[p]$ if it is larger. The loop then goes on from $m$. If the best key is at a child, the child has no larger descendants than itself, so one swap ends the work. At a max node, the same steps run with the order reversed.

**PUSH-UP** (lines L10 to L15), called BubbleUp, places a new leaf. First it compares the leaf with its parent, which is on the other kind of level. If the leaf belongs on the side of the parent, for example a key larger than its max-node parent, they swap. Then the key moves up past its grandparents, which are on its own kind of level, as in [sift-up](/sift-up/) on every second level.

**Delete-min and delete-max** (lines L16 to L19) move the last key into the place of the removed key and push it down. **Find-min** returns $A[0]$, and **find-max** returns the key at the index of line L18.

**Build** puts the keys in the array in any order and calls PUSH-DOWN at $i = \lfloor n/2 \rfloor - 1, \dots, 1, 0$, as in [Floyd's heap construction](/floyd-heap-construction/).

## Example

The array $A$ = [8, 71, 41, 31, 10, 11, 16, 46, 51, 31, 21, 13] is a min-max heap with $n = 12$. By levels:

| level | kind | indices | keys |
|---|---|---|---|
| 0 | min | 0 | 8 |
| 1 | max | 1, 2 | 71, 41 |
| 2 | min | 3 to 6 | 31, 10, 11, 16 |
| 3 | max | 7 to 11 | 46, 51, 31, 21, 13 |

So find-min is 8 and find-max is $\max(71, 41) = 71$.

**Insert 5.** The new leaf is $A[12]$, on max level 3. Its parent is $A[5] = 11$, a min node, and 5 is better than 11 for a min level, so they swap: $A[5] = 5$, $A[12] = 11$. Now 5 is at index 5 on a min level, and its grandparent $A[0] = 8$ is larger, so they swap. The heap is [5, 71, 41, 31, 10, 8, 16, 46, 51, 31, 21, 13, 11].

**Insert 80.** The new leaf is $A[13]$, on max level 3. Its parent $A[6] = 16$ is a min node, and 80 is not smaller than 16, so there is no swap at line L13. Its grandparent $A[2] = 41$ is a max node and $80 > 41$, so they swap. Index 2 has no grandparent. The heap is [5, 71, 80, 31, 10, 8, 16, 46, 51, 31, 21, 13, 11, 41], with find-max 80.

**Delete-min.** It returns 5 and moves the last key 41 to $A[0]$; now $n = 13$. PUSH-DOWN at 0, a min node: the children and grandchildren hold 71, 80, 31, 10, 8, 16, and the smallest is 8 at the grandchild 5. Since $8 < 41$, they swap. The parent of 5 is $A[2] = 80$, and 80 is not smaller than 41, so line L8 does nothing. The loop goes on at index 5, whose children $A[11] = 13$ and $A[12] = 11$ have no children. The best is 11 at the child 12, and $11 < 41$, so they swap and the loop stops. The heap is [8, 71, 80, 31, 10, 11, 16, 46, 51, 31, 21, 13, 41].

**Delete-max.** The larger of $A[1] = 71$ and $A[2] = 80$ is at index 2. It returns 80 and moves the last key 41 to $A[2]$; now $n = 12$. PUSH-DOWN at 2, a max node: the candidates are $A[5] = 11$, $A[6] = 16$ and the grandchild $A[11] = 13$. The largest is 16 at the child 6, and 16 is not larger than 41, so nothing moves. The heap is again [8, 71, 41, 31, 10, 11, 16, 46, 51, 31, 21, 13].

## Correctness

The invariant is local to pairs of an ancestor and a descendant, and it fixes the answers of find-min and find-max as shown in Representation. PUSH-DOWN at a node $i$ whose subtree is in order everywhere except at $i$ puts the subtree in order: the best key among the children and grandchildren of $i$ is the best key of the whole subtree, so it may move to $i$, and the swap at line L8 repairs the only pair that the move can break. PUSH-UP on a new leaf decides at lines L12 and L13 whether the key belongs to the min nodes or to the max nodes on its path, and then sifts it up among those nodes only. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | key comparisons, this code |
|---|---|---|
| find-min, find-max | $O(1)$ | 0 and at most 1 |
| insert | $O(\log n)$ | at most $1 + \lfloor \lfloor \lg n \rfloor / 2 \rfloor$ |
| delete-min, delete-max | $O(\log n)$ | at most about $\tfrac{7}{2} \lg n$, plus 1 for delete-max |
| build from $n$ keys | $O(n)$ | |
| space | $n$ array cells and $O(1)$ extra | |

The tree has height $h = \lfloor \lg n \rfloor$. PUSH-UP does one comparison with the parent and then at most one per two levels, so it does at most $1 + \lfloor h/2 \rfloor$ comparisons. Each round of PUSH-DOWN goes down two levels and does at most 5 comparisons to find the best of up to 6 children and grandchildren, plus one at line L6 and one at line L8, so at most 7 per two levels, or about $\tfrac{7}{2} \lg n$ in total. This is about twice the cost of a delete in a binary heap, which pays for the second end. The build does PUSH-DOWN at each internal node, and the work at a node of height $k$ is $O(k)$, so the sum is $O(n)$ by the same count as for a binary heap.

Atkinson et al. note that the comparisons of PUSH-UP can be cut to $O(\log \log n)$ by a [binary search](/binary-search/) on the path of grandparents, which is sorted, although the number of moves stays $O(\log n)$.

## Variants

- **Max-min heap.** Put the max nodes on the even levels instead. The root is then the maximum.
- **Generalized priority queues.** Atkinson et al. also extend the idea to queues that return the median or another fixed order statistic in $O(1)$ time, with $O(\log n)$ updates.
- **Other double-ended heaps.** The [interval heap](/interval-heap/) stores a pair of keys in each node, a low and a high one, and its operations are simpler and need fewer comparisons. The [deap](/deap/) keeps a min-heap and a max-heap side by side in one array. Two heaps with links between their copies of each key also work, at twice the space.

## When to use it

Use a min-max heap when you need both the smallest and the largest key of a changing set, in a small amount of memory, with no pointers. Examples are a bounded buffer that keeps the best $k$ items and must drop the worst one when full, and the "double-ended" queues of some search and scheduling programs. If only one end is needed, a [binary heap](/binary-heap/) does about half the comparisons. If many comparisons are costly, an [interval heap](/interval-heap/) is usually faster. If you also need order statistics other than the two ends, use a [balanced binary search tree](/balanced-binary-search-tree/).

## Pitfalls

- **The swap with the parent at line L8.** After a key moves down to a grandchild, it can be larger than the max node between them. Without line L8, the order breaks at that max node and a later find-max returns a wrong key.
- **Stopping at a child.** When the best candidate is a child, PUSH-DOWN must stop after the swap of line L4. A program that goes on from the child uses the wrong kind of level for it.
- **Level of an index.** The level of a 0-based index $i$ is $\lfloor \lg(i + 1) \rfloor$. Using $\lfloor \lg i \rfloor$, the formula for 1-based arrays, gives the wrong kind of level for half of the nodes.
- **Find-max on small heaps.** With $n = 1$ the maximum is the root, and with $n = 2$ it is $A[1]$. Code that always reads $A[1]$ and $A[2]$ reads past the end.
- **Delete-max of the last cell.** If the maximum is in the last cell, DELETE-MAX must only remove it, without a push-down, as the test $m < n$ of line L19 does.

## Implementations

The Python version keeps the keys in a list with 0-based indices and uses the helper `_better` for the order of a level. Its `check_invariant` method checks every pair of an ancestor and a descendant.

## History

M. D. Atkinson, J.-R. Sack, N. Santoro and Th. Strothotte published the min-max heap in Communications of the ACM in 1986, as an array structure for double-ended priority queues with the same layout as the heap of Williams and Floyd. Carlsson's deap of 1987 and later the interval heap gave other array layouts for the same type.

## References
