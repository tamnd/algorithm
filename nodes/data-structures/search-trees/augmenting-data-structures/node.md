---
tag: 53C58P
kind: technique
slug: augmenting-data-structures
name: Augmenting data structures
aliases:
- data structure augmentation
area: data-structures/search-trees
level: core
summary: Store extra per-node information and maintain it under updates to support new queries.
prereqs: [binary-search-tree, tree-rotation, representation-invariant]
see_also: [order-statistic-tree, interval-tree, segment-tree, red-black-tree, treap, ordered-set, link-cut-tree, rank]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 17 (Augmenting data structures), Sections 17.1 (dynamic order statistics), 17.2 (how to augment a data structure, Theorem 17.1) and 17.3 (interval trees)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), the size field and the rank() and select() methods
---

Augmenting a data structure means storing extra information in each node of a known structure, such as a [binary search tree](/binary-search-tree/), and keeping it correct under updates, so that the structure answers new queries. The standard example is the subtree size, which turns a balanced tree into an [order statistic tree](/order-statistic-tree/) with [rank](/rank/) and select in $O(\log n)$ time. CLRS, Chapter 17, states the method in four steps and proves the key fact: a field that a node can compute from its own key and the fields of its children can be kept in a red-black tree at no extra asymptotic cost.

## In plain words

A search tree already keeps keys in order. Sometimes you want to ask more, such as "how many keys are smaller than this one?" Counting them each time is slow. Instead, let each node remember a small fact about the group of nodes below it, for example how many there are. Then the answer can be read off a few nodes on one path.

The work is to keep these facts true. Each time the tree changes, only the nodes on one path, and the few nodes that a rotation moves, can have a wrong fact. Fix those, from the bottom up, and the whole tree is right again.

## When it applies

- A known structure already does most of the work: it stores the right set and supports the updates in the time you want.
- The new query can be answered from a summary of each subtree, combined along one or two root-to-leaf paths.
- The summary $f(x)$ of a node $x$ can be computed in $O(1)$ time from $x$ itself and the summaries of its children. Sums, counts, minima, maxima and the product of matrices under an associative operation all have this form.
- The updates of the base structure change the shape of the tree only through local steps, such as leaf inserts, splices and [rotations](/tree-rotation/), each of which touches $O(1)$ nodes.

## The template

CLRS gives four steps: choose the base structure, choose the extra field, check that the updates of the base structure can keep the field, and write the new operations. The heart of the third step is one routine and one rule.

```pseudo id=main
PULL(x)                                          ▷ recompute the field of x from its children
L1  x.f ← COMBINE(x, f(x.left), f(x.right))       ▷ f(NIL) is a fixed value, such as 0
L2  return

AFTER-UPDATE(T, x)                               ▷ x is the lowest node whose subtree changed
L3  while x ≠ NIL do
L4      PULL(x)
L5      x ← x.p

AFTER-ROTATION(x, y)                             ▷ y was the child of x and is now its parent
L6  PULL(x)                                      ▷ the lower node first
L7  PULL(y)
```

Lines L3 to L5 run after an insert or a delete: the subtrees that changed are exactly those of the nodes on the path from the changed place to the root, so recomputing them from the bottom up makes all fields right. Lines L6 and L7 run after each rotation: only the subtrees of the two nodes that rotate change, and the new lower node must be fixed before the new upper node. A query then reads the fields on one path, for example rank and select, or prunes whole subtrees by their field, as in interval search.

**Theorem (CLRS, Theorem 17.1).** If the field $f$ of a red-black tree can be computed for each node from the node and the fields of its children, then insert and delete keep $f$ in $O(\log n)$ time.

*Reason.* Both operations change the tree along one path of length $O(\log n)$ and do $O(1)$ rotations (at most 2 for insert and at most 3 for delete). The path costs $O(\log n)$ calls of PULL, and each rotation costs 2 more.

## Classic examples

- **Order statistic tree (subtree size).** $x.size = x.left.size + x.right.size + 1$ with $\mathrm{NIL}.size = 0$. Select$(x, i)$ compares $i$ with $x.left.size$ and goes left, stops, or goes right with $i - x.left.size - 1$. Rank adds $x.left.size + 1$ at each node where the path goes right. See the [order statistic tree](/order-statistic-tree/). For the tree with root 50, left subtree $\{20, 30, 35, 40, 45\}$ and right subtree $\{60, 65, 70, 80\}$, the root has size 10 and its left child has size 5, so 50 has rank 5 (0-based), and select$(7)$ goes right with $i = 7 - 5 - 1 = 1$.
- **Interval tree (subtree maximum).** Each node stores an interval keyed by its low end, and $x.max$ is the largest high end in its subtree. A search for an interval that overlaps $[a, b]$ goes left when the left child exists and $x.left.max \ge a$, and right otherwise. See the [interval tree](/interval-tree/).
- **Subtree sums.** With a value at each node, $x.sum$ gives the sum of the values of all keys in a range in $O(\log n)$ time: sum the left parts along the path to $lo$ and $hi$.
- **Implicit keys.** In an implicit [treap](/treap/), the size field alone gives the position of each node, so the tree acts as a sequence with split, join and insert at a position in $O(\log n)$ expected time.
- **Segment tree.** A [segment tree](/segment-tree/) is a static shape with the field "the combination of the values in my range", recomputed along one path per update.
- **Path aggregates in dynamic trees.** A [link-cut tree](/link-cut-tree/) keeps fields in splay trees over preferred paths, with the same PULL after each rotation.

## Variations

- **Lazy propagation.** Some updates change a whole subtree, such as "add $c$ to all values in a range". Store a pending tag at the top node and push it to the children (PUSH) before each visit below. PUSH comes before the descent and PULL after it.
- **Fields that depend on the parent.** A field such as the depth of a node, which depends on its ancestors, cannot be kept this way: one rotation changes it in a whole subtree. Store a difference from the parent instead, so that the field again depends only on local values.
- **Monoid fields.** If COMBINE is the operation of a monoid on values in in-order, the field of a node is the product of the values in its subtree, in order. Then any range product costs $O(\log n)$ operations, and the order of the operands is kept even if the operation does not commute.
- **Persistent and functional trees.** With path copying, each copied node recomputes its field once, at no extra cost; see [persistent data structures](/persistent-data-structure/).
- **Augmenting other structures.** Skip lists keep the width of each link, and B-trees keep a count per child pointer, with the same rule: recompute on the path that changed.

## Pitfalls

- **Wrong order in a rotation.** After a rotation the node that moved down must be recomputed first (line L6). Recomputing the new parent first uses the old field of its child and gives a wrong value.
- **Forgetting the path below the deleted node.** In a two-child delete, the node that moves up is the successor, from deeper in the tree. The fields of all nodes from the old place of the successor up to the root change, not only those above the deleted key.
- **A field that is not local.** "The rank of this node" or "the depth of this node" seems easy to store, but a single insert can change it at $\Theta(n)$ nodes. Store subtree data, not global data.
- **Wrong value for NIL.** The value of $f(\mathrm{NIL})$ must be the identity of COMBINE: 0 for sums and sizes, $-\infty$ for maxima. A wrong identity changes every field above a leaf.
- **Updating fields on the way down.** Adding 1 to each size on the way down during an insert is correct only if the insert surely adds a key. If the key is already present, the sizes on the path become wrong. Recompute on the way up, or search first.

## Exercises

1. Augment a red-black tree so that it returns the number of keys in $[lo, hi]$ in $O(\log n)$ time. Which field do you need, and how many nodes do you read?
2. Show that the depth of each node cannot be kept in $O(\log n)$ time per insert in a red-black tree, by giving a sequence of inserts whose rotations change the depth of $\Omega(n)$ nodes.
3. Augment an [order statistic tree](/order-statistic-tree/) so that it returns the sum of the $i$ smallest keys in $O(\log n)$ time.
4. Keep, in each node, the maximum gap between consecutive keys in its subtree. Which fields besides the gap must each node store so that PULL is $O(1)$?
5. Prove that AFTER-ROTATION fixes all fields after one rotation: show that exactly two subtrees change their set of nodes.

## References
