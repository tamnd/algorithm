---
tag: V66CR9
kind: technique
slug: lock-striping
name: Lock striping
aliases:
- lock splitting
area: data-structures/concurrent-structures
level: core
summary: Partition a structure into segments each guarded by its own lock, so operations on different stripes run in parallel.
prereqs: [mutex, critical-section, lock-ordering]
see_also: [concurrent-hash-table, two-lock-queue, sloppy-counter, readers-writer-lock, lock-coupling, deadlock]
sources:
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 13, Section 13.2.2 (A Striped Hash Set) and Section 13.2.3 (A Refinable Hash Set)
  - book: isbn:9780321349606
    title: Brian Goetz and others, Java Concurrency in Practice
    locator: Section 11.4 (Reducing lock contention), Sections 11.4.2 (lock splitting) and 11.4.3 (lock striping)
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: Section 2, the two-lock queue
---

Lock striping is a technique for shared data structures: split the data into $L$ disjoint parts, called stripes, give each stripe its own [mutex](/mutex/), and let each operation take only the locks of the stripes it touches. Operations on different stripes then run in parallel, while operations on the same stripe still take turns. An operation that must see the whole structure, such as a resize, takes all stripe locks in one fixed order. The [concurrent hash table](/concurrent-hash-table/) with $L$ locks for its buckets is the standard example; the [two-lock queue](/two-lock-queue/) is the case of two stripes, the two ends.

## In plain words

A shop with one cash desk makes everyone wait in one line. A shop with sixteen desks lets sixteen people pay at the same time. Each customer goes to the desk of their group, for example by the last digit of their ticket, so two people of different groups never wait for each other.

Lock striping does the same with a shared data structure. Instead of one lock for the whole structure, it uses several, and each lock guards a fixed part. An operation takes only the lock of the part it needs. If two operations need different parts, they run at the same time. If some operation needs everything, it takes every lock, always in the same order, so that two such operations can never wait for each other in a circle.

## When it applies

- **Most operations touch one small part.** A key picks one bucket, an index picks one cell, a thread updates its own counter.
- **The part can be computed before the lock is taken,** from the arguments alone, and does not change while the structure changes. In a hash table, the stripe of a key must not depend on the capacity.
- **The parts are independent for correctness.** An invariant that links two stripes, such as a total count that must always be exact, forces the operations that keep it to take more than one lock.
- **Contention is the bottleneck,** not the work inside the critical section. If each operation does a lot of work outside the lock, one lock is already enough.

Signs that it does not apply: most operations need the whole structure (an ordered scan, a global minimum), or a few keys get most of the traffic, so that the hot keys put most threads on one stripe anyway.

## The template

```pseudo id=main
STRIPED-OPERATION(S, args)
L1  i ← STRIPE(args)                  ▷ hole: a function of the arguments only, in 0 .. L − 1
L2  acquire(S.locks[i])
L3  r ← SEQUENTIAL-OPERATION(S.part(i), args)   ▷ hole: the sequential code on stripe i
L4  release(S.locks[i])
L5  return r

GLOBAL-OPERATION(S, args)
L6  for i ← 0 to L − 1 do acquire(S.locks[i])   ▷ the same order in every thread
L7  r ← WHOLE-OPERATION(S, args)                 ▷ hole: resize, exact size, snapshot
L8  for i ← 0 to L − 1 do release(S.locks[i])
L9  return r

MULTI-STRIPE-OPERATION(S, args)
L10 I ← the set of stripes of args, sorted increasingly
L11 for i in I do acquire(S.locks[i])
L12 r ← SEQUENTIAL-OPERATION on the stripes in I
L13 for i in I do release(S.locks[i])
L14 return r
```

The holes are the stripe function, the sequential code on one stripe, and the whole-structure operation. The rules that make the template correct are these.

1. **Stripe ownership.** Each piece of shared state belongs to exactly one stripe, and it is read or written only by a thread that holds that stripe's lock, or all locks.
2. **Stable stripe function.** STRIPE depends only on the arguments, and its value for a given element never changes. If the layout changes (a hash table doubles), it must keep each element in its stripe.
3. **One lock order.** Each thread that holds two or more stripe locks takes them in increasing index order. By the argument of [lock ordering](/lock-ordering/), no cycle of waits can form, so there is no [deadlock](/deadlock/).

With rules 1 to 3, the striped structure is [linearizable](/linearizability/) when operations on different stripes commute in the sequential specification: each operation can be linearized when it takes its (last) lock. The proof for the hash table is on the page of the [concurrent hash table](/concurrent-hash-table/).

**How many stripes.** If $p$ operations run at the same time and each picks one of $L$ stripes uniformly and independently, the expected number of pairs that collide is $\binom{p}{2}/L$, and the probability that no two collide is $\prod_{i=0}^{p-1}(1 - i/L)$, the birthday bound. For $L = 16$ and $p = 4$ this is $0.67$; for $L = 16$ and $p = 8$ it is only $0.12$; for $L = 64$ and $p = 8$ it is $0.63$. So $L$ should grow about as $p^2$ for most batches to run without any collision, and as $p$ for a constant expected number of colliding pairs. More stripes cost memory, and a global operation must take all of them.

## Classic examples

- **[Concurrent hash table](/concurrent-hash-table/).** Lock $i$ guards each bucket $b$ with $b \bmod L = i$. The capacity stays a multiple of $L$, so a resize by doubling keeps each key in its stripe. Resize is the global operation.
- **[Two-lock queue](/two-lock-queue/).** Two stripes: the head with its sentinel, and the tail with the last next pointer. A [sentinel node](/sentinel-node/) keeps the two stripes apart even when the queue is empty. Herlihy and Shavit's bounded queue adds a shared counter, which is the place where the two stripes interact.
- **[Sloppy counter](/sloppy-counter/) and striped counters.** One counter per thread or core, each with its own lock or atomic, and a global sum that reads all of them. Java's `LongAdder` stripes a counter over cells in this way.
- **Striped cuckoo hashing.** Herlihy and Shavit give a [cuckoo hashing](/cuckoo-hashing/) table whose operation touches two buckets, so it takes two stripe locks in a fixed order, as in MULTI-STRIPE-OPERATION.
- **Bank transfers.** A transfer between two accounts takes the locks of both stripes in increasing order; a total audit takes all locks.

## Variations

- **Refinable striping.** The number of locks grows with the structure. Herlihy and Shavit's refinable hash set marks one thread as owner of a resize, waits until no thread holds an old lock, and then installs a larger lock array.
- **Lock splitting.** Two locks for two unrelated groups of fields of one object, the case $L = 2$ with a stripe per field group, not per key.
- **Striped [readers-writer locks](/readers-writer-lock/).** Readers of one stripe share it; useful when reads dominate.
- **Hand-over-hand locking.** For linked structures where the parts form a path, [lock coupling](/lock-coupling/) holds two adjacent locks at a time instead of a fixed stripe.
- **Lock-free stripes.** Replace each stripe lock by an atomic word with [compare-and-swap](/compare-and-swap/), as in per-bin CAS of Java 8 `ConcurrentHashMap` for an empty bin.
- **Padding.** Put each lock, or each stripe counter, on its own cache line, so that two stripes do not share a line and slow each other down by false sharing.

## Pitfalls

- **A stripe that moves.** If a key's stripe depends on the current size, for example $h(k) \bmod C$ with a lock per bucket and $C$ changing, a thread can take the lock of the old stripe while another takes the lock of the new one, and both change the same bucket. Keep the stripe function stable (rule 2).
- **Reading the layout before the lock.** Read the array of buckets or segments after taking the stripe lock; a global operation may replace it in between.
- **Two locks in any order.** Two transfers, $a \to b$ and $b \to a$, that each take the source lock first deadlock. Sort the stripes (line L10).
- **An exact global value from unlocked reads.** Summing $L$ stripe counters without the locks gives a value that may never have existed at one moment. Either accept an approximate value or take all locks (line L6).
- **Hot keys.** Striping spreads keys, not load. If one key gets most operations, its stripe is as contended as one global lock.
- **Too many locks.** A global operation costs $\Theta(L)$ acquisitions, and $L$ locks cost memory and cache space. Do not use more stripes than the parallelism needs.

## Exercises

1. A striped table has $L = 8$ locks, $h(k) = k$, and the capacity starts at 8. Someone changes the resize to grow the capacity by half, to 12. Find two keys that are in the same bucket after the resize but whose lock indices $k \bmod 8$ differ. (Answer: for example 0 and 12, both in bucket 0, with locks 0 and 4.) What goes wrong if two threads put these two keys at the same time? Why does growth by a factor of 3 not have this problem?
2. Prove that with rule 3 no deadlock is possible even when operations take any number of stripe locks: assign to each waiting thread the largest index it holds, and show that it increases strictly along a chain of waits.
3. For $p = 8$ threads that each pick a uniform stripe, find the smallest $L$ such that the probability of no collision is at least $1/2$. (Answer: $L = 43$, where the probability is about 0.5002; for $L = 42$ it is about 0.491.)
4. Design a size operation for the striped hash table that is linearizable, and one that is not but never blocks. Which one can return a value that the table never had?

## References
