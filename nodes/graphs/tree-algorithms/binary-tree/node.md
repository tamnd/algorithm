---
tag: KHSGX1
kind: definition
slug: binary-tree
name: Binary tree
aliases:
- binary trees
area: graphs/tree-algorithms
level: intro
summary: A rooted tree in which each node has at most a left child and a right child.
prereqs: [rooted-tree]
see_also: [complete-binary-tree, binary-search-tree, binary-heap, inorder-traversal, catalan-numbers, left-child-right-sibling, threaded-binary-tree, cartesian-tree]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3 (Trees), the recursive definition of a binary tree and the remark that a binary tree is not a special case of a tree; Section 2.3.2 (Binary Tree Representation of Trees), the natural correspondence; Section 2.3.4.4 (Enumeration of Trees), the count of binary trees
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5.3 (Binary and positional trees), the recursive definition, full binary trees, and the bound on the number of nodes of a given height
---

A binary tree is either empty, or a root node together with two binary trees, its *left subtree* and its *right subtree*. In graph terms it is a [rooted tree](/rooted-tree/) in which each node has at most two children, and each child is marked as the *left* child or the *right* child, so a node with a single child still records on which side the child sits. Binary trees hold [binary search trees](/binary-search-tree/), [heaps](/binary-heap/), expression trees and Huffman codes, and the number of binary trees with $n$ nodes is the [Catalan number](/catalan-numbers/) $C_n$.

## Definition

A *binary tree* is a finite set of nodes that either is empty or consists of a node $r$, the *root*, and two disjoint binary trees $L$ and $R$, the *left subtree* and the *right subtree* of $r$ (Knuth, Section 2.3; CLRS, Appendix B.5.3). The root of $L$, if $L$ is not empty, is the *left child* of $r$, and the root of $R$ is the *right child*. Every node is the root of the binary tree formed by it and its descendants.

The definition is recursive and includes the empty tree, which a [rooted tree](/rooted-tree/) does not. The key difference from an ordered tree is the position of a lone child. An ordered tree with two nodes is unique, but there are two binary trees with two nodes: the root with a left child, and the root with a right child.

**Representation.** In code, the nodes are numbered $0, \ldots, n-1$ with the root at index $r$, and two arrays $left$ and $right$ hold the index of each child, or $-1$ for an empty subtree; a $parent$ array is often added. With pointers, each node is a record with the fields $left$ and $right$, and an empty subtree is the null pointer. A binary tree with $n \ge 1$ nodes has $2n$ child fields, of which $n - 1$ point to nodes and $n + 1$ are empty.

**Shape terms.** The *depth* of a node is the number of edges from the root to it, and the *height* of a non-empty tree is the largest depth; by convention the empty tree has height $-1$. A node with no children is a *leaf*, and the others are *internal* nodes.

- A *full* (or *proper*, or *strict*) binary tree is one in which every node has 0 or 2 children.
- A *perfect* binary tree of height $h$ is a full binary tree whose leaves all have depth $h$; it has $2^{h+1} - 1$ nodes.
- A [complete binary tree](/complete-binary-tree/) is a perfect binary tree with some of the rightmost nodes of the last level removed. (Some books, CLRS among them, use "complete" for what is called perfect here.)
- A *degenerate* binary tree is one in which every node has at most one child; it is a path.

**Basic facts.** For a binary tree with $n$ nodes and height $h$:

1. $h + 1 \le n \le 2^{h+1} - 1$, so $h \ge \lceil \log_2 (n + 1) \rceil - 1$.
2. Level $d$ holds at most $2^d$ nodes.
3. A full binary tree with $i$ internal nodes has $i + 1$ leaves, so $n = 2i + 1$ is odd.
4. The number of binary trees with $n$ nodes is $C_n = \frac{1}{n+1}\binom{2n}{n}$: 1, 1, 2, 5, 14, 42 for $n = 0, \ldots, 5$. This follows from $C_0 = 1$ and $C_n = \sum_{k=0}^{n-1} C_k C_{n-1-k}$, where $k$ is the size of the left subtree.

## Examples and non-examples

The running example has $n = 6$ nodes numbered $0, \ldots, 5$, root 0, and no weights:

```
        0
      /   \
     1     2
    / \     \
   3   4     5
```

$left = [1, 3, -1, -1, -1, -1]$ and $right = [2, 4, 5, -1, -1, -1]$. The height is 2 and the leaves are 3, 4 and 5. Of the 12 child fields, 5 point to nodes and $7 = n + 1$ are empty. The tree is not full, since node 2 has one child, and it is not complete, since node 2 has a right child but no left child. Its [inorder traversal](/inorder-traversal/) is $3, 1, 4, 0, 2, 5$, its [preorder](/preorder-traversal/) is $0, 1, 3, 4, 2, 5$, and its [postorder](/postorder-traversal/) is $3, 4, 1, 5, 2, 0$.

Small cases:

- **Empty tree.** No nodes, height $-1$. It is the base case of the definition and of most recursive algorithms on binary trees.
- **One node.** The root, with both subtrees empty; height 0, one leaf, two empty fields. It is full, perfect and complete.
- **A path.** Each node $i < n - 1$ has the single child $i + 1$. There are $2^{n-1}$ such binary trees, one for each choice of left or right at each of the $n - 1$ edges; all have height $n - 1$, the largest possible. A [binary search tree](/binary-search-tree/) built by inserting keys in sorted order has this shape.
- **Three nodes.** There are $C_3 = 5$ binary trees: the root with two children, and four paths (left-left, left-right, right-left, right-right).

Non-examples:

- **A star.** A root with three or more children is a rooted tree but not a binary tree.
- **Two trees that differ only in the side.** The root with a left child and the root with a right child are different binary trees, though they are the same rooted tree. They are not a non-example of binary trees, but a non-example of "binary tree = rooted tree with at most two children per node": that phrase forgets the sides.
- **A shared subtree.** A structure in which two nodes point to the same child is a DAG, such as an [expression DAG](/expression-dag/), not a binary tree, because the left and right subtrees in the definition must be disjoint.

## Related definitions

- **[Complete binary tree](/complete-binary-tree/).** The shape used by [binary heaps](/binary-heap/), stored in an array with no pointers.
- **[Binary search tree](/binary-search-tree/).** A binary tree with keys, ordered so that the [inorder traversal](/inorder-traversal/) lists the keys in sorted order.
- **[Cartesian tree](/cartesian-tree/).** The binary tree of an array that is in inorder by position and in heap order by value.
- **Natural correspondence.** The [left-child, right-sibling](/left-child-right-sibling/) representation turns a forest of ordered trees with $n$ nodes into a binary tree with $n$ nodes, and back (Knuth, Section 2.3.2). So binary trees with $n$ nodes and ordered forests with $n$ nodes are both counted by $C_n$.
- **Extended binary tree.** Replace each empty subtree by a special external leaf. A binary tree with $n$ nodes becomes a full binary tree with $n$ internal and $n + 1$ external nodes, which is the form used in the analysis of search costs.
- **[Threaded binary tree](/threaded-binary-tree/).** The $n + 1$ empty fields are reused to point to the inorder predecessor and successor.

### History

Knuth stresses in Section 2.3 that a binary tree is not a special case of a tree, because of the empty tree and the distinction between left and right.

## References
