---
tag: 3ZSHF1
kind: problem
slug: bounded-buffer-problem
name: Bounded buffer problem
aliases:
- Producer-consumer problem
- bounded-buffer problem
- producer-consumer problem
- producers and consumers
area: concurrency/mutual-exclusion
level: intro
summary: Producers put items into a buffer of N slots and consumers take them out, with no overflow, no underflow and no deadlock. Solved with semaphores full, empty and mutex, or with a monitor.
history:
  year: 1965
  people: [Edsger W. Dijkstra, C. A. R. Hoare]
  note: Dijkstra solved the bounded buffer with semaphores in Cooperating Sequential Processes (EWD 123). Hoare gave a monitor solution in 1974.
prereqs: [semaphore, queue]
see_also: [semaphore, monitor, condition-variable, circular-buffer, queue, deadlock, sleeping-barber-problem, readers-writers-problem]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating Sequential Processes, EWD 123, 1965
    locator: Section 4.3, the bounded buffer, with a semaphore for the empty places, one for the filled places, and a binary semaphore for the buffer manipulation
  - paper: doi:10.1145/355620.361161
    title: C. A. R. Hoare, Monitors, an operating system structuring concept, Communications of the ACM 17(10), 1974, pages 549 to 557
    locator: the bounded buffer monitor, with the conditions nonempty and nonfull
  - paper: doi:10.1145/358818.358824
    title: Butler W. Lampson and David D. Redell, Experience with processes and monitors in Mesa, Communications of the ACM 23(2), 1980, pages 105 to 117
    locator: the section on condition variables, where a NOTIFY is only a hint and a woken process must test its condition again in a loop
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 2, the section on interprocess communication, the producer-consumer problem with sleep and wakeup, with semaphores and with monitors
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, version 2.2
    locator: Chapter 4, the section Producer-consumer problem, with the subsection on the finite buffer
---

In the bounded buffer problem, also called the producer-consumer problem, producers make items and put them into a shared buffer with room for $N$ items, and consumers take items out. A producer must wait while the buffer is full, a consumer must wait while it is empty, and two processes must not change the buffer at the same time. Dijkstra solved it in 1965 with three [semaphores](/semaphore/), and it is the standard example of semaphores that count resources, of the [deadlock](/deadlock/) that one wrong order of P operations causes, and of [monitors](/monitor/) with [condition variables](/condition-variable/).

## In plain words

A baker puts loaves on a shelf that holds ten loaves, and customers take them away. When the shelf is full, the baker must wait. When the shelf is empty, a customer must wait. And two people must not grab at the same place on the shelf at the same time.

The classic fix uses three counters that make people wait: one counts the free places, one counts the loaves, and one lets only one person at a time touch the shelf. Each person first waits for a place or a loaf, and only then for the shelf.

If the baker takes the shelf first and then waits for a free place, everyone is stuck: the baker holds the shelf while it waits, and the customers who would free a place cannot reach the shelf.

## Definition

The model has $n$ asynchronous processes in a sequentially consistent memory, each a producer or a consumer. A process may crash between steps, but the problem asks for nothing when a process crashes inside the buffer code. The shared objects are a buffer of $N$ slots, used as a [queue](/queue/) (usually a [circular buffer](/circular-buffer/) with an in index and an out index), and the synchronization objects of the solution: counting [semaphores](/semaphore/) with P and V, or a [mutex](/mutex/) and [condition variables](/condition-variable/), or sleep and wakeup.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes (producers and consumers) |
| $p, q$ | process names; $i, j$ index slots and items |
| $N$ | the capacity of the buffer, in items |
| $k$ | the contention: the number of processes that try to put or take at the same time |
| $m$ | the number of shared objects: the buffer, its two indices, and the semaphores or the monitor |

A producer runs: make an item, then put it. A consumer runs: take an item, then use it. A solution must have these properties.

- **No overflow** (safety): a producer never puts an item into a full buffer, so no item is overwritten.
- **No underflow** (safety): a consumer never takes from an empty buffer.
- **Exclusion on the buffer** (safety): two processes never change the same slot or index at the same time.
- **Order**: items come out in the order they went in (the buffer is a FIFO queue).
- **[Deadlock freedom](/deadlock-freedom/)** (progress): if some producer has an item and the buffer is not full, or some consumer waits and the buffer is not empty, then some put or take eventually happens.

## Variants

- **One producer and one consumer.** With a circular buffer, the producer writes only the in index and the slot at it, and the consumer only the out index and the slot at it. The two counting semaphores are enough, and the mutex can go.
- **An unbounded buffer.** With $N = \infty$ the producer never waits, and only the semaphore that counts the items is needed.
- **$N = 1$.** A one slot buffer is a handoff: producer and consumer take turns.
- **Message passing.** A channel with a bounded queue, such as a Go channel with a buffer or a Unix pipe, is a bounded buffer in the runtime or kernel.
- **[Sleeping barber](/sleeping-barber-problem/).** The waiting room is a bounded buffer of customers, with one consumer (the barber), and a customer who finds it full leaves instead of waiting.

## Examples

**The semaphore solution (Dijkstra).** Three semaphores: empty counts the free slots and starts at $N$, full counts the filled slots and starts at 0, and mutex protects the buffer and starts at 1. These are the textbook names; in EWD 123 Dijkstra calls them number of empty positions, number of queuing portions, and buffer manipulation.

```text
PRODUCER                         CONSUMER
loop                             loop
  make item                        P(full)
  P(empty)                         P(mutex)
  P(mutex)                           item := take from buffer
    put item into buffer           V(mutex)
  V(mutex)                         V(empty)
  V(full)                          use item
```

A producer first waits for a free slot and only then for the buffer; a consumer first waits for an item and only then for the buffer. The order of the two V operations does not matter.

**Swapping the two P operations deadlocks.** If the producer does P(mutex) before P(empty), then a producer that finds the buffer full blocks in P(empty) while it holds mutex. The consumer, which would free a slot, blocks in P(mutex). Each waits for the other: a cycle of two. The simulator finds this state with $N = 1$, one producer and one consumer, two items: the producer puts the first item, takes mutex for the second, and blocks on empty, and the consumer blocks on mutex. With the P operations in Dijkstra's order, a search over all interleavings finds no deadlock and no overflow or underflow, for every mix of one or two producers and one or two consumers, with $N = 1$ and $N = 2$ and two items per producer.

**Without the mutex.** With one producer and one consumer and a circular buffer, the search finds no error when the mutex is removed. With two producers it finds a schedule where both read the same in index and the second overwrites the first's item.

**The monitor solution.** A [monitor](/monitor/) holds the buffer, a count, and two conditions, notFull and notEmpty.

```text
PUT(item)                              TAKE()
lock m                                 lock m
while count = N: wait(notFull)         while count = 0: wait(notEmpty)
put item; count := count + 1           item := take; count := count - 1
signal(notEmpty)                       signal(notFull)
unlock m                               unlock m; return item
```

**If and while.** Hoare's 1974 bounded buffer tests each condition with if, which is correct under Hoare semantics, where a signal hands the monitor straight to the waiter, so the condition still holds when it runs. Under Mesa semantics (Lampson and Redell, and Java, POSIX threads and most libraries), a signal only makes the waiter ready, and another process can enter the monitor first. With if, the search finds this schedule with $N = 1$, one producer and two consumers: consumer $c_0$ finds the buffer empty and waits; the producer puts an item and signals; consumer $c_1$ enters before $c_0$ runs and takes the item; then $c_0$ goes on, does not test again, and takes from an empty buffer. With while, $c_0$ tests again and waits; the search finds no error under Mesa or Hoare semantics, and with if no error under Hoare semantics.

**Sleep and wakeup lose a wakeup.** Before semaphores, a common attempt (Tanenbaum's example) kept a shared count without a lock: a consumer that sees count = 0 calls sleep, and a producer that raises count to 1 calls wakeup(consumer); the producer sleeps when count = $N$ and the consumer wakes it when count drops to $N - 1$. A wakeup sent to a process that is not asleep is lost. The search finds the classic 10 step schedule with $N = 1$: the consumer reads count = 0; before it sleeps, the producer puts an item, raises count to 1 and sends a wakeup, which is lost; the producer then sees count = 1 = $N$ and sleeps, and the consumer sleeps too. Both sleep for ever with an item in the buffer. The search also finds a second error: a wakeup that the producer decided to send while the buffer held an item arrives after the consumer has emptied the buffer and gone to sleep again, and the consumer then takes from an empty buffer. Semaphores fix both, because a V on a semaphore that nobody waits on is kept in the count, not lost, and a P tests and waits in one atomic step.

## Known algorithms

| solution | primitives | per item | notes |
|---|---|---|---|
| Dijkstra's semaphores | 3 semaphores | 2 P and 2 V per put or take | correct; order of the P operations matters |
| one producer and one consumer | 2 semaphores | 1 P and 1 V | no mutex needed |
| monitor | 1 mutex, 2 conditions | 1 lock, 1 unlock, 1 signal, and waits | correct with while; with if only under Hoare semantics |
| sleep and wakeup | sleep, wakeup | | wrong: loses wakeups |
| lock free ring | atomic loads and stores, or compare and swap | $O(1)$ | single producer single consumer rings need only ordered loads and stores |

With one condition variable for both producers and consumers, a signal can wake a process of the wrong kind, and all can end up waiting; use two conditions, or broadcast.

## Bounds

**Theorem (safety of the semaphore solution).** In every reachable state, $0 \le$ (items in the buffer) $\le N$, and no take finds an empty buffer.

*Proof.* Let $a$ be the number of completed P(empty) operations and $b$ the number of completed V(empty) operations. The semaphore never goes negative, so $N - a + b \ge 0$. Each put follows its own P(empty), and each V(empty) follows its own take, so the number of items in the buffer, puts minus takes, is at most $a - b \le N$. In the same way, let $c$ be the number of completed V(full) and $d$ the number of completed P(full); then $c - d \ge 0$, each take follows its own P(full), and each V(full) follows its own put, so takes $\le d \le c \le$ puts. Under mutex, puts and takes do not overlap, so each take finds the item of an earlier put. $\square$

**Theorem (deadlock freedom).** With the P operations in Dijkstra's order, if each producer has items left and the consumers want as many items as the producers make, the system cannot reach a state where every process that has not finished is blocked.

*Proof.* A process holds mutex only between P(mutex) and V(mutex), where it does no P, so it never blocks while it holds mutex. Hence if all unfinished processes are blocked, nobody holds mutex, and each one is blocked in P(empty) or P(full), with no process between its first P and its last V. Then empty $+$ full $= N \ge 1$, and full is the number of items in the buffer. If empty $> 0$, no producer is blocked, so every producer has finished; the unfinished consumers want exactly the items still in the buffer, so if any consumer is unfinished then full $> 0$ and it is not blocked. If full $> 0$, no consumer is blocked, so every consumer has finished, but then every item made so far was taken and full $= 0$, which is impossible. So in every case all processes have finished, and none is blocked. $\square$

**Swapped P is a deadlock.** With P(mutex) first in the producer, the state "buffer full, a producer holds mutex and waits in P(empty), a consumer waits in P(mutex)" is reachable, and the wait for graph has the cycle producer $\to$ consumer $\to$ producer. All four [Coffman conditions](/coffman-conditions/) hold.

**Cost.** Each put or take does a constant number of synchronization operations, and at most one process works on the buffer at a time, so the buffer is a sequential bottleneck. Production and consumption overlap with each other and with buffer access.

## Reductions

- The semaphores empty and full are a split semaphore: their sum, plus the processes between a P on one and the matching V on the other, is always $N$.
- The [sleeping barber problem](/sleeping-barber-problem/) is a bounded buffer of customers with one consumer and producers who leave instead of waiting.
- A blocking queue in a library (Java's ArrayBlockingQueue, Python's queue.Queue with a maxsize) is the monitor solution packaged as a [queue](/queue/) type.
- The bounded buffer is the standard case for the choice between [semaphores](/semaphore/) and [monitors](/monitor/): Hoare's paper shows the monitor version, and the difference between if and while shows the difference between Hoare and Mesa semantics.

## Applications

- **Pipelines.** Unix pipes, stream processing stages and thread pools with a task queue connect a fast stage to a slow one with a bounded buffer, which also gives back pressure: a fast producer is slowed down.
- **Device drivers and kernels.** Keyboard and network buffers fill at interrupt time and empty in a process, often as single producer single consumer rings.
- **Logging and audio.** Real time code writes into a lock free ring that another thread drains.
- **Channels.** Buffered channels in Go and in other languages are bounded buffers.

### History

Dijkstra introduced semaphores in "Cooperating Sequential Processes" (EWD 123, 1965) and used them for the producer and consumer, first with an unbounded buffer and then, in Section 4.3, with a bounded one. Hoare's 1974 monitor paper gives the bounded buffer as a monitor with two conditions, under his semantics in which a signal passes control to the waiter at once. Lampson and Redell's 1980 account of monitors in Mesa made a notify only a hint, which is why code today tests a condition in a while loop. The sleep and wakeup version, with its lost wakeup, is a standard textbook illustration of why semaphores and monitors were needed.

### Exercises

1. Show that swapping the two V operations in the producer is harmless.
2. In the consumer, swap P(full) and P(mutex). Give a schedule that deadlocks.
3. Prove that with one producer and one consumer the mutex can go, if a slot is written before V(full) and read before V(empty).
4. Write the monitor solution with one condition variable and signal. Give a schedule in which all processes wait. Does broadcast fix it?
5. Add a wakeup waiting bit to the sleep and wakeup solution (a wakeup sent to a process that is awake is saved for its next sleep). Does it fix both errors that the simulator finds?

## References
