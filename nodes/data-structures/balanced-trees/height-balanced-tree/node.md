---
tag: J77RXK
kind: definition
slug: height-balanced-tree
name: Height-balanced tree
aliases:
- height-balanced binary tree
area: data-structures/balanced-trees
level: intro
summary: A binary tree in which the subtrees of every node differ in height by at most a fixed bound.
prereqs: [binary-tree, recursion]
see_also: [balance-factor, avl-tree, avl-height-theorem, balanced-binary-search-tree, weight-balanced-tree, red-black-tree, tree-rebalancing]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (the definition of a balanced tree and the height bound of Theorem A)
  - paper: "G. M. Adelson-Velsky and E. M. Landis, An algorithm for the organization of information, Doklady Akademii Nauk SSSR 146, 1962 (English translation in Soviet Mathematics Doklady 3, 1962)"
    locator: the trees with subtree heights differing by at most one
  - paper: "Caxton C. Foster, A generalization of AVL trees, Communications of the ACM 16(8), 1973"
    locator: HB(k) trees, in which the subtree heights may differ by at most k
---

A binary tree is height-balanced when, at every node, the heights of the left and right subtrees differ by at most a fixed bound $k$. With $k = 1$ these are the trees of the [AVL tree](/avl-tree/), and "height-balanced" without a number usually means this case. The condition must hold at every node, not only at the root. For each fixed $k$, a height-balanced tree with $n$ nodes has height $O(\log n)$; for $k = 1$ the height is less than $1.4405 \lg(n + 2)$.

## Definition

Let $h(t)$ be the height of a binary tree $t$: the number of nodes on a longest path from the root down, with $h(\text{nil}) = 0$. Let $k \ge 1$ be an integer. A binary tree $t$ is **height-balanced with bound $k$**, or an HB($k$) tree, if

- $t$ is nil, or
- $|h(t.left) - h(t.right)| \le k$, and both $t.left$ and $t.right$ are HB($k$) trees.

The difference $h(t.right) - h(t.left)$ is the [balance factor](/balance-factor/) of the root, so a tree is HB($k$) exactly when every node has a balance factor in $\{-k, \ldots, k\}$. A **height-balanced tree**, with no bound given, is an HB(1) tree. The definition does not mention keys; an AVL tree is a binary search tree that is also height-balanced.

The definition gives a test in linear time: compute the heights bottom-up, $h(x) = 1 + \max(h(x.left), h(x.right))$, and check the difference at each node. Computing the height of each subtree from scratch at each node, instead, takes $\Theta(n^2)$ time on a path-shaped tree.

**Height bound.** Let $N_k(h)$ be the least number of nodes of an HB($k$) tree of height $h$. A smallest tree of height $h \ge 2$ has one subtree of height $h - 1$ and one of height $\max(0, h - 1 - k)$, both smallest, so $N_k(h) = 1 + N_k(h - 1) + N_k(\max(0, h - 1 - k))$. For $k = 1$ this gives $N_1(h) = F_{h+2} - 1$ with the Fibonacci numbers (see the [AVL height bound](/avl-height-theorem/)). For each $k$, $N_k(h)$ grows like $r^h$, where $r > 1$ is the largest root of $x^{k+1} = x^k + 1$, so the height is at most $\log_r n + O(1)$, which is $O(\log n)$.

## Examples and non-examples

- **The empty tree and a single node** are height-balanced.
- **A perfect binary tree** with $2^h - 1$ nodes is height-balanced: every node has two subtrees of the same height.
- **A complete binary tree,** as used by a binary heap, is height-balanced: at each node the subtree heights differ by at most 1.
- **The chain of three nodes** 1, 2, 3, each the right child of the one before, is not height-balanced: the root has subtrees of heights 0 and 2. It is an HB(2) tree, but the chain of four nodes is not.
- **A tree balanced only at the root.** Take a root whose left and right subtrees are both chains of three nodes. Both subtrees have height 3, so the root is fine, but the top of each chain has subtrees of heights 0 and 2. This tree is not height-balanced.
- **Fibonacci trees.** The tree with a root, a Fibonacci tree of height $h - 1$ on one side and one of height $h - 2$ on the other, is height-balanced and has the fewest nodes for its height: 1, 2, 4, 7, 12, 20 nodes for heights 1 to 6.
- **Few nodes but not balanced in weight.** In the Fibonacci tree of height 6, the root has 12 nodes on one side and 7 on the other. Height balance does not bound the ratio of the subtree sizes.

## Related definitions

- **[Balance factor](/balance-factor/).** The height difference at one node; height balance says that all balance factors are small.
- **[AVL tree](/avl-tree/).** A binary search tree that stays HB(1) under insertion and deletion, by [rotations](/tree-rotation/).
- **[Weight-balanced tree](/weight-balanced-tree/).** The analogous condition on the sizes of the subtrees instead of their heights. A weight-balanced tree has height $O(\log n)$ too, but it need not be height-balanced, and the converse also fails.
- **[Red-black tree](/red-black-tree/).** Balanced by a count of black nodes on paths, which allows one subtree to be up to about twice as tall as the other. Every AVL tree can be colored as a red-black tree.
- **[Balanced binary search tree](/balanced-binary-search-tree/).** The general idea: any scheme that keeps the height $O(\log n)$. Height balance is one such scheme.

## References
