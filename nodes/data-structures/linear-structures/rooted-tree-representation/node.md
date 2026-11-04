---
tag: X6DGHS
kind: data-structure
slug: rooted-tree-representation
name: Rooted tree representation (left-child right-sibling)
aliases:
- Rooted trees representation
area: data-structures/linear-structures
level: core
summary: A way to store a rooted tree with arbitrary branching using, for each node, a pointer to its leftmost child and one to its next sibling.
implements: [tree]
prereqs: [rooted-tree, binary-tree, pointer, singly-linked-list]
see_also: [left-child-right-sibling, tree, binary-tree, rooted-tree, tree-traversal, preorder-traversal, depth-first-search, singly-linked-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.3 (Representing rooted trees), the parts on binary trees and on rooted trees with unbounded branching
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 10.4 (Representing rooted trees), Exercise 10.4-4 (print the keys of a left-child, right-sibling tree in O(n) time)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.2 (Binary tree representation of trees), the natural correspondence between forests and binary trees
---

The left-child, right-sibling representation stores a [rooted tree](/rooted-tree/) in which a node may have any number of children, using three [pointers](/pointer/) per node: one to its parent, one to its leftmost child, and one to its next sibling to the right. The children of each node form a [singly linked list](/singly-linked-list/), so the space is $\Theta(n)$ for $n$ nodes whatever the degrees, adding a child and finding the parent cost $O(1)$, and listing the children of a node $x$ costs $\Theta(\deg x)$. Read as a [binary tree](/binary-tree/), with the first child as the left child and the next sibling as the right child, the representation is the classic one-to-one correspondence between ordered forests and binary trees.

## In plain words

A family tree can have one child under a person or ten. If each person had a slot for every child, you would need to know the largest family in advance, and most slots would stay empty.

Instead, give each person two arrows. The first arrow points to their oldest child. The second arrow points to their next younger brother or sister. To list the children of a person, follow the first arrow once, then keep following the sibling arrows until they stop. Each person also keeps an arrow back to their parent. Every person then uses the same small amount of memory, however many children they have, and any shape of tree fits.

## The abstract type

The structure implements the [tree](/tree/) type: ordered rooted trees whose nodes carry keys, with these operations.

- `new_node(k)`: a tree with one node, of key $k$.
- `add_child(x, y)`: make the root $y$ of another tree the new leftmost child of $x$.
- `parent(x)`: the parent of $x$, or nil for a root.
- `children(x)`: the children of $x$, from left to right.
- `detach(y)`: cut the subtree of $y$ from its parent, so that $y$ becomes a root.
- `preorder(r)` and `postorder(r)`: all keys of the subtree of $r$, each node before its children, or each node after its children.

## Representation

Each node $x$ has a key $x.key$ and three pointers: $x.p$ (the parent), $x.\mathit{left}$ (the leftmost child) and $x.\mathit{right}$ (the next sibling to the right). Write them as in CLRS, $x.p$, $x.\text{left-child}$ and $x.\text{right-sibling}$.

**Invariant.** For each node $x$ with children $c_1, \dots, c_d$ in left-to-right order:

- (T1) $x.\text{left-child} = c_1$, or nil when $d = 0$;
- (T2) $c_i.\text{right-sibling} = c_{i+1}$ for $1 \le i < d$, and $c_d.\text{right-sibling} = \text{nil}$;
- (T3) $c_i.p = x$ for each $i$;
- (T4) a root has $p = \text{nil}$ and $\text{right-sibling} = \text{nil}$.

So the children of $x$ are exactly the nodes of the list that starts at $x.\text{left-child}$ and follows the right-sibling pointers. Each node except a root appears in exactly one such list, the list of its parent.

## Operations

```pseudo id=main
NEW-NODE(k)
L1  x ← a new node; x.key ← k; x.p, x.left-child, x.right-sibling ← nil; return x
ADD-CHILD(x, y)                       ▷ y is a root, x is not in the subtree of y
L2  y.p ← x
L3  y.right-sibling ← x.left-child
L4  x.left-child ← y
CHILDREN(x)
L5  c ← x.left-child
L6  while c ≠ nil do
L7      visit c; c ← c.right-sibling
PREORDER(r)                           ▷ visit the subtree of r, with O(1) extra space
L8  x ← r
L9  while x ≠ nil do
L10     visit x
L11     if x.left-child ≠ nil then x ← x.left-child
        else
L12         while x ≠ r and x.right-sibling = nil do x ← x.p
L13         if x = r then x ← nil else x ← x.right-sibling
```

**ADD-CHILD** pushes $y$ on the front of the child list of $x$, as a push on a [stack](/stack/) made of a linked list, in $O(1)$ time. To build the children of a node in left-to-right order, add them from right to left.

**CHILDREN** walks the child list in $\Theta(\deg x)$ time. The degree of $x$ and its $k$-th child cost the same walk, $O(\deg x)$ and $O(k)$.

**PREORDER** walks the tree with no stack. After it visits $x$, the next node in preorder is the leftmost child of $x$ (line L11). If $x$ has no child, the subtree of $x$ is done, and the next node is the right sibling of the nearest node on the path from $x$ up to $r$, excluding $r$, that has one. Line L12 climbs to that node by parent pointers, and line L13 steps to its sibling, or ends the walk at $r$. The walk costs $\Theta(n)$ for a subtree of $n$ nodes.

```pseudo id=detach
DETACH(y)                             ▷ cut the subtree of y from its parent
D1  x ← y.p; if x = nil then return
D2  if x.left-child = y then x.left-child ← y.right-sibling
D3  else c ← x.left-child
D4      while c.right-sibling ≠ y do c ← c.right-sibling
D5      c.right-sibling ← y.right-sibling
D6  y.p ← nil; y.right-sibling ← nil
```

DETACH removes $y$ from the singly linked child list of its parent. It must find the sibling before $y$, so it costs $O(\deg x)$ where $x$ is the parent.

## Example

Build the tree with root A, whose children are B, C, D; B has the children E and F, and D has the child G. With ADD-CHILD the children go in from right to left: ADD-CHILD(A, D), ADD-CHILD(A, C), ADD-CHILD(A, B), ADD-CHILD(B, F), ADD-CHILD(B, E), ADD-CHILD(D, G). The fields are then:

| node | p | left-child | right-sibling |
|---|---|---|---|
| A | nil | B | nil |
| B | A | E | C |
| C | A | nil | D |
| D | A | G | nil |
| E | B | nil | F |
| F | B | nil | nil |
| G | D | nil | nil |

CHILDREN(A) follows B, then B.right-sibling = C, then C.right-sibling = D, then nil. PREORDER(A) visits A, B, E (left-child steps), then F (a sibling step, since E is a leaf), then climbs from F to B and steps to C, then to D, down to G, and climbs from G to D and to A $= r$, where it stops. The order is A, B, E, F, C, D, G, and the postorder is E, F, B, C, G, D, A.

Read as a binary tree with left = left-child and right = right-sibling, the same seven nodes have the preorder A, B, E, F, C, D, G, the same as the tree, and the inorder E, F, B, C, G, D, A, which is the postorder of the tree.

## Correctness

ADD-CHILD keeps (T1) to (T4): $y$ becomes $c_1$ of $x$, the old first child becomes its right sibling, the parent of $y$ is $x$, and no other list changes; the condition that $x$ is not in the subtree of $y$ keeps the structure a tree. DETACH removes $y$ from the child list of its parent and resets its two fields, which is (T4) for the new root $y$. CHILDREN reads the list of (T1) and (T2). For PREORDER, the key fact is that the subtree of $x$ is a contiguous part of the preorder, so the node after its last node is the right sibling of $x$, or, if $x$ is the last child, the node after the subtree of its parent. Each climb in line L12 leaves a subtree that is complete, so each node is climbed from at most once. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time (worst case) | notes |
|---|---|---|
| new_node, add_child | $O(1)$ | push on the child list |
| parent | $O(1)$ | one pointer |
| children of $x$, degree of $x$ | $\Theta(\deg x)$ | walk the child list |
| $k$-th child of $x$ | $O(k)$ | no random access to the children |
| detach $y$ | $O(\deg x)$, $x$ the parent of $y$ | find the sibling before $y$ |
| preorder, postorder of $n$ nodes | $\Theta(n)$ time, $O(1)$ extra space | at most $2(n - 1)$ pointer steps |
| space | three pointers and a key per node | $\Theta(n)$, whatever the degrees |

The bounds hold on the [word RAM](/word-ram/) with one step per pointer read or write. In PREORDER, each of the $n - 1$ nodes other than $r$ is entered once by line L11 or line L13, and each is left upward at most once by line L12, which gives at most $2(n - 1)$ moves.

## Variants

- **Without parent pointers.** If the program only walks from the root, drop $x.p$; a traversal then needs a [stack](/stack/) of depth up to the height. A threaded form instead lets the right-sibling pointer of the last child point back to the parent, with a tag bit, which recovers the parent with two pointers per node.
- **Doubly linked siblings.** A left-sibling pointer makes DETACH take $O(1)$ time, at the cost of a fourth pointer.
- **Bounded degree.** When each node has at most $k$ children and $k$ is small, an array of $k$ child pointers per node gives $O(1)$ access to the $i$-th child but uses $k + 1$ pointers per node; for $k = 2$ this is the usual [binary tree](/binary-tree/) node.
- **Parent array.** Storing only $p[x]$ for nodes numbered $1$ to $n$ uses one integer per node and supports parent queries and union-find style operations, but listing the children of a node takes $\Theta(n)$ time.
- **The binary tree view.** The [left-child, right-sibling binary tree](/left-child-right-sibling/) is the same structure seen as a binary tree, and it maps each ordered forest to a unique binary tree and back.

## When to use it

Use the left-child, right-sibling form when nodes have very different numbers of children and the program visits children in order: file system trees, syntax trees, the DOM of a web page, and game trees. It uses the same memory per node for every shape and needs no resizing. Use an array of children per node when the program needs the $i$-th child in $O(1)$ time, for example in a trie with a fixed alphabet or in a [B-tree](/b-tree/) node. Use a parent array when the program only goes up the tree.

## Pitfalls

- **Children come out reversed.** ADD-CHILD puts the new child first. A program that adds the children from left to right gets them in reverse order from CHILDREN. Add them from right to left, or keep a pointer to the last child and append.
- **Climbing past the root of a subtree.** In line L12, the test $x \ne r$ is needed when $r$ is not the root of the whole tree: without it, a walk of the subtree of B continues to C and D. The test with PREORDER(B) catches this.
- **Detaching the first child.** DETACH must update $x.\text{left-child}$ when $y$ is the first child (line D2). A loop that only searches for the predecessor sibling fails on the first child, because it has none.
- **Stale fields after a move.** Moving a subtree with ADD-CHILD without a DETACH first leaves $y$ in two child lists. Line D6 resets $y.p$ and $y.\text{right-sibling}$, and ADD-CHILD should accept only a root.
- **Recursion depth.** A recursive traversal of a path-shaped tree with $10^5$ nodes overflows the call stack in many languages. The loop of lines L8 to L13 uses constant extra space.

## Implementations

## References
