---
tag: WA1GJ6
kind: data-structure
slug: b-star-tree-floorplan
name: B*-tree floorplan representation
aliases:
- B*-tree floorplan
area: eda/partitioning-floorplanning-and-placement
level: core
summary: Chang and coauthors' ordered binary tree for compacted packings in which a left child is the block to the right and a right child the block above.
model: word-ram
complexity:
  vars: {n: the number of blocks}
  time: {worst: O(n), average: O(n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 2000
  people: [Yun-Chih Chang, Yao-Wen Chang, Guang-Ming Wu, Shu-Wei Wu]
  note: Chang, Chang, Wu and Wu presented the B*-tree at the Design Automation Conference in 2000, as a binary form of the O-tree with a linear-time packing.
prereqs: [floorplanning, binary-tree, preorder-traversal, doubly-linked-list]
see_also: [o-tree-floorplan, sequence-pair, normalized-polish-expression, rectangle-packing, skyline-problem, simulated-annealing, catalan-numbers, left-child-right-sibling]
sources:
  - paper: doi:10.1145/337292.337541
    title: Yun-Chih Chang, Yao-Wen Chang, Guang-Ming Wu and Shu-Wei Wu, B*-trees, a new representation for non-slicing floorplans, Proceedings of the 37th Design Automation Conference, 458 to 463, 2000
    locator: the definition of the B*-tree, the construction of the tree of an admissible placement, the contour packing in amortized linear time, and the three perturbations of the annealing
  - paper: doi:10.1145/309847.309928
    title: Pei-Ning Guo, Chung-Kuan Cheng and Takeshi Yoshimura, An O-tree representation of non-slicing floorplan and its applications, Proceedings of the 36th Design Automation Conference, 268 to 273, 1999
    locator: the O-tree, admissible placements, and the contour that the B*-tree takes over
  - paper: doi:10.1109/TCAD.2006.870076
    title: Tung-Chieh Chen and Yao-Wen Chang, Modern floorplanning based on B*-tree and fast simulated annealing, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 25(4), 637 to 650, 2006
    locator: fixed-outline and bus-driven floorplanning with B*-trees and a three-stage annealing
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplan representations; general locator)
---

A B*-tree is an ordered binary tree whose nodes are the blocks of a floorplan. The root is the block at the lower-left corner. The left child of a block $b$ is placed just to the right of $b$, and the right child of $b$ is placed above $b$ at the same $x$. Every block then drops down until it rests on the floor or on a block below it. Chang, Chang, Wu and Wu introduced it in 2000 as a binary form of the [O-tree](/o-tree-floorplan/). A contour of the placed blocks gives the packing in $O(n)$ time. Every packing that is compact to the left and down has a B*-tree, so a search over trees, such as an [annealing](/simulated-annealing/), can reach a [packing](/rectangle-packing/) of least area, slicing or not.

## In plain words

Put the first block in the lower-left corner. For each block, you can name one block that goes directly to its right and one block that goes directly above it, starting at its left side. These choices form a tree.

To build the picture, visit the tree from the root, always the right-hand block first and then the block above. When you visit a block, you already know where its left side is. Slide it down from the top until it lands on the floor or on a block. Keep a record of the skyline of the blocks so far, so that you can see at once how high a block lands.

## The abstract type

The type stores a B*-tree on a set of $n$ blocks. The operations are:

- PACK$(w, h)$: given the width $w_b$ and the height $h_b$ of each block, return the lower-left corner $(x_b, y_b)$ of each block and the width $W$ and the height $H$ of the packing.
- ROTATE$(b)$: exchange $w_b$ and $h_b$.
- SWAP$(a, b)$: exchange the places of two blocks in the tree.
- MOVE$(b, p, \text{side})$: delete $b$ and insert it again as the left or the right child of $p$.

These are the three perturbations of Chang and coauthors. Each tree is a legal floorplan, so every move gives a packing without overlap.

## Representation

Each node has a left child, a right child and, for the moves, a parent. The packing rules are:

- the root has $x = 0$;
- the left child $c$ of $b$ has $x_c = x_b + w_b$, so $c$ is to the right of $b$ and touches it;
- the right child $c$ of $b$ has $x_c = x_b$, so $c$ is above $b$ with the same left side.

The blocks are placed in [preorder](/preorder-traversal/), so the parent of a block is placed before it. The $y$ of a block is the highest top of the blocks already placed whose $x$-ranges meet its own. The *contour* stores these tops: it is a [doubly linked list](/doubly-linked-list/) of horizontal segments that covers $[0, \infty)$, the same picture as the output of the [skyline problem](/skyline-problem/). Each block keeps a pointer to its own segment of the contour. Its right child starts the walk at this segment, and its left child at the next one.

## Operations

```pseudo id=main
PACK(T, w, h)
L1  contour ← one segment [0, ∞) at height 0
L2  stack ← (root, the first segment of the contour)
L3  while the stack is not empty do pop (b, s)        ▷ s starts at x_b
L4      x_b ← the left end of s; e ← x_b + w_b
L5      y_b ← the largest height of the segments from s on that start before e
L6      replace those segments by [x_b, e) at height y_b + h_b, and keep the part of the last one after e
L7      record (x_b, y_b); W ← max(W, e); H ← max(H, y_b + h_b)
L8      if b has a right child c then push (c, s)
L9      if b has a left child c then push (c, the segment after s)
L10 return x, y, W, H
```

The left child is pushed last, so it is popped next, and preorder is kept. Line L9 gives the left child the segment that starts at $x_b + w_b$, which is where the left child goes. Line L8 gives the right child the segment of $b$ itself, which starts at $x_b$. The blocks of the left subtree of $b$ are placed in between, but all of them are to the right of $x_b + w_b$, so they do not change the segment of $b$.

ROTATE changes only the sizes. SWAP exchanges two labels. MOVE deletes a node: a node with at most one child is replaced by that child, and a node with two children is first swapped down along its left children until it has one child. Then it inserts the node at a free or used child place of $p$, and the old child of that place becomes a child of the new node on the same side.

## Example

Take five blocks: A is $3 \times 2$, B is $2 \times 3$, C is $2 \times 1$, D is $2 \times 2$ and E is $3 \times 1$ (width by height). The tree has the root A, with B as the left child of A, C as the left child of B, D as the right child of A, and E as the left child of D. The preorder is A, B, C, D, E.

| block | rule | $x$ | segments walked | $y$ | contour after the block |
|---|---|---|---|---|---|
| A | root | 0 | $[0, \infty)$ at 0 | 0 | $[0,3)$:2, $[3,\infty)$:0 |
| B | left of A | 3 | $[3, \infty)$ at 0 | 0 | $[0,3)$:2, $[3,5)$:3, $[5,\infty)$:0 |
| C | left of B | 5 | $[5, \infty)$ at 0 | 0 | $[0,3)$:2, $[3,5)$:3, $[5,7)$:1, $[7,\infty)$:0 |
| D | right of A | 0 | $[0, 3)$ at 2 | 2 | $[0,2)$:4, $[2,3)$:2, $[3,5)$:3, $[5,7)$:1, $[7,\infty)$:0 |
| E | left of D | 2 | $[2,3)$ at 2, $[3,5)$ at 3 | 3 | $[0,2)$:4, $[2,5)$:4, $[5,7)$:1, $[7,\infty)$:0 |

The packing is $7 \times 4$, area 28, for a block area of $6 + 6 + 2 + 4 + 3 = 21$. Block E is the left child of D, so its left side is at the right side of D, $x = 2$. It lands on B, not on A, because B is higher. Below E, over $[2, 3)$, there is a gap of height 1 above A. Block D starts its walk at the segment of A, which the blocks B and C did not change.

## Correctness

The parent of each block is placed first, so each $x$ is known when it is needed. The contour list stays a correct skyline: a block replaces the segments under its $x$-range by one segment at its top, which is not lower than the old heights there. The walk of a block starts at the segment that begins at its left side, because a left child is popped right after its parent and a right child starts at the segment of its parent, which the left subtree does not touch. So each $y$ is the highest top under the block, the same value as a direct search over all placed blocks. Any two blocks either have disjoint $x$-ranges or the later one is above the earlier one, so there is no overlap. Every block rests on the floor or on a block, so the packing is compact downward. The full proof is in [the correctness proof](proofs/correctness.md).

Two things are not true, and the tests check both. The packing need not be compact to the left: with three unit squares, the root A, its left child B and the right child C of B, block C is at $(1, 1)$, but $(0, 1)$ is free. And two trees can give the same packing: with the root A, the right child D of A and the left child E of D, the squares are at $A = (0, 0)$, $D = (0, 1)$, $E = (1, 0)$, which is also the packing of the tree with E as the left child and D as the right child of A. What Chang and coauthors prove is the other direction: each placement that is compact to the left and down (an *admissible* placement) is the packing of exactly one B*-tree. Its left child is the lowest block that touches its right side, and its right child is the lowest block above it with the same $x$. This is cited, and the tests check its consequence for up to four blocks: the least area over all trees equals the least area of any packing.

## Complexity

| operation | time | extra space |
|---|---|---|
| PACK with the contour | $O(n)$ | $O(n)$ |
| PACK by a direct search over the placed blocks | $\Theta(n^2)$ | $O(n)$ |
| ROTATE, SWAP | $O(1)$ | none |
| MOVE | $O(1)$ to relink, plus the swaps down a path for a node with two children | none |

PACK is linear because each segment that a walk passes, except the first, is removed from the contour or cut at the end of the block. Each block makes at most one new segment, so at most $n + 1$ segments are made and removed in total, and all walks together take $O(n)$ steps. This is an amortized bound: one block can walk over many segments.

There are $C_n$ binary trees with $n$ nodes, where $C_n$ is the $n$th [Catalan number](/catalan-numbers/), and $n!$ ways to put the blocks on the nodes. So there are $n! \cdot C_n = (2n)!/(n+1)!$ B*-trees, which is less than the $(n!)^2$ of a [sequence pair](/sequence-pair/) for $n \ge 3$. For $n = 4$ there are $24 \cdot 14 = 336$ trees, against 576 sequence pairs.

## Variants

- **The O-tree.** The [O-tree](/o-tree-floorplan/) of Guo, Cheng and Yoshimura stores the same packings with an ordered tree. The [left-child right-sibling](/left-child-right-sibling/) form of an O-tree is a B*-tree.
- **Fixed outline.** Chen and Chang's floorplanner of 2006 searches over B*-trees with a three-stage annealing for a packing inside a fixed outline, and also handles buses between blocks.
- **Symmetry and analog layout.** Trees in which a symmetric group of blocks forms one island are used for analog placement.
- **Hierarchical B*-trees.** A node can stand for a cluster of blocks with its own tree.
- **Soft blocks.** A search can change the shape of a soft block between packings; the tree does not change.

## When to use it

Use a B*-tree in a search for compact packings of hard blocks, such as macros, when the packing is evaluated very many times. The packing takes linear time, the moves are simple, and there is less redundancy than in a sequence pair. If the floorplan must be slicing, use a [normalized Polish expression](/normalized-polish-expression/), which also allows exact sizing of soft blocks. If the relations of every pair must be read in $O(1)$ time, for example for constraints between blocks, a [sequence pair](/sequence-pair/) is simpler.

## Pitfalls

- **Swapping the meaning of the children.** In the B*-tree the left child is to the right of its parent, and the right child is above. Some texts draw it the other way. Use one convention in PACK and in the moves.
- **Starting every walk at the head.** If each block walks the contour from $x = 0$, PACK takes quadratic time. Start at the segment of the parent, or at the one after it.
- **The order of the pushes.** Push the right child first and the left child last, so that the left child is popped next and its segment is still the one after the segment of the parent.
- **Counting packings by trees.** Different trees can give the same packing, as in the example above, so $n! \cdot C_n$ is not the number of distinct packings.
- **Expecting a left-compact packing.** A block can have free space to its left, because its $x$ is fixed by its parent. A compaction step after the packing removes it, but then the tree of the result is a different tree.

## Implementations

The Python class stores the tree as two maps, left and right, and implements PACK with the linked contour in preorder, a direct quadratic packing for the tests, SWAP, DELETE and INSERT. SWAP renames the keys of the maps, in $O(n)$ time; with parent pointers it takes $O(1)$ time. Rotation changes the size maps. The tests pack all $336$ trees of four blocks, and all smaller trees, with random sizes, and check that the contour and the direct packing agree, that there is no overlap, that every block rests on the floor or on a block, and that the child rules hold. For three and four blocks they check that the best area over all trees equals the best area of a search over all positions. They also run random moves on trees of up to 30 blocks.

## History

Guo, Cheng and Yoshimura introduced the O-tree and admissible placements at DAC 1999. Chang, Chang, Wu and Wu gave the B*-tree at DAC 2000. It is a binary tree, so the moves need no balance of parentheses, and the packing with a contour takes amortized linear time. Chen and Chang used B*-trees with a fast annealing for fixed-outline and bus-driven floorplanning in 2006, and B*-trees became a common representation in floorplanners and in analog placement.

## References
