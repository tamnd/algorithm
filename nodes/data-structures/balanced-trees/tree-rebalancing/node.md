---
tag: JJEC3Y
kind: concept
slug: tree-rebalancing
name: Tree rebalancing
aliases:
- rebalancing
area: data-structures/balanced-trees
level: intro
summary: Restoring a tree's balance invariant after an insertion or deletion, typically by a constant number of rotations along the path to the root.
prereqs: [tree-rotation, balanced-binary-search-tree]
see_also: [avl-tree, red-black-tree, scapegoat-tree, weight-balanced-tree, treap, splay-tree, wavl-tree, two-three-four-tree]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13, Red-Black Trees (Section 13.2, rotations; Sections 13.3 and 13.4, the fixups) and Chapter 18, B-Trees
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.3, Balanced Trees (single and double rotations after insertion, and the discussion of deletion)
  - paper: Igal Galperin and Ronald L. Rivest, Scapegoat trees, Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms, 1993
    locator: pages 165 to 174, rebuilding a subtree into a perfectly balanced tree
  - paper: doi:10.1145/2689412
    title: Bernhard Haeupler, Siddhartha Sen and Robert E. Tarjan, Rank-balanced trees, ACM Transactions on Algorithms 11(4), 2015
    locator: amortized O(1) rebalancing steps and the comparison of AVL, red-black and WAVL rebalancing
---

Tree rebalancing is the work a [balanced binary search tree](/balanced-binary-search-tree/) does after an insertion or a deletion to restore its balance rule. The update itself is the one of a plain [binary search tree](/binary-search-tree/); it can break the rule only at the nodes on the path from the changed place to the root. Rebalancing walks along that path, bottom-up or top-down, and repairs each node it finds broken with local steps: [rotations](/tree-rotation/), which change the shape and keep the key order, and changes to the balance data stored in the nodes, such as colors, heights or ranks. Some trees instead rebuild a whole subtree at once. The schemes differ in how many rotations they need: AVL insertion needs at most one single or double rotation, red-black insertion at most two and deletion at most three, and a scapegoat tree uses no rotations at all.

## In plain words

A balanced tree has a rule that keeps it short, for example "the two sides of every node have almost the same height". Adding or removing a key changes the tree in one spot, and the rule may now fail at that spot or at the nodes above it.

To fix it, go up from the changed spot. At each node, check the rule. If it holds, update the stored numbers, such as heights or colors. If it fails, turn a few nodes around by rotations, which lift one side and lower the other while keeping the keys in order. Often one fix is enough and the walk can stop. Some trees do something else: when a part of the tree gets too lopsided, they take all its keys and build that part again from scratch.

## The idea

**Where the rule can break.** An insertion adds a leaf and a deletion removes a node with at most one child (after swapping with the successor). Every balance rule in common use is local: it compares data of a node with data of its children, such as heights, sizes or colors. That data changes only at the ancestors of the changed place. So only the $O(h)$ nodes of one path need to be checked, and for a tree of height $O(\log n)$ the checks take $O(\log n)$ time.

**Local repair by rotation.** A rotation at a node moves one child up and the node down, changes the subtrees of only two nodes, and keeps the in-order sequence. A double rotation does this twice to lift a grandchild two levels. Rotations repair a height difference of 2 in an AVL tree, a red node with a red child in a red-black tree, a priority that is out of heap order in a [treap](/treap/), and a size imbalance in a [weight-balanced tree](/weight-balanced-tree/). Because only two nodes get new children, any data computed from the children, such as heights or subtree sizes, is fixed in $O(1)$ time per rotation.

**Changing the balance data.** Many steps change no pointers at all. An AVL tree updates heights or [balance factors](/balance-factor/), a red-black tree recolors nodes, and a [WAVL tree](/wavl-tree/) promotes or demotes ranks. These steps can move a problem one level up, so they can repeat along the path, but each is $O(1)$ work.

**Bottom-up and top-down.** Bottom-up rebalancing makes the change at the bottom and repairs on the way back to the root, using parent pointers or a stack of the path; CLRS's red-black fixups and AVL insertion work this way. Top-down rebalancing prepares each node on the way down so that the change at the bottom cannot break anything above, as in the [2-3-4 tree](/two-three-four-tree/) and the [top-down red-black deletion](/red-black-tree-deletion/). Top-down passes need no stack and suit concurrent trees, but they often do more rotations than needed.

**Partial rebuilding.** A [scapegoat tree](/scapegoat-tree/) stores no balance data. When an insertion makes a path too long, it finds an ancestor whose subtree is too lopsided in size and rebuilds that subtree into a perfectly balanced tree, in time linear in its size. The cost is high once in a while, but the amortized cost per update is $O(\log n)$.

**Counting the work.** Three measures matter. The number of nodes visited is $O(\log n)$ for all the schemes above. The number of rotations, or structural changes, matters when changes are costly, as in persistent trees or trees on disk:

| tree | rotations per insertion | rotations per deletion | balance-data changes |
|---|---|---|---|
| [AVL tree](/avl-tree/) | at most 2 (one single or double) | $O(\log n)$ worst case | $O(\log n)$ worst case |
| [red-black tree](/red-black-tree/), bottom-up | at most 2 | at most 3 | $O(1)$ amortized |
| [WAVL tree](/wavl-tree/) | at most 2 | at most 2 | $O(1)$ amortized |
| [treap](/treap/) | fewer than 2 expected | fewer than 2 expected | none |
| [scapegoat tree](/scapegoat-tree/) | none, rebuilds instead | none, rebuilds instead | none stored |
| [splay tree](/splay-tree/) | $O(\log n)$ amortized | $O(\log n)$ amortized | none stored |

The amortized bounds for colors and ranks are for sequences of updates that start from an empty tree.

## Examples

**AVL insertion.** Insert 10, 20, 30 into an empty AVL tree. After 30, the root 10 has [balance factor](/balance-factor/) $+2$, and its right child 20 has $+1$: the same sign, so one left rotation at 10 gives 20 with children 10 and 30. The subtree has the height it had before the insertion, so nothing above it changes, and the walk stops.

**A double rotation.** Insert 10, 30, 20. Now the root 10 has balance factor $+2$ and its right child 30 has $-1$: the signs differ, the long subtree is the inner one, and a single rotation would only move it. A right rotation at 30 and then a left rotation at 10 give 20 with children 10 and 30.

**Recoloring that moves up.** In a red-black tree, insert a red node whose parent and uncle are red. Recoloring the parent and uncle black and the grandparent red fixes this level, but the grandparent may now have a red parent, so the check moves two levels up. No pointer changes until the walk meets a black uncle, where one or two rotations end it.

**Rebuilding.** In a scapegoat tree with $\alpha = 2/3$, insert 1, 2, 3, 4, 5 in this order. The tree is a chain. After 5, the new node has depth 4, more than $\log_{3/2} 5 \approx 3.97$, so the insertion looks for a scapegoat. Going up from 5, the node 2 is the first whose right subtree is too big: 3 of its 4 nodes, more than $\frac23 \cdot 4$. Its subtree is rebuilt as the balanced tree with root 4, left child 3 (with left child 2) and right child 5, and the height drops from 5 to 4.

## Where it is used

- Every balanced search tree in libraries rebalances after updates: `std::map` in C++ libraries and Java's `TreeMap` use bottom-up red-black rebalancing.
- [B-trees](/b-tree/) rebalance by splitting and merging nodes, which is the same idea with wide nodes; the [red-black correspondence](/red-black-correspondence-with-2-3-4-trees/) shows that red-black rebalancing is B-tree rebalancing written in binary.
- [Order-statistic trees](/order-statistic-tree/) and other augmented trees rely on rebalancing being local, so that their extra fields can be updated in each rotation.
- Persistent and functional trees prefer schemes with few changes per update, since each changed node is copied.
- Concurrent trees prefer top-down or relaxed rebalancing, in which the repair is done later or by other threads, so that locks are held for a short time.

## References
