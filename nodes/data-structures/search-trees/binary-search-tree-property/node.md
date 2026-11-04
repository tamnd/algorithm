---
tag: BVY8YQ
kind: definition
slug: binary-search-tree-property
name: Binary search tree property
aliases:
- BST property
- search tree ordering
area: data-structures/search-trees
level: intro
summary: Keys in the left subtree are smaller than a node's key and keys in the right subtree are larger.
prereqs: [binary-tree, inorder-traversal, total-order]
see_also: [binary-search-tree, bst-search, heap-property, representation-invariant, tree-rotation, catalan-numbers]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.1 (What is a binary search tree?), the binary-search-tree property and Theorem 12.1 on the in-order walk
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), the definition of a binary search tree by symmetric order
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), the definition of a BST
---

The binary search tree property is the order condition on the keys of a [binary tree](/binary-tree/) that makes it a [binary search tree](/binary-search-tree/): for each node $x$, each key in the left subtree of $x$ is smaller than the key of $x$, and each key in the right subtree of $x$ is larger. It holds exactly when the [in-order traversal](/inorder-traversal/) lists the keys in increasing order. It is the [representation invariant](/representation-invariant/) that each search tree operation must keep, and it is what lets a search discard one subtree at each node.

## Definition

Let $(K, <)$ be a [total order](/total-order/), and let $T$ be a binary tree in which each node $x$ has a key $x.key \in K$. For a node $x$, write $L(x)$ and $R(x)$ for the sets of nodes of its left and right subtrees (each may be empty).

$T$ has the **binary search tree property** if, for each node $x$ of $T$,

$$\forall y \in L(x):\ y.key < x.key \qquad \text{and} \qquad \forall y \in R(x):\ x.key < y.key.$$

The empty tree has the property. The condition is on whole subtrees, not only on children. With strict inequalities the keys of $T$ are distinct, because two nodes with the same key would have a lowest common ancestor $u$, and the two nodes cannot both be on allowed sides of $u$.

**Equivalent forms.** For a binary tree $T$ with keys, the following three statements are equivalent.

1. $T$ has the binary search tree property.
2. **In-order form.** The in-order sequence of keys $x_1.key, x_2.key, \ldots, x_n.key$ is strictly increasing.
3. **Interval form.** There is a way to give each node $x$ an open interval $(a_x, b_x)$, with $a_x, b_x \in K \cup \{-\infty, +\infty\}$, such that the root gets $(-\infty, +\infty)$, $a_x < x.key < b_x$ for each node, the left child of $x$ gets $(a_x, x.key)$ and the right child gets $(x.key, b_x)$.

*Proof that 1 implies 2.* By induction on the number of nodes. The in-order sequence of a tree with root $r$ is the sequence of $L(r)$, then $r$, then the sequence of $R(r)$. Both subtrees have the property, so their sequences are increasing by the induction hypothesis. By the property at $r$, each key of the first part is less than $r.key$, and each key of the last part is greater. So the whole sequence is increasing.

*Proof that 2 implies 3.* Give each node the interval of item 3, defined from the root down; this is always possible as a definition. We show $a_x < x.key < b_x$. The bound $a_x$ is $-\infty$ or the key of an ancestor $u$ such that $x$ is in $R(u)$, and in-order lists $u$ before each node of $R(u)$, so $u.key < x.key$ by item 2. The same argument with $L(u)$ gives $x.key < b_x$.

*Proof that 3 implies 1.* Let $y \in L(x)$. Each node on the path from the left child of $x$ down to $y$ has an interval inside $(a_x, x.key)$, because the interval of a child is inside the interval of its parent. So $y.key < x.key$. The case $y \in R(x)$ is the mirror image. $\square$

The in-order form gives a linear-time test: walk the tree in in-order and check each pair of neighbours. The interval form gives another linear-time test that also works top-down, as in the recursive check $\mathrm{valid}(x, a, b)$ that tests $a < x.key < b$, then $\mathrm{valid}(x.left, a, x.key)$ and $\mathrm{valid}(x.right, x.key, b)$.

**Duplicate keys.** Some texts allow equal keys and use $\le$ on one side, for example $y.key \le x.key$ for $y \in L(x)$ and $x.key \le y.key$ for $y \in R(x)$, as in CLRS Section 12.1. Then the in-order sequence is non-decreasing instead of increasing, and a search for a key must decide on which side equal keys can be. A map with distinct keys, as in Sedgewick and Wayne, uses the strict form.

## Examples and non-examples

**Example.** The tree with root 8, whose left child 3 has children 1 and 6, and whose right child 10 has a right child 14, has the property. Its in-order sequence is 1, 3, 6, 8, 10, 14, which is increasing.

```
        8
      /   \
     3     10
    / \      \
   1   6      14
```

The intervals of the interval form are $(-\infty, +\infty)$ for 8, $(-\infty, 8)$ for 3, $(-\infty, 3)$ for 1, $(3, 8)$ for 6, $(8, +\infty)$ for 10 and $(10, +\infty)$ for 14. Each key lies in its interval.

**Non-example: only the children are checked.** The tree with root 10, left child 5, and a right child 12 of the node 5:

```
     10
    /
   5
    \
     12
```

Each node is larger than its left child and smaller than its right child, but 12 is in the left subtree of 10 and $12 > 10$. The in-order sequence 5, 12, 10 is not increasing. A search for 12 compares with 10, goes right, finds an empty subtree and reports that 12 is absent. This is the most common error in a check of the property.

**Non-example: equal keys with the strict form.** A root 5 with left child 5 fails the strict property; it has the non-strict form above.

**Same keys, many trees.** The keys 1, 2 and 3 give exactly 5 binary search trees, one for each shape of a binary tree with 3 nodes: two trees with root 1, two with root 3, and the balanced tree with root 2. In general $n$ distinct keys give $C_n = \frac{1}{n+1}\binom{2n}{n}$ trees, the [Catalan number](/catalan-numbers/), because the in-order form fixes which key goes on each node of a given shape. For $n = 4$ that is 14 trees.

**The property is not the heap property.** In a binary tree with the [heap property](/heap-property/), each key is at most the keys of its children, so the minimum is at the root. In a BST the minimum is at the end of the leftmost path. A tree with distinct keys and at least two nodes cannot have both properties when a node has a left child, because that child would have to be both larger and smaller than its parent.

## Related definitions

- [Binary search tree](/binary-search-tree/): a binary tree with this property, with the operations that keep it.
- [In-order traversal](/inorder-traversal/): the order of the nodes that the property makes sorted.
- [Representation invariant](/representation-invariant/): the general notion; the BST property is the invariant of each search tree.
- [Tree rotation](/tree-rotation/): a local change of shape that keeps the in-order sequence, so it keeps the property.
- [Heap property](/heap-property/): the other main order condition on a binary tree, from parent to child.
- Balance conditions, such as those of the [AVL tree](/avl-tree/) and the [red-black tree](/red-black-tree/), are extra conditions on the shape, on top of this property.

## References
