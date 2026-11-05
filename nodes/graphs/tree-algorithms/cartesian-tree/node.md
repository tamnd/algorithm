---
tag: 3X8X1H
kind: data-structure
slug: cartesian-tree
name: Cartesian tree
aliases:
- Cartesian tree of an array
area: graphs/tree-algorithms
level: intro
summary: Binary tree whose inorder traversal is the array and which is heap-ordered by value.
model: comparison-model
complexity:
  vars: {n: the length of the array}
  time: {build: Θ(n), query: O(1)}
  space: {extra: Θ(n)}
prereqs: [binary-tree, inorder-traversal, heap-property, stack]
see_also: [treap, range-minimum-query, rmq-lca-equivalence, lowest-common-ancestor, monotonic-stack, fischer-heun-rmq, largest-rectangle-in-histogram, suffix-tree]
sources:
  - paper: doi:10.1145/358841.358852
    title: "Jean Vuillemin, A unifying look at data structures, Communications of the ACM 23(4) (1980), 229-239"
    locator: the definition of the Cartesian tree of a set of points, with one coordinate in search-tree order and the other in heap order
  - paper: doi:10.1145/800057.808675
    title: "Harold N. Gabow, Jon Louis Bentley and Robert E. Tarjan, Scaling and related techniques for geometry problems, STOC 1984, 135-143"
    locator: the use of the Cartesian tree to reduce range minimum queries to lowest common ancestor queries, and its linear-time construction
  - paper: doi:10.1007/10719839_9
    title: "Michael A. Bender and Martin Farach-Colton, The LCA Problem Revisited, LATIN 2000: Theoretical Informatics, LNCS 1776, 88-94"
    locator: the reduction from RMQ to LCA through the Cartesian tree
  - url: https://cp-algorithms.com/graph/rmq_linear.html
    title: cp-algorithms, Solve RMQ by finding LCA
    locator: the construction of the Cartesian tree with a stack in O(n) and the reduction of RMQ to LCA
---

The Cartesian tree of an array $A[0..n-1]$ is the [binary tree](/binary-tree/) whose root is the position of the minimum of $A$, whose left subtree is the Cartesian tree of the part before the minimum, and whose right subtree is the Cartesian tree of the part after it. So its [inorder traversal](/inorder-traversal/) lists the positions $0, 1, \ldots, n-1$, and along every root-to-leaf path the values do not decrease, like a heap. A stack builds it in $\Theta(n)$ time with fewer than $2n$ comparisons. Its main use is that the minimum of a range $A[i..j]$ sits at the [lowest common ancestor](/lowest-common-ancestor/) of $i$ and $j$, which turns [range minimum queries](/range-minimum-query/) into LCA queries. A [treap](/treap/) is a Cartesian tree on (key, priority) pairs.

## In plain words

Take a row of numbers. Find the smallest one and make it the top of a tree. Everything to its left becomes its left branch, and everything to its right becomes its right branch. Then do the same in each branch: its smallest number goes on top of that branch, and so on until each number has its place.

The tree has two orders at once. Read it from left to right and you get the row back in its order. Walk from the top down and the numbers never get smaller. So, for any stretch of the row, the smallest number in that stretch is the point where the paths up from its two ends meet. The tree can be built in one pass over the row, using a pile of the numbers that are still waiting for a right branch.

## The abstract type

A Cartesian tree is a static structure. It stores a sequence $A[0..n-1]$ of values from a totally ordered set and supports:

- $\mathrm{build}(A)$: make the tree.
- $\mathrm{root}$, $\mathrm{left}(i)$, $\mathrm{right}(i)$, $\mathrm{parent}(i)$: move in the tree.
- $\mathrm{rmq}(i, j)$ for $i \le j$: the position of the leftmost minimum of $A[i..j]$, answered as $\mathrm{lca}(i, j)$.
- $\mathrm{append}(x)$: add a value at the end. The build below is online, so this is supported in $O(1)$ amortized time.

## Representation

The nodes are the positions $0, \ldots, n-1$, so the tree is rooted and its nodes are numbered by position; the values $A[i]$ sit on the nodes, and the edges have no weights. Four arrays of $n$ integers hold $parent$, $left$ and $right$, with $-1$ for a missing node, and an integer holds the root.

**Ties.** With equal values, the tree is defined with the leftmost minimum as root. This is the same as comparing the pairs $(A[i], i)$, which are distinct, so the tree is unique. Each node $x$ then satisfies the two rules

1. (inorder) every node in the left subtree of $x$ has a smaller position than $x$, and every node in the right subtree a larger one;
2. (heap) $A[parent(x)] \le A[x]$, and $A[parent(x)] < A[x]$ when $x$ is a left child.

**Subtrees are ranges.** By rule 1 the subtree of $x$ is a contiguous range of positions $[lo(x), hi(x)]$, and by rule 2 $x$ is the leftmost minimum of $A[lo(x)..hi(x)]$. The *right spine*, the path from the root that always goes right, is the list of the positions $i$ for which $A[i]$ is smaller than every value after it: the suffix minima.

## Operations

The build reads the array from left to right and keeps the right spine of the tree of the prefix read so far on a stack, with the root at the bottom. The values on the stack increase from bottom to top.

```pseudo id=main
BUILD-CARTESIAN(A[0..n-1])
L1  S ← empty stack                                  ▷ the right spine, root at the bottom
L2  for i ← 0 to n - 1 do
L3      last ← NIL
L4      while S is not empty and A[top(S)] > A[i] do
L5          last ← pop S                             ▷ leaves the right spine
L6      left[i] ← last;  if last ≠ NIL then parent[last] ← i
L7      if S is not empty then right[top(S)] ← i;  parent[i] ← top(S)
L8      push i on S
L9  root ← bottom of S, or NIL if n = 0
```

Node $i$ is larger in position than every node so far, so by rule 1 it must go on the right spine, at the bottom of it. Lines L4 and L5 pop the spine nodes with a larger value: by rule 2 they must lie below $i$. The last of them, the highest one, becomes the left child of $i$ in line L6, and it brings along its whole subtree. The remaining top of the stack, whose value is at most $A[i]$, takes $i$ as its new right child in line L7. Its old right child, if any, was popped, and is now inside the left subtree of $i$.

**Range minimum.** For $i \le j$, the leftmost minimum of $A[i..j]$ is $\mathrm{lca}(i, j)$. Go down from the root toward $i$. At a node $x$ outside $[i, j]$, both $i$ and $j$ are on the same side of $x$, so the paths to $i$ and to $j$ go on together. At the first node $x$ with $i \le x \le j$, $i$ is $x$ or in its left subtree and $j$ is $x$ or in its right subtree, so the paths split there and $x = \mathrm{lca}(i, j)$. The range of $x$ contains $[i, j]$, and $x$ is the leftmost minimum of its range, so it is also the leftmost minimum of $A[i..j]$. With a linear-time LCA structure, such as [Bender and Farach-Colton's](/bender-farach-colton-rmq/), each query takes $O(1)$ time. The code below climbs from both ends by depth, which takes $O(h)$ time.

**Append.** Adding $A[n]$ is one more round of lines L3 to L8. The spine shrinks by the number of pops, so $n$ appends cost $O(n)$ in total.

## Example

$A = [3, 1, 4, 1, 5, 9, 2, 6]$, positions $0, \ldots, 7$. The build, with the stack bottom to top after each round:

| $i$ | $A[i]$ | popped | $left[i]$ | new parent of $i$ | stack after |
|---|---|---|---|---|---|
| 0 | 3 | none | NIL | none | 0 |
| 1 | 1 | 0 | 0 | none | 1 |
| 2 | 4 | none | NIL | 1 | 1, 2 |
| 3 | 1 | 2 | 2 | 1 | 1, 3 |
| 4 | 5 | none | NIL | 3 | 1, 3, 4 |
| 5 | 9 | none | NIL | 4 | 1, 3, 4, 5 |
| 6 | 2 | 5, 4 | 4 | 3 | 1, 3, 6 |
| 7 | 6 | none | NIL | 6 | 1, 3, 6, 7 |

At $i = 3$ the value 1 equals $A[1]$, and the test of line L4 is strict, so 1 stays and 3 becomes its right child: the leftmost minimum is the root. At $i = 6$ the nodes 5 and 4 are popped, and 4, with its right child 5, becomes the left child of 6. The tree, with values in brackets:

```
          1 [1]
         /     \
     0 [3]     3 [1]
              /     \
          2 [4]     6 [2]
                   /     \
               4 [5]     7 [6]
                   \
                   5 [9]
```

$parent = [1, -1, 3, 1, 6, 4, 3, 6]$, $left = [-1, 0, -1, 2, -1, -1, 4, -1]$, $right = [-1, 3, -1, 6, 5, -1, 7, -1]$, and the depths are $[1, 0, 2, 1, 3, 4, 2, 3]$. The inorder is $0, 1, \ldots, 7$. Queries: $\mathrm{rmq}(4, 7) = \mathrm{lca}(4, 7) = 6$, with $A[6] = 2$; $\mathrm{rmq}(2, 5) = \mathrm{lca}(2, 5) = 3$; $\mathrm{rmq}(0, 7) = 1$, the leftmost of the two 1s.

Small shapes. For $n = 0$ the tree is empty, and for $n = 1$ it is one node. An increasing array gives a path that goes right at every step, and a decreasing array a path that goes left; both have height $n - 1$, and the build pushes and pops at most $n$ times either way. An array of equal values is a right path too, because of the tie rule. The array $[5, 0, 5]$ gives the star shape that a binary tree allows: root 1 with the leaves 0 and 2.

## Correctness

Write $C(A)$ for the tree defined by the recursion: the leftmost minimum $m$ at the root, $C(A[0..m-1])$ on the left, $C(A[m+1..n-1])$ on the right. A tree on the positions $0, \ldots, n-1$ that satisfies rules 1 and 2 is exactly $C(A)$, by induction on $n$: rule 2 forces the root to be the leftmost minimum, and rule 1 forces the two subtrees to be the trees of the two sides. The invariant of BUILD-CARTESIAN is: after round $i$, the arrays describe $C(A[0..i])$, and the stack holds its right spine from the root to the deepest node. The proof file below shows that one round of lines L3 to L8 keeps this invariant, and that the leftmost minimum of $A[i..j]$ is $\mathrm{lca}(i, j)$.

## Complexity

- **Build.** Each position is pushed once in line L8 and popped at most once in line L5. So the loop of line L4 runs at most $n$ times in total over all rounds, and each test of line L4 either pops or ends a round. The time is $\Theta(n)$. Each test of line L4 on a non-empty stack is one comparison; it either pops, at most $n - 1$ times in all because the root is never popped, or ends the round, at most once in each of the rounds $1, \ldots, n-1$. So there are at most $2n - 2$ comparisons, and the extra space is the stack, at most $n$ entries.
- **Queries.** Moving in the tree costs $O(1)$. With an $O(n)$-time LCA structure on top, $\mathrm{rmq}$ costs $O(1)$. By depth climbing, as in the reference code, it costs $O(h)$, where $h$ is between $\lceil \log_2(n+1) \rceil - 1$ and $n - 1$.
- **Lower bound.** In the [comparison model](/comparison-model/), building the tree needs at least $n - 1$ comparisons for $n \ge 1$, since the root is the minimum and finding the minimum needs $n - 1$ comparisons. So the build is optimal up to a factor of 2.
- **Space.** Three arrays of $n$ integers.

## Variants

- **Max-Cartesian tree.** Reverse the order: the maximum at the root. It answers range maximum queries.
- **[Treap](/treap/).** Vuillemin's original form: a set of points $(x, y)$ in a tree that is a search tree by $x$ and a heap by $y$. With random $y$ values it is a balanced search tree in expectation.
- **[Implicit treap](/implicit-treap/).** A Cartesian tree on positions with random priorities, which supports split, merge and reversal of ranges of a sequence.
- **Shape as a fingerprint.** Two arrays have the same Cartesian tree shape if and only if every range has its leftmost minimum at the same position in both. The [Fischer and Heun RMQ](/fischer-heun-rmq/) encodes the shape of each small block in $2b$ bits and shares one table per shape; there are only the Catalan number $C_b$ of them.
- **The LCP Cartesian tree.** The Cartesian tree of the [LCP array](/lcp-array/) of a [suffix array](/suffix-array/) has the shape of the internal nodes of the [suffix tree](/suffix-tree/); building it with the same stack gives the suffix tree in linear time.
- **Nearest smaller values.** The same stack is the [monotonic stack](/monotonic-stack/) that finds, for each $i$, the nearest position on the left with a value at most $A[i]$: it is the top of the stack after the pops of round $i$, and it is the parent of $i$ when $i$ is a right child.

## When to use it

Use a Cartesian tree when a problem asks about the minimum (or maximum) of ranges of a fixed array and the answer needs structure, not only a value: the [largest rectangle in a histogram](/largest-rectangle-in-histogram/) is the best over the nodes $x$ of $A[x] \cdot (hi(x) - lo(x) + 1)$; "for each element, the largest range in which it is the minimum" is its subtree range; divide and conquer at the minimum becomes a walk of the tree. For plain RMQ with $O(1)$ queries, a [sparse table](/sparse-table/) is simpler and needs $O(n \log n)$ space; the Cartesian tree plus a linear LCA structure, or Fischer and Heun's method, reaches $O(n)$ space.

## Pitfalls

- **Ties.** With $\ge$ instead of $>$ in line L4, equal values pop each other and the rightmost minimum becomes the root. Either rule gives a valid tree, but the answer to $\mathrm{rmq}$ and the shape change, and code that mixes the two disagrees on arrays with repeated values.
- **Recursion.** The recursive definition, done literally, takes $\Theta(n^2)$ time on a sorted array, since each step scans for the minimum, and its recursion is $n$ levels deep. Use the stack build.
- **Deep trees.** A sorted input gives a path of height $n - 1$. Any later walk of the tree must be iterative, and LCA by climbing then costs $\Theta(n)$ per query.
- **Forgetting the parent of the popped node.** Line L6 must also set $parent[last] \gets i$; the popped node's old parent was on the spine and is no longer its parent.
- **Positions, not values.** The nodes are positions. Storing values and searching for them by value fails as soon as a value repeats.

## Implementations

## History

Vuillemin introduced the Cartesian tree in 1980 for a set of points in the plane, as a tree that is ordered by one coordinate and heap-ordered by the other, and used it in a unified view of data structures. Gabow, Bentley and Tarjan used Cartesian trees in 1984 to reduce range minimum queries to lowest common ancestor queries, which, with the linear-time LCA algorithm of Harel and Tarjan, gave $O(n)$ preprocessing and $O(1)$ query time. Seidel and Aragon's treaps (1989, 1996) are Cartesian trees with random priorities. Bender and Farach-Colton (2000) used the same reduction in their simple RMQ and LCA method.

## References
