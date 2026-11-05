---
tag: EM48V4
kind: problem
slug: tree-traversal
name: Tree traversal
aliases:
- binary tree traversal
- tree walk
area: graphs/tree-algorithms
level: intro
summary: Visit every node of a tree exactly once in a systematic order.
prereqs: [rooted-tree, binary-tree]
see_also: [preorder-traversal, postorder-traversal, inorder-traversal, level-order-traversal, morris-traversal, depth-first-orders, euler-tour-technique, graph-traversal]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1 (Traversing binary trees, preorder, inorder and postorder, Algorithm T with a stack, and threaded trees) and Section 2.3.2 (Binary tree representation of trees, preorder and postorder of a forest)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.1 (What is a binary search tree?), the inorder, preorder and postorder tree walks and Theorem 12.1 on the time of an inorder walk
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Section 5.6, Tree traversal (recursive and stack-based preorder, inorder and postorder, and level order with a queue)
---

Tree traversal is the problem of listing all vertices of a [rooted tree](/rooted-tree/), each exactly once, in an order that the shape of the tree fixes. The standard orders are preorder (a vertex before its subtrees), postorder (a vertex after its subtrees), inorder (for [binary trees](/binary-tree/): left subtree, vertex, right subtree) and level order (by depth). Each order takes $\Theta(n)$ time on a tree with $n$ vertices, and the orders differ in the extra memory they need and in the problems they fit.

## In plain words

A tree has a top node, and each node hangs some children below it, in a fixed order from left to right. To process every node, you need a rule for the order of the visits. One rule says: handle a node, then go down into each child in turn. Another says: go down into all children first, and handle the node when you come back up. A third, for nodes with a left and a right side, says: left side, then the node, then the right side. A fourth reads the tree line by line, from the top. Each rule visits each node once, so the work grows in step with the number of nodes. The rules differ in what is already done when a node is handled.

## Definition

**Input.** An ordered rooted tree $T$ with $n \ge 1$ vertices, given by its root $r$ and, for each vertex $v$, the list of its children $c_1(v), \ldots, c_{k(v)}(v)$ in order. The tree is not weighted. The vertices are numbered $0, \ldots, n-1$, but the orders below depend only on the shape and the order of the children, not on the numbers. For a binary tree, each vertex has a left child and a right child, each of which may be missing.

**Output.** A sequence that holds each vertex exactly once. Let $T_v$ be the subtree of $v$ and write the concatenation of sequences by juxtaposition. The orders are defined by recursion on the subtrees.

$$\mathrm{pre}(T_v) = v, \ \mathrm{pre}(T_{c_1}), \ \ldots, \ \mathrm{pre}(T_{c_k})$$

$$\mathrm{post}(T_v) = \mathrm{post}(T_{c_1}), \ \ldots, \ \mathrm{post}(T_{c_k}), \ v$$

$$\mathrm{in}(T_v) = \mathrm{in}(T_{\mathrm{left}(v)}), \ v, \ \mathrm{in}(T_{\mathrm{right}(v)}) \quad \text{(binary trees; an empty subtree gives the empty sequence)}$$

The *level order* lists the vertices sorted by depth, and within one depth in the order of $\mathrm{pre}$. A *traversal algorithm* produces one of these sequences, or calls a procedure VISIT on the vertices in this order.

## Variants

- **Preorder** (NLR, "node, left, right"): solved by [preorder traversal](/preorder-traversal/). Each vertex comes before all of its proper descendants.
- **Postorder** (LRN): solved by [postorder traversal](/postorder-traversal/). Each vertex comes after all of its proper descendants.
- **Inorder** (LNR), for binary trees only: solved by [inorder traversal](/inorder-traversal/). In a [binary search tree](/binary-search-tree/) it lists the keys in sorted order.
- **Level order**: solved by [level-order traversal](/level-order-traversal/) with a queue.
- **Reverse orders.** Visiting the children from right to left gives the mirror orders. The reverse of the postorder is the preorder of the mirror tree.
- **Euler tour.** The walk that lists a vertex each time the search enters or leaves it, with $2n - 1$ entries if a vertex is written on each arrival, is the basis of the [Euler tour technique](/euler-tour-technique/).
- **Memory-limited traversal.** List the orders with $O(1)$ extra words: with parent pointers, or with temporary threads as in [Morris traversal](/morris-traversal/).
- **Free trees and graphs.** A free tree given as an edge list is first rooted, see [tree rooting](/tree-rooting/). On a general graph the problem becomes [graph traversal](/graph-traversal/), and the orders become the [depth-first orders](/depth-first-orders/) of a search.

## Examples

Take the binary tree on $\{0, \ldots, 7\}$ rooted at $0$, with left and right children $0(1, 2)$, $1(3, 4)$, $2(-, 5)$ and $4(6, 7)$, where "$-$" is a missing child.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

| order | sequence |
|---|---|
| preorder | 0, 1, 3, 4, 6, 7, 2, 5 |
| inorder | 3, 1, 6, 4, 7, 0, 2, 5 |
| postorder | 3, 6, 7, 4, 1, 5, 2, 0 |
| level order | 0, 1, 2, 3, 4, 5, 6, 7 |

Read as a general ordered tree (the children of 2 are just $[5]$), the preorder, postorder and level order do not change, and the inorder is not defined.

The small cases:

- **Single vertex.** Every order is $[0]$.
- **Path** $0, 1, \ldots, n-1$ rooted at $0$, each vertex the only child of the one before. Preorder and level order are $0, 1, \ldots, n-1$, and postorder is $n-1, \ldots, 1, 0$. As a binary tree in which each child is a left child, inorder equals postorder; if each child is a right child, inorder equals preorder.
- **Star** with centre $0$ and children $1, \ldots, n-1$. Preorder and level order are $0, 1, \ldots, n-1$, and postorder is $1, \ldots, n-1, 0$.

## Known algorithms

| algorithm | order | time | extra space |
|---|---|---|---|
| [Preorder traversal](/preorder-traversal/) | preorder | $\Theta(n)$ | $O(h)$ with a stack of child positions |
| [Postorder traversal](/postorder-traversal/) | postorder | $\Theta(n)$ | $O(h)$ |
| [Inorder traversal](/inorder-traversal/) | inorder | $\Theta(n)$ | $O(h)$ |
| [Level-order traversal](/level-order-traversal/) | level order | $\Theta(n)$ | $\Theta(w)$, the largest level size |
| [Morris traversal](/morris-traversal/) | inorder or preorder | $\Theta(n)$ | $O(1)$, changes pointers for a while |
| [Iterative DFS](/iterative-depth-first-search/) | depth-first orders | $\Theta(n)$ | $O(h)$ to $O(n)$ |

Here $h$ is the height of the tree. A recursive program uses a call stack of depth $h + 1$, which is $n$ on a path.

## Bounds

- **Upper bound.** Each order takes $\Theta(n)$ time in the [word RAM](/word-ram/) model: each vertex is visited once, and each child list is read once, so the work is $O(n + (n - 1)) = O(n)$ by the [tree edge count](/tree-edge-count/).
- **Lower bound.** Each algorithm needs $\Omega(n)$ time, because the output has $n$ entries. So $\Theta(n)$ is tight.
- **Space.** A stack-based depth-first traversal needs $\Theta(h)$ extra words in the worst case over trees of height $h$, when it keeps one entry per vertex on the current path. With parent pointers, each depth-first order can be produced with $O(1)$ extra words by walking up and down the tree.

## Reductions

- **Postorder to preorder.** The postorder of $T$ is the reverse of the preorder of the mirror of $T$, so one algorithm gives the other in $O(n)$ extra time.
- **Rebuilding a tree.** The preorder and the postorder together determine an ordered tree: the first vertex of the preorder is the root, and the subtree of each child is a contiguous block of the postorder that ends with the child. The preorder and the inorder determine a binary tree with distinct labels. The preorder and the postorder do not determine a binary tree: a root with only a left child and a root with only a right child have the same two orders.
- **To graph search.** A tree traversal is a [depth-first search](/depth-first-search/) or a [breadth-first search](/breadth-first-search/) in which no vertex can be found twice, so no visited marks are needed.

## Applications

- **Postorder.** Evaluate an [expression tree](/expression-tree/), compute [subtree sizes](/subtree-sizes/) and other bottom-up dynamic programs, free the nodes of a tree, add up the sizes of folders.
- **Preorder.** Copy or serialize a tree, print an indented outline or a file listing, number the vertices so that each subtree is a contiguous range, as in [Euler tour subtree queries](/euler-tour-subtree-queries/).
- **Inorder.** List the keys of a [binary search tree](/binary-search-tree/) in sorted order.
- **Level order.** Store a [complete binary tree](/complete-binary-tree/) in an array, print a tree by levels, find a shallowest vertex with a property.

## References
