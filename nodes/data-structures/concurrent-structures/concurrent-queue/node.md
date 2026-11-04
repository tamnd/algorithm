---
tag: EBTAW1
kind: data-structure
slug: concurrent-queue
name: Concurrent queue
aliases:
- thread-safe queue
area: data-structures/concurrent-structures
level: core
summary: A FIFO queue supporting concurrent enqueue and dequeue from many threads.
implements: [queue]
prereqs: [queue, linearizability, mutex]
see_also: [two-lock-queue, michael-scott-queue, lcrq, lamport-spsc-queue, vyukov-bounded-mpmc-queue, kogan-petrank-queue, disruptor-ring-buffer, consensus-number]
sources:
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 10 (Concurrent Queues and the ABA Problem), the sections on the bounded partial queue, the unbounded total queue and the unbounded lock-free queue
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: Section 1 (the survey of earlier queues) and Section 2 (the two algorithms)
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM TOPLAS 12(3), 1990
    locator: Section 2 (the definition) and the queue examples of Section 2
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM TOPLAS 13(1), 1991
    locator: the section on read-modify-write and queue objects, which shows that a FIFO queue has consensus number 2
---

A concurrent queue is a [queue](/queue/) that many threads share: each thread may call enqueue and dequeue at any time, and each call acts as if it took effect at one instant between its call and its return. This condition is [linearizability](/linearizability/). The simplest correct design guards a sequential linked queue with one [mutex](/mutex/). Faster designs split the lock in two, as the [two-lock queue](/two-lock-queue/) does, or use no lock at all, as the [Michael-Scott queue](/michael-scott-queue/) and [LCRQ](/lcrq/) do. This page gives the abstract type, the one-lock design and its proof, and a map of the other designs.

## In plain words

A queue is a line of items: you add at the back and take from the front. When several threads use the same queue at the same time, their steps can mix. Without care, two threads can add at the back at the same moment and one item is lost, or two threads take the same item from the front.

A concurrent queue prevents this. The simplest way is one lock. A thread takes the lock, does its whole change of the line, and gives the lock back. Other threads wait. The result is the same as if the operations came one after another, in the order in which the threads got the lock. The cost is that only one thread works on the queue at a time, so more threads do not make it faster.

## The abstract type

The object holds a sequence $s$ of items, at first empty. It has two operations.

- $\mathrm{enq}(x)$ changes $s$ to $s \cdot x$ and returns nothing.
- $\mathrm{deq}()$ returns the first item $s_1$ and changes $s$ to $s_2 \cdots s_k$ when $s$ is not empty. On an empty $s$ it returns the special value EMPTY and does not change $s$.

A dequeue that returns EMPTY is a *total* method. Some designs make deq *partial* instead: on an empty queue it waits until an item comes. A *bounded* queue has a capacity $N$, and enq on a full queue returns FULL or waits. The type is the sequential [queue](/queue/) type. The concurrent object must be linearizable with respect to it: for each history $H$ of calls and returns there is a sequential history $S$ of the queue type that has the same calls and results, and that keeps the real-time order of $H$ (if a call returns before another call starts, it comes first in $S$).

## Representation

The queue is a singly linked list with a sentinel node. The fields are:

- $Q.head$: the sentinel. The items are the values of the nodes after it.
- $Q.tail$: the last node of the list.
- $Q.lock$: one mutex.

**Invariant (Q).** When no thread holds $Q.lock$: the list from $Q.head$ is finite, $Q.tail$ is its last node, and the values of the nodes after $Q.head$, in list order, are the sequence $s$ of the abstract queue.

The sentinel means that an empty queue still has one node, so enqueue never has to test for an empty list and dequeue never has to change $Q.tail$.

## Operations

```pseudo id=main
ENQ(Q, x)
L1  n ← new node with value x and next = nil
L2  acquire(Q.lock)
L3  Q.tail.next ← n
L4  Q.tail ← n
L5  release(Q.lock)

DEQ(Q)
L6  acquire(Q.lock)
L7  first ← Q.head.next
L8  if first = nil then release(Q.lock); return EMPTY
L9  Q.head ← first                         ▷ first becomes the new sentinel
L10 x ← first.value
L11 release(Q.lock)
L12 return x
```

**Enqueue.** Line L1 builds the node before the lock is taken, so the critical section holds only the two pointer writes of lines L3 and L4. Both run alone, so no other thread sees the list between them.

**Dequeue.** Line L7 reads the first real node. If there is none, the queue is empty and the call returns EMPTY (line L8). Otherwise line L9 moves the sentinel one node forward: the old first node becomes the new sentinel, and its value is the result. The old sentinel is no longer reachable and can be freed.

Each operation runs $O(1)$ steps of its own. The wait at line L2 or L6 depends on the lock and on the other threads, see the complexity section.

## Example

Three threads share an empty queue: $A$ calls enq(1), $B$ calls enq(2) and $C$ calls deq(). One step is one action on shared memory or one failed try to take the lock (a spin). The interleaving is this.

| step | thread | what it does | lock holder | list after head |
|---|---|---|---|---|
| 1 | $A$ | L1 to L3: takes the lock, links node 1 | $A$ | 1 |
| 2 | $B$ | L2: the lock is taken, spins | $A$ | 1 |
| 3 | $C$ | L6: the lock is taken, spins | $A$ | 1 |
| 4 | $A$ | L4: tail is node 1 | $A$ | 1 |
| 5 | $A$ | L5: releases; enq(1) returns | none | 1 |
| 6 | $C$ | L6, L7: takes the lock, first is node 1 | $C$ | 1 |
| 7 | $B$ | L2: spins | $C$ | 1 |
| 8 | $C$ | L9: node 1 is the new sentinel | $C$ | empty |
| 9 | $C$ | L10, L11: releases; deq() returns 1 | none | empty |
| 10 | $B$ | L2, L3: takes the lock, links node 2 | $B$ | 2 |
| 11 | $B$ | L4 | $B$ | 2 |
| 12 | $B$ | L5: releases; enq(2) returns | none | 2 |

The calls of $B$ and $C$ overlap, and $B$ started first. Still, the linearization is enq(1), deq() → 1, enq(2): the order in which the threads got the lock. This order is legal for a queue. Real time puts no constraint here, because each call started before any call returned (enq(1) returned at step 5, after $B$ and $C$ had started at steps 2 and 3).

## Correctness

The one-lock queue is linearizable, and it is deadlock-free when the lock is deadlock-free. The proof takes the moment at which each call gets the lock as its [linearization point](/linearization-point/). Mutual exclusion orders the critical sections. Each critical section runs the sequential code alone, so the invariant (Q) holds at each release, and the result of each call is the result that the sequential queue gives in that order. The full proof, with the case of the total dequeue, is in [the correctness proof](proofs/correctness.md).

No design can be both wait-free and built only from read and write registers. A FIFO queue solves wait-free [consensus](/consensus-number/) for two threads: put WIN and then LOSE in the queue; each thread writes its proposal to its own register, dequeues, and decides its own proposal if it got WIN and the other proposal if it got LOSE. Exactly one thread gets WIN, so both decide the proposal of the winner. Registers have consensus number 1 (see [registers have consensus number one](/registers-have-consensus-number-one/)), so a wait-free queue needs a stronger primitive, such as [compare-and-swap](/compare-and-swap/) or [fetch-and-add](/fetch-and-add/). Herlihy proved that the queue has consensus number exactly 2.

## Complexity

Let $p$ be the number of threads. A step is one shared-memory action.

| operation | own steps | wait at the lock |
|---|---|---|
| enq | $O(1)$ | up to $p - 1$ critical sections with a FIFO lock; unbounded with a test-and-set lock |
| deq | $O(1)$ | the same |
| space | $n + 1$ nodes for $n$ items | |

A critical section has $O(1)$ steps. With a fair (first-come, first-served) lock such as a [ticket lock](/ticket-lock/), a thread waits for at most the $p - 1$ threads that are ahead of it, so its call ends within $O(p)$ critical sections. With a plain [spin lock](/spin-lock/) a thread can lose the race for the lock each time, so the lock is only deadlock-free, not [starvation-free](/starvation-freedom/).

The throughput is the problem. All calls pass through one lock, so at most one call makes progress at a time, whatever $p$ is. On a real machine the cache line of the lock also moves from core to core at each handoff, so the time for one handoff grows with contention.

## Variants

- **[Two-lock queue](/two-lock-queue/).** One lock for the head and one for the tail, so one enqueue and one dequeue run in parallel. The sentinel keeps the two ends apart.
- **[Michael-Scott queue](/michael-scott-queue/).** No lock: enqueue links its node with [compare-and-swap](/compare-and-swap/) and fixes a lagging tail. It is [lock-free](/lock-freedom/). It needs safe memory reclamation, for example [hazard pointers](/hazard-pointers/), and care for the [ABA problem](/aba-problem/).
- **[LCRQ](/lcrq/).** Ring buffers driven by [fetch-and-add](/fetch-and-add/), linked in a list. Fewer failed CAS loops under high contention.
- **[Lamport's single-producer single-consumer queue](/lamport-spsc-queue/).** A ring buffer with two indices and no atomic read-modify-write at all, correct when only one thread enqueues and one thread dequeues.
- **[Vyukov's bounded MPMC queue](/vyukov-bounded-mpmc-queue/)** and the **[Disruptor ring buffer](/disruptor-ring-buffer/).** Bounded, preallocated rings with a sequence number in each cell.
- **[Kogan-Petrank queue](/kogan-petrank-queue/).** A wait-free queue that uses [helping](/helping/).
- **Blocking queue.** A partial deq that waits on a [condition variable](/condition-variable/) when the queue is empty, as in the [bounded buffer problem](/bounded-buffer-problem/).
- **Relaxed queues.** Give up exact FIFO order for speed, in the same way as a [relaxed priority queue](/relaxed-priority-queue/).

## When to use it

Use the one-lock queue when contention is low, when the code must be short and easy to check, or when each item takes much longer to process than the queue operation. Use the [two-lock queue](/two-lock-queue/) when producers and consumers both run at a high rate. Use a lock-free queue when a thread can be delayed while it holds a lock (a page fault, a preemption, a signal handler) and the other threads must not wait for it. Use a bounded ring when memory must be preallocated or when the producer must slow down when the consumers fall behind.

## Pitfalls

- **Two separate checks.** Code that tests "is the queue empty?" and then calls deq in a second critical section can fail, because another thread can take the last item between the two calls. Make the check and the removal one operation, as line L8 does.
- **No sentinel.** Without the sentinel node, a dequeue of the last item must change $Q.tail$ too, and an enqueue on an empty queue must change $Q.head$. With one lock this is only more code, but with two locks the two ends then share fields and the design breaks.
- **Work inside the critical section.** Allocating the node after line L2 makes the critical section longer for all threads. Line L1 allocates first.
- **Releasing on each path.** The early return of line L8 must release the lock too. A missing release blocks all threads for ever.
- **Reading the result after release.** If line L10 runs after line L11, another dequeue can make the node the old sentinel and free it, so the read touches freed memory in a language without a garbage collector.

## Implementations

The Python class follows the pseudocode. Each operation is a generator that yields after each shared step, and the lock is taken by repeated non-blocking tries, so the tests can drive any interleaving step by step, and then check the history with a linearizability search. The plain methods run the same steps in the calling thread, so the class also works with real `threading` threads.

## History

Herlihy and Wing defined linearizability in 1990 and used the FIFO queue as their main example. Herlihy showed in 1991 that a queue has consensus number 2. Michael and Scott in 1996 gave the two-lock queue and the lock-free queue, and surveyed the earlier designs. The `ConcurrentLinkedQueue` class of Java is based on their lock-free queue.

## References
