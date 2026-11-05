---
tag: NWHW83
kind: data-structure
slug: left-child-right-sibling
name: Left-child right-sibling representation
aliases:
- first-child next-sibling
- child-sibling representation
area: graphs/graph-representation
level: core
summary: 'Rooted tree stored with two pointers per node: first child and next sibling.'
implements: [tree]
model: word-ram
complexity:
  vars: {n: the number of nodes, d: the number of children of the node of the call}
  time: {worst: O(1 + d)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [tree, rooted-tree, linked-list]
see_also: [binary-tree, parent-pointer-tree, preorder-traversal, postorder-traversal, inorder-traversal, tree-traversal, trie]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 10.3 (Representing rooted trees), the left-child, right-sibling representation and its exercises
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.2 (Binary tree representation of trees), the natural correspondence between forests and binary trees, and the preorder and postorder of a forest
  - book: isbn:9780201000238
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, Data Structures and Algorithms, Addison-Wesley, 1983
    locator: Chapter 3 (Trees), the leftmost-child, right-sibling representation
---

The left-child right-sibling representation stores a [rooted tree](/rooted-tree/) in which a node may have any number of children, with a fixed number of links in each node: a link to its leftmost child and a link to its next sibling to the right, and often a link to its parent. The children of a node then form a singly [linked list](/linked-list/), so the space is $\Theta(n)$ for $n$ nodes whatever the degrees are. Read as a [binary tree](/binary-tree/), with the child link as the left link and the sibling link as the right link, it is Knuth's *natural correspondence* between ordered forests and binary trees. It implements the [tree](/tree/) type for trees of unbounded degree.

## In plain words

Think of a family tree drawn on paper. Each person can have many children, and a program cannot know in advance how many slots to keep for them. This representation keeps only two slots in each person. One slot points to the eldest child. The other slot points to the next younger brother or sister.

To list all the children of a person, follow the eldest-child slot once, and then follow the sibling slots until they run out. So each family of brothers and sisters is a chain. Every person needs the same small amount of memory, whether they have no children or a hundred.

## The abstract type

The structure implements the [tree](/tree/) type for an *ordered* rooted tree, in which the children of each node have an order from left to right. The operations are:

- `root(T)`, `parent(T, x)` and `is-leaf(T, x)`.
- `children(T, x)`, the children of $x$ from left to right.
- `first-child(T, x)` and `next-sibling(T, x)`.
- `add-child(T, p) → x`, a new leaf $x$ as the leftmost child of $p$.
- `preorder(T, x)` and `postorder(T, x)`, the nodes of the subtree of $x$ in these orders.

## Representation

Each node $x$ has three fields: $x.child$, the leftmost child of $x$ or NIL; $x.sibling$, the child of $x.parent$ just to the right of $x$, or NIL if $x$ is the rightmost child; and $x.parent$, the parent of $x$ or NIL for the root. The tree $T$ has a field $T.root$. A node also has its key and data.

**Invariant.** For each node $p$ with children $c_1, c_2, \ldots, c_k$ from left to right:

- **(S1)** If $k = 0$, then $p.child = $ NIL. If $k \ge 1$, then $p.child = c_1$, $c_i.sibling = c_{i+1}$ for $1 \le i < k$, and $c_k.sibling = $ NIL.
- **(S2)** $c_i.parent = p$ for each $i$, and $T.root.parent = T.root.sibling = $ NIL.

So each node other than the root is in exactly one sibling chain, the chain of its parent. The tree has $n - 1$ child-parent pairs; (S1) uses one link for each of them, so of the $2n$ child and sibling links exactly $n - 1$ are not NIL and $n + 1$ are NIL. Compare an array of $k$ child links in each node: with $n$ nodes it has $kn$ links, of which only $n - 1$ are used, so $(k - 1)n + 1$ of them are NIL.

## Operations

```pseudo id=main
ADD-CHILD(T, p, x)                    ▷ x is a new node; it becomes the leftmost child of p
L1  x.parent ← p
L2  x.sibling ← p.child
L3  p.child ← x

CHILDREN(T, p)
L4  c ← p.child
L5  while c ≠ NIL do
L6      report c
L7      c ← c.sibling

PREORDER(T, r)                        ▷ the subtree of r
L8  S ← a stack holding r
L9  while S is not empty do
L10     x ← POP(S)
L11     report x
L12     if x ≠ r and x.sibling ≠ NIL then PUSH(S, x.sibling)
L13     if x.child ≠ NIL then PUSH(S, x.child)
```

**Add a child.** Lines L1 to L3 put the new node at the front of the chain of $p$ in $O(1)$ time. A new node goes to the right end of the chain only after a walk along it, in $O(1 + d)$ time, or in $O(1)$ time if each node also keeps a link to its rightmost child.

**Children.** Lines L4 to L7 walk the chain of $p$. The $i$-th child is found after $i - 1$ steps, so there is no $O(1)$ access to a child by its index.

**Preorder.** Lines L8 to L13 do a [preorder traversal](/preorder-traversal/). Line L13 pushes the first child last, so it pops first, and the subtrees of its younger siblings wait below it on the stack. The test $x \ne r$ in line L12 keeps the walk inside the subtree of $r$: the siblings of $r$ are not part of it. A [postorder traversal](/postorder-traversal/) reports each node after its subtree instead.

**Parent and depth.** With the parent field, `parent` is $O(1)$ and the depth of $x$ takes $O(1 + \text{depth}(x))$ time. Without it, a parent can only be found by a search from the root, or by a flag in the rightmost child whose sibling link then points back to the parent (the threaded form of Knuth).

## Example

Take the tree with root $A$, the children $B, C, D$ of $A$, the children $E, F$ of $B$, and the child $G$ of $D$.

```
        A                 A
      / | \              /
     B  C  D            B ─ C ─ D
    / \     \           |       |
   E   F     G          E ─ F   G
```

The left picture is the tree. The right picture shows the links: a vertical line is a child link and a horizontal line is a sibling link. The fields are:

| node | child | sibling | parent |
|---|---|---|---|
| A | B | NIL | NIL |
| B | E | C | A |
| C | NIL | D | A |
| D | G | NIL | A |
| E | NIL | F | B |
| F | NIL | NIL | B |
| G | NIL | NIL | D |

There are 7 nodes and 14 child and sibling links, of which 6 are not NIL and 8 are NIL. CHILDREN$(T, A)$ follows $A.child = B$, then $B.sibling = C$, then $C.sibling = D$, and stops at $D.sibling = $ NIL. PREORDER$(T, A)$ reports $A, B, E, F, C, D, G$. The postorder is $E, F, B, C, G, D, A$. PREORDER$(T, B)$ reports $B, E, F$ and does not go on to $C$, because of the test in line L12.

Read the right picture as a binary tree, with the child link to the left and the sibling link to the right. Its preorder is $A, B, E, F, C, D, G$, the preorder of the tree, and its [inorder](/inorder-traversal/) is $E, F, B, C, G, D, A$, the postorder of the tree.

## Correctness

ADD-CHILD keeps (S1) and (S2): the old chain $c_1, \ldots, c_k$ of $p$ becomes $x, c_1, \ldots, c_k$, because line L2 links $x$ to the old first child and line L3 makes $x$ the first child. CHILDREN reports exactly the chain of $p$, which by (S1) is the list of its children in order. PREORDER is correct because each node $x$ on the stack stands for a suffix of a sibling chain: the subtrees of $x$ and of its right siblings, in that order, are still to be reported. Popping $x$ reports $x$ and replaces this suffix by the subtrees of the children of $x$, then the subtrees of the right siblings of $x$. This is the recursive definition of preorder, and the full proof by induction on the size of the subtree is in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/). The times are worst case, where $d$ is the number of children of $p$ and $s$ the size of the subtree of $r$.

| operation | time |
|---|---|
| root, parent, first-child, next-sibling, is-leaf | $O(1)$ |
| add-child at the left end | $O(1)$ |
| add-child at the right end | $O(1 + d)$, or $O(1)$ with a rightmost-child link |
| children$(p)$, degree$(p)$ | $\Theta(1 + d)$ |
| the $i$-th child of $p$ | $\Theta(i)$ |
| remove a given child of $p$ | $O(1 + d)$, or $O(1)$ with a left-sibling link |
| preorder$(r)$, postorder$(r)$ | $\Theta(s)$ |
| space | three links and the data for each node, so $\Theta(n)$ |

Each traversal pushes and pops each node of the subtree once, and checks two links of it. The stack holds at most one node for each level of the subtree, plus the pending siblings, so its size is $O(s)$.

## Variants

- **Two links only.** Drop the parent field when the algorithm only walks down. The space is then two links for each node.
- **Doubly linked sibling chains.** Add a left-sibling link, and a removal of a given child becomes $O(1)$. Fibonacci heaps keep the children of a node in a circular doubly linked list for this reason.
- **Arrays instead of pointers.** Number the nodes $0$ to $n - 1$ and keep three integer arrays. The Python code does this. With a [parent-pointer tree](/parent-pointer-tree/) as input, one pass over the nodes in decreasing order builds the chains with the children in increasing order.
- **The binary-tree view.** The natural correspondence of Knuth turns each ordered forest into a binary tree and back. So code written for binary trees, such as a [binary tree](/binary-tree/) traversal, runs on a general tree without change.
- **Tries.** A [trie](/trie/) with a large alphabet can store the children of each node as a sibling chain instead of an array of size of the alphabet. This trades the $O(1)$ step to a child for space.

## When to use it

Use this representation when the nodes can have many children, when the degrees vary a lot, and when the algorithm visits the children of a node in order rather than by index. Examples are syntax trees, file system trees and the trees of heaps such as binomial and Fibonacci heaps. Use an array of child links when the degree is small and fixed, as in a binary or a 4-ary tree, because the child of index $i$ is then one step away. Use a [parent-pointer tree](/parent-pointer-tree/) when the algorithm only walks up, as in a [disjoint-set forest](/disjoint-set-forest/).

## Pitfalls

- **Leaving the subtree.** A traversal of the subtree of $r$ that follows $r.sibling$ visits nodes outside it. Line L12 must not push the sibling of the start node.
- **Deep recursion.** In the binary-tree view, a node with $d$ children has a right chain of length $d$. A recursive traversal that recurses on the sibling link reaches a depth of $n - 1$ on a star with $n$ nodes, and overflows the call stack for large $n$. Loop along the sibling chain, or use an explicit stack.
- **Order of the children.** ADD-CHILD puts the new node at the left end. Inserting the children in their natural order with it gives them in reverse order. Insert them in reverse order, or keep a rightmost-child link.
- **The $i$-th child.** The $i$-th child costs $\Theta(i)$ steps. Code that calls it in a loop over $i$ takes $\Theta(d^2)$ time for a node of degree $d$; walk the chain once instead.

## Implementations

The Python module numbers the nodes from 0, with the root 0, and keeps the three links in integer arrays with $-1$ for NIL. It builds a tree from a parent array in one pass and does both traversals with an explicit stack.

## History

Knuth, in Section 2.3.2, describes the natural correspondence between forests and binary trees, in which the left link of a node points to its first child and the right link to its next sibling, and shows that preorder and postorder of a forest become preorder and inorder of the binary tree. CLRS call this the left-child, right-sibling representation, and Aho, Hopcroft and Ullman call it the leftmost-child, right-sibling representation.

## References
