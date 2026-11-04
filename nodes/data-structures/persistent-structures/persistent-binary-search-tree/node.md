---
tag: F9C8A3
kind: data-structure
slug: persistent-binary-search-tree
name: Persistent binary search tree
aliases:
- persistent BST
- functional binary search tree
area: data-structures/persistent-structures
level: core
summary: A binary search tree updated by path copying, so each insert or delete yields a new root with O(log n) new nodes when balanced.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the version, h: the height of the version, N: the number of nodes made by all updates}
  time: {contains: Θ(h), insert: Θ(h), delete: Θ(h)}
  space: {total: Θ(N)}
history:
  year: 1986
  people: [Neil Sarnak, Robert E. Tarjan]
  note: Sarnak and Tarjan used persistent search trees for planar point location; path copying in functional search trees is older.
prereqs: [binary-search-tree, bst-search, bst-insertion, bst-deletion, path-copying]
see_also: [persistent-red-black-tree, persistent-treap, persistent-dynamic-set, structural-sharing, version-tree, sarnak-tarjan-point-location, node-copying, join-based-tree-algorithms]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.2 Binary Search Trees (insert copies the search path and shares the rest)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Problem 13-1, Persistent dynamic sets
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the discussion of path copying for search trees
---

A persistent binary search tree is a [binary search tree](/binary-search-tree/) in which insertion and deletion never change a node: they copy the nodes on the search path and return a new root, and all other nodes are shared with the old version. Each version is the tree reachable from its root, so every old version stays valid and searchable. On a version of height $h$ an update takes $\Theta(h)$ time and makes at most $h + 1$ new nodes. With a balanced shape, such as a [persistent red-black tree](/persistent-red-black-tree/) or a [persistent treap](/persistent-treap/), this is $O(\log n)$ per update.

## In plain words

In a search tree, each key is in a node, smaller keys go to the left and larger keys go to the right. To add a key, you walk down from the top to the place where it belongs.

The persistent version does not change any node on this walk. It makes a new copy of each node that it passed, and each copy points to the next copy on the way down. The new key hangs at the bottom. Each copy keeps its other child pointing to the old subtree, which is shared and not copied.

The new top node is the new tree. The old top node is still the old tree, because none of its nodes changed. So both trees can be searched at any time later, and the second one cost only as many new nodes as the length of the walk.

## The abstract type

A persistent binary search tree implements the [ordered set](/ordered-set/) with value semantics: `contains(T, k)` returns a boolean, and `insert(T, k)` and `delete(T, k)` return a new set and leave $T$ as it was. It also gives the order queries of a search tree on each version (minimum, maximum, predecessor, successor, in-order listing). The keys come from a total order. The structure is fully persistent: any version can be updated. The [persistent dynamic set](/persistent-dynamic-set/) problem asks for exactly this.

## Representation

A version is a pointer to a root, which is nil for the empty set. Each node $x$ has a key $x.key$ and two children $x.left$ and $x.right$.

**Invariant.** (B1) *Search order.* In each version, for each node $x$, every key in the subtree of $x.left$ is less than $x.key$, and every key in the subtree of $x.right$ is greater. (B2) *Immutability.* No field of a node changes after the node is made.

A node can be in many versions at once. By (B2), its subtree is the same in all of them. The nodes of all versions form a directed acyclic graph, not a tree, because a node can have several parents in different versions.

## Operations

NEW-NODE$(k, l, r)$ makes a node with the given key and children; it is the only way to set a field. SEARCH is the plain [search](/bst-search/) and changes nothing.

```pseudo id=main
SEARCH(t, k)
L1  while t ≠ nil and t.key ≠ k do
L2      if k < t.key then t ← t.left else t ← t.right
L3  return t ≠ nil

INSERT(t, k)                                ▷ returns the root of the new version
L4  (path, x) ← DESCEND(t, k)
L5  if x ≠ nil then return t                ▷ k is present: share the whole tree
L6  return REBUILD(path, k, NEW-NODE(k, nil, nil))

DELETE(t, k)                                ▷ returns the root of the new version
L7  (path, x) ← DESCEND(t, k)
L8  if x = nil then return t                ▷ k is absent: share the whole tree
L9  if x.left = nil then c ← x.right
L10 else if x.right = nil then c ← x.left
L11 else                                    ▷ two children: use the successor y
L12     q ← the nodes on the left steps from x.right, without the last node y (y.left = nil)
L13     c ← NEW-NODE(y.key, x.left, REBUILD(q, y.key, y.right))
L14 return REBUILD(path, k, c)

DESCEND(t, k)                               ▷ the nodes passed, and the node of k or nil
L15 path ← an empty list
L16 while t ≠ nil and t.key ≠ k do
L17     append t to path
L18     if k < t.key then t ← t.left else t ← t.right
L19 return (path, t)

REBUILD(path, k, c)                         ▷ copy path bottom up; c replaces the child toward k
L20 for each node y of path, from the last to the first do
L21     if k < y.key then c ← NEW-NODE(y.key, c, y.right)
L22     else c ← NEW-NODE(y.key, y.left, c)
L23 return c
```

DESCEND records the search path for $k$: the nodes whose key differs from $k$, from the root down. REBUILD then makes one copy of each of these nodes, from the bottom up. The copy of a node gets the new subtree $c$ on the side where $k$ goes, and the old child on the other side. So the copies form a new path from a new root down to the place of the change, and every subtree off the path is shared.

INSERT hangs a new leaf where the search fell off the tree. DELETE replaces the node $x$ of $k$ by a subtree $c$. If $x$ has at most one child, $c$ is that child, shared as it is. If $x$ has two children, its successor $y$ is the leftmost node of the right subtree. Line L13 removes $y$ from the right subtree by copying the left path down to it (REBUILD with the key $y.key$, which is less than each key on $q$, so each copy changes its left child), and makes a new node with key $y.key$ in the place of $x$. When the key is present at line L5 or absent at line L8, the update returns the old root, so the two versions are the same tree.

The procedures use loops and an explicit path, not recursion, because the height of an unbalanced tree can be $n$.

## Example

Insert 50, 30, 70, 20, 40, 60, 80 in this order into the empty tree $v_0$. Each insertion copies the search path and adds one leaf.

| version | operation | copied nodes | new leaf | new nodes |
|---|---|---|---|---|
| $v_1$ | insert 50 | none | 50 | 1 |
| $v_2$ | insert 30 | 50 | 30 | 2 |
| $v_3$ | insert 70 | 50 | 70 | 2 |
| $v_4$ | insert 20 | 50, 30 | 20 | 3 |
| $v_5$ | insert 40 | 50, 30 | 40 | 3 |
| $v_6$ | insert 60 | 50, 70 | 60 | 3 |
| $v_7$ | insert 80 | 50, 70 | 80 | 3 |

The eight versions use 17 nodes in total. Keeping each version as a separate tree would need $0 + 1 + 2 + \cdots + 7 = 28$ nodes. The tree $v_7$ is the full tree of height 3, with root 50, children 30 and 70, and leaves 20, 40, 60, 80.

Next, $v_8 = $ INSERT$(v_7, 35)$. The search path is 50, 30, 40, and 35 becomes the left child of a copy of 40. This makes 4 new nodes: copies of 50, 30, 40 and the leaf 35. The copy of 50 shares the old right subtree (70, 60, 80), and the copy of 30 shares the old leaf 20.

Last, $v_9 = $ DELETE$(v_8, 50)$. The node of 50 is the root, so the path is empty, and it has two children. Its successor is $y = 60$, reached from 70 by one left step, so $q = [70]$. Line L13 makes a copy of 70 with left child nil (the old right child of 60) and right child 80, and a new root with key 60, left child the left subtree of $v_8$, and right child the copy of 70. This makes 2 new nodes. The version $v_9$ holds 20, 30, 35, 40, 60, 70, 80, and $v_7$ and $v_8$ are unchanged: $v_7$ still has root 50 and 7 keys.

## Correctness

The proof uses the open interval of keys that may appear at a position of the tree. A node reached from the root by the search path for $k$ has all its keys between the largest key on the path at which the search went right and the smallest key at which it went left. REBUILD keeps (B1) if the new subtree $c$ has all its keys in that interval, and INSERT and DELETE call it only with such a subtree. Since only NEW-NODE writes fields, (B2) holds, so the old version is the same tree as before. The full proof is in the proofs folder.

## Complexity

| operation | time | new nodes |
|---|---|---|
| contains | $\Theta(h)$ worst case | none |
| insert | $\Theta(h)$ worst case | at most $h + 1$ |
| delete | $\Theta(h)$ worst case | at most $h - 1$ |

Here $h$ is the height of the version that the operation uses, counted in nodes. The model is the [comparison model](/comparison-model/) for the keys, with a pointer machine for the nodes. DESCEND visits at most $h$ nodes, and REBUILD copies each node of the path once. In DELETE with two children, the nodes of the path to $x$, the node $x$, the nodes of $q$ and the node $y$ all lie on one root-to-leaf path, so the path and $q$ have at most $h - 2$ nodes together; with the new node at line L13 the count is at most $h - 1$. With at most one child, only the path above $x$ is copied, which is at most $h - 1$ nodes.

The height depends on the order of the updates on the chain of versions that led to the version, as for an ephemeral tree. It is $\Theta(n)$ in the worst case, for example after inserting keys in sorted order. If the keys of one chain of versions arrive in a uniformly random order, the expected depth of a node is $O(\log n)$, as in a [random binary search tree](/random-binary-search-tree/). To get $O(\log n)$ in the worst case, use a balanced tree with path copying; the rebalancing touches only nodes on or next to the search path, so it adds $O(\log n)$ new nodes.

**Space.** The structure uses one node per NEW-NODE call. After a sequence of updates the total space is the number of nodes made, which is at most the sum over all updates of $h_i + 1$, where $h_i$ is the height of the version used by update $i$.

## Variants

- **Balanced persistent trees.** The [persistent red-black tree](/persistent-red-black-tree/) and the [persistent treap](/persistent-treap/) bound the height by $O(\log n)$ (worst case or expected), so each update costs $O(\log n)$ time and new nodes.
- **Node copying.** For partial persistence, the [node copying](/node-copying/) method of Driscoll, Sarnak, Sleator and Tarjan gives a red-black tree with $O(1)$ amortized new space per update instead of $O(\log n)$. Sarnak and Tarjan used it for [planar point location](/planar-point-location/) in $O(n)$ space, see [Sarnak-Tarjan point location](/sarnak-tarjan-point-location/).
- **Join-based trees.** Union, intersection and difference of two sets can be written with split and join, all with path copying, so that the inputs stay valid; see [join-based tree algorithms](/join-based-tree-algorithms/).
- **Augmented nodes.** A node can store the size or a sum of its subtree. The value depends only on the subtree, so it is computed once in NEW-NODE and is right in every version that shares the node. With sizes, each version supports rank and selection queries, as in an [order-statistic tree](/order-statistic-tree/).

## When to use it

Use a persistent search tree when a program needs many versions of an ordered set that differ by a few updates each: snapshots of a database index, the states of a search algorithm, the sets in a sweep line algorithm that later queries must reach, or the values of a functional program. Use a balanced variant unless the update order is known to be random. If only the newest version is ever needed, an ephemeral balanced tree uses less memory and is faster.

## Pitfalls

- **Writing to a node on the path.** Setting $t.left \gets$ INSERT$(t.left, k)$, as an ephemeral insert does, changes a node that old versions share. Every change must go through NEW-NODE, as in lines L21 and L22.
- **Copying for nothing.** An insert of a present key or a delete of an absent key that copies the path anyway still gives a correct tree, but it wastes $h$ nodes and makes a version that is equal to the old one but not the same object. Lines L5 and L8 return the old root instead.
- **Deleting the successor in place.** The ephemeral deletion moves the successor key into $x$ and then unlinks $y$ from its parent. Both are writes to old nodes. Line L13 makes a new node for the place of $x$ and copies the path down to $y$ instead.
- **Recursion on a tall tree.** A recursive INSERT on a tree built from sorted keys uses $n$ levels of the call stack. The procedures above use a loop and an explicit path.
- **Parent pointers.** A node with a parent pointer cannot be shared, because in different versions it has different parents. Persistent trees have no parent pointers; the path from DESCEND plays their role.

## Implementations

## History

Search trees that copy the search path are the natural form of a search tree in a functional language, where no value changes, and they were in use before persistence had a theory. Sarnak and Tarjan used persistent search trees for planar point location in 1986, with a method that adds $O(1)$ amortized space per update. Driscoll, Sarnak, Sleator and Tarjan described path copying, the fat node method and node copying for general linked structures in 1989. Okasaki's book of 1998 uses the binary search tree with path copying as its first example of a persistent tree.

## References
