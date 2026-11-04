---
tag: 0AZZFQ
kind: data-structure
slug: two-three-four-tree
name: 2-3-4 tree
aliases:
- 2-4 tree
area: data-structures/balanced-trees
level: core
summary: A perfectly balanced search tree with nodes of 2, 3 or 4 children; insertion splits full nodes on the way down.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, two-three-tree]
see_also: [red-black-tree, red-black-correspondence-with-2-3-4-trees, b-tree, two-three-tree, left-leaning-red-black-tree, red-black-tree-deletion]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18, B-Trees (B-TREE-INSERT with B-TREE-SPLIT-CHILD, and top-down deletion; a 2-3-4 tree is the B-tree with minimum degree t = 2)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (2-3-4 trees in the exercises and the discussion of top-down insertion)
  - paper: doi:10.1109/SFCS.1978.3
    title: Leo J. Guibas and Robert Sedgewick, A dichromatic framework for balanced trees, FOCS 1978
    locator: the 2-3-4 view of red-black trees and top-down insertion
  - paper: doi:10.1007/BF00289509
    title: Rudolf Bayer, Symmetric binary B-trees, Acta Informatica 1, 1972
    locator: the binary form of B-trees of order 4
---

A 2-3-4 tree is a search tree in which each node holds one, two or three keys and has two, three or four children (a *2-node*, *3-node* or *4-node*), and all leaves are at the same depth. It is the B-tree of minimum degree 2. Insertion and deletion can work *top-down*, in one pass from the root: on the way down, an insertion splits each 4-node it meets, so the leaf at the bottom has room for the new key; a deletion makes each node it enters hold at least two keys, so the key can leave the leaf. The height is between $\log_4(n + 1)$ and $\lg(n + 1)$, so search, insertion and deletion take $\Theta(\log n)$ time in the worst case. Each 2-3-4 tree is the same thing as a [red-black tree](/red-black-tree/), written with binary nodes (see [the correspondence](/red-black-correspondence-with-2-3-4-trees/)).

## In plain words

A [2-3 tree](/two-three-tree/) splits a node only after a key has made it too full, and the split can go back up to the top. A 2-3-4 tree is more careful. It allows nodes with up to three keys, and on the way down to insert, it splits every node that already has three keys. Then the node at the bottom always has room, and nothing needs to go back up.

Deletion works the same way in reverse. On the way down, each node gets a second key from a neighbor or from its parent before the walk enters it. At the bottom, a key can leave without emptying its node.

The tree grows only when the top node splits and shrinks only when the top node empties. So all leaves stay at the same depth.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on a set of keys from a totally ordered universe, with the keys in order on request. Insert returns false if the key is present, and delete returns false if it is absent.

## Representation

A node has a sorted list of 1 to 3 keys $x_0 < x_1 < \dots$ and, unless it is a leaf, one more child than keys. The child $c_i$ holds the keys between $x_{i-1}$ and $x_i$. Every leaf is at the same depth. The tree stores the root and the number of keys. A node with $j$ keys can be an array of 3 keys and 4 child pointers, so all nodes have one size.

The rules are:

1. (B1) Each node has 1, 2 or 3 keys, in increasing order.
2. (B2) An internal node with $j$ keys has $j + 1$ children.
3. (B3) The keys are in search-tree order.
4. (B4) All leaves are at the same depth.

## Operations

Indices start at 0. SPLIT-CHILD and MERGE are the two local steps; FILL chooses between a borrow and a merge.

```pseudo id=main
INSERT(T, k)
L1  if T.root = nil then T.root ← a leaf with the key k; return true
L2  if T.root is a 4-node then T.root ← a node with no key and the one child T.root; SPLIT-CHILD(T.root, 0)
L3  t ← T.root
L4  loop
L5      i ← the number of keys of t that are less than k
L6      if i < |t.keys| and t.key[i] = k then return false
L7      if t is a leaf then insert k into t.keys at position i; return true
L8      if t.child[i] is a 4-node then SPLIT-CHILD(t, i); if k = t.key[i] then return false; if k > t.key[i] then i ← i + 1
L9      t ← t.child[i]

SPLIT-CHILD(t, i)                          ▷ t is not a 4-node; c = t.child[i] has keys a < b < d
L10 c ← t.child[i]; make a 2-node with a and the two left children of c, and a 2-node with d and the two right children
L11 insert b into t.keys at position i; replace child i of t by the two new nodes

DELETE(T, k)
L12 t ← T.root
L13 loop                                   ▷ t is the root or has at least 2 keys
L14     i ← the number of keys of t that are less than k
L15     if t is a leaf then remove k from t.keys if it is there; exit the loop
L16     if i < |t.keys| and t.key[i] = k then
L17         if t.child[i] has ≥ 2 keys then p ← the largest key below t.child[i]; t.key[i] ← p; k ← p; t ← t.child[i]
L18         else if t.child[i + 1] has ≥ 2 keys then s ← the least key below t.child[i + 1]; t.key[i] ← s; k ← s; t ← t.child[i + 1]
L19         else MERGE(t, i); t ← t.child[i]
        else
L20         if t.child[i] is a 2-node then i ← FILL(t, i)
L21         t ← t.child[i]
L22 if T.root has no key then T.root ← its only child, or nil if it is a leaf

FILL(t, i)                                 ▷ t.child[i] is a 2-node; returns the child that now covers its range
L23 if i > 0 and t.child[i − 1] has ≥ 2 keys then move t.key[i − 1] to the front of t.child[i], the last key of t.child[i − 1] up into t.key[i − 1], and the last child of t.child[i − 1] to the front of t.child[i]; return i
L24 if t.child[i + 1] exists and has ≥ 2 keys then do the mirror image of line L23; return i
L25 if t.child[i + 1] exists then MERGE(t, i); return i else MERGE(t, i − 1); return i − 1

MERGE(t, i)                                ▷ t.child[i] and t.child[i + 1] are 2-nodes
L26 t.child[i] ← one node with the keys of t.child[i], then t.key[i], then the keys of t.child[i + 1], and the children of both; remove t.key[i] and t.child[i + 1] from t
```

CONTAINS is the search of a multiway tree: at each node, find the first key that is not less than $k$; stop if it equals $k$, else go to the child at that position.

**Insert.** Line L2 is the only place where the tree grows: a full root splits, and all leaves move one level down together. Line L8 keeps the invariant that $t$ is not a 4-node, so the split of a child always has room for the middle key in $t$. At the leaf, line L7 has room.

**Delete.** The invariant is that $t$ is the root or has at least 2 keys. Then a merge below $t$ can take a key from $t$, and at the leaf, line L15 can remove a key and leave at least one. An internal key is replaced by its predecessor or successor from a child that can spare a key (lines L17 and L18); if neither child can, the key moves down into a merged 4-node (line L19). Line L22 is the only place where the tree shrinks.

## Example

Insert 50, 20, 80, 10, 30, 60, 90, 40, 70, 25, the same keys as on the [2-3 tree](/two-three-tree/) page. A node is written as its keys in brackets, with its children after it in parentheses.

| step | what happens | tree |
|---|---|---|
| 50, 20, 80 | all go into the root leaf | [20 50 80] |
| 10 | line L2 splits the full root | [50] ([10 20], [80]) |
| 30, 60, 90 | go into leaves | [50] ([10 20 30], [60 80 90]) |
| 40 | line L8 splits [10 20 30]; 40 goes right of 20 | [20 50] ([10], [30 40], [60 80 90]) |
| 70 | line L8 splits [60 80 90]; 70 goes left of 80 | [20 50 80] ([10], [30 40], [60 70], [90]) |
| 25 | line L2 splits the full root; 25 goes into [30 40] | [50] ([20] ([10], [25 30 40]), [80] ([60 70], [90])) |

The 2-3 tree with the same keys also has height 3, but it splits at the bottom: after 25 it has [20 30] where this tree has [20] with the leaf [25 30 40].

Now delete 10, 50, 90, 20, 40.

| step | what happens | tree |
|---|---|---|
| delete 10 | [20] is a 2-node and its sibling [80] too: line L25 merges them with 50 into [20 50 80], and the root empties. [10] is a 2-node and its right sibling [25 30 40] can spare a key: line L24 moves 20 down and 25 up. Line L15 removes 10, and line L22 drops the empty root | [25 50 80] ([20], [30 40], [60 70], [90]) |
| delete 50 | 50 is in the root; the left child [30 40] has 2 keys, so line L17 copies its largest key 40 into the root and removes it from the leaf | [25 40 80] ([20], [30], [60 70], [90]) |
| delete 90 | [90] is a 2-node; its left sibling [60 70] can spare a key: line L23 moves 80 down and 70 up | [25 40 70] ([20], [30], [60], [80]) |
| delete 20 | [20] and its sibling [30] are 2-nodes: line L25 merges them with 25 | [40 70] ([20 25 30], [60], [80]) then [40 70] ([25 30], [60], [80]) |
| delete 40 | 40 is in the root; the left child [25 30] has 2 keys: line L17 copies 30 up | [30 70] ([25], [60], [80]) |

## Correctness

The proof checks each local step. A split takes a 4-node whose parent is not full and makes two 2-nodes and one more key in the parent, with the search order and all leaf depths unchanged. A borrow moves one key through the parent and one child across, and a merge is a split in reverse. The insertion keeps "$t$ is not a 4-node" as it goes down, and the deletion keeps "$t$ is the root or has at least 2 keys", so each split or merge has room. The tree changes height only at the root, where all leaves move together. The full proof is in the proofs folder.

## Complexity

A tree of height $h$ (nodes on a root-to-leaf path) has at least $2^h - 1$ keys, when all nodes are 2-nodes, and at most $4^h - 1$, when all are 4-nodes. So $\log_4(n + 1) \le h \le \lg(n + 1)$. Each operation goes down one path, with $O(1)$ work per level: one split at most, or one borrow or merge, and a search among at most three keys. A deletion of an internal key also walks to the predecessor or successor, which is the same path continued. So all three operations take $\Theta(\log n)$ time in the worst case and $O(1)$ extra space, since the loops need no stack. The tree uses $\Theta(n)$ space.

An insertion can split a node at every level, but over a sequence of insertions into an empty tree the splits are $O(1)$ amortized per insertion: each split makes one more node, and the number of nodes is at most $n$.

## Variants

- **Bottom-up updates.** Insert into the leaf and split the overfull nodes on the way back up, as in a [2-3 tree](/two-three-tree/). This does fewer splits, since it splits only nodes that overflow.
- **Red-black trees.** A 2-3-4 tree written with binary nodes is a [red-black tree](/red-black-tree/): a 3-node becomes a black node with one red child and a 4-node a black node with two red children. Guibas and Sedgewick gave red-black trees in this view; top-down insertion in a 2-3-4 tree is top-down insertion in a red-black tree.
- **B-trees.** The [B-tree](/b-tree/) of minimum degree $t$ has nodes with $t - 1$ to $2t - 1$ keys; the 2-3-4 tree is the case $t = 2$, and the code above is the CLRS B-tree code at that degree. Large $t$ suits disks, where one node fills one block.
- **(a, b)-trees.** Nodes have between $a$ and $b$ children. With $b \ge 2a$, the amortized number of splits and merges per update is $O(1)$, even with deletions; the 2-3-4 tree is the (2, 4)-tree.
- **2-3 trees and LLRB trees.** The [left-leaning red-black tree](/left-leaning-red-black-tree/) can model the 2-3 tree or the 2-3-4 tree, depending on where the color flip is placed.

## When to use it

Use a 2-3-4 tree as a teaching model for red-black trees, or as an in-memory B-tree when a one-pass update matters, for example with locks taken top-down in a concurrent tree, where a node can be unlocked as soon as the step below it cannot reach back up. For a plain in-memory ordered set, a red-black or [AVL tree](/avl-tree/) uses less code; with large nodes on disk, use a B-tree with a large degree.

## Pitfalls

- **Splits for a key that is already there.** Top-down insertion splits full nodes before it knows whether the key is present. Inserting 2 into [1 2 3] returns false but leaves [2] ([1], [3]). The tree is still valid, but code that expects an unchanged tree after a failed insert must search first.
- **Merges for a key that is absent.** In the same way, a deletion of an absent key can merge and borrow on the way down: deleting 5 from [2] ([1], [3]) gives [1 2 3].
- **The middle key after a split.** After SPLIT-CHILD at line L8, the key $t.key[i]$ is new, and $k$ must be compared with it again: it may be equal, or $k$ may belong to the right half.
- **The replacement key.** At line L17 the predecessor must come from the subtree of $t.child[i]$, which has at least 2 keys; taking it from a 2-node child would empty a leaf below without a fill.
- **The empty root.** A merge at a root with one key leaves a root with no keys and one child; line L22 removes it. Forgetting this breaks the next search, which reads a node with no keys.

## Implementations

## History

Rudolf Bayer and Edward McCreight described B-trees in 1970 to 1972, and the 2-3-4 tree is the B-tree of order 4. Bayer (1972) gave the *symmetric binary B-tree*, the binary form of this tree, and Guibas and Sedgewick (1978) recast it with red and black colors, with top-down insertion and deletion in the 2-3-4 view. The top-down form of B-tree insertion and deletion in CLRS, with SPLIT-CHILD on the way down, is the form used here.

## References
