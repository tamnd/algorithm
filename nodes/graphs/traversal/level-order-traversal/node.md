---
tag: F8MRDB
kind: algorithm
slug: level-order-traversal
name: Level-order traversal
aliases:
- breadth-first tree traversal
area: graphs/traversal
level: intro
summary: Visits tree nodes level by level using a queue.
solves: [tree-traversal]
model: word-ram
complexity:
  vars: {n: the number of nodes, w: the largest number of nodes at one depth}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(w)}
properties: {deterministic: true, recursive: false}
prereqs: [binary-tree, queue, tree-traversal]
see_also: [breadth-first-search, bfs-layers, preorder-traversal, inorder-traversal, postorder-traversal, binary-heap, complete-binary-tree, rooted-tree]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.3, Other representations of trees (the level order of the nodes of a forest, and the sequential representation in level order)
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Section 5.6, Tree traversal (level-order traversal of a binary tree with a queue, compared with the stack-based preorder traversal)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search (the queue discipline that level order applies to a tree)
---

Level-order traversal visits the nodes of a rooted tree by increasing depth: first the root, then its children, then their children, and within each depth from left to right. It keeps the nodes that are found but not visited yet in a first-in first-out [queue](/queue/): take the front node, visit it, and append its children. On a [binary tree](/binary-tree/) this takes $\Theta(n)$ time, and the queue never holds more than the nodes of about two consecutive levels. Level order is [breadth-first search](/breadth-first-search/) on a tree, where no node can be found twice, so no visited marks are needed. It is the order of the nodes in the array layout of a [binary heap](/binary-heap/) and of a [complete binary tree](/complete-binary-tree/).

## In plain words

Read a family tree one generation at a time. First the oldest ancestor. Then all of the children, from left to right. Then all of the grandchildren, from left to right, and so on.

To do this, keep a waiting line. Put the top person in the line. Then, again and again, take the person at the front, write down the name, and put that person's children at the back of the line, left child first. The children of a person in one generation always join the line after everyone of that generation who is already waiting, so the generations come out one after the other.

## The problem

The input is a binary tree with $n$ nodes, given by its root and, for each node $x$, its left child and right child, either of which may be missing. Let $\mathrm{depth}(x)$ be the number of edges from the root to $x$. For two nodes $x \ne y$ of the same depth, $x$ is *left of* $y$ if at the deepest common ancestor of $x$ and $y$, the path to $x$ goes to the left child and the path to $y$ to the right child. The task is to list all nodes, sorted by depth, and within a depth by the relation "left of". This is one of the standard orders of [tree traversal](/tree-traversal/), next to [preorder](/preorder-traversal/), [inorder](/inorder-traversal/) and [postorder](/postorder-traversal/).

## The algorithm

```pseudo id=main
LEVEL-ORDER(T)
L1  if T.root = NIL then return
L2  Q ← a queue that holds T.root
L3  while Q is not empty do
L4      x ← DEQUEUE(Q)
L5      VISIT(x)
L6      if x.left ≠ NIL then ENQUEUE(Q, x.left)
L7      if x.right ≠ NIL then ENQUEUE(Q, x.right)
```

For a general [rooted tree](/rooted-tree/), lines L6 and L7 become one loop that enqueues the children of $x$ from left to right.

## Example

Take the tree with root $A$ and the children $A(B, C)$, $B(D, E)$, $C(-, F)$, $E(G, -)$, $F(H, I)$, where "$-$" is a missing child.

```
          A
        /   \
       B     C
      / \     \
     D   E     F
        /     / \
       G     H   I
```

| visit | queue after the step |
|---|---|
| $A$ | $B, C$ |
| $B$ | $C, D, E$ |
| $C$ | $D, E, F$ |
| $D$ | $E, F$ |
| $E$ | $F, G$ |
| $F$ | $G, H, I$ |
| $G$ | $H, I$ |
| $H$ | $I$ |
| $I$ | empty |

The level order is $A, B, C, D, E, F, G, H, I$: depth 0 is $A$, depth 1 is $B, C$, depth 2 is $D, E, F$, and depth 3 is $G, H, I$. The preorder of the same tree is $A, B, D, E, G, C, F, H, I$, which goes down first. The queue never holds more than 3 nodes, and the widest levels have 3 nodes.

## Correctness

The queue is FIFO, so the nodes are visited in the order in which they were enqueued. The root comes first. The children of the nodes of depth $k$ are enqueued while those nodes are visited, one parent after the other, so if depth $k$ is visited in left-to-right order, depth $k + 1$ is enqueued in left-to-right order, and all of it after depth $k$. Induction on the depth gives the level order. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model.

- Each node is enqueued one time, by its parent or at line L2, and dequeued one time.
- Each dequeue does $O(1)$ work at lines L5 to L7.

So the time is $\Theta(n)$ on every tree. When a node of depth $k$ is at the front of the queue, the queue holds only nodes of depth $k$ and $k + 1$: the rest of depth $k$ and the children found so far. So it holds at most $w_k + w_{k+1} \le 2w$ nodes, where $w_k$ is the number of nodes at depth $k$, and just after the last node of depth $k - 1$ is visited, it holds all $w_k$ nodes of depth $k$, so for the widest level it holds $w$ nodes. The extra space is $\Theta(w)$. For a complete binary tree, $w$ is about $n/2$; for a path, $w = 1$.

## Properties

- **Deterministic.** The order is fixed by the tree.
- **Not recursive.** The loop uses only the queue.
- **Shallow nodes first.** All nodes of depth $k$ come before all nodes of depth $k + 1$. A search for the shallowest node with some property can stop at the first one it finds.
- **Width-bound memory.** The queue grows with the width of the tree, while the stack of a preorder traversal grows with the height. A tall thin tree favours level order, and a short wide tree favours preorder.

## Variants and improvements

- **Level by level.** Read the size $q$ of the queue at the start of each round and dequeue exactly $q$ nodes. Each round is one level, which gives the levels as separate lists, the width of each level, or the height of the tree.
- **Zigzag order.** Reverse every second level, or use two stacks, to list depth 0 left to right, depth 1 right to left, and so on.
- **Right view.** The last node of each round is the rightmost node of its level.
- **General graphs.** On a graph, the same loop needs visited marks, because a vertex can be found from several vertices, and it becomes [breadth-first search](/breadth-first-search/). Its rounds are the [BFS layers](/bfs-layers/).
- **Heap layout.** If a complete binary tree is stored in an array with the children of index $i$ at $2i + 1$ and $2i + 2$, the array is already in level order, and no queue is needed. This is the layout of a [binary heap](/binary-heap/).
- **Less memory.** Iterative deepening visits the nodes of depth $0, 1, 2, \ldots$ by repeated depth-limited preorder walks. This needs only $O(h)$ space for height $h$, but it takes $O(nh)$ time in the worst case.

## When to use it

Use level order when the depth matters: to print a tree by levels, to find the shallowest node that meets a test, to compute the width or the height of a tree without recursion, to connect each node to its right neighbour on the same level, or to serialize a tree level by level, as many test formats do. Use [preorder](/preorder-traversal/), [inorder](/inorder-traversal/) or [postorder](/postorder-traversal/) traversal when the work for a node depends on its subtree.

## Pitfalls

- **Stack instead of queue.** With a stack, the same loop gives a preorder of the mirror tree, not level order.
- **Enqueuing missing children.** Without the tests in lines L6 and L7, the queue fills with NIL entries. Some versions enqueue them on purpose, for example to serialize the shape, and must then skip them at line L4.
- **Levels from a single queue.** Without the round sizes of the level-by-level variant, the output does not show where one level ends.
- **Memory on wide trees.** The queue can hold about half of the nodes of a complete tree. On very wide trees, this is more than the $O(h)$ stack of a depth-first traversal.

## Implementations

## History

Knuth describes level order as one of the orders of the nodes of a forest, and uses it for a sequential representation of trees, in the section on other representations of trees in the first volume of The Art of Computer Programming. Sedgewick presents level-order traversal with a queue as the queue-based counterpart of the stack-based preorder traversal. The same queue discipline on general graphs is [breadth-first search](/breadth-first-search/).

## References
