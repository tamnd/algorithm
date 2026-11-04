---
tag: S6DS4V
kind: data-structure
slug: treap
name: Treap
area: data-structures/balanced-trees
level: core
summary: A binary search tree in which each node also has a random priority and the tree is kept heap ordered by priority, giving expected logarithmic height.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {expected: Θ(log n), worst: Θ(n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, tree-rotation, heap-property, random-binary-search-tree]
see_also: [treap-split, treap-merge, implicit-treap, cartesian-tree, zip-tree, skip-list, persistent-treap, random-bst-expected-depth]
sources:
  - paper: doi:10.1007/BF01940876
    title: Raimund Seidel and Cecilia R. Aragon, Randomized search trees, Algorithmica 16(4/5), 1996
    locator: pages 464 to 497 (the expected depth, the expected number of rotations, and the analysis by ancestor events)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, end-of-chapter problem on treaps (insertion by rotations, and fewer than 2 expected rotations)
  - url: https://opendatastructures.org/
    title: Pat Morin, Open Data Structures
    locator: Chapter 7, Random Binary Search Trees, Section 7.2 Treap
  - url: https://jeffe.cs.illinois.edu/teaching/algorithms/notes/03-treaps.pdf
    title: Jeff Erickson, Algorithms lecture notes, Treaps and Skip Lists
    locator: the analysis of treaps by ancestor indicator variables
---

A treap is a [binary search tree](/binary-search-tree/) in which each node also holds a random number, its *priority*, and the tree is a heap on the priorities: no node has a higher priority than its parent. For one set of keys and priorities there is exactly one such tree, the [Cartesian tree](/cartesian-tree/) of the pairs. With priorities drawn at random, it has the shape of a [random binary search tree](/random-binary-search-tree/) whatever the order of the updates, so the expected depth of each node is less than $2 \ln n$, and search, insertion and deletion take $O(\log n)$ expected time. An insertion puts the key at a leaf and rotates it up while its priority is higher than its parent's; a deletion rotates the key down to a leaf and cuts it off. Each update does fewer than two rotations on average. Seidel and Aragon introduced the treap in 1989.

## In plain words

A binary search tree is short when the keys arrive in a random order, and tall when they arrive sorted. A treap gets the good case for any order of keys.

When a key comes in, it gets a random ticket. The tree is kept as if the keys had been inserted in the order of their tickets, highest ticket first. So the key with the highest ticket is at the top, the highest ticket on each side is at the top of that side, and so on down. You cannot know the ticket order in advance, so the tree is built by moving each new key up: put it at the bottom as usual, then turn it above its parent while its ticket is higher.

Since the tickets are random, the tree looks like one built from a random order of keys, and that tree is short on average.

## The abstract type

A treap implements the [ordered set](/ordered-set/): `contains(T, k)`, `insert(T, k)`, `delete(T, k)`, and the order operations of a search tree (minimum, maximum, predecessor, successor, in-order iteration). With a value in each node it is an [ordered symbol table](/ordered-symbol-table/). The keys come from a total order. The treap also supports split and merge, which other balanced trees do with more work: see [treap split](/treap-split/) and [treap merge](/treap-merge/).

## Representation

Each node $t$ has a key $t.key$, a priority $t.pri$, and two children $t.left$ and $t.right$ (each a node or nil). The priorities are drawn independently from a continuous distribution, such as uniform real numbers in $[0, 1)$, or random integers of 32 or more bits, where ties are rare.

**Invariant.** (P1) The keys are in search-tree order. (P2) Each node has a priority at least as high as the priorities of its children: the tree is a max-heap on priorities (see [heap property](/heap-property/)).

**Uniqueness.** If the priorities are distinct, (P1) and (P2) fix the tree. The root must be the node of highest priority. The keys less than the root's key form the left subtree and the greater keys form the right subtree, and each is fixed in the same way. So the treap is the binary search tree that results from inserting the keys in decreasing order of priority, with no rotations.

## Operations

A search is the search of a [binary search tree](/bst-search/); it ignores the priorities. The procedures below are recursive and return the new root of the subtree. They use the [rotations](/tree-rotation/) ROTATE-RIGHT$(t)$, which lifts $t.left$ above $t$, and ROTATE-LEFT$(t)$, its mirror image.

```pseudo id=main
INSERT(t, k, p)                            ▷ p is a fresh random priority
L1  if t = nil then return a new node with key k and priority p
L2  if k < t.key then t.left ← INSERT(t.left, k, p)
L3      if t.left.pri > t.pri then t ← ROTATE-RIGHT(t)
L4  else if k > t.key then t.right ← INSERT(t.right, k, p)
L5      if t.right.pri > t.pri then t ← ROTATE-LEFT(t)
L6  return t

DELETE(t, k)
L7  if t = nil then return nil
L8  if k < t.key then t.left ← DELETE(t.left, k)
L9  else if k > t.key then t.right ← DELETE(t.right, k)
L10 else if t.left = nil then return t.right
L11 else if t.right = nil then return t.left
L12 else if t.left.pri > t.right.pri then t ← ROTATE-RIGHT(t); t.right ← DELETE(t.right, k)
L13 else t ← ROTATE-LEFT(t); t.left ← DELETE(t.left, k)
L14 return t
```

INSERT goes down as in a plain search tree and adds the new node as a leaf at line L1. On the way back up, lines L3 and L5 rotate the new node above its parent while its priority is higher; the node stops where the heap order holds. DELETE finds the node and, while it has two children, lifts the child of higher priority above it (lines L12 and L13); the node goes one level down each time and keeps the other nodes in heap order. When it has at most one child, lines L10 and L11 replace it by that child.

## Example

Insert the keys 50, 30, 70, 20, 40, 60 with the priorities 30, 60, 40, 10, 80, 50, then delete 40 and 30. A tree is written as (left, key, right), and a leaf as its key.

| operation | rotations | tree after |
|---|---|---|
| insert 50 (priority 30) | none | 50 |
| insert 30 (60) | 30 goes left of 50; 60 > 30: rotate right at 50 | (nil, 30, 50) |
| insert 70 (40) | 70 goes right of 50; 40 > 30: rotate left at 50 | (nil, 30, (50, 70, nil)) |
| insert 20 (10) | none | (20, 30, (50, 70, nil)) |
| insert 40 (80) | 40 goes left of 50 and rises three times: above 50, above 70, above 30 | ((20, 30, nil), 40, (50, 70, nil)) |
| insert 60 (50) | 60 goes right of 50 and rises above 50, then above 70 | ((20, 30, nil), 40, (50, 60, 70)) |
| delete 40 | children 30 (60) and 60 (50): rotate right; 40 has no left child and is replaced by its right subtree | (20, 30, (50, 60, 70)) |
| delete 30 | children 20 (10) and 60 (50): rotate left; then children 20 (10) and 50 (30): rotate left; then 30 is a leaf | ((20, 50, nil), 60, 70) |

The tree after the six insertions is the one that inserting 40, 30, 60, 70, 50, 20 into a plain search tree gives: the keys in decreasing order of priority. Any order of the six insertions gives the same tree.

## Correctness

A rotation keeps (P1). In INSERT, the new leaf $x$ may break (P2) only with its parent; a rotation that lifts $x$ above its parent $y$ makes $y$ a child of $x$, and the other children of $x$ and $y$ were already below both, so the only possible violation is again between $x$ and its new parent. When the test at line L3 or L5 fails, the tree is a treap. In DELETE, the node $x$ to remove is the only node that may have a lower priority than a child, and lifting the child of higher priority keeps the order among all other nodes. The full proof is in the proofs folder.

## Complexity

The priorities make the shape random, whatever the keys and the order of the operations, as long as the operations do not depend on the priorities. Let $x_1 < x_2 < \dots < x_n$ be the keys. Since the treap is the search tree built by inserting the keys in random order, $x_i$ is an ancestor of $x_k$ exactly when $x_i$ has the highest priority among $x_i, \dots, x_k$ (or $x_k, \dots, x_i$). This has probability $1 / (|i - k| + 1)$. By [linearity of expectation](/linearity-of-expectation/), the expected number of proper ancestors of $x_k$ is

$$\sum_{i \ne k} \frac{1}{|i - k| + 1} = H_k + H_{n - k + 1} - 2 < 2 \ln n,$$

where $H_m = 1 + 1/2 + \dots + 1/m$. So a search takes $O(\log n)$ expected time, and so do insertion and deletion, which follow one path down and back. The height is $O(\log n)$ with high probability. The worst case is $\Theta(n)$, which happens only with very small probability.

**Rotations.** The rotations of a deletion of $x_k$ move $x_k$ down once for each node on the right spine of its left subtree and the left spine of its right subtree. These spines have expected lengths $1 - 1/k$ and $1 - 1/(n - k + 1)$, so a deletion makes fewer than two rotations on average. An insertion is a deletion run backward, so the same bound holds. This is important when a rotation is costly, for example when each node stores a summary of its subtree.

**Space.** Each node holds a key, a priority and two pointers: $\Theta(n)$ space in total.

## Variants

- **Split and merge.** A treap can be cut at a key into two treaps, and two treaps with separated keys can be joined, in $O(\log n)$ expected time; see [treap split](/treap-split/) and [treap merge](/treap-merge/). Insertion and deletion can be written with them instead of rotations.
- **Implicit treap.** Keyed by position instead of by value, a treap stores a sequence with insertion, deletion, reversal and range sums at any position. See [implicit treap](/implicit-treap/).
- **Priorities by hashing.** The priority can be a hash of the key. Then the shape depends only on the set of keys, which helps for persistent and concurrent trees. See [persistent treap](/persistent-treap/).
- **Zip trees** store a treap with random ranks drawn from a geometric distribution, with insertion and deletion by unzipping and zipping paths instead of rotations. See [zip tree](/zip-tree/).
- **Skip lists** use the same kind of randomness in a linked structure. See [skip list](/skip-list/).

## When to use it

Use a treap when you want a balanced search tree with short code, and expected bounds are good enough. It is the easiest balanced tree to extend with split and merge, so it is common in contest code and for sequences with range operations. Avoid it when you need worst-case bounds for each operation, or when an adversary can see the priorities and choose the keys.

## Pitfalls

- **Priorities that are not random.** If the priority is a fixed function of the order of arrival, or of the key, the tree is no better than a plain search tree. With priority equal to the key, sorted input gives a path of height $n$. A test of the implementation checks this case.
- **Breaking ties by the wrong side.** Lines L3 and L5 use a strict test. With equal priorities both orders satisfy (P2), so no rotation is needed; a test with $\ge$ would rotate for nothing, and with many ties it could do many rotations. Use priorities with enough bits that ties are rare.
- **Rotating down to the wrong side.** Lines L12 and L13 must lift the child of the *higher* priority. Lifting the other child puts a node of lower priority above one of higher priority.
- **Seeding.** Use a random source that each tree owns. A fixed seed makes the shape repeatable for tests, but a known seed lets an adversary choose keys that give a tall tree.

## Implementations

## History

Jean Vuillemin described the Cartesian tree, a binary tree with search order on one coordinate and heap order on another, in 1980. Cecilia Aragon and Raimund Seidel proposed treaps with random priorities at FOCS in 1989, and gave the full analysis in the journal version in Algorithmica in 1996. The name joins "tree" and "heap". Later work added split and merge, finger searches, and the implicit form for sequences.

## References
