---
tag: Q9AZES
kind: data-structure
slug: rank-pairing-heap
name: Rank-pairing heap
aliases:
- rank-pairing heaps
area: data-structures/heaps
level: research
summary: Heap combining rank-based linking with pairing that matches Fibonacci heap bounds.
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(n), amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [fibonacci-heap, pairing-heap, binomial-heap, decrease-key, potential-method]
see_also: [fibonacci-heap, pairing-heap, thin-heap, hollow-heap, violation-heap, strict-fibonacci-heap, weak-heap, dijkstra]
sources:
  - paper: doi:10.1137/100785351
    title: Bernhard Haeupler, Siddhartha Sen and Robert E. Tarjan, Rank-pairing heaps, SIAM Journal on Computing 40(6), 2011
    locator: pages 1463 to 1485; Section 3 (half trees and links), Section 4 (lazy binomial queues, one-pass and multipass linking), Section 5 (type-1 and type-2 rank rules, rank reduction, Lemmas 5.1 to 5.3), Section 6 (Theorem 6.1 and the type-1 analysis), Section 8 (simpler key decreases that fail)
  - paper: "Bernhard Haeupler, Siddhartha Sen and Robert E. Tarjan, Rank-pairing heaps, Proceedings of the 17th European Symposium on Algorithms (ESA), 2009"
    locator: pages 659 to 670, the conference version
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: the bounds that rank-pairing heaps match
---

A rank-pairing heap is a set of *half trees*, binary trees with a key order only toward the left, in which each node has a rank and ranks control which trees are linked. It has the amortized bounds of the [Fibonacci heap](/fibonacci-heap/): $O(1)$ for insert, find-min, meld and [decrease-key](/decrease-key/), and $O(\log n)$ for delete-min. Like a [pairing heap](/pairing-heap/), it does at most one cut per decrease-key and no other restructuring: the only thing that can cascade is a series of rank changes. Bernhard Haeupler, Siddhartha Sen and Robert Tarjan introduced it in 2009. This page describes the type-2 version with multipass linking, which is the version with the simpler analysis.

## In plain words

A heap is a list of trees. Each tree is a binary tree in which every item is no larger than anything in its left subtree, and the root has no right subtree. Each item also has a rank, which is about the logarithm of the size below it.

To join two trees of the same rank, compare the two roots. The loser goes under the winner, and the rank of the winner goes up by one. A delete-min breaks the tree of the minimum into smaller trees and joins trees of equal rank until all ranks differ.

To lower a key, cut the item out with its left subtree, and put its right subtree in its place. The ranks above the cut may now be too high. Walk up and lower them until a rank does not change.

## The abstract type

A rank-pairing heap implements the [meldable priority queue](/meldable-priority-queue/) with decrease-key: `insert(k)` returns a handle, and there are `find-min()`, `delete-min()`, `meld(H1, H2)` and `decrease-key(handle, k)`. This page uses a min-heap. Delete of an arbitrary item is decrease-key to $-\infty$ and then delete-min.

## Representation

Each node $x$ has a key, a rank $r(x)$ and three pointers: $left$, $right$ and $parent$. A missing child has rank $-1$. The roots are in a list, with a pointer $min$ to the root of smallest key. The implementation links the roots with a fourth field, $next$; the paper uses the empty right pointer of a root for this.

**Half trees.** A *half tree* is a binary tree whose root has no right child. It is *half-ordered* if the key of each node is at most every key in its left subtree. A half tree is the binary (left child, right sibling) form of a heap-ordered tree: the left child of a node is its first child, and the right child is its next sibling. So the root of a half tree holds its smallest key.

**Rank differences.** For a child $x$ with parent $p$, the *rank difference* is $\Delta(x) = r(p) - r(x)$. A non-root whose two children (one or both may be missing) have rank differences $i$ and $j$ is an *$i,j$-node*; the order of $i$ and $j$ does not matter. A root whose left child has rank difference $i$ is an *$i$-node*.

**Invariants.**
1. *Half order* in every half tree.
2. *Type-2 rank rule.* Every root is a 1-node: $r(x) = r(x.left) + 1$. Every non-root is a 1,1-node, a 1,2-node, or a 0,$i$-node with $i > 1$.

The rule fixes the rank of a non-root from the ranks $a \ge b$ of its children: it is $a$ when $a - b > 1$, and $a + 1$ when $a - b \le 1$. Call this value $f(a, b)$.

**Rank bound.** A child of rank $k$ has at least $F_{k+3} - 1$ nodes in its subtree, and a root of rank $k$ has at least $F_{k+2} \ge \varphi^k$ nodes in its half tree, where $F$ is the [Fibonacci sequence](/fibonacci-numbers/) with $F_0 = 0$ and $\varphi$ is the golden ratio (Lemma 5.3 of the paper). So every rank is at most $\log_\varphi n$.

## Operations

```pseudo id=main
LINK(x, y)                              ▷ roots of two half trees of equal rank
L1  if y.key < x.key then swap x and y  ▷ x wins
L2  y.right ← x.left; x.left ← y; r(x) ← r(x) + 1; return x

INSERT(H, k)
L3  add a new node of rank 0 to the root list; update H.min

DELETE-MIN(H)                           ▷ H is not empty
L4  z ← H.min; make each node s on the right spine of z.left a root, with s.right ← NIL and r(s) ← r(s.left) + 1
L5  for each half tree x, the new ones first: while the bucket of rank r(x) holds y: empty it; x ← LINK(x, y)
L6      put x in the bucket of rank r(x)
L7  make the buckets the root list; H.min ← the smallest root; return z.key

DECREASE-KEY(H, x, k)                   ▷ k ≤ x.key
L8  x.key ← k; if x is a root then update H.min and return
L9  u ← x.parent; y ← x.right; put y in the place of x as a child of u; x.right ← NIL; r(x) ← r(x.left) + 1; add x to the root list
L10 while u ≠ NIL                       ▷ rank reduction
L11     if u is a root then r(u) ← r(u.left) + 1; return
L12     k ← f(r(u.left), r(u.right))
L13     if k ≥ r(u) then return
L14     r(u) ← k; u ← u.parent
```

**Link** (lines L1 and L2) is the link of half trees: the old left subtree of the winner $x$ becomes the right subtree of the loser $y$, and $y$ becomes the left child of $x$. In the heap-ordered view, $y$ becomes the first child of $x$. Both roots had rank $k$ and were 1-nodes, so the loser has two children of rank $k - 1$ and is a 1,1-node, and the winner is a 1-node of rank $k + 1$.

**Delete-min** (lines L4 to L7) deletes the root $z$ of minimum key. The nodes on the right spine of $z.left$, the path from $z.left$ through right children, are the nodes that lost links to $z$. Each of them, with its left subtree, becomes a new half tree, and gets the rank that makes it a 1-node. Then the half trees are processed with one bucket per rank: if the bucket of the rank of a tree is full, the two trees are linked and the result is processed again; otherwise the tree goes into the bucket. This is *multipass linking*. At the end, all roots have distinct ranks.

**Decrease-key** (lines L8 to L14) lowers the key of $x$. If $x$ is not a root, line L9 detaches $x$ with its left subtree and puts the right subtree of $x$ in the place of $x$. This is the only change of structure. Now $x$ is a root, and gets the rank $r(x.left) + 1$. The new child of $u$ has a rank at most that of $x$, so $u$ may now break the rank rule. Lines L10 to L14 walk up: each step gives $u$ the rank $f$ of its children, and stops when this rank does not go down. At a root, line L11 fixes the rank to make the root a 1-node.

**Insert, meld and find-min.** Insert adds a one-node half tree of rank 0 (line L3). Meld joins the two root lists and keeps the smaller minimum. Find-min returns $H.min$.

## Example

Write a half tree as key:rank(left, right), with "-" for a missing child and a leaf as key:rank alone. Insert 10, 20, ..., 90 and delete the minimum. The delete-min returns 10, links the 8 other roots in 7 links, and leaves one half tree:

20:3(60:2(80:1(90:0, 70:0), 40:1(50:0, 30:0)), -)

In the heap-ordered view, 20 has the children 60, 40 and 30, and 60 has the children 80 and 70. Every non-root here is a 1,1-node.

**Decrease 30 to 25.** Node 30 is the right child of 40 and has no right child, so a missing node takes its place. Node 40 has children of ranks 0 and $-1$, so $f = 1$, which is its rank, and the walk stops after one step. The heap is 20:3(60:2(80:1(90:0, 70:0), 40:1(50:0, -)), -) and the root 25:0. Node 40 is now a 1,2-node.

**Decrease 80 to 75.** Node 80 is the left child of 60. Its right child 70 takes its place, and 75 becomes a root with its left subtree 90, so its rank is 1. Node 60 now has children of ranks 0 and 1, so $f = 2$, and the walk stops. The roots are 20:3(60:2(70:0, 40:1(50:0, -)), -), 25:0 and 75:1(90:0, -).

**Decrease 50 to 45.** Node 50 is the left child of 40, with no right child. After the cut, 40 has no children, so $f = 0 < 1$ and its rank drops to 0. Then 60 has children of ranks 0 and 0, so $f = 1 < 2$ and its rank drops to 1. Then 20 is a root, and gets rank $1 + 1 = 2$. That is 3 steps, with one cut. The roots are 20:2(60:1(70:0, 40:0), -), 25:0, 75:1(90:0, -) and 45:0.

**Delete-min.** It returns 20. The right spine of 60 is 60, 40, so the new half trees are 60:1(70:0, -) and 40:0. The trees are processed in the order 60:1, 40:0, 25:0, 75:1, 45:0. Tree 25:0 meets 40:0 in bucket 0, and the link gives 25:1(40:0, -), which meets 60:1 in bucket 1. The second link gives 25:2(60:1(70:0, 40:0), -). With 2 links, the roots are 45:0, 75:1(90:0, -) and 25:2(60:1(70:0, 40:0), -).

## Correctness

Half order holds after each operation: a link puts the half tree of the larger root to the left of the smaller root, the disassembly in delete-min keeps each spine node with its left subtree, and decrease-key removes $x$ with its left subtree, so every left subtree that loses keys only loses them. The rank rule fixes the rank of each non-root as $f$ of its children's ranks, and $f$ does not decrease when an argument increases. So after a child loses rank, the correct rank of its parent can only go down, and the walk of lines L10 to L14 stops at the first node whose rank is already correct. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | worst case | amortized |
|---|---|---|
| find-min | $O(1)$ | $O(1)$ |
| insert, meld | $O(1)$ | $O(1)$ |
| decrease-key | $O(\log n)$ | $O(1)$ |
| delete-min | $O(n)$ | $O(\log n)$, at most $2 \log_\varphi n$ comparisons |
| space | key, rank and three pointers per node | |

**Worst case.** The walk of decrease-key goes up the ancestors of the cut, and the half trees can become unbalanced, and the paper gives no bound on their height better than $n$. So one decrease-key can take more than $O(\log n)$ time; the bound that holds for every single operation is the height of the half tree. A delete-min can see $n - 1$ roots after $n$ inserts.

**Amortized cost.** Haeupler, Sen and Tarjan give each node a potential: a root has potential 1, a 1,1-node has potential 0, and any other $i,j$-node has potential $i + j - 1$. Each link turns a root into a 1,1-node, so it lowers the potential by 1. A rank reduction by $k$ lowers the rank differences of both children of the node by $k$ and raises its own rank difference by $k$, which lowers the sum by $k$. The difficult part is that a 1,1-node has potential 0 and not 1. The argument shows that at most one 1,1-node loses rank in one decrease-key: after the first 1,1-node, every later reduction is by exactly 1, and a 1,1-node whose child loses one rank becomes a 1,2-node and stops the walk. The results are $O(1)$ amortized for decrease-key and $2 \log_\varphi n + O(1)$ amortized time for delete-min (Theorem 6.1 of the paper). The full proof is in [the complexity proof](proofs/complexity.md).

## Variants

- **Type-1 rank rule.** Every non-root is a 1,1-node or a 0,$i$-node with $i > 0$. The rank bound is better, $r \le \lg n$ (Lemma 5.1), but the analysis is harder, and the paper proves the bounds only with a restricted order of links in delete-min.
- **One-pass linking.** Link each pair of equal rank once and do not link the results again. The bounds still hold, with a lazier delete-min and longer root lists.
- **One-tree rank-pairing heap.** Section 7 of the paper keeps a single half tree by doing a link at each insert and meld, with unfair links between trees of different ranks.
- **Type-3 rank rule.** The paper remarks that allowing 1,3-nodes instead of 0,2-nodes gives an even simpler analysis, with a weaker size bound.

## When to use it

Use a rank-pairing heap where a Fibonacci heap fits, in algorithms with many decrease-keys, such as [Dijkstra's algorithm](/dijkstra/) on dense graphs. It is simpler to code than a Fibonacci heap: no cascading cuts, no mark bits, and only one cut per decrease-key. The authors report preliminary experiments in which it is competitive in practice. For a heap without decrease-key, a [binary heap](/binary-heap/) is simpler and usually faster.

## Pitfalls

- **Unfair links.** LINK must join two half trees of equal rank. A link of trees of different ranks breaks the rank rule of the loser, and the rank bound is lost.
- **The rank of a new root.** After a cut or the disassembly, set $r(x) = r(x.left) + 1$. Keeping the old rank of a 0,$i$-node can make a root that is not a 1-node.
- **Where the walk starts.** The walk starts at the old parent $u$ of $x$, which is now the parent of $y$, not at $x$.
- **A simpler rule fails.** Section 8 of the paper shows that two simpler decrease-key methods, with no walk over siblings or with no rank changes, lose the $O(1)$ amortized bound.

## Implementations

The Python version follows the pseudocode. It keeps the root list as a linked list with a tail pointer, so that meld takes $O(1)$ time, and it counts links and rank-reduction steps in `links` and `rank_steps`, which the tests use for the example. The `check_invariant` method checks half order, the type-2 rule, the parent pointers and the size bound $F_{k+3} - 1$ for children.

## History

Haeupler, Sen and Tarjan presented rank-pairing heaps at ESA 2009, and the full version appeared in the SIAM Journal on Computing in 2011. They build on the half-ordered trees of the tournament view of heaps, on Peterson's and Høyer's work on heaps with ranks, and on the [thin heap](/thin-heap/) of Kaplan and Tarjan. Their aim was a heap with the efficiency of the Fibonacci heap and much of the simplicity of the pairing heap. The journal version thanks Haim Kaplan and Uri Zwick for pointing out an error in the original analysis of type-1 heaps.

## References
