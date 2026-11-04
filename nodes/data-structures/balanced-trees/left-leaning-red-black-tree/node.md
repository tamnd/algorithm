---
tag: 1ZQX62
kind: data-structure
slug: left-leaning-red-black-tree
name: Left-leaning red-black tree
aliases:
- LLRB tree
- left-leaning RB tree
area: data-structures/balanced-trees
level: core
summary: A red-black variant restricting red links to the left, which simplifies insertion and deletion to a small set of cases.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, tree-rotation, two-three-tree, red-black-tree]
see_also: [red-black-tree-deletion, two-three-tree, red-black-correspondence-with-2-3-4-trees, aa-tree, two-three-four-tree, red-black-height-theorem]
sources:
  - url: https://sedgewick.io/wp-content/themes/sedgewick/papers/2008LLRB.pdf
    title: Robert Sedgewick, Left-leaning Red-Black Trees, 2008
    locator: insertion with rotateLeft, rotateRight and colorFlip; deletion with moveRedLeft and moveRedRight
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (red-black BSTs, Algorithm 3.4, and the deletion exercises)
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, 19th Annual Symposium on Foundations of Computer Science, 1978
    locator: pages 8 to 21
---

A left-leaning red-black tree (LLRB tree) is a [red-black tree](/red-black-tree/) with one more rule: a red link may only be a left link. With this rule, each LLRB tree is the binary form of exactly one [2-3 tree](/two-three-tree/): a black node with a red left child is a 3-node, and every other node is a 2-node. Insertion needs only three local steps, which are a left rotation, a right rotation and a color flip, applied on the way back up the search path, and the whole procedure fits in a few lines. The height is at most $2 \lg(n + 1)$, so search, insertion and deletion take $\Theta(\log n)$ time in the worst case. Robert Sedgewick described the variant in 2008.

## In plain words

Think of a 2-3 tree, where a node holds one key or two. To store it as a binary tree, keep each one-key node as it is, and split each two-key node into two binary nodes: the larger key on top, the smaller key as its left child, joined by a link that you color red. All other links are black.

The rules then say what a 2-3 tree says. A red link always points left, because a two-key node is always split the same way. No node has two red links, because a node holds at most two keys. Every path from the top to the bottom crosses the same number of black links, because all 2-3 leaves are at one depth.

An insertion adds a red link at the bottom. Three small fixes repair any broken rule and may pass a red link up.

## The abstract type

An LLRB tree implements the [ordered set](/ordered-set/): `contains(T, k)`, `insert(T, k)` and `delete(T, k)`, and the order operations of a search tree (minimum, maximum, predecessor, successor, in-order iteration). With a value in each node it is an [ordered symbol table](/ordered-symbol-table/); Sedgewick and Wayne use it this way. The keys come from a total order, and the tree holds each key at most once.

## Representation

Each node $h$ has a key, a left and a right child (each a node or nil), and a color bit $h.red$. The color of a node is the color of the link from its parent to it; nil links are black. A *black-link count* of a path is the number of black nodes on it.

**Invariant.**

1. (L1) The tree is a binary search tree.
2. (L2) No right child is red: red links lean left.
3. (L3) No red node has a red left child, so no path has two red links in a row.
4. (L4) Every path from the root to nil has the same number of black nodes.
5. (L5) The root is black.

By (L2) and (L3), each black node has at most one red child, on the left. Merging each red node into its black parent gives a node with one or two keys, and by (L4) all of the resulting nodes at the bottom are at the same depth: the result is a 2-3 tree. The map works in both directions, so LLRB trees and 2-3 trees are in one-to-one correspondence. The [2-3-4 correspondence](/red-black-correspondence-with-2-3-4-trees/) of the classic red-black tree is the same idea with one more node type.

**Height.** If the 2-3 tree has height $H$, each LLRB path has $H$ black nodes and at most $H$ red nodes, so the height is at most $2H \le 2 \lg(n + 1)$.

## Operations

A search is the search of a [binary search tree](/bst-search/); it ignores the colors.

Three steps change the shape. ROTATE-LEFT turns a red right link into a red left link: the right child $x$ of $h$ moves up, takes the color of $h$, and $h$ becomes its red left child. ROTATE-RIGHT is the mirror image. FLIP-COLORS inverts the colors of a node and its two children: when both children are red, this splits a temporary 4-node and passes the middle key up to the parent as a red link. Each takes $O(1)$ time and keeps (L1) and (L4).

```pseudo id=main
PUT(h, k)                                       ▷ returns the new root of this subtree
L1  if h = nil then return a new red node with key k
L2  if k < h.key then h.left ← PUT(h.left, k)
L3  else if k > h.key then h.right ← PUT(h.right, k)
L4  else return h                               ▷ k is already there
L5  return FIX-UP(h)

FIX-UP(h)
L6  if h.right is red and h.left is black then h ← ROTATE-LEFT(h)
L7  if h.left is red and h.left.left is red then h ← ROTATE-RIGHT(h)
L8  if h.left is red and h.right is red then FLIP-COLORS(h)
L9  return h

INSERT(T, k)
L10 T.root ← PUT(T.root, k); T.root.red ← false
```

Deletion is longer. On the way down it makes sure that the current node or its left child is red, so that the key to delete is never in a 2-node; on the way up, FIX-UP removes the red right links and 4-nodes it made. The page [red-black tree deletion](/red-black-tree-deletion/) gives the full argument.

```pseudo id=delete
DELETE(T, k)
L11 if k is not in T then return
L12 if T.root.left and T.root.right are both black then T.root.red ← true
L13 T.root ← REMOVE(T.root, k)
L14 if T.root ≠ nil then T.root.red ← false
L15 n ← n − 1

MOVE-RED-LEFT(h)                                ▷ h is red; h.left and h.left.left are black
L16 FLIP-COLORS(h)
L17 if h.right.left is red then h.right ← ROTATE-RIGHT(h.right); h ← ROTATE-LEFT(h); FLIP-COLORS(h)
    return h

MOVE-RED-RIGHT(h)                               ▷ h is red; h.right and h.right.left are black
L18 FLIP-COLORS(h)
L19 if h.left.left is red then h ← ROTATE-RIGHT(h); FLIP-COLORS(h)
    return h

REMOVE(h, k)                                    ▷ k is in the subtree; h or h.left is red
L20 if k < h.key then
L21     if h.left and h.left.left are both black then h ← MOVE-RED-LEFT(h)
L22     h.left ← REMOVE(h.left, k)
    else
L23     if h.left is red then h ← ROTATE-RIGHT(h)
L24     if k = h.key and h.right = nil then return nil
L25     if h.right and h.right.left are both black then h ← MOVE-RED-RIGHT(h)
L26     if k = h.key then h.key ← the least key of h.right; h.right ← DELETE-MIN(h.right)
L27     else h.right ← REMOVE(h.right, k)
L28 return FIX-UP(h)
```

DELETE-MIN$(h)$ is REMOVE for the least key: it returns nil if $h.left$ is nil, else it does line L21, recurses on $h.left$ and returns FIX-UP$(h)$.

## Example

Insert the letters S, E, A, R, C, H, X, M, P, L into an empty tree, then delete E, X and S. A tree is written as (left, key, right), a leaf as its key, and a star marks a red node.

| operation | steps | tree after |
|---|---|---|
| insert S | new root, painted black | S |
| insert E | red left child, no fix | (E\*, S, nil) |
| insert A | A goes left of E: E and A are red in a row, rotate right at S, flip colors at E | (A, E, S) |
| insert R | red left child of S | (A, E, (R\*, S, nil)) |
| insert C | C is a red right child of A: rotate left at A | ((A\*, C, nil), E, (R\*, S, nil)) |
| insert H | H goes left of R, so S has two red links in a row on its left: rotate right at S, flip colors at R; now R is a red right child of E: rotate left at E | (((A\*, C, nil), E\*, H), R, S) |
| insert X | red right child of S: rotate left at S | (((A\*, C, nil), E\*, H), R, (S\*, X, nil)) |
| insert M | red right child of H: rotate left at H | (((A\*, C, nil), E\*, (H\*, M, nil)), R, (S\*, X, nil)) |
| insert P | P goes right of M, which then has two red children: flip colors at M; M is a red right child of E: rotate left at E; M and E are two red links in a row below R: rotate right at R, flip colors at M | (((A\*, C, nil), E, H), M, (P, R, (S\*, X, nil))) |
| insert L | red right child of H: rotate left at H | (((A\*, C, nil), E, (H\*, L, nil)), M, (P, R, (S\*, X, nil))) |

The final tree is the 2-3 tree [M] ([E] ([A C], [H L]), [R] ([P], [S X])) in binary form. Its height is 4, and every path has three black nodes.

| operation | tree after |
|---|---|
| delete E | (((A\*, C, nil), H, L), M, (P, R, (S\*, X, nil))) |
| delete X | (((A\*, C, nil), H, L), M, (P, R, S)) |
| delete S | (((A\*, C, nil), H\*, L), M, (P\*, R, nil)) |

The deletion of E replaces it by its successor H, which was in a 3-node [H L]. The deletion of S moves red links down from the root, borrows and merges as in the 2-3 tree, and leaves the 2-3 tree [H M] ([A C], [L], [P R]).

## Correctness

Each step preserves (L1) and (L4): a rotation keeps the in-order sequence and gives the top node the color of the old top, and a color flip at a black node with two red children moves one black from the children to the node. After a recursive PUT returns, at most one rule fails at $h$: a red right link, two red left links in a row, or two red children. FIX-UP removes them in this order, and each fix can only make a later case true, never an earlier one. A flip can make $h$ red, which the parent repairs in its own FIX-UP. The full proof, with the 2-3 tree view of each case and the invariant of REMOVE, is in the proofs folder.

## Complexity

PUT and REMOVE visit each level once and do $O(1)$ work at each, and the height is at most $2 \lg(n + 1)$, so each operation takes $\Theta(\log n)$ time in the worst case. Unlike the classic red-black insertion, which does at most two rotations, an LLRB insertion can rotate at many levels, $O(\log n)$ in the worst case. In random tests with $10^5$ keys, one insertion made up to 12 rotations. The extra space is one bit for each node and $O(\log n)$ for the recursion stack.

## Variants

- **2-3-4 form.** Moving line L8, the color flip, to the start of PUT, before the recursive call, splits 4-nodes on the way down and gives an LLRB form of the [2-3-4 tree](/two-three-four-tree/). Sedgewick's paper gives both.
- **AA trees** use the mirror rule, with red links only on the right, and store a level number instead of a color. See [AA tree](/aa-tree/).
- **Classic red-black trees** allow red links on both sides. They need more cases, but fewer rotations. See [red-black tree](/red-black-tree/).

## When to use it

Use an LLRB tree when you want a balanced search tree with a short, recursive implementation, for teaching or for a program where clear code matters more than the last factor of speed. Library code usually prefers the classic red-black tree, which does fewer rotations and fewer writes on each update; persistent and functional code often prefers a red-black tree too.

## Pitfalls

- **The order of the three tests.** The tests at lines L6, L7 and L8 must come in this order. A rotation at line L6 can make the case of line L7 true, and a rotation at line L7 makes the case of line L8 true. A different order leaves a red right link or a 4-node.
- **Painting the root.** Line L10 paints the root black after each insertion. Without it, a flip at the root leaves it red and (L5) fails; the next insertion can then meet a red root with a red left child.
- **Deleting a key that is not there.** REMOVE assumes that $k$ is in the subtree: it moves red links down along the search path, and when $k$ is absent it reaches nil and reads a child of nil. Line L11 searches first. In the tree (1, 2, 3), REMOVE of 0 without this test fails at the leaf 1.
- **The root before a deletion.** Line L12 makes the root red when both of its children are black, so that REMOVE starts with its precondition: $h$ or $h.left$ is red.
- **Testing h.left.left on nil.** Line L7 reads $h.left.left$ only after it finds $h.left$ red, so $h.left$ is not nil there.

## Implementations

## History

Guibas and Sedgewick introduced red-black trees in 1978, as a binary form of 2-3 and 2-3-4 trees, and noted that the red links could be kept on one side. Arne Andersson used right-leaning links in the AA tree (1993). Sedgewick presented the left-leaning form in 2008, with the observation that insertion takes three lines of FIX-UP code, and made it the red-black BST of the fourth edition of Algorithms with Kevin Wayne (2011).

## References
