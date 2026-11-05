---
tag: V880D8
kind: algorithm
slug: morris-traversal
name: Morris traversal
aliases:
- Morris inorder traversal
area: graphs/traversal
level: advanced
summary: Inorder traversal using O(1) extra space by temporarily threading the tree.
model: word-ram
complexity:
  vars: {n: the number of nodes}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: true}
prereqs: [inorder-traversal, threaded-binary-tree]
see_also: [tree-traversal, preorder-traversal, postorder-traversal, binary-search-tree, level-order-traversal, iterative-depth-first-search, in-place-algorithm, mark-and-sweep]
sources:
  - paper: doi:10.1016/0020-0190(79)90068-1
    title: Joseph M. Morris, Traversing binary trees simply and cheaply, Information Processing Letters 9(5), 197 to 200 (1979)
    locator: the inorder traversal that sets a temporary thread from the inorder predecessor of a node to the node and removes it on the second visit, with no stack and no tag bits
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1, Traversing binary trees (inorder traversal with a stack, threaded binary trees, and the exercises on traversal without an auxiliary stack)
---

Morris traversal lists the nodes of a binary tree in [inorder](/inorder-traversal/) with only a constant number of extra pointers: no [stack](/stack/), no recursion and no mark bits. It borrows the empty right pointer of the inorder predecessor of a node, as in a [threaded binary tree](/threaded-binary-tree/), and points it back to the node, so that the walk can climb back up after it finishes the left subtree. It removes each such thread on the way back, so the tree is unchanged at the end. Joseph Morris published the method in 1979. It runs in $\Theta(n)$ time on a tree with $n$ nodes.

## In plain words

To list a tree in order, one goes down to the left, lists a node, and then goes into its right part. The hard step is to come back up from the end of a left part to the node above it. Usually a stack remembers the way back.

Morris traversal has no stack. Before it goes down to the left of a node, it finds the last node of that left part, the one just before the node in the order. That node has no right child, so its right link is free. The walk points this free link back to the node. Later, when the walk reaches the end of the left part, it follows this link back up. It then sees the link a second time, knows that the left part is done, removes the link, lists the node and goes right.

## The problem

The input is a binary tree on the nodes $0, \ldots, n - 1$, given by the arrays $\mathrm{left}$ and $\mathrm{right}$ with NIL for a missing child, and its root. The output is the list of the nodes in inorder: for each node, all nodes of its left subtree, then the node, then all nodes of its right subtree. The algorithm may write to $\mathrm{right}$ during the run, but it must leave $\mathrm{left}$ and $\mathrm{right}$ as they were at the end, and it may use only $O(1)$ extra words besides the output.

## The algorithm

```pseudo id=main
MORRIS-INORDER(root)
L1  x ← root
L2  while x ≠ NIL do
L3      if left[x] = NIL then
L4          visit x; x ← right[x]
        else
L5          p ← left[x]; while right[p] ≠ NIL and right[p] ≠ x do p ← right[p]
L6          if right[p] = NIL then right[p] ← x; x ← left[x]
L7          else right[p] ← NIL; visit x; x ← right[x]
L8  return
```

The node $p$ that line L5 finds is the last node of the left subtree of $x$ in inorder, which is the inorder predecessor of $x$. Line L6 makes the thread from $p$ to $x$ on the first visit to $x$ and goes left. Line L7 finds the thread on the second visit, removes it, visits $x$ and goes right. A node without a left child is reached once and visited at once by line L4, and if it is the end of a left subtree, its right pointer is a thread, so line L4 also follows the thread back up.

## Example

Take the tree with root 4, where 4 has the children 1 and 5, node 1 has the children 0 and 3, node 3 has the left child 2, and node 5 has the right child 6. Its inorder is $0, 1, 2, 3, 4, 5, 6$.

| step | $x$ | line | action | next $x$ |
|---|---|---|---|---|
| 1 | 4 | L5, L6 | predecessor 3 (path 1, 3); thread $3 \to 4$ | 1 |
| 2 | 1 | L5, L6 | predecessor 0; thread $0 \to 1$ | 0 |
| 3 | 0 | L4 | visit 0, follow the thread | 1 |
| 4 | 1 | L5, L7 | predecessor 0 points to 1; remove the thread, visit 1 | 3 |
| 5 | 3 | L5, L6 | predecessor 2; thread $2 \to 3$ | 2 |
| 6 | 2 | L4 | visit 2, follow the thread | 3 |
| 7 | 3 | L5, L7 | remove $2 \to 3$, visit 3, then $\mathrm{right}[3]$ is the thread to 4 | 4 |
| 8 | 4 | L5, L7 | the path 1, 3 ends at 3, which points to 4; remove it, visit 4 | 5 |
| 9 | 5 | L4 | visit 5 | 6 |
| 10 | 6 | L4 | visit 6 | NIL |

The visits are $0, 1, 2, 3, 4, 5, 6$. The three nodes with a left child (4, 1 and 3) are reached twice, and the other four are reached once, so the loop runs $3 \cdot 2 + 4 = 10$ times. At step 7, the right pointer of 3 is still the thread to 4 when line L7 reads it, so the walk climbs from 3 to 4 although 4 is not the parent of 3. After step 8 all threads are gone.

## Correctness

The proof is by induction on the size of a subtree. Suppose the walk arrives at a node $x$ when all pointers in the subtree $T$ of $x$ are original, except that the right pointer of the last node $r$ of $T$ in inorder may point to some node $s$ outside $T$. Then the walk visits $T$ in inorder and arrives at $s$, with $T$ in the same state. If $x$ has a left subtree $T_L$, the predecessor search walks down the right edge of $T_L$ to its last node, which has a free right pointer, and line L6 points it to $x$. By induction on $T_L$, with $s = x$, the walk lists $T_L$ and comes back to $x$. The second search now stops at the thread, line L7 removes it and visits $x$, and the right subtree is handled by induction. Applied to the root with $s = \mathrm{NIL}$, this gives the inorder and a restored tree. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model.

- **Main loop.** A node with a left child is reached twice, at lines L6 and L7, and a node without a left child once, at line L4. So the loop of line L2 runs at most $2n$ times.
- **Predecessor searches.** For a node $x$ with a left child, line L5 walks the right edge of the left subtree of $x$, the path from $\mathrm{left}[x]$ along right pointers, twice. Each node $y$ lies on this path for at most one $x$: follow parent links up from $y$ while $y$ is a right child; the node reached is $\mathrm{left}[x]$ for the only possible $x$. So the paths have at most $n$ nodes in all, and all searches take $O(n)$ time.

So the time is $\Theta(n)$, with about three pointer moves per edge, more than a traversal with a stack. The extra space is $\Theta(1)$: the two pointers $x$ and $p$. The threads use the right pointers that are NIL anyway.

## Properties

- **Constant extra space.** No stack, no parent pointers and no mark bits.
- **Temporary writes.** The tree is changed during the run and restored at the end. Only right pointers that are NIL in the tree are written.
- **Same visit order as inorder.** On a [binary search tree](/binary-search-tree/), the visits come in sorted order of the keys.
- **Not reentrant.** While the walk runs, the tree is not a valid tree: it has cycles through the threads.
- **Deterministic** and not recursive.

## Variants and improvements

- **Preorder.** Visit $x$ at line L6, when the thread is made, instead of at line L7, and keep line L4. This gives the [preorder](/preorder-traversal/) with the same bounds.
- **Postorder.** At line L7, before going right, output the right edge of the left subtree, from $p$ up to $\mathrm{left}[x]$, in reverse. Reversing the path in place and back keeps the space at $O(1)$. A dummy node above the root, with the root as its left child, makes the last path come out too. This gives the [postorder](/postorder-traversal/) in $\Theta(n)$ time.
- **Threaded trees.** A [threaded binary tree](/threaded-binary-tree/) keeps all such threads all the time, with a tag bit on each pointer, and needs no search for the predecessor. Morris traversal makes each thread only when it needs it and needs no tag bits.
- **Pointer reversal.** The Schorr-Waite method used in [mark-and-sweep](/mark-and-sweep/) garbage collection also walks a structure without a stack, but reverses the pointers on the way down and needs a mark bit per node.

## When to use it

Use Morris traversal when the memory for a stack of the height of the tree is not available and the tree may be changed for a short time, for example on a deep or degenerate tree in a small memory, or to find the median or the $k$-th smallest key of a [binary search tree](/binary-search-tree/) with no extra storage. In most programs, a recursive or stack-based [inorder traversal](/inorder-traversal/) is simpler and faster, and it works on a shared or read-only tree.

## Pitfalls

- **Stopping the walk early.** If the walk stops before it ends, for example after the $k$-th node, some threads are still in the tree. Continue the walk without output, or remove the threads, before the tree is used again.
- **Concurrent readers.** Another thread of control that reads the tree during the walk sees the temporary links as children and can loop.
- **The predecessor search must stop at $x$.** The loop of line L5 must test $\mathrm{right}[p] \ne x$, or it follows the thread back into $x$ and loops forever.
- **Trees with parent pointers or shared subtrees.** The method needs a tree in which each node has one parent. If the structure is a DAG, a thread can be made twice and the walk goes wrong.
- **Read-only memory.** The method writes to the tree, so it does not work on a tree in read-only memory or on a persistent tree that other versions share.

## Implementations

## History

Joseph M. Morris published the method in Information Processing Letters in 1979, under the title "Traversing binary trees simply and cheaply". Threaded binary trees, which keep such links all the time, go back to Perlis and Thornton in 1960 and are described by Knuth in the section on traversing binary trees, together with exercises on traversal without a stack. Earlier stackless methods for lists and trees, such as the Schorr-Waite marking algorithm of 1967, reversed pointers and needed extra mark bits. Morris's method needs neither, and it is now a standard example of a traversal in constant extra space.

## References
