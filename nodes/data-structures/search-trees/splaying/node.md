---
tag: AA2JCV
kind: algorithm
slug: splaying
name: Splaying
aliases:
- splay operation
- bottom-up splaying
area: data-structures/search-trees
level: advanced
summary: Move an accessed node to the root through a sequence of zig, zig-zig and zig-zag rotations.
model: pointer-machine
complexity:
  vars: {n: the number of nodes, d: the depth of the splayed node}
  time: {worst: Θ(d), amortized: O(log n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: false, recursive: false, in_place: true}
prereqs: [binary-search-tree, tree-rotation, potential-method]
see_also: [splay-tree, static-optimality-theorem, working-set-theorem, dynamic-optimality-conjecture, link-cut-tree, move-to-front, amortized-cost, tango-tree]
sources:
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: Section 2 (Splaying and its analysis), the three cases zig, zig-zig and zig-zag, and Lemma 1 (the Access Lemma); Section 4 for top-down splaying and semi-splaying
---

Splaying is the restructuring step of the [splay tree](/splay-tree/): it moves a node $x$ of a [binary search tree](/binary-search-tree/) to the root by [rotations](/tree-rotation/), taken in pairs from the bottom of the path. If $x$ and its parent are both left children (or both right children), the parent is rotated first and then $x$ (zig-zig); if they are on different sides, $x$ is rotated twice (zig-zag); a single rotation (zig) is used only when the parent is the root. Sleator and Tarjan (1985) showed that this pairing makes the amortized cost $O(\log n)$, measured with the potential $\sum_x \lg s(x)$; plain rotate-to-root, which uses single rotations only, can cost $\Theta(n)$ per access forever.

## In plain words

You have just found a key deep in a tree, and you expect to need it again soon, so you want to bring it to the top. Rotating it up one level at a time does this, but it leaves the rest of the path as long as it was.

Splaying moves the key up two levels at a time, and the choice of how to do each double step depends on the shape: if the path goes in a straight line, first turn the upper link, then the lower one; if the path bends, turn the lower link twice. The straight-line rule is the trick. It folds the path in half, so the other keys on it also end up closer to the top, and the tree gets better as you use it.

## The problem

The input is a binary search tree with parent pointers and a node $x$ of it. The output is a binary search tree on the same keys, with the same in-order sequence, whose root is $x$. The goal is a low amortized cost over a sequence of splays: each splay may be slow, but the total over many is small.

## The algorithm

```pseudo id=main
SPLAY(T, x)
L1  while x.p ≠ NIL do
L2      y ← x.p; z ← y.p
L3      if z = NIL then ROTATE(x)                                  ▷ zig
L4      elseif (x = y.left) = (y = z.left) then ROTATE(y); ROTATE(x)  ▷ zig-zig
L5      else ROTATE(x); ROTATE(x)                                  ▷ zig-zag
L6  T.root ← x

ROTATE(x)                                ▷ move x above its parent y
L7  y ← x.p; z ← y.p
L8  if x = y.left then y.left ← x.right; if x.right ≠ NIL then x.right.p ← y; x.right ← y
L9  else y.right ← x.left; if x.left ≠ NIL then x.left.p ← y; x.left ← y
L10 y.p ← x; x.p ← z
L11 if z ≠ NIL then (if z.left = y then z.left ← x else z.right ← x)
```

Each round of the loop of line L1 does one of three steps.

- **Zig** (line L3). The parent $y$ is the root. One rotation makes $x$ the root.
- **Zig-zig** (line L4). $x$ and $y$ are children on the same side. Rotate $y$ over $z$, then $x$ over $y$. The path $z, y, x$ turns into $x, y, z$.
- **Zig-zag** (line L5). $x$ and $y$ are on different sides. Rotate $x$ over $y$, then over $z$. Then $x$ has $y$ and $z$ as its two children.

ROTATE is the standard [tree rotation](/tree-rotation/) with parent pointers. It keeps the in-order sequence.

## Example

**A chain.** Insert 7, 6, 5, 4, 3, 2, 1 into an empty BST with no splaying. The result is a chain to the left, with 1 at depth 6. Splay 1:

| step | case | path before the step (from the top) | after the step |
|---|---|---|---|
| 1 | zig-zig at 1, 2, 3 | 7, 6, 5, 4, 3, 2, 1 | 1 replaces 3, with 2 then 3 below it on the right |
| 2 | zig-zig at 1, 4, 5 | 7, 6, 5, 4, 1 | 1 replaces 5, with 4 then 5 below it |
| 3 | zig-zig at 1, 6, 7 | 7, 6, 1 | 1 is the root, with 6 then 7 below it |

The final tree is

```
    1
     \
      6
     / \
    4   7
   / \
  2   5
   \
    3
```

The splay made 6 rotations, one per level. The height dropped from 6 to 4, and the depths of 2, 3, 4, 5 and 6 changed from 5, 4, 3, 2, 1 to 3, 4, 2, 3, 1. A second rotate-to-root with single rotations would instead leave the chain $1, 7, 6, 5, 4, 3, 2$, still of height 6.

**A zig-zag.** In the tree with root 50, children 30 and 70, 20 and 40 below 30, and 35 and 45 below 40, splay 40. Here 40 is a right child and 30 a left child, so line L5 rotates 40 twice. The result has root 40, left child 30 with children 20 and 35, and right child 50 with children 45 and 70: a perfect tree of height 2.

## Correctness

Each rotation keeps the in-order sequence and the BST property, and keeps the parent pointers consistent (lines L8 to L11 change exactly the links between $x$, $y$, the middle subtree and $z$). Each round of the loop moves $x$ up by one level (zig) or two levels (zig-zig and zig-zag), and the depth of $x$ does not increase otherwise, so after $\lceil d/2 \rceil$ rounds $x$ has no parent and is the root. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Actual cost.** Each round costs $O(1)$, and the number of rotations is exactly $d$, the depth of $x$. So one splay takes $\Theta(d + 1)$ time, which is $\Theta(n)$ on a chain.

**Amortized cost (Access Lemma).** Give each node $i$ a weight $w(i) > 0$, let $s(x)$ be the sum of the weights in the subtree of $x$, and $r(x) = \lg s(x)$ its rank. With the potential $\Phi = \sum_x r(x)$ and the cost of a splay counted as the number of rotations (at least 1), the [amortized cost](/amortized-cost/) of splaying $x$ in a tree with root $t$ is at most
$$3\,(r(t) - r(x)) + 1 = O\!\left(\log \frac{s(t)}{s(x)}\right).$$
With all weights 1 this is $3 \lg n + 1$. The proof checks each of the three steps: a zig-zig or zig-zag step has amortized cost at most $3(r'(x) - r(x))$, a zig step at most $3(r'(x) - r(x)) + 1$, and the sum telescopes. The key inequality is $\lg a + \lg b \le 2 \lg(a + b) - 2$. The full proof is in [the complexity proof](proofs/complexity.md).

Different weights give the theorems of the splay tree: uniform weights give the balance theorem, access frequencies give the [static optimality theorem](/static-optimality-theorem/), and weights by recency give the [working set theorem](/working-set-theorem/). The algorithm is the same; only the analysis changes.

**Space.** $O(1)$ extra: the loop needs only $x$, $y$ and $z$.

## Properties

- **Halves the depth of the path.** Splaying roughly halves the depth of each node on the access path (Sleator and Tarjan), as in the chain example, while nodes off the path go down by at most 2 levels.
- **Order of the rotations.** The zig-zig rotates the parent first. Rotating $x$ twice in that case gives rotate-to-root, which has no good amortized bound.
- **No balance data.** The tree stores no heights, colours or sizes; the rotations are the same whatever the history.
- **Pointer machine.** Only pointer changes and no comparisons of keys: the search that finds $x$ is separate.
- **Changes the tree on reads.** Each access writes to the tree, which is a cost for caches and for concurrent readers.

## Variants and improvements

- **Top-down splaying.** Sleator and Tarjan also give a top-down form that splays while searching, keeping a left tree and a right tree of the nodes passed, and joins them at the end. It needs no parent pointers and no second pass, and is the form most often coded.
- **Semi-splaying.** In the zig-zig case rotate only the parent and continue from it. It does fewer rotations and keeps an $O(\log n)$ amortized bound with a larger constant.
- **Splay at a key.** If the key is absent, splay the last node of the search path. Then the root is the floor or the ceiling of the key, which split and insert use.
- **Splaying in other structures.** [Link-cut trees](/link-cut-tree/) splay inside each preferred path.
- **The list analogue.** For lists, [move-to-front](/move-to-front/) plays the role of splaying.

## When to use it

Use splaying as the restructuring step of a [splay tree](/splay-tree/), or of any structure that should adapt to the access pattern: recently or often used keys move near the root. It also gives cheap split and join, since a splay brings the split point to the root. Avoid it when the tree is read by many threads at once, or when each single access needs a worst-case bound.

## Pitfalls

- **Rotate-to-root instead of zig-zig.** Using two single rotations of $x$ in the zig-zig case is a different algorithm. On a sequence that accesses the keys of a chain in order, it costs $\Theta(n)$ per access forever.
- **Wrong case test.** The test of line L4 compares sides: both left or both right. Testing only whether $x$ is a left child mixes up zig-zig and zig-zag.
- **Forgetting the root pointer.** After the loop, $x$ is the root; line L6 must update $T.root$. A tree object that still points to the old root sees only part of the tree.
- **Stale parent of the grandparent.** In ROTATE, the link from $z$ down to $y$ must switch to $x$ (line L11). If it is missed, the tree above $z$ loses $x$.
- **Not splaying on a miss.** If an unsuccessful search does not splay the last node visited, a sequence of misses deep in the tree costs $\Theta(n)$ each with no amortization.

## Implementations

The Python file has ROTATE and SPLAY with parent pointers, as in the main block, with leaf insertion and search helpers. The tests compare SPLAY with an independent version on immutable tuples, and check the Access Lemma bound on random trees with unit weights.

## History

Sleator and Tarjan introduced splaying in 1985, in the paper that defines splay trees. Their Section 2 gives the three cases, the potential with weights and the Access Lemma; Section 4 gives top-down splaying and semi-splaying.

## References
