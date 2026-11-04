---
tag: EJENNS
kind: data-structure
slug: threaded-binary-tree
name: Threaded binary tree
aliases:
- threaded BST
area: data-structures/search-trees
level: intro
summary: BST whose null child pointers link to in-order predecessor or successor, enabling stackless traversal.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), amortized: O(1)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binary-search-tree, inorder-traversal]
see_also: [morris-traversal, tree-traversal, bst-insertion, parent-pointer-tree, binary-tree, ordered-set]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.1 (Traversing binary trees), threaded trees, Algorithm S (symmetric successor) and Algorithm I (insertion into a threaded tree)
  - paper: doi:10.1145/367177.367202
    title: Alan J. Perlis and Charles Thornton, Symbol manipulation by threaded lists, Communications of the ACM 3(4), 1960
    locator: pages 195 to 204
---

A threaded binary tree is a [binary search tree](/binary-search-tree/) in which each empty child field holds a *thread* instead of NIL: an empty left field points to the in-order predecessor of the node, and an empty right field points to its in-order successor. One bit per field tells a thread from a real child. With threads, the in-order successor of each node is found without a stack and without parent pointers, so a full [in-order traversal](/inorder-traversal/) takes $\Theta(n)$ time and $O(1)$ extra space. Perlis and Thornton introduced threads in 1960, and Knuth gives the standard algorithms in Volume 1, Section 2.3.1.

## In plain words

A tree with a number of nodes has one more empty child slot than nodes, so about half of all child slots in a tree are empty. A threaded tree puts these slots to work. Each empty right slot points to the node that comes next in sorted order, and each empty left slot points to the node that comes just before.

To walk the keys in order, start at the smallest. From any node, if its right slot is a thread, follow it: that is the next key. If it is a real child, go there and then left as far as you can. No list of nodes to come back to is needed, because the threads already say where to go back to.

## The abstract type

A threaded BST implements the [ordered set](/ordered-set/) operations search, insert, minimum, maximum, successor and predecessor, and an in-order iteration. The threads change only the cost of successor, predecessor and iteration: they become $O(1)$ amortized over a walk, in $O(1)$ extra space, without parent pointers. Search and insert work as in a plain BST.

## Representation

Each node $x$ has a key $x.key$, two link fields $x.left$ and $x.right$, and two tag bits $x.lthread$ and $x.rthread$.

- If $x.lthread$ is false, $x.left$ is the left child. If it is true, $x.left$ is a thread to the in-order predecessor of $x$, or NIL if $x$ holds the smallest key.
- If $x.rthread$ is false, $x.right$ is the right child. If it is true, $x.right$ is a thread to the in-order successor of $x$, or NIL if $x$ holds the largest key.

**Invariant.**

- **(H1) Order.** The tree formed by the child links (the links whose tag is false) has the [binary search tree property](/binary-search-tree-property/) with distinct keys.
- **(H2) Threads.** If $x_1, x_2, \ldots, x_n$ is the in-order sequence of the nodes in the tree of child links, then for each $i$: if $x_i.lthread$ then $x_i.left = x_{i-1}$ (NIL for $i = 1$), and if $x_i.rthread$ then $x_i.right = x_{i+1}$ (NIL for $i = n$).

A tree with $n \ge 1$ nodes has $n - 1$ child links and $2n$ link fields, so it has $n + 1$ threads; exactly two of them, the left thread of $x_1$ and the right thread of $x_n$, are NIL. Knuth adds a header node so that these two threads also point to a node, which removes the tests for NIL. The cost is two bits per node, often hidden in the low bits of an aligned pointer.

## Operations

```pseudo id=main
SUCCESSOR(x)                                 ▷ the in-order successor of x, or NIL
L1  if x.rthread then return x.right         ▷ a thread points straight to it
L2  y ← x.right
L3  while not y.lthread do y ← y.left        ▷ leftmost node of the right subtree
L4  return y

INSERT(T, k)
L5  if T.root = NIL then T.root ← a node (k) with both tags true and both links NIL; return
L6  x ← T.root
L7  loop
L8      if k = x.key then return                     ▷ already a key
L9      if k < x.key then
L10         if not x.lthread then x ← x.left; continue
L11         z ← a node (k), both tags true; z.left ← x.left; z.right ← x; x.left ← z; x.lthread ← false; return
L12     if not x.rthread then x ← x.right; continue
L13     z ← a node (k), both tags true; z.left ← x; z.right ← x.right; x.right ← z; x.rthread ← false; return
```

**Successor.** If the right field is a thread, it is the answer (line L1). Else the successor is the leftmost node of the right subtree (lines L2 to L4). The walk of line L3 stops at a node whose left field is a thread; it never follows a thread. PREDECESSOR is the mirror image. The cost is $O(h)$ in the worst case.

**In-order walk.** Start at the minimum (go left from the root while the left tag is false), then apply SUCCESSOR until it returns NIL. Each child link is followed down exactly once, by line L3 or by the walk to the minimum, and each thread is followed exactly once, by line L1, so the walk takes $\Theta(n)$ time and $O(1)$ extra space.

**Search.** As in a plain BST, except that a thread stops the search as NIL would: when the search wants to go left at a node whose left field is a thread, the key is absent.

**Insert.** Lines L6 to L12 walk down as in [BST insertion](/bst-insertion/), with threads in the place of NIL. A new left child $z$ of $x$ (line L11) comes just before $x$ in in-order, so $z$ takes over the old left thread of $x$, which points to the predecessor of $x$, and its right thread points to $x$. A new right child (line L13) is the mirror case. Only $O(1)$ fields change after the walk, so the cost is $O(h)$.

**Delete.** Deletion is possible but has more cases than in a plain BST, because the threads that point to the removed node must be redirected. When a node with two children is replaced by its successor, the thread that pointed to the successor must be moved too. The Python code does not include it.

## Example

Insert 50, 30, 70, 20, 40, 60 and 80, then 45. The table lists the threads of each node that has one; "child" means a real child link.

| node | left field | right field |
|---|---|---|
| 50 | child 30 | child 70 |
| 30 | child 20 | child 40 |
| 70 | child 60 | child 80 |
| 20 | thread NIL (smallest key) | thread to 30 |
| 40 | thread to 30 | thread to 50 |
| 60 | thread to 50 | thread to 70 |
| 80 | thread to 70 | thread NIL (largest key) |

Seven nodes have $7 + 1 = 8$ threads. Now insert 45. The walk goes $50 \to 30 \to 40$; at 40 the right field is a thread, so line L13 runs: the new node 45 gets the left thread to 40 and the right thread to 50 (the old right thread of 40), and 40 gets 45 as its right child.

| node | left field | right field |
|---|---|---|
| 40 | thread to 30 | child 45 |
| 45 | thread to 40 | thread to 50 |

The in-order walk from 20 follows: thread to 30; child 40 and no left child, so 40; child 45, so 45; thread to 50; child 70, then left to 60; thread to 70; child 80. The keys are 20, 30, 40, 45, 50, 60, 70, 80, with no stack.

## Correctness

SUCCESSOR is right by (H2) when the right field is a thread. When it is a child, the successor is the minimum of the right subtree, as in a plain BST, and line L3 finds it because a left tag is false exactly when there is a left child. INSERT keeps (H1) as leaf insertion does. It keeps (H2) because the new node $z$ lands between two in-order neighbours, $x$ and the old target of the thread of $x$ that $z$ replaces, and $z$ gets exactly these two nodes as its threads. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | cost |
|---|---|
| search | $O(h)$ worst |
| insert | $O(h)$ worst |
| minimum, maximum | $O(h)$ worst |
| successor, predecessor | $O(h)$ worst; $O(1)$ amortized over a full walk |
| in-order walk of all keys | $\Theta(n)$ time, $O(1)$ extra space |
| space | $\Theta(n)$ words plus $2n$ tag bits |

A plain BST without parent pointers needs a stack of size $\Theta(h)$ for a walk, and a BST with parent pointers needs one more pointer per node. The threads give the same walk at the cost of two bits per node. The height is as in a plain BST: up to $n - 1$ for sorted input.

## Variants

- **Right-threaded trees.** Only the empty right fields hold threads, which is enough for in-order walks forward. This halves the cost of the tag updates.
- **Header node.** Knuth's form adds a header whose left link is the root and whose threads close the cycle, so the in-order sequence is circular and no thread is NIL.
- **Threads in other orders.** Threads can point to the preorder or postorder neighbours instead.
- **Temporary threads.** [Morris traversal](/morris-traversal/) adds threads during a walk of an ordinary binary tree and removes them again, which gives an $O(1)$-space walk without permanent tag bits.
- **Parent pointers.** A [parent-pointer tree](/parent-pointer-tree/) gives the same successor walk with one more pointer per node and simpler updates.

## When to use it

Use a threaded tree when in-order walks are frequent, memory is tight, and parent pointers are not wanted, for example in old systems with small memories or in embedded code. In most modern code, parent pointers or an explicit stack are simpler, and a balanced tree is needed anyway for its height. Threads make deletion and rotations more complex, so balanced threaded trees are rare.

## Pitfalls

- **Following a thread as a child.** A search or a walk that ignores the tag bits treats a thread as a child and loops forever or returns a wrong node. Each move down must test the tag first, as lines L3, L10 and L12 do.
- **Wrong threads for the new node.** In line L11 the new left child must inherit the *old left thread of $x$* as its left thread. Setting it to NIL, or to $x$, breaks the predecessor of $z$.
- **Forgetting to clear the tag.** After line L11 or L13, the tag of $x$ on that side must become false. Else $x$ still sees a thread, and the new node is lost to searches.
- **Deleting without fixing threads.** Removing a leaf by setting its parent's field to NIL leaves a NIL where a thread must be, and leaves other threads pointing to a freed node. The parent's field must take over the thread of the removed leaf.

## Implementations

The Python class is a fully threaded BST without a header node, with the two tags as booleans. It has search, insert, successor, predecessor and a stackless in-order iterator.

## History

Alan Perlis and Charles Thornton introduced threaded lists in 1960, as a way to traverse list structures without a stack. Knuth, in Volume 1, Section 2.3.1, gives the threaded representation of binary trees, the algorithm for the symmetric-order successor, and insertion into a threaded tree, and credits the idea to Perlis and Thornton.

## References
