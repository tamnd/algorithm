---
tag: 63WNND
kind: data-structure
slug: lamport-spsc-queue
name: Lamport single-producer single-consumer queue
aliases:
- wait-free SPSC ring buffer
- Lamport queue
area: concurrency/lock-free-structures
level: advanced
summary: Wait-free bounded ring buffer for exactly one producer and one consumer, needing no CAS.
implements: [queue]
complexity:
  vars: {N: the capacity of the buffer}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [queue, circular-buffer, wait-freedom, linearizability]
see_also: [michael-scott-queue, vyukov-bounded-mpmc-queue, disruptor-ring-buffer, sequential-consistency, registers-have-consensus-number-one, consensus-number]
sources:
  - paper: doi:10.1145/69624.357207
    title: Leslie Lamport, Specifying concurrent program modules, ACM Transactions on Programming Languages and Systems 5(2), 1983
    locator: the bounded FIFO queue example in which the producer and the consumer act on the buffer at the same time with no lock
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, 2020
    locator: Chapter 3 (Concurrent objects), the wait-free single-enqueuer single-dequeuer queue and its linearization points
  - paper: doi:10.1145/1345206.1345215
    title: "John Giacomoni, Tipp Moseley and Manish Vachharajani, FastForward for efficient pipeline parallelism: a cache-optimized concurrent lock-free queue, PPoPP 2008"
    locator: the queue that marks empty slots with NULL and keeps the indices local
  - paper: "Nhat Minh Lê, Adrien Guatto, Albert Cohen and Antoniu Pop, Correct and efficient bounded FIFO queues, SBAC-PAD 2013"
    locator: the Lamport queue in C11 with relaxed, acquire and release accesses, and its proof
---

The Lamport queue is a bounded [queue](/queue/) for exactly two processes: one producer that only enqueues, and one consumer that only dequeues. It is a [circular buffer](/circular-buffer/) of $N$ slots with two counters, `tail` and `head`. Only the producer writes `tail`, and only the consumer writes `head`. Each operation reads both counters, touches one slot, and writes its own counter. It needs no lock and no read-modify-write step such as [compare-and-swap](/compare-and-swap/), and each operation ends in at most four steps, so it is [wait-free](/wait-freedom/). Leslie Lamport used it in 1983 as an example of a concurrent module that is correct with no mutual exclusion. On real hardware it is correct only with the right memory order: the item must be visible before the new `tail`.

## In plain words

Picture a round table with $N$ plates and two people. The cook puts food on the next empty plate and then moves his own marker forward. The eater takes food from the next full plate and then moves her own marker forward. Each person moves only their own marker and only looks at the other's.

The cook stops when all plates are full, and the eater stops when all plates are empty. They never touch the same plate at the same time, so they never need to take turns. The cook must put the food down before he moves his marker, or the eater may pick up an empty plate.

## The abstract type

The queue has enq$(x)$, which adds $x$ at the back or returns FULL if $N$ items are in the queue, and deq(), which removes and returns the front item or returns EMPTY. Only one process calls enq, and only one other process calls deq. The safety condition is [linearizability](/linearizability/) with respect to a bounded sequential FIFO queue. The progress condition is [wait-freedom](/wait-freedom/): each operation ends in a fixed number of its own steps.

Lamport's paper writes the operations so that they wait while the buffer is full or empty. The form here returns FULL or EMPTY at once, which is what makes it wait-free; a caller that must block can retry.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $N$ | the capacity, the number of slots |
| $p, q$ | the producer $p$ and the consumer $q$ |
| $i, j$ | indices of items; item $i$ lives in slot $i \bmod N$ |

There are two asynchronous processes that may crash. They use atomic reads and writes of single words only, with no read-modify-write steps. The proofs assume sequential consistency; the paragraph on weak memory gives the orders that real hardware needs. The counters grow without bound here; in practice a 64-bit counter does not wrap, or the code keeps indices modulo $2N$.

### Fields

- `buf[0..N-1]` holds the items.
- `tail` is the number of items that the producer has put in. Only $p$ writes it.
- `head` is the number of items that the consumer has taken out. Only $q$ writes it.

**Invariant.** $0 \le$ `tail` $-$ `head` $\le N$, and the items in the queue, front first, are `buf[head mod N]`, ..., `buf[(tail − 1) mod N]`.

## Operations

```pseudo id=main
ENQ(v)                         ▷ producer only
L1  t ← tail; h ← head
L2  if t − h = N then return FULL
L3  buf[t mod N] ← v
L4  tail ← t + 1               ▷ release: the item is visible first
L5  return OK

DEQ()                          ▷ consumer only
L6  h ← head; t ← tail         ▷ acquire on the read of tail
L7  if t = h then return EMPTY
L8  v ← buf[h mod N]
L9  head ← h + 1               ▷ release: the slot is free for the producer
L10 return v
```

**Why no CAS.** Each shared word has one writer. The producer reads `head` only to see if a slot is free, and `head` only grows, so a stale value is safe: it makes the producer see fewer free slots, never more. In the same way, a stale `tail` makes the consumer see fewer items. The producer writes slot $t \bmod N$ only when $t - h < N$, that is when the consumer has already moved past the item that used that slot before. So the two processes never touch the same slot at the same time.

**Linearization points.** An enq that returns OK takes effect at its write of `tail` at L4. A deq that returns an item takes effect at its write of `head` at L9. A FULL result takes effect at the read of `head` in L1, and an EMPTY result at the read of `tail` in L6. Reading the counter of the other process is enough, since the process owns its own counter, and nobody else can change it.

**FastForward.** Giacomoni, Moseley and Vachharajani (2008) remove the shared counters. An empty slot holds NULL. The producer keeps its index in a local variable, checks that the slot holds NULL, writes the item and moves its index; the consumer reads the slot, returns EMPTY on NULL, and else writes NULL back and moves its index. The two processes now share only the slots, so the counters no longer move between the caches of two cores on each operation. The cost is that NULL cannot be an item.

### Memory reclamation

The queue allocates nothing after it starts: the buffer has a fixed size, and items are copied in and out. So there is no node to free and no [ABA problem](/aba-problem/). This is one reason why bounded ring buffers are popular in systems code.

### Weak memory

Under sequential consistency the code is correct as it is. Real processors and compilers can reorder memory accesses, and two orders matter:

- **The item before `tail`.** The write at L3 must be visible before the write at L4. In C11 or C++11, make L4 a release store and the read of `tail` in L6 an acquire load. If the store of `tail` becomes visible first, the consumer sees a new item, reads the slot before the item is there, and returns garbage. The test `test_store_reorder_breaks_it` models this: with the two writes swapped, the explorer finds a run in which deq returns a value that nobody enqueued.
- **The read of the slot before `head`.** The read at L8 must be done before the write at L9 is visible, or the producer may overwrite the slot first. A release store at L9 with an acquire load of `head` in L1 gives this.

On x86 (TSO) the hardware keeps these orders, and only the compiler must be stopped; on ARM and POWER the release and acquire need fences or special instructions. Lê, Guatto, Cohen and Pop (2013) give the C11 version with the weakest orders that are still correct, with a proof.

## Example

$N = 2$. The producer runs enq(1), enq(2), enq(3), and the consumer runs deq(), deq() in this order.

| step | process | lines | action | head | tail | buf |
|---|---|---|---|---|---|---|
| 1 | $p$ | L1 to L4 | enq(1): $t = 0, h = 0$, write slot 0 | 0 | 1 | [1, −] |
| 2 | $p$ | L1 to L4 | enq(2): $t = 1$, write slot 1 | 0 | 2 | [1, 2] |
| 3 | $p$ | L1, L2 | enq(3): $t - h = 2 = N$, return FULL | 0 | 2 | [1, 2] |
| 4 | $q$ | L6 to L9 | deq(): $h = 0, t = 2$, read slot 0 | 1 | 2 | [1, 2] |
| 5 | $p$ | L1 to L4 | enq(3) again: $t = 2, h = 1$, write slot 0 | 1 | 3 | [3, 2] |
| 6 | $q$ | L6 to L9 | deq(): read slot 1 | 2 | 3 | [3, 2] |

The results are OK, OK, FULL, 1, OK, 2, and slot 0 now holds 3, the item with index 2. The consumer freed slot 0 at step 4 by moving `head`, and only then could the producer reuse it.

## Correctness

The invariant holds after each step: L4 raises `tail` only when `tail` $-$ `head` $< N$ held at L1, and `head` can only have grown since; L9 raises `head` only when `head` $<$ `tail` held at L6, and `tail` can only have grown since. A slot is written at L3 only for an index $t$ with $t - N <$ `head`, so the item that used the slot before has been taken. A slot is read at L8 only for an index $h <$ `tail`, so its item was written before. With the linearization points above, each operation acts on the queue that the counters describe at its point, which gives FIFO results. The proof file has the details.

## Complexity

| operation | steps, in every run |
|---|---|
| enq | 4 (2 reads, 2 writes), or 2 when it returns FULL |
| deq | 4 (3 reads, 1 write), or 2 when it returns EMPTY |
| FastForward enq, deq | 2 (1 read, 1 write), or 1 |

These are exact counts, proved by the code and checked in every interleaving of the tests. The space is $N$ slots and two counters. The main cost on real machines is not the step count but cache traffic: each operation reads the counter of the other side, so the line that holds it moves between cores. Implementations keep a local copy of the other counter and read the shared one only when the copy says the queue is full or empty, and they put the two counters on different cache lines.

## Variants

- **FastForward.** NULL marks an empty slot, so the indices are local, as above.
- **Cached indices.** Each side keeps a stale copy of the other counter, which is safe for the reasons given above, and refreshes it only when needed. MCRingBuffer and B-Queue use this idea with batches.
- **Unbounded SPSC queues.** A linked list of ring buffers grows when one is full.
- **Many producers or many consumers.** One writer per counter is the key. With several producers, the counter needs a read-modify-write step, as in the [Vyukov bounded MPMC queue](/vyukov-bounded-mpmc-queue/) or the [Michael-Scott queue](/michael-scott-queue/). The [Disruptor ring buffer](/disruptor-ring-buffer/) uses sequence counters in a similar way.

## When to use it

Use it when exactly one thread sends data to exactly one other thread: pipeline stages, a thread that hands work to an I/O thread, audio and real-time code that must never block, or a channel between an interrupt handler and the main loop. It is the fastest queue for this case. Do not use it with more than one producer or more than one consumer; the test `test_two_producers_break_it` shows that two producers lose an item.

## Pitfalls

- **Two producers or two consumers.** Two producers read the same `tail` and write the same slot. The queue has no defense against this.
- **Missing release and acquire.** On ARM, POWER or with an optimizing compiler, the plain code can publish `tail` before the item.
- **Counters on one cache line.** Then every operation causes cache traffic for both sides (false sharing), and the queue is much slower than it needs to be.
- **Using `tail` = `head` for both full and empty with indices modulo $N$.** Then a full and an empty buffer look the same. Use unbounded counters, indices modulo $2N$, or leave one slot unused.

## Implementations

## History

Lamport (1983) gave this queue in a paper on how to specify concurrent modules, as an example of two processes that share data with no mutual exclusion. The textbook of Herlihy and Shavit uses it as an early example of a wait-free object and of linearization points. A queue with one enqueuer and one dequeuer can be built from registers alone, because the roles are fixed; a queue shared by any two processes has [consensus number](/consensus-number/) 2, and so it cannot be built from [registers](/registers-have-consensus-number-one/). FastForward (2008) and later cache-aware designs made the queue fast on multicore machines, and Lê, Guatto, Cohen and Pop (2013) proved a version for the C11 memory model.

## References
