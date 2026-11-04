---
tag: 9VPK2S
kind: data-structure
slug: wavl-tree
name: WAVL tree
aliases:
- weak AVL tree
- rank-balanced tree
area: data-structures/balanced-trees
level: research
summary: A rank-based balanced tree that relaxes AVL rules, giving worst-case O(1) rotations per update and height bounds close to AVL.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [avl-tree, tree-rotation, red-black-tree, balance-factor]
see_also: [avl-tree, red-black-tree, tree-rebalancing, avl-height-theorem, red-black-height-theorem, aa-tree, height-balanced-tree, black-height]
sources:
  - paper: doi:10.1145/2689412
    title: Bernhard Haeupler, Siddhartha Sen and Robert E. Tarjan, Rank-balanced trees, ACM Transactions on Algorithms 11(4), 2015
    locator: Sections 2 to 4, the rank rule, bottom-up insertion and deletion, the height bounds, and the amortized number of rank changes
  - paper: Bernhard Haeupler, Siddhartha Sen and Robert E. Tarjan, Rank-balanced trees, Workshop on Algorithms and Data Structures (WADS), Lecture Notes in Computer Science 5664, 2009
    locator: pages 351 to 362, the first version of the weak AVL rule
---

A WAVL tree, or *weak AVL tree*, is a [balanced binary search tree](/balanced-binary-search-tree/) in which each node stores an integer *rank*, and the *rank difference* of a child, its parent's rank minus its own, must be 1 or 2, with nil at rank $-1$ and every leaf at rank 0. In an [AVL tree](/avl-tree/), the rank would be the height and a node could not have two children of difference 2; the WAVL rule allows such 2,2 nodes. This small change makes deletion as easy as insertion: each insertion or deletion does at most two rotations, in the worst case, like a [red-black tree](/red-black-tree/), and the number of rank changes is $O(1)$ amortized. If no deletions are done, a WAVL tree is exactly an AVL tree, with height at most $1.44 \lg n$; with deletions, the height is at most $2 \lg n$, the bound of red-black trees. Bernhard Haeupler, Siddhartha Sen and Robert Tarjan introduced the trees in 2009.

## In plain words

In an AVL tree, each node knows its height, and the two sides of a node may differ by at most one. After a deletion, a height can shrink, and fixing it can need a rotation at many levels of the tree.

A WAVL tree stores a rank in place of the height and is less strict about it. A rank is like a height that is allowed to stay too high for a while. Each child must be one or two steps below its parent, and leaves are at the bottom step. Insertions fix the ranks exactly like AVL trees do. Deletions mostly just lower ranks, and they stop with at most two rotations. Because ranks may stay high after deletions, the tree can get a little deeper than an AVL tree, but never deeper than a red-black tree.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on keys from a totally ordered universe, and the keys in increasing order. INSERT returns false when the key is present, and DELETE returns false when it is absent.

## Representation

A node holds a key, two children, a parent pointer and a rank $r$. Write $r(\text{nil}) = -1$ and, for a child $x$ of $p$, $\delta(x) = r(p) - r(x)$. A node whose children have differences $i$ and $j$ is an $i,j$ node. The rules are:

1. (W1) The tree is a binary search tree.
2. (W2) Every rank difference is 1 or 2.
3. (W3) Every leaf has rank 0.

So a leaf is a 1,1 node, a node with one child is a 1,2 node of rank 1, and a 2,2 node must have two children. Only the rank difference matters, so a node can store just one bit per child, or one bit for its own difference, instead of the whole rank. To *promote* a node is to add one to its rank, and to *demote* it is to subtract one.

The rank rule is the AVL rule with 2,2 nodes allowed: in an AVL tree, a node's children have height differences 1,1 or 1,2. It is also stricter than the red-black rule: a red-black tree is a tree with rank differences 0 or 1 under each node, read in another way, and every WAVL tree can be colored as a red-black tree.

## Operations

CONTAINS is the search of a binary search tree. Both updates start as in a binary search tree and then walk up from the changed place. Below, $p$ is the parent of $x$, $s$ is the sibling of $x$, and the mirror cases, with left and right exchanged, are not written.

```pseudo id=main
INSERT(k)
L1  add a leaf x with key k and rank 0 as in a binary search tree; if the tree was empty, return
L2  while x is not the root and δ(x) = 0:                       ▷ p is a 0,1 or a 0,2 node
L3      if δ(s) = 1 then PROMOTE(p); x ← p; continue
        let x be the left child of p; y ← x.right               ▷ the inner child
L4      if δ(y) = 2 then ROTATE(x) above p; DEMOTE(p)          ▷ single rotation
L5      else ROTATE(y) twice, above x and above p; PROMOTE(y); DEMOTE(x); DEMOTE(p)
L6      stop

DELETE(k)
L7  delete k as in a binary search tree; x ← the child (or nil) that takes the place of the removed node; p ← its parent
L8  if p is a leaf of rank 1 then DEMOTE(p); x ← p
L9  while x is not the root and δ(x) = 3:
        let x be the left child of p; y ← p.right               ▷ δ(y) is 1 or 2
L10     if δ(y) = 2 then DEMOTE(p); x ← p; continue
L11     if y is a 2,2 node then DEMOTE(p); DEMOTE(y); x ← p; continue
        z ← y.right; v ← y.left                                 ▷ outer and inner child
L12     if δ(z) = 1 then ROTATE(y) above p; PROMOTE(y); DEMOTE(p); if p is a leaf then DEMOTE(p)
L13     else ROTATE(v) twice, above y and above p; v.rank += 2; DEMOTE(y); p.rank −= 2
L14     stop
```

INSERT is exactly AVL insertion, written with ranks: a 0,1 parent is promoted and the problem moves up, and a 0,2 parent is fixed by a single or double rotation, after which the loop stops. DELETE moves a difference of 3 up the tree by demotions (lines L10 and L11), and fixes it at once with a single or double rotation when the sibling has difference 1 and is not 2,2.

## Example

Insert 1 to 7 in increasing order. A node is written key:rank, and a tree (left, node, right).

| insert | what happens | tree |
|---|---|---|
| 1, 2 | 2 is a leaf under 1, which is promoted to rank 1 | (nil, 1:1, 2:0) |
| 3 | 2 is promoted to rank 1; then 1 is a 0,2 node, and the inner child of 2 is nil, of difference 2: a single rotation and a demotion of 1 | (1:0, 2:1, 3:0) |
| 4 | 3 is promoted, and then 2 is promoted to rank 2 | (1:0, 2:2, (nil, 3:1, 4:0)) |
| 5, 6, 7 | the same steps on the right; inserting 6 also rotates at the root, and 4 becomes the root | ((1:0, 2:1, 3:0), 4:2, (5:0, 6:1, 7:0)) |

With insertions only, each rank is the height, as in an AVL tree.

Now take the tree after inserting 1 to 4, (1:0, 2:2, (nil, 3:1, 4:0)), and delete 1. The leaf goes, and the nil left child of 2 has difference $2 - (-1) = 3$. The sibling 3 has difference 1 and is a 2,1 node, not 2,2, and its outer child 4 has difference 1, so line L12 rotates 3 above 2, promotes 3 to rank 2 and demotes 2 to rank 1; then 2 is a leaf, so it is demoted again to 0. The result is (2:0, 3:2, 4:0). Here 3 is a 2,2 node: its rank is 2 but its height is 1. An AVL tree would store height 1 there; the WAVL tree keeps the higher rank, which is allowed, and saved work.

## Correctness

The proof checks each case of the two loops, as in the AVL proof. During insertion, the only possible violation is a difference of 0 at $x$; a promotion moves it up, and a rotation removes it while giving the new top of the subtree the old rank of $p$, so nothing changes above. During deletion, the only possible violation is a difference of 3 at $x$, or a leaf of rank 1, which line L8 turns into the first case. A demotion of $p$ alone (sibling of difference 2), or of $p$ and a 2,2 sibling, moves the 3 up. Otherwise a single or double rotation, with the rank changes listed, gives a subtree whose root has the old rank of $p$ and whose nodes all satisfy (W2) and (W3). The full case analysis is in the proofs folder.

## Complexity

**Height.** The height of a node is at most its rank. A node of rank $k$ has two children of rank at least $k - 2$, so a subtree of rank $k$ has at least $2^{k/2 + 1} - 1$ nodes, and the height is at most $2 \lg(n + 1) - 2$. If no deletions have been done, the tree is an AVL tree, with height at most $\log_\varphi n \approx 1.44 \lg n$. In general Haeupler, Sen and Tarjan show the height is at most $\log_\varphi m$, where $m$ is the number of insertions done, so it depends on the history and not only on the current size; the bound $2 \lg n$ holds always.

**Time.** Each update walks one path down and at most one path up, with $O(1)$ work per node, so it takes $\Theta(\log n)$ time in the worst case. Each update does at most two rotations. The number of promotions and demotions is $O(\log n)$ in the worst case and $O(1)$ amortized over any sequence of insertions and deletions from the empty tree. Haeupler, Sen and Tarjan also show that rebalancing at a node of height $h$ happens with a frequency that decreases exponentially in $h$, which matters for trees where a change near the root is costly.

**Space.** One rank, or two bits for the rank differences, per node; $\Theta(n)$ in all.

| tree | rotations per insertion | rotations per deletion | height |
|---|---|---|---|
| [AVL tree](/avl-tree/) | at most 2 | $O(\log n)$ | $1.44 \lg n$ |
| [red-black tree](/red-black-tree/) | at most 2 | at most 3 | $2 \lg n$ |
| WAVL tree | at most 2 | at most 2 | $\min(1.44 \lg m, 2 \lg n)$ |

## Variants

- **AVL trees.** Forbidding 2,2 nodes gives AVL trees. Deletion must then repair 2,2 nodes as they appear, which can need rotations all the way up.
- **Red-black trees as rank trees.** Allowing rank differences 0 and 1, with no two 0s in a row, describes [red-black trees](/red-black-tree/), where a child of difference 0 is red. In this view, WAVL trees sit between AVL and red-black trees.
- **Relaxed AVL trees.** Sen and Tarjan studied trees that do no rebalancing at all on deletion, with ranks only lowered lazily. Their height is logarithmic in the number of insertions, which is enough when deletions are rare or rebuilding is done from time to time.
- **Top-down versions.** Haeupler, Sen and Tarjan give top-down insertion and deletion for rank-balanced trees, which suit concurrent use.
- **Rank bits.** Storing only the rank-difference bits, one per child, makes a node as small as in a red-black tree.

## When to use it

Use a WAVL tree when you want the shallow trees of AVL for insert-heavy loads and the constant number of rotations of red-black trees for deletions, with one simple rank rule and no colors. It is a good choice for library maps and sets and for kernel data structures, where the cost of restructuring matters. If the data structure must be persistent or concurrent, its $O(1)$ amortized rank changes reduce the number of nodes written.

## Pitfalls

- **Forgetting the 2,2 leaf.** After deleting a leaf, its parent may become a leaf of rank 1, which breaks (W3) without any difference of 3. Line L8 must demote it first.
- **Nil has rank $-1$.** With nil at rank 0, leaves would need rank 1 and the case tests would be off by one.
- **The double demotion in the single rotation.** After the rotation of line L12, $p$ may be a leaf; then it must be demoted twice in total, once by the rotation case and once more, or it is a leaf of rank 1.
- **Moving the wrong way on a 2,2 sibling.** When the sibling $y$ has difference 1 and is 2,2, the right step is to demote both $p$ and $y$ and go on upward, not to rotate. Rotating there gives a node with difference 3.
- **Using the rank as a height.** After deletions the rank can exceed the height, so code that needs the height, such as a height-based join, must not read the rank as the height.

## Implementations

## History

Bernhard Haeupler, Siddhartha Sen and Robert Tarjan presented rank-balanced trees at WADS 2009, and the journal version appeared in ACM Transactions on Algorithms in 2015. Their goal was a tree with the height of AVL trees under insertions and the cheap deletions of red-black trees, and the rank view also gave a single framework for AVL, red-black and other trees. Sen and Tarjan had earlier studied deletion without rebalancing, which led to the relaxed rule. The FreeBSD kernel's tree macros moved from red-black trees to rank-balanced trees in 2020.

## References
