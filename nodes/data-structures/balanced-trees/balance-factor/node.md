---
tag: 0AS1W0
kind: definition
slug: balance-factor
name: Balance factor
aliases:
- node balance
area: data-structures/balanced-trees
level: core
summary: The height of a node's right subtree minus the height of its left subtree, stored or computed to decide when to rebalance.
prereqs: [binary-tree, binary-search-tree]
see_also: [avl-tree, height-balanced-tree, avl-height-theorem, tree-rotation, tree-rebalancing, wavl-tree, black-height]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (the balance factor B(P) = height of right subtree minus height of left subtree, and Algorithm A)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13 problems, AVL trees
  - paper: "G. M. Adelson-Velsky and E. M. Landis, An algorithm for the organization of information, Doklady Akademii Nauk SSSR 146, 1962 (English translation in Soviet Mathematics Doklady 3, 1962)"
    locator: the balance indicator of a node
---

The balance factor of a node in a binary tree is the height of its right subtree minus the height of its left subtree. An [AVL tree](/avl-tree/) requires every balance factor to be $-1$, $0$ or $+1$; an update that makes some balance factor $\pm 2$ is fixed with one or two [rotations](/tree-rotation/) at that node. Since an AVL node only needs to know which of three values it has, the balance factor can be stored in two bits instead of a full height. Some books define it with the opposite sign, left minus right.

## Definition

Let $h(t)$ be the height of a binary tree $t$, the number of nodes on a longest path from its root down, with $h(\text{nil}) = 0$. For a node $x$, the **balance factor** is

$$bf(x) = h(x.right) - h(x.left).$$

A node is *left-heavy* if $bf(x) < 0$, *balanced* if $bf(x) = 0$, and *right-heavy* if $bf(x) > 0$. A binary tree is [height-balanced](/height-balanced-tree/) (AVL) when $bf(x) \in \{-1, 0, 1\}$ for every node $x$.

The height of a node follows from the heights of its children: $h(x) = 1 + \max(h(x.left), h(x.right))$. So a tree that stores heights gets $bf(x)$ with one subtraction. A tree that stores only balance factors must update them along the path of a change: an insertion that makes a subtree of $x$ one taller adds $+1$ to $bf(x)$ if it was the right subtree and $-1$ if it was the left one, and the change goes on up only if $h(x)$ grew, which happens when the new $bf(x)$ is not 0.

With the other sign, left minus right, as in CLRS's problem on AVL trees and in many lecture notes, every statement holds with left and right swapped.

## Examples and non-examples

- **A leaf.** Both subtrees are nil, so $bf = 0$.
- **A node with only a right child that is a leaf.** $bf = 1 - 0 = 1$: right-heavy but allowed in an AVL tree.
- **A chain of three keys 1, 2, 3 inserted in order** into a plain search tree. The root 1 has $bf = 2 - 0 = 2$, node 2 has $bf = 1$, node 3 has $bf = 0$. The root breaks the AVL rule; a left rotation at 1 gives the tree $(1, 2, 3)$, where all balance factors are 0.
- **The zig-zag case.** The tree with root 3, left child 1, and 2 as the right child of 1 has $bf(3) = -2$ and $bf(1) = +1$. The two signs differ, so a single rotation at 3 does not fix it; a rotation at 1 and then at 3 does. This is the case of a double rotation.
- **Balance factors do not bound the subtree sizes.** The [Fibonacci tree](/avl-height-theorem/) of height 6 has 20 nodes, with 12 on one side of the root and 7 on the other, and every balance factor is $\pm 1$. A small balance factor bounds the difference of heights, not of sizes.
- **A tree that is not AVL with small root balance.** A root with two subtrees of height 3, one of which is a chain, has $bf = 0$ at the root, but the chain has a node with $bf = \pm 2$. The rule must hold at every node.

## Related definitions

- **[Height-balanced tree](/height-balanced-tree/).** The tree in which all balance factors lie in $\{-1, 0, 1\}$; more generally, $|bf(x)| \le k$ gives the HB($k$) trees.
- **[AVL height bound](/avl-height-theorem/).** If all balance factors are in $\{-1, 0, 1\}$, the height is less than $1.4405 \lg(n + 2)$.
- **Rank difference.** [WAVL trees](/wavl-tree/) store a rank at each node and bound the rank difference between a node and its child by 1 or 2; this replaces the balance factor and allows a simpler deletion.
- **Weight balance.** [Weight-balanced trees](/weight-balanced-tree/) compare the sizes of the two subtrees instead of their heights.
- **[Black-height](/black-height/).** The red-black counterpart: a count of black nodes that must agree on all paths.

## References
