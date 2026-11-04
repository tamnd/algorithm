---
tag: ZNK1BM
kind: concept
slug: tree-rotation
name: Tree rotation
aliases:
- left rotation
- right rotation
- rotation
area: data-structures/balanced-trees
level: intro
summary: A local pointer change that moves one node up and another down while preserving the BST order; the basic rebalancing step.
prereqs: [binary-search-tree, binary-search-tree-property, inorder-traversal]
see_also: [tree-rebalancing, balanced-binary-search-tree, avl-tree, red-black-tree, treap, splay-tree, augmenting-data-structures]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Section 13.2 (Rotations, the procedure LEFT-ROTATE)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (rotations in red-black BSTs, rotateLeft and rotateRight)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (single and double rotation)
  - paper: doi:10.1090/S0894-0347-1988-0928904-4
    title: Daniel D. Sleator, Robert E. Tarjan and William P. Thurston, Rotation distance, triangulations, and hyperbolic geometry, Journal of the American Mathematical Society 1(3), 1988
    locator: pages 647 to 681 (the maximum rotation distance 2n − 6 for large n)
---

A tree rotation is a local change of a [binary search tree](/binary-search-tree/) that moves one child up to the place of its parent and moves the parent down, while it keeps the in-order sequence of the keys. It changes three pointers, takes $O(1)$ time, and keeps the [binary-search-tree property](/binary-search-tree-property/). It is the basic step of almost every [balanced binary search tree](/balanced-binary-search-tree/): [AVL trees](/avl-tree/), [red-black trees](/red-black-tree/), [treaps](/treap/) and [splay trees](/splay-tree/) all restore their shape with rotations.

## In plain words

Think of a small family in the tree: a parent, its left child, and the three subtrees that hang below them. A right rotation lifts the left child into the place of the parent. The old parent becomes the right child of the lifted node. The middle subtree, which lies between the two keys, changes sides: it was the right subtree of the child, and it becomes the left subtree of the old parent.

Nothing else in the tree changes. If you read the keys from left to right, you get the same order as before. So the tree is still a search tree. What changes is the shape: the left side gets one level shorter and the right side one level longer. A left rotation is the same move in a mirror. Balanced trees use these moves to make a tall side shorter.

## The idea

Let $y$ be a node with a left child $x$. Let $\alpha$ and $\beta$ be the left and right subtrees of $x$, and $\gamma$ the right subtree of $y$. Any of the three may be empty. A **right rotation at $y$** gives the tree in which $x$ takes the place of $y$, with $\alpha$ as its left subtree and $y$ as its right child, and $y$ has $\beta$ as its left subtree and $\gamma$ as its right subtree. A **left rotation at $x$** is the inverse: it starts from the second shape and gives the first.

$$
\begin{array}{ccc}
\text{before: } (\alpha \; x \; \beta) \; y \; \gamma & \xrightarrow{\text{right rotation at } y} & \text{after: } \alpha \; x \; (\beta \; y \; \gamma) \\
\end{array}
$$

Here $(L \; v \; R)$ is the tree with root $v$, left subtree $L$ and right subtree $R$.

```pseudo id=main
ROTATE-RIGHT(T, y)                         ▷ y.left ≠ nil
L1  x ← y.left
L2  y.left ← x.right                       ▷ the subtree β moves to y
L3  if x.right ≠ nil then x.right.parent ← y
L4  x.parent ← y.parent
L5  if y.parent = nil then T.root ← x
L6  else if y = y.parent.left then y.parent.left ← x
L7  else y.parent.right ← x
L8  x.right ← y
L9  y.parent ← x
```

Lines L2, L6 or L7, and L8 change the three child pointers. Lines L3, L4 and L9 keep the parent pointers right. Without parent pointers, as in a recursive implementation, the procedure is three lines: $x \leftarrow y.left$, $y.left \leftarrow x.right$, $x.right \leftarrow y$, and the caller stores $x$ where $y$ was. LEFT-ROTATE is the same with left and right exchanged.

**The order is kept.** In the tree $(\alpha \; x \; \beta) \; y \; \gamma$, the in-order sequence is $\alpha, x, \beta, y, \gamma$, where each subtree stands for its own in-order sequence. In $\alpha \; x \; (\beta \; y \; \gamma)$ the in-order sequence is again $\alpha, x, \beta, y, \gamma$. A binary tree is a search tree exactly when its in-order sequence is sorted, so the rotation keeps the search-tree property. The rest of the tree sees the rotated part only through its root pointer, so the in-order sequence of the whole tree is the same too.

**What changes.** Each node of $\alpha$ moves up one level, each node of $\gamma$ moves down one level, and the nodes of $\beta$ keep their depth. The node $x$ moves up one level and $y$ moves down one level. Only $x$ and $y$ get new subtrees. So a field that is a function of a node and its two children, such as the subtree size or the height, needs to be computed again only at $y$ and then at $x$, in that order. This is why an [augmented](/augmenting-data-structures/) tree keeps its fields through rotations in $O(1)$ time.

**Double rotation.** When $x$ is the left child of $y$ and the long subtree is $\beta$ (the inner subtree), one rotation at $y$ does not help: it only moves $\beta$ from $x$ to $y$ at the same depth. Then a left rotation at $x$ followed by a right rotation at $y$ lifts the root of $\beta$ two levels to the top. This pair is the *double rotation* of AVL trees, and the *zig-zag* step of splay trees.

**Rotation distance.** Any binary search tree on $n$ keys can be changed into any other one on the same keys by rotations. Let the right spine be the path from the root along right children. A right rotation at a spine node that has a left child puts that child on the spine, so it adds one node to the spine and removes none. The spine has at least one node, so at most $n - 1$ rotations turn any tree into the right chain. Rotations are invertible, so at most $2n - 2$ rotations turn any tree into any other. Sleator, Tarjan and Thurston proved that the largest distance needed is exactly $2n - 6$ for all large $n$.

## Examples

**A chain becomes balanced.** Insert 10, 20 and 30 into an empty search tree without balancing. The tree is a right chain $10 \to 20 \to 30$ of height 3 (counting nodes on the longest path). A left rotation at 10 makes 20 the root, with 10 as its left child and 30 as its right child. The height is now 2, and the in-order sequence is still 10, 20, 30.

**A rotation with a moving middle subtree.** Take the tree with root 50, left child 30, and right child 60, where 30 has the children 20 and 40. A right rotation at 50 gives:

| | before | after |
|---|---|---|
| root | 50 | 30 |
| left child of root | 30 | 20 |
| right child of root | 60 | 50 |
| children of 30 | 20, 40 | 20, 50 |
| children of 50 | 30, 60 | 40, 60 |
| in-order | 20 30 40 50 60 | 20 30 40 50 60 |

Here $\alpha = \{20\}$, $\beta = \{40\}$ and $\gamma = \{60\}$. The key 40 moves from the right of 30 to the left of 50. It stays between 30 and 50 in the order, and its depth stays 2. The key 20 moves up from depth 2 to depth 1, and 60 moves down from depth 1 to depth 2.

**A zig-zag needs two rotations.** Insert 10, 30, 20. The tree is 10 with right child 30, and 30 has left child 20. A left rotation at 10 gives 30 as root with left child 10 and the subtree of 20 under 10: the height is still 3. Do the double rotation instead: a right rotation at 30 gives the chain $10 \to 20 \to 30$, and then a left rotation at 10 gives root 20 with children 10 and 30, of height 2.

**Subtree sizes.** In the second example, store the size of each subtree. Before the rotation, $size(30) = 3$ and $size(50) = 5$. After it, $size(50) = size(40) + size(60) + 1 = 3$, and then $size(30) = size(20) + size(50) + 1 = 5$. The new root has the size of the old root, as it must.

## Where it is used

- [AVL trees](/avl-tree/) restore the [balance factor](/balance-factor/) of a node with one single or one double rotation after an insertion.
- [Red-black trees](/red-black-tree/) and [left-leaning red-black trees](/left-leaning-red-black-tree/) use at most two rotations for an insertion and at most three for a deletion, together with color changes.
- [Treaps](/treap/) rotate a new node up until its priority fits the heap order.
- [Splay trees](/splay-tree/) move an accessed node to the root by zig, zig-zig and zig-zag steps, each made of one or two rotations.
- [Weight-balanced trees](/weight-balanced-tree/), [AA trees](/aa-tree/) and [WAVL trees](/wavl-tree/) also rebalance by rotations; the [tree rebalancing](/tree-rebalancing/) page compares these schemes.
- An [order-statistic tree](/order-statistic-tree/) and other [augmented](/augmenting-data-structures/) trees update their extra fields at the two rotated nodes only.

## References
