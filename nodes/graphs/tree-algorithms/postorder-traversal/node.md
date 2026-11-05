---
tag: M0CFJK
kind: algorithm
slug: postorder-traversal
name: Postorder traversal
aliases:
- LRN traversal
area: graphs/tree-algorithms
level: intro
summary: Visit all children before the node; the basis of bottom-up evaluation.
solves: [tree-traversal]
model: word-ram
complexity:
  vars: {n: the number of vertices, h: the height of the tree}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(h)}
properties: {deterministic: true, recursive: false}
prereqs: [rooted-tree, tree-traversal, stack]
see_also: [preorder-traversal, inorder-traversal, level-order-traversal, subtree-sizes, expression-tree, depth-first-orders, tree-dynamic-programming, topological-sort]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1 (Traversing binary trees, postorder) and Section 2.3.2 (postorder of a forest, and its use for the evaluation of expressions)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.1, the postorder tree walk
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Section 5.6, Tree traversal (postorder, and its use for the evaluation of postfix expressions)
---

Postorder traversal lists the vertices of a [rooted tree](/rooted-tree/) so that the subtrees of the children of a vertex come first, from the first child to the last, and the vertex itself comes last. It is the order in which a [depth-first search](/depth-first-search/) of the tree finishes the vertices. Because each vertex comes after all of its descendants, postorder is the order of each bottom-up computation on a tree: [subtree sizes](/subtree-sizes/), heights, the value of an [expression tree](/expression-tree/), and [tree dynamic programming](/tree-dynamic-programming/). This version uses an explicit [stack](/stack/), so it runs in $\Theta(n)$ time with $\Theta(h)$ extra space and does not overflow the call stack on deep trees.

## In plain words

Walk down the tree as in a depth-first search: go into the first child, then into its first child, and so on. When you are about to leave a node for the last time, because all its children are done, write it down. So a node is written only after everything below it.

That is the order you need when a node's answer depends on its children's answers. To get the total size of a folder, you first need the sizes of the folders inside it. To get the value of a formula such as "two plus three, times ten", you first need the value of "two plus three". The walk keeps a pile of the nodes on the way from the top, so it needs as much memory as the tree is deep.

## The problem

The input is an ordered rooted tree with the vertices $0, \ldots, n-1$, $n \ge 1$: a root $r$ and the list $C[v]$ of the children of each vertex $v$, in order. The tree is not weighted. The output is the postorder $\mathrm{post}(T_r)$, where $\mathrm{post}(T_v) = \mathrm{post}(T_{c_1}), \ldots, \mathrm{post}(T_{c_k}), v$ for $C[v] = [c_1, \ldots, c_k]$. This is one of the orders of the [tree traversal](/tree-traversal/) problem.

## The algorithm

```pseudo id=main
POSTORDER(C, r)                         ▷ C[v] lists the children of v in order
L1  out ← empty list
L2  S ← a stack that holds the pair (r, 0)
L3  while S is not empty do
L4      (v, i) ← TOP(S)                 ▷ i children of v are already entered
L5      if i < |C[v]| then
L6          TOP(S) ← (v, i + 1)
L7          PUSH(S, (C[v][i], 0))
L8      else
L9          POP(S)
L10         append v to out             ▷ all children of v are already in out
L11 return out
```

The stack holds the path from the root to the current vertex. The pair $(v, i)$ says that the walk has entered $i$ children of $v$. When $i$ reaches the number of children, the walk leaves $v$ for good, and line L10 writes it. The only change from [preorder](/preorder-traversal/) is the place where a vertex is written: there it is written when it is pushed, here when it is popped.

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
| 1 | push 1 | (0,1) (1,0) | |
| 2 | push 3 | (0,1) (1,1) (3,0) | |
| 3 | pop 3 | (0,1) (1,1) | 3 |
| 4 | push 4 | (0,1) (1,2) (4,0) | 3 |
| 5 | push 6 | (0,1) (1,2) (4,1) (6,0) | 3 |
| 6 | pop 6 | (0,1) (1,2) (4,1) | 3 6 |
| 7 | push 7 | (0,1) (1,2) (4,2) (7,0) | 3 6 |
| 8 | pop 7 | (0,1) (1,2) (4,2) | 3 6 7 |
| 9 | pop 4 | (0,1) (1,2) | 3 6 7 4 |
| 10 | pop 1 | (0,1) | 3 6 7 4 1 |
| 11 | push 2 | (0,2) (2,0) | 3 6 7 4 1 |
| 12 | push 5 | (0,2) (2,1) (5,0) | 3 6 7 4 1 |
| 13 | pop 5 | (0,2) (2,1) | 3 6 7 4 1 5 |
| 14 | pop 2 | (0,2) | 3 6 7 4 1 5 2 |
| 15 | pop 0 | empty | 3 6 7 4 1 5 2 0 |

The postorder is $3, 6, 7, 4, 1, 5, 2, 0$. Each vertex appears after all of its children, and the root is last.

A second example is bottom-up evaluation. The expression tree with root "$\times$", whose children are "$+$" over the leaves $2, 3$ and "$+$" over the leaves $4, 1, 5$, has the postorder $2, 3, +, 4, 1, 5, +, \times$. Evaluated in this order, the first "$+$" gives $5$, the second gives $10$, and the root gives $50$.

On the single vertex the output is $[0]$. On the path $0, 1, \ldots, n-1$ rooted at $0$, it is $n-1, \ldots, 1, 0$, and the stack grows to $n$ pairs. On the star with centre $0$, it is $1, 2, \ldots, n-1, 0$.

## Correctness

The key fact is about one subtree: if the walk pushes $(v, 0)$, then from that moment until $(v, \cdot)$ is popped, it appends exactly $\mathrm{post}(T_v)$ to out, the last entry being $v$ at the pop, and it does not touch the stack below $(v, \cdot)$. The proof is by induction on the height of $v$, with an inner induction over the children of $v$: between the step that raises $i$ to $j$ and the step that reads $(v, j)$ again, the walk appends $\mathrm{post}(T_{c_j})$. Applied to the root, this gives $\mathrm{out} = \mathrm{post}(T_r)$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the child lists as arrays.

- Each vertex other than the root is pushed once at line L7, and each vertex is popped once at line L9. Each iteration does one of the two, so the loop runs $2n - 1$ times, with $O(1)$ work each time.
- The stack holds the vertices of one path from the root, so it never holds more than $h + 1$ pairs, and it holds $h + 1$ when the walk is at a deepest leaf.

So the time is $\Theta(n)$ on every tree, and the extra space, apart from the output, is $\Theta(h)$: $\Theta(n)$ on a path and $\Theta(\log n)$ on a balanced binary tree.

## Properties

- **Deterministic and not recursive.** The order is fixed by the tree, and the explicit stack replaces the call stack.
- **Descendants first.** Each vertex comes after all of its proper descendants. So the postorder is a [topological order](/topological-sort/) of the tree with each edge directed from child to parent, and each bottom-up recurrence $f(v) = g(v, f(c_1), \ldots, f(c_k))$ can be computed in one pass over it.
- **Subtrees are contiguous.** The vertices of $T_v$ form a contiguous block of the postorder that ends with $v$.
- **Reverse postorder.** The reverse of the postorder is the preorder of the mirror tree, in which each child list is reversed. In a directed acyclic graph, the reverse postorder of a depth-first search is a topological order, as on the page on [depth-first orders](/depth-first-orders/).
- **Postfix notation.** The postorder of an expression tree, with each operator at its vertex, is the expression in postfix (reverse Polish) notation, which a stack machine evaluates left to right.

## Variants and improvements

- **Recursive form.** Call the procedure on each child, then VISIT$(v)$. It is short, but it needs a call stack of depth $h + 1$.
- **Reverse of a modified preorder.** Pop a vertex, write it, and push its children in their natural order. The output is the preorder of the mirror tree. Reversing it gives the postorder. This needs a second list and a stack of up to $\Theta(n)$ vertices.
- **Binary trees with one stack.** For a binary tree, keep the last vertex written. A vertex on the top of the stack is written when its right child is missing or was just written. This is the classic iterative postorder of binary trees.
- **Order from a parent array.** If the vertices are numbered so that each parent has a smaller number than its children (for example a BFS or preorder numbering), then processing the vertices from $n - 1$ down to $0$ visits each vertex after its children. This is not the postorder, but it serves each bottom-up computation with no stack at all.
- **Single pass for all results.** Most uses do not need the list. They do the work of line L10 in place: add the size of $v$ to its parent, or combine the values of the children.

## When to use it

Use postorder whenever a vertex needs the results of its children: sizes, heights, sums, the value of an expression, the dynamic programs of [maximum independent set in trees](/maximum-independent-set-in-trees/) and other tree problems, and freeing a tree before its root. Use [preorder](/preorder-traversal/) for work that flows from the root down, and both in one walk (preorder at the push, postorder at the pop) when a computation needs a downward and an upward pass, as in the [rerooting technique](/rerooting-technique/).

## Pitfalls

- **Writing at the push.** Writing $v$ when $(v, 0)$ is pushed gives the preorder. The write belongs at line L10, after the test of line L5 fails.
- **Deep recursion.** The recursive form overflows the call stack on a path of $10^5$ vertices in Python. Keep the explicit stack of lines L2 to L10.
- **Popping too early.** A one-stack version that pops a vertex as soon as it is on top, without the child counter of line L4, writes the vertex before its later children. Each stack entry must know how many children are done.
- **Parent edges.** On an undirected adjacency list, skip the parent of $v$ when you push its neighbours, or the walk goes back up.

## Implementations

## History

Knuth defines postorder for binary trees in the section on traversing binary trees, and postorder of a forest in the next section, where he relates it to the evaluation of expressions. Older texts, including earlier editions of Knuth's volume, used other names for some of these orders, so the definition in an old source must be checked before its results are used. CLRS give the postorder tree walk next to the inorder and preorder walks.

## References
