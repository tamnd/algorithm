---
tag: P00R5P
kind: concept
slug: red-black-correspondence-with-2-3-4-trees
name: Red-black and 2-3-4 tree correspondence
aliases:
- red-black to 2-3-4 correspondence
area: data-structures/balanced-trees
level: core
summary: Each red-black tree corresponds to a 2-3-4 tree by merging red children into their parent, which explains its rebalancing rules.
prereqs: [red-black-tree, two-three-four-tree, black-height]
see_also: [red-black-height-theorem, left-leaning-red-black-tree, two-three-tree, red-black-tree-deletion, aa-tree, b-tree, tree-rotation]
sources:
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, FOCS 1978
    locator: the representation of 2-3-4 trees by red and black binary nodes
  - paper: doi:10.1007/BF00289509
    title: Rudolf Bayer, Symmetric binary B-trees, data structure and maintenance algorithms, Acta Informatica 1(4), 1972
    locator: the binary form of B-trees of order 4, with horizontal and vertical pointers
  - url: "https://opendatastructures.org/"
    title: Pat Morin, Open Data Structures
    locator: Chapter 9, Red-Black Trees (Section 9.1, 2-4 trees, and Section 9.2, red-black trees as simulated 2-4 trees)
  - url: https://sedgewick.io/wp-content/themes/sedgewick/papers/2008LLRB.pdf
    title: Robert Sedgewick, Left-leaning Red-Black Trees, 2008
    locator: the one-to-one correspondence of left-leaning red-black trees with 2-3 and 2-3-4 trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13 notes and Chapter 18, B-Trees (2-3-4 trees as B-trees with t = 2)
---

A [red-black tree](/red-black-tree/) is a [2-3-4 tree](/two-three-four-tree/) written with binary nodes. Merge each red node into its black parent: each black node and its red children become one node with 1, 2 or 3 keys, and the result is a 2-3-4 tree with all leaves at the same depth. Conversely, each 2-3-4 node can be written as a black node with zero, one or two red children. The red-black rules are exactly the rules that make this work: "no red node has a red child" says that a group is at most one black node and its children, and "every path has the same number of black nodes" says that all 2-3-4 leaves are at one depth. The [black-height](/black-height/) of the root is the height of the 2-3-4 tree. Under this view, each step of red-black insertion and deletion is a split, a merge or a borrow of the 2-3-4 tree.

## In plain words

Think of a red link as glue. A red node is not really a separate node: it is glued to its parent, and the two of them together are one fat node of the 2-3-4 tree. A black node with no red children is a node with one key. With one red child, it is a node with two keys. With two red children, it is a node with three keys.

Now the red-black rules read simply. Two red nodes in a row would glue three levels together, which is too fat, so it is not allowed. The same number of black nodes on every path means that every path passes the same number of fat nodes, so the fat tree has all its bottom nodes on one level. The fixes after an update are the splits and merges of fat nodes, written in colors and rotations.

## The idea

**The map.** Let $T$ be a red-black tree: a binary search tree with black leaves nil, a black root, (R3) no red node with a red child, and (R4) the same number of black nodes on every path from a node down to a leaf. Each red node has a parent, because the root is black, and that parent is black by (R3). So the nodes split into *groups*: each black node $x$ together with its red children. A group has 1, 2 or 3 nodes, one of them black. Let $\Gamma(T)$ be the tree whose nodes are the groups, where the keys of a group, in order, are its keys, and the children of a group are the groups of the black nodes (or the nils) just below it. A group with $j$ nodes has $j + 1$ children: the black node and its red children have $2j$ child slots, of which $j - 1$ hold the red members themselves.

**Theorem.** $\Gamma(T)$ is a 2-3-4 tree with the same keys in the same order, and its height (levels of nodes) is $bh(\text{root})$. Conversely, each 2-3-4 tree $U$ is $\Gamma(T)$ for exactly $2^{t}$ red-black trees $T$, where $t$ is the number of 3-nodes of $U$.

*Proof.* Each group has 1 to 3 keys and one more child than keys, so (B1) and (B2) hold. The in-order sequence of $T$ visits the keys of a group between the subtrees of its children, in order, so (B3) holds. Going down one level in $\Gamma(T)$ means passing one black node in $T$, so the depth of a nil leaf in $\Gamma(T)$ is the number of black internal nodes above it, which is $bh(\text{root})$ by (R4); all leaves are at that depth, and (B4) holds. For the converse, write a 2-node as a black node, a 4-node with keys $a < b < c$ as a black $b$ with red children $a$ and $c$, and a 3-node with keys $a < b$ as a black $a$ with a red right child $b$ or a black $b$ with a red left child $a$. The result satisfies (R3), because red nodes have black children (the tops of the groups below); and (R4), because each path from the root passes one black node per level of $U$. Each tree $T$ with $\Gamma(T) = U$ is of this form, since a group of two nodes is a black node with one red child on one side. The choices for the 3-nodes are independent, which gives $2^t$ trees. $\square$

**The operations.** Each primitive of red-black trees has a 2-3-4 meaning:

| red-black step | 2-3-4 meaning |
|---|---|
| a rotation inside a group (both nodes in the same group) | the same 3-node, written with the red link on the other side |
| a color flip: black $x$ with two red children becomes red with two black children | split the 4-node at $x$ and push its middle key $x$ into the parent group |
| the inverse flip: red $x$ with two black children becomes black with two red children | merge $x$ with its two children groups, which are 2-nodes, into one 4-node (the parent group loses a key) |
| insert a red leaf | add a key to a leaf node of the 2-3-4 tree |
| the fix of a red-red pair by rotation (cases 2 and 3 of insertion) | the new key made a group of 4 nodes in a bad shape; rotations rewrite the 4-node in the standard shape |
| the fix by recoloring when the uncle is red (case 1 of insertion) | the leaf was a 4-node: split it, and the middle key goes up, maybe causing another split |
| deletion case 2: the sibling and its children are black, the sibling becomes red | merge the 2-node that lost its key with its sibling 2-node and a key of the parent |
| deletion cases 3 and 4: rotate a red nephew up | borrow a key from a sibling with 2 or 3 keys, through the parent |
| deletion case 1: the sibling is red | change the way the parent's 3-node is written, so the real sibling is next to $x$ |

The bottom-up insertion of CLRS works like the bottom-up 2-3-4 insertion: the key goes into a leaf, and 4-nodes split up the path. Top-down red-black insertion splits each 4-node on the way down, exactly like top-down 2-3-4 insertion.

**Left-leaning trees.** If every 3-node is written with its red link on the left, the map becomes one-to-one: each 2-3-4 tree has exactly one [left-leaning red-black tree](/left-leaning-red-black-tree/). If, in addition, 4-nodes are not allowed to stay, the trees are in one-to-one correspondence with [2-3 trees](/two-three-tree/), which is the form of Sedgewick and Wayne. [AA trees](/aa-tree/) do the same with the red link on the right.

## Examples

**From red-black to 2-3-4.** The left-leaning red-black tree built by inserting S, E, A, R, C, H, X, M, P, L is, with a star for red,

$$(((A^*, C, \text{nil}), E, (H^*, L, \text{nil})), M, (P, R, (S^*, X, \text{nil}))).$$

The groups are [M], [E], [R], [A C], [H L], [P], [S X], so the 2-3-4 tree (here a 2-3 tree) is [M] ([E] ([A C], [H L]), [R] ([P], [S X])). The black-height of M is 3, and the 2-3 tree has 3 levels.

**From 2-3-4 to red-black.** Take the 2-3-4 tree [50] ([20] ([10], [25 30 40]), [80] ([60 70], [90])). Write the 4-node [25 30 40] as a black 30 with red children 25 and 40, and the 3-node [60 70] as a black 70 with a red left child 60 or as a black 60 with a red right child 70. With the left-leaning choice the tree is

$$((10, 20, (25^*, 30, 40^*)), 50, ((60^*, 70, \text{nil}), 80, 90)).$$

Every path from the root has black nodes 50, then 20 or 80, then one of 10, 30, 70, 90, then nil. Since the 2-3-4 tree has one 3-node, there are exactly $2^1 = 2$ red-black trees for it.

**A split as a color flip.** Insert 35 into the second tree. In the 2-3-4 tree, top-down insertion splits [25 30 40] on the way down: 30 goes up into [20], which becomes [20 30], and 35 goes into [40], giving [35 40]. In the red-black tree, the flip at 30 makes 30 red and 25, 40 black; now 30 is a red right child of 20, which a left-leaning tree fixes with one rotation; 35 becomes the red left child of 40. The groups are [20 30] and [35 40], as in the 2-3-4 tree.

**A merge as the inverse flip.** In the first tree, deleting R with the [top-down deletion](/red-black-tree-deletion/) first paints the root M red and flips at M: M becomes black with two red children E and R. In the 2-3-4 view, the three 2-nodes [E], [M], [R] are merged into the 4-node [E M R], so that a key can leave the right side.

## Where it is used

- **Proofs.** The [red-black height bound](/red-black-height-theorem/) is the 2-3-4 fact that a tree of height $b$ has at least $2^b - 1$ keys, plus the fact that each level of the 2-3-4 tree is at most two binary levels.
- **Teaching and design.** Sedgewick's left-leaning trees and ODS Chapter 9 present red-black trees as simulated 2-4 trees, so that the cases of the fix-ups follow from splits and merges instead of being memorized.
- **Choosing variants.** The view explains why [AA trees](/aa-tree/) and left-leaning trees have fewer cases: they forbid some ways of writing 3-nodes and 4-nodes, so fewer shapes can occur.
- **Bulk operations.** Joins and splits of red-black trees, used in [join-based algorithms](/join-based-tree-algorithms/), follow the joins of B-trees: attach the shorter tree at the level of the same black-height.
- **B-trees in memory.** A [B-tree](/b-tree/) of larger order can be written in binary form in the same way, though this is rarely done.

## References
