---
tag: 3F3XMG
kind: data-structure
slug: persistent-red-black-tree
name: Persistent red-black tree
aliases:
- Okasaki red-black tree
- functional red-black tree
area: data-structures/persistent-structures
level: core
summary: A red-black tree with a purely functional balance step, giving O(log n) persistent insert and delete.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the version, N: the number of nodes made by all updates}
  time: {contains: Θ(log n), insert: Θ(log n), delete: Θ(log n)}
  space: {total: Θ(N)}
history:
  year: 1999
  people: [Chris Okasaki, Stefan Kahrs]
  note: Okasaki gave the functional insertion with a four-case balance in 1999; Kahrs gave a functional deletion in 2001.
prereqs: [red-black-tree, persistent-binary-search-tree, path-copying, tree-rotation]
see_also: [persistent-binary-search-tree, persistent-treap, persistent-dynamic-set, left-leaning-red-black-tree, red-black-tree-deletion, two-three-four-tree, purely-functional-data-structure, structural-sharing]
sources:
  - paper: doi:10.1017/S0956796899003494
    title: Chris Okasaki, Red-black trees in a functional setting, Journal of Functional Programming 9(4), 1999
    locator: the functional pearl as a whole (insertion with the balance function and its four cases)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.3 Red-Black Trees
  - paper: Stefan Kahrs, Red-black trees with types, Journal of Functional Programming 11(4), 2001
    locator: the deletion functions (balleft, balright and app) and their invariants
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 13 (Lemma 13.1, the height of a red-black tree) and Problem 13-1, Persistent dynamic sets
---

A persistent red-black tree is a [red-black tree](/red-black-tree/) whose insertion and deletion never change a node. Each update rebuilds the nodes on one search path from the bottom up, and a small function BALANCE repairs the colors on the way, so the result is a new red-black tree that shares all other nodes with the old one. Since a red-black tree with $n$ keys has height at most $2 \lg(n + 1)$, each operation takes $O(\log n)$ time in the worst case and each update makes $O(\log n)$ new nodes. Okasaki gave the insertion in 1999, and Kahrs gave a matching deletion in 2001; together they are the standard balanced tree of functional languages.

## In plain words

A red-black tree keeps itself short by coloring each node red or black and keeping two rules: a red node has no red child, and every path down from a node meets the same number of black nodes.

The usual code fixes the rules after an insert by changing colors and turning nodes in place. The persistent version cannot change nodes, so it builds new ones. On the way back up from the new leaf, at each black node, it looks at the node and the two levels below it. If it sees a red node under a red node, it builds three new nodes in a fixed shape with no such pair. There are only four bad shapes, and all four have the same repair.

Deletion works the same way with a few more shapes. Every node off the search path is shared with the old tree.

## The abstract type

A persistent red-black tree implements the [ordered set](/ordered-set/) with value semantics: `contains(T, k)`, and `insert(T, k)` and `delete(T, k)`, which return a new set and leave $T$ as it was. In-order listing, minimum, maximum, successor and predecessor work as in any search tree. With a value in each node it is a persistent ordered map. It solves the [persistent dynamic set](/persistent-dynamic-set/) problem with full persistence.

## Representation

A tree is nil or a node $\text{NODE}(c, l, x, r)$ with a color $c \in \{\text{red}, \text{black}\}$, a left subtree $l$, a key $x$ and a right subtree $r$. Nil counts as black. The fields never change after the node is made. The *black height* $\text{bh}(t)$ is the number of black nodes on any path from $t$ down to nil, counting $t$ itself when it is black; $\text{bh}(\text{nil}) = 0$.

**Invariant.** For each version $t$:

- (R1) the keys are in search-tree order;
- (R2) no red node has a red child;
- (R3) every path from a node down to nil has the same number of black nodes;
- (R4) the root is black.

Write $\text{RB}(t, h)$ when $t$ meets (R1) to (R3) with $\text{bh}(t) = h$ (the root may be red). An *infrared* tree with black height $h$, $\text{IR}(t, h)$, is a tree that meets $\text{RB}(t, h)$, or a red root whose two children meet $\text{RB}(\cdot, h)$ with any colors: it can break (R2) only at its root. BLACKEN turns the root black, and REDDEN turns a black root red; both make one new node.

## Operations

```pseudo id=main
INSERT(t, k)
L1  if CONTAINS(t, k) then return t
L2  return BLACKEN(INS(t, k))

INS(t, k)
L3  if t = nil then return NODE(red, nil, k, nil)
L4  if k < t.key then
L5      if t is black then return BALANCE(INS(t.left, k), t.key, t.right)
L6      else return NODE(red, INS(t.left, k), t.key, t.right)
L7  else                                       ▷ k > t.key
L8      if t is black then return BALANCE(t.left, t.key, INS(t.right, k))
L9      else return NODE(red, t.left, t.key, INS(t.right, k))

BALANCE(a, x, b)                               ▷ a node with a red pair below it is rebuilt
L10 if a and b are red then return NODE(red, BLACKEN(a), x, BLACKEN(b))
L11 if a and a.left are red then return NODE(red, BLACKEN(a.left), a.key, NODE(black, a.right, x, b))
L12 if a and a.right are red then return NODE(red, NODE(black, a.left, a.key, a.right.left), a.right.key, NODE(black, a.right.right, x, b))
L13 if b and b.right are red then return NODE(red, NODE(black, a, x, b.left), b.key, BLACKEN(b.right))
L14 if b and b.left are red then return NODE(red, NODE(black, a, x, b.left.left), b.left.key, NODE(black, b.left.right, b.key, b.right))
L15 return NODE(black, a, x, b)

DELETE(t, k)
L16 if not CONTAINS(t, k) then return t
L17 return BLACKEN(DEL(t, k))                   ▷ BLACKEN(nil) = nil

DEL(t, k)                                      ▷ k is a key of t
L18 if k < t.key then
L19     if t.left is black then return BAL-LEFT(DEL(t.left, k), t.key, t.right)
L20     else return NODE(red, DEL(t.left, k), t.key, t.right)
L21 if k > t.key then
L22     if t.right is black then return BAL-RIGHT(t.left, t.key, DEL(t.right, k))
L23     else return NODE(red, t.left, t.key, DEL(t.right, k))
L24 return FUSE(t.left, t.right)                ▷ k = t.key

BAL-LEFT(l, x, r)                              ▷ bh(l) = bh(r) − 1
L25 if l is red then return NODE(red, BLACKEN(l), x, r)
L26 if r is black then return BALANCE(l, x, REDDEN(r))
L27 a ← r.left                                 ▷ r is red, so a is black
L28 return NODE(red, NODE(black, l, x, a.left), a.key, BALANCE(a.right, r.key, REDDEN(r.right)))

BAL-RIGHT(l, x, r)                             ▷ bh(r) = bh(l) − 1, the mirror image
L29 if r is red then return NODE(red, l, x, BLACKEN(r))
L30 if l is black then return BALANCE(REDDEN(l), x, r)
L31 a ← l.right; return NODE(red, BALANCE(REDDEN(l.left), l.key, a.left), a.key, NODE(black, a.right, x, r))

FUSE(a, b)                                     ▷ keys of a < keys of b, bh(a) = bh(b)
L32 if a = nil then return b
L33 if b = nil then return a
L34 if a and b are red then
L35     c ← FUSE(a.right, b.left)
L36     if c is red then return NODE(red, NODE(red, a.left, a.key, c.left), c.key, NODE(red, c.right, b.key, b.right))
L37     return NODE(red, a.left, a.key, NODE(red, c, b.key, b.right))
L38 if a and b are black then
L39     c ← FUSE(a.right, b.left)
L40     if c is red then return NODE(red, NODE(black, a.left, a.key, c.left), c.key, NODE(black, c.right, b.key, b.right))
L41     return BAL-LEFT(a.left, a.key, NODE(black, c, b.key, b.right))
L42 if b is red then return NODE(red, FUSE(a, b.left), b.key, b.right)
L43 return NODE(red, a.left, a.key, FUSE(a.right, b))   ▷ a is red, b is black
```

**Insertion.** INS goes down the search path and puts a red leaf at the bottom (line L3). A red leaf keeps (R3), but it can be the red child of a red node. On the way up, each new node above a black node goes through BALANCE. If one child of the black node is red and has a red child, the three nodes involved (the black node $z$, its red child $y$ and the red grandchild $x$) are rebuilt as a red node with two black children, holding the keys of $x$, $y$ and $z$ in order and the four subtrees below them in order. Lines L11 to L14 are the four positions of the red pair, and each gives the same shape. Line L10, the case of two red children, makes the same shape by recoloring. The repaired subtree has a red root, so the problem may move up two levels, where the next BALANCE sees it. At the top, BLACKEN makes the root black, which also removes a red pair at the root.

**Deletion.** DEL goes down to the node of $k$ and replaces it by FUSE of its two children, which joins two trees of equal black height. Removing a black node makes a subtree one black level short. BAL-LEFT and BAL-RIGHT repair this on the way up: if the short side has a red root, making it black restores the height (line L25); if the sibling is black, making the sibling red lowers the other side to match, and BALANCE removes any red pair that this makes (line L26); if the sibling is red, the code moves one black node of the sibling over to the short side (line L28). The test at lines L19 and L22 decides whether the child is black: deleting from a black child makes it short, and deleting from a red child does not.

**Present and absent keys.** Lines L1 and L16 return the old tree when nothing changes. Without them the code would still give a valid tree, but it would rebuild the path and might recolor nodes for no reason.

## Example

Insert 1, 2, 3, 4, 5 into the empty tree, then delete 2. A tree is written as (left key right), a leaf as its key, nil as a dot, and each key has its color: B for black, R for red.

| version | operation | what happens | tree |
|---|---|---|---|
| $v_1$ | insert 1 | a red leaf; BLACKEN | B1 |
| $v_2$ | insert 2 | red leaf right of the black 1; no red pair | (. B1 R2) |
| $v_3$ | insert 3 | red 3 under red 2 under black 1: line L13 | (B1 B2 B3) |
| $v_4$ | insert 4 | red leaf right of the black 3 | (B1 B2 (. B3 R4)) |
| $v_5$ | insert 5 | red 5 under red 4 under black 3: line L13 gives (B3 R4 B5) | (B1 B2 (B3 R4 B5)) |
| $v_6$ | delete 2 | FUSE(B1, (B3 R4 B5)) | ((. B1 R3) B4 B5) |

The insertion of 3 in detail: INS reaches the black root 1 and goes right to the red 2, which is not black, so line L9 makes a new red 2 with the new red leaf 3 as its right child. Back at 1, line L8 calls BALANCE(nil, 1, (. R2 R3)). The right child is red with a red right child, so line L13 returns a red 2 with black children 1 and 3, and BLACKEN at line L2 makes the root black. Three new nodes are made for the final tree, and the old versions $v_1$ and $v_2$ are unchanged.

The deletion of 2 from $v_5$: the root has key 2, so line L24 calls FUSE with $a = $ B1 and $b = $ (B3 R4 B5). Here $a$ is black and $b$ is red, so line L42 makes a red 4 with left child FUSE(B1, B3) and right child B5. That inner FUSE has two black trees: $c = $ FUSE(nil, nil) $=$ nil, which is not red, so line L41 calls BAL-LEFT(nil, 1, B3). The sibling B3 is black, so line L26 calls BALANCE(nil, 1, R3), which finds no red pair and returns (. B1 R3). The result is the red 4 with children (. B1 R3) and B5, and BLACKEN gives $v_6$. Each path has black height 2, as before. The version $v_5$ still has its root 2.

## Correctness

The proof rests on four lemmas about black heights. If $a$ and $b$ are infrared with black height $h$ and at least one of them is a red-black tree, BALANCE$(a, x, b)$ is a red-black tree of black height $h + 1$. INS on a black root keeps $\text{RB}$ with the same black height, and INS on a red root gives an infrared tree. If $\text{bh}(l) = \text{bh}(r) - 1$, with $l$ infrared and $r$ a red-black tree, BAL-LEFT gives an infrared tree of black height $\text{bh}(r)$, and a red-black tree when $r$ is black. FUSE of two red-black trees of black height $h$ is infrared of black height $h$, and red-black when both roots are black. From these, DEL on a black root gives an infrared tree one black level lower, and DEL on a red root keeps the black height and (R2). BLACKEN at the root then restores (R4). The full proof is in the proofs folder.

## Complexity

| operation | time | new nodes |
|---|---|---|
| contains | $\Theta(\log n)$ worst case | none |
| insert | $\Theta(\log n)$ worst case | $O(\log n)$ |
| delete | $\Theta(\log n)$ worst case | $O(\log n)$ |

The model is the [comparison model](/comparison-model/) for keys, with one unit for each node made or read. A red-black tree with $n$ keys has height at most $2 \lg(n + 1)$ (CLRS Lemma 13.1), so each search path has $O(\log n)$ nodes. INS does one call per level of the search path, and each call makes at most three nodes in BALANCE. DEL also does one call per level, and FUSE then follows the right spine of the left child and the left spine of the right child, one level per call, so it too makes $O(1)$ nodes per level. The lower bound $\Omega(\log n)$ for contains is the comparison bound of search; for insert and delete it comes from the search for the key.

**Space.** Each version shares all nodes off its search path with the version it came from. So $m$ updates on sets of at most $n$ keys make $O(m \log n)$ nodes in total.

## Variants

- **Okasaki's original insertion.** The paper of 1999 has only the four cases of lines L11 to L14 and no line L10. Both versions are correct. Line L10 recolors a black node with two red children even when there is no red pair. Kahrs' code uses this form of BALANCE, so one BALANCE serves both updates here.
- **Other functional deletions.** Other authors give deletions with a temporary "double black" color and a few more cases. Another route is to delete by [join-based tree algorithms](/join-based-tree-algorithms/): split at the key and join the two halves.
- **Left-leaning red-black trees.** The [left-leaning red-black tree](/left-leaning-red-black-tree/) allows a red link only on the left, which halves the number of cases. It can be made persistent by path copying in the same way.
- **Node copying.** For partial persistence, the method of Driscoll, Sarnak, Sleator and Tarjan stores each change in old nodes with a version stamp, and gets $O(1)$ amortized new space per update instead of $O(\log n)$.

## When to use it

Use a persistent red-black tree when you need an ordered set or map with worst-case $O(\log n)$ operations and cheap snapshots, in a functional language or in any program that keeps many versions. Many functional libraries use a balanced tree of this kind or a weight-balanced tree. If expected bounds are enough and you need split and merge, a [persistent treap](/persistent-treap/) is shorter. If only the newest version matters, an ephemeral red-black tree does fewer allocations.

## Pitfalls

- **Forgetting BLACKEN at the root.** INS can return a red root with a red child. Without line L2 the tree breaks (R2) at the root, and the next INS may not repair it, because BALANCE only runs at black nodes.
- **Calling BALANCE at a red node.** Lines L6 and L9 make a red node without BALANCE. The red pair below a red node is repaired one level higher, at its black parent; trying to repair it at the red node gives a wrong black height.
- **Taking the wrong test in DEL.** The test at lines L19 and L22 is on the color of the child, not of $t$. A deletion from a black child makes that side one black level short and needs BAL-LEFT or BAL-RIGHT; a deletion from a red child does not.
- **REDDEN of a red or nil node.** Line L26 and line L28 apply REDDEN only to black nodes. The black height lemmas show that these nodes exist and are black; code that reaches REDDEN with a nil tree has a wrong black height somewhere.
- **Imperative rotations.** Porting the textbook insertion with in-place rotations and parent pointers breaks persistence. Each repair must make new nodes, and parent pointers cannot be used at all, because a shared node has different parents in different versions.

## Implementations

## History

Guibas and Sedgewick introduced red-black trees in 1978 as a coloring of the symmetric binary B-trees of Bayer. Chris Okasaki published the functional insertion with the four-case BALANCE as a functional pearl in the Journal of Functional Programming in 1999, and also in Section 3.3 of his book of 1998. The pearl gave no deletion. Stefan Kahrs gave a functional deletion in 2001, in a paper that also checks the invariants with the types of Haskell. The code above follows these two papers.

## References
