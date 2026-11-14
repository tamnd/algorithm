---
tag: GM5XEG
kind: data-structure
slug: o-tree-floorplan
name: O-tree
aliases:
- ordered tree floorplan
area: eda/partitioning-floorplanning-and-placement
level: advanced
summary: Guo, Cheng and Yoshimura's ordered tree for an admissible packing, encoded by a 2n bit string and a permutation, which is decoded in linear time.
model: word-ram
complexity:
  vars: {n: the number of blocks}
  time: {worst: O(n), average: O(n), best: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1999
  people: [Pei-Ning Guo, Chung-Kuan Cheng, Takeshi Yoshimura]
  note: Guo, Cheng and Yoshimura presented the O-tree and admissible placements at the Design Automation Conference in 1999.
prereqs: [floorplanning, rooted-tree, balanced-parentheses, b-star-tree-floorplan]
see_also: [sequence-pair, left-child-right-sibling, dyck-language, catalan-numbers, ordered-tree-generation, rectangle-packing, preorder-traversal, mosaic-floorplan]
sources:
  - paper: doi:10.1145/309847.309928
    title: Pei-Ning Guo, Chung-Kuan Cheng and Takeshi Yoshimura, An O-tree representation of non-slicing floorplan and its applications, Proceedings of the 36th Design Automation Conference, 268 to 273, 1999
    locator: the definition of the horizontal and the vertical O-tree, the encoding by a 2n-bit string and a permutation, the linear-time packing with a contour, admissible placements, and the search with deletions and insertions
  - paper: doi:10.1145/337292.337541
    title: Yun-Chih Chang, Yao-Wen Chang, Guang-Ming Wu and Shu-Wei Wu, B*-trees, a new representation for non-slicing floorplans, Proceedings of the 37th Design Automation Conference, 458 to 463, 2000
    locator: the binary tree form of the O-tree and the comparison with it
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 3, Chip Planning (floorplan representations; general locator)
---

An O-tree is an ordered tree that stores a packing of $n$ blocks. Its root is a virtual block of width 0 that stands for the left side of the chip, and each child is placed just to the right of its parent. The blocks are placed in depth-first order, and each one drops down onto the blocks placed before it. The tree is stored as a string of $2n$ bits for its shape and a [permutation](/permutation/) of the blocks for its labels, and a contour gives the packing in $O(n)$ time. Guo, Cheng and Yoshimura introduced it in 1999, with *admissible* placements: placements in which no block can move left or down. Its [left-child right-sibling](/left-child-right-sibling/) form is the [B*-tree](/b-star-tree-floorplan/) of the same packing.

## In plain words

Think of the left side of the chip as a wall. Some blocks touch the wall; they are the children of the wall. Each block can have blocks that touch its right side; they are its children. Children keep an order, from the lowest to the highest.

To build the picture, walk the tree from the wall: go to the first child, then to its first child, and so on, and come back to try the next child. Each time you reach a block, its left side is where its parent ends. Drop it down until it lands. The tree shape is a list of down and up steps, two steps for each block.

## The abstract type

The type stores an O-tree $(T, \pi)$ of a set of $n$ blocks. The operations are:

- PACK$(w, h)$: given the width $w_b$ and the height $h_b$ of each block, return the lower-left corner $(x_b, y_b)$ of each block and the width $W$ and the height $H$ of the packing.
- PARENTS: return the parent of each block, or the root.
- TO-B-STAR and FROM-B-STAR: change to the B*-tree of the same packing and back.

Guo and coauthors search over O-trees by deleting a block and inserting it at another place of the tree, and they turn a horizontal O-tree into a vertical one, built in the same way from the bottom side, to compact a packing in the other direction.

## Representation

$T$ is a string of $n$ zeros and $n$ ones. Read from the left, it is a depth-first walk of the tree: a 0 goes down to the next child of the current node, and a 1 goes back up to the parent. A string is a tree if and only if no prefix has more ones than zeros, the condition of [balanced parentheses](/balanced-parentheses/) with 0 as an open and 1 as a close parenthesis. Some sources use the opposite bits. $\pi$ lists the blocks in the order in which the walk reaches them, which is [preorder](/preorder-traversal/).

The packing rules are:

- the root $R$ is a virtual block with $x_R = 0$ and $w_R = 0$;
- a child $c$ of $p$ has $x_c = x_p + w_p$;
- each block, in the order of $\pi$, gets the highest top of the blocks before it whose $x$-ranges meet its own.

So the children of a node all start at the same $x$, and a later child sits above an earlier one. The storage is $2n$ bits for $T$ and $n \lceil \log_2 n \rceil$ bits for $\pi$.

The left-child right-sibling form turns the O-tree into a binary tree: the left child of a block is its first child, and the right child is its next sibling. The first child of $R$ is the root. This is exactly a B*-tree, and both rules give the same $x$: a first child is at $x_p + w_p$, and a next sibling at the $x$ of the sibling before it.

## Operations

```pseudo id=main
PACK(T, π, w, h)
L1  contour ← one segment [0, ∞) at height 0
L2  stack ← (R, the first segment)                ▷ each entry: a node, the segment where its next child starts
L3  for each bit t of T, from the left do
L4      if t = 1 then pop the stack; go on with the next bit
L5      b ← the next block of π; (p, s) ← the top entry of the stack
L6      x_b ← the left end of s; e ← x_b + w_b
L7      y_b ← the largest height of the segments from s on that start before e
L8      replace those segments by [x_b, e) at height y_b + h_b, keep the part of the last one after e; record (x_b, y_b), W, H
L9      set the segment of the top entry to s; push (b, the segment after s)
L10 return x, y, W, H
```

A first child of $b$ is the next block after $b$, so the segment that line L9 pushes still starts at $x_b + w_b$ when it is used. A later sibling of $b$ starts at the segment of $b$, which line L9 stores in the entry of the parent. The subtree of $b$ lies to the right of $x_b + w_b$ and does not change that segment.

## Example

Take the five blocks of the [B*-tree](/b-star-tree-floorplan/) example: A is $3 \times 2$, B is $2 \times 3$, C is $2 \times 1$, D is $2 \times 2$ and E is $3 \times 1$. Let $T = 0001110011$ and $\pi = (A, B, C, D, E)$. The walk goes down to A, B and C, up three times to $R$, down to D and E, and up two times. So A and D are the children of $R$, B is the child of A, C is the child of B, and E is the child of D.

| bit | block | parent | $x$ | $y$ | why |
|---|---|---|---|---|---|
| 0 | A | $R$ | 0 | 0 | the floor |
| 0 | B | A | 3 | 0 | the floor |
| 0 | C | B | 5 | 0 | the floor |
| 1, 1, 1 | | | | | back to $R$ |
| 0 | D | $R$ | 0 | 2 | on top of A |
| 0 | E | D | 2 | 3 | on top of B, which is higher than A over $[2, 5)$ |
| 1, 1 | | | | | back to $R$ |

The packing is $7 \times 4$. Its left-child right-sibling form has the root A, the left child B of A, the left child C of B, the right child D of A (the next sibling of A) and the left child E of D. That is the tree of the B*-tree example, with the same packing.

## Correctness

The string defines a unique ordered tree when no prefix has more ones than zeros, and the walk meets the blocks in preorder, so a parent is placed before its children and each $x$ is known in time. Each walk of line L7 starts at the segment that begins at $x_b$: for a first child, the segment pushed by its parent a moment before; for a later sibling, the segment of the sibling before it, which the subtree of that sibling does not touch. So each $y$ is the highest top below the block, and no two blocks overlap. Its left-child right-sibling form places the blocks in the same order and at the same $x$, so the O-tree and its B*-tree give the same packing. The full proof is in [the correctness proof](proofs/correctness.md).

The packing is compact downward but not always to the left, and two O-trees can give the same packing; the tests check an example of each. Guo and coauthors prove that each admissible placement has an O-tree, and that alternate changes between horizontal and vertical O-trees make any placement admissible. This is cited. The tests check its consequence for up to four blocks: the least area over all O-trees equals the least area of any packing.

## Complexity

| operation | time | extra space |
|---|---|---|
| PACK with the contour | $O(n)$ | $O(n)$ |
| PACK by a direct search over the placed blocks | $\Theta(n^2)$ | $O(n)$ |
| PARENTS, TO-B-STAR, FROM-B-STAR | $O(n)$ | $O(n)$ |
| check that a string is a tree | $O(n)$ | $O(1)$ |

PACK reads each bit one time. Each segment that a walk passes, except the first, is removed or cut, and each block makes at most one new segment, so all walks together take $O(n)$ steps. There are $C_n$ tree strings with $n$ zeros, where $C_n$ is the $n$th [Catalan number](/catalan-numbers/), so there are $n! \cdot C_n$ O-trees, as many as B*-trees. This is fewer than the $(n!)^2$ [sequence pairs](/sequence-pair/) for $n \ge 3$.

## Variants

- **Horizontal and vertical O-trees.** The tree on this page is the horizontal O-tree, with the left wall as the root. The vertical O-tree has the bottom side as the root, with $x$ and $y$ exchanged. Turns between the two compact a packing in both directions.
- **The B*-tree.** The B*-tree stores the same trees as binary trees, which makes deletion and insertion simpler and removes the need to keep the bit string valid.
- **Soft blocks and constraints.** Later works add soft blocks, pre-placed blocks and other constraints to O-tree searches.

## When to use it

Use an O-tree when a compact code of a packing matters, for example to store many packings, or when the search changes the tree by deletions and insertions of whole subtrees. The code needs about $n (2 + \log_2 n)$ bits. For most searches the [B*-tree](/b-star-tree-floorplan/) is simpler, since its moves need no change of a bit string. For slicing floorplans, a [normalized Polish expression](/normalized-polish-expression/) is the usual code.

## Pitfalls

- **Forgetting the virtual root.** The root is the left wall, not a block. There are $n + 1$ nodes and $2n$ bits. Without the virtual root, the blocks that touch the left wall have no common parent, and the tree is a forest.
- **Invalid strings.** A move that changes bits must keep the prefix condition and the equal counts. Otherwise the walk pops the root or ends inside the tree.
- **The wrong start segment for a sibling.** A later sibling starts at the segment of the sibling before it, not at the segment after its parent: the segment after the parent may have been cut by the subtrees in between.
- **Counting packings by trees.** Two O-trees can give the same packing, so $n! \cdot C_n$ is an upper bound on the number of packings of $n$ blocks, not the count.

## Implementations

The Python class stores the bit string and the permutation and implements the tree test, PARENTS, PACK with the linked contour, a direct quadratic packing for the tests, TO-B-STAR and FROM-B-STAR. The tests check all O-trees of up to four blocks with random sizes: the two packings agree, there is no overlap, the $x$ rule and the rest on the floor or on a block hold, the packing equals that of the B*-tree form, and FROM-B-STAR gives the same O-tree back. For three and four blocks, the best area over all O-trees equals the best area of a search over all positions. They also check 300 random O-trees of up to 40 blocks.

## History

Guo, Cheng and Yoshimura introduced the O-tree at DAC 1999, with admissible placements, the $2n$-bit code, the linear-time packing and a search by deletions and insertions. Chang, Chang, Wu and Wu gave the B*-tree at DAC 2000 as a binary tree for the same packings, and it replaced the O-tree in many later floorplanners.

## References
