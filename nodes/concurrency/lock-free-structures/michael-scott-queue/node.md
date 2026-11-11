---
tag: N8QFHV
kind: data-structure
slug: michael-scott-queue
name: Michael-Scott lock-free queue
aliases:
- MS queue
- Michael-Scott non-blocking queue
- Michael-Scott queue
area: concurrency/lock-free-structures
level: core
summary: Lock-free linearizable FIFO queue on a linked list with a dummy node. CAS links nodes at the tail, and a lagging tail pointer is fixed by whoever sees it.
implements: [queue]
complexity:
  vars: {n: the number of processes, k: the number of operations that run at the same time}
  space: {extra: Θ(1)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [queue, concurrent-queue, singly-linked-list, sentinel-node, compare-and-swap, linearizability, lock-freedom]
see_also: [two-lock-queue, treiber-stack, kogan-petrank-queue, helping, linearization-point, aba-problem, hazard-pointers, lcrq]
sources:
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: Section 2, Figure 1 (the non-blocking queue) and Figure 2 (the two-lock queue); Section 3 (correctness, linearization points and liveness)
  - url: https://www.cs.rochester.edu/research/synchronization/pseudocode/queues.html
    title: Maged M. Michael and Michael L. Scott, pseudocode of the non-blocking and two-lock concurrent queues
    locator: the non-blocking concurrent queue algorithm, with counted pointers
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: Chapter 10 (Concurrent queues and the ABA problem), the unbounded lock-free queue
  - paper: doi:10.1109/TPDS.2004.8
    title: "Maged M. Michael, Hazard pointers: safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004"
    locator: the FIFO queue example, which uses hazard pointers in place of counted pointers
---

The Michael-Scott queue is a [lock-free](/lock-freedom/) [queue](/queue/) on a [singly linked list](/singly-linked-list/). Maged Michael and Michael Scott published it at PODC 1996, together with the blocking [two-lock queue](/two-lock-queue/). The list starts with a dummy node ([sentinel node](/sentinel-node/)). The shared word `Head` points to the dummy, and `Tail` points to the last node or to the node just before it. An enqueue links its node at the end with a [compare-and-swap](/compare-and-swap/) on a `next` field, and then moves `Tail`. A dequeue moves `Head` one node forward with a CAS. Any operation that finds `Tail` one node behind moves it forward first. This is a simple form of [helping](/helping/), and it is what makes the queue lock-free. The queue is [linearizable](/linearizability/), and it is the basis of `ConcurrentLinkedQueue` in Java.

## In plain words

Think of a line of people where each person holds the hand of the next one. A new person takes the hand of the last person in the line, and then a sign that says "the last person is here" is moved to them. A clerk serves people from the front.

Two things happen at the back: holding the hand, and moving the sign. Between them, the sign is one person behind. Anyone who sees that the sign is behind moves it forward before they do their own work. So if the new person falls asleep after taking the hand, nobody waits for them: the next person who comes moves the sign for them.

## The abstract type

The queue has enq$(x)$, which adds $x$ at the back, and deq(), which removes and returns the front item, or returns EMPTY if the queue has no items. Many processes call the operations at the same time. The safety condition is [linearizability](/linearizability/) with respect to a sequential FIFO queue. The progress condition is [lock-freedom](/lock-freedom/): a process that stops at any point does not stop the others, and some operation always completes. The queue is not [wait-free](/wait-freedom/): one operation can fail its CAS without end.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names |
| $k$ | the number of operations in progress at the same time (contention) |

The processes are asynchronous and may crash between any two steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$). The memory is sequentially consistent, except in the paragraph on weak memory. The original paper also uses counted pointers (a pointer and a counter in one word, changed by a double-width CAS) against the [ABA problem](/aba-problem/); the pseudocode below assumes that a node is not reused while a process holds it, as with a garbage collector.

### Fields

- A node has `val` and `next`.
- `Head` points to the dummy node. The items of the queue are in the nodes after the dummy, front first.
- `Tail` points to the last node of the list, or to the node just before the last one.

**Invariant.**

- **(Q1)** The nodes reachable from `Head` form a finite list, and only the last node has `next` = NULL.
- **(Q2)** `Tail` points to a node of this list, and it is the last node or the node before the last one. So `Tail` never points before `Head`.
- **(Q3)** Once a `next` field is not NULL, it never changes; `Head` and `Tail` only move forward along the list.

## Operations

```pseudo id=main
ENQUEUE(v)
L1  n ← new node with n.val = v, n.next = NULL
L2  loop
L3      t ← Tail
L4      nx ← t.next
L5      if t = Tail then                  ▷ t and nx were seen together
L6          if nx = NULL then
L7              if CAS(t.next, NULL, n) then break   ▷ linearization point
L8          else CAS(Tail, t, nx)         ▷ help: Tail lags, move it
L9  CAS(Tail, t, n)                       ▷ swing Tail; failure is fine

DEQUEUE()
L10 loop
L11     h ← Head
L12     t ← Tail
L13     nx ← h.next
L14     if h = Head then
L15         if h = t then                 ▷ empty, or Tail lags
L16             if nx = NULL then return EMPTY   ▷ linearization point: L13
L17             CAS(Tail, t, nx)          ▷ help, so Head cannot pass Tail
L18         else v ← nx.val               ▷ read before the CAS
L19             if CAS(Head, h, nx) then  ▷ linearization point
L20                 retire(h); return v
```

**Enqueue.** L3 to L5 read `Tail` and its `next` field and check that `Tail` did not move in between. If `next` is NULL, $t$ is the last node, and the CAS at L7 links the new node after it. If `next` is not NULL, `Tail` lags behind the last node, and L8 moves it one node forward on behalf of the enqueue that is late. After the node is linked, L9 tries once to move `Tail` to it. If this CAS fails, someone else already moved `Tail`.

**Dequeue.** L11 to L14 read `Head`, `Tail` and the node after `Head`, and check that `Head` did not move. If `Head` and `Tail` point to the same node, either the queue is empty (`next` is NULL) or `Tail` lags, and L17 moves it first. Otherwise L18 reads the value of the next node, and the CAS at L19 makes that node the new dummy. The value is read before the CAS, because after the CAS another dequeue can remove and free that node.

**Linearization points.** An enqueue takes effect at its successful CAS at L7: from then on, its node is in the list. A dequeue that returns an item takes effect at its successful CAS at L19. A dequeue that returns EMPTY takes effect at its read of $h.next$ at L13: the check at L14 shows that `Head` was still $h$ just before and after that read, so at the read, the dummy had no successor.

**The two-lock queue.** The same paper gives a blocking queue with the same list and dummy node, but with one lock for `Head` and one for `Tail`. An enqueue takes the tail lock, links the node and moves `Tail`; a dequeue takes the head lock and moves `Head`. One enqueue and one dequeue run in parallel. The dummy node keeps them apart: they never write the same word. It has its own page, the [two-lock queue](/two-lock-queue/).

### Memory reclamation

After the CAS at L19, the old dummy $h$ is out of the list, but other processes may still hold it: a dequeue that read it at L11 reads $h.next$ at L13, and an enqueue that read it as `Tail` reads $t.next$ at L4. If $h$ is freed and its address is reused, two things go wrong. A stale read at L4 or L13 reads freed memory, and a stale CAS at L7 or L19 can succeed on a new node at the same address (the [ABA problem](/aba-problem/)), which links an item into a node that is no longer in the queue, or moves `Head` to a node that is not in the list. Michael and Scott put nodes on a free list (never back to the system) and add a counter to each pointer, so a stale CAS fails. Later work uses [hazard pointers](/hazard-pointers/) (two per process: one for $h$ or $t$ and one for $nx$) or [epoch-based reclamation](/epoch-based-reclamation/), with plain pointers.

### Weak memory

The fields of a new node must be visible before the node is linked. In C++11 terms, the CAS at L7 needs release order and the reads at L4 and L13 need acquire order. The read of `nx.val` at L18 must also come before the CAS at L19, which the dependency on `nx` and the order of the CAS give on common hardware. On x86 a locked CAS is a full fence, so only the compiler must keep the order.

## Example

**The tail lag and helping.** The queue is empty. Process $p$ enqueues 1 and stops after its CAS at L7, before L9. Then $q$ enqueues 2 and dequeues twice.

| step | process | line | action | state after it |
|---|---|---|---|---|
| 1 | $p$ | L1 to L7 | link node $A$ (val 1) after the dummy $D$ | $D \to A$, `Head` $= D$, `Tail` $= D$ |
| 2 | $q$ | L3 to L6 | `Tail` $= D$, $D.next = A$, not NULL | |
| 3 | $q$ | L8 | CAS(`Tail`, $D$, $A$): help $p$ | `Tail` $= A$ |
| 4 | $q$ | L3 to L7 | link node $B$ (val 2) after $A$ | $D \to A \to B$, `Tail` $= A$ |
| 5 | $q$ | L9 | CAS(`Tail`, $A$, $B$) | `Tail` $= B$ |
| 6 | $q$ | L11 to L19 | deq: $h = D$, $t = B$, CAS(`Head`, $D$, $A$) | returns 1, $A$ is the dummy |
| 7 | $q$ | L11 to L19 | deq: $h = A$, $t = B$, CAS(`Head`, $A$, $B$) | returns 2, $B$ is the dummy |

The results are enq(1), enq(2), deq() = 1, deq() = 2, as in a sequential queue. $p$ is still stopped before its L9; when it runs again, its CAS(`Tail`, $D$, $A$) fails, which is harmless.

**Without helping.** Remove L8 and L17 and repeat the run. At step 2, $q$ sees $D.next = A$, cannot link after $D$, and does not move `Tail`. It reads `Tail` again and gets $D$ again, forever. In the simulation, $q$ takes 2000 steps and completes nothing. One stopped process blocks all enqueues and all dequeues, so the queue is no longer lock-free.

**Without the test at L15.** Remove the test $h = t$. In the run above, after step 1, a dequeue reads $h = D$, $t = D$ and $nx = A$, and moves `Head` to $A$ while `Tail` still points to $D$. Now `Tail` points to a node that is no longer in the list, which breaks (Q2). If $D$ is then freed, `Tail` points to freed memory, and the next enqueue reads it at L4.

## Correctness

The invariants (Q1) to (Q3) hold after each step. The CAS at L7 succeeds only on the last node, so the list only grows at the end; the CAS at L8, L9 and L17 moves `Tail` only from a node to its successor; and the test at L15 with the help at L17 makes sure that `Head` moves only when `Head` and `Tail` differ, so `Head` never passes `Tail`. With these invariants, each successful CAS at L7 appends exactly one item, each successful CAS at L19 removes exactly the front item, and the read at L13 that a dequeue uses to return EMPTY sees an empty list. The full proof is in the proof file below.

## Complexity

| operation | alone | under contention, one operation | amortized |
|---|---|---|---|
| enqueue | 6 steps (1 allocation, 3 reads, 2 CAS) | unbounded | $O(k)$ |
| dequeue | 6 steps (4 when empty) | unbounded | $O(k)$ |

The space is one node per item plus the dummy. The amortized bound $O(k)$ for each operation follows as for the [Treiber stack](/treiber-stack/): a loop iteration fails only when some other operation made progress in it (a successful CAS on `next`, `Head` or `Tail`), and each operation makes $O(1)$ successful CASes. This bound is shown here and not in the paper; the paper proves lock-freedom.

**Not wait-free.** A dequeue can fail its CAS at L19 each time if other dequeues always win. [Kogan and Petrank](/kogan-petrank-queue/) (2011) built a wait-free queue on the same list by adding helping of whole operations.

## Variants

- **[Two-lock queue](/two-lock-queue/).** The blocking queue of the same paper, described above. It is simpler and fast at low contention.
- **[Kogan-Petrank queue](/kogan-petrank-queue/).** A wait-free queue on the same list: each operation first publishes itself in a state array, and the others finish it.
- **Optimistic queue.** Ladan-Mozes and Shavit (2004) use a doubly linked list so that an enqueue needs only one CAS.
- **Baskets queue and [LCRQ](/lcrq/).** Later queues cut contention: LCRQ uses fetch-and-add on ring buffers in place of CAS on the list ends.
- **Bounded rings.** For a fixed capacity, an array queue such as the [Vyukov bounded MPMC queue](/vyukov-bounded-mpmc-queue/) avoids allocation.

## When to use it

Use it when you need an unbounded FIFO queue shared by many threads with no lock, for example a task queue in a runtime that must not stall when a thread is descheduled. In Java, use `ConcurrentLinkedQueue`, which follows this design. In C or C++, plan the memory reclamation first. At high contention, `Head` and `Tail` are two hot spots, and a queue based on fetch-and-add or a bounded ring can be much faster. With a single producer and a single consumer, a [Lamport ring buffer](/lamport-spsc-queue/) needs no CAS at all.

## Pitfalls

- **Reading the value after the CAS.** After a successful CAS at L19, another dequeue can remove and free $nx$. Read $nx.val$ first.
- **Skipping the check at L5 or L14.** Without them, $t$ and $nx$ (or $h$ and $nx$) may come from different moments, and the code acts on a stale pair.
- **Dropping the helping CAS.** Without L8 and L17, one stopped enqueuer blocks everyone, as the example shows.
- **Dropping the test $h = t$.** Then `Head` can pass `Tail`, and with reuse an enqueue links a node into freed memory.
- **Freeing the old dummy at once.** Other processes may still read it. Use counted pointers with a free list, hazard pointers, or epochs.

## Implementations

## History

Michael and Scott (1996) gave the queue and the two-lock queue in one paper, with linearization points, a liveness argument and measurements, and compared them with earlier non-blocking queues, which were complex or needed a double CAS. Their counted pointers deal with ABA. Michael (2004) later showed the queue with hazard pointers. The algorithm is the standard lock-free queue in textbooks and in the Java library, and it is the base of wait-free queues such as the one of [Kogan and Petrank](/kogan-petrank-queue/).

## References
