---
tag: 6XA3BY
kind: technique
slug: path-copying
name: Path copying
aliases:
- path-copying method
- copy-on-write path
area: data-structures/persistent-structures
level: core
summary: To update a node, copy the nodes on the root-to-node path and share everything else.
prereqs: [binary-search-tree, full-persistence]
see_also: [node-copying, fat-node, persistent-binary-search-tree, persistent-segment-tree, persistent-stack, persistent-vector, dsst-persistence-theorem, hash-consing]
sources:
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: pages 86 to 124, the introduction (path copying and its earlier users, and its cost of O(log n) space per update in a balanced tree)
  - paper: doi:10.1145/6138.6151
    title: Neil Sarnak and Robert E. Tarjan, Planar point location using persistent search trees, Communications of the ACM 29(7), 1986
    locator: pages 669 to 679, the section on persistent search trees (path copying, then the improvement to O(1) amortized space)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence, Section 2.1 (lists, where append copies its first argument) and Section 2.2 (binary search trees, where insert copies the search path)
  - paper: doi:10.1145/800017.800517
    title: Eugene W. Myers, Efficient applicative data types, Proceedings of the 11th ACM Symposium on Principles of Programming Languages (POPL 1984)
    locator: pages 66 to 75 (applicative AVL trees and arrays by copying the access path)
---

Path copying is a way to make a tree-shaped pointer structure [fully persistent](/full-persistence/): to change a node, copy that node and every node on the path from the root to it, and let the copies point to the old, unchanged subtrees. The new root is the root of the new version, and the old root still describes the old version in full. In a balanced tree of $n$ nodes an update costs $O(\log n)$ extra time and space, and queries run at full speed on every version. It is the method behind most [purely functional data structures](/purely-functional-data-structure/), from the [persistent stack](/persistent-stack/) to the [persistent vector](/persistent-vector/).

## In plain words

Think of a family tree drawn on paper that many people share. You want to correct one name, but others still need the old drawing. So you redraw the box with the new name. Its parent box must point to the new box, so you redraw the parent too, and its parent, up to the top. Every box that is not on this path is the same in both drawings, so you do not redraw it. Your new top box leads to the new tree, and the old top box still leads to the old one.

The work is the length of one path from the top, not the size of the whole tree. If the tree is balanced, that path is short.

## When it applies

- **Each node has one incoming pointer.** The structure is a tree, or a forest with an array of roots: a node is reached from exactly one parent. Then a changed node has only one pointer to fix, in its parent, and the copying stops at the root. With parent pointers or other back pointers, a change propagates everywhere (see Pitfalls).
- **Updates are local.** An update changes $O(1)$ nodes, or a set of nodes close to one root-to-leaf path, as the insertion into a [binary search tree](/binary-search-tree/) or the point update of a [segment tree](/segment-tree/) does.
- **The paths are short.** The cost of an update is the length of the copied path. Path copying is cheap for balanced trees of depth $O(\log n)$ and for wide trees such as the 32-way trie of a [persistent vector](/persistent-vector/), and it is costly for a long list.
- **Old versions are reached through their roots.** Each version is named by its root pointer, which the program keeps in a variable or in an array of roots indexed by version.

## The template

The template changes one target node $x$ in the version with root $r$ and returns the root of the new version. CHILD-TOWARD and CHANGE are the holes.

```pseudo id=main
PATH-COPY(v, x)                          ▷ v is a node of the old version; returns a node of the new version
L1  if v = x then
L2      return CHANGE(a copy of v)       ▷ hole: the update of the target node
L3  c ← CHILD-TOWARD(v, x)               ▷ hole: the child of v whose subtree holds x
L4  c′ ← PATH-COPY(c, x)
L5  v′ ← a copy of v                     ▷ same fields, same children
L6  in v′, replace the pointer to c by c′
L7  return v′

NEW-VERSION(roots, i, x)
L8  roots[m + 1] ← PATH-COPY(roots[i], x); m ← m + 1
```

Lines L1 and L2 make the change on a fresh copy of the target, so the old target is untouched. Lines L5 and L6 copy each ancestor and redirect one child pointer to the new copy below it. All other child pointers of the copies point to the old subtrees, which the new version now shares with the old one. Line L8 stores the new root, and any $i \le m$ can be the version to update, which gives full persistence.

Insertion of a new leaf fits the template with CHANGE creating the leaf below the target. An update that rebalances, as in a [red-black tree](/red-black-tree/) or an [AVL tree](/avl-tree/), changes nodes on the search path and the siblings that rotations move. Each changed node is copied once, and each node that points to a changed node is also copied.

**Why it is correct.** No line writes a field of a node that exists before the call: lines L2 and L5 write only into fresh copies. So every node reachable from an old root keeps its fields, and every old version is unchanged. In the new version, the path from the new root to the copy of $x$ consists of the copies, and every other subtree is an old subtree that the update does not change. So the new version is exactly the old one with the change applied.

**Cost.** If the target is at depth $d$, PATH-COPY makes $d + 1$ copies, each of $O(1)$ size, so the update takes $O(d + 1)$ time and space, plus the cost of CHANGE. In a balanced tree, $d = O(\log n)$. Queries are unchanged: they run on the tree of one version as on an [ephemeral](/ephemeral-data-structure/) tree.

## Classic examples

### A trace on a binary search tree

Insert 5, 3, 8, 1, 4, 7, 9 into an empty binary search tree. The result, version 1, is the perfect tree of 7 nodes with root 5, children 3 and 8, and leaves 1, 4, 7 and 9. Now insert 6 into version 1 with path copying.

| step | node | action |
|---|---|---|
| 1 | 5 | $6 > 5$, go right; later copy 5 as $5'$ |
| 2 | 8 | $6 < 8$, go left; later copy 8 as $8'$ |
| 3 | 7 | $6 < 7$ and the left child is empty: the target |
| 4 | 7 | copy 7 as $7'$ with the new leaf 6 as its left child |
| 5 | 8 | $8'$ has left child $7'$ and right child 9 (shared) |
| 6 | 5 | $5'$ has left child 3 (shared) and right child $8'$ |

Version 2 has root $5'$ and 8 nodes. Memory holds 11 nodes in total: the 7 old ones and the 4 new ones $5'$, $8'$, $7'$ and $6$. The subtree $\{3, 1, 4\}$ and the leaf 9 belong to both versions. Two full copies would need $7 + 8 = 15$ nodes. In a perfect tree of $2^{20} - 1$ nodes, an insertion copies 20 nodes and adds one leaf, against about a million nodes for a full copy.

### Other examples, simple to hard

- **[Persistent stack](/persistent-stack/).** The stack is a linked list read from its head. Push makes one new cell that points to the old head, and pop returns the next pointer. The copied path has length 0 or 1, so each operation is $O(1)$.
- **Append of two lists.** In a functional language, `xs ++ ys` copies every cell of `xs` and shares `ys` (Okasaki, Section 2.1). The path to the change is the whole first list, which shows the limit of the method.
- **[Persistent binary search tree](/persistent-binary-search-tree/) and [persistent red-black tree](/persistent-red-black-tree/).** Insert and delete copy the search path and the $O(1)$ nodes changed by rotations: $O(\log n)$ time and space per update.
- **[Persistent segment tree](/persistent-segment-tree/).** A point update copies the $O(\log n)$ nodes from the root to one leaf. One version per prefix of an array gives the classic solution of the [range k-th smallest query](/range-kth-smallest-query/).
- **[Persistent treap](/persistent-treap/) and [persistent trie](/persistent-trie/).** The same idea, on a tree whose shape is set by random priorities or by the bits of the keys.
- **[Persistent vector](/persistent-vector/).** A 32-way tree of arrays: an update copies $\lceil \log_{32} n \rceil$ arrays of 32 slots.
- **[Binary random-access list](/binary-random-access-list/).** An update of the element at an index copies the path inside one complete tree and the list cells before that tree.

## Variations

- **Node copying.** [Node copying](/node-copying/) gives each node a few spare fields, so that most changes write into a spare field instead of copying. A copy happens only when the spare fields are full, and the copying stops early. This reduces the space of an update to $O(1)$ amortized for structures of bounded in-degree. Sarnak and Tarjan used it to bring the space of a persistent red-black tree from $O(\log n)$ to $O(1)$ amortized per update.
- **Fat nodes.** The [fat node](/fat-node/) method copies nothing and stores all values of each field with version stamps, at a cost of $O(\log m)$ time per access.
- **Transient (in-place) updates.** If the program knows that no one holds the old version, it can change a node in place instead of copying it. Clojure's transient vectors do this for a batch of updates. Reference counts give the same test at run time: a node with count 1 is not shared.
- **Sharing equal subtrees.** [Hash-consing](/hash-consing/) makes equal subtrees the same node, which saves space across versions that were built separately.

## Pitfalls

- **Parent pointers.** If nodes point to their parents, then a copied node needs new children that point back to it, and those need new children in turn: one change forces a copy of the whole tree. Remove parent pointers and keep the search path on a stack during the descent.
- **A write into a shared node.** Any in-place write to a node that existed before the update changes all versions that share it. All writes must go to fresh copies, including the writes of rebalancing code that was written for ephemeral trees.
- **Forgetting nodes changed by rebalancing.** A rotation changes a node off the search path, such as the sibling that moves up. It must be copied too, and so must every node that points to a copied node.
- **Long paths.** On an unbalanced tree or a list, the path can have length $\Theta(n)$, and so can each update. Use a balanced tree, or put the changes near the root, as a stack does.
- **Memory held by old roots.** Every kept root keeps its whole version alive. If old versions are no longer needed, drop their roots so that the garbage collector can free the nodes that only they use.
- **Counting the space.** Path copying uses $O(\log n)$ space per update in a balanced tree, so $m$ updates use $O(n + m \log n)$ space, not $O(n + m)$. The $O(1)$ space bound needs node copying.

## Exercises

1. Insert 2 into version 2 of the trace above, and then insert 2 into version 1. List the new nodes in each case and the nodes that the two new versions share.
2. Show that path copying on a [red-black tree](/red-black-tree/) makes $O(\log n)$ new nodes for an insertion, given that an insertion does $O(\log n)$ recolorings and at most two rotations.
3. A singly linked list keeps a pointer to its last cell for $O(1)$ append. Why does path copying cost $\Theta(n)$ for a persistent append, and which structure of this area avoids it?
4. Prove that after $m$ updates by path copying on a balanced tree, the total number of nodes in memory is at most $n_0 + m(c \log n + 1)$ for a constant $c$, where $n_0$ is the size of the first version and $n$ the largest size.

## References
