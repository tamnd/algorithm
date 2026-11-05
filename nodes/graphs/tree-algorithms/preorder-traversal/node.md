---
tag: K1CRY0
kind: algorithm
slug: preorder-traversal
name: Preorder traversal
aliases:
- NLR traversal
- depth-first tree visit
area: graphs/tree-algorithms
level: intro
summary: Visit each node before its subtrees; a DFS of a tree.
solves: [tree-traversal]
model: word-ram
complexity:
  vars: {n: the number of vertices, h: the height of the tree}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(h)}
properties: {deterministic: true, recursive: false}
prereqs: [rooted-tree, tree-traversal, stack]
see_also: [postorder-traversal, inorder-traversal, level-order-traversal, depth-first-search, depth-first-orders, euler-tour-technique, morris-traversal, iterative-depth-first-search]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1 (Traversing binary trees, the definitions of preorder, inorder and postorder) and Section 2.3.2 (preorder of a forest and its relation to the binary tree representation)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.1, the preorder tree walk, and Section 10.3 (Representing rooted trees, left-child right-sibling form)
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Section 5.6, Tree traversal (recursive preorder and the nonrecursive preorder with an explicit stack)
---

Preorder traversal lists the vertices of a [rooted tree](/rooted-tree/) so that each vertex comes before its subtrees, and the subtrees of its children come one after the other, from the first child to the last. It is the order in which a [depth-first search](/depth-first-search/) of the tree first reaches each vertex. This version keeps an explicit [stack](/stack/) of (vertex, next child) pairs instead of recursion, so it runs in $\Theta(n)$ time with $\Theta(h)$ extra space for a tree of height $h$, and it does not overflow the call stack on a path of $10^5$ vertices.

## In plain words

Start at the top of the tree and write it down. Then go to its first child, write that down, and keep going down to the first child of each new node. When a node has no child left to visit, step back up to its parent and try the parent's next child. Each node is written the first time you arrive at it.

To remember where you are, keep a pile of the nodes on the way from the top to where you stand, and for each of them the number of children you have already entered. The pile is as tall as the tree is deep. The result is the order of a table of contents: a chapter, then all its sections, then the next chapter.

## The problem

The input is an ordered rooted tree with the vertices $0, \ldots, n-1$, $n \ge 1$: a root $r$ and, for each vertex $v$, the list $C[v]$ of its children in order. The tree is not weighted. The output is the preorder $\mathrm{pre}(T_r)$, defined by $\mathrm{pre}(T_v) = v, \mathrm{pre}(T_{c_1}), \ldots, \mathrm{pre}(T_{c_k})$ where $c_1, \ldots, c_k$ is $C[v]$. This is one of the orders of the [tree traversal](/tree-traversal/) problem.

## The algorithm

```pseudo id=main
PREORDER(C, r)                          ▷ C[v] lists the children of v in order
L1  out ← [r]
L2  S ← a stack that holds the pair (r, 0)
L3  while S is not empty do
L4      (v, i) ← TOP(S)                 ▷ i children of v are already entered
L5      if i < |C[v]| then
L6          TOP(S) ← (v, i + 1)
L7          c ← C[v][i]
L8          append c to out
L9          PUSH(S, (c, 0))
L10     else POP(S)                     ▷ the whole subtree of v is listed
L11 return out
```

The stack holds the path from the root to the current vertex. The number $i$ in the pair of a vertex $v$ says how many children of $v$ the walk has already entered. Line L8 writes a vertex at the moment the walk enters it, which is what makes the order a preorder. Moving line L8 to line L10, so that a vertex is written when it is popped, gives [postorder](/postorder-traversal/).

## Example

The tree on $\{0, \ldots, 7\}$ rooted at $0$ has $C[0] = [1, 2]$, $C[1] = [3, 4]$, $C[2] = [5]$, $C[4] = [6, 7]$, and the other lists are empty.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

| step | action | stack after the step (bottom to top) | out |
|---|---|---|---|
| 0 | start | (0,0) | 0 |
| 1 | push 1 | (0,1) (1,0) | 0 1 |
| 2 | push 3 | (0,1) (1,1) (3,0) | 0 1 3 |
| 3 | pop 3 | (0,1) (1,1) | |
| 4 | push 4 | (0,1) (1,2) (4,0) | 0 1 3 4 |
| 5 | push 6 | (0,1) (1,2) (4,1) (6,0) | 0 1 3 4 6 |
| 6 | pop 6 | (0,1) (1,2) (4,1) | |
| 7 | push 7 | (0,1) (1,2) (4,2) (7,0) | 0 1 3 4 6 7 |
| 8 | pop 7 | (0,1) (1,2) (4,2) | |
| 9 | pop 4 | (0,1) (1,2) | |
| 10 | pop 1 | (0,1) | |
| 11 | push 2 | (0,2) (2,0) | 0 1 3 4 6 7 2 |
| 12 | push 5 | (0,2) (2,1) (5,0) | 0 1 3 4 6 7 2 5 |
| 13 | pop 5 | (0,2) (2,1) | |
| 14 | pop 2 | (0,2) | |
| 15 | pop 0 | empty | |

The output is $0, 1, 3, 4, 6, 7, 2, 5$. The loop ran $15 = 2n - 1$ times: $7$ pushes and $8$ pops. The stack never held more than $4 = h + 1$ pairs, for the height $h = 3$.

On the single vertex, the loop pops the root once and the output is $[0]$. On the path $0, 1, \ldots, n-1$ rooted at $0$, the stack grows to $n$ pairs and the output is $0, 1, \ldots, n-1$. On the star with centre $0$, the stack never holds more than 2 pairs and the output is $0, 1, \ldots, n-1$.

## Correctness

The key fact is about one subtree. If the walk pushes $(v, 0)$ just after it writes $v$, then from that moment until $(v, \cdot)$ is popped, it writes exactly $\mathrm{pre}(T_v)$ without its first entry $v$, and it does not change the stack below $(v, \cdot)$. This follows by induction on the height of $v$: the pair of $v$ goes through $i = 0, 1, \ldots, |C[v]|$, and between two steps the walk handles the whole subtree of one child, by the hypothesis. Applied to the root, the claim gives $\mathrm{out} = \mathrm{pre}(T_r)$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the child lists as arrays.

- Each vertex other than the root is pushed once, by its parent at line L9, and each vertex is popped once at line L10. Each iteration of the loop does one push or one pop, so the loop runs $(n - 1) + n = 2n - 1$ times.
- Each iteration does $O(1)$ work.

So the time is $\Theta(n)$ on every tree, in the best, average and worst case. The stack holds the path from the root to the current vertex, so its size is at most $h + 1$, and it reaches $h + 1$ when the walk enters a deepest leaf. The extra space is $\Theta(h)$, apart from the output list. This is $\Theta(n)$ on a path and $\Theta(\log n)$ on a balanced binary tree.

## Properties

- **Deterministic.** The order is fixed by the tree and the order of the child lists.
- **Not recursive.** The explicit stack replaces the call stack, so deep trees are safe in languages with a small call stack, such as Python.
- **Each subtree is a contiguous block.** The vertices of $T_v$ occupy positions $\mathrm{tin}(v)$ to $\mathrm{tin}(v) + |T_v| - 1$ of the output, where $\mathrm{tin}(v)$ is the position of $v$. This is the base of [Euler tour subtree queries](/euler-tour-subtree-queries/).
- **Ancestors first.** Each vertex comes after all of its proper ancestors. So a preorder is a [topological order](/topological-sort/) of the tree with edges directed away from the root.

## Variants and improvements

- **Recursive form.** VISIT$(v)$; then call the procedure on each child. It is shorter, but it uses a call stack of depth $h + 1$, which is $10^5$ frames on a path of $10^5$ vertices.
- **Push all children.** Pop a vertex, write it, and push its children in reverse order. This is shorter than the version above, but the stack can hold $\Theta(n)$ vertices: on a star it holds $n - 1$ at once.
- **Binary trees.** With a left and a right pointer, push the right child before the left child, or use [Morris traversal](/morris-traversal/) in its preorder form for $O(1)$ extra space.
- **Parent pointers.** With a parent pointer and a next-sibling pointer at each vertex, the walk can go down to the first child, across to the next sibling, and up to the parent, with $O(1)$ extra space.
- **Entry and exit times.** Record the step at line L8 as $\mathrm{tin}(c)$ and the step at line L10 as $\mathrm{tout}(v)$. Then $u$ is an ancestor of $v$ if and only if $\mathrm{tin}(u) \le \mathrm{tin}(v)$ and $\mathrm{tout}(v) \le \mathrm{tout}(u)$, as in the [parenthesis theorem](/parenthesis-theorem/) of depth-first search.
- **Unrooted input.** For a free tree given as an edge list, keep the parent of each vertex on the stack and skip the edge back to it. This roots the tree and lists it in preorder in one pass, as in [tree rooting](/tree-rooting/).

## When to use it

Use preorder when the work at a vertex must happen before the work in its subtree: to copy or serialize a tree, to push values from the root down (depths, prefix sums along root paths), to print an indented outline, or to number the vertices so that subtrees become intervals. Use [postorder](/postorder-traversal/) when a vertex needs the results of its children, and [level order](/level-order-traversal/) when the depth matters more than the subtree.

## Pitfalls

- **Deep recursion.** The recursive form fails with a stack overflow on a path with about $10^4$ to $10^5$ vertices in Python and other languages with a limited call stack. Keep the explicit stack of lines L2 to L10.
- **Wrong push order.** In the push-all-children variant, pushing the children in their natural order lists them in reverse. Push them from last to first.
- **Writing at the pop.** Appending $v$ at line L10 instead of at line L8 gives the postorder, not the preorder.
- **Edge lists without a parent check.** On an undirected adjacency list, each child also lists its parent. Without a test that skips the parent, the walk goes back up and loops for ever.

## Implementations

## History

Knuth gives the three classic orders of a binary tree, preorder, inorder and postorder, in the section on traversing binary trees in the first volume of The Art of Computer Programming, and he extends preorder to forests through the binary tree representation of a forest. CLRS present the preorder tree walk next to the inorder walk of binary search trees. Sedgewick gives both the recursive and the stack-based forms.

## References
