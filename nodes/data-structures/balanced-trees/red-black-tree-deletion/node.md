---
tag: KYJFQJ
kind: algorithm
slug: red-black-tree-deletion
name: Red-black tree deletion
aliases:
- Red-black BST deletion
area: data-structures/balanced-trees
level: core
summary: Removing a key from a left-leaning red-black tree while keeping it balanced, by carrying red links down the search path.
uses: [left-leaning-red-black-tree, tree-rotation]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(log n)}
prereqs: [left-leaning-red-black-tree, two-three-tree, tree-rotation, bst-deletion]
see_also: [red-black-tree, two-three-four-tree, red-black-correspondence-with-2-3-4-trees, aa-tree, avl-tree, red-black-height-theorem]
sources:
  - url: https://sedgewick.io/wp-content/themes/sedgewick/papers/2008LLRB.pdf
    title: Robert Sedgewick, Left-leaning Red-Black Trees, 2008
    locator: deletion, with moveRedLeft, moveRedRight, deleteMin and fixUp
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (deletion in red-black BSTs, the exercises on delete the minimum and delete)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Section 13.4, Deletion (the bottom-up method with RB-DELETE-FIXUP, for comparison)
---

Red-black tree deletion removes a key from a [left-leaning red-black tree](/left-leaning-red-black-tree/) and keeps all its rules. It works top-down, in one pass from the root: on the way down it makes sure that the current node is not a 2-node of the corresponding [2-3 tree](/two-three-tree/), by borrowing a key from a sibling or by merging with the parent, which in the binary tree means color flips and rotations. When the key is reached at the bottom, it is in a red node, so it can be cut off without changing any black count. On the way back up, the same FIX-UP step as in insertion removes the temporary right-leaning red links and 4-nodes. The time is $\Theta(\log n)$ in the worst case. The method is Sedgewick's, from 2008; the classic bottom-up deletion for [red-black trees](/red-black-tree/) is on that page.

## In plain words

In a 2-3 tree, a key can leave a node that holds two keys, but not a node that holds one key: that node would become empty, and the tree would lose a level in one place. So the deletion walks down and never steps into a one-key node. If the next node on the way has only one key, it first gets a second one: from a sibling that has two, or else by pulling one key down from the parent and merging with the sibling. The parent can spare a key, because the walk made sure of that one step before.

At the bottom, the key to delete then sits in a node with two keys, and it can go. On the way back up, the temporary fat nodes made during the walk are split again.

## The problem

Input: a left-leaning red-black tree $T$ and a key $k$. The tree satisfies (L1) the search order, (L2) no red right link, (L3) no two red links in a row, (L4) the same number of black links on every path from the root to nil, and (L5) a black root. Output: the same kind of tree, with the keys of $T$ except $k$. If $k$ is not in $T$, the tree does not change.

## The algorithm

The tree uses the steps of the [left-leaning red-black tree](/left-leaning-red-black-tree/): ROTATE-LEFT and ROTATE-RIGHT, which turn a red link to the other side and give the new top the color of the old one, and FLIP-COLORS, which inverts the colors of a node and its two children. In the 2-3 view, a flip at a black node with two red children splits a 4-node, and a flip at a red node with two black children merges the node with its parent's key and its sibling into a 4-node.

```pseudo id=main
DELETE(T, k)
L1  if k is not in T then return
L2  if T.root.left and T.root.right are both black then T.root.red ← true
L3  T.root ← REMOVE(T.root, k)
L4  if T.root ≠ nil then T.root.red ← false

MOVE-RED-LEFT(h)                           ▷ h is red; h.left and h.left.left are black
L5  FLIP-COLORS(h)                         ▷ merge: h.left joins its parent key and its sibling
L6  if h.right.left is red then h.right ← ROTATE-RIGHT(h.right); h ← ROTATE-LEFT(h); FLIP-COLORS(h)   ▷ borrow
    return h

MOVE-RED-RIGHT(h)                          ▷ h is red; h.right and h.right.left are black
L7  FLIP-COLORS(h)
L8  if h.left.left is red then h ← ROTATE-RIGHT(h); FLIP-COLORS(h)   ▷ borrow
    return h

REMOVE(h, k)                               ▷ k is in the subtree, and h is not a 2-node
L9  if k < h.key then
L10     if h.left and h.left.left are both black then h ← MOVE-RED-LEFT(h)
L11     h.left ← REMOVE(h.left, k)
    else
L12     if h.left is red then h ← ROTATE-RIGHT(h)
L13     if k = h.key and h.right = nil then return nil
L14     if h.right and h.right.left are both black then h ← MOVE-RED-RIGHT(h)
L15     if k = h.key then h.key ← the least key of h.right; h.right ← DELETE-MIN(h.right)
L16     else h.right ← REMOVE(h.right, k)
L17 return FIX-UP(h)

DELETE-MIN(h)
L18 if h.left = nil then return nil
L19 if h.left and h.left.left are both black then h ← MOVE-RED-LEFT(h)
L20 h.left ← DELETE-MIN(h.left)
L21 return FIX-UP(h)

FIX-UP(h)
L22 if h.right is red and h.left is black then h ← ROTATE-LEFT(h)
L23 if h.left is red and h.left.left is red then h ← ROTATE-RIGHT(h)
L24 if h.left is red and h.right is red then FLIP-COLORS(h)
L25 return h
```

On the way left (lines L9 to L11), the test at line L10 asks whether $h.left$ is a 2-node of the 2-3 tree: it is when both $h.left$ and its left child are black. Then MOVE-RED-LEFT borrows from the right sibling if that sibling is a 3-node (line L6), and else merges. On the way right, line L12 first turns a red left link to the right, so that a red link on the right side can carry the key down, and line L14 does the same check as line L10 on the right child. Line L13 handles the bottom: there the node is red and has no children. An internal key is replaced by its successor, which DELETE-MIN removes from the right subtree (line L15), as in the deletion of a plain [binary search tree](/bst-deletion/).

## Example

Start from the tree that the insertion of S, E, A, R, C, H, X, M, P, L gives. A tree is written as (left, key, right), a leaf as its key, and a star marks a red node:

$$(((A^*, C, \text{nil}), E, (H^*, L, \text{nil})), M, (P, R, (S^*, X, \text{nil}))).$$

It is the 2-3 tree [M] ([E] ([A C], [H L]), [R] ([P], [S X])). Delete R, then M, then A.

**Delete R.** The root M has two black children, so line L2 paints it red. Since R > M, line L14 finds the right child R and its left child P black and calls MOVE-RED-RIGHT(M), which flips M, E and R: now M is black with two red children (the 4-node [E M R] in the 2-3 view). The left child E has a black left child C, so line L8 does nothing. REMOVE goes right to R, which now is red. R has a right child X with the red left child S, so line L14 does nothing there; line L15 replaces R by its successor S and deletes S from the subtree of X, where S is a red leaf. On the way up, FIX-UP at M sees two red children and flips them. The tree is

$$(((A^*, C, \text{nil}), E, (H^*, L, \text{nil})), M, (P, S, X)).$$

**Delete M.** Line L2 paints the root red again; line L14 calls MOVE-RED-RIGHT(M), which flips. Now $k = M$, so line L15 replaces M by its successor P and calls DELETE-MIN on S. There P is a black leaf, so line L19 calls MOVE-RED-LEFT(S): the flip makes S black, P and X red (the merge of [P], S and [X] into [P S X]), and line L6 does nothing, since X has no red left child. DELETE-MIN removes the red leaf P, and FIX-UP at S sees the red right link to X and rotates left. The tree is

$$(((A^*, C, \text{nil}), E^*, (H^*, L, \text{nil})), P, (S^*, X, \text{nil})).$$

**Delete A.** The root P has a red left child, so line L2 does nothing. On the way down to A, each left child is red or has a red left child, so no move is needed, and A is a red leaf, cut off at line L13. The tree is $((C, E^*, (H^*, L, \text{nil})), P, (S^*, X, \text{nil}))$.

In the 2-3 view, the three results are [M] ([E] ([A C], [H L]), [S] ([P], [X])), then [E P] ([A C], [H L], [S X]), and last [E P] ([C], [H L], [S X]).

## Correctness

The proof has two parts. First, each step keeps the search order and the black counts: a rotation moves a red link and gives the new top the color of the old one, and a flip is done only at a node whose two children have the color opposite to its own. Second, a precondition holds at each call of REMOVE: $h$ is red, or $h.left$ is red, or $h.right$ is red with $k \ge h.key$. Lines L10 and L14 restore it one level down before each recursive call, so at the bottom the key is in a red leaf, and cutting it off keeps the black counts. On the way up, FIX-UP gets a node whose two subtrees are valid and returns a valid subtree. The full proof, with each case, is in the proofs folder.

## Complexity

REMOVE and DELETE-MIN go down one path and back up, with $O(1)$ work at each level: a constant number of flips, rotations and color tests for each node on the path. The height is at most $2 \lg(n + 1)$ (see [red-black height bound](/red-black-height-theorem/)), so a deletion takes $\Theta(\log n)$ time in the worst case. The search at line L1 costs another $O(\log n)$. The recursion uses $O(\log n)$ stack space.

Unlike the bottom-up deletion of CLRS, which does at most three rotations, this method can rotate and flip at every level of the path, also when the tree did not need it: it prepares each node on the way down whether or not the deletion will end there.

## Properties

- **One pass.** The method is top-down: it does not need parent pointers or a stack of the path, apart from the recursion, which only carries FIX-UP back up.
- **Shared code.** FIX-UP is the same as in insertion.
- **Deterministic.** The result depends only on the tree and the key.

## Variants and improvements

- **Delete the minimum or the maximum.** DELETE-MIN alone gives a priority-queue deletion on a balanced tree. DELETE-MAX is its mirror image, with a rotation to the right at each step, because red links lean left.
- **2-3-4 trees.** The same top-down idea works for the 2-3-4 form of LLRB trees and for [2-3-4 trees](/two-three-four-tree/) themselves, where each node on the path is made a 3-node or 4-node before the step down.
- **Bottom-up deletion.** The classic [red-black tree](/red-black-tree/) deletes as in a plain search tree and then repairs a missing black from the bottom up, with at most three rotations.
- **Lazy deletion.** Marking a node as deleted and rebuilding later avoids the cases entirely, at the cost of space.

## When to use it

Use this method with a left-leaning red-black tree, where it keeps the code short and shares FIX-UP with insertion. When rotations are costly, for example in a persistent tree or a tree with large summaries in its nodes, the bottom-up method of the classic red-black tree does fewer changes.

## Pitfalls

- **Deleting a key that is not there.** REMOVE moves red links down along the search path and assumes that the key is in the subtree. For an absent key it reaches nil and fails. Line L1 searches first. A test of the implementation removes 0 from the tree (1, 2, 3) without this test and gets an error.
- **The test at line L12.** On the way right, a red left link must be rotated to the right before the step down. Without it, the right child can be a 2-node with no red link to borrow, and the precondition fails one level down.
- **Reading a child of nil.** The tests at lines L10, L14 and L19 read the left child of a child. That child is not nil there: the key lies below it, or by the black counts it has a sibling at the same black height.
- **Forgetting line L4.** If the root stays red after REMOVE, (L5) fails, and the test at line L2 of the next deletion is no longer enough.

## Implementations

## History

Guibas and Sedgewick (1978) gave top-down insertion and deletion for their red-black trees, in the 2-3-4 view. Sedgewick's 2008 paper on left-leaning red-black trees gave the short recursive form with moveRedLeft and moveRedRight, and the fourth edition of Algorithms by Sedgewick and Wayne (2011) presents it with deleteMin and deleteMax as exercises. The bottom-up deletion with RB-DELETE-FIXUP, in CLRS Chapter 13, is the common choice in libraries.

## References
