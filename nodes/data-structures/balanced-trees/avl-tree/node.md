---
tag: 195NAP
kind: data-structure
slug: avl-tree
name: AVL tree
aliases:
- Adelson-Velsky and Landis tree
area: data-structures/balanced-trees
level: core
summary: 'The first self-balancing BST: balance factors in {-1, 0, 1} are restored by single or double rotations after updates.'
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, height-balanced-tree, balance-factor, tree-rotation]
see_also: [avl-height-theorem, red-black-tree, wavl-tree, balanced-binary-search-tree, tree-rebalancing, order-statistic-tree]
sources:
  - paper: "G. M. Adelson-Velsky and E. M. Landis, An algorithm for the organization of information, Doklady Akademii Nauk SSSR 146 (1962); English translation in Soviet Mathematics Doklady 3 (1962)"
    locator: pages 263 to 266 of the Russian original (pages 1259 to 1263 of the translation)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (Algorithm A, balanced tree search and insertion, and Theorem A on the height)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, end-of-chapter problem on AVL trees
---

An AVL tree is a [binary search tree](/binary-search-tree/) in which, at every node, the heights of the two subtrees differ by at most one. Each node stores its height, or its [balance factor](/balance-factor/) in $\{-1, 0, +1\}$, and after an insertion or a deletion the tree repairs the nodes on the search path with single and double [rotations](/tree-rotation/). The rule keeps the height below $1.4405 \lg(n + 2)$, so search, insertion and deletion take $\Theta(\log n)$ time in the worst case. Adelson-Velsky and Landis published it in 1962, and it was the first [balanced binary search tree](/balanced-binary-search-tree/).

## In plain words

A search tree is fast when it is short. An AVL tree keeps it short with one local rule: at each node, the left side and the right side may differ in height by at most one level.

Each node remembers its height. When you insert or delete a key, you walk down to the place, change the tree there, and then walk back up the same path. On the way up, each node computes its height again. If a node finds that one side is now two levels taller than the other, it fixes itself with a rotation, which lifts the tall side up by one level. If the tall part is on the inside, two rotations are needed. The fix is local, so the whole update looks only at one path from the top to the bottom.

## The abstract type

An AVL tree implements the [ordered set](/ordered-set/): `contains(T, k)`, `insert(T, k)` and `delete(T, k)`, plus the order operations of a search tree (minimum, maximum, predecessor, successor and in-order iteration). With a value in each node it is an [ordered symbol table](/ordered-symbol-table/). The keys come from a total order, and the tree holds each key at most once.

## Representation

Each node $t$ has a key $t.key$, two children $t.left$ and $t.right$ (each a node or nil), and a height $t.h$. Write $h(\text{nil}) = 0$, so a single node has height 1: the height is the number of nodes on the longest path from the node down. The balance factor is

$$bf(t) = h(t.right) - h(t.left).$$

**Invariant.** (A1) The tree is a binary search tree: each key in $t.left$ is less than $t.key$, and each key in $t.right$ is greater. (A2) Each stored height is right: $t.h = 1 + \max(h(t.left), h(t.right))$. (A3) Each node has $bf(t) \in \{-1, 0, +1\}$.

Part (A3) makes the tree [height-balanced](/height-balanced-tree/). The page [AVL height bound](/avl-height-theorem/) proves that it gives $h < 1.4405 \lg(n + 2) - 0.3277$. Knuth stores only the balance factor, in two bits; this page stores the height, which makes the code shorter.

## Operations

The procedures are recursive and return the new root of the subtree they change. The caller stores it in place of the old root. A search is the search of a [binary search tree](/bst-search/) and changes nothing.

```pseudo id=main
INSERT(t, k)                               ▷ returns the new root of this subtree
L1  if t = nil then return a new node with key k and height 1
L2  if k < t.key then t.left ← INSERT(t.left, k)
L3  else if k > t.key then t.right ← INSERT(t.right, k)
L4  else return t                          ▷ k is already in the tree
L5  return REBALANCE(t)

REBALANCE(t)                               ▷ both subtrees of t are AVL, heights differ by ≤ 2
L6  t.h ← 1 + max(h(t.left), h(t.right))
L7  if bf(t) = 2 then                      ▷ the right side is too tall
L8      if bf(t.right) < 0 then t.right ← ROTATE-RIGHT(t.right)
L9      return ROTATE-LEFT(t)
L10 if bf(t) = −2 then                     ▷ the left side is too tall
L11     if bf(t.left) > 0 then t.left ← ROTATE-LEFT(t.left)
L12     return ROTATE-RIGHT(t)
L13 return t

DELETE(t, k)                               ▷ returns the new root of this subtree
L14 if t = nil then return nil
L15 if k < t.key then t.left ← DELETE(t.left, k)
L16 else if k > t.key then t.right ← DELETE(t.right, k)
L17 else                                   ▷ t holds k
L18     if t.left = nil then return t.right
L19     if t.right = nil then return t.left
L20     m ← the node with the least key in t.right
L21     t.key ← m.key, t.right ← DELETE(t.right, m.key)
L22 return REBALANCE(t)
```

```pseudo id=rotate
ROTATE-LEFT(x)                             ▷ x.right ≠ nil
L1  y ← x.right
L2  x.right ← y.left, y.left ← x
L3  x.h ← 1 + max(h(x.left), h(x.right))
L4  y.h ← 1 + max(h(y.left), h(y.right))
L5  return y
```

ROTATE-RIGHT is the mirror image. Each rotation recomputes the height of the node that moved down first, and then of the node that moved up.

**Insertion.** INSERT goes down as in a plain search tree and puts the new key in a new leaf. On the way back up, each node on the path calls REBALANCE. An insertion raises the height of a subtree by at most one, so a balance factor can reach $\pm 2$ but not more. There are four cases at a node $t$ with $bf(t) = 2$ and right child $r$, and their mirrors:

- $bf(r) = +1$ (right-right): the new key went into the outer subtree of $r$. One left rotation at $t$ fixes it (line L9).
- $bf(r) = -1$ (right-left): the new key went into the inner subtree. A right rotation at $r$ (line L8) and then a left rotation at $t$ (line L9) fix it. This is the *double rotation*.
- $bf(r) = 0$ cannot happen after an insertion. It can happen after a deletion, and then the single rotation of line L9 is right.

After an insertion, the first rotation brings the subtree back to the height it had before the insertion. So the nodes above it do not change their heights, and an insertion does at most one single or one double rotation. The code still calls REBALANCE up to the root, but each of these calls only recomputes a height.

**Deletion.** DELETE removes a node with at most one child directly (lines L18 and L19). A node with two children takes the key of its successor $m$, the least key of the right subtree, and the successor is deleted from the right subtree (lines L20 and L21). On the way back up, REBALANCE repairs each node. A deletion lowers the height of a subtree by at most one, so again a balance factor can reach only $\pm 2$. A rotation after a deletion can make the subtree one level shorter, and then the parent may need a rotation too. So a deletion can do one rotation (single or double) at each level of the path.

**Cost.** Each call does $O(1)$ work besides its recursive call, and the recursion follows one path. So each operation takes $O(h) = O(\log n)$ time.

## Example

Insert 10, 20, 30, 40, 50, 25 into an empty tree, then delete 40 and 50. A tree is written as (left, key, right), and a leaf as its key.

| operation | what REBALANCE does | tree after | height |
|---|---|---|---|
| insert 10 | nothing | 10 | 1 |
| insert 20 | nothing, $bf(10) = +1$ | (nil, 10, 20) | 2 |
| insert 30 | $bf(10) = 2$, $bf(20) = +1$: left rotation at 10 | (10, 20, 30) | 2 |
| insert 40 | nothing | (10, 20, (nil, 30, 40)) | 3 |
| insert 50 | $bf(30) = 2$, $bf(40) = +1$: left rotation at 30 | (10, 20, (30, 40, 50)) | 3 |
| insert 25 | $bf(20) = 2$, $bf(40) = -1$: right rotation at 40, left rotation at 20 | ((10, 20, 25), 30, (nil, 40, 50)) | 3 |
| delete 40 | 40 has no left child, 50 takes its place; $bf(30) = -1$ | ((10, 20, 25), 30, 50) | 3 |
| delete 50 | $bf(30) = -2$, $bf(20) = 0$: right rotation at 30 | (10, 20, (25, 30, nil)) | 3 |

The insertion of 25 is the double case: 25 goes into the inner subtree of 40, under 30. A single left rotation at 20 would leave the tree as tall as before. The double rotation lifts 30, the root of the inner subtree, to the top. The last deletion shows the case $bf = 0$ of the child, which only a deletion makes: one rotation suffices, and the height stays 3.

Inserting 1, 2, ..., 7 in order gives the perfect tree ((1, 2, 3), 4, (5, 6, 7)) of height 3, and inserting 1 to 1023 in order gives height 10, the least possible. A plain search tree would have height 1023.

## Correctness

Each operation keeps (A1), (A2) and (A3), and returns the right answer. The key fact is a lemma on REBALANCE: if both subtrees of $t$ satisfy the invariant, with heights that differ by at most 2, then REBALANCE$(t)$ returns a tree that satisfies the invariant, holds the same keys, and has height $\max(h(t.left), h(t.right))$ or one more. With it, induction on the path shows that INSERT and DELETE return an AVL tree that holds the old keys plus or minus $k$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the [comparison model](/comparison-model/) for the keys, with $O(1)$ time for each pointer change and each height update. Let $n$ be the number of keys.

| operation | worst case | rotations |
|---|---|---|
| contains, minimum, maximum, predecessor, successor | $\Theta(\log n)$ | 0 |
| insert | $\Theta(\log n)$ | at most 2 (one single or one double) |
| delete | $\Theta(\log n)$ | $O(\log n)$ |
| space | $\Theta(n)$ nodes, each with a height of $O(\log \log n)$ bits | |

**Upper bound.** By the [AVL height bound](/avl-height-theorem/), $h < 1.4405 \lg(n+2) - 0.3277$. Each operation does $O(1)$ work per level of one path, so it takes $O(\log n)$ time.

**Lower bound.** Each binary tree with $n$ nodes has height at least $\lceil \lg(n+1) \rceil$, so a search for a key at the deepest level takes $\Omega(\log n)$ comparisons. An insertion and a deletion also search first. So each bound of the table is $\Theta(\log n)$ in the worst case.

**Rotations.** The bound of one single or one double rotation per insertion is proved in the correctness proof. For deletion, a rotation can make the subtree shorter, so the parent may need a rotation too, and a deletion can do rotations at $\Theta(\log n)$ levels of the path in the worst case.

**Space.** A balance factor needs 2 bits. A height is at most $1.4405 \lg(n+2)$, so it fits in $O(\log \log n)$ bits, one byte for any real $n$.

## Variants

- **Balance factors only.** Knuth's Algorithm A stores $bf$ in two bits. On the way down it remembers the last node of the path with a nonzero balance factor, which is the only node where a rotation can be needed, so it needs no stack. The rules are the same.
- **Top-down or bottom-up with parent pointers.** An iterative version walks back up with parent pointers and stops at the first node whose height does not change.
- **[WAVL trees](/wavl-tree/).** Rank-balanced trees of Haeupler, Sen and Tarjan behave as AVL trees when there are no deletions, but do at most two rotations per deletion, and their height never gets worse than that of a red-black tree.
- **Relaxed AVL trees.** Allowing a height difference up to a constant $\Delta > 1$ gives HB[$\Delta$] trees, with fewer rotations and a larger height bound; see [height-balanced tree](/height-balanced-tree/).
- **Augmented AVL trees.** A size field gives an [order-statistic tree](/order-statistic-tree/); the field is recomputed after each rotation, as the height is.

## When to use it

Use an AVL tree when searches are much more common than updates. Its height is at most about $1.44 \lg n$, against $2 \lg n$ for a [red-black tree](/red-black-tree/), so searches look at fewer nodes in the worst case. A red-black tree does at most three rotations per deletion, and an AVL tree may do one per level, so the red-black tree is the usual choice of libraries with frequent updates. For keys on disk, use a [B-tree](/b-tree/). For a simple program with expected bounds, a [treap](/treap/) is shorter to write.

## Pitfalls

- **Testing the wrong child in the double case.** Line L8 must test $bf(t.right) < 0$, not $bf(t.right) \le 0$. With $\le 0$, a deletion that leaves $bf(t.right) = 0$ does a double rotation, and the result can have $bf = \pm 2$. Insert 1, 7, 2, 6, 3, 5, 8, 4 and delete 1: the root 3 gets $bf = 2$ with $bf(6) = 0$. The right single rotation gives ((2, 3, (4, 5, nil)), 6, (nil, 7, 8)). The wrong double rotation lifts 5 and leaves 6 with $bf = +2$. A test of the implementation checks this case.
- **Updating heights in the wrong order.** In ROTATE-LEFT, line L3 must update $x$ before line L4 updates $y$, because $x$ is now a child of $y$. The other order leaves a wrong height at $y$, and the next rebalance takes a wrong decision.
- **Forgetting to rebalance after a deletion of the successor.** Line L21 deletes $m$ from $t.right$ with a recursive DELETE, so that the path from $t$ down to $m$ is rebalanced too. Unlinking $m$ by hand skips these nodes.
- **Height of nil.** Code that reads $t.left.h$ without a check for nil fails at the leaves. Use a function $h(\cdot)$ with $h(\text{nil}) = 0$.

## Implementations

## History

Georgy Adelson-Velsky and Evgenii Landis described the tree in 1962, in the Doklady of the Soviet Academy of Sciences, as a way to organize information for fast search and insertion. Knuth gives the insertion algorithm with balance factors and the height bound as Theorem A in Section 6.2.3. Deletion with $O(\log n)$ rotations is also discussed there. Later schemes, the red-black tree of Guibas and Sedgewick (1978) and the WAVL tree of Haeupler, Sen and Tarjan (2015), relax the AVL rule to reduce the number of rotations.

## References
