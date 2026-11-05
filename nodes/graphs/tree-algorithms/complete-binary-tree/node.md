---
tag: VZ3WQZ
kind: definition
slug: complete-binary-tree
name: Complete binary tree
aliases:
- nearly complete binary tree
- heap-shaped tree
area: graphs/tree-algorithms
level: intro
summary: A binary tree in which every level is full except possibly the last, which is filled from left to right.
prereqs: [binary-tree]
see_also: [binary-heap, heap, heapsort, d-ary-heap, level-order-traversal, segment-tree, binary-tree, threaded-binary-tree]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority Queues), the complete binary tree, its array representation with the parent of k at k/2, and the height bound lg N
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.1 (Heaps), the nearly complete binary tree in an array with PARENT, LEFT and RIGHT; Appendix B.5.3, where complete means perfect
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.5 (Path Length), the complete binary tree with nodes numbered 1 to n and the children of k at 2k and 2k+1
---

A complete binary tree is a [binary tree](/binary-tree/) in which every level is full except perhaps the last one, and the nodes of the last level sit as far left as possible. For each $n$ there is exactly one such shape, and it has height $\lfloor \log_2 n \rfloor$, the least possible. Its nodes, numbered level by level from left to right, fill an array with no gaps, and a node's parent and children are found by arithmetic on its index, so no pointers are stored. This is the shape of a [binary heap](/binary-heap/).

## Definition

Number the positions of an infinite binary tree level by level and, within a level, from left to right, starting with 0 at the root. So the children of position $i$ are $2i + 1$ and $2i + 2$, and the parent of position $i \ge 1$ is $\lfloor (i - 1)/2 \rfloor$.

A *complete binary tree* with $n \ge 0$ nodes is the binary tree whose nodes occupy exactly the positions $0, 1, \ldots, n - 1$. Equivalently, a binary tree of height $h$ is complete if levels $0, \ldots, h - 1$ hold $2^0, \ldots, 2^{h-1}$ nodes, and the nodes of level $h$ are the leftmost ones of that level.

With 1-based numbering, as in CLRS Section 6.1, Sedgewick and Wayne Section 2.4 and Knuth Section 2.3.4.5, the root is 1, the children of $k$ are $2k$ and $2k + 1$, and the parent of $k \ge 2$ is $\lfloor k / 2 \rfloor$. This page uses 0-based numbering, as Python arrays do.

**Facts.** For a complete binary tree with $n \ge 1$ nodes:

1. The height is $h = \lfloor \log_2 n \rfloor$, and position $i$ is at depth $\lfloor \log_2 (i + 1) \rfloor$.
2. The leaves are the positions $\lfloor n/2 \rfloor, \ldots, n - 1$, so there are $\lceil n/2 \rceil$ leaves. Position $i$ is internal exactly when $2i + 1 < n$.
3. At most one node has exactly one child: position $(n - 2)/2$ when $n$ is even, and that child is a left child.
4. The subtree of any node is again complete, and of the two subtrees of the root, at least one is perfect. Each subtree of the root has at most $\lfloor 2n/3 \rfloor$ nodes, with near-equality when the last level is exactly half full (CLRS uses this bound in the analysis of MAX-HEAPIFY).

**Terminology.** Books disagree. CLRS calls this shape a *nearly complete* binary tree and uses *complete* for a [binary tree](/binary-tree/) whose levels are all full, which is called *perfect* here. Some authors use "complete" to mean full, that is, each node has 0 or 2 children. When a text says "complete", check which of the three it means.

## Examples and non-examples

The nodes are numbered by position, and the trees are unweighted.

**Ten nodes.** Positions $0, \ldots, 9$:

```
                0
           /         \
         1             2
       /   \         /   \
      3     4       5     6
     / \   /
    7   8 9
```

The height is $3 = \lfloor \log_2 10 \rfloor$. Levels 0, 1 and 2 are full, and level 3 holds the three leftmost positions 7, 8 and 9. The leaves are positions 5 to 9, which is $\lceil 10/2 \rceil = 5$ leaves. Node 4 has one child, 9, its left child. The parent of 9 is $\lfloor 8/2 \rfloor = 4$. The left subtree of the root has the 6 nodes $\{1, 3, 4, 7, 8, 9\}$ and the right subtree is the perfect tree $\{2, 5, 6\}$.

Small cases:

- **Empty and one node.** The empty tree is complete. A single node is complete, with height 0.
- **Paths.** A path is complete only for $n \le 2$: the root with a left child is complete, the root with a right child is not.
- **Stars.** A star with $n - 1 \ge 3$ leaves is not a binary tree. The only complete trees in which one node is adjacent to all others are those with $n \le 3$.
- **Perfect trees.** For $n = 2^{h+1} - 1$ the complete tree is perfect: 1, 3, 7, 15 nodes.

Non-examples:

- **A gap in the last level.** Nodes at positions $0, 1, 2, 3, 5$: level 2 has a node at position 5 but not at position 4. Every level but the last is full, but the last is not filled from the left.
- **A short level above the last.** Positions $0, 1, 3$: node 3 is at depth 2 while level 1 lacks position 2.
- **The tree in [binary tree](/binary-tree/).** There node 2 has a right child but no left child, so the positions in use are $0, 1, 2, 3, 4, 6$, with 5 missing.

**A test.** A binary tree with $n$ nodes is complete if and only if, after giving the root position 0 and the children of position $i$ the positions $2i + 1$ and $2i + 2$, every position is less than $n$. A [level-order traversal](/level-order-traversal/) that records the positions checks this in $O(n)$ time.

## Related definitions

- **[Binary heap](/binary-heap/).** A complete binary tree stored in an array with keys in heap order. Insertion fills position $n$ and deletion empties position $n - 1$, so the shape stays complete, and both take $O(\log n)$ steps because the height is $\lfloor \log_2 n \rfloor$.
- **[d-ary heap](/d-ary-heap/).** The same layout with $d$ children per node: the children of $i$ are $di + 1, \ldots, di + d$ and the parent is $\lfloor (i - 1)/d \rfloor$.
- **Perfect binary tree.** All levels full, $n = 2^{h+1} - 1$. Each perfect tree is complete; a complete tree is perfect exactly when $n + 1$ is a power of 2.
- **[Segment tree](/segment-tree/).** The array form of a segment tree over $2^k$ leaves uses the 1-based layout of a perfect binary tree, and for other sizes many implementations pad to the next power of 2.
- **Implicit data structure.** A complete binary tree is the standard example of a structure whose links are computed rather than stored.

### History

The array layout of a complete binary tree is due to J. W. J. Williams, who introduced it for heapsort in 1964, with the children of position $k$ at $2k$ and $2k + 1$.

## References
