---
tag: TPBFGF
kind: data-structure
slug: aa-tree
name: AA tree
aliases:
- AA-tree
area: data-structures/balanced-trees
level: advanced
summary: A simpler red-black variant where only right-leaning red links are allowed, using a level field instead of colours.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, tree-rotation, two-three-tree, red-black-tree]
see_also: [left-leaning-red-black-tree, red-black-correspondence-with-2-3-4-trees, black-height, wavl-tree, avl-tree, red-black-height-theorem]
sources:
  - paper: doi:10.1007/3-540-57155-8_236
    title: Arne Andersson, Balanced search trees made simple, Workshop on Algorithms and Data Structures (WADS), 1993
    locator: pages 60 to 71, the level rules, skew, split, insertion and deletion
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (red-black BSTs that model 2-3 trees, for comparison)
  - paper: doi:10.1007/BF00289509
    title: Rudolf Bayer, Symmetric binary B-trees, data structure and maintenance algorithms, Acta Informatica 1(4), 1972
    locator: horizontal and vertical pointers, the model of the level rules
---

An AA tree is a [balanced binary search tree](/balanced-binary-search-tree/) in which each node stores a small integer, its *level*, instead of a color. A child may be at the same level as its parent only if it is a right child, and two such *horizontal* links may not follow each other. In red-black terms, a horizontal link is a red link, and only right links may be red, which makes the AA tree the right-leaning mirror of the [left-leaning red-black tree](/left-leaning-red-black-tree/) and a binary form of the [2-3 tree](/two-three-tree/). Two short rotations repair everything: SKEW removes a horizontal left link, and SPLIT removes two horizontal right links in a row by lifting the middle node. The height is at most $2 \lg(n + 1)$, so search, insertion and deletion take $\Theta(\log n)$ time. Arne Andersson gave the tree in 1993 as a red-black tree with far fewer cases.

## In plain words

Picture the tree drawn in floors. Each node lives on a floor, the leaves on the ground floor. A node's left child is always one floor down. Its right child is one floor down or on the same floor, and then the two sit side by side like one wide node with two keys.

A new key always arrives on the ground floor. If it lands to the left of a node on the same floor, the two swap roles, which is one rotation. If three nodes now sit side by side, the middle one moves up a floor, which is another rotation. The same two moves, applied a few times on the way up, also clean up after a deletion. Every node of floor $\ell$ has at least $2^\ell - 1$ nodes below and including it, so the floors stay few.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on keys from a totally ordered universe, and the keys in increasing order. Insert returns false when the key is present, and delete returns false when it is absent.

## Representation

A node holds a key, a left and a right child, and its level $\ell$, a positive integer. Write $\ell(\text{nil}) = 0$. The rules are:

1. (A1) Each leaf has level 1.
2. (A2) A left child is exactly one level below its parent: $\ell(t.left) = \ell(t) - 1$.
3. (A3) A right child is at the same level as its parent or one below: $\ell(t.right) \in \{\ell(t), \ell(t) - 1\}$.
4. (A4) A right grandchild is below its grandparent: $\ell(t.right.right) < \ell(t)$.
5. (A5) Each node above level 1 has two children.

(A1) and (A5) follow from the other three, with $\ell(\text{nil}) = 0$. A link to a child of the same level is *horizontal*; by (A2) and (A4), horizontal links point right and never come two in a row. A node with a horizontal right link is a 3-node of a 2-3 tree; other nodes are 2-nodes. The level of a node is the [black-height](/black-height/) of the same node in the red-black reading, plus one.

## Operations

CONTAINS is the search of a binary search tree; it never reads levels. INSERT and DELETE below take a present-key or absent-key precondition, and the class methods search first.

```pseudo id=main
SKEW(t)                                    ▷ remove a horizontal left link
L1  if t ≠ nil and t.left ≠ nil and t.left.level = t.level then
L2      l ← t.left; t.left ← l.right; l.right ← t; return l
    return t

SPLIT(t)                                   ▷ remove two horizontal right links in a row
L3  if t ≠ nil and t.right ≠ nil and t.right.right ≠ nil and t.right.right.level = t.level then
L4      r ← t.right; t.right ← r.left; r.left ← t
L5      r.level ← r.level + 1; return r
    return t

INSERT(t, k)                               ▷ k is not in the subtree of t
L6  if t = nil then return a new node with key k and level 1
L7  if k < t.key then t.left ← INSERT(t.left, k) else t.right ← INSERT(t.right, k)
L8  t ← SKEW(t); t ← SPLIT(t); return t

DELETE(t, k)                               ▷ k is in the subtree of t
L9  if k < t.key then t.left ← DELETE(t.left, k) else if k > t.key then t.right ← DELETE(t.right, k)
L10 else if t is a leaf then return nil
L11 else if t.left = nil then s ← the least key of t.right; t.key ← s; t.right ← DELETE(t.right, s)
L12 else p ← the largest key of t.left; t.key ← p; t.left ← DELETE(t.left, p)
L13 DECREASE-LEVEL(t)
L14 t ← SKEW(t); t.right ← SKEW(t.right); if t.right ≠ nil then t.right.right ← SKEW(t.right.right)
L15 t ← SPLIT(t); t.right ← SPLIT(t.right); return t

DECREASE-LEVEL(t)
L16 should ← min(level(t.left), level(t.right)) + 1
L17 if should < t.level then t.level ← should; if level(t.right) > should then t.right.level ← should
```

SKEW is a right rotation and SPLIT a left rotation with a level increase; they are the only steps that change pointers. After an insertion, a subtree can come back one level higher, with a horizontal link at its root: line L8 turns a horizontal left link into a right one and splits a run of three nodes on one level. After a deletion, a subtree can come back one level lower; line L17 lowers $t$ (and its horizontal right child) to match, and the three SKEWs and two SPLITs of lines L14 and L15 put the at most five nodes now on that level in the right shape.

## Example

Insert 1 to 7 in increasing order. A node is written key:level.

| step | what happens | tree |
|---|---|---|
| 1 | a leaf | 1:1 |
| 2 | 2 becomes the horizontal right child of 1 | (nil, 1:1, 2:1) |
| 3 | at 1, three nodes on level 1: SPLIT lifts 2 | (1:1, 2:2, 3:1) |
| 4 | 4 is the horizontal right child of 3 | (1:1, 2:2, (nil, 3:1, 4:1)) |
| 5 | at 3, SPLIT lifts 4 to level 2, a horizontal right child of 2 | (1:1, 2:2, (3:1, 4:2, 5:1)) |
| 6 | 6 is the horizontal right child of 5 | (1:1, 2:2, (3:1, 4:2, (nil, 5:1, 6:1))) |
| 7 | at 5, SPLIT lifts 6 to level 2; at 2, the nodes 2, 4, 6 are on level 2, and SPLIT lifts 4 to level 3 | ((1:1, 2:2, 3:1), 4:3, (5:1, 6:2, 7:1)) |

Sorted input gives the perfect tree here. No SKEW was needed, because each new key went to the right.

Now delete 1. The leaf is removed, and at 2, DECREASE-LEVEL finds children of levels 0 and 1, so 2 drops to level 1 and 3 becomes its horizontal right child. At 4, the children now have levels 1 and 2, so 4 drops to level 2, and 6 is its horizontal right child. No SKEW or SPLIT applies. The tree is ((nil, 2:1, 3:1), 4:2, (5:1, 6:2, 7:1)).

Then delete 4. It has a left child, so its key is replaced by the predecessor 3, which is removed from the leaf. The levels stay, and the tree is (2:1, 3:2, (5:1, 6:2, 7:1)).

## Correctness

The rules are local, so the proof is a case analysis at the node where the recursion returns. For insertion: a recursive call returns a valid subtree at the same level, or one level higher with both children one level below it; in the second case, at most one SKEW and one SPLIT at the parent restore the rules, and the parent can itself come back one level higher only if it already had a horizontal right child. For deletion: a recursive call returns a valid subtree at the same level or one level lower; when lower, DECREASE-LEVEL lowers the parent and its horizontal right child, after which the nodes on the parent's level form a run of at most five nodes along the right spine, some with horizontal left links. The three SKEWs remove the left links, and the two SPLITs break the run, so the subtree comes back valid at the old level or one lower. The full proof, with every case, is in the proofs folder.

## Complexity

A node of level $\ell$ has at least $2^\ell - 1$ nodes in its subtree, since both its children have level at least $\ell - 1$. On a downward path, a left step lowers the level by one, and of two right steps in a row at least one lowers it. So a tree with $n$ nodes and root level $L$ has height at most $2L \le 2 \lg(n + 1)$. Search, insertion and deletion follow one path and do $O(1)$ work per node, so they take $\Theta(\log n)$ time in the worst case. The recursion uses $O(\log n)$ stack space, and the tree uses $\Theta(n)$ space; a level fits in $O(\log \log n)$ bits, though it is usually a full byte or word.

The number of rotations is $O(\log n)$ in the worst case per update, more than in the classic [red-black tree](/red-black-tree/), because each node on the path calls SKEW and SPLIT, even if most of them do nothing.

## Variants

- **Left-leaning red-black trees.** Sedgewick's [left-leaning red-black tree](/left-leaning-red-black-tree/) is the mirror image: horizontal (red) links lean left. It stores a color, not a level, so it needs color flips where the AA tree changes a level.
- **Colors instead of levels.** An AA tree can also store one bit per node, whether the link from its parent is horizontal. The level is then the number of non-horizontal links on a path down to nil, but DECREASE-LEVEL must then compare the levels of children by walking down, so the integer level is the usual choice.
- **2-3-4 form.** Allowing a horizontal left link next to a horizontal right link gives a binary form of 2-3-4 trees, the [red-black tree](/red-black-tree/) of Guibas and Sedgewick; this needs more cases.
- **Rank-balanced trees.** [WAVL trees](/wavl-tree/) also store an integer per node, a rank, with rank differences of 1 or 2; the AA level rules are a stricter form of rank rule.

## When to use it

Use an AA tree when you want a balanced search tree with worst-case $O(\log n)$ operations and the least code: the whole tree is two rotations and two recursive procedures, and the deletion has no case table. It is a good choice for teaching and for small embedded code. For heavy write loads, a classic red-black tree does fewer rotations; for read-heavy loads, an [AVL tree](/avl-tree/) is a little shallower.

## Pitfalls

- **Only two SKEWs in the deletion.** Line L14 must skew $t$, $t.right$ and $t.right.right$. Insert 18, 15, 19, 7, 3, 13 and delete 7. The key 7 is replaced by its predecessor 3, and the root and its right child 18 drop to level 1, so the nodes 3, 13, 15, 18, 19 are all on level 1. The second SKEW rotates 13 above 18, which gives 18 the new horizontal left child 15; only the third SKEW removes that link. Without it, the tree breaks rule (A2). A test checks this case.
- **Forgetting the right child in DECREASE-LEVEL.** When $t$ drops a level, a horizontal right child must drop with it, or it would be one level above its parent.
- **SPLIT on a short spine.** SPLIT reads $t.right.right$; the test must check $t.right \ne \text{nil}$ first.
- **The level of nil.** All tests compare levels, and nil must count as level 0. With nil at level 1, a leaf would look like a node with horizontal children.
- **Deleting a node with only a right child.** Such a node is at level 1 and its right child is a leaf at level 1. Line L11 copies the successor key into the node and deletes the leaf, so the fix-up code of lines L13 to L15 runs in the same way as in the other cases.

## Implementations

## History

Rudolf Bayer's symmetric binary B-trees (1972) had horizontal and vertical pointers, which Guibas and Sedgewick (1978) recolored as red and black. Arne Andersson, in "Balanced search trees made simple" (WADS 1993), allowed horizontal links only on the right, replaced the colors by levels, and reduced the maintenance to SKEW and SPLIT. The name AA comes from his initials. Mark Allen Weiss's textbooks spread the tree, and Sedgewick's 2008 left-leaning red-black tree applies the same idea in mirror image.

## References
