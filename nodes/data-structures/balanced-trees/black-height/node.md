---
tag: DZMQFW
kind: definition
slug: black-height
name: Black-height
aliases:
- black height of a node
area: data-structures/balanced-trees
level: core
summary: The number of black nodes on any path from a node down to a leaf, excluding the node itself; the same on all such paths in a red-black tree.
prereqs: [binary-search-tree, binary-tree]
see_also: [red-black-tree, red-black-height-theorem, red-black-correspondence-with-2-3-4-trees, left-leaning-red-black-tree, two-three-four-tree, join-based-tree-algorithms, aa-tree, wavl-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 13.1, Properties of red-black trees (the definition of bh(x) and Lemma 13.1)
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, FOCS 1978
    locator: the red-black framework and the rank of a node
  - paper: doi:10.1145/2935764.2935768
    title: Guy E. Blelloch, Daniel Ferizovic and Yihan Sun, Just join for parallel ordered sets, SPAA 2016
    locator: the join of red-black trees by black height
---

The black-height $bh(x)$ of a node $x$ in a [red-black tree](/red-black-tree/) is the number of black nodes on a path from $x$ down to a leaf, not counting $x$ itself but counting the black leaf nil at the end. The red-black rules make this number the same for every such path, so it is a property of the node. The black-height of the root is the black-height of the tree. It is the quantity that the red-black rules keep balanced, and it is the height of the corresponding [2-3-4 tree](/two-three-four-tree/).

## Definition

Let $T$ be a binary tree whose leaves are the empty nodes nil, with each node colored red or black and each nil black. Suppose that (R4) for each node $x$, all simple paths from $x$ down to a leaf contain the same number of black nodes. For a node $x$, the **black-height** $bh(x)$ is the number of black nodes on any path from $x$ down to a leaf, not counting $x$. In particular $bh(\text{nil}) = 0$. The black-height of $T$ is $bh$ of its root.

For a child $y$ of $x$, the definition gives

$$bh(x) = \begin{cases} bh(y) + 1 & \text{if } y \text{ is black,} \\ bh(y) & \text{if } y \text{ is red.} \end{cases}$$

So $bh(x)$ can be computed from either child, and (R4) says that both children give the same answer. With this rule, (R4) can be checked bottom-up in linear time: compute $bh$ at each node from its left child and compare with the value from its right child.

Some books use other counting conventions:

- Sedgewick and Wayne count black *links* rather than black nodes, where the color of a node is the color of the link from its parent. On a path from the root to nil, this count is the number of black nodes on the path below the root, which is $bh(\text{root})$.
- Some texts count $x$ itself when it is black, or do not count the nil leaf. These differ from $bh(x)$ by 0 or 1 and give the same bounds up to a constant.

## Examples and non-examples

- **A single black node.** Its two children are nil, so $bh = 1$. A single red node (not allowed as the root, but possible inside a tree) also has $bh = 1$.
- **A perfect all-black tree** with $2^b - 1$ internal nodes and height $b$ has $bh(\text{root}) = b$: each path from the root meets $b - 1$ more internal nodes and the nil leaf.
- **The tree (A\*, C, nil),** a black C with a red left child A and an empty right side. Every path from C meets one black node, the nil at the end, so $bh(C) = 1$, and also $bh(A) = 1$.
- **A node with two different counts.** In the tree (B, C, nil) where all nodes are black, the path from C through B meets two black nodes (B and a nil), but the path to the right meets one. So (R4) fails at C, and $bh(C)$ is not defined. This tree is not a red-black tree.
- **Black-height and height.** In the tree $(((A^*, C, \text{nil}), E, (H^*, L, \text{nil})), M, (P, R, (S^*, X, \text{nil})))$, the black-height of the root M is 3 and the height is 4.

## Related definitions

- **[Height](/red-black-height-theorem/).** In a red-black tree, $bh(x) \le h(x) \le 2\, bh(x)$ for each node $x$, where $h(x)$ is the number of edges on a longest path from $x$ down to a leaf: each black node below $x$ is on such a path, and no two red nodes are adjacent. The subtree of $x$ has at least $2^{bh(x)} - 1$ internal nodes. Together these give the height bound $2 \lg(n + 1)$.
- **2-3-4 tree height.** Merging each red node into its black parent gives a 2-3-4 tree; the black-height of the root is the height of that tree, measured in levels of nodes (see [the correspondence](/red-black-correspondence-with-2-3-4-trees/)).
- **Rank.** In [rank-balanced trees](/wavl-tree/) such as WAVL and in [AA trees](/aa-tree/), each node stores an integer rank, which plays the role of the black-height: a rank difference of 0 corresponds to a red child, and a difference of 1 to a black one.
- **Joins.** The [join](/join-based-tree-algorithms/) of two red-black trees walks down the spine of the one with the larger black-height until it meets a black node of the same black-height as the other, which gives joins in $O(|bh_1 - bh_2| + 1)$ time.
- **[Balance factor](/balance-factor/).** The AVL counterpart: the difference of the heights of the two subtrees, rather than a count that must agree.

## References
