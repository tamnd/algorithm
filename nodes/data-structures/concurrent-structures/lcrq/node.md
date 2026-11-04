---
tag: 83B4J8
kind: data-structure
slug: lcrq
name: LCRQ (linked concurrent ring queue)
aliases:
- linked concurrent ring queue
area: data-structures/concurrent-structures
level: research
summary: Queue built from linked fetch-and-add ring buffers, avoiding CAS retry loops on the hot ends.
prereqs: [michael-scott-queue, fetch-and-add, circular-buffer]
see_also: [concurrent-queue, disruptor-ring-buffer, vyukov-bounded-mpmc-queue, two-lock-queue, compare-and-swap, aba-problem, lock-freedom, linearizability]
sources:
  - paper: doi:10.1145/2442516.2442527
    title: Adam Morrison and Yehuda Afek, Fast concurrent queues for x86 processors, PPoPP 2013
    locator: pages 103 to 112, the CRQ with its cell states and the unsafe bit, the fix of the tail, the closing of a ring, the LCRQ list of rings, the proofs and the experiments
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: pages 267 to 275, the lock-free linked queue that the LCRQ uses to link its rings
---

The LCRQ is a lock-free, unbounded FIFO queue built from *concurrent ring queues* (CRQs). Each CRQ is a ring of $R$ cells with a head counter and a tail counter. An enqueue takes a ticket with one [fetch-and-add](/fetch-and-add/) on the tail and puts its item into cell $t \bmod R$; a dequeue takes a ticket with one fetch-and-add on the head and takes the item from the cell of its ticket. In a [compare-and-swap](/compare-and-swap/) (CAS) queue such as the [Michael-Scott queue](/michael-scott-queue/), all threads fight over the same word and most of their CASes fail and are retried. A fetch-and-add always succeeds, so under contention each thread gets its own cell in one step. When a ring becomes full, or an enqueue keeps failing, the ring is *closed*, and a new ring is linked after it, as in a Michael-Scott queue of rings. Morrison and Afek introduced the CRQ and the LCRQ in 2013.

## In plain words

At a bakery each customer pulls a numbered ticket, and each baker pulls a number from a second roll. The baker with number 7 serves the customer with ticket 7. Nobody has to push to the counter: pulling a ticket always works at once.

The counter has only $R$ places. Sometimes a baker arrives at a place before its customer, and then the baker leaves a mark so that the late customer goes for a new ticket. If the counter is full, or a customer keeps getting bad tickets, the shop closes the counter and opens a new one next to it.

## The abstract type

The LCRQ implements an unbounded FIFO queue:

- enqueue$(x)$ adds $x$ at the back.
- dequeue() removes and returns the item at the front, or returns EMPTY if the queue is empty.

Each operation is [linearizable](/linearizability/), and the queue is [lock-free](/lock-freedom/). Each single CRQ is a linearizable queue that can also answer CLOSED to an enqueue.

## Representation

A CRQ has:

- $head$, a counter changed by fetch-and-add.
- $tail$, a word with a counter $t$ and a *closed* bit, changed by fetch-and-add on $t$ and by test-and-set of the bit.
- $ring[0..R-1]$: each cell is one double-width word $(safe, idx, val)$, changed together by CAS2 (on x86, CMPXCHG16B). $val$ is an item or $\bot$, and $idx$ is the ticket the cell currently serves: it starts at $i$ for cell $i$ and grows by $R$ each round. $safe$ is 1, or 0 after a dequeuer found an item from an older round in the cell.
- $next$: a pointer to the next CRQ, or NIL.

The LCRQ has pointers $head$ and $tail$ to CRQs in a linked list, changed by CAS as in a Michael-Scott queue. Items are in the CRQs from the head of the list to its end.

## Operations

```pseudo id=main
CRQ-ENQUEUE(C, x)
L1  loop: (closed, t) ← FETCH-AND-ADD(C.tail, 1)
L2      if closed then return CLOSED
L3      (s, idx, val) ← READ(C.ring[t mod R])
L4      if val = ⊥ and idx ≤ t and (s = 1 or READ(C.head) ≤ t) then
L5          if CAS2(C.ring[t mod R], (s, idx, ⊥), (1, t, x)) then return OK
L6      if t − READ(C.head) ≥ R or this enqueue has failed too often then set C.tail.closed; return CLOSED

CRQ-DEQUEUE(C)
L7  loop: h ← FETCH-AND-ADD(C.head, 1)
L8      loop: (s, idx, val) ← READ(C.ring[h mod R])
L9          if idx > h then exit this inner loop                 ▷ a later round owns the cell
L10         if val ≠ ⊥ and idx = h then if CAS2(cell, (s, h, val), (s, h + R, ⊥)) then return val
L11         if val ≠ ⊥ and idx < h then if CAS2(cell, (s, idx, val), (0, idx, val)) then exit   ▷ mark unsafe
L12         if val = ⊥ then if CAS2(cell, (s, idx, ⊥), (s, h + R, ⊥)) then exit             ▷ kill ticket h
L13     t ← the counter of READ(C.tail)
L14     if t ≤ h + 1 then FIX-STATE(C); return EMPTY
FIX-STATE(C)
L15 loop: read tail, then head, then tail again; if tail changed, retry; if closed or head ≤ t then return; if CAS(C.tail, (open, t), (open, head)) then return

LCRQ-ENQUEUE(Q, x)
L16 loop: C ← READ(Q.tail); if C.next ≠ NIL then CAS(Q.tail, C, C.next); continue
L17     if CRQ-ENQUEUE(C, x) = OK then return
L18     N ← a new CRQ that holds x in cell 0, with tail 1; if CAS(C.next, NIL, N) then CAS(Q.tail, C, N); return

LCRQ-DEQUEUE(Q)
L19 loop: C ← READ(Q.head); v ← CRQ-DEQUEUE(C); if v ≠ EMPTY then return v
L20     if READ(C.next) = NIL then return EMPTY
L21     v ← CRQ-DEQUEUE(C); if v ≠ EMPTY then return v           ▷ C is closed; drain it once more
L22     CAS(Q.head, C, C.next)
```

**Tickets.** Enqueue ticket $t$ and dequeue ticket $t$ meet in cell $t \bmod R$. If the enqueue gets there first, it stores $(1, t, x)$, and dequeue $t$ takes $x$ and moves the cell on to round $t + R$. If the dequeue gets there first, it moves the cell on itself (line L12), so the late enqueue sees $idx > t$ and fails at line L4; it takes a new ticket.

**The unsafe bit.** A dequeue with ticket $h$ may find an item of an older round, with $idx < h$, whose own dequeuer is late. It cannot take it and cannot wait, so it clears $safe$ (line L11) and gives up its ticket. When the late dequeuer has taken the old item, the cell is empty with $idx = h$, but dequeue $h$ is gone. So an enqueue with ticket $h$ must not store into an unsafe cell unless $head \le h$, which means that dequeue $h$ has not started yet (line L4).

**Empty.** A dequeue whose ticket failed returns EMPTY only if the tail is at most $h + 1$, so every enqueue ticket handed out so far is below $h + 1$ and has a dequeue ticket. Dequeues that find the queue empty push $head$ past $tail$; FIX-STATE moves $tail$ up to $head$, so that later enqueues do not take tickets whose dequeuers have already given up.

**Closing.** When the ring is full ($t - head \ge R$) or an enqueue keeps losing its tickets, the enqueue closes the CRQ. Every later fetch-and-add on the tail returns the closed bit, so the CRQ takes no more items. The enqueue then links a new CRQ that already contains its item (line L18). A dequeue that finds a CRQ empty and sees a next CRQ drains it once more (line L21), since items may have arrived between its first look and the closing, and only then moves the head on.

## Example

Take $R = 2$. Enqueue $a$, $b$: tickets 0 and 1 fill cells 0 and 1 with $(1, 0, a)$ and $(1, 1, b)$. Enqueue $c$ gets ticket 2, finds $a$ still in cell 0, and since $2 - head = 2 \ge R$ it closes the ring and links a new CRQ holding $c$. Dequeues get tickets 0 and 1 and return $a$ and $b$. The next dequeue gets ticket 2, finds the cell of round 0 empty with $idx = 2$, kills ticket 2 and sees tail 3, so the first CRQ is empty; its $next$ is set, so after draining it again it moves $Q.head$ to the new CRQ and returns $c$.

Now a dequeue that overtakes an enqueue, with a fresh ring of 2 cells:

| step | thread | action | cell 0 | cell 1 | head | tail |
|---|---|---|---|---|---|---|
| 1 | $E$ | L1: ticket 0 | (1, 0, ⊥) | (1, 1, ⊥) | 0 | 1 |
| 2 | $D$ | L7: ticket 0 | (1, 0, ⊥) | (1, 1, ⊥) | 1 | 1 |
| 3 | $D$ | L12: kills ticket 0 | (1, 2, ⊥) | (1, 1, ⊥) | 1 | 1 |
| 4 | $D$ | L13, L14: tail 1 ≤ 0 + 1; returns EMPTY | (1, 2, ⊥) | (1, 1, ⊥) | 1 | 1 |
| 5 | $E$ | L3, L4: $idx = 2 > 0$, fails; L6: no close | (1, 2, ⊥) | (1, 1, ⊥) | 1 | 1 |
| 6 | $E$ | L1: ticket 1; L5: stores $x$ | (1, 2, ⊥) | (1, 1, $x$) | 1 | 2 |

A later dequeue gets ticket 1 and returns $x$. The enqueue of step 1 is linearized after the EMPTY of step 4, at its second ticket, which is consistent: it had not finished when $D$ answered.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). The key facts, for one CRQ:

- *Cells move forward.* Every CAS2 on a cell keeps or raises its $idx$, and none brings back an earlier state, so CAS2 has no [ABA problem](/aba-problem/).
- *Tickets match.* A value stored with ticket $t$ is taken only by dequeue ticket $t$. If enqueue ticket $t$ succeeds, dequeue ticket $t$, when it comes, takes its item; if dequeue ticket $t$ gave up, enqueue ticket $t$ cannot succeed afterwards. This is where the unsafe bit is needed.
- *Linearization.* A successful enqueue is linearized at the fetch-and-add of its successful ticket. A dequeue that returns the item of ticket $t$ is linearized at the latest of: its own fetch-and-add, the fetch-and-add of enqueue ticket $t$, and the point of the dequeue of the previous item. A dequeue that returns EMPTY is linearized at its read of the tail. Then enqueues and dequeues are both in ticket order, every item is dequeued after it was enqueued, and at an EMPTY point every enqueued item has been dequeued.
- *The list.* A closed CRQ takes no more items, a new CRQ is linked only after the old one is closed, and the head moves on only after a drain that saw the closed ring empty. So the queue is the concatenation of the CRQs in list order.
- *Progress.* Fetch-and-add never fails. An enqueue that keeps losing its tickets closes the ring after a bounded number of tries and links a new ring with one CAS, which fails only if another enqueue linked one. A dequeue that loses its ticket either returns EMPTY or sees that an enqueue took a later ticket. So the LCRQ is lock-free.

## Complexity

| quantity | value |
|---|---|
| enqueue or dequeue without contention | $O(1)$: one fetch-and-add, one read and one CAS2 |
| shared atomic steps that can fail, per operation | CAS2 on a cell, at most a few times per ticket; no retry loop on the head or tail |
| a new ring | $O(R)$ to allocate and initialise, once per $R$ items or per closing |
| space | $R$ cells per ring, for the rings from the head to the tail |

Morrison and Afek measured the LCRQ on x86 machines with up to 80 hardware threads against the Michael-Scott queue, flat-combining queues and others, and found it several times faster under high contention, close to the throughput of the fetch-and-add instruction itself. The gain comes from replacing CAS loops on the two hot words by fetch-and-add, which the hardware performs without failing.

## Variants

- **A single CRQ.** A bounded queue that can refuse enqueues with CLOSED; a [circular buffer](/circular-buffer/) for many producers and consumers.
- **Without CAS2.** Later queues, such as the LPRQ of Romanov and Koval (2023), replace the double-width CAS by single-word CAS, for machines that lack it.
- **Wait-free fetch-and-add queues.** Yang and Mellor-Crummey (2016) built a wait-free queue on the same idea of tickets in an infinite array, with a helping scheme for slow operations.
- **Bounded rings.** The [Vyukov bounded MPMC queue](/vyukov-bounded-mpmc-queue/) uses per-cell sequence numbers and CAS on the counters; the [Disruptor](/disruptor-ring-buffer/) uses sequence counters and lets consumers wait.
- **Locks.** A [two-lock queue](/two-lock-queue/) is simpler and good enough when few threads share the queue.

## When to use it

Use an LCRQ, or one of its successors, as a shared work queue on a machine with many cores and a fast fetch-and-add, when producers and consumers hammer both ends at once and plain FIFO order is needed, for example in a thread pool or a message-passing runtime. With few threads, a Michael-Scott queue or a lock is simpler. On hardware without a double-width CAS, use a variant without CAS2.

## Pitfalls

- **Dropping the unsafe bit.** Without it, an enqueue may store into a cell whose dequeuer has already given up, and its item is never dequeued.
- **Moving the head without draining again.** A dequeue that saw a CRQ empty and then a next ring must drain the CRQ once more before it moves the head, or an item that came between the two reads is lost.
- **Livelock without closing.** Dequeues that run ahead can kill the tickets of an enqueue for ever. The enqueue must close the ring after a bounded number of tries; the paper calls this the starvation check.
- **Garbage.** Old rings can only be freed when no thread still works on them. In languages without a garbage collector, use hazard pointers or epochs.
- **Counter overflow.** Tickets grow for ever; with 63-bit counters this takes centuries, but narrower counters overflow.

## Implementations

The Python module models each cell as one shared word holding the triple, with a CAS that stands for CAS2, and the counters as words with fetch-and-add, test-and-set and CAS, all simulated with a lock; each access is one step of a generator. The ring size and the number of tries before closing are parameters, so the tests can use rings of one to three cells. The tests replay the example of the full ring, the dequeue that overtakes an enqueue and the cell that becomes unsafe, compare random sequential runs with a deque, check random interleavings of three threads with a linearizability search that includes a final drain, count that many of them closed a ring, and run producers and consumers under real threads.

## History

Michael and Scott published the lock-free linked queue in 1996, and it stayed the standard for years. Ring buffers indexed by fetch-and-add were known from earlier array queues, but needed locks or unbounded arrays to be correct under concurrency. Morrison and Afek combined fetch-and-add tickets with CAS2 on cells, closing and linking of rings, and the unsafe bit, in 2013. Later work by Yang and Mellor-Crummey, and by Romanov and Koval, extended the design to wait-freedom and to single-word CAS.

## References
