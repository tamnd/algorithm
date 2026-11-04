---
tag: V45MQ4
kind: data-structure
slug: strict-fibonacci-heap
name: Strict Fibonacci heap
aliases:
- strict Fibonacci heaps
area: data-structures/heaps
level: research
summary: Fibonacci-like heap with worst-case O(1) decrease-key and O(log n) delete.
implements: [priority-queue, meldable-priority-queue]
model: pointer-machine
complexity:
  vars: {n: the number of items in the heap}
  time: {worst: O(log n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [fibonacci-heap, decrease-key, amortized-vs-worst-case, binomial-heap]
see_also: [fibonacci-heap, brodal-queue, hollow-heap, rank-pairing-heap, relaxed-heap, decrease-key, dijkstra, comparison-sort-lower-bound]
sources:
  - paper: doi:10.1145/2213977.2214082
    title: "Gerth Stølting Brodal, George Lagogiannis and Robert E. Tarjan, Strict Fibonacci heaps, Proceedings of the 44th ACM Symposium on Theory of Computing (STOC), 2012"
    locator: Section 2 (the invariants I1 to I4 and Lemma 1), Section 3 (the four transformations, Figure 1 and Table 1), Section 4 (the operations), Section 5 (the correctness of the invariants) and Section 6 (the representation)
  - paper: doi:10.1145/3707692
    title: Gerth Stølting Brodal, George Lagogiannis and Robert E. Tarjan, Strict Fibonacci heaps, ACM Transactions on Algorithms, 2025
    locator: the journal version of the same paper
  - paper: doi:10.1145/28869.28874
    title: Michael L. Fredman and Robert E. Tarjan, Fibonacci heaps and their uses in improved network optimization algorithms, Journal of the ACM 34(3), 1987
    locator: Sections 2 and 3 (the amortized bounds that the strict Fibonacci heap makes worst-case)
---

A strict Fibonacci heap is a meldable [priority queue](/priority-queue/) of Gerth Stølting Brodal, George Lagogiannis and Robert Tarjan (STOC 2012). It does insert, find-min, meld and [decrease-key](/decrease-key/) in $O(1)$ time and delete-min and delete in $O(\log n)$ time, all in the worst case, on a pointer machine. These are the amortized bounds of the [Fibonacci heap](/fibonacci-heap/), made to hold for every single operation. The [Brodal queue](/brodal-queue/) of 1996 had the same bounds, but it needs arrays and is much more complex. The strict Fibonacci heap is a single heap-ordered tree. It replaces the cascading cuts of a Fibonacci heap with a fixed amount of balancing work in each operation, and it keeps the counts that would make that work fail below fixed limits of order $\log n$. The code on this page follows the tree, the invariants, the transformations and the operations of the paper, but it finds the transformations by short scans, not with the paper's pointer lists. It is therefore $O(\log n)$ per operation, not $O(1)$; see Complexity.

## In plain words

A Fibonacci heap is fast on average, but now and then one delete-min has to clean up a long list of trees, and one decrease-key can start a long chain of cuts. A strict Fibonacci heap never lets the mess grow. It keeps everything in one tree under the smallest item. Some nodes are marked "active". Active nodes have a rank and a count of lost children, and these must stay small. After each operation the heap does a few repair steps, such as joining two active nodes of the same rank, or turning three small subtrees of the root into one. The paper proves that this fixed number of steps per operation is always enough to keep the tree shallow and the root of small degree, so no operation ever has a large cleanup.

## The abstract type

A strict Fibonacci heap implements the [meldable priority queue](/meldable-priority-queue/) with decrease-key: `insert(k)` returns a handle, and there are `find-min()`, `delete-min()`, `meld(H1, H2)`, `decrease-key(handle, k)` and `delete(handle)`. Delete is decrease-key to $-\infty$ followed by delete-min. This page uses a min-heap. Equal keys are allowed: the code breaks ties by the order of insertion, so the keys behave as distinct.

## Representation

The heap is one tree that is heap-ordered: every key is larger than the key of its parent, so the root holds the minimum. Each node is **active** or **passive**. An **active root** is an active node whose parent is passive. Every active node $x$ has a **rank**, the number of its active children, and a **loss** $\ell(x) \ge 0$, which counts the active children it has lost since its loss was last reset. A passive node is **linkable** if all its children are passive. All nodes except the root are in a queue $Q$, which is used to spread some work over the nodes in a round-robin way.

To *link* $x$ below $y$ means to make $x$ a child of $y$: as the leftmost child if $x$ is active, and as the rightmost child if $x$ is passive. Let $R = 2 \lg n + 6$. The paper keeps four invariants.

- **I1 (structure).** The active children of a node come before its passive children. The root is passive, and its linkable passive children are its rightmost children. For an active node, its $i$-th rightmost active child $c$ has $\mathrm{rank}(c) + \ell(c) \ge i - 1$. An active root has loss 0.
- **I2 (active roots).** There are at most $R + 1$ active roots.
- **I3 (loss).** The total loss of all nodes is at most $R + 1$.
- **I4 (degrees).** The root has degree at most $R + 3$, and a node at position $p$ of $Q$ has degree at most $2 \lg(2n - p) + 9$, or one more if it is active with loss 0.

The rank condition of I1 is the Fibonacci heap rule in disguise: a node may lose children, but each loss is counted, and the total count is bounded by I3. Lemma 1 of the paper derives from I1 that every rank is at most $\lg n + \sqrt{2L} + 2$, where $L$ is the total loss, so I3 gives a rank bound of $R$. I2 and I4 bound the work of delete-min.

Meld must make every node of one tree passive in $O(1)$ time. The paper does this with a shared *active record*: each active node points to a record with one flag, all active nodes of a heap share the same record, and a node is active exactly when its record says so. One write to the flag makes a whole tree passive. The code does the same with the class `Record`.

## Operations

There are four transformations. Each is done only when its condition holds.

- **Active root reduction.** Two active roots $x$, $y$ of the same rank, with $x$ of smaller key: link $y$ below $x$ and add one to the rank of $x$. If the rightmost child $z$ of $x$ is passive, link $z$ below the root.
- **Root degree reduction.** Three linkable passive children of the root, sorted as $x < y < z$ by key: make $x$ and $y$ active with loss 0, link $z$ below $y$ and $y$ below $x$, set $\mathrm{rank}(x) = 1$ and $\mathrm{rank}(y) = 0$, and link $x$ below the root as its leftmost child. The root loses two children and gains one active root.
- **One-node loss reduction.** An active node $x$ with loss at least 2 and parent $y$: link $x$ below the root, as an active root with loss 0. Subtract one from the rank of $y$, and if $y$ is not an active root, add one to its loss.
- **Two-node loss reduction.** Two active nodes $x$, $y$ with loss 1 and the same rank, with $x$ of smaller key: link $y$ below $x$, add one to the rank of $x$ and set both losses to 0. Then subtract one from the rank of $z$, the old parent of $y$, and if $z$ is not an active root, add one to its loss.

A *loss reduction* is either of the last two.

```pseudo id=main
INSERT(H, k)
L1  meld H with a heap of one passive node with key k

MELD(H1, H2)
L2  make every node of the smaller heap passive, by one write to its shared active record
L3  link the root v of larger key below the other root; Q ← Q_small, then v, then Q_large
L4  do one active root reduction and one root degree reduction, if possible

FIND-MIN(H)
L5  return the key of the root

DECREASE-KEY(H, x, k)                ▷ k ≤ key(x)
L6  key(x) ← k; if x is the root, return; if key(x) < key(root), swap the items of x and the root
L7  y ← parent(x); link x below the root
L8  if x and y are active: x becomes an active root with loss 0; rank(y) ← rank(y) − 1;
        if y is not an active root, loss(y) ← loss(y) + 1
L9  do one loss reduction, if possible; then up to 6 active root and up to 4 root degree reductions

DELETE-MIN(H)
L10 x ← the child of the root with the smallest key; if x is active, make it passive,
        and make its active children active roots with loss 0
L11 link every other child of the root below x; remove x from Q; delete the old root; x is the root
L12 twice: move the front node y of Q to the back, and link the passive ones among the two
        rightmost children of y below x
L13 do one loss reduction, if possible
L14 repeat active root reductions and root degree reductions while one of them is possible
```

Insert (line L1) is a meld with a one-node heap. Meld (lines L2 to L4) makes the smaller tree all passive, so that its invariants do not have to be merged with those of the larger tree, puts the larger root below the smaller one, and joins the queues. Decrease-key (lines L6 to L9) moves $x$ with its subtree below the root, where its new key cannot break heap order. If $x$ had an active parent, that parent loses an active child, which is counted in its loss. The paper's Table 1 shows that the fixed number of reductions in line L9 is enough to restore I2 and I4.

Delete-min (lines L10 to L14) is the one operation with $\Theta(\log n)$ work. The smallest child of the root becomes the new root, and all other children of the old root move below it. This may make the new root's degree large, and the many reductions of line L14 bring it back. Line L12 is how the paper keeps I4 for nodes deep in the tree: each node reaches the front of $Q$ from time to time, and when it does, it gives two of its passive children to the root.

## Example

Insert the keys 50, 20, 70, 10 and 60, in this order. Write a tree as key(children), with [rank,loss] after an active node. Until now no transformation applies, because there is no active node and the root has fewer than three linkable children, and the tree is `10(20(50 70) 60)`.

*Insert 30.* Line L3 links 30 below 10, as its rightmost child, and $Q$ is 30, 60, 20, 70, 50. There is no active root. The root has three linkable passive children, 20, 60 and 30, so line L4 does a root degree reduction with $x = 20$, $y = 30$, $z = 60$. The tree is `10(20[1,0](30[0,0](60) 50 70))`.

*Insert 80 and 40.* Each is linked below the root, and nothing else applies: `10(20[1,0](30[0,0](60) 50 70) 80 40)`.

*Insert 90.* After the link, the root has the linkable children 80, 40 and 90, so a root degree reduction makes `40[1,0](80[0,0](90))` the leftmost child of the root. Now 40 and 20 are active roots of rank 1, and the active root reduction links 40 below 20, which gets rank 2. The rightmost child of 20 is now the passive 70, which moves to the root:

```text
10(20[2,0](40[1,0](80[0,0](90)) 30[0,0](60) 50) 70)
Q = 90 40 80 30 60 20 70 50
```

*Delete-min.* The children of 10 are 20 and 70, so line L10 picks $x = 20$, makes it passive, and its active children 40 and 30 become active roots. Line L11 moves 70 below 20 and removes 20 from $Q$. Line L12 moves 90 and then 40 to the back of $Q$; 90 has no children, and the only child of 40 is active, so nothing moves. There is no loss, the two active roots have ranks 1 and 0, and 20 has only two linkable children, so line L14 does nothing. The result is `20(40[1,0](80[0,0](90)) 30[0,0](60) 50 70)` with $Q$ = 80, 30, 60, 70, 50, 90, 40. The test `test_page_example` checks every tree and queue above.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows that every operation keeps heap order, so the root is always the minimum and delete-min removes the right item. It also shows that every operation keeps the bookkeeping exact (each rank is the number of active children, the active children come first, active roots have loss 0) and keeps the rank condition of I1. The key step is that whenever a node loses an active child, either its loss goes up by one, so $\mathrm{rank} + \ell$ does not change, or it is an active root or passive, where the condition does not apply. The loop of line L14 ends because each reduction lowers $2 \cdot \deg(\text{root}) + 3 \cdot (\text{number of active roots})$ by at least one.

That I2, I3 and I4 always hold, and so that the fixed number of reductions per operation is enough, is the long case analysis of Section 5 of the paper, which this page does not repeat. The code checks all four invariants after every operation in 600 random tests.

## Complexity

**The paper.** On a pointer machine, insert, find-min, meld and decrease-key take $O(1)$ time in the worst case, and delete-min and delete take $O(\log n)$. Each transformation is $O(1)$ work once found. To find them in $O(1)$ time, Section 6 of the paper keeps the active roots and the nodes with positive loss in lists grouped by rank (the rank list and the fix list), so that two active roots of equal rank, or a node with loss 2, or two of loss 1 and equal rank, are found at the front of a list. The linkable children of the root are kept at its right end (part of I1) so that three of them are found in $O(1)$ time. Delete-min does $O(\log n)$ reductions because the root degree is $O(\log n)$ by I4 and the number of active roots is $O(\log n)$ by I2. The bounds are optimal for a comparison-based heap: if insert is $O(1)$, delete-min must be $\Omega(\log n)$, else $n$ inserts and $n$ delete-mins would beat the [comparison sort lower bound](/comparison-sort-lower-bound/).

**This code.** It keeps the active roots and the nodes with positive loss in Python sets, and it finds a pair of equal rank by one pass over the set, which by I2 and I3 has $O(\log n)$ elements. It finds the linkable children of the root by a scan of the root's children, which by I4 are $O(\log n)$. So insert, meld and decrease-key take $O(\log n)$ time, and delete-min takes $O(\log^2 n)$, since it does $O(\log n)$ reductions. This is enough to test the structure, but it does not show the worst-case $O(1)$ bounds. The space is $\Theta(n)$ for both: each node has a constant number of fields and pointers.

## Variants

- **Fibonacci heap.** The [Fibonacci heap](/fibonacci-heap/) has the same bounds, but amortized. A strict Fibonacci heap is what one gets by keeping the Fibonacci heap's structure in check at every step.
- **Brodal queue.** The [Brodal queue](/brodal-queue/) has the same worst-case bounds, but it uses two trees, guides of a [redundant number system](/redundant-number-system/), and arrays, so it does not run on a pointer machine.
- **Hollow heap and rank-pairing heap.** The [hollow heap](/hollow-heap/) and the [rank-pairing heap](/rank-pairing-heap/) have the Fibonacci heap bounds, amortized, with much simpler code. In practice these are the ones to use.
- **Relaxed heaps.** The run-relaxed heap of the [relaxed heap](/relaxed-heap/) page has worst-case $O(1)$ decrease-key, but no $O(1)$ meld.

## When to use it

Use a strict Fibonacci heap when a program needs a guaranteed $O(1)$ decrease-key and meld for every single operation, for example in a real-time system that runs [Dijkstra's algorithm](/dijkstra/), and an amortized bound is not enough. In most programs a [binary heap](/binary-heap/) or a pairing heap is faster: the constant factors of the strict Fibonacci heap are large, since every operation does several reductions, and each node has many fields.

## Pitfalls

- **The order of the steps in a two-node loss reduction.** The old parent $z$ of $y$ may be $x$ itself. If the loss of $z$ is raised before the losses of $x$ and $y$ are set to 0, the raise is lost, and $\mathrm{rank}(x) + \ell(x)$ drops by one, which can break I1 at the parent of $x$. The code updates $z$ last. An earlier version of this code had the steps the other way, and the random tests caught it.
- **Losses of new active roots.** When delete-min makes the new root passive, its active children become active roots, and they must get loss 0, as I1 asks. Otherwise loss stays on nodes that no loss reduction will remove.
- **Rank is only for active nodes.** When an active root leaves its passive parent, nothing is subtracted from that parent: the rank of a passive node is not used, and a passive node gets a fresh rank when a root degree reduction makes it active.
- **Making a tree passive by a traversal.** Meld must not walk the smaller tree. The shared active record does it with one write.
- **Swapping items, not nodes.** When a decreased key is smaller than the key at the root, the items of the two nodes are swapped, so the handle of an item must point to the item, and the item must know its current node. The code keeps the field `Item.node` up to date on every swap.

## Implementations

The Python version follows the pseudocode, with `_active_root_reduction`, `_root_degree_reduction` and `_loss_reduction` for the transformations. It keeps the queue $Q$ as a circular doubly linked list through the nodes, so that meld joins two queues in $O(1)$ time. The simplification is in how a transformation is found: by a pass over a set or over the children of the root, instead of the rank list and the fix list of Section 6 of the paper, and the root's linkable children are not kept at its right end. The method `check_invariant` checks heap order, the queue, the bookkeeping, the rank condition of I1, and the bounds of I2, I3 and I4.

## History

Fredman and Tarjan introduced the Fibonacci heap in 1984, with $O(1)$ amortized decrease-key. Driscoll, Gabow, Shrairman and Tarjan gave the relaxed heaps in 1988, with worst-case $O(1)$ decrease-key, and Brodal gave the first heap with all the Fibonacci heap bounds in the worst case in 1996. Brodal, Lagogiannis and Tarjan presented strict Fibonacci heaps at STOC 2012 as the first such heap on a pointer machine, and the journal version appeared in ACM Transactions on Algorithms.

## References
