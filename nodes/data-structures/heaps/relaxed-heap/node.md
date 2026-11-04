---
tag: KN6FTW
kind: data-structure
slug: relaxed-heap
name: Relaxed heap
aliases:
- Driscoll relaxed heap
area: data-structures/heaps
level: research
summary: Heap with worst-case bounds matching Fibonacci heaps for decrease-key and delete.
implements: [priority-queue]
model: comparison-model
complexity:
  vars: {n: the number of items in the heap}
  time: {amortized: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [binomial-heap, decrease-key, fibonacci-heap]
see_also: [fibonacci-heap, binomial-heap, brodal-queue, strict-fibonacci-heap, violation-heap, thin-heap, weak-heap, dijkstra]
sources:
  - paper: doi:10.1145/50087.50096
    title: "James R. Driscoll, Harold N. Gabow, Ruth Shrairman and Robert E. Tarjan, Relaxed heaps: an alternative to Fibonacci heaps with applications to parallel computation, Communications of the ACM 31(11), 1988, pp. 1343 to 1354"
    locator: the sections on rank relaxed heaps (invariants, the cleaning and pair transformations, amortized bounds) and on run relaxed heaps (worst-case bounds)
  - paper: "Amr Elmasry, Claus Jensen and Jyrki Katajainen, Two-tier relaxed heaps, Acta Informatica 45(3), 2008, pp. 193 to 210"
    title: "Amr Elmasry, Claus Jensen and Jyrki Katajainen, Two-tier relaxed heaps, Acta Informatica 45(3), 2008, pp. 193 to 210"
    locator: the description of run-relaxed heaps and the comparison bounds
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Sections 2 and 3 (the amortized bounds that relaxed heaps match)
---

A relaxed heap is a collection of binomial trees in which a few nodes may break heap order. Such a node is *active*. Driscoll, Gabow, Shrairman and Tarjan described two kinds in 1988. In a *rank relaxed heap* there is at most one active node of each rank and every active node is the last child of its parent; it has the amortized bounds of the [Fibonacci heap](/fibonacci-heap/), $O(1)$ for [decrease-key](/decrease-key/) and $O(\log n)$ for delete-min. In a *run relaxed heap* there are at most $\lfloor \lg n \rfloor$ active nodes, and the same bounds hold in the worst case, except for meld. The point of the design is that decrease-key does not cut a node. It only marks the node, and a constant number of local transformations keeps the number of marks small. This page explains rank relaxed heaps and gives a working implementation. The transformations of this implementation are a reconstruction, not a copy of the paper, and the page says where.

## In plain words

Start with a [binomial heap](/binomial-heap/). When a key decreases and becomes smaller than the key of its parent, a Fibonacci heap cuts the node out. A relaxed heap leaves the node where it is and marks it as active. So the tree keeps its exact binomial shape, and the depth stays at most $\lg n$.

Marks must not pile up, because find-min must look at every active node. The rule is: at most one active node for each rank. When a second active node of the same rank appears, the heap moves a few subtrees of the same rank around so that one or both marks go away. Each move is a swap or a link of two trees of equal rank, so the shape stays binomial.

## The abstract type

A relaxed heap implements the [priority queue](/priority-queue/) with decrease-key: `insert(k)` returns a handle, and there are `find-min()`, `delete-min()` and `decrease-key(handle, k)`. This page uses a min-heap. Delete of an arbitrary item is decrease-key to $-\infty$ and then delete-min. Meld is possible for rank relaxed heaps but the implementation here does not offer it.

## Representation

Each node $x$ has a key, a pointer to its parent, an array of children with `children[i]` the child of rank $i$, and a bit *active*. The rank of $x$ is the number of children. So every tree is a binomial tree: a node of rank $k$ has children of the ranks $0, 1, \ldots, k - 1$, and its subtree has exactly $2^k$ nodes. The *last child* of a node of rank $k$ is its child of rank $k - 1$.

The heap keeps the roots in a table by rank, at most one root for each rank, and a table of the active nodes by rank. A non-root node $x$ is a *violation* if its key is smaller than the key of its parent. Roots are never active.

**Invariants** (between operations, as in the paper):
- (a) There is at most one active node of each rank.
- (b) Every active node is the last child of its parent.
- (c) Every non-root node that is not active has a key at least the key of its parent.

An active node does not need to be a violation. A mark can become stale when the key of the parent decreases, and the code removes stale marks when it meets them. By (a), there are at most $\lfloor \lg n \rfloor$ active nodes, because a non-root node has rank at most $\lfloor \lg n \rfloor - 1$.

## Operations

Inside an operation, the heap keeps a *work list* $W$ of nodes that may break the invariants. The procedure FIX empties it.

```pseudo id=main
INSERT(H, k)
L1  x ← a new node of rank 0; add x to the roots, linking roots of equal rank as in a binary counter; FIX(H); return x

FIND-MIN(H)
L2  return the smallest key among the roots and the active nodes

DECREASE-KEY(H, x, k)                   ▷ k ≤ x.key
L3  x.key ← k
L4  push x on W; FIX(H)

FIX(H)                                  ▷ repeat while W is not empty: pop v; p ← the parent of v; r ← rank of v
L5  if p = NIL or v.key ≥ p.key then make v not active; continue
L6  make v active
L7  if v is not the last child of p then s ← the child of p of rank r + 1
L8      if s.key < p.key then: if s is not the last child of p then push v, s and continue, else PARENT(s)
L9      if v is still not the last child: c ← the last child of s; if c is active or c.key < s.key then TRIPLE(v, s, c); continue
L10     CLEAN: exchange v and c, so c is the child of rank r of p and v is the last child of s; push c, v; continue
L11 if another active node y of rank r exists: if y is not a last child that is a violation then push v, y, else PAIR(v, y)

DELETE-MIN(H)
L12 m ← the node of FIND-MIN
L13 if m is not a root: remove the root t of smallest rank and make its children roots
L14     if m is still not a root: link t with the children of m in the order of rank, and put the result in the place of m
L15 if m is a root: remove m, make its children roots and add t back if it was removed; FIX(H); return the old key of m
```

The three transformations work on subtrees of equal rank. Every transformation makes the nodes that it moves not active, and pushes on $W$ every node that it moves and every node that becomes or stops being a last child.
- **PARENT(s)**, where $s$ is the last child of $p$ and $s.key < p.key$: cut $s$ from $p$. Now $p$ and $s$ have the same rank, so link them with $s$ on top, and put $s$ in the old place of $p$.
- **TRIPLE(v, s, c)**: $v$ is the child of rank $r$ of $p$, $s$ is the child of rank $r + 1$, and $c$ is the last child of $s$. Cut $c$ from $s$, so $s$ has rank $r$, and put $s$ in the place of $v$. Link $v$ and $c$, which gives a tree of rank $r + 1$, and put it in the place of $s$.
- **PAIR(x, y)**: $x$ and $y$ are active last children of rank $r$ of different parents $p$ and $q$, with $p.key \le q.key$. Cut both, so $p$ and $q$ have rank $r$. Link $q$ under $p$, so $p$ has its old rank $r + 1$ again. Link $x$ and $y$, and put the result in the old place of $q$.

Every link puts the larger key below, so the loser of a link is never a violation. The old last child of the winner stops being a last child, so it goes on $W$.

**What comes from the paper and what does not.** The invariants (a) to (c), the idea of marks on last children, the *pair* and *cleaning* transformations, and the bounds are from Driscoll, Gabow, Shrairman and Tarjan. The cleaning transformation of the paper exchanges an active node that is not a last child with a node of the same rank that is not active, so that the active node becomes a last child; line L10 is this idea. The exact case analysis of lines L7 to L11, the use of the work list, PARENT on a violating sibling, TRIPLE, and the delete-min of lines L13 to L15 are this page's own design. They are checked by the proof in [the correctness proof](proofs/correctness.md) and by the tests, but they are not the paper's text.

## Example

Insert the keys $10, 20, \ldots, 160$. The carries of the binary counter give one tree of rank 4. Write a tree as `key(children in the order of rank)` and mark an active node with `*`:

```text
10(20, 30(40), 50(60, 70(80)), 90(100, 110(120), 130(140, 150(160))))
```

Now do three decrease-key operations and one delete-min.

| step | operation | what happens | transformations |
| --- | --- | --- | --- |
| 1 | 60 to 5 | 5 is the child of rank 0 of 50, and it is not the last child. The sibling of rank 1 is $s = 70$, and its last child $c = 80$ is not active and not smaller than 70. So CLEAN exchanges 5 and 80, and 5 becomes the active last child of 70. | 1 |
| 2 | 120 to 15 | 15 is the last child of 110 and a violation, and 5 is already active with rank 0. So PAIR(15, 5): the parents are 110 and 70, and 70 is smaller, so 110 goes under 70, and the tree 5(15) goes to the old place of 110 under 90. There 5 is a violation of rank 1 that is not the last child, and CLEAN exchanges it with 150, the last child of 130. | 2 |
| 3 | 140 to 25 | 25 is a violation under 130 and not the last child. Its sibling of rank 1 is 5, which is smaller than 130 and is the last child, so PARENT(5) cuts 5 and links 130 under it. Now 25 is the last child of 130, and 5 is the last child of 90. Both are active, with the ranks 0 and 2. | 1 |
| 4 | delete-min | FIND-MIN scans the root 10 and the active nodes 25 and 5, and finds 5. The root of smallest rank is 10; its children become roots. Then 10 is linked with the children 15 and 130(25) of 5, and the tree 10(15, 130(25)) takes the place of 5 under 90. | 0 |

After step 2 and after step 3 the trees are

```text
10(20, 30(40), 50(80, 70(110)), 90(100, 150(160), 130(140, 5*(15))))
10(20, 30(40), 50(80, 70(110)), 90(100, 150(160), 5*(15, 130(25*))))
```

and after the delete-min, which returns 5, the heap has four trees of the ranks 0 to 3:

```text
20  30(40)  50(80, 70(110))  90(100, 150(160), 10*(15, 130(25*)))
```

The node 10 is now active under 90, so FIND-MIN still finds it. The test file checks every tree of this trace and the count of transformations.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). These are the main points.
- *Shape.* Every transformation cuts and links trees of equal rank, and puts a tree of rank $k$ in a slot of rank $k$. So every tree stays a binomial tree, and all ranks are at most $\lg n$.
- *The work list.* At the top of the loop in FIX, every node that breaks (b) or (c), and all but one active node of each rank, are on $W$. Each transformation pushes the nodes whose parent or last-child status it changes. So when $W$ is empty, (a), (b) and (c) hold.
- *Termination.* Each transformation lowers the tuple (number of violations, minus the sum of the ranks of the violations, number of violations that are not last children, number of stale marks) in lexicographic order. Between two transformations, the pushes of lines L8 and L11 go to nodes of higher rank or remove a stale mark, so there are at most $O(\log n)$ of them.
- *Find-min.* Go up from any node while the node is not active and not a root. By (c) the keys do not grow. So a root or an active node has a key at most the key of the start node, and the minimum is among the roots and the active nodes.
- *Delete-min.* When $m$ is not a root, the root $t$ loses its children and has rank 0. Linking it with the children of $m$ of the ranks $0, \ldots, r - 1$ gives a binomial tree of rank $r$, which fills the slot of $m$. So exactly one node, $m$, leaves the heap.

## Complexity

| operation | paper, rank relaxed heap | paper, run relaxed heap | this implementation |
| --- | --- | --- | --- |
| find-min | $O(1)$ amortized with a pointer to the minimum | $O(1)$ worst case | $O(\log n)$ worst case (a scan) |
| insert | $O(1)$ amortized | $O(1)$ worst case | $O(\log n)$ worst case, carries |
| decrease-key | $O(1)$ amortized | $O(1)$ worst case | measured, see below |
| delete-min | $O(\log n)$ amortized | $O(\log n)$ worst case | $O(\log n)$ plus FIX |

The bounds in the first two columns are the results of the paper, and this page does not prove them. Each transformation and each step of FIX costs $O(1)$ time, and each delete-min does $O(\log n)$ links and pushes $O(\log n)$ nodes. For this implementation the page proves that FIX ends, but it does not prove an $O(1)$ amortized bound for its own case analysis. In one run with 4096 items and 20000 decrease-key operations to a new minimum (seed 1), there were on average 1.92 transformations per decrease-key, and at most 18 in one call. The test `test_many_new_minima` checks that the number of active nodes stays at most $\lfloor \lg n \rfloor + 1$.

Space is $\Theta(n)$: a key, a parent pointer, a child array and a bit per node; the child arrays together hold $n - $ (number of roots) pointers.

## Variants

- *Run relaxed heaps* allow more than one active node of a rank, but at most $\lfloor \lg n \rfloor$ active nodes in all. Active nodes that are last children of consecutive ranks form a *run*. With a run list and a singleton list, each decrease-key does $O(1)$ transformations in the worst case. Meld is not supported in $O(1)$ time.
- *Two-tier relaxed heaps* (Elmasry, Jensen and Katajainen, 2008) put a second heap on top of the roots and the active nodes. They reach $O(1)$ worst-case find-min, insert and decrease-key, and delete-min with at most $3 \lg n + O(1)$ key comparisons.
- *Relaxed weak queues* use the same ideas on [weak heaps](/weak-heap/), with the cleaning, parent and sibling transformations.
- The paper also gives a parallel version, which the title mentions; it is the motivation for the worst-case bounds.

## When to use it

Use a run relaxed heap when you need [decrease-key](/decrease-key/) in $O(1)$ worst-case time, for example in a real-time system or in a parallel algorithm where every step must be short. The trees are binomial, so the depth is $O(\log n)$ and there are no long cut chains. For amortized bounds a [Fibonacci heap](/fibonacci-heap/) or a [pairing heap](/pairing-heap/) is simpler. For worst-case bounds with meld, use a [Brodal queue](/brodal-queue/) or a [strict Fibonacci heap](/strict-fibonacci-heap/). For [Dijkstra's algorithm](/dijkstra/) in practice, a binary heap is usually fastest.

## Pitfalls

- **Forgetting the old last child.** A link, a cut or a swap can change which child of a node is the last one. An active node that stops being a last child breaks (b), so it must go on the work list.
- **Pairing with a node that is not ready.** PAIR needs two active last children that are violations, and their parents must be different. The other active node of the same rank may still be waiting on $W$; push both and handle the other one first, as line L11 does.
- **Stale marks.** A mark can stay on a node that is no longer a violation. Do not count it as a violation, but remove it, or it blocks invariant (a) for no reason.
- **Rank changes of active nodes.** When an active node gets or loses a child, it moves to another rank in the table of active nodes. Update the table, or find-min and the pair rule see wrong data.
- **Delete-min of a non-root.** The minimum can be an active node deep in a tree. Removing it leaves a hole of rank $r$, and the hole must be filled with a binomial tree of rank $r$, or the shape breaks.
- **Find-min must scan the active nodes.** The minimum is not always a root, because an active node can be smaller than every root.

## Implementations

The Python implementation in `impl/python/relaxed_heap.py` follows the pseudocode line by line. It counts transformations, and `check_invariant` checks the binomial shape, the parent pointers, the table of active nodes, invariants (a) to (c), the size, and that the work list is empty. The tests check the example trace, an empty heap, duplicate keys, a stress run of decrease-keys to new minima, and 600 random sequences of operations against `heapq`.

## History

Driscoll, Gabow, Shrairman and Tarjan published relaxed heaps in Communications of the ACM in 1988, as an alternative to the Fibonacci heaps of Fredman and Tarjan (1987). Their aim was worst-case bounds and a parallel implementation of Dijkstra's shortest path algorithm. Later work used the same ideas for worst-case efficient heaps with few comparisons: the two-tier relaxed heaps of Elmasry, Jensen and Katajainen (2006 and 2008), and relaxed weak queues of Edelkamp, Elmasry and Katajainen. Other heaps with Fibonacci-heap bounds and a simpler structure, such as [thin heaps](/thin-heap/) and [violation heaps](/violation-heap/), compare themselves with relaxed heaps.

## References
