---
tag: 5H2XC9
kind: data-structure
slug: buffer-tree
name: Buffer tree
aliases:
- Arge buffer tree
area: data-structures/external-memory-structures
level: advanced
summary: Batched external-memory search tree whose nodes hold buffers of pending operations.
implements: [dictionary]
model: external-memory-model
prereqs: [b-tree, external-memory-model, amortized-cost, external-merge-sort]
see_also: [external-memory-priority-queue, b-epsilon-tree, time-forward-processing, log-structured-merge-tree, write-optimized-structure, offline-algorithm, external-stack]
sources:
  - paper: "Lars Arge, The buffer tree: a technique for designing batched external data structures, Algorithmica 37(1) (2003)"
    locator: pp. 1 to 24 (the structure, buffer emptying, rebalancing, the O((N/B) log_{M/B}(N/B)) bound, and the priority queue)
  - paper: "Lars Arge, The buffer tree: a new technique for optimal I/O-algorithms, Workshop on Algorithms and Data Structures (WADS 1995), Lecture Notes in Computer Science 955"
    locator: pp. 334 to 345, the first version
  - book: isbn:9781601981066
    title: Jeffrey Scott Vitter, Algorithms and Data Structures for External Memory, Foundations and Trends in Theoretical Computer Science 2(4) (2008)
    locator: Section 11.4, buffer trees
---

The buffer tree of Arge is a search tree for external memory in which each internal node has a *buffer* that holds up to $M$ pending operations. An insert, a delete or a query is not carried out at once: it is put into the buffer of the root, and when a buffer overflows, all its operations move one level down together, at a cost of $O(1/B)$ I/Os each. When an operation reaches the leaves it is applied, and a query is answered then. With fan-out $\Theta(M/B)$, a sequence of $N$ operations costs $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os in total, the cost of [sorting](/external-merge-sort/), which is $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ amortized per operation and far below one I/O. The price is that answers come late: the structure is *batched*, for algorithms that can wait for their answers. It is the base of the I/O-optimal [external memory priority queue](/external-memory-priority-queue/) and of many batched algorithms, such as [time-forward processing](/time-forward-processing/).

## In plain words

Think of a large office where letters must reach the right desk. A clerk who walks each letter to its desk spends the day walking. Instead, each room has a tray. New letters go into the tray at the entrance. When the tray is full, someone sorts it and carries each bundle to the tray of the next room on the way. Bundles move only when a tray is full, so each walk carries many letters.

A letter that asks a question gets its answer only when it reaches the last desk. So you wait for answers, but the total walking is small: each letter is carried only a few times, always in a big bundle.

## The abstract type

The buffer tree on this page is a *batched* [dictionary](/dictionary/) on a set of distinct keys: `insert(k)`, `delete(k)`, and `query(k)`, which asks whether $k$ is in the set at the time of the query. A query returns at once only a ticket. Its answer is the correct answer for the moment when it was asked, but it is ready only when the query reaches the leaves, at the latest after `flush`, which empties all buffers. This fits algorithms that know all their queries in advance, or that can go on without the answers for a while: [offline algorithms](/offline-algorithm/), sorting, and graph algorithms. Arge also gives batched range queries and a priority queue on the same tree.

## Representation

There is a block size $B$, a memory of $M$ items, and $m = M/B$.

- The tree is an $(a, b)$-tree with $b = m$: each internal node has at most $m$ children and routing keys between them, as in a [B-tree](/b-tree/), and all leaves have the same depth. A *leaf* is one block of at most $B$ keys. An internal node whose children are leaves is a *bottom node*.
- Each internal node $x$ has a *buffer*, a list of operations on disk. An operation is a triple of a kind (insert, delete or query), a key, and a *time stamp*, its position in the input sequence. The buffer of $x$ holds operations on keys in the range of $x$.
- A buffer is *full* when it holds more than $M$ operations.

**Invariants.**

- **(T1)** The routing keys give the search order, and all leaves are at one depth.
- **(T2)** Each operation in the buffer of $x$ has its key in the range of $x$.
- **(T3)** The buffer of each node is in time order, and every operation in the buffer of a node is older than every operation in the buffers of its ancestors.
- **(T4)** No buffer is full after an operation ends.

Invariant (T3) is the heart of the structure. For one key $k$, all operations on $k$ go down the same path, and the older ones are always lower. So when they reach the leaves, they are applied in the order of time.

Arge's tree uses $a = m/4$ and keeps every node between $a$ and $b$ children by splits, fusions and shares, as in a B-tree. The code of this page splits nodes as Arge does, but handles deletions by global rebuilding: after many deletions it flushes the tree and builds it again from the sorted keys.

## Operations

```pseudo id=main
OPERATION(T, op)               ▷ op: insert, delete or query, with a key and a time stamp
L1  append op to T.root.buf     ▷ one block of the root buffer is kept in memory
L2  if T.root.buf has more than M operations then EMPTY(T.root)

EMPTY(x)                       ▷ all ancestors of x have empty buffers
L3  ops ← the buffer of x, in time order; x.buf ← empty
L4  if x is a bottom node then EMPTY-BOTTOM(x, ops), return
L5  for each op in ops, in order: append op to the buffer of the child whose range holds op.key
L6  for each child c of x whose buffer is now full: EMPTY(c)

EMPTY-BOTTOM(x, ops)           ▷ the children of x are leaves
L7  S ← the set of keys in the leaves of x
L8  for each op in ops, in order do
L9      insert: add op.key to S; delete: remove op.key from S; query: answer (op.key ∈ S)
L10 replace the leaves of x by ⌈|S|/B⌉ leaves holding S in order, and set the routing keys
L11 if x has more than m children then SPLIT(x)

SPLIT(x)                       ▷ the buffer of x and of all its ancestors is empty
L12 g ← ⌈(number of children of x)/m⌉; cut the children into g groups of nearly equal size
L13 x keeps the first group; the other groups go into new nodes, put right after x in its parent with the routing keys between the groups
L14 if x is the root then make a new root whose children are x and the new nodes
L15 if the parent now has more than m children then SPLIT(parent)
```

**Why the ancestors are empty.** EMPTY clears the buffer of $x$ in line L3 before it recurses in line L6. So when EMPTY reaches a node, the buffers of all nodes on the path above it are empty. A split happens only in line L11, inside such a call, and goes up only along that path, so line L12 never cuts a node with pending operations. This is why Arge empties buffers top-down and rebalances only at the bottom.

**Reading a buffer.** In line L3 Arge reads the first $M$ operations into memory, sorts them by key, and merges them with the rest of the buffer, which was written as sorted runs. The code of this page keeps the buffer in time order and routes each operation on its own, which gives the same moves and the same count of block transfers.

**Flush.** To get all answers, empty the buffers of all nodes top-down, full or not. A query that only needs one answer soon can force the buffers on its own path.

## Example

Take $B = 2$ and $m = 4$, so $M = 8$: a leaf holds 2 keys, a node has at most 4 children, and a buffer is full above 8 operations. An internal node is written $\langle$routing keys | operations in the buffer$\rangle$ followed by its children.

1. Insert $50, 20, 80, 10, 60, 30, 70, 40$. All eight wait in the root buffer, and no key is in a leaf: $\langle\ |\ 8\rangle([\,])$.
2. Query 30. The buffer now has 9 operations, more than $M$, so EMPTY runs on the root, which is a bottom node. It applies the nine operations in time order, so the query finds 30, and builds four leaves: $\langle 30\ 50\ 70 \mid 0\rangle([10\ 20]\ [30\ 40]\ [50\ 60]\ [70\ 80])$.
3. Insert $90, 15, 25$, delete 30, query 30, query 25. These six operations wait in the root buffer. The second query of 30 has no answer yet.
4. Flush. The root applies the six operations: the query of 30 comes after the delete and gets *false*, the query of 25 gets *true*. The ten keys need five leaves, more than $m = 4$, so the root splits into two bottom nodes of 3 and 2 leaves under a new root: $\langle 60 \mid 0\rangle(\langle 20\ 40 \mid 0\rangle([10\ 15]\ [20\ 25]\ [40\ 50])\ \ \langle 80 \mid 0\rangle([60\ 70]\ [80\ 90]))$.

From now on, a full root buffer is not applied to leaves but split by the routing key 60 into the buffers of the two children, and each child is emptied only when its own buffer overflows.

## Correctness

The answer to a query depends only on the operations on the same key that came before it. By (T2), all operations on a key $k$ are on the path from the root to the leaf of $k$. By (T3), on that path, older operations are lower, and in one buffer they are in time order. EMPTY keeps this: it moves a whole buffer, in order, to the end of the child buffers, and every operation already in a child buffer is older, because it left $x$ in an earlier emptying. EMPTY-BOTTOM then applies the operations on $k$ to the leaves in time order, after all older ones, so the set $S$ at the time of a query is the set of the abstract dictionary at that time, restricted to the keys of $x$. Splits only move whole subtrees with empty buffers above them, so they keep (T1) to (T3). The full proof is below.

## Complexity

**Height.** Each node other than the root has at least about $m/2$ children when it is made by a split, and with Arge's fusions every node keeps at least $m/4$. The leaves hold $\Theta(B)$ keys. So the height is $O(\log_m \frac{N}{B})$.

**Theorem (Arge).** A sequence of $N$ operations on an initially empty buffer tree makes $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os, so $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ amortized per operation.

*Why.* An emptying of a full buffer with $X > M$ operations reads $\lceil X/B \rceil$ blocks and writes at most one partial block to each of at most $m$ children besides $X/B$ full ones, so it costs $O(X/B + m)$. Since $X > M = mB$, $m < X/B$, and the cost is $O(X/B)$: each operation in the buffer pays $O(1/B)$ to move one level down. An operation goes down at most once per level, so it pays $O(\frac{1}{B}\log_m\frac{N}{B})$ in all. At a bottom node, reading and writing at most $m$ leaves plus the new ones is again $O(X/B)$. A split writes $O(1)$ nodes per new node, and each new node needs $\Omega(m)$ inserts below it, so splits add $O(N/(Bm))$ I/Os. The root buffer costs $N/B$ writes. Flushing at the end costs $O(\frac{N}{B}\log_m\frac{N}{B})$, since each operation still goes down at most once per level, plus $O(m)$ per node for partial blocks, which is $O(N/B)$ in total.

| measure | cost |
|---|---|
| $N$ operations, total | $O\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os |
| one operation, amortized | $O\big(\frac{1}{B}\log_{M/B}\frac{N}{B}\big)$ I/Os |
| delay of an answer | up to the next flush |
| space | $O(N/B)$ blocks |
| memory | $O(M)$ |

For comparison, $N$ inserts into a [B-tree](/b-tree/) cost $\Theta(N\log_B N)$ I/Os, more than $B$ times as many, and [sorting](/external-merge-sort/) $N$ keys costs $\Theta\big(\frac{N}{B}\log_{M/B}\frac{N}{B}\big)$, the same as the buffer tree. In fact, inserting $N$ keys and flushing sorts them, so the buffer tree gives an optimal sort.

## Variants

- **Priority queue.** Arge's priority queue keeps the $\Theta(M)$ smallest elements in memory, refilled by flushing the buffers on the leftmost path; see the [external memory priority queue](/external-memory-priority-queue/).
- **Batched range searching.** Range queries go down like other operations and report the keys in their range at the bottom nodes, with an extra $O(Z/B)$ for $Z$ answers. Arge uses this for batched segment trees and for the orthogonal line segment intersection problem.
- **Rebalancing.** Arge's tree fuses or shares a bottom node that has too few leaves with a sibling, after emptying the sibling's buffer, so all nodes keep $\Theta(m)$ children. The code of this page uses global rebuilding for deletions instead.
- **The B^ε-tree.** The [B^ε-tree](/b-epsilon-tree/) uses the same buffers with a fan-out of $B^\varepsilon$ and buffers of $B$, so that a query can read the buffers on its path and get its answer at once, with no batching.
- **The log-structured merge tree.** The [LSM tree](/log-structured-merge-tree/) also defers writes, by merging sorted runs. See [write-optimized data structures](/write-optimized-structure/).

## When to use it

Use a buffer tree when an algorithm issues a long sequence of operations and can wait for the answers: building indexes, batched range queries, sweep-line algorithms in external memory, and graph algorithms that send values through a priority queue. It turns an algorithm that would make one I/O per operation into one that runs at the speed of sorting. When each answer is needed before the next operation can be chosen, as in an online database, use a [B-tree](/b-tree/) or a [B^ε-tree](/b-epsilon-tree/).

## Pitfalls

- **Losing the time order.** Operations must reach the leaves in the order of their time stamps for each key. Sorting a buffer by key alone, without the time stamp as a second key, can apply a delete before the insert it should follow.
- **Rebalancing a node with a full buffer above it.** A split or fusion moves key ranges between nodes. If a buffer above has pending operations, they may be routed by the old ranges. Rebalance only along a path whose buffers are empty, as EMPTY guarantees.
- **Forgetting the partial blocks.** Emptying a buffer writes a partial block to each child that receives operations. With fan-out $m$ this is up to $m$ extra writes, which is only paid for because a full buffer has more than $mB$ operations. Emptying small buffers often, for example to answer each query early, loses the bound.
- **A flush that misses nodes.** A split during a flush can move children that were not yet visited to a new node. The flush must go on until no buffer holds an operation, as the code of this page does.
- **Expecting online answers.** A query is answered only when it reaches a leaf. Code that reads the answer at once gets nothing.

## Implementations

## History

Arge introduced the buffer tree at WADS 1995, with the journal version in Algorithmica in 2003, as a general way to turn internal-memory algorithms that use search trees and priority queues into I/O-optimal batched algorithms. He applied it to sorting, to batched range searching, to an external priority queue, and to problems of computational geometry such as orthogonal line segment intersection. The external priority queue built on it was used in the external graph algorithms of Chiang and others for [time-forward processing](/time-forward-processing/). Vitter's survey presents buffer trees in its chapter on multiway trees.

## References
