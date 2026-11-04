---
tag: RSMQKE
kind: algorithm
slug: bst-deletion
name: Binary search tree deletion
aliases:
- BST delete
area: data-structures/search-trees
level: intro
summary: Handles leaf, one-child and two-child cases, the last by replacing the key with its successor.
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search-tree, bst-search, bst-insertion]
see_also: [red-black-tree-deletion, random-binary-search-tree, lazy-deletion, treap, tree-rotation, splay-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.3 (Insertion and deletion), TRANSPLANT and TREE-DELETE
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), Algorithm D (tree deletion) and the discussion of deletions in random trees
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), deleteMin and Hibbard deletion
  - paper: doi:10.1145/321105.321108
    title: Thomas N. Hibbard, Some combinatorial properties of certain trees with applications to searching and sorting, Journal of the ACM 9(1), 1962
    locator: pages 13 to 28
  - paper: doi:10.1145/358172.358183
    title: Jeffrey L. Eppinger, An empirical study of insertion and deletion in binary search trees, Communications of the ACM 26(9), 1983
    locator: pages 663 to 669
---

BST deletion removes a key from a [binary search tree](/binary-search-tree/) and keeps the [binary search tree property](/binary-search-tree-property/). It has three cases: a node with no child is cut off, a node with one child is replaced by that child, and a node with two children takes the key of its in-order successor, whose node has no left child and is then removed by one of the first two cases. This last case is Hibbard deletion (1962). It takes $O(h)$ time on a tree of height $h$.

## In plain words

Removing a leaf from a tree is easy: cut it off. Removing a node with one branch is also easy: the branch moves up and takes its place, and the order is still right, because everything in that branch was already on the right side of everything above.

The hard case is a node with two branches. You cannot lift both branches into one place. So find the key that comes just after it in sorted order. That key is the leftmost node of the right branch, and it never has a left branch. Copy it into the node you want to remove, and then remove the old copy, which is one of the easy cases.

## The problem

The input is a binary search tree $T$ with distinct keys and a key $k$. The output is a binary search tree with the keys of $T$ except $k$, where each other key keeps its value, and a flag that says whether $k$ was in $T$. If $k$ is not a key, $T$ does not change.

## The algorithm

Each node has the fields $key$, $value$, $left$, $right$ and $p$ (the parent).

```pseudo id=main
TREE-DELETE(T, k)
L1  z ← TREE-SEARCH(T.root, k)
L2  if z = NIL then return false
L3  if z.left ≠ NIL and z.right ≠ NIL then          ▷ case 3: two children
L4      y ← TREE-MINIMUM(z.right)                    ▷ the successor; y.left = NIL
L5      z.key ← y.key; z.value ← y.value
L6      z ← y                                         ▷ now remove the node y
L7  c ← z.left if z.left ≠ NIL else z.right           ▷ z has at most one child c
L8  if c ≠ NIL then c.p ← z.p
L9  if z.p = NIL then T.root ← c
L10 elseif z = z.p.left then z.p.left ← c
L11 else z.p.right ← c
L12 T.n ← T.n − 1; return true
```

Line L1 is the [BST search](/bst-search/). If $z$ has two children, lines L4 to L6 find its successor $y$, the leftmost node of the right subtree, copy its key and value into $z$, and make $y$ the node to remove. The successor has no left child, because a left child would have a smaller key that is still larger than $z.key$. After line L6, the node $z$ to remove has at most one child. Lines L7 to L11 splice it out: its child $c$ (or NIL for a leaf) takes its place under its parent. This handles case 1 (a leaf, $c = $ NIL) and case 2 (one child) with the same code.

## Example

Start from the tree built by inserting 50, 30, 70, 20, 40, 60, 80, 35, 45 and 65. Then delete 60, 30, 20 and 50, in this order.

```
              50
           /      \
         30        70
        /  \      /  \
      20    40   60   80
           /  \    \
         35    45   65
```

| delete | case | what happens | tree after (root, left subtree, right subtree) |
|---|---|---|---|
| 60 | one child | 65 takes the place of 60 as the left child of 70 | 50; 30(20, 40(35, 45)); 70(65, 80) |
| 30 | two children | the successor is 35, the leftmost node under 40; 35 is copied into the node of 30, and the leaf 35 is cut off | 50; 35(20, 40(-, 45)); 70(65, 80) |
| 20 | leaf | the left child of 35 becomes NIL | 50; 35(-, 40(-, 45)); 70(65, 80) |
| 50 | two children, at the root | the successor is 65, the leftmost node under 70; 65 is copied into the root, and the leaf 65 is cut off | 65; 35(-, 40(-, 45)); 70(-, 80) |

```
         65
       /    \
     35      70
       \       \
        40      80
          \
           45
```

The in-order sequence after the four deletes is 35, 40, 45, 65, 70, 80. A delete of 50 now returns false.

## Correctness

Splicing out a node $z$ with at most one child $c$ is safe: the subtree of $c$ was inside the subtree of $z$, so each ancestor of $z$ still has it on the correct side. In case 3, the successor $y$ holds the smallest key larger than $z.key$. After the copy, the key $y.key$ sits at $z$, and it is larger than each key of the left subtree of $z$ (they are smaller than $z.key$) and smaller than each other key of the right subtree (by the choice of $y$ as their minimum). So the BST property holds, and the only key that leaves the tree is $k$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The search of line L1 takes $O(d_z + 1)$ time, where $d_z$ is the depth of $z$. The walk of line L4 goes from $z$ down to $y$, at most $h - d_z$ more steps. Lines L5 to L12 take $O(1)$ time. So the time is $O(h + 1)$ in the worst case, and $\Theta(n)$ on a chain. A delete of the root of a tree whose root has at most one child takes $\Theta(1)$ time after the search.

In a tree built by random insertions, a delete takes $O(\log n)$ expected time, because the expected height is $O(\log n)$. Hibbard deletion does not keep this distribution under long mixed sequences of inserts and deletes; Knuth discusses this effect in Section 6.2.2. In experiments of Eppinger (1983) with long random sequences of inserts and deletes, the average search path became longer than in a random tree. The reason is the asymmetry: case 3 always takes from the right subtree.

The extra space is $O(1)$; the algorithm uses loops and no recursion.

## Properties

- **Moves keys, not only links.** Case 3 copies a key and a value into another node. A pointer that a user kept to the successor node now points to a removed node, and a pointer to $z$ now sees another key. The variant of CLRS below avoids this.
- **Asymmetric.** It always takes the successor, never the predecessor.
- **Local.** It changes links only at the removed node and its parent, and the keys of at most one other node.
- **Uses parent pointers.** Lines L8 to L11 need $z.p$. Without parent pointers, keep the parent during the search, or use the recursive form.

## Variants and improvements

- **Splice the successor node (CLRS).** CLRS Section 12.3 does not copy keys. It uses TRANSPLANT to move the successor node itself into the place of $z$, with the two subtrees of $z$. Each other node keeps its key, so external pointers to nodes stay valid. This is the form used inside [red-black tree deletion](/red-black-tree-deletion/).
- **Recursive Hibbard deletion (Sedgewick and Wayne).** `delete(x, k)` returns the new root of the subtree of $x$. For two children it saves $t = x$, sets $x$ to `min(t.right)`, sets `x.right = deleteMin(t.right)` and `x.left = t.left`. This form needs no parent pointers.
- **Predecessor or random choice.** Use the predecessor, the rightmost node of the left subtree, instead of the successor. Choosing between the two at random, or by turns, removes the systematic drift to one side.
- **Delete by rotation.** Rotate $z$ down with [tree rotations](/tree-rotation/), toward the child of higher priority in a [treap](/treap/), until it is a leaf, then cut it off. This keeps the treap shape random.
- **Lazy deletion.** Mark the node as deleted and leave it in the tree, then rebuild when too many nodes are marked. See [lazy deletion](/lazy-deletion/). A [scapegoat tree](/scapegoat-tree/) uses rebuilds of this kind.
- **Balanced deletion.** [AVL trees](/avl-tree/) and [red-black trees](/red-black-tree/) run this deletion and then repair the balance condition on the path to the root.
- **Splay deletion.** A [splay tree](/splay-tree/) splays $k$ to the root, removes it, and joins the two subtrees.

## When to use it

Use it as the delete of a plain binary search tree, and as the first step of the delete of a balanced tree. Prefer the CLRS node-splicing form when other code keeps pointers to nodes, for example in an [augmented tree](/augmenting-data-structures/) or a tree with node handles. If deletes are frequent and the tree is not balanced, expect the shape to drift; use a balanced tree or a [treap](/treap/) instead.

## Pitfalls

- **Taking the successor from the wrong place.** The successor in case 3 is the minimum of the right subtree (line L4), not the right child itself. Moving the right child up in general breaks the BST property when the right child has a left subtree.
- **Forgetting the child of the successor.** The successor has no left child but can have a right child. Lines L7 to L11 must move that child up into the place of the successor; cutting the successor off as if it were a leaf loses a whole subtree.
- **Deleting the root.** When $z.p = $ NIL, the new subtree root must go into $T.root$ (line L9). Code that only updates a parent pointer field leaves the old root in place.
- **Stale parent pointer.** If line L8 is missing, the child $c$ keeps its old parent, and a later successor or delete walks into the removed node.
- **Handles after a key copy.** With the key copy of line L5, a stored pointer to the successor node is stale after the delete. If the tree hands out node handles, use the CLRS form.
- **Augmented fields.** In an [order statistic tree](/order-statistic-tree/), the subtree sizes must drop by 1 on the whole path from the removed node to the root, including the part below $z$ down to the successor.

## Implementations

The Python function follows the main block and uses parent pointers. The search of line L1 and the walk of line L4 are written inline as loops.

## History

Hibbard's paper of 1962 introduced this method of deletion and analysed it in random trees. Knuth gives it as Algorithm D in Section 6.2.2, and discusses there how deletions affect the randomness of the tree. The node-splicing form with TRANSPLANT appears in the third and fourth editions of CLRS.

## References
