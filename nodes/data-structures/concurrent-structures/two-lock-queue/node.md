---
tag: PMYQM4
kind: data-structure
slug: two-lock-queue
name: Two-lock queue
aliases:
- Michael-Scott two-lock queue
area: data-structures/concurrent-structures
level: core
summary: Blocking concurrent queue with separate locks for head and tail, so enqueuers and dequeuers do not contend.
implements: [queue]
prereqs: [concurrent-queue, sentinel-node, mutex]
see_also: [michael-scott-queue, lock-striping, linearization-point, lcrq, deadlock-freedom, linked-list]
sources:
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: Section 2, Figure 2 (the two-lock queue) and Section 3 (correctness)
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 10 (Concurrent Queues and the ABA Problem), the sections on the bounded partial queue and the unbounded total queue, which use an enqueue lock and a dequeue lock
  - url: https://www.cs.rochester.edu/research/synchronization/pseudocode/queues.html
    title: Maged M. Michael and Michael L. Scott, pseudocode of the non-blocking and two-lock concurrent queues
    locator: the two-lock concurrent queue algorithm
---

The two-lock queue is a [concurrent queue](/concurrent-queue/) on a singly linked list with a [sentinel node](/sentinel-node/), and with two [mutexes](/mutex/): one for the head, held by dequeuers, and one for the tail, held by enqueuers. So one enqueue and one dequeue run at the same time, while two enqueues, or two dequeues, still take turns. Michael and Scott published it in 1996, next to their lock-free queue. It is [linearizable](/linearizability/) and [deadlock-free](/deadlock-freedom/), each operation takes $O(1)$ steps besides the wait for its lock, and it is the design of the `LinkedBlockingQueue` class of Java.

## In plain words

Think of a line of people at a counter. New people join at the back, and the clerk serves people at the front. The back and the front are far apart, so the person who joins and the clerk who serves do not get in the way of each other. Only two people who join at the same moment must take turns, and so must two clerks.

The two-lock queue does this with two locks: one for the back and one for the front. A thread that adds an item takes the back lock. A thread that removes an item takes the front lock. The trick that makes this safe is a dummy first node that is always there. Because of it, the back and the front never share a field, except one pointer when the queue is empty, and that pointer is written and read in one step.

## The abstract type

The two-lock queue implements the [queue](/queue/): enq$(x)$ appends $x$, and deq() removes and returns the first item, or returns EMPTY when there is none. Both methods are total: they never wait for the queue to change. The concurrent correctness condition is [linearizability](/linearizability/) with respect to this sequential type, as on the page [concurrent queue](/concurrent-queue/).

## Representation

- $Q.head$: the sentinel node. The items are the values of the nodes after it.
- $Q.tail$: a node of the list, normally the last one.
- $Q.hlock$, $Q.tlock$: two mutexes.

Each node has a value and a next pointer. A read or a write of one next pointer, of $Q.head$ and of $Q.tail$ is atomic.

**Invariant (T).** At each moment the list from $Q.head$ is finite and acyclic, and the abstract queue is the sequence of the values of the nodes after $Q.head$. Only a holder of $Q.tlock$ writes $Q.tail$ or a next pointer of a node in the list. Only a holder of $Q.hlock$ writes $Q.head$. If no thread is between lines L3 and L4, then $Q.tail$ is the last node of the list.

While an enqueuer is between lines L3 and L4, the last node is the one it just linked, and $Q.tail$ is its predecessor. Then a dequeuer can move $Q.head$ to the new node, one node past $Q.tail$, see the example.

## Operations

```pseudo id=main
ENQ(Q, x)
L1  node ← new node with value x and next = nil
L2  acquire(Q.tlock)
L3  Q.tail.next ← node                     ▷ linearization point
L4  Q.tail ← node
L5  release(Q.tlock)

DEQ(Q)
L6  acquire(Q.hlock)
L7  node ← Q.head
L8  new_head ← node.next                   ▷ linearization point if nil
L9  if new_head = nil then release(Q.hlock); return EMPTY
L10 x ← new_head.value
L11 Q.head ← new_head                      ▷ linearization point otherwise
L12 release(Q.hlock)
L13 return x                               ▷ node, the old sentinel, can be freed
```

**Enqueue.** The enqueuer holds $Q.tlock$, so it is the only writer of $Q.tail$ and of the next pointer of the last node. Line L3 links the new node; from this moment the item is in the queue. Line L4 then moves the tail.

**Dequeue.** The dequeuer holds $Q.hlock$, so it is the only writer of $Q.head$. Line L8 reads the next pointer of the sentinel. This is the only field that an enqueuer and a dequeuer can touch at the same time: when the queue is empty, the sentinel is also the last node, and an enqueuer may be writing its next pointer at line L3. The read gets either nil, and then the queue is empty at that moment, or the new node. Line L11 makes the first node the new sentinel, which removes its item.

Each operation runs $O(1)$ steps of its own, plus the wait at line L2 or L6.

## Example

The queue holds one item, 7. Thread $A$ calls enq(8), and threads $B$ and $C$ each call deq(). The nodes are written by their values, and $s$ is the sentinel.

| step | thread | what it does | head | tail | list from head |
|---|---|---|---|---|---|
| 0 | | start | $s$ | 7 | $s$, 7 |
| 1 | $A$ | L1 to L3: takes tlock, links node 8 | $s$ | 7 | $s$, 7, 8 |
| 2 | $B$ | L6 to L8: takes hlock, new_head is node 7 | $s$ | 7 | $s$, 7, 8 |
| 3 | $B$ | L10: $x = 7$ | $s$ | 7 | $s$, 7, 8 |
| 4 | $B$ | L11: head is node 7 | 7 | 7 | 7, 8 |
| 5 | $B$ | L12: releases hlock; deq() returns 7 | 7 | 7 | 7, 8 |
| 6 | $C$ | L6 to L8: new_head is node 8 | 7 | 7 | 7, 8 |
| 7 | $C$ | L10: $x = 8$ | 7 | 7 | 7, 8 |
| 8 | $C$ | L11: head is node 8, one past the tail | 8 | 7 | 8 |
| 9 | $C$ | L12: releases hlock; deq() returns 8 | 8 | 7 | 8 |
| 10 | $A$ | L4: tail is node 8 | 8 | 8 | 8 |
| 11 | $A$ | L5: releases tlock; enq(8) returns | 8 | 8 | 8 |

$A$ never waited for $B$ or $C$. Thread $C$ returned 8 at step 9, before enq(8) returned at step 11. This is allowed: enq(8) took effect at step 1, so the linearization is enq(8) at step 1, deq() → 7 at step 4 and deq() → 8 at step 8. Between steps 8 and 10 the tail is behind the head. The old node 7 is then unreachable from the head, but no thread reads it again: $A$ writes only $Q.tail$ at line L4.

## Correctness

Each operation has one [linearization point](/linearization-point/), a single atomic step inside its critical section: line L3 for an enqueue, line L11 for a dequeue that returns an item, and line L8 for a dequeue that returns EMPTY. Each of these steps changes the abstract queue, the values after $Q.head$, exactly as the operation does in the sequential queue, and no other step changes it. Two facts carry the proof. The tail lock makes $Q.tail$ the last node whenever an enqueuer is about to link, and the head never moves past the last node, so line L3 appends to the list that the head reaches. The two critical sections touch disjoint fields except the next pointer of an empty sentinel, which is read and written atomically. Two locks never nest, so there is no [deadlock](/deadlock/). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $p$ be the number of threads, and a step one shared-memory action.

| operation | own steps | contends with |
|---|---|---|
| enq | 4 shared steps | other enqueuers only, at tlock |
| deq | 4 shared steps, 2 when empty | other dequeuers only, at hlock |
| space | $n + 1$ nodes for $n$ items, 2 locks | |

With a fair lock a call waits for at most $p - 1$ critical sections of the same kind. So the queue can complete up to two operations at a time, against one for the [one-lock queue](/concurrent-queue/). Michael and Scott measured that the two-lock queue beats a single lock when both ends are busy, and that their lock-free queue beats both on a multiprogrammed machine, where a preempted lock holder blocks the others.

## Variants

- **[Michael-Scott queue](/michael-scott-queue/).** The lock-free queue of the same paper, with the same sentinel list. A [compare-and-swap](/compare-and-swap/) replaces each lock, and a thread that sees a tail behind the last node helps to move it.
- **Bounded two-lock queue.** Add an atomic count of the items and a capacity. Enqueuers wait when the count is full and dequeuers when it is zero, with a [condition variable](/condition-variable/) for each lock. Java's `LinkedBlockingQueue` and the bounded partial queue of Herlihy and Shavit work in this way.
- **Partial deq.** A dequeuer that finds the queue empty waits for a signal from the next enqueuer instead of returning EMPTY.
- **More stripes.** The idea of one lock per independent part of a structure is [lock striping](/lock-striping/). The queue has exactly two parts, its ends.

## When to use it

Use the two-lock queue when producers and consumers both work at a high rate, when blocking is acceptable, and when the code must stay simple: it needs no atomic read-modify-write and no special memory reclamation, because a node is freed only by the dequeuer that holds the head lock and no enqueuer reads a node that is no longer the tail. Use a lock-free queue when lock holders can be preempted or when a process must not block. Use one lock if the queue is rarely contended, and a bounded ring if memory must be preallocated.

## Pitfalls

- **No sentinel.** Without the dummy node, an enqueue on an empty queue writes $Q.head$ and a dequeue of the last item writes $Q.tail$, so each side writes a field of the other side and the two locks no longer protect anything. Keep the sentinel: line L11 makes the dequeued node the new sentinel.
- **Publishing the node too early.** Line L3 must run after line L1 has written the value. On hardware or in a language with a weak memory model, the store of line L3 needs release order (and the load of line L8 acquire order); otherwise a dequeuer can see the new pointer before the value.
- **Testing the tail for emptiness.** A dequeuer that tests $Q.head = Q.tail$ for an empty queue reads a field that the enqueuers own, and is wrong between lines L3 and L4. Test the next pointer of the sentinel, as line L8 does.
- **Taking both locks.** An operation that holds both locks, for example a size or a clear, must take them in one fixed order (see [lock ordering](/lock-ordering/)); two such operations with opposite orders deadlock.
- **Freeing the wrong node.** The dequeuer frees the old sentinel, `node` of line L7, not `new_head`, which is now the sentinel.

## Implementations

The Python class follows the pseudocode line by line. The operations are generators that yield after each shared step, and the locks are taken by repeated tries, so the tests replay the interleaving of the example, check that an enqueuer and a dequeuer do not block each other, and check random interleavings against the sequential queue with a linearizability search. The plain methods also run under real threads.

## History

Michael and Scott gave the two-lock queue at PODC 1996, in the paper that also gives their lock-free queue. They wrote it for machines on which no universal atomic primitive was available, and they noted that it allows one enqueue and one dequeue to proceed at the same time.

## References
