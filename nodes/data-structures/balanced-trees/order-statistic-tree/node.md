---
tag: S2AJN7
kind: data-structure
slug: order-statistic-tree
name: Order-statistic tree
aliases:
- Order statistic tree
- augmented balanced tree
- dynamic order-statistic tree
- indexed BST
- rank tree
area: data-structures/balanced-trees
level: core
summary: A balanced BST augmented with subtree sizes so that the i-th smallest key and the rank of a key are found in O(log n) time.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [balanced-binary-search-tree, left-leaning-red-black-tree, tree-rotation]
see_also: [augmenting-data-structures, order-statistic, red-black-tree, implicit-treap, fenwick-tree, selection-problem, rank-select-dictionary, quickselect]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 17, Augmenting Data Structures, Section 17.1, Dynamic order statistics (OS-SELECT, OS-RANK, size in rotations) and Section 17.2, How to augment a data structure
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2, Binary Search Trees (the size field, select and rank) and Section 3.3, Balanced Search Trees
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (linear list representation with the RANK field)
---

An order-statistic tree is a [balanced binary search tree](/balanced-binary-search-tree/) in which each node also stores the number of nodes in its subtree. With these sizes, two more queries take $O(\log n)$ time: SELECT$(i)$, the key with exactly $i$ smaller keys (the [order statistic](/order-statistic/) of rank $i$), and RANK$(k)$, the number of keys less than $k$. The sizes are kept right with $O(1)$ work at each node whose subtree changes: the nodes on the update path and the nodes moved by a rotation. The balancing can be that of any balanced tree; this page uses the [left-leaning red-black tree](/left-leaning-red-black-tree/), and CLRS uses the classic [red-black tree](/red-black-tree/). It is the standard first example of [augmenting a data structure](/augmenting-data-structures/).

## In plain words

In a search tree, all keys of the left subtree come before the root and all keys of the right subtree come after it. If the root knows how many keys its left subtree holds, say 5, then the root is key number 6 in sorted order. To find key number 8, skip the left subtree and the root, and look for key number 2 in the right subtree. Each step goes one level down, so the work is the height of the tree.

The other way round works too. To count the keys smaller than some key, walk down to it and add up the left subtrees and the nodes passed on the right.

Each node stores the size of its own subtree. When the tree changes, only the nodes on one path and a few rotated nodes need a new size.

## The abstract type

The tree implements an [ordered set](/ordered-set/) with two more operations: SELECT$(i)$ for $0 \le i < n$ returns the key with exactly $i$ smaller keys, and RANK$(k)$ returns the number of keys less than $k$, for any $k$. So SELECT$(\text{RANK}(k)) = k$ for a present $k$. CONTAINS, INSERT and DELETE are as usual. Counting the keys in a range $[a, b)$ is RANK$(b) - $ RANK$(a)$.

## Representation

A node holds a key, a color, two child pointers and an integer $size$. The tree is a left-leaning red-black tree, with its rules: search order, no red right link, no two red links in a row, the same number of black links on every path to nil, and a black root. One more rule is added:

1. (Z) $x.size = 1 + $ SIZE$(x.left) + $ SIZE$(x.right)$, where SIZE(nil) $= 0$.

So $x.size$ is the number of nodes of the subtree of $x$, and the tree size is the size of the root.

## Operations

Ranks start at 0.

```pseudo id=main
SELECT(T, i)                               ▷ 0 ≤ i < SIZE(T.root)
L1  x ← T.root
L2  loop
L3      r ← SIZE(x.left)
L4      if i = r then return x.key
L5      if i < r then x ← x.left
L6      else i ← i − r − 1; x ← x.right

RANK(T, k)                                 ▷ the number of keys less than k
L7  r ← 0; x ← T.root
L8  while x ≠ nil
L9      if k < x.key then x ← x.left
L10     else if k = x.key then return r + SIZE(x.left)
L11     else r ← r + SIZE(x.left) + 1; x ← x.right
L12 return r

SIZE(x)
L13 if x = nil then return 0 else return x.size

UPDATE(x)
L14 x.size ← 1 + SIZE(x.left) + SIZE(x.right)

ROTATE-LEFT(h)                             ▷ ROTATE-RIGHT is the mirror image
L15 x ← h.right; h.right ← x.left; x.left ← h; x.red ← h.red; h.red ← true
L16 UPDATE(h); UPDATE(x); return x         ▷ h is now the lower node, so it goes first

FIX-UP(h)
L17 the three steps of the left-leaning red-black tree, then UPDATE(h); return h
```

INSERT and DELETE are those of the left-leaning red-black tree. PUT, REMOVE and DELETE-MIN all return FIX-UP$(h)$ for each node $h$ on the path, so line L17 recomputes the size of every node whose subtree changed, from the bottom up. A new node gets size 1. Color flips do not change sizes.

## Example

Insert S, E, A, R, C, H, X, M, P, L. A node is written key/size, and a star marks a red node:

$$(((A^*/1, C/2, \text{nil}), E/5, (H^*/1, L/2, \text{nil})), M/10, (P/1, R/4, (S^*/1, X/2, \text{nil}))).$$

The keys in order are A C E H L M P R S X.

**SELECT(6).** At M, the left size is 5 and $6 > 5$, so go right with $i = 6 - 5 - 1 = 0$. At R, the left size is 1 and $0 < 1$, so go left. At P, the left size is 0 $= i$: the answer is P, the seventh key.

**RANK(Q).** At M, $Q > M$: $r = 5 + 1 = 6$, go right. At R, $Q < R$: go left. At P, $Q > P$: $r = 6 + 0 + 1 = 7$, go right to nil. The answer is 7: A C E H L M P are less than Q.

**RANK(L).** At M, go left. At E, $L > E$: $r = 2 + 1 = 3$, go right. At L, the key is equal: the answer is $3 + 1 = 4$.

**INSERT(D).** D becomes the red right child of C. FIX-UP at C finds two red children and flips them, and C gets size 3. FIX-UP at E and at M only recompute the sizes, to 6 and 11. The tree is

$$(((A/1, C^*/3, D/1), E/6, (H^*/1, L/2, \text{nil})), M/11, (P/1, R/4, (S^*/1, X/2, \text{nil}))).$$

## Correctness

Since the keys of $x$'s subtree in order are those of $x.left$, then $x.key$, then those of $x.right$, the key of rank $i$ in $x$'s subtree is $x.key$ when $i$ equals the size of $x.left$, is in $x.left$ when $i$ is smaller, and else is the key of rank $i - |x.left| - 1$ in $x.right$. SELECT follows this, and RANK adds up the same counts on the way to $k$. The sizes stay right because a rotation recomputes its two nodes from their children, lower node first, and FIX-UP recomputes each node on the update path after its children are done. The full proof is in the proofs folder.

## Complexity

SELECT and RANK go down one path with $O(1)$ work per node, so they take $O(h)$ time, which is $\Theta(\log n)$ in the worst case because $h \le 2 \lg(n + 1)$ ([red-black height bound](/red-black-height-theorem/)). INSERT and DELETE do one more addition per node on the path and two per rotation, so they keep their $\Theta(\log n)$ bound. The size field is one word per node, so the space is $\Theta(n)$. All queries use $O(1)$ extra space; the updates use the $O(\log n)$ recursion stack of the left-leaning red-black tree.

## Variants

- **Other balancing.** The size field works with any balanced tree whose updates touch $O(\log n)$ nodes: [AVL trees](/avl-tree/), [treaps](/treap/), [weight-balanced trees](/weight-balanced-tree/), which already store sizes for balancing, and [skip lists](/skip-list/), with the length of each link.
- **Implicit keys.** An [implicit treap](/implicit-treap/) stores no keys at all: the position in the sequence is the rank, found from the sizes, so it supports insertion and deletion at any position of a list.
- **Other summaries.** Any value that can be computed at a node from the values at its children, such as a sum, a minimum or the maximum endpoint of an interval, can be kept the same way. This is the theorem of CLRS Section 17.2, and it gives interval trees.
- **Duplicates.** A multiset stores a count at each node and sums the counts instead of the nodes.
- **Static sets and small universes.** When the keys are fixed, a sorted array answers both queries with binary search. When the keys are integers from $0$ to $m - 1$, a [Fenwick tree](/fenwick-tree/) over the universe gives RANK as a prefix sum and SELECT by a descent, in $O(\log m)$ time with less code.

## When to use it

Use an order-statistic tree when a set changes and you need ranks or the $i$-th key between the changes: a running median, a leaderboard, counting inversions online, or the number of keys in a range. For one query on a fixed array, [quickselect](/quickselect/) or sorting is simpler. For integer keys in a small range, a Fenwick tree is shorter and faster.

## Pitfalls

- **Ranks from 0 or from 1.** CLRS gives the rank of a key as its position from 1, and this page counts the smaller keys, from 0. Mixing the two is an off-by-one error; a test checks that SELECT$(\text{RANK}(k)) = k$.
- **The order in a rotation.** After a rotation, the old top is now the lower node, and its size must be recomputed first, from its new children. Copying the old size of $h$ to $x$ is also correct, but only if $h.size$ was right before the rotation; inside FIX-UP it may not be, because a child of $h$ has just changed. Recomputing both from their children is always safe.
- **Paths that are not on the search path.** A size changes at every ancestor of an inserted or deleted node. An update that stops early, for example a delete that returns on an absent key after it has already changed the tree, leaves wrong sizes above. The implementation searches first.
- **Out-of-range select.** SELECT$(i)$ for $i \ge n$ walks into nil. Check the range first.

## Implementations

## History

Knuth's Volume 3 (1973) already describes balanced trees with a RANK field that gives the position of each node in its subtree, so that a balanced tree can serve as a linear list with access by position. CLRS, since its first edition in 1990, presents the form with subtree sizes on a red-black tree under the name *order-statistic tree*, as the first example of augmenting a data structure. The GNU C++ library offers the same structure as a policy-based tree with `find_by_order` and `order_of_key`.

## References
