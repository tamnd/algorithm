---
tag: GNF11S
kind: problem
slug: readers-writers-problem
name: Readers-writers problem
aliases:
- readers-writers
- readers and writers problem
- first readers-writers problem
- second readers-writers problem
area: concurrency/mutual-exclusion
level: intro
summary: Readers may share data, but a writer needs it alone. Readers priority starves writers, writers priority starves readers, and a FIFO turnstile starves neither.
history:
  year: 1971
  people: [P. J. Courtois, F. Heymans, D. L. Parnas]
  note: Courtois, Heymans and Parnas stated two problems, readers priority and writers priority, and solved each with semaphores. Fair solutions came later.
prereqs: [semaphore]
see_also: [readers-writer-lock, semaphore, starvation, starvation-freedom, mutex, monitor, bounded-buffer-problem, fairness]
sources:
  - paper: doi:10.1145/362759.362813
    title: P. J. Courtois, F. Heymans and D. L. Parnas, Concurrent control with "readers" and "writers", Communications of the ACM 14(10), 1971, pages 667 to 668
    locator: Problem 1 with its solution in Figure 1 (readcount, mutex and w), and Problem 2 with its solution in Figure 2 (readcount, writecount, mutex 1, mutex 2, mutex 3, w and r)
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, version 2.2
    locator: Chapter 4, the section Readers-writers problem, with the subsections on the lightswitch, starvation, the no-starve readers-writers solution (the turnstile) and writer-priority readers-writers
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 7, Synchronization Examples, the section on the readers-writers problem (the first and second readers-writers problems)
  - book: isbn:9780123705914
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, first edition (2008)
    locator: Chapter 8, Monitors and Blocking Synchronization, the section on readers-writers locks
---

In the readers-writers problem, many processes share one data object. Readers only look at it, so any number of them may use it at the same time; a writer changes it, so it must use it alone. The task is an entry and an exit protocol for each kind of process that keeps this exclusion and lets readers overlap. Courtois, Heymans and Parnas posed it in 1971 in two forms, one that favours readers and one that favours writers, and showed that each favoured class can starve the other. A fair solution, which starves neither class, needs a fair [semaphore](/semaphore/).

## In plain words

Think of a notice board. Many people can read it at the same time. But a person who wants to change a notice must be alone at the board, so nobody reads half of an old notice and half of a new one.

The question is who goes first when both are waiting. If readers always go first, a steady stream of readers can keep a writer out for ever. If writers always go first, a steady stream of writers can keep the readers out for ever.

The fair fix is a door that everyone passes in the order they arrive. When a writer is at the door, new readers queue behind it. The readers already inside finish, then the writer goes in.

## Definition

The model has $n$ asynchronous processes in a sequentially consistent memory, each of them a reader or a writer, that share one data object. A process may crash between steps, but not while it is inside a protocol or uses the object; the problem says nothing about crashes there. The protocols use counting [semaphores](/semaphore/) with P and V and ordinary shared integers that are read and written under a semaphore. A semaphore is weak if a V wakes any one of the blocked processes, and FIFO (strong) if it wakes the one that has waited longest.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $r_i$ is a reader and $w_j$ a writer, with indices $i, j$ |
| $k$ | the contention: the number of processes in an entry protocol or using the object |
| $m$ | the number of shared objects: one data object, plus the semaphores and counters of the protocol |

Each process runs, again and again, an entry protocol, a read or a write, and an exit protocol. A solution has these properties.

- **Exclusion** (safety): a writer never uses the object together with another writer or with a reader.
- **Concurrent reading**: readers do not exclude each other. Without this the problem is the [mutual exclusion problem](/mutual-exclusion-problem/).
- **[Deadlock freedom](/deadlock-freedom/)** (progress): if a process is in an entry protocol, then some process eventually uses the object.
- **[Starvation freedom](/starvation-freedom/)** for a class: every reader (or every writer) in its entry protocol eventually uses the object.

The two problems of Courtois, Heymans and Parnas add a priority rule.

- **Problem 1 (readers priority).** No reader waits unless a writer has already got permission to use the object. In particular, no reader waits only because a writer is waiting.
- **Problem 2 (writers priority).** Once a writer is ready to write, it writes as soon as possible: a reader that arrives after a writer is waiting does not get in before it.

## Variants

- **The first readers-writers problem** is Problem 1, and **the second readers-writers problem** is Problem 2; these are the textbook names (for example in Silberschatz, Galvin and Gagne).
- **The third readers-writers problem** asks that neither class starve. Solutions serve processes roughly in order of arrival, so readers that arrive together still overlap.
- **A lock object.** As a reusable object with shared and exclusive modes, the problem becomes the [readers-writer lock](/readers-writer-lock/), with policies such as reader preference, writer preference, task fair and phase fair.
- **Upgrades.** A reader that wants to become a writer while it reads. Two readers that both try to upgrade deadlock, so most locks do not allow it.
- **Other primitives.** The same policies can be written with a [monitor](/monitor/) and [condition variables](/condition-variable/), with spinning on atomic words, or with versions of the data (as in [read-copy-update](/read-copy-update/)) so that readers never block.

## Examples

**Problem 1 (Courtois, Heymans and Parnas, Figure 1).** The semaphores mutex and w both start at 1, and readcount at 0. mutex protects readcount, and w is held by the writer, or by the readers as a group.

```text
READER                                  WRITER
P(mutex)                                P(w)
readcount := readcount + 1              ... writing is performed ...
if readcount = 1 then P(w)              V(w)
V(mutex)
... reading is performed ...
P(mutex)
readcount := readcount - 1
if readcount = 0 then V(w)
V(mutex)
```

The first reader in takes w for all readers, and the last reader out gives it back. While the first reader waits in P(w) it holds mutex, so the other readers queue on mutex. When a writer does V(w), either the waiting reader or a waiting writer can go on; the paper leaves this choice to the semaphore.

**Writers starve under Problem 1.** Two readers $r_0$ and $r_1$ take turns: $r_1$ starts to read while $r_0$ reads, then $r_0$ leaves and comes back while $r_1$ reads, and so on. readcount never drops to 0, so w is never released, and a writer blocked in P(w) waits for ever. The test runs this schedule for 61 reads; the writer is never enabled and never writes. Each reader is fair, and each one leaves after each read; the writer starves only because the readers overlap.

**Problem 2 (Courtois, Heymans and Parnas, Figure 2).** The semaphores mutex 1, mutex 2, mutex 3, w and r all start at 1, and readcount and writecount at 0.

```text
READER                                  WRITER
P(mutex 3)                              P(mutex 2)
  P(r)                                    writecount := writecount + 1
    P(mutex 1)                            if writecount = 1 then P(r)
      readcount := readcount + 1        V(mutex 2)
      if readcount = 1 then P(w)        P(w)
    V(mutex 1)                          ... writing is performed ...
  V(r)                                  V(w)
V(mutex 3)                              P(mutex 2)
... reading is performed ...              writecount := writecount - 1
P(mutex 1)                                if writecount = 0 then V(r)
  readcount := readcount - 1            V(mutex 2)
  if readcount = 0 then V(w)
V(mutex 1)
```

The first writer that arrives takes r, and the last writer to leave gives it back, so while any writer is waiting or writing, no new reader can pass P(r). mutex 3 lets at most one reader wait on r at a time. Without it, many readers could queue on r, and a writer's P(r) would compete with all of them; with it, the writer competes with at most one reader.

**Readers starve under Problem 2.** Two writers overlap: $w_1$ registers (writecount becomes 2) while $w_0$ writes; $w_0$ finishes and registers again before $w_1$ is done. writecount never drops to 0, so r is never released, and a reader blocked in P(r) waits for ever. The test runs 16 writes this way and the reader never reads.

**A fair solution (the third problem).** Downey's no-starve solution adds a turnstile that every process passes. The semaphores turnstile, roomEmpty and mutex start at 1.

```text
READER                                  WRITER
P(turnstile)                            P(turnstile)
V(turnstile)                            P(roomEmpty)
P(mutex)                                ... writing is performed ...
readcount := readcount + 1              V(turnstile)
if readcount = 1 then P(roomEmpty)      V(roomEmpty)
V(mutex)
... reading is performed ...
P(mutex)
readcount := readcount - 1
if readcount = 0 then V(roomEmpty)
V(mutex)
```

The readers part (mutex, readcount and roomEmpty) is the same light switch as in Problem 1. A writer holds the turnstile while it waits for the room to empty and while it writes, so readers that arrive after it stop at the turnstile.

**The fairness rests on the turnstile.** If the turnstile is a FIFO semaphore, a writer that has done P(turnstile) is served after at most one read by each reader: each reader passes the turnstile at most once more before the writer, and every later P(turnstile) of a reader queues behind the writer. The test checks this bound over all interleavings with two readers. If the turnstile is weak, the writer can still starve: while $r_0$ reads, $r_1$ passes the turnstile, and while $r_1$ reads, $r_0$ passes it, again and again. The writer's P(turnstile) is enabled only at the moments when no reader is inside the turnstile, so a scheduler that is weakly fair (it must run a process that stays enabled) never has to run it. The test runs 30 such cycles: the writer is disabled at some point in each one and never writes.

**What the tests check.** For each of the three solutions, a search over all interleavings with two readers and one writer, and with one reader and two writers, two rounds each, finds no state that breaks exclusion and no deadlock. Seeded random runs with three readers and two writers, three rounds each, end with every read and write done.

## Known algorithms

| solution | semaphores | readers starve | writers starve | needs FIFO semaphores |
|---|---|---|---|---|
| Problem 1 (Courtois, Heymans and Parnas) | 2 | no | yes | no |
| Problem 2 (Courtois, Heymans and Parnas) | 5 | yes | no | no |
| turnstile (Downey's no-starve solution) | 3 | no | no | yes, for the turnstile |

- **Problem 1** costs a reader at most 3 P and 3 V operations per access, and a writer one P and one V.
- **Problem 2** costs a reader at most 5 P and 5 V operations, and a writer at most 4 P and 4 V.
- **The turnstile** costs a reader at most 4 P and 4 V operations, and a writer 2 P and 2 V.
- **Monitor solutions.** A [monitor](/monitor/) keeps counts of active and waiting readers and writers, and two [condition variables](/condition-variable/), okToRead and okToWrite. Hoare's 1974 monitor paper has a readers and writers example in this style. The policy is in the conditions on which a process waits, so it is easy to change.
- **Readers-writer locks.** Libraries package the protocol as a [readers-writer lock](/readers-writer-lock/), for example POSIX pthread_rwlock and Java ReentrantReadWriteLock, often with a fair mode. Queue locks with local spinning (Mellor-Crummey and Scott) and phase fair locks (Brandenburg and Anderson) are described on that page.

## Bounds

**Priority forces starvation.** Any solution of Problem 1 can starve a writer. Take two readers that read in overlapping turns, as in the example. Each time a reader arrives, some reader is reading and no writer has permission, so by the rule of Problem 1 the reader must not wait; hence at every moment some reader reads, and by exclusion no writer ever writes. In the same way any solution of Problem 2 can starve a reader, under two writers with overlapping turns. So starvation freedom for both classes needs a weaker priority rule, such as order of arrival.

**Bounded bypass with a FIFO turnstile.** In the turnstile solution with a FIFO turnstile and $r$ readers, once a writer has done P(turnstile), at most $r$ reads start before its write. This is the bound the test checks for $r = 2$.

**Concurrency.** With order of arrival, readers that arrive between two writers overlap, but a reader that arrives after a waiting writer must wait for that writer even when the object is in shared use. No solution can both let every such reader in at once (which is Problem 1) and stop writers from starving (by the argument above).

## Reductions

- With only writers, the problem is the [mutual exclusion problem](/mutual-exclusion-problem/), and each solution above reduces to a [mutex](/mutex/) (w, or roomEmpty) around the [critical section](/critical-section/).
- The light switch, a counter under a mutex in which the first one in locks a semaphore and the last one out unlocks it, appears in all three solutions, and in many other semaphore programs.
- Database [two-phase locking](/two-phase-locking/) uses shared locks for reads and exclusive locks for writes on each item, which is the readers-writers problem per item, with transactions as processes.

## Applications

- **Shared caches and tables** that are read often and written rarely, such as routing tables, configuration and symbol tables, use a [readers-writer lock](/readers-writer-lock/).
- **File and record locks**, such as shared and exclusive locks on files, are the same protocol.
- **Databases** use shared and exclusive locks in [concurrency control](/concurrency-control/); [multiversion concurrency control](/multiversion-concurrency-control/) avoids the conflict between readers and writers by keeping old versions.
- **Teaching.** The problem is a standard example of [starvation](/starvation/) and of how a priority rule decides who starves.

### History

Courtois, Heymans and Parnas published "Concurrent control with readers and writers" in the Communications of the ACM in October 1971. They gave Problem 1 and Problem 2 with semaphore solutions, and noted that each solution can starve the class it does not favour. Hoare used readers and writers as a monitor example in 1974. Solutions that starve neither class, often called the third readers-writers problem, appear in later textbooks; Downey's turnstile solution is one of them. Later work turned the problem into the readers-writer lock and studied scalable and real time versions.

### Exercises

1. In Problem 1, a writer does V(w) while one reader waits in P(w) and another writer also waits in P(w). Which one goes on, and what does the answer depend on? Does the rule of Problem 1 hold for the readers that wait on mutex at that moment?
2. Remove mutex 3 from Problem 2. Give a schedule in which a writer waits on r while several readers pass it.
3. Show that the turnstile solution with a weak turnstile is starvation free under strong fairness (a process that is enabled infinitely often eventually takes a step).
4. Write a [monitor](/monitor/) solution with the conditions okToRead and okToWrite that serves readers and writers in alternating batches. Prove that it is starvation free.
5. Two readers try to upgrade to writers while they read, using the turnstile solution. Show the deadlock.

## References
