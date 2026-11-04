---
tag: PYFMNC
kind: data-structure
slug: weak-heap
name: Weak heap
aliases:
- Dutton weak heap
area: data-structures/heaps
level: advanced
summary: Heap variant with a relaxed order that makes heapsort use fewer comparisons.
implements: [priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binary-heap, heap-property, binary-tree, sift-down]
see_also: [weak-heapsort, heapsort, binary-heap, d-ary-heap, sift-down, sift-up, priority-queue, relaxed-heap]
sources:
  - paper: Ronald D. Dutton, Weak-heap sort, BIT 33(3), 1993
    locator: the definition of the weak heap, the array form with reverse bits, and the bound of n⌈lg n⌉ − 2^⌈lg n⌉ + n − 1 comparisons for weak-heapsort
  - paper: Stefan Edelkamp and Ingo Wegener, On the performance of weak-heapsort, STACS 2000, Lecture Notes in Computer Science 1770
    locator: the worst-case and average-case comparison counts of weak-heapsort
  - paper: "Stefan Edelkamp, Amr Elmasry and Jyrki Katajainen, The weak-heap data structure: variants and applications, Journal of Discrete Algorithms 16, 2012"
    locator: pages 187 to 205 (the distinguished ancestor, join, sift-up and sift-down; insert in O(1) amortized time with a buffer; relaxed weak heaps)
---

A weak heap is a binary tree of keys in an array, with one extra bit per node, in which each key is at most every key in its *right* subtree, but has no order with respect to its left subtree. This relaxed order lets a delete-min use exactly one comparison per level of the tree, where a [binary heap](/binary-heap/) uses two. Ronald Dutton introduced it in 1993 for [weak-heapsort](/weak-heapsort/), which sorts $n$ keys with at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - 1 < n \lg n + 0.1n$ comparisons, close to the lower bound of $\lg n! \approx n \lg n - 1.44n$. The same structure is a [priority queue](/priority-queue/) with $O(1)$ find-min, $O(\log n)$ insert and delete-min, and a build that uses $n - 1$ comparisons.

## In plain words

In a binary heap, each item must be smaller than everything below it. A weak heap asks for less: each item must be smaller than everything in its right branch only. The left branch is free. The top item has no left branch, so it is still the smallest of all.

Because the left branch is free, we can turn a node around: swap its left and right branches. A weak heap does not move the branches. It keeps one bit per node that says "these two branches are swapped". Flipping that bit costs nothing.

To merge two parts, compare their top items once. If the lower one is smaller, swap the two items and flip the bit. Every operation is a short chain of these one-comparison merges.

## The abstract type

A weak heap implements the [priority queue](/priority-queue/) on a multiset of keys from a total order: `insert(k)`, `find-min()` and `delete-min()`, plus `build` from a list. This page uses a min-heap. Dutton's sort uses the max form, which is the same with the order reversed.

## Representation

The keys are in an array $a[0..n-1]$, and there is a bit array $r[0..n-1]$ of *reverse bits*, all 0 at the start. Node $i$ has the two children $2i + r[i]$ (the left child) and $2i + 1 - r[i]$ (the right child), if those indices are less than $n$. To flip $r[i]$ swaps the two subtrees of $i$ without moving any key. The root $a[0]$ has only a right child, $a[1]$; keep $r[0] = 0$.

For a node $x$, write $L(x)$ and $R(x)$ for the sets of nodes in its left and right subtrees.

**Invariant (weak-heap order).** For every node $x$ and every $y \in R(x)$, $a[x] \le a[y]$. Nothing is required between $x$ and the nodes of $L(x)$.

Since $R(0)$ holds every other node, $a[0]$ is a smallest key.

**Distinguished ancestor.** For $j > 0$, walk up from $j$ while the current node is a left child; the parent of the node where the walk stops is the *distinguished ancestor* $d(j)$. Then $j \in R(d(j))$, and $d(j)$ is the lowest ancestor of $j$ with this property. So $y \in R(x)$ exactly when $x$ is one of $d(y), d(d(y)), \ldots$, and the invariant is the same as $a[d(j)] \le a[j]$ for every $j > 0$. The implementation checks the invariant in this form.

The indices alone give the shape of a [complete binary tree](/complete-binary-tree/): node $i$ has the two children $2i$ and $2i + 1$. The reverse bits only decide which of the two is the left child, so the order refers to a different tree each time a bit flips, on the same nodes.

## Operations

```pseudo id=main
D-ANCESTOR(j)                           ▷ j > 0
L1  while j mod 2 = r[⌊j/2⌋]: j ← ⌊j/2⌋  ▷ j is a left child: go up
L2  return ⌊j/2⌋

JOIN(i, j)                              ▷ i = D-ANCESTOR(j); one comparison
L3  if a[j] < a[i] then
L4      swap a[i] and a[j]; r[j] ← 1 − r[j]; return false
    return true                         ▷ no swap

BUILD(a[0..n−1])                        ▷ r[0..n−1] ← 0 first
L5  for j ← n − 1 down to 1
L6      JOIN(D-ANCESTOR(j), j)

SIFT-DOWN(m)                            ▷ restore the order of a[0..m−1] after a[0] changed
L7  x ← 1
L8  while 2x + r[x] < m: x ← 2x + r[x]  ▷ follow left children to the bottom
L9  while x > 0
L10     JOIN(0, x); x ← ⌊x/2⌋

DELETE-MIN()                            ▷ n ≥ 1
    top ← a[0]
L11 a[0] ← a[n − 1]; n ← n − 1
L12 if n ≥ 2 then SIFT-DOWN(n)
    return top

INSERT(k)
L13 j ← n; a[j] ← k; r[j] ← 0; n ← n + 1; if j > 0 and j is even then r[j/2] ← 0
L14 while j ≠ 0
L15     i ← D-ANCESTOR(j); if JOIN(i, j) then stop; j ← i
```

**Join** (lines L3 and L4) is the only step that compares keys. It is called with $i = d(j)$, when the subtree of $j$ is in weak-heap order and $a[i]$ is at most every key of $L(j)$. If $a[j] < a[i]$, it swaps the two keys and flips $r[j]$, so the old $L(j)$, whose keys are at least the old $a[i]$, becomes the new right subtree of $j$, under the old $a[i]$. After the join, $a[i]$ is at most every key in the subtree of $j$.

**Build** (lines L5 and L6) joins each node to its distinguished ancestor, from the last index down to 1. A node is joined only after all its descendants, so the precondition of the join holds every time. The build uses exactly $n - 1$ comparisons.

**Sift-down** (lines L7 to L10) repairs the order after the root key changed. The nodes $1, 2 + r[1], \ldots$ reached by following left children from node 1 are the nodes whose distinguished ancestor is the root. Line L8 goes down this path, and lines L9 and L10 join the root with each node of the path, from the bottom up. This is one comparison per level, with no comparison between two children. Compare [sift-down](/sift-down/) in a binary heap, which compares the two children and then the larger with the key.

**Delete-min** (lines L11 and L12) moves the last key to the root and sifts it down. It uses at most $\lceil \lg n \rceil$ comparisons.

**Insert** (lines L13 to L15) puts the new key at index $n$. If the parent was a leaf, line L13 resets its reverse bit so that the new node is its left child. Then the key moves up along distinguished ancestors, like [sift-up](/sift-up/), but each step goes to $d(j)$, not to the parent. The loop stops at the first join that does not swap.

**Find-min** returns $a[0]$.

## Example

**Build.** Start with $a = [8, 3, 6, 1, 5, 9, 2, 7]$ and all reverse bits 0. Each row is one call of line L6.

| $j$ | $d(j)$ | compare $a[d(j)]$, $a[j]$ | swap and flip $r[j]$? | $a$ after |
|---|---|---|---|---|
| 7 | 3 | 1, 7 | no | [8, 3, 6, 1, 5, 9, 2, 7] |
| 6 | 1 | 3, 2 | yes | [8, 2, 6, 1, 5, 9, 3, 7] |
| 5 | 2 | 6, 9 | no | [8, 2, 6, 1, 5, 9, 3, 7] |
| 4 | 0 | 8, 5 | yes | [5, 2, 6, 1, 8, 9, 3, 7] |
| 3 | 1 | 2, 1 | yes | [5, 1, 6, 2, 8, 9, 3, 7] |
| 2 | 0 | 5, 6 | no | [5, 1, 6, 2, 8, 9, 3, 7] |
| 1 | 0 | 5, 1 | yes | [1, 5, 6, 2, 8, 9, 3, 7] |

At $j = 4$ the ancestor is the root: 4 is the left child of 2, and 2 is the left child of 1, which is the right child of 0. The build uses 7 comparisons and gives $a = [1, 5, 6, 2, 8, 9, 3, 7]$ with $r = [0, 1, 0, 1, 1, 0, 1, 0]$. For example, $r[1] = 1$ now, so the left child of node 1 is 3 and its right child is 2. The right subtree $R(1)$ is $\{2, 4, 5\}$, with keys 6, 8 and 9, all at least $a[1] = 5$. The left subtree $L(1) = \{3, 6, 7\}$ holds the keys 2, 3 and 7, which are less than 5; the weak-heap order allows this.

**Delete-min.** It returns 1. The last key, 7, moves to the root, and $n = 7$. The left path from node 1 is $1 \to 2 \cdot 1 + r[1] = 3$, and $2 \cdot 3 + r[3] = 7$ is not less than 7, so the path ends at 3. The join of 0 and 3 compares 7 with 2 and swaps, flipping $r[3]$ to 0. The join of 0 and 1 compares 2 with 5 and does not swap. With 2 comparisons, $a = [2, 5, 6, 7, 8, 9, 3]$ and $r = [0, 1, 0, 0, 1, 0, 1]$.

**Insert 4.** It goes to index 7, which is odd, so line L13 does not change $r[3]$. With $r[3] = 0$, node 7 is the right child of 3, so $d(7) = 3$. The join compares 7 with 4, swaps, and sets $r[7] = 1$. Next, 3 is the left child of 1 (as $r[1] = 1$), and 1 is the right child of 0, so $d(3) = 0$. The join compares 2 with 4 and stops. With 2 comparisons, $a = [2, 5, 6, 4, 8, 9, 3, 7]$ and $r = [0, 1, 0, 0, 1, 0, 1, 1]$.

**Sort.** Weak-heapsort of the same 8 keys does the build and then 7 sift-downs, each after the root key is swapped with the last key of the shrinking heap. It uses 18 comparisons in total. Dutton's bound for $n = 8$ is $8 \cdot 3 - 8 + 8 - 1 = 23$, and $\lceil \lg 8! \rceil = 16$.

## Correctness

The proof rests on one lemma about JOIN. If the subtree of $j$ is in weak-heap order and $a[i] \le a[y]$ for every $y \in L(j)$, then after JOIN$(i, j)$ the subtree of $j$ is still in weak-heap order and $a[i]$ is at most every key in it. In the no-swap case this is $a[i] \le a[j] \le R(j)$. In the swap case, the new $a[j]$ is the old $a[i]$, and after the flip its right subtree is the old $L(j)$. From the lemma:

- Build is correct by induction from the last index down. Each node is joined after all nodes of its subtree, and the earlier joins of the left-path nodes below $j$ already made $a[d(j)]$ at most every key of $L(j)$.
- Sift-down is correct by induction up the left path. After the join with a path node $s$, the root key is at most every key in the subtree of $s$, and that subtree is the left subtree of the next node up.
- Insert keeps the order except, at each step, between the moving key and its distinguished ancestors, and the loop removes that exception.

The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | comparisons, worst case | time, worst case |
|---|---|---|
| find-min | 0 | $O(1)$ |
| build | $n - 1$ | $O(n)$ |
| delete-min | $\lceil \lg n \rceil$ | $O(\log n)$ |
| insert | $\lceil \lg n \rceil$ | $O(\log n)$ |
| weak-heapsort | $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - 1$ | $O(n \log n)$ |
| space | | $n$ keys and $n$ bits |

**Build.** Line L6 runs once for each $j$ from $n - 1$ down to 1, and each JOIN is one comparison. During the build, a node's bit changes only when the node itself is joined, so when $j$ is processed all its proper ancestors still have $r = 0$. A node is then a left child exactly when its index is even, and the walk of D-ANCESTOR from $j = 2^t m$, with $m$ odd, takes $t$ steps. The sum of $t$ over all $j < n$ is less than $n$, so the build takes $O(n)$ time.

**Delete-min.** The left path from node 1 visits indices at least $1, 2, 4, \ldots$, so it has at most $\lfloor \lg (n - 1) \rfloor + 1 \le \lceil \lg n \rceil$ nodes in a heap of $n - 1$ keys, with one comparison each. A binary heap needs up to about $2 \lg n$ comparisons, two per level.

**Insert.** Each step of the loop moves to a distinguished ancestor, which is a proper ancestor, so there are at most $\lfloor \lg n \rfloor$ joins. The D-ANCESTOR walks of one insert are all on the path from the new leaf to the root, so the time is $O(\log n)$. In practice inserts are cheap: in a test with 4096 inserts, the mean was 1.0 comparisons per insert for increasing keys, 1.8 for random keys and 2.5 for decreasing keys. Edelkamp, Elmasry and Katajainen show that with a buffer for new keys and a bulk insert, insert takes $O(1)$ amortized time and delete-min keeps its $\lg n + O(1)$ comparisons.

**Weak-heapsort.** The build uses $n - 1$ comparisons, and the sift-down in a heap of $m$ keys uses at most $\lceil \lg m \rceil$, for $m = n - 1$ down to 2. So the total is at most $n - 1 + \sum_{m=2}^{n-1} \lceil \lg m \rceil$, which is Dutton's bound $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + n - 1$. The tests check this bound for every $n$ from 2 to 259. For $n = 1$ the formula gives $-1$, and the sort uses 0 comparisons. The bound is less than $n \lg n + 0.1n$.

## Variants

- **Max weak heap.** Reverse the order to get the form that Dutton used for sorting.
- **Relaxed weak heap.** Edelkamp, Elmasry and Katajainen allow a bounded number of nodes to violate the order, in the style of a [relaxed heap](/relaxed-heap/). This gives decrease-key in $O(1)$ worst-case time with few comparisons.
- **Weak heap with an insertion buffer.** A small buffer collects new keys, and a bulk insert moves them into the heap. Insert is then $O(1)$ amortized.
- **Forests of perfect weak heaps.** A weak heap with $2^k$ nodes and a full shape has the same order as a binomial tree of rank $k$, and JOIN is the link of two such trees. So a forest of these, in the style of a [binomial heap](/binomial-heap/), gives a meldable form.

## When to use it

Use a weak heap when the number of key comparisons is the cost that matters, for example when comparing two keys is much more expensive than moving them, as with long strings or keys that are computed. It is the base of [weak-heapsort](/weak-heapsort/), one of the [heapsort](/heapsort/) variants with the fewest comparisons. When comparisons are cheap, a plain [binary heap](/binary-heap/) or a [d-ary heap](/d-ary-heap/) is usually faster, because the reverse bits and the D-ANCESTOR walks add work and branches that the comparisons saved do not pay for.

## Pitfalls

- **Children from the bit.** The left child of $i$ is $2i + r[i]$, not $2i$. Code that ignores $r$ reads the wrong subtree. In the example, the left child of node 3 is 7 when $r[3] = 1$.
- **The root has no left child.** Node 0 has only the child 1, and $r[0]$ must stay 0. With $r[0] = 1$, node 0 would be its own child.
- **Stale bits on insert.** A new key at an even index $j$ is the first child of a node that was a leaf. That node may have an old bit of 1, which would make $j$ its right child. Line L13 resets the bit. Without the reset, the order can break.
- **Flip with the swap.** JOIN must flip $r[j]$ when, and only when, it swaps. A swap without the flip puts the old $a[i]$ above the old $R(j)$, whose keys may be smaller.
- **The sift-down path.** The path of SIFT-DOWN goes from node 1 down the left children. Going down by comparisons, as in a binary heap, gives a wrong result and also loses the saving.
- **Not a sorted left side.** The left subtree of a node may hold smaller keys. Do not use a weak heap as if each key were at most all keys below it; only the root has that property.

## Implementations

The Python version stores $a$ and $r$ as two lists and counts comparisons in `comparisons`, which the tests use to check the bounds. The function `weak_heapsort` sorts with the min form: it moves each minimum to the end of the shrinking heap, and reverses the result at the end.

## History

Dutton introduced the weak heap and weak-heapsort in BIT in 1993. Edelkamp and Wegener analyzed the number of comparisons of weak-heapsort in the worst and the average case in 2000. Edelkamp, Elmasry and Katajainen collected the variants and applications in 2012: the insertion buffer for $O(1)$ amortized insert, the relaxed weak heap for decrease-key, and the use of weak heaps in adaptive sorting and in shortest-path algorithms.

## References
