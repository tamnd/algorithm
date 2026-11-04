---
tag: THZT7C
kind: data-structure
slug: multiqueue
name: MultiQueue
area: data-structures/concurrent-structures
level: research
summary: Relaxed concurrent priority queue of many sequential heaps, where operations pick random heaps to cut contention.
prereqs: [relaxed-priority-queue, binary-heap, mutex]
see_also: [spraylist, power-of-two-choices, balls-into-bins, delta-stepping, fine-grained-concurrent-heap, lock-striping, work-stealing, linearizability]
sources:
  - paper: doi:10.1145/2755573.2755616
    title: Hamza Rihani, Peter Sanders and Roman Dementiev, MultiQueues, simple relaxed concurrent priority queues, SPAA 2015 (brief announcement)
    locator: pages 80 to 82, the structure, the two-choice delete-min, and the measured rank error and throughput
  - paper: doi:10.1145/3087801.3087810
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Giorgi Nadiradze, The power of choice in priority scheduling, PODC 2017
    locator: pages 283 to 292, the sequential two-choice process and its bounds on the expected and the largest rank
  - paper: doi:10.1145/2688500.2688523
    title: Dan Alistarh, Justin Kopinsky, Jerry Li and Nir Shavit, The SprayList, a scalable relaxed priority queue, PPoPP 2015
    locator: pages 11 to 20, the relaxed priority queue that the MultiQueue is compared with
---

A MultiQueue is a [relaxed priority queue](/relaxed-priority-queue/) made of $c$ ordinary sequential [binary heaps](/binary-heap/), each protected by its own lock, with $c$ usually a small multiple of the number of threads. Insert puts the item into a random heap. Delete-min looks at the minima of two random heaps and removes the smaller of the two. Threads almost never want the same lock, so the structure scales, and by the [power of two choices](/power-of-two-choices/) the heaps stay balanced enough that the item removed is close to the true minimum: its expected rank grows linearly with $c$ and does not depend on the number of items. Rihani, Sanders and Dementiev proposed the structure in 2015, and Alistarh, Kopinsky, Li and Nadiradze proved its rank bounds in 2017.

## In plain words

A bank has many counters instead of one line. Each new customer joins the line at a random counter. When a teller is free, it looks at the first customer at two random counters and serves the one who has waited longer.

The customer served is not always the one who has waited longest in the whole bank, but almost always one of the first few. In return, tellers rarely get in each other's way, because each one works at its own pair of counters.

## The abstract type

The MultiQueue implements a relaxed priority queue over a multiset $Q$:

- insert$(x)$ adds $x$ to $Q$.
- delete-min() removes and returns some item of $Q$, or returns EMPTY if $Q$ is empty.

Each operation is [linearizable](/linearizability/) with respect to this nondeterministic specification: the item returned is some item present at the linearization point. The specification says nothing about which one. How close the item is to the minimum is a separate, probabilistic guarantee: the *rank* of $x$ is $1 + |\{y \in Q : y < x\}|$, and the MultiQueue keeps the expected rank $O(c)$ under the conditions of the analysis (see Complexity).

## Representation

- $Q.heap[0..c-1]$: sequential min-heaps.
- For each heap, a lock and a cached minimum $top$, written under the lock and read without it ($+\infty$ for an empty heap). Reading the cached minimum is one read of one word, so delete-min can compare two heaps without locking them.

The items of $Q$ are the union of the heaps. There is no order between heaps.

## Operations

```pseudo id=main
INSERT(Q, x)
L1  repeat i ← a random index in 0..c−1 until TRY-LOCK(Q.heap[i])
L2  push x on Q.heap[i] and update its top
L3  UNLOCK(Q.heap[i])

DELETE-MIN(Q)
L4  loop
L5      i, j ← two random indices in 0..c−1
L6      read Q.heap[i].top and Q.heap[j].top; let k be the index with the smaller top
L7      if both tops are +∞ then return SCAN(Q)
L8      if TRY-LOCK(Q.heap[k]) then
L9          if Q.heap[k] is not empty then x ← pop the minimum of Q.heap[k]; update its top; UNLOCK(Q.heap[k]); return x
L10         UNLOCK(Q.heap[k])                ▷ emptied since the read; try again

SCAN(Q)
L11 LOCK(Q.heap[0]), ..., LOCK(Q.heap[c−1]), in this order
L12 if all heaps are empty then x ← EMPTY else x ← pop the minimum of the heap with the smallest top
L13 UNLOCK all heaps; return x
```

**Insert.** An insert never waits for a lock: if the heap it picked is busy, it picks another one (line L1).

**Delete-min.** The two tops are read without locks, so they may be stale. That only affects quality, not safety: after the lock is taken, the heap is checked again (line L9), and the minimum of the heap at that moment is removed.

**Empty.** Two empty heaps do not mean an empty MultiQueue. The scan of lines L11 to L13 locks all heaps, in index order, and returns EMPTY only when all of them are empty at once. Rihani, Sanders and Dementiev do not need this step for their uses; it is what makes EMPTY linearizable.

## Example

Four heaps: heap 0 holds 3 and 9, heap 1 holds 1 and 7, heap 2 holds 5, heap 3 holds 4. The true order is 1, 3, 4, 5, 7, 9.

| call | heaps picked | tops | removes | rank of the item | heaps after |
|---|---|---|---|---|---|
| delete-min | 0 and 2 | 3 and 5 | 3 | 2 (1 is smaller) | [9], [1, 7], [5], [4] |
| delete-min | 1 and 3 | 1 and 4 | 1 | 1 | [9], [7], [5], [4] |
| delete-min | 2 and 3 | 5 and 4 | 4 | 1 | [9], [7], [5], [] |

The first call returns 3 although 1 is present, a rank error of 1. Now let two threads call delete-min at the same time, and both pick heap 1 as the better heap. One of them gets the lock. The other fails at line L8 and picks two new heaps, instead of waiting. Calls that pick different heaps do not interact at all.

## Correctness

The structure is linearizable with respect to the relaxed specification. An insert takes effect at its push at line L2, while it holds the lock of its heap. A delete-min that returns an item takes effect at its pop at line L9 or line L12; the item is in the heap at that moment, so it is in $Q$. A delete-min that returns EMPTY takes effect at line L12, when it holds every lock and every heap is empty, so $Q$ is empty at that moment. Each heap is changed only under its lock, so it stays a valid heap with a correct cached minimum. Progress: a thread waits for a lock only in the scan, which takes the locks in a fixed order, and every holder of a single lock releases it within a constant number of its own steps, so there is no deadlock; inserts and the fast path of delete-min only try locks and never wait for one. The full proof is in [the correctness proof](proofs/correctness.md). The rank bounds below are proved by Alistarh, Kopinsky, Li and Nadiradze and are not part of this proof.

## Complexity

| quantity | value |
|---|---|
| insert | $O(\log m)$ for a heap of $m$ items, plus retries when a lock is busy |
| delete-min | $O(\log m)$, plus retries; a scan, when both picks are empty, costs $O(c)$ locks |
| expected rank of a deleted item | $O(c)$ |
| largest rank over a long run, with high probability | $O(c \log c)$ |
| space | $O(c + |Q|)$ |

The rank bounds are those that Alistarh, Kopinsky, Li and Nadiradze proved for the sequential process in which each insert goes to a uniformly random heap and each delete-min removes the better of two random heaps, with $c$ heaps. Concurrent runs only approximate this process, since reads of the tops may be stale. The intuition is that of [balls into bins](/balls-into-bins/) with two choices: a heap whose minimum is unusually small is likely to be chosen and corrected soon, so no heap falls far behind the others. With a single random choice the heaps drift apart and the rank grows without bound over time. In the tests of the Python module, with 8 heaps, the mean rank is below 7.

Rihani, Sanders and Dementiev report that the MultiQueue scales better than the other concurrent priority queues in their experiments, with a small rank error.

## Variants

- **Buffers and stickiness.** Later engineering work lets a thread keep using the same heaps for several operations and buffer items at each heap, which saves cache misses at the cost of a larger rank error.
- **One choice versus two.** Picking only one random heap is cheaper but unstable in the sense above. Picking $d > 2$ heaps gives smaller ranks and more reads.
- **[SprayList](/spraylist/).** A relaxed queue on one shared skip list, where delete-min jumps to a random item among the first $O(p \log^3 p)$.
- **k-LSM.** A relaxed queue with a deterministic bound $k$ on the rank error of every call.
- **Exact queues.** With $c = 1$ the MultiQueue is a heap with one lock, an exact but sequential priority queue. A [fine-grained concurrent heap](/fine-grained-concurrent-heap/) is exact with more parallelism.

## When to use it

Use a MultiQueue as the work list of a parallel algorithm that tolerates out-of-order processing, such as parallel shortest paths in the style of [delta-stepping](/delta-stepping/) or Dijkstra with relaxed order, branch and bound, and task schedulers with priorities. It is simple: a few sequential heaps and locks, no lock-free code. Do not use it where the order is part of the correctness of the program, for example where an event must not be processed before an earlier one.

## Pitfalls

- **Too few heaps.** With $c$ close to the number of threads, threads often pick the same heaps and the locks become hot. Use a small multiple, such as $2p$ to $4p$ for $p$ threads.
- **Trusting a stale top.** The cached minimum is read without the lock. Check the heap again after locking, or a delete-min may pop from an empty heap.
- **Returning EMPTY too early.** Two empty heaps say nothing about the other heaps. Return EMPTY only after a full check, or document that EMPTY is approximate.
- **A bad random source.** A shared random generator is itself a point of contention. Give each thread its own generator.
- **Rank as a guarantee.** The rank bounds are probabilistic. An adversarial pattern of inserts and deletes, or a scheduler that delays one thread for long, can make single calls return items of high rank.

## Implementations

The Python module keeps each heap as a list with heapq, a lock and a cached minimum, and models each read of a cached minimum, each lock attempt and each heap change as one step of a generator. The tests replay the example with scripted random choices, show that a busy lock makes delete-min try other heaps, compare random sequential runs with a multiset, measure the mean rank, check random interleavings of three threads against the relaxed specification with a linearizability search, and run the plain methods under real threads.

## History

Earlier parallel codes, for example for branch and bound, already kept several local queues and moved work between them. Rihani, Sanders and Dementiev presented the MultiQueue, with the two-choice delete-min, as a brief announcement at SPAA 2015. Alistarh, Kopinsky, Li and Nadiradze analysed it in 2017 and proved that the two-choice process keeps the rank error bounded in terms of the number of heaps alone.

## References
