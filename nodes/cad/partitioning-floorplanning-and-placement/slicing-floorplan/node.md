---
tag: CD0S40
kind: definition
slug: slicing-floorplan
name: Slicing floorplan
aliases:
- slicing structure
- guillotine floorplan
area: cad/partitioning-floorplanning-and-placement
level: core
summary: A floorplan obtained by cutting the chip rectangle again and again by horizontal or vertical lines, represented by a slicing tree.
prereqs: [floorplanning, binary-tree, guillotine-cut-technique]
see_also: [normalized-polish-expression, shape-function, stockmeyer-floorplan-sizing, wong-liu-floorplanning, mosaic-floorplan, mosaic-floorplan-baxter-theorem, floorplan-constraint-graphs, expression-tree]
sources:
  - paper: doi:10.1109/DAC.1982.1585510
    title: Ralph H. J. M. Otten, Automatic floorplan design, Proceedings of the 19th Design Automation Conference, 261 to 267, 1982
    locator: slicing structures, the recursive cuts and their trees
  - paper: "D. F. Wong and C. L. Liu, A new algorithm for floorplan design, Proceedings of the 23rd ACM/IEEE Design Automation Conference, 101 to 107, 1986"
    locator: slicing trees, skewed slicing trees and their one to one correspondence with slicing floorplans and normalized Polish expressions
  - paper: doi:10.1016/S0019-9958(83)80038-2
    title: Larry Stockmeyer, Optimal orientations of cells in slicing floorplan designs, Information and Control 57(2-3), 91 to 101, 1983
    locator: the polynomial orientation algorithm for slicing floorplans, and NP-completeness for general floorplans
  - paper: "Bo Yao, Hongyu Chen, Chung-Kuan Cheng and Ronald L. Graham, Floorplan representations: complexity and connections, ACM Transactions on Design Automation of Electronic Systems 8(1), 55 to 80, 2003"
    locator: the exact number of slicing floorplans with n rooms
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (slicing and non-slicing floorplans, slicing trees; general locator)
---

A slicing floorplan is a division of the chip rectangle into rectangular rooms that can be made by straight cuts alone: cut the rectangle from one side to the opposite side by a vertical or a horizontal line, then cut each part in the same way, until each part holds one block. It is the [guillotine](/guillotine-cut-technique/) structure of cutting stock, used for [floorplanning](/floorplanning/) in chip design, and it is stored as a slicing tree, a [binary tree](/binary-tree/) whose inner nodes are the cuts and whose leaves are the blocks. Its value is that the tree can be optimized bottom up: [shape functions](/shape-function/) and [Stockmeyer's algorithm](/stockmeyer-floorplan-sizing/) find the best shapes of all blocks in polynomial time, while for general floorplans the same problem is NP-complete. The cost is that some packings, such as the pinwheel of five blocks, are not slicing.

## Definition

**Dissection.** Let $R$ be an axis-parallel rectangle. A dissection of $R$ into $n$ rooms is a set of $n$ axis-parallel rectangles with disjoint interiors whose union is $R$.

**Slicing floorplan.** A dissection of $R$ is *slicing* if $n = 1$, or if some vertical or horizontal line segment from one side of $R$ to the opposite side, a *cut*, crosses no room and splits $R$ into two rectangles $R_1$ and $R_2$ such that the rooms inside $R_1$ and the rooms inside $R_2$ are both slicing. In a floorplan, each room holds one block, and the block fits in its room.

**Slicing tree.** A slicing tree is a full binary tree: each inner node has two children. The leaves are the rooms. Each inner node is labeled $V$ or $H$. A node labeled $V$ stands for a vertical cut, with the left child for the part to the left of the cut and the right child for the part to the right. A node labeled $H$ stands for a horizontal cut, with the left child for the part below and the right child for the part above. This is the convention of the [normalized Polish expression](/normalized-polish-expression/) page, whose words are the postorders of these trees. The tree of a slicing floorplan follows the cuts in the definition, and conversely a tree with given block sizes gives a floorplan by the bottom-up rule: a $V$ node has width $W_a + W_b$ and height $\max(H_a, H_b)$, and an $H$ node has width $\max(W_a, W_b)$ and height $H_a + H_b$.

**Same floorplan, several trees.** Three side-by-side rooms $a$, $b$, $c$ have two trees, $(a\,b\,V)\,c\,V$ and $a\,(b\,c\,V)\,V$, because the order of two parallel cuts is not fixed. A slicing tree is *skewed* if no node has a right child with the same label. Take slicing floorplans up to sliding of segments and with no point where four rooms meet. Then each slicing floorplan has exactly one skewed tree, and each skewed tree gives exactly one such floorplan (Wong and Liu 1986). Collapse each maximal chain of equal labels into one node: the result is an ordered tree in which each inner node has at least two children, and the labels alternate between $V$ and $H$ from a node to its children. So the label of the root fixes all the others.

**Counting.** Let $t(n)$ be the number of ordered trees with $n$ leaves in which no node has exactly one child. A leaf gives $t(1) = 1$, and a tree with $n \ge 2$ leaves is a root with an ordered list of $k \ge 2$ subtrees whose leaf counts add up to $n$. So $t(n)$ is the sum, over all ordered ways $n = n_1 + \cdots + n_k$ with $k \ge 2$ and all $n_j \ge 1$, of $t(n_1) \cdots t(n_k)$. This gives $1, 1, 3, 11, 45, 197, 903$ for $n = 1, \ldots, 7$. By the collapse above, the number of slicing floorplans with $n$ unlabeled rooms is $1$ for $n = 1$ and $2\,t(n)$ for $n \ge 2$, the factor $2$ for the label of the root:

| rooms $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| slicing floorplans | 1 | 2 | 6 | 22 | 90 | 394 | 1806 |
| full binary trees with labels, $C_{n-1}\, 2^{n-1}$ | 1 | 2 | 8 | 40 | 224 | 1344 | 8448 |

The first row is the sequence of large Schröder numbers $S_{n-1}$, as Yao, Chen, Cheng and Graham (2003) state. The second row counts all slicing trees, with $C_{n-1}$ the [Catalan number](/catalan-numbers/) of full binary trees with $n$ leaves; the gap between the rows is the redundancy that normalization removes. With $n$ different blocks in the rooms, each count is multiplied by $n!$: there are $3! \cdot 6 = 36$ normalized Polish expressions of three blocks and $4! \cdot 22 = 528$ of four.

**Recognition.** A dissection is slicing exactly when the recursive search for a cut succeeds. A cut of a part is a maximal segment of the dissection that runs from one side of the part to the other, so a search over the segments of each part decides the question in polynomial time.

## Examples and non-examples

**Three rooms.** The six slicing floorplans of three rooms are three columns, three rows, a vertical cut with the left or the right part cut once more horizontally, and a horizontal cut with the lower or the upper part cut once more vertically. Their skewed trees are $V(V(\cdot,\cdot),\cdot)$, $H(H(\cdot,\cdot),\cdot)$, $V(H(\cdot,\cdot),\cdot)$, $V(\cdot,H(\cdot,\cdot))$, $H(V(\cdot,\cdot),\cdot)$ and $H(\cdot,V(\cdot,\cdot))$. The trees $V(\cdot, V(\cdot,\cdot))$ and $H(\cdot, H(\cdot,\cdot))$ are not skewed: they are the columns and the rows again.

**A cross junction is allowed.** Cut a square in half vertically, then cut both halves horizontally at the same height. The two horizontal cuts meet the vertical one at one point, where four rooms touch. The dissection is slicing, and it has two skewed trees, $V(H(a, b), H(c, d))$ and $H(V(a, c), V(b, d))$, with $a$ and $b$ on the left and $a$ and $c$ at the bottom. A [mosaic floorplan](/mosaic-floorplan/) does not allow such a point. Move the two horizontal pieces apart and the vertical segment stays whole, which gives the first tree. Move the two vertical pieces apart and the horizontal segment stays whole, which gives the second tree. The count $22$ for four rooms counts these two floorplans once each.

**Non-example: the pinwheel.** Dissect a $3 \times 3$ square into the rooms $[0, 1] \times [0, 2]$, $[1, 3] \times [0, 1]$, $[2, 3] \times [1, 3]$, $[0, 2] \times [2, 3]$ and the center $[1, 2] \times [1, 2]$. A cut must be a straight segment from one side of the square to the opposite side. The dissection has four inner segments, and each of them ends at the boundary at one end and on another segment at the other end, so none of them is a cut. So the pinwheel is not slicing. Its mirror image is the other non-slicing floorplan with five rooms: there are 92 mosaic floorplans with five rooms (the [Baxter number](/mosaic-floorplan-baxter-theorem/)) and 90 slicing ones.

**The price of slicing.** Take the five blocks of the pinwheel with fixed orientation: two tall blocks $1 \times 2$, two wide blocks $2 \times 1$ and one square $1 \times 1$. The pinwheel packs them into the $3 \times 3$ square with no empty space. No slicing floorplan does. The width and the height of a slicing floorplan of these blocks are integers, since they are sums and maxima of block sides, so area $9$ means a $3 \times 3$, $1 \times 9$ or $9 \times 1$ rectangle with no empty space. The wide blocks do not fit in width $1$ and the tall blocks do not fit in height $1$. In the $3 \times 3$ square the first cut makes a $3 \times 1$ strip and a $3 \times 2$ part, or the same turned by a quarter turn, which swaps the tall and the wide blocks, so one case is enough. The strip holds only blocks of height $1$, so it holds a wide block and the square. The $3 \times 2$ part must then hold both tall blocks and one wide block. A horizontal cut of it makes strips of height $1$, too low for a tall block, and a vertical cut makes a $1 \times 2$ part and a $2 \times 2$ part that must hold a tall block and a wide block, which no cut of the $2 \times 2$ part allows. The best slicing floorplan has area $10$: a tall block at each end of a $5 \times 2$ rectangle, and between them a $3 \times 2$ part with a wide block at the bottom and the square and the other wide block above it.

**Non-example: a packing with a gap.** Blocks placed freely in the chip, with empty space between them, do not form a dissection at all. A floorplan of a [B*-tree](/b-star-tree-floorplan/) or a [sequence pair](/sequence-pair/) is such a packing. It is slicing in the sense of this page only when its blocks can be put into the rooms of a slicing dissection with the same relations.

## Related definitions

- **[Normalized Polish expression](/normalized-polish-expression/).** The postorder word of the skewed slicing tree, the usual way to store a slicing floorplan in a search.
- **[Shape function](/shape-function/) and [Stockmeyer floorplan sizing](/stockmeyer-floorplan-sizing/).** The bottom-up computation of the best width and height pairs of a slicing tree, polynomial because each node needs only the lists of its two children.
- **[Wong-Liu floorplanning](/wong-liu-floorplanning/).** Simulated annealing over normalized Polish expressions.
- **[Mosaic floorplan](/mosaic-floorplan/).** The wider class of dissections without cross junctions, counted up to sliding of segments, which includes the pinwheel; the [Baxter number theorem](/mosaic-floorplan-baxter-theorem/) counts it.
- **[Guillotine cut technique](/guillotine-cut-technique/).** The same recursive cuts in cutting stock and in approximation schemes for packing.
- **[Floorplan constraint graphs](/floorplan-constraint-graphs/).** For a slicing floorplan, the left-of order is a series-parallel order built from the tree.
- **[Expression tree](/expression-tree/).** A slicing tree is an expression tree with the two operators $V$ and $H$.

## References
