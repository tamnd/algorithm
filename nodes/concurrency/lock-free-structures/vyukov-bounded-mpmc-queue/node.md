---
tag: 8Z65SA
kind: data-structure
slug: vyukov-bounded-mpmc-queue
name: Vyukov bounded MPMC queue
aliases:
- bounded MPMC queue
- Vyukov queue
- Vyukov MPMC ring buffer
area: concurrency/lock-free-structures
level: advanced
summary: Array-based bounded multi-producer multi-consumer queue using per-slot sequence numbers.
implements: [queue]
complexity:
  vars: {N: the capacity, n: the number of processes}
  space: {extra: Θ(N)}
properties: {persistent: false, concurrent: true, external: false}
prereqs: [queue, circular-buffer, compare-and-swap, linearizability, lock-freedom]
see_also: [lamport-spsc-queue, michael-scott-queue, disruptor-ring-buffer, lcrq, obstruction-freedom, kogan-petrank-queue]
sources:
  - url: https://www.1024cores.net/home/lock-free-algorithms/queues/bounded-mpmc-queue
    title: Dmitry Vyukov, Bounded MPMC queue, on the 1024cores web site
    locator: the C++ class mpmc_bounded_queue, with the per-cell sequence numbers and the enqueue and dequeue loops
  - paper: doi:10.1145/2442516.2442527
    title: Adam Morrison and Yehuda Afek, Fast concurrent queues for x86 processors, PPoPP 2013
    locator: the CRQ, a ring of cells with indices handed out by fetch-and-add, which is lock-free where this queue is not
  - url: https://lmax-exchange.github.io/disruptor/disruptor.html
    title: "Martin Thompson, Dave Farley, Michael Barker, Patricia Gee and Andrew Stewart, Disruptor: high performance alternative to bounded queues for exchanging data between concurrent threads, technical paper, 2011"
    locator: the ring buffer with sequence numbers that tell producers and consumers when a slot is ready
---

The Vyukov bounded MPMC queue is a bounded [queue](/queue/) on a [circular buffer](/circular-buffer/) for many producers and many consumers. Dmitry Vyukov published it as C++ code on his web site 1024cores. Each cell of the array has a *sequence number* that says whose turn it is: the producer of position $pos$ may fill the cell when its number is $pos$, and the consumer of $pos$ may empty it when its number is $pos + 1$. A producer claims a position with one [compare-and-swap](/compare-and-swap/) on a shared counter, writes the item, and then sets the number. The queue is fast, simple, and allocates nothing. It is not [lock-free](/lock-freedom/) as a FIFO queue: a producer that stops between its claim and its write of the number blocks every consumer behind its cell. Its try operations are [linearizable](/linearizability/) only if they may return FULL or EMPTY spuriously.

## In plain words

Think of a round table with numbered seats and a ticket machine for cooks and one for eaters. A cook takes the next cook ticket, and may put food on the seat only when the seat's card shows the cook's number. Then the cook turns the card to say "ready for eater number so-and-so". An eater takes the next eater ticket, waits for that card, takes the food, and turns the card to say "ready for the cook of the next round".

The tickets keep everyone in order, and nobody needs a lock. But if a cook takes a ticket and then falls asleep before putting the food down, the eater who holds the matching ticket waits for ever, and so does every eater after them.

## The abstract type

The queue has enq$(x)$, which adds $x$ at the back or returns FULL, and deq(), which removes and returns the front item or returns EMPTY. Any number of processes may call both. The safety condition proved here is [linearizability](/linearizability/) with respect to a *try queue*: a bounded FIFO queue of capacity $N$ in which enq may also return FULL, and deq may also return EMPTY, at any time, with no effect. With respect to a strict bounded queue, where EMPTY is allowed only when the queue has no item, the queue is not linearizable; the example shows a run. When each operation runs alone, the results are exact.

## Representation

### Model and notation

| Symbol | Meaning |
|---|---|
| $N$ | the capacity, the number of cells |
| $n$ | the number of processes |
| $p, q$ | process names |
| $pos$ | a position; position $pos$ uses cell $pos \bmod N$ |
| $i$ | a cell index |

The processes are asynchronous and may crash between any two steps. They use atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$). The proofs assume sequential consistency; the paragraph on weak memory gives the orders that the C++ code needs. Counters do not wrap here; the C++ code uses machine words, compares them by signed difference, and needs $N$ to be a power of two so that the cell index is a bit mask.

### Fields

- `cell[i]` has `seq` and `data`. At the start, `cell[i].seq` $= i$.
- `enqPos` is the next position for a producer, and `deqPos` is the next position for a consumer. Both start at 0.

**Invariant (the cell protocol).** For each position $pos$, the cell $pos \bmod N$ goes through three states in this order: `seq` $= pos$ (free for the producer of $pos$), `seq` $= pos + 1$ (full, for the consumer of $pos$), `seq` $= pos + N$ (free for the producer of $pos + N$). Also $0 \le$ `enqPos` $-$ `deqPos` $\le N$.

## Operations

```pseudo id=main
ENQ(v)
L1  pos ← enqPos
L2  loop
L3      s ← cell[pos mod N].seq          ▷ acquire
L4      d ← s − pos
L5      if d = 0 then                    ▷ the cell is free for position pos
L6          old ← CMPXCHG(enqPos, pos, pos + 1)
L7          if old = pos then break      ▷ claimed: linearization point
            pos ← old                    ▷ lost the race: try the new position
L8      else if d < 0 then return FULL   ▷ the cell still holds an older item
L9      else pos ← enqPos                ▷ pos is stale: read it again
L10 cell[pos mod N].data ← v
L11 cell[pos mod N].seq ← pos + 1        ▷ release: the item is ready

DEQ()
L12 pos ← deqPos
L13 loop
L14     s ← cell[pos mod N].seq          ▷ acquire
L15     d ← s − (pos + 1)
L16     if d = 0 then                    ▷ the cell holds the item of position pos
L17         old ← CMPXCHG(deqPos, pos, pos + 1)
L18         if old = pos then break      ▷ claimed: linearization point
            pos ← old
L19     else if d < 0 then return EMPTY  ▷ the item of pos is not there yet
L20     else pos ← deqPos
L21 v ← cell[pos mod N].data
L22 cell[pos mod N].seq ← pos + N        ▷ release: free for the next lap
    return v
```

CMPXCHG returns the old value of the word, and writes the new value if the old value was the expected one, like `compare_exchange_weak` in C++, which loads the current value on failure.

**Why each claim is safe.** A producer claims $pos$ only after it read `seq` $= pos$ in its cell. Only the consumer of $pos - N$ writes that value, after it has read its item, so the cell is free. Nobody else writes the cell until the claimer writes $pos + 1$ at L11. A consumer claims $pos$ only after it read `seq` $= pos + 1$, which the producer of $pos$ writes after the data, so the item is there. The CAS on the counter makes each claim unique.

**Linearization points.** An enq that returns OK takes effect at its successful CAS at L6, and a deq that returns an item at its successful CAS at L17. At any time, the abstract queue holds the items of positions `deqPos` to `enqPos` $- 1$, in order. FULL and EMPTY have no effect; the try queue allows them at any time.

**Why EMPTY can be wrong.** EMPTY comes from L19, when the cell at `deqPos` does not hold its item yet. That happens when the queue is empty, but also when the producer of that position has claimed it and not yet written `seq`. In that case later producers may already have finished, and their items are in the queue behind the slow one.

### Memory reclamation

Nothing is allocated after the start, and items are copied in and out, so there is no reclamation problem and no [ABA problem](/aba-problem/) on pointers. The counters grow by one on each claim, and a cell's number is compared with a full position, not with the cell index, so an old value is never mistaken for a new one until the counter wraps around a 64-bit word.

### Weak memory

The read of `seq` at L3 and L14 must be an acquire load, and the writes at L11 and L22 must be release stores. Then the consumer sees the data when it sees `seq` $= pos + 1$, and the producer of the next lap writes the data only after the consumer has read it. The counters `enqPos` and `deqPos` carry no data, so their loads and the CAS can be relaxed: a stale position only makes the loop try again. On x86, the plain C++ code compiles to ordinary moves for the loads and stores and to `lock cmpxchg` for the CAS.

## Example

**A stalled producer.** $N = 4$. Process $p$ calls enq(100), claims position 0 at L6, and stops before L10. Process $q$ then calls enq$(0)$, enq$(1)$, ..., enq$(9)$, and process $r$ calls deq() ten times.

| step | process | action | result |
|---|---|---|---|
| 1 | $p$ | L1 to L7: claims position 0, `enqPos` $= 1$ | stops |
| 2 | $q$ | enq$(0)$, enq$(1)$, enq$(2)$ claim positions 1, 2, 3 and finish | OK, OK, OK |
| 3 | $q$ | enq$(3)$: position 4 uses cell 0, whose `seq` is still 0 $< 4$ | FULL |
| 4 | $q$ | enq$(4)$ to enq$(9)$: the same | FULL each time |
| 5 | $r$ | deq(): cell 0 has `seq` $= 0 \ne 1$ | EMPTY, ten times |

Three items are in the queue, and the queue reports EMPTY to every consumer and FULL to every producer, for as long as $p$ sleeps. The history enq$(0)$ = OK, then deq() = EMPTY, with nothing else completed, is not linearizable for a strict queue. A consumer that loops until it gets an item spins for ever; in the test, it takes 2000 steps and returns nothing. When $p$ runs again, it writes its item and the number, and everything flows again.

So the queue is *blocking* in the sense of progress conditions: one stopped process can stop all useful work. Each try operation does return, and the try operations are lock-free with respect to the try queue, since a loop iteration that does not return means that another claim succeeded. But a try queue that may always say FULL and EMPTY is a weak object, and that is not the progress that users of a queue want.

## Correctness

The cell protocol holds by the argument above: each of the three values of `seq` for a position is written by exactly one process, after it has done its claim or its read, and each claim is a unique CAS on a counter. With the linearization points at the claims, the abstract queue is the range of positions from `deqPos` to `enqPos` $- 1$; an enq appends at the back, a deq takes the item of the front position, and `enqPos` $-$ `deqPos` $\le N$ because a producer can claim $pos$ only after the consumer of $pos - N$ has finished. The proof file gives the details, and also the proof that the try operations are lock-free.

## Complexity

| operation | alone | under contention, one operation |
|---|---|---|
| enq | 5 steps (2 when FULL) | unbounded |
| deq | 5 steps (2 when EMPTY) | unbounded |

The counts alone are measured and exact: one read of the counter, one read of `seq`, one CAS, one access to the data, one write of `seq`. Under contention, a loop iteration fails only when another claim on the same counter succeeds, so the number of failed iterations of all operations is at most the number of successful claims. The space is $N$ cells and two counters.

## Variants

- **[Lamport SPSC queue](/lamport-spsc-queue/).** With one producer and one consumer, no CAS is needed: each counter has one writer. The Lamport queue is wait-free; this queue trades that for many producers and consumers.
- **Blocking wrappers.** Most users retry on FULL and EMPTY, often with a spin, a yield, or a futex wait. This is fine if threads are not descheduled for long inside an operation.
- **Fetch-and-add on the counters.** Claiming with [fetch-and-add](/fetch-and-add/) never fails, but then a claim can land on a cell that is not ready, and the code must handle it. The CRQ ring of [LCRQ](/lcrq/) does this and is lock-free, at the cost of a more complex cell protocol and a double-width CAS.
- **[Disruptor ring buffer](/disruptor-ring-buffer/).** Uses sequence numbers in a similar way, with consumers that track their own positions and see every event.

## When to use it

Use it as a fast bounded queue between thread pools, for example to pass tasks or messages, when threads run on their own cores and are rarely stopped in the middle of an operation. It needs no allocation and no memory reclamation, and the code is short. Do not use it where a thread may be stopped or killed for a long time in the middle of an operation and the others must still make progress, or where a spurious EMPTY or FULL is a problem; then use the [Michael-Scott queue](/michael-scott-queue/) or a lock-free ring such as LCRQ.

## Pitfalls

- **Calling it lock-free.** As the example shows, one stalled producer makes all consumers see EMPTY. The code has no locks, but that is not the same as lock-freedom.
- **Treating EMPTY as "the queue is empty".** It can mean that the next item is not ready yet. Code that stops a worker on EMPTY may stop too early.
- **A capacity that is not a power of two** in the C++ code, where the index is `pos & mask`. In this page's implementation, `pos mod N` works for any $N$, since the counters do not wrap.
- **Comparing sequence numbers without a signed difference.** With machine words, `seq − pos` must be taken as a signed number, or a cell that is one lap behind looks ready.

## Implementations

## History

Vyukov posted the queue on his site 1024cores, with C++ code and notes on its use. It became a common bounded queue in systems code and in the libraries of several languages. The idea of a sequence number per slot also appears in the LMAX Disruptor (2011). Morrison and Afek (2013) built CRQ, a ring of cells with indices from fetch-and-add, and showed how to make such a ring lock-free by letting an operation give up on a cell that is not ready and close the ring when it gets stuck.

## References
