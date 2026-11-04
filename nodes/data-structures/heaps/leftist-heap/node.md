---
tag: Z662CN
kind: data-structure
slug: leftist-heap
name: Leftist heap
aliases:
- leftist tree
- leftist heaps
area: data-structures/heaps
level: advanced
summary: Binary heap tree that keeps the right spine short, so merge runs in O(log n).
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heaps}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [heap-property, binary-tree, priority-queue, induction]
see_also: [skew-heap, pairing-heap, binomial-heap, binary-heap, meldable-priority-queue, purely-functional-data-structure, randomized-heap, fibonacci-heap]
sources:
  - paper: Clark Allan Crane, Linear lists and priority queues as balanced binary trees, PhD thesis, Stanford University, 1972, technical report STAN-CS-72-259
    locator: the definition of leftist trees and the merge along the right paths
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the part on leftist trees and merging of priority queues
  - book: isbn:9780898711875
    title: Robert Endre Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 3 (Heaps), the section on leftist heaps
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Section 3.1 (Leftist heaps)
---

A leftist heap is a heap-ordered binary tree in which, at every node, the shortest path to an empty subtree goes through the right child. So the right spine of every subtree is short: a tree with $n$ nodes has a right spine of at most $\lg(n + 1)$ nodes. Two leftist heaps are merged by walking down their two right spines, which takes $O(\log n)$ time in the worst case, and insert and delete-min are merges. Clark Crane introduced the structure in 1972, and it is the simplest heap with a worst-case $O(\log n)$ merge.

## In plain words

A heap keeps the smallest item at the top, and every item is smaller than the items below it. To merge two such heaps, you can follow one path down each heap and zip the two paths together, keeping the smaller item at each step. The work is the length of the two paths.

A leftist heap makes the path on the right side short, on purpose. At each item, it keeps the "thin" side on the right and the "thick" side on the left. When a merge makes the right side too thick, it swaps the two sides. So the walk down the right side stays short, even when the heap holds a million items.

## The abstract type

A leftist heap implements the [meldable priority queue](/meldable-priority-queue/), and so the [priority queue](/priority-queue/), on a multiset of keys from a total order: `insert(H, k)`, `find-min(H)`, `delete-min(H)` and `meld(H1, H2)`, which destroys its inputs. This page uses a min-heap. Delete and decrease-key of an item given by a handle are possible with parent pointers, as in Variants.

## Representation

Each node $x$ holds a key, pointers $x.left$ and $x.right$, and a *rank* $x.s$. For an empty tree, $s(\mathrm{NIL}) = 0$. For a node, the rank is the number of nodes on the right spine of its subtree: the path that starts at $x$ and always goes to the right child. Knuth calls it $\mathrm{DIST}$, and other books call it the null path length. The heap is a pointer $H.root$ and a count $n$.

**Invariant.**

- **(L1) Heap order.** The key of each node is at least the key of its parent.
- **(L2) Leftist property.** At each node $x$, $s(x.left) \ge s(x.right)$.
- **(L3) Ranks.** At each node $x$, $x.s = s(x.right) + 1$.

By (L2) and (L3), the rank of $x$ is the length of a shortest path from $x$ down to an empty subtree.

**Lemma (short right spine).** A leftist tree whose root has rank $r$ has at least $2^r - 1$ nodes. So $r \le \lg(n + 1)$.

*Proof.* By induction on $r$. For $r = 0$ the tree is empty, with $2^0 - 1 = 0$ nodes. For $r \ge 1$, the right subtree has rank $r - 1$ by (L3), and the left subtree has rank at least $r - 1$ by (L2). A leftist tree of rank at least $r - 1$ contains, from its root, a full binary tree of height $r - 1$, because every path from the root to an empty subtree has at least $r - 1$ nodes. So each subtree has at least $2^{r-1} - 1$ nodes, and the whole tree has at least $2(2^{r-1} - 1) + 1 = 2^r - 1$. $\square$

The tree is not balanced: its left spine can have $\Theta(n)$ nodes. Only the right spine is short.

## Operations

```pseudo id=main
MERGE(a, b)                             ▷ roots of two leftist heaps; either may be NIL
L1  if a = NIL then return b; if b = NIL then return a
L2  if b.key < a.key then swap a and b  ▷ a has the smaller root
L3  a.right ← MERGE(a.right, b)
L4  if s(a.left) < s(a.right) then swap a.left and a.right
L5  a.s ← s(a.right) + 1
L6  return a

INSERT(H, k)
L7  H.root ← MERGE(H.root, a new node with key k and rank 1)

DELETE-MIN(H)                           ▷ H is not empty
L8  r ← H.root; H.root ← MERGE(r.left, r.right)
L9  return r.key
```

**Merge** (lines L1 to L6) keeps the smaller root, merges the other heap into its right subtree, and then swaps the children if the right one now has the larger rank. Each call goes one step down the right spine of $a$ or of $b$, so there are at most $s(a) + s(b) + 1$ calls. By the lemma, this is at most $2 \lg(n + 1) + 1$, where $n$ is the total number of nodes, and each call does $O(1)$ work.

**Insert** (line L7) merges with a heap of one node.

**Find-min** returns $H.root.key$.

**Delete-min** (lines L8 and L9) removes the root and merges its two subtrees.

**Build from $n$ keys.** Put $n$ one-node heaps in a FIFO queue. While the queue holds two or more heaps, remove the first two, merge them, and add the result at the end. This takes $O(n)$ time, as shown in Complexity. Repeated insertion takes $O(n \log n)$.

## Example

Write a tree as key(left, right), with "-" for an empty subtree and a leaf as its key alone. Insert 5, 3, 8, 1, 7, 2 into an empty heap.

| operation | merge steps | tree after | rank of root |
|---|---|---|---|
| insert 5 | | 5 | 1 |
| insert 3 | 3 wins; 5 goes right; swap, since s(-) = 0 < 1 | 3(5, -) | 1 |
| insert 8 | 3 wins; merge 8 into the empty right subtree | 3(5, 8) | 2 |
| insert 1 | 1 wins; 3(5, 8) goes right; swap | 1(3(5, 8), -) | 1 |
| insert 7 | 1 wins; merge 7 into the empty right subtree | 1(3(5, 8), 7) | 2 |
| insert 2 | 1 wins; merge(7, 2): 2 wins, 7 goes right, swap to 2(7, -); 2(7, -) is the right child of 1 | 1(3(5, 8), 2(7, -)) | 2 |

Delete-min returns 1 and merges 3(5, 8) with 2(7, -). The root 2 wins, and 3(5, 8) merges into its empty right subtree. Now the right child has rank 2 and the left child 7 has rank 1, so they swap: 2(3(5, 8), 7). A second delete-min returns 2 and merges 3(5, 8) with 7. The root 3 wins, and merge(8, 7) gives 7(8, -), of rank 1. The left child 5 has rank 1, so there is no swap: 3(5, 7(8, -)).

**A meld.** Merge $x$ = 1(5(8, 7), 2(3, -)) of 6 nodes with $y$ = 4(6, 9(10, -)) of 4 nodes.

1. 1 < 4, so 1 is the root. Merge its right subtree 2(3, -) with $y$.
2. 2 < 4, so 2 is the root of that merge. Its right subtree is empty, so merge(-, $y$) returns $y$, of rank 2.
3. At 2: the right child $y$ has rank 2 and the left child 3 has rank 1. Swap: 2(4(6, 9(10, -)), 3), of rank 2.
4. At 1: the left child 5(8, 7) has rank 2 and the right child has rank 2. No swap. The rank of 1 is 3.

The result is 1(5(8, 7), 2(4(6, 9(10, -)), 3)), with 10 nodes and root rank $3 \le \lg 11 \approx 3.46$. The merge did 2 key comparisons, one per node on the right spine of $x$ that it passed.

## Correctness

MERGE returns a leftist heap with the union of the keys of its inputs. The proof is by induction on $s(a) + s(b)$. The recursive call returns a leftist heap by induction. Line L2 makes the root the smallest key of both heaps, so heap order holds at the root. Line L4 makes the leftist property hold at the root, and line L5 makes its rank correct. All other nodes keep their subtrees. Insert and delete-min are merges, and delete-min removes the root, which holds a smallest key by heap order. The full proof, with the bound on the rank, is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case |
|---|---|
| find-min | $O(1)$ |
| insert | $O(\log n)$ |
| delete-min | $O(\log n)$ |
| meld | $O(\log n)$, with $n$ the total size |
| build from $n$ keys | $O(n)$ |
| space | $\Theta(n)$: a key, two pointers and a small rank per node |

**Merge.** The calls of MERGE go down the right spines of the two heaps. Each call takes one node from one of them, so the number of calls is at most $s(a) + s(b) + 1 \le \lg(n_a + 1) + \lg(n_b + 1) + 1 \le 2 \lg(n + 1) + 1$. Insert and delete-min each do one merge.

**Build.** The queue processes the heaps in rounds: in round $j$, it merges pairs of heaps made in round $j - 1$, so each heap of round $j$ has at most $2^j$ nodes, and round $j$ does at most $n/2^j + 1$ merges, each of cost $O(j)$. The total is $O\left(\sum_{j \ge 1} (n/2^j + 1)\, j\right) = O(n)$, because $\sum_j j/2^j = 2$ and there are $O(\log n)$ rounds.

**Comparison with other heaps.** A [binary heap](/binary-heap/) in an array needs $\Theta(n)$ time to meld. A [binomial heap](/binomial-heap/) also melds in $O(\log n)$ worst-case time, with more code. A [skew heap](/skew-heap/) drops the ranks and gets $O(\log n)$ amortized time. A [pairing heap](/pairing-heap/) or a [Fibonacci heap](/fibonacci-heap/) melds in $O(1)$.

## Variants

- **Weight-biased leftist heap.** Cho and Sahni use the size of a subtree in place of its rank: at each node, the left subtree has at least as many nodes as the right one. The right spine is again at most $\lg(n + 1)$ long, and the merge can fix the sizes on the way down, in one top-down pass.
- **Purely functional leftist heap.** With MERGE written as a recursive function that builds new nodes, the old heap stays valid, and each operation copies only $O(\log n)$ nodes. Okasaki uses this as his first example of a [purely functional data structure](/purely-functional-data-structure/).
- **Delete and decrease-key.** With a parent pointer in each node, an item can be cut out and its two subtrees merged back. The ranks on the path from the cut to the root must then be fixed, and the walk can stop at the first node whose rank does not change. Tarjan describes this, and the walk takes $O(\log n)$ time.
- **Skew heap.** The [skew heap](/skew-heap/) swaps the children at every step of the merge without checking ranks. It is the self-adjusting form of the leftist heap.

## When to use it

Use a leftist heap when you need a meldable priority queue with worst-case $O(\log n)$ bounds and want the shortest code, or a persistent heap in a functional language. Merge, insert and delete-min are each a few lines. If meld is not needed, a [binary heap](/binary-heap/) in an array is faster and smaller. If decrease-key dominates, as in [Dijkstra's algorithm](/dijkstra/) on dense graphs, a [pairing heap](/pairing-heap/) or a [Fibonacci heap](/fibonacci-heap/) is better.

## Pitfalls

- **Swap on the wrong side.** The swap of line L4 must keep the subtree of the larger rank on the left. If it compares sizes or heights instead of ranks, the right spine can become long, and the $O(\log n)$ bound fails.
- **Rank not updated.** Line L5 must run after the swap. If it uses the old right child, the ranks become wrong and a later merge can make a long right spine without an error.
- **Recursion depth.** The recursion of MERGE has depth at most $2\lg(n+1) + 1$, so it is safe. A recursive *traversal* of the whole tree is not safe, because the left spine can have $\Theta(n)$ nodes, for example after inserts in decreasing order.
- **Build by repeated insertion.** Building a heap from $n$ keys by $n$ inserts takes $O(n \log n)$ time. The FIFO queue of merges takes $O(n)$.
- **Meld is destructive.** In the pointer form, meld reuses the nodes of both heaps. The old heaps must not be used after it.

## Implementations

The Python version does MERGE with an explicit stack: it walks down the two right spines, then fixes the children and the ranks on the way back, in the order of lines L3 to L6. The constructor builds a heap with the FIFO queue of merges. Its `check_invariant` method checks heap order, the leftist property, the ranks, the count and the bound $s(\mathrm{root}) \le \lg(n+1)$.

## History

Clark Crane described leftist trees in his 1972 Stanford thesis, as a way to make priority queues that can be merged. Knuth presented them in Volume 3 of The Art of Computer Programming in 1973. Tarjan used them in his 1983 book as a basic meldable heap. Sleator and Tarjan's [skew heap](/skew-heap/) of 1986 is the self-adjusting form. Okasaki made the leftist heap the first example of his 1998 book on purely functional data structures.

## References
