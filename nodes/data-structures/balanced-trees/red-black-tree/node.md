---
tag: WQME6V
kind: data-structure
slug: red-black-tree
name: Red-black tree
aliases:
- red-black BST
- RB tree
area: data-structures/balanced-trees
level: core
summary: A BST with red/black node colours obeying four invariants that bound the height by 2 log2(n+1); the standard balanced BST in libraries.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, tree-rotation, black-height]
see_also: [red-black-height-theorem, red-black-correspondence-with-2-3-4-trees, left-leaning-red-black-tree, avl-tree, two-three-four-tree, order-statistic-tree, persistent-red-black-tree, aa-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Sections 13.1 to 13.4 (properties, Lemma 13.1, rotations, RB-INSERT-FIXUP and RB-DELETE-FIXUP)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (red-black BSTs, Algorithm 3.4)
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, 19th Annual Symposium on Foundations of Computer Science, 1978
    locator: pages 8 to 21
  - paper: doi:10.1007/BF00289509
    title: Rudolf Bayer, Symmetric binary B-trees, data structure and maintenance algorithms, Acta Informatica 1(4), 1972
    locator: pages 290 to 306
  - url: "https://opendatastructures.org/"
    title: Pat Morin, Open Data Structures
    locator: Chapter 9, Red-Black Trees (Section 9.1, 2-4 trees, and Section 9.2, a simulated 2-4 tree)
---

A red-black tree is a [binary search tree](/binary-search-tree/) in which each node is red or black, the root and the empty leaves are black, a red node has no red child, and each path from a node down to an empty leaf has the same number of black nodes. These rules keep the height at most $2 \lg(n + 1)$ for $n$ keys, so search, insertion and deletion take $\Theta(\log n)$ time in the worst case, with at most two [rotations](/tree-rotation/) per insertion and three per deletion. It is the [balanced binary search tree](/balanced-binary-search-tree/) behind `std::map` in the common C++ libraries and `TreeMap` in Java.

## In plain words

Each node carries one extra bit, a color. Count only the black nodes: on every way down from the top to the bottom, the count is the same. So if you ignore the red nodes, the tree is perfectly balanced. No red node has a red child, so a path has at most one red node for each black one. The longest path is at most twice as long as the shortest.

A new key goes into a new red node at the bottom. That never changes the black counts, but it can put a red node under a red node. The fix either repaints a few nodes and moves the problem two levels up, or ends it with one or two rotations. A deletion can remove a black node, and its fix pushes a missing black up the tree in the same way.

## The abstract type

A red-black tree implements the [ordered set](/ordered-set/): `contains(T, k)`, `insert(T, k)`, `delete(T, k)`, and the order queries minimum, maximum, predecessor, successor and in-order iteration of a [binary search tree](/binary-search-tree/). With a value in each node it is an [ordered symbol table](/ordered-symbol-table/). The keys come from a total order, and each key is stored once.

## Representation

Each node has a key, a color, two children and a parent. As in CLRS, all empty children point to one black sentinel node $T.nil$, which plays the part of every leaf, and the root's parent is $T.nil$. The keys sit in the *internal* nodes, the nodes other than $T.nil$.

**Invariant.** Besides the search-tree order (R0), the tree satisfies:

1. (R1) The root is black.
2. (R2) Every leaf ($T.nil$) is black.
3. (R3) A red node has two black children.
4. (R4) For each node $x$, all paths from $x$ down to a leaf contain the same number of black nodes.

The number of black nodes on such a path, not counting $x$, is the [black-height](/black-height/) $bh(x)$. The [red-black height bound](/red-black-height-theorem/) proves from (R3) and (R4) that a tree with $n$ internal nodes has height at most $2\lg(n+1)$. The [correspondence with 2-3-4 trees](/red-black-correspondence-with-2-3-4-trees/) explains the rules: merging each red node into its black parent gives a [2-3-4 tree](/two-three-four-tree/) with all leaves at one depth.

## Operations

A search is the search of a [binary search tree](/bst-search/). It ignores the colors and changes nothing. Below, $z.p$ is the parent of $z$ and $z.p.p$ its grandparent.

```pseudo id=main
RB-INSERT(T, k)
L1  y ← T.nil, x ← T.root
L2  while x ≠ T.nil do                     ▷ walk down to the place of k
L3      y ← x
L4      if k < x.key then x ← x.left else if k > x.key then x ← x.right else return
L5  z ← a new red node with key k, children T.nil and parent y
L6  if y = T.nil then T.root ← z
L7  else if k < y.key then y.left ← z else y.right ← z
L8  INSERT-FIXUP(T, z)

INSERT-FIXUP(T, z)                         ▷ only (R1) or (R3) at z may fail
L9  while z.p.color = red do               ▷ z and its parent are red
L10     if z.p = z.p.p.left then
L11         u ← z.p.p.right                ▷ u is the uncle of z
L12         if u.color = red then          ▷ case 1: recolor, move up two levels
L13             z.p.color ← black, u.color ← black, z.p.p.color ← red, z ← z.p.p
L14         else
L15             if z = z.p.right then z ← z.p, LEFT-ROTATE(T, z)   ▷ case 2 becomes case 3
L16             z.p.color ← black, z.p.p.color ← red              ▷ case 3
L17             RIGHT-ROTATE(T, z.p.p)
L18     else the same as lines L11 to L17, with left and right exchanged
L19 T.root.color ← black
```

**Insertion.** Lines L1 to L7 insert $k$ in a new leaf position, as in a plain search tree, and color the new node $z$ red. A red node adds nothing to the black counts, so (R4) still holds. The only rules that can fail are (R1), if $z$ is the root, and (R3), if the parent of $z$ is red. The loop of line L9 runs while $z$ and its parent are both red. The parent is then not the root (the root is black), so the grandparent exists and is black.

- *Case 1, the uncle is red.* Line L13 paints the parent and the uncle black and the grandparent red. Each path through the grandparent still has the same number of black nodes. The only possible violation is now at the grandparent, two levels up, so $z$ moves there.
- *Case 2, the uncle is black and $z$ is an inner child.* Line L15 rotates at the parent, which makes $z$ an outer child, and the old parent becomes the new $z$. This is case 3.
- *Case 3, the uncle is black and $z$ is an outer child.* Line L16 swaps the colors of the parent and the grandparent, and line L17 rotates at the grandparent. The parent is now a black root of the subtree with two red children, and the loop ends.

Line L19 repairs (R1) if case 1 painted the root red. Case 1 can repeat up the tree, but cases 2 and 3 run at most once, so an insertion does at most two rotations.

```pseudo id=delete
RB-TRANSPLANT(T, u, v)                     ▷ put the subtree v in the place of u
L20 if u.p = T.nil then T.root ← v
L21 else if u = u.p.left then u.p.left ← v else u.p.right ← v
L22 v.p ← u.p

RB-DELETE(T, z)                            ▷ z is a node of T
L23 y ← z, c ← y.color                     ▷ y is the node that leaves its place
L24 if z.left = T.nil then x ← z.right, RB-TRANSPLANT(T, z, z.right)
L25 else if z.right = T.nil then x ← z.left, RB-TRANSPLANT(T, z, z.left)
L26 else
L27     y ← the node with the least key in z.right, c ← y.color
L28     x ← y.right
L29     if y ≠ z.right then RB-TRANSPLANT(T, y, y.right), y.right ← z.right, y.right.p ← y
L30     else x.p ← y                       ▷ also when x = T.nil
L31     RB-TRANSPLANT(T, z, y), y.left ← z.left, y.left.p ← y, y.color ← z.color
L32 if c = black then DELETE-FIXUP(T, x)

DELETE-FIXUP(T, x)                         ▷ x carries one extra black
L33 while x ≠ T.root and x.color = black do
L34     if x = x.p.left then
L35         w ← x.p.right                  ▷ w is the sibling of x
L36         if w.color = red then          ▷ case 1: make the sibling black
L37             w.color ← black, x.p.color ← red, LEFT-ROTATE(T, x.p), w ← x.p.right
L38         if w.left.color = black and w.right.color = black then
L39             w.color ← red, x ← x.p     ▷ case 2: move the extra black up
L40         else
L41             if w.right.color = black then          ▷ case 3: make the far child red
L42                 w.left.color ← black, w.color ← red, RIGHT-ROTATE(T, w), w ← x.p.right
L43             w.color ← x.p.color, x.p.color ← black, w.right.color ← black
L44             LEFT-ROTATE(T, x.p), x ← T.root          ▷ case 4: done
L45     else the same as lines L35 to L44, with left and right exchanged
L46 x.color ← black
```

**Deletion.** RB-DELETE removes $z$ as in a plain search tree. If $z$ has at most one child, $z$ itself leaves the tree and its child $x$ takes its place (lines L24 and L25). If $z$ has two children, its successor $y$ takes the place of $z$ with the color of $z$, and the right child $x$ of $y$ takes the old place of $y$ (lines L27 to L31). In each case one node of color $c$ leaves its place, and $x$ moves into that place. If $c$ is red, no black count changes and no red node gets a red child, so nothing is to fix. If $c$ is black, each path through $x$ lost one black node. We say that $x$ carries an *extra black*: it counts twice. DELETE-FIXUP moves the extra black up or gets rid of it.

- If $x$ is red, line L46 paints it black and the extra black is gone.
- *Case 1, the sibling $w$ is red.* Its children are black. Line L37 swaps the colors of $w$ and the parent and rotates at the parent. The new sibling is one of the old black children, so one of cases 2 to 4 follows.
- *Case 2, $w$ is black with two black children.* Line L39 paints $w$ red, which removes one black from the paths through $w$, and moves the extra black to the parent. If the parent was red (always the case after case 1), the loop ends and line L46 paints it black.
- *Case 3, $w$ is black, its near child red and its far child black.* Line L42 swaps the colors of $w$ and its near child and rotates at $w$. Now the far child of the new sibling is red: case 4.
- *Case 4, $w$ is black and its far child is red.* Lines L43 and L44 give $w$ the color of the parent, paint the parent and the far child black, and rotate at the parent. The extra black is absorbed, and $x \leftarrow T.root$ ends the loop.

Only case 2 repeats, and it does no rotation. Cases 1, 3 and 4 do one rotation each, and case 4 ends the loop, so a deletion does at most three rotations.

**Cost.** The walk down takes $O(h)$ steps. Each pass of a fixup loop does $O(1)$ work and moves $x$ or $z$ up by at least one level (case 1 of the insertion by two), or ends the loop. So each operation takes $O(h) = O(\log n)$ time.

## Example

Insert 10, 20, 30, 15, 25, 5, 1, then delete 20, 1, 30. A tree is written as (left, key, right), with $r$ for red and $b$ for black, and an empty child as nil.

| operation | fixup | tree after |
|---|---|---|
| insert 10 | line L19 paints the root black | 10b |
| insert 20 | parent is black, no fix | (nil, 10b, 20r) |
| insert 30 | uncle nil is black, 30 is outer: case 3, left rotation at 10 | (10r, 20b, 30r) |
| insert 15 | uncle 30 is red: case 1, then the root is painted black | ((nil, 10b, 15r), 20b, 30b) |
| insert 25 | parent 30 is black | ((nil, 10b, 15r), 20b, (25r, 30b, nil)) |
| insert 5 | parent 10 is black | ((5r, 10b, 15r), 20b, (25r, 30b, nil)) |
| insert 1 | uncle 15 is red: case 1 at 5, then 10 is red under the black root | (((1r, 5b, nil), 10r, 15b), 20b, (25r, 30b, nil)) |
| delete 20 | successor 25 is red; it takes the place and the color of 20; no fix | (((1r, 5b, nil), 10r, 15b), 25b, 30b) |
| delete 1 | 1 is red; no fix | ((5b, 10r, 15b), 25b, 30b) |
| delete 30 | $x$ = nil, sibling 10 red: case 1, right rotation at 25; new sibling 15 has black children: case 2, the extra black moves to 25, which is red, and line L46 paints it black | (5b, 10b, (15r, 25b, nil)) |

After each step, every path from the root down to a nil leaf has the same number of black nodes: 1 after the first insertion, 2 after "insert 15", and 2 at the end. The six insertions after the first one did one rotation in total, and the three deletions one rotation.

## Correctness

Each operation keeps (R0) to (R4) and holds the right set of keys. The insertion proof is a [loop invariant](/loop-invariant/) of line L9: the tree satisfies (R0), (R2) and (R4); if $z$ is the root, it is the only possible failure of (R1); and the only possible failure of (R3) is that $z$ and its parent are both red. The deletion proof counts the extra black at $x$ and shows that the invariant "the tree with $x$ counted twice satisfies (R0) to (R4), except that $x$ may be red and doubly black" holds at line L33. Both loops move up the tree or stop. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [comparison model](/comparison-model/), with $O(1)$ time for each pointer change, color change and rotation. Let $n$ be the number of keys.

| operation | worst case | rotations |
|---|---|---|
| contains, minimum, maximum, predecessor, successor | $\Theta(\log n)$ | 0 |
| insert | $\Theta(\log n)$ | at most 2 |
| delete | $\Theta(\log n)$ | at most 3 |
| space | $\Theta(n)$ nodes, one bit of color each | |

**Upper bound.** By the [red-black height bound](/red-black-height-theorem/), the height is at most $2 \lg(n + 1)$. The walk down and the fixup loops take $O(1)$ time per level, so each operation takes $O(\log n)$.

**Lower bound.** Each binary tree of $n$ nodes has height at least $\lceil \lg(n+1) \rceil$, so a search for a deepest key takes $\Omega(\log n)$ comparisons, and insertion and deletion search first. So the time is $\Theta(\log n)$ in the worst case.

**Rotations.** In INSERT-FIXUP, case 1 does no rotation, and cases 2 and 3 end the loop after at most two rotations. In DELETE-FIXUP, case 2 does no rotation; case 1 can be followed only by case 2 with a red parent, which ends the loop, or by case 3 or 4; case 3 is always followed by case 4, which ends the loop. So at most three rotations happen. The color changes can go up the whole path, $O(\log n)$ in the worst case.

## Variants

- **[Left-leaning red-black trees](/left-leaning-red-black-tree/).** Sedgewick's variant allows a red node only as a left child. It matches [2-3 trees](/two-three-tree/) one to one and has much shorter code, but makes more rotations.
- **[AA trees](/aa-tree/).** Andersson's variant allows a red node only as a right child and stores levels instead of colors.
- **Top-down insertion.** Guibas and Sedgewick split 4-nodes on the way down, so the insertion needs one pass and no parent pointers. This is the insertion of [2-3-4 trees](/two-three-four-tree/) in red-black form.
- **Augmented red-black trees.** A size field gives the [order-statistic tree](/order-statistic-tree/), and a maximum endpoint field gives the [interval tree](/interval-tree/). Each rotation recomputes the field at the two rotated nodes.
- **[Persistent red-black trees](/persistent-red-black-tree/).** Path copying keeps the old versions in $O(\log n)$ extra space per update.
- **[WAVL trees](/wavl-tree/).** Rank-balanced trees with the AVL height when there are no deletions and never worse than the red-black height.

## When to use it

Use a red-black tree as the default balanced tree when insertions and deletions are frequent: each update does $O(1)$ rotations, so augmented fields and the memory are touched little. An [AVL tree](/avl-tree/) is shorter by up to a factor of about $1.44/2$ in the worst case and so searches a bit faster, but a deletion may rotate at each level. A [left-leaning red-black tree](/left-leaning-red-black-tree/) or a [treap](/treap/) is easier to write correctly. For data on disk, use a [B-tree](/b-tree/), and for a cache-friendly in-memory set of small keys, a B-tree with small nodes is often faster than any binary tree.

## Pitfalls

- **Forgetting line L19.** Case 1 can paint the root red. Without line L19, (R1) fails after "insert 15" of the example: the root 20 stays red. The test of the example checks the color of each node.
- **Setting the parent of the sentinel.** Line L30 sets $x.p \leftarrow y$ even when $x = T.nil$, and RB-TRANSPLANT sets $v.p$ even for the sentinel. DELETE-FIXUP reads $x.p$ at line L34. With nil pointers instead of a sentinel, keep the parent of $x$ in a separate variable. The step "delete 30" of the example needs it.
- **The wrong color test.** Line L32 must test the color $c$ of the node that left its place ($y$ in the two-child case), not the color of $z$. In the two-child case, $y$ takes the color of $z$, so the color that disappears is the old color of $y$.
- **Case 3 without the update of $w$.** After the rotation in line L42, the sibling of $x$ is a new node. Line L42 must read $w \leftarrow x.p.right$ again, or case 4 recolors the wrong node.

## Implementations

## History

Rudolf Bayer described *symmetric binary B-trees* in 1972, binary trees that represent B-trees of order 4. Leo Guibas and Robert Sedgewick gave the red and black coloring in 1978, in "A dichromatic framework for balanced trees", and showed how many balanced trees fit in this frame, with insertion in one pass down. The delete-fixup with four cases and the bound of three rotations per deletion are presented in CLRS, Chapter 13. In 2008 Sedgewick introduced the [left-leaning variant](/left-leaning-red-black-tree/).

## References
