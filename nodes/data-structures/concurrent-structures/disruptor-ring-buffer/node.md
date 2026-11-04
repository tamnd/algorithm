---
tag: 1JS632
kind: data-structure
slug: disruptor-ring-buffer
name: Disruptor ring buffer
aliases:
- LMAX Disruptor
area: data-structures/concurrent-structures
level: advanced
summary: Pre-allocated ring buffer with sequence-number barriers for low-latency inter-thread message passing.
prereqs: [circular-buffer, concurrent-queue, fetch-and-add]
see_also: [lamport-spsc-queue, vyukov-bounded-mpmc-queue, lcrq, bounded-buffer-problem, backpressure, two-lock-queue, linearizability]
sources:
  - url: https://lmax-exchange.github.io/disruptor/files/Disruptor-1.0.pdf
    title: Martin Thompson, Dave Farley, Michael Barker, Patricia Gee and Andrew Stewart, Disruptor, high performance alternative to bounded queues for exchanging data between concurrent threads, technical paper, May 2011
    locator: Section 4.1 (Memory Allocation), 4.2 (Teasing Apart the Concerns), 4.3 (Sequencing), 4.4 (Batching Effect) and 4.5 (Dependency Graphs)
  - url: https://lmax-exchange.github.io/disruptor/
    title: LMAX Disruptor, project site and user guide
    locator: the user guide, the sections on the ring buffer, sequences, the sequencer and the sequence barrier
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 10 (Concurrent Queues and the ABA Problem), for the bounded queues that the Disruptor replaces
---

The Disruptor is a pre-allocated [ring buffer](/circular-buffer/) through which threads pass events, coordinated only by sequence numbers. A producer claims the next sequence number, writes the slot of that number, and publishes it by moving a *cursor*. Each consumer keeps its own sequence, the last event it has finished, and reads every event up to the cursor, in order, in batches. A consumer may also wait for other consumers, so one ring holds a whole graph of processing stages. A producer never overwrites a slot until the slowest consumer has finished it. With one producer, no lock and no read-modify-write instruction is needed. Thompson, Farley, Barker, Gee and Stewart built it at LMAX for a financial exchange and described it in 2011.

## In plain words

Think of a round table with eight plates and a cook who puts food on the plates one after another, round and round. Each plate has a number that keeps growing: 0, 1, 2, and after 7 the cook comes back to the first plate as plate 8. A board on the wall shows the last plate that is ready.

Several waiters each look at the board and take care of every plate up to that number, in order. One waiter may have to wait until another has finished a plate, for example the one who adds the sauce waits for the one who adds the rice. Each waiter writes on a card the last plate they have finished. The cook looks at the slowest card before reusing a plate.

Nobody locks anything. Each number is written by one person only, and the others just read it.

## The abstract type

The Disruptor is a bounded broadcast channel with a fixed set of consumers. Its sequential type holds the list $P$ of published events and a position $pos_c$ for each consumer $c$, the number of events $c$ has finished; consumer $c$ also has a set $deps_c$ of consumers it must stay behind.

- publish$(x)$ appends $x$ to $P$ and returns its sequence number $|P| - 1$. It is allowed only while $|P| - \min_c pos_c < N$, the ring size; otherwise it waits.
- consume$(c)$ returns a nonempty batch $P[pos_c .. a - 1]$ for some $a$ with $pos_c < a \le \min(|P|, \min_{d \in deps_c} pos_d)$, and sets $pos_c = a$. If no such $a$ exists, it waits.

Each consumer sees every event once and in order, and no consumer passes a consumer it depends on. Unlike a [concurrent queue](/concurrent-queue/), the consumers do not split the events between them: every consumer gets all of them. A work queue is built on top by letting each consumer handle only some of the events, for example those with $s \bmod k = c$.

## Representation

- $R.entry[0..N-1]$: the slots, allocated once. $N$ is a power of 2, so slot $s \bmod N$ is $s$ AND $(N - 1)$.
- $R.claim$: the next sequence number to hand out. With one producer it is a plain variable; with many it is changed by [fetch-and-add](/fetch-and-add/) or compare-and-swap.
- $R.cursor$: the largest published sequence number, initially $-1$.
- For each consumer $c$: $c.seq$, the largest sequence number it has finished, initially $-1$, and its dependencies $c.deps$.

Each sequence number is written by one thread only: the cursor by the producers in turn, $c.seq$ by consumer $c$. All sequences only grow.

**Invariant.** For each consumer $c$ and each $d \in c.deps$: $c.seq \le d.seq \le R.cursor$, and $R.cursor - c.seq \le N$. So the $N$ slots hold the events $R.cursor - N + 1, \ldots, R.cursor$, and every event that some consumer still needs is among them.

## Operations

```pseudo id=main
PUBLISH(R, x)
L1  s ← FETCH-AND-ADD(R.claim, 1)                   ▷ one producer: s ← R.claim; R.claim ← s + 1
L2  wait until s − N ≤ min over consumers c of c.seq   ▷ slot s mod N is free
L3  R.entry[s mod N] ← x
L4  wait until R.cursor = s − 1                     ▷ publish in sequence order
L5  R.cursor ← s                                     ▷ linearization point

CONSUME(R, c)
L6  next ← c.seq + 1
L7  wait until a ≥ next, where a ← min(R.cursor, min over d in c.deps of d.seq)
L8  batch ← R.entry[next mod N], ..., R.entry[a mod N]
L9  c.seq ← a                                        ▷ frees the slots for the producer
L10 return batch
```

**Claiming and gating.** Line L1 gives each producer its own sequence number. Line L2 is the gate: sequence $s$ reuses the slot of $s - N$, so the producer waits until every consumer has finished $s - N$. It is enough to gate on the consumers at the end of the dependency graph, because the others are ahead of them.

**Publishing.** Line L3 writes the slot, and line L5 makes it visible. With many producers, a producer that claimed $s$ waits at line L4 until all smaller numbers are published, so the cursor always means that every number up to it is ready. With one producer line L4 never waits.

**Consuming.** Line L7 reads the cursor and the sequences of the dependencies. If the cursor has moved ahead by many slots, the consumer takes all of them in one batch (lines L8 and L9), without any further synchronization: the *batching effect* of the paper, which lets a consumer that fell behind catch up quickly.

On real hardware the writes of lines L5 and L9 need release order and the reads of lines L2, L4 and L7 acquire order, so that a reader that sees a sequence number also sees the slot contents written before it.

## Example

Ring size $N = 4$, one producer $P$, consumer $A$, and consumer $B$ that depends on $A$ (for example, $A$ writes events to a journal and $B$ applies them only once they are journaled).

| step | thread | what it does | cursor | $A.seq$ | $B.seq$ | slots 0 to 3 |
|---|---|---|---|---|---|---|
| 1 | $P$ | publishes 10 as $s = 0$ | 0 | $-1$ | $-1$ | 10, -, -, - |
| 2 | $P$ | publishes 11 as $s = 1$ | 1 | $-1$ | $-1$ | 10, 11, -, - |
| 3 | $A$ | L7: $a = 1$; takes [10, 11] | 1 | 1 | $-1$ | 10, 11, -, - |
| 4 | $P$ | publishes 12 and 13 | 3 | 1 | $-1$ | 10, 11, 12, 13 |
| 5 | $P$ | claims $s = 4$; L2: $4 - 4 = 0 > \min(1, -1)$, waits | 3 | 1 | $-1$ | 10, 11, 12, 13 |
| 6 | $B$ | L7: $a = \min(3, A.seq = 1) = 1$; takes [10, 11] | 3 | 1 | 1 | 10, 11, 12, 13 |
| 7 | $P$ | L2 passes; L3: slot 0 gets 14; L5 | 4 | 1 | 1 | 14, 11, 12, 13 |
| 8 | $A$ | takes [12, 13, 14] | 4 | 4 | 1 | 14, 11, 12, 13 |
| 9 | $B$ | takes [12, 13, 14] | 4 | 4 | 4 | 14, 11, 12, 13 |

At step 5 the ring is full for the slowest consumer, so the producer waits; this is the [backpressure](/backpressure/) of a bounded buffer. At step 6, $B$ could see events up to 3 in the ring, but it stops at 1, where $A$ is. At step 8, $A$ takes three events in one batch.

## Correctness

Take the abstract list $P$ to be the events with sequence number at most $R.cursor$, and $pos_c = c.seq + 1$. Publishes are linearized at line L5, which, thanks to line L4, happens in sequence order, so each publish appends exactly its own event and returns $|P| - 1$. A consume is linearized at the read of line L7 that succeeds; the reads of different sequences need not be one atomic step, because all sequences only grow, so the value $a$ is at most the true minimum at the time of the last read. The gate of line L2 ensures that the slot of sequence $s$ is not overwritten until every consumer has finished $s$, so the batch read at line L8 is exactly $P[pos_c .. a]$. No call waits except at lines L2, L4 and L7, which are the full and empty conditions of the abstract type and, with many producers, the wait for a producer that claimed an earlier number. With one producer, every operation is wait-free whenever its abstract condition holds. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | steps | shared writes |
|---|---|---|
| publish, one producer | $O(1)$ plus the reads of the gate, $O(k)$ for $k$ gating consumers | the slot and the cursor |
| publish, many producers | the same plus one fetch-and-add and the wait for earlier producers | the claim, the slot and the cursor |
| consume a batch of $b$ events | $O(b + |deps|)$ | the consumer's own sequence |
| space | $N$ slots and one sequence per consumer, allocated once | |

The gain over a queue comes from the memory system, not from the step count. There is no lock, and with one producer no read-modify-write instruction. Each sequence number has one writer, so its cache line moves only from the writer to the readers. Slots are reused, so in a garbage-collected language no object is allocated per event. A producer can cache the minimum of the consumer sequences and read them again only when it reaches that bound. The paper reports, for its three-stage pipeline test, a mean latency hundreds of times lower than with Java's ArrayBlockingQueue between the stages.

## Variants

- **Wait strategies.** A thread that must wait at lines L2, L4 or L7 can spin, spin and then yield, or sleep on a lock and a condition variable. Spinning gives the lowest latency and costs a core.
- **Multi-producer sequencers.** Later versions of the library avoid the wait at line L4: each slot gets a flag with the round number of its last write, and a consumer reads the highest number such that all slots up to it are flagged.
- **Work pools.** Several workers share one sequence and claim events from it by compare-and-swap, so that each event goes to one worker.
- **[Lamport's single-producer single-consumer queue](/lamport-spsc-queue/).** The special case with one consumer and no dependencies, and the origin of the idea of a ring with one writer per index.
- **[Vyukov's bounded MPMC queue](/vyukov-bounded-mpmc-queue/).** A ring where each slot has its own sequence number, so many producers and many consumers split the events like a queue.

## When to use it

Use a Disruptor between a few threads with fixed roles when latency matters, when every stage must see every event, and when the stages form a fixed graph: order handling, logging pipelines, market data, journaling and replication before processing. Use an ordinary blocking queue when threads come and go, when consumers must share the work, or when the rate is low and simplicity matters more. Spinning wait strategies need a core per waiting thread.

## Pitfalls

- **A slow consumer stops the producer.** The ring is bounded, and the gate waits for the slowest gating consumer. A consumer that stops, stops the whole system.
- **Forgetting a consumer in the gate.** A consumer that is not gated on can have its slots overwritten while it reads them. Gate on every consumer at the end of the dependency graph.
- **Reading the slot after updating the sequence.** Line L9 must come after line L8 is done, including any copy of the event that the consumer keeps; otherwise the producer may overwrite the slot during the read.
- **A size that is not a power of 2.** The mask $N - 1$ works only for powers of 2; with another size, use the remainder, which is slower.
- **False sharing.** Sequence numbers of different threads on one cache line make every update slow down the other threads. The library pads each sequence to its own cache line.
- **Overflow of sequence numbers.** A 64-bit sequence is enough for centuries at any real rate, but a 32-bit one wraps.

## Implementations

The Python module models each sequence number as a word with atomic get, set and fetch-and-add, simulated with a lock, and the slots as a list. Each step of a generator is one access to shared memory, so the tests replay the example, show the gate and the in-order publishing of two producers, and check random interleavings of one or two producers and two consumers, with and without a dependency, against the sequential type above with a linearizability search. The plain methods also run under real threads.

## History

Lamport's single-producer single-consumer ring of 1983 already used one writer per index. Thompson, Farley, Barker, Gee and Stewart designed the Disruptor for the LMAX exchange, where queues between the stages of a transaction took most of the time, and published the technical paper in May 2011 together with an open-source Java library.

## References
