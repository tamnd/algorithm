---
tag: JDE4T3
kind: algorithm
slug: inorder-traversal
name: Inorder traversal
aliases:
- LNR traversal
- symmetric order
- symmetric traversal
area: graphs/tree-algorithms
level: intro
summary: Visit left subtree, node, right subtree; yields sorted order on a binary search tree.
solves: [tree-traversal]
model: word-ram
complexity:
  vars: {n: the number of nodes, h: the height of the tree}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(h)}
properties: {deterministic: true, recursive: false}
prereqs: [binary-tree, stack]
see_also: [preorder-traversal, postorder-traversal, level-order-traversal, morris-traversal, threaded-binary-tree, binary-search-tree, tree-sort, cartesian-tree]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1 (Traversing Binary Trees), the definitions of preorder, inorder (symmetric order) and postorder, and Algorithm T (traverse a binary tree in inorder with a stack)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.1 (What is a binary search tree?), the procedure INORDER-TREE-WALK, Theorem 12.1 (the walk takes Θ(n) time) and the exercise on a nonrecursive walk with a stack
  - paper: "Joseph M. Morris, Traversing binary trees simply and cheaply, Information Processing Letters 9(5) (1979), 197-200"
    locator: the inorder traversal with O(1) extra space that threads the tree temporarily
---

Inorder traversal visits the nodes of a [binary tree](/binary-tree/) in the order: the left subtree in inorder, then the root, then the right subtree in inorder. Knuth calls it *symmetric order*. On a [binary search tree](/binary-search-tree/) it lists the keys in sorted order, which is the reason it matters: it turns a search tree into a sorted list in $\Theta(n)$ time, checks the search-tree property, and gives the successor of each node. The version below uses an explicit [stack](/stack/) instead of recursion, takes $\Theta(n)$ time and $\Theta(h)$ extra space for a tree of height $h$, and is Knuth's Algorithm T.

## In plain words

Picture a family tree where each person has at most a left child and a right child. You want to read out every person once, in a fixed order. The rule is: first read out everyone on the left side of a person, then the person, then everyone on the right side, and use the same rule inside each side.

To do this by hand, start at the top and keep going left, and write down on a pile each person you pass. When you cannot go left any more, take the last person from the pile, read that person out, and go one step to the right. Then go left again as far as you can. When the pile is empty and there is nowhere to go, you are done.

## The problem

The input is a binary tree with $n \ge 0$ nodes numbered $0, \ldots, n-1$, rooted at $r$, or empty, with $r = \mathrm{NIL}$. The tree is unweighted. For each node $x$, $left[x]$ and $right[x]$ are its children or NIL; in the code NIL is $-1$. The output is the list of the nodes in inorder, defined recursively by
$$In(\mathrm{NIL}) = (\,), \qquad In(x) = In(left[x]) \cdot (x) \cdot In(right[x]),$$
where $\cdot$ joins lists. Each node appears exactly once. This is one of the orders of the [tree traversal](/tree-traversal/) problem; the others are [preorder](/preorder-traversal/), [postorder](/postorder-traversal/) and [level order](/level-order-traversal/).

## The algorithm

The recursion of the definition is replaced by a stack that holds the nodes whose left subtree is being walked and which are not yet visited.

```pseudo id=main
INORDER(left, right, r)
L1  S ← empty stack;  out ← empty list;  x ← r
L2  while x ≠ NIL or S is not empty do
L3      while x ≠ NIL do                        ▷ go down the left spine of x
L4          push x on S;  x ← left[x]
L5      x ← pop S                                ▷ its left subtree is done
L6      append x to out                          ▷ visit x
L7      x ← right[x]                             ▷ now walk its right subtree
L8  return out
```

Lines L3 and L4 push the left spine of the current subtree: $x$, $left[x]$, $left[left[x]]$, and so on. The node on top of the stack then has an empty left subtree, or one that is already listed, so line L6 visits it, and line L7 starts the same walk on its right subtree. When $x$ is NIL and the stack is empty, every node has been visited.

Each node is pushed once and popped once. The stack holds the nodes on one root-to-node path whose left subtree is being walked, so it never holds more than $h + 1$ nodes. The Python code also counts the pushes and rejects input whose links contain a cycle, which would make the walk run for ever.

## Example

The tree has 6 nodes with the keys $50, 30, 70, 20, 40, 80$ on the nodes $0, \ldots, 5$, so it is a binary search tree:

```
          0 (50)
        /        \
     1 (30)      2 (70)
     /    \          \
  3 (20) 4 (40)     5 (80)
```

$left = [1, 3, -1, -1, -1, -1]$ and $right = [2, 4, 5, -1, -1, -1]$, root 0. The trace, with the stack written bottom to top:

| step | lines | stack after | out after | $x$ after |
|---|---|---|---|---|
| 1 | L3 to L4, three times | 0, 1, 3 | | NIL |
| 2 | L5 to L7 | 0, 1 | 3 | NIL |
| 3 | L5 to L7 | 0 | 3, 1 | 4 |
| 4 | L3 to L4 | 0, 4 | 3, 1 | NIL |
| 5 | L5 to L7 | 0 | 3, 1, 4 | NIL |
| 6 | L5 to L7 | empty | 3, 1, 4, 0 | 2 |
| 7 | L3 to L4 | 2 | 3, 1, 4, 0 | NIL |
| 8 | L5 to L7 | empty | 3, 1, 4, 0, 2 | 5 |
| 9 | L3 to L4 | 5 | 3, 1, 4, 0, 2 | NIL |
| 10 | L5 to L7 | empty | 3, 1, 4, 0, 2, 5 | NIL |

The loop ends, and the output is $3, 1, 4, 0, 2, 5$, with the keys $20, 30, 40, 50, 70, 80$ in sorted order. The stack held at most 3 nodes, which is $h + 1$ for the height $h = 2$.

Three small shapes:

- **Empty tree and one node.** For $r = \mathrm{NIL}$ the loop does not run and the output is empty. For one node the output is $(0)$.
- **A path.** If every node $i < n - 1$ has only the left child $i + 1$, lines L3 and L4 push all $n$ nodes and the output is $n - 1, \ldots, 1, 0$; the stack reaches $n$ entries, which is $h + 1$. If every node has only the right child $i + 1$, the stack never holds more than one node and the output is $0, 1, \ldots, n - 1$.
- **A star.** The largest star that is a binary tree is a root with two leaves; with $left[0] = 1$ and $right[0] = 2$ the output is $1, 0, 2$.

## Correctness

For the state at the test of line L2, with the stack $s_1, \ldots, s_k$ from bottom to top, define the *pending list*
$$pend = In(x) \cdot (s_k) \cdot In(right[s_k]) \cdot (s_{k-1}) \cdot In(right[s_{k-1}]) \cdots (s_1) \cdot In(right[s_1]).$$
The invariant is $out \cdot pend = In(r)$. At the start $out$ and $S$ are empty and $x = r$, so it holds. Lines L3 and L4 replace $In(x)$ by $In(left[x]) \cdot (x) \cdot In(right[x])$ with $x$ on top of the stack, which is the definition of $In(x)$, so $pend$ does not change. Lines L5 to L7 run when $x = \mathrm{NIL}$, so $In(x)$ is empty and $pend$ starts with the top node $s_k$; they move $s_k$ to $out$ and make $In(right[s_k])$ the first part of $pend$, which again keeps $out \cdot pend$ the same. At the end $x = \mathrm{NIL}$ and $S$ is empty, so $pend$ is empty and $out = In(r)$. The loop ends because each node is pushed at most once, as shown in the proof file. The full proof is in the proof file below.

## Complexity

- **Time.** Each node is pushed once in line L4 and popped once in line L5, and each push or pop costs $O(1)$. The outer loop runs once per pop, $n$ times, and the inner loop runs once per push. So the time is $\Theta(n)$ for every tree, with no best or worst case: Theorem 12.1 of CLRS states the same bound for the recursive walk.
- **Space.** Besides the output, the stack holds the nodes of one root-to-node path, so the extra space is at most $h + 1$ words, and a left path makes it $n$. A balanced tree needs $\Theta(\log n)$ and a degenerate one $\Theta(n)$.

## Properties

- **Sorted keys.** A binary tree with keys is a binary search tree, with distinct keys, if and only if its inorder key sequence is strictly increasing. So one traversal checks the search-tree property in $\Theta(n)$ time.
- **Inorder does not fix the tree.** Different binary trees with the same nodes can have the same inorder; all $C_n$ trees on the keys $1, \ldots, n$ in search-tree order have inorder $1, \ldots, n$. Inorder with preorder, or inorder with postorder, does determine a binary tree with distinct labels; preorder with postorder does not.
- **Successor.** The node after $x$ in inorder is the leftmost node of $right[x]$ if that subtree is not empty, and otherwise the nearest ancestor of which $x$ is in the left subtree. This is the TREE-SUCCESSOR of CLRS Section 12.2.
- **Stable under rotations.** A [tree rotation](/tree-rotation/) changes the shape but not the inorder. This is why balanced search trees can rebalance without changing the order of the keys.
- **Online output.** The stack form yields one node at a time and can stop early, which makes it a natural iterator: the first $k$ nodes cost $O(k + h)$ time.

## Variants and improvements

- **Recursive form.** INORDER-TREE-WALK of CLRS: walk the left subtree, print the node, walk the right subtree. It is the shortest code, but its call stack is as deep as the tree, which fails in Python on a path of $10^5$ nodes.
- **[Morris traversal](/morris-traversal/).** Morris (1979) uses the empty right link of the inorder predecessor as a temporary thread back to the node, and removes it on the second visit. It needs $O(1)$ extra space and $O(n)$ time, and changes the tree during the walk.
- **[Threaded binary trees](/threaded-binary-tree/).** If the empty links hold permanent threads to the inorder predecessor and successor, the traversal needs no stack and each successor step takes $O(1)$ amortized time.
- **With parent pointers.** If each node knows its parent, the successor rule above walks the tree in $O(n)$ total time and $O(1)$ extra space without changing it.
- **Reverse inorder.** Swap $left$ and $right$ to list the keys in decreasing order, for example to find the $k$ largest keys of a search tree.
- **Inorder of other trees.** For a [B-tree](/b-tree/) or any ordered tree with keys between children, inorder visits child 0, key 1, child 1, key 2, and so on, and again lists the keys in sorted order.

## When to use it

Use inorder when the order of the left and right subtrees means "smaller" and "larger": to list or iterate the keys of a search tree in order, to check that a tree is a search tree, to find the $k$-th smallest key, to merge two search trees through their sorted lists, or to print an arithmetic expression tree in infix notation (with parentheses added). Use the stack form when the tree can be deep, the recursive form when the height is small, and Morris traversal when no extra memory is allowed. For copying or serializing a tree, [preorder](/preorder-traversal/) is better; for freeing or evaluating it, [postorder](/postorder-traversal/).

## Pitfalls

- **Recursion depth.** A sorted insertion order builds a search tree that is a path. A recursive walk of $10^5$ nodes exceeds the Python recursion limit; the stack form does not.
- **Visiting on push.** Appending $x$ in line L4 instead of line L6 gives preorder, not inorder.
- **Forgetting to go right.** If line L7 sets $x$ to NIL instead of $right[x]$, the right subtrees are never visited, and on the example the output is only $3, 1, 0$. If line L7 is left out, $x$ stays at the popped node, which is pushed again, and the loop never ends.
- **Loop test.** The outer test must be "$x \ne \mathrm{NIL}$ or the stack is not empty". With only the stack test, the loop does not start on a non-empty tree whose stack starts empty, and with only the $x$ test it stops at the first leaf.
- **Duplicate keys.** With equal keys the inorder of a search tree is non-decreasing, not strictly increasing, and the check of the search-tree property must use the same convention as the insertion code.
- **Shared nodes or cycles.** If the links are not a tree, the walk can visit a node twice or loop for ever. The implementation counts pushes and stops after $n$.

## Implementations

## History

The three orders preorder, inorder (symmetric order) and postorder are in Knuth's Section 2.3.1, with Algorithm T for inorder with an auxiliary stack, and the threaded-tree version that needs no stack. Morris published the stack-free traversal by temporary threads in 1979. CLRS uses the recursive walk to print the keys of a binary search tree in sorted order.

## References
