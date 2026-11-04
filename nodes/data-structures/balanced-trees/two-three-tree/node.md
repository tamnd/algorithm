---
tag: 3W4BM4
kind: data-structure
slug: two-three-tree
name: 2-3 tree
aliases:
- 2,3-tree
area: data-structures/balanced-trees
level: core
summary: A perfectly balanced search tree whose internal nodes have 2 or 3 children, with all leaves at the same depth.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, balanced-binary-search-tree]
see_also: [two-three-four-tree, b-tree, left-leaning-red-black-tree, red-black-tree, aa-tree, red-black-correspondence-with-2-3-4-trees]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.3, Balanced Search Trees (2-3 search trees, insertion by splitting temporary 4-nodes)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (2-3 trees) and Section 6.2.4, Multiway Trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 18, B-Trees (insertion by splitting, deletion by borrowing and merging, and the chapter notes on 2-3 trees)
---

A 2-3 tree is a search tree in which each node holds one key and has two children (a *2-node*) or holds two keys and has three children (a *3-node*), and all leaves are at the same depth. An insertion puts the key into a leaf; a leaf with three keys splits into two nodes and sends its middle key up to the parent, and the splits can go up to the root, where the tree grows by one level. A deletion borrows a key from a sibling or merges two nodes, and the tree loses a level only at the root. Because the leaves stay at one depth, the height is between $\log_3(n + 1)$ and $\lg(n + 1)$, and search, insertion and deletion take $\Theta(\log n)$ time in the worst case. The 2-3 tree is the B-tree of order 3, and it is the model behind the [left-leaning red-black tree](/left-leaning-red-black-tree/).

## In plain words

A binary search tree gets tall when keys arrive in a bad order, because a new key always hangs a new node below the old ones. A 2-3 tree never does that. A new key goes into a node that is already there, so the node can get fat but the tree does not get deeper.

A node may hold one key or two. When a node gets a third key, it is too fat: it breaks into two nodes of one key each, and the middle key moves up into the parent. The parent may then break too. If the top node breaks, a new top node appears above it. This is the only way the tree gets taller, and it adds a level above all leaves at the same time. So every leaf is always at the same distance from the top.

## The abstract type

A 2-3 tree implements the [ordered set](/ordered-set/): `contains(T, k)`, `insert(T, k)` and `delete(T, k)`, together with the order operations minimum, maximum, predecessor, successor and in-order iteration. With a value next to each key it is an [ordered symbol table](/ordered-symbol-table/). The keys come from a total order, and each key is in the tree at most once.

## Representation

A node $t$ has a sorted list of keys $t.keys$ and a list of children $t.kids$. A *2-node* has one key $a$ and, if it is not a leaf, two children: the left subtree holds the keys less than $a$, and the right subtree holds the keys greater than $a$. A *3-node* has keys $a < b$ and, if it is not a leaf, three children, which hold the keys less than $a$, between $a$ and $b$, and greater than $b$.

**Invariant.** (T1) Each node has one or two keys, in increasing order. (T2) An internal node with $j$ keys has $j + 1$ children, and the keys of the children lie in the ranges that its keys separate. (T3) All leaves are at the same depth.

**Height.** Write $h$ for the number of nodes on a path from the root to a leaf. Each level has at least twice and at most three times as many nodes as the level above. A tree of height $h$ has at least $2^h - 1$ keys (all 2-nodes) and at most $3^h - 1$ keys (all 3-nodes). So

$$\log_3(n + 1) \le h \le \lg(n + 1).$$

During an update a node may hold three keys (a temporary *4-node*) or zero keys (an *empty* node) for a moment. The procedures below remove these before they return.

## Operations

A search starts at the root. At a node, it compares $k$ with the one or two keys: if $k$ is equal to a key it stops, and else it goes down into the one child whose range holds $k$. It costs at most two comparisons for each level.

An insertion goes down to a leaf, puts the key there, and repairs 4-nodes on the way back up. INS returns nil, or a *split* $(m, a, b)$: a key $m$ and two nodes $a$, $b$ that replace the node, with $m$ to go into the parent.

```pseudo id=main
INSERT(T, k)
L1  if T.root = nil then T.root ← a leaf with keys [k]; return
L2  r ← INS(T.root, k)
L3  if r = (m, a, b) then T.root ← a node with keys [m] and children [a, b]   ▷ the height grows by one

INS(t, k)                                  ▷ returns nil or a split (m, a, b)
L4  if k is a key of t then return nil
L5  if t is a leaf then put k into t.keys in order
L6  else
L7      i ← the index of the child of t whose range holds k
L8      r ← INS(t.kids[i], k)
L9      if r = nil then return nil
L10     with r = (m, a, b): put m into t.keys at position i, and replace t.kids[i] by a, b
L11 if t has three keys x < y < z then
L12     return (y, a node with key x and the first two children, a node with key z and the last two children)
L13 return nil
```

A deletion first moves the key to a leaf: if $k$ is in an internal node, it is replaced by its successor, the least key of the next child to the right, and the successor is deleted from that subtree instead. Then it removes the key from the leaf. If the leaf becomes empty, the parent repairs it with FIX, and an empty internal node is repaired the same way one level up.

```pseudo id=delete
DELETE(T, k)
L14 if T.root = nil then return
L15 DEL(T.root, k)
L16 if T.root has no keys then T.root ← its only child, or nil if it is a leaf   ▷ the height shrinks by one

DEL(t, k)                                  ▷ may leave t with no keys
L17 if t is a leaf then remove k from t.keys if it is there; return
L18 i ← the index of the child of t whose range holds k; if k = t.keys[j] for some j then
L19     s ← the least key in the subtree t.kids[j + 1]; t.keys[j] ← s; k ← s; i ← j + 1
L20 DEL(t.kids[i], k)
L21 if t.kids[i] has no keys then FIX(t, i)

FIX(t, i)                                  ▷ c = t.kids[i] is empty: no keys and one child, or none
L22 if a sibling s next to c has two keys then
L23     move the key of t between c and s down into c, move the near key of s up into t, and move the near child of s over to c
L24 else                                   ▷ the sibling s next to c has one key
L25     merge c, the key of t between them and s into one node with two keys; remove that key and c from t
```

The cost is $O(1)$ for each level in each procedure, so each operation takes $\Theta(h) = \Theta(\log n)$ time.

## Example

Insert 50, 20, 80, 10, 30, 60, 90, 40, 70, 25 into an empty tree. A node is written as its keys in brackets, followed by its children.

| operation | what happens | tree after |
|---|---|---|
| insert 50, 20 | the root leaf takes both keys | [20 50] |
| insert 80 | the leaf [20 50 80] splits, 50 goes up into a new root | [50] ([20], [80]) |
| insert 10 | goes into the leaf [20] | [50] ([10 20], [80]) |
| insert 30 | [10 20 30] splits, 20 goes up into the root | [20 50] ([10], [30], [80]) |
| insert 60 | goes into [80] | [20 50] ([10], [30], [60 80]) |
| insert 90 | [60 80 90] splits and sends 80 up; the root [20 50 80] splits and sends 50 up into a new root | [50] ([20] ([10], [30]), [80] ([60], [90])) |
| insert 40, 70 | go into [30] and [60] | [50] ([20] ([10], [30 40]), [80] ([60 70], [90])) |
| insert 25 | [25 30 40] splits, 30 goes up into [20] | [50] ([20 30] ([10], [25], [40]), [80] ([60 70], [90])) |

The tree has ten keys and height 3. Now delete 10, 50, 90, 20 and 40.

| operation | what happens | tree after |
|---|---|---|
| delete 10 | the leaf is empty; its sibling [25] has one key, so merge: [20 25] | [50] ([30] ([20 25], [40]), [80] ([60 70], [90])) |
| delete 50 | 50 is in the root: replace it by its successor 60 and delete 60 from [60 70] | [60] ([30] ([20 25], [40]), [80] ([70], [90])) |
| delete 90 | merge [70], 80 into [70 80]; now [80] is empty, and its sibling [30] has one key, so merge again into [30 60]; the root is empty and goes away | [30 60] ([20 25], [40], [70 80]) |
| delete 20 | the leaf keeps the key 25 | [30 60] ([25], [40], [70 80]) |
| delete 40 | the leaf is empty; the sibling [70 80] has two keys, so borrow: 60 comes down, 70 goes up | [30 70] ([25], [60], [80]) |

The deletion of 90 shows the merges going up to the root, where the height goes from 3 to 2 for all leaves at the same time. The deletion of 40 shows a borrow, which ends the repair at once.

## Correctness

Each operation keeps (T1) to (T3). An insertion never changes the depth of a leaf except at line L3, which adds a new root above all of them; a split replaces a node by two nodes at the same depth, each with one key and with children whose ranges are those of the old node. A deletion changes depths only at line L16, which removes the root above all leaves. A borrow keeps the order because the key that moves down lies between the key ranges of c and s, and the moved child lies in the right range for its new parent. The full proof, with the key ranges in each case, is in the proofs folder.

## Complexity

Each of the three operations visits one node for each level, does $O(1)$ work at each node and so takes $\Theta(\log n)$ time in the worst case; the bound comes from $h \le \lg(n + 1)$. An insertion does at most $h$ splits, and a deletion at most $h$ merges and one borrow. Over a sequence of insertions only, the number of splits is less than the number of nodes made, so the amortized number of splits for each insertion is $O(1)$. The space is $\Theta(n)$: there are at most $n$ nodes.

## Variants

- **2-3-4 trees** allow nodes with three keys. Their insertion can split full nodes on the way down, in one pass. See [2-3-4 tree](/two-three-four-tree/).
- **B-trees** allow up to $2t - 1$ keys in a node, for disks and caches; a 2-3 tree is the B-tree with at most two keys in each node. See [B-tree](/b-tree/).
- **Left-leaning red-black trees** store a 2-3 tree as a binary tree: a 3-node becomes two binary nodes joined by a red link. See [left-leaning red-black tree](/left-leaning-red-black-tree/).
- **AA trees** use the mirror form, with the second key of a 3-node as a right child at the same level. See [AA tree](/aa-tree/).
- **Leaf-oriented 2-3 trees** keep all keys in the leaves, and the internal nodes hold copies of keys as guides. This is the form of B+ trees.

## When to use it

Use a 2-3 tree to learn how balanced trees work, or when you want a worst-case height bound with no rotations. In practice, a program stores the same shape as a red-black tree, because binary nodes of one size are simpler to allocate and to search. On disks, use a B-tree with many keys in each node.

## Pitfalls

- **Inserting a key that is already there.** Line L4 must stop at the first node that holds $k$. If the code adds $k$ to a leaf that holds it, a full leaf splits for no reason, and the tree holds $k$ twice.
- **Children of a split node.** At line L12, the first two children go to the left node and the last two to the right node. Giving three children to one side breaks (T2).
- **Borrowing from a sibling that is not next to $c$.** In a 3-node parent, the left child and the right child are not siblings next to each other: a borrow must go through the middle child. FIX looks only at the siblings at $i - 1$ and $i + 1$.
- **Forgetting the root.** After a deletion, the root may be empty with one child. Line L16 must remove it, or the root breaks (T1).

## Implementations

## History

John Hopcroft introduced 2-3 trees in 1970, in work that was not published at the time; Aho, Hopcroft and Ullman described them in their 1974 book, and Knuth discusses them in Section 6.2.3. Bayer and McCreight generalized the idea to B-trees in 1972. Guibas and Sedgewick (1978) showed how to store 2-3 and 2-3-4 trees as binary trees with colored links, and Sedgewick's left-leaning red-black tree (2008) uses this form for 2-3 trees.

## References
