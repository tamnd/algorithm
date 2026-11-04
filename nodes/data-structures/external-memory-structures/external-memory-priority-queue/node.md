---
tag: Z1W9D1
kind: data-structure
slug: external-memory-priority-queue
name: External memory priority queue
aliases:
- I/O-efficient priority queue
area: data-structures/external-memory-structures
level: advanced
summary: Priority queue that supports insert and delete-min with amortized O((1/B) log_{M/B}(N/B)) I/Os per operation.
implements: [priority-queue]
model: external-memory-model
prereqs: [buffer-tree, priority-queue, external-memory-model]
see_also: [buffer-tree, time-forward-processing, binary-heap, tournament-tree, external-merge-sort, external-sorting-lower-bound, k-way-merge]
sources:
  - paper: "Lars Arge, The buffer tree: a technique for designing batched external data structures, Algorithmica 37(1) (2003)"
    locator: pp. 1 to 24, the section on the external priority queue (the smallest elements in memory, emptying the leftmost path)
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Section 11.4 (buffer trees and the priority queue built on them)
  - paper: "Peter Sanders, Fast priority queues for cached memory, ACM Journal of Experimental Algorithmics 5 (2000)"
    locator: the sequence heap, Sections 2 and 3
  - paper: "Gerth Stolting Brodal and Jyrki Katajainen, Worst-case efficient external-memory priority queues, Scandinavian Workshop on Algorithm Theory (SWAT 1998), Lecture Notes in Computer Science 1432"
    locator: pp. 107 to 118 (worst-case bounds)
---

An external memory priority queue stores items with keys on disk and supports `insert` and `delete-min` with $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ amortized I/Os per operation, far less than one block transfer. A [binary heap](/binary-heap/) on disk pays $\Theta(\log_B N)$ I/Os or more per operation, because each operation follows a path that crosses many blocks. The structure on this page is the one of Arge: it keeps the smallest $\Theta(M)$ items in internal memory and all others in a [buffer tree](/buffer-tree/), which takes inserts in batches. When the memory part runs out, it empties the buffers on the leftmost path of the tree and moves the leftmost leaves into memory. The bound is optimal, since $N$ inserts and $N$ delete-mins [sort](/external-merge-sort/) the keys. This priority queue is the engine of [time-forward processing](/time-forward-processing/) and of many external graph algorithms.

## In plain words

You keep a small box on your desk with the most urgent tasks, all sorted. Every other task goes into a big filing system in the basement, where new papers wait in trays and are only sorted further when a tray is full.

When someone hands you a task that is more urgent than the least urgent one in your box, you swap them: the new task goes in the box, and the old one goes to the basement. When your box is empty, you go down once, finish the sorting of the trays on the way to the most urgent drawer, and bring that whole drawer up. One trip feeds you for a long time, so the trips are rare.

## The abstract type

A [priority queue](/priority-queue/) on a multiset of keys:

- `insert(k)` adds the key $k$.
- `delete-min()` removes and returns a smallest key. Equal keys come out in the order they were inserted.
- `find-min()` returns a smallest key without removing it.
- `size()` returns the number of keys.

There is no `decrease-key`. In external algorithms, a decrease is done by inserting the new key and ignoring the stale copy when it comes out.

## Representation

There is a block size $B$, a memory of $M$ items, and $m = M/B$. Each key $k$ is stored as the pair $(k, s)$, where $s$ is its insertion number, so all items are distinct and ties go by insertion order.

- **The memory part** `mem` is a sorted list of at most $M$ items in internal memory.
- **The tree** is a [buffer tree](/buffer-tree/) with fan-out at most $m$, leaves of at most $B$ items and buffers of at most $M$ pending inserts. It takes only inserts.

**Invariants.**

- **(P1)** Every item in `mem` is smaller than every item in the tree, in leaves or in buffers.
- **(P2)** The tree has the invariants of the buffer tree: search order, equal leaf depth, each buffered item in the range of its node, and no full buffer between operations.

## Operations

```pseudo id=main
INSERT(Q, k)
L1  if Q.mem is not empty and k < max(Q.mem) then
L2      swap k with max(Q.mem)               ▷ k goes to memory, the old maximum goes to the tree
L3  BT-INSERT(Q.tree, k)                     ▷ the insert of the buffer tree

DELETE-MIN(Q)
L4  if Q.mem is empty then REFILL(Q)
L5  if Q.mem is empty then error "empty queue"
L6  remove and return min(Q.mem)

REFILL(Q)
L7  while a node on the leftmost path has a nonempty buffer: EMPTY the highest such node
L8  x ← the leftmost bottom node
L9  move all items in the leaves of x into Q.mem
L10 remove x from the tree, and remove each ancestor that is left with no children
L11 while the root is internal with one child: make that child the root
```

EMPTY is the buffer emptying of the [buffer tree](/buffer-tree/): it moves the buffer of a node one level down, or, at a bottom node, merges it into the leaves and splits nodes that get more than $m$ children. Line L7 empties buffers that are not full. This is allowed: it costs $O(X/B + m)$ for a buffer of $X$ items, and it keeps all buffer tree invariants.

**Why the leftmost leaves hold the smallest items.** After line L7, the buffers on the leftmost path are empty. Every item not below $x$ is in a subtree to the right of the path, so it is at least a routing key that is larger than all items below $x$. And all items below $x$ are in its leaves, since the buffer of $x$ is empty. So the items of $x$ are the smallest items of the tree, and by (P1) they are larger than the items of `mem`, which is empty at that time.

**Why INSERT keeps (P1).** If $k$ is smaller than the largest item of `mem`, line L2 puts $k$ in its place and sends the old maximum to the tree. The old maximum is smaller than every tree item by (P1), and the new `mem` has a smaller maximum than before. Otherwise, $k$ is at least the maximum of `mem` and goes to the tree.

## Example

Take $B = 2$, $m = 4$, so $M = 8$. An internal node is written $\langle$routing keys | number of buffered items$\rangle$ followed by its children.

1. Insert $50, 20, 80, 10, 60, 30, 70, 40, 90$. The ninth insert overflows the root buffer, the root applies it to its leaves, gets 5 leaves and splits: $\langle 70 \mid 0\rangle(\langle 30\ 50 \mid 0\rangle([10\ 20]\ [30\ 40]\ [50\ 60])\ \langle 90 \mid 0\rangle([70\ 80]\ [90]))$. The memory part is empty.
2. Insert $15, 25, 35, 45, 55, 65, 75, 85, 5$. The ninth insert overflows the root buffer again, and the root sends 7 items left and 2 right: $\langle 70 \mid 0\rangle(\langle 30\ 50 \mid 7\rangle(\ldots)\ \langle 90 \mid 2\rangle(\ldots))$.
3. Delete-min. The memory part is empty, so REFILL runs. Line L7 empties the left child: its 6 items and 7 buffered items make 7 leaves, more than $m$, so it splits into a node with $[5\ 10]\ [15\ 20]\ [25\ 30]\ [35\ 40]$ and a node with $[45\ 50]\ [55\ 60]\ [65]$. The first is the leftmost bottom node: its 8 items move to memory, and the node is removed. The call returns 5, and `mem` is $[10, 15, 20, 25, 30, 35, 40]$. The tree is $\langle 70 \mid 0\rangle(\langle 55\ 65 \mid 0\rangle([45\ 50]\ [55\ 60]\ [65])\ \langle 90 \mid 2\rangle([70\ 80]\ [90]))$.
4. Delete-min twice returns 10 and 15 from memory, with no I/O.
5. Insert 12. It is smaller than the maximum 40 of `mem`, so 12 goes into memory and 40 goes to the root buffer. Insert 1: likewise, 1 goes in and 35 goes to the tree. Now `mem` is $[1, 12, 20, 25, 30]$, and the root buffer has 2 items.
6. The remaining delete-mins return $1, 12, 20, 25, 30, 35, 40, 45, \ldots, 90$ in order. The whole run makes 75 block transfers in the count of the code.

## Correctness

By (P1), the smallest item of the queue is the smallest item of `mem` whenever `mem` is not empty, so line L6 returns a correct minimum. When `mem` is empty, REFILL moves into it the smallest items of the tree, as shown above, and then (P1) holds again, because every item left in the tree is larger than the items moved. INSERT keeps (P1) as shown above, and the buffer tree code keeps (P2). Removing whole subtrees in lines L10 and L11 keeps the search order and the equal depth of the leaves. The proof is below.

## Complexity

Let $N$ be the number of operations, and $h = O(\log_m \frac{N}{B})$ the height of the tree.

- **Inserts.** Each item that reaches the tree pays $O(\frac{1}{B})$ per level for full-buffer emptyings and the leaf merges, as in the [buffer tree](/buffer-tree/), so $O(\frac{1}{B}\log_m \frac{N}{B})$ amortized.
- **Refills.** Line L7 empties at most $h$ buffers that may not be full. Each costs $O(X/B + m)$, where the $X/B$ part is paid by the items, which move down as in a normal emptying. The rest is $O(m h)$ per refill. A bottom node made by a split has at least about $m/2$ leaves, almost all full, so it has $\Omega(M)$ items, and a refill brings $\Omega(M) = \Omega(mB)$ items into memory. So the $O(mh)$ cost is $O(h/B)$ per item that later leaves through delete-min.
- **Memory operations.** Lines L1, L2, L4 to L6 work in internal memory and cost no I/O.

| operation | amortized I/Os |
|---|---|
| insert | $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ |
| delete-min | $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ |
| find-min | same as delete-min, by the refill |
| space | $O(N/B)$ blocks and $O(M)$ memory |

**Optimality.** Inserting $N$ keys and then calling delete-min $N$ times outputs them in sorted order, so any priority queue that moves whole items costs at least $\Omega\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os for $2N$ operations, by the [sorting lower bound](/external-sorting-lower-bound/). The amortized bound of this page is therefore optimal.

## Variants

- **Sequence heap.** Sanders' sequence heap keeps sorted runs in groups, merged by [k-way merging](/k-way-merge/) into group buffers and a small deletion buffer, with a [tournament tree](/tournament-tree/) of loser type over the run heads. It has the same I/O bound and is much faster in practice, because it does little work per item beyond merging.
- **Worst-case bounds.** Brodal and Katajainen gave an external priority queue whose bounds hold in the worst case per $B$ operations, not only amortized over the whole sequence.
- **Cache-oblivious priority queues.** Arge and others, and Brodal and Fagerberg (the funnel heap), reach the same bound without knowing $M$ and $B$, under the tall-cache assumption.
- **External heaps.** Fadel, Jakobsen, Katajainen and Teuhola store a heap whose nodes are pages of $\Theta(M)$ items, with heap order between pages.
- **Decrease-key.** External graph algorithms, such as Dijkstra's algorithm on disk, use a separate tournament tree or insert a new copy and delete the old one lazily.

## When to use it

Use it when an algorithm on disk-sized data needs a priority queue and calls it many times: [time-forward processing](/time-forward-processing/) of a DAG, external sweep lines in geometry, external graph search, event simulation, and merging of many sorted streams. If all items fit in memory, use a [binary heap](/binary-heap/). If each operation must touch the disk at most a constant number of times in the worst case, use a worst-case variant.

## Pitfalls

- **Forgetting the swap in INSERT.** A small key inserted while `mem` is not empty must go to memory, or a later delete-min returns a key that is not the smallest. The swap sends out the old maximum, so the memory part does not grow.
- **Taking leaves before the path is empty.** Pending inserts in the buffers on the leftmost path may be smaller than every key in the leftmost leaves. Line L7 must empty all of them first, full or not.
- **A refill that brings too little.** If the leftmost bottom node can be tiny, a refill costs $O(mh)$ I/Os for a few items and the bound fails. Keep bottom nodes at $\Omega(m)$ leaves, by splitting into halves and by fusion when they shrink, or by taking several bottom nodes per refill.
- **Ties.** With equal keys, compare pairs $(k, s)$; otherwise routing keys and (P1) are ambiguous.
- **Using the memory twice.** The memory part and the buffer emptying both need $\Theta(M)$ space; with a real $M$, give each a constant fraction of it.

## Implementations

## History

Arge described the priority queue on the buffer tree at WADS 1995, with the journal version in Algorithmica in 2003, and used it for external graph algorithms and for sorting. Kumar and Schwabe gave an external priority queue based on a tournament tree in 1996, with decrease-key, for external graph search. Fadel, Jakobsen, Katajainen and Teuhola studied external heaps in 1999, and Brodal and Katajainen gave worst-case bounds at SWAT 1998. Sanders introduced the sequence heap for cached memory in 2000; it is the basis of the priority queue in the STXXL library. Vitter's survey treats these structures in its chapter on multiway trees.

## References
