---
tag: HQKVBH
kind: data-structure
slug: concurrent-hash-table
name: Concurrent hash table
aliases:
- concurrent hash map
area: data-structures/concurrent-structures
level: core
summary: Hash table supporting concurrent insert, lookup and delete, typically with lock striping or lock-free buckets.
implements: [dictionary]
prereqs: [hash-table, separate-chaining, lock-striping, linearizability]
see_also: [split-ordered-list, michael-hash-table, ctrie, rehashing, load-factor, readers-writer-lock, lock-ordering]
sources:
  - book: isbn:9780123973375
    title: Maurice Herlihy and Nir Shavit, The Art of Multiprocessor Programming, revised reprint
    locator: Chapter 13 (Concurrent Hashing and Natural Parallelism), Sections 13.2.1 (coarse-grained hash set), 13.2.2 (striped hash set), 13.2.3 (refinable hash set) and 13.3 (lock-free hash set)
  - book: isbn:9780321349606
    title: Brian Goetz and others, Java Concurrency in Practice
    locator: Section 11.4.3 (Lock striping), on the 16 locks of ConcurrentHashMap
  - paper: doi:10.1145/1147954.1147958
    title: Ori Shalev and Nir Shavit, Split-ordered lists, lock-free extensible hash tables, Journal of the ACM 53(3), 2006
    locator: whole paper
  - paper: doi:10.1145/564870.564881
    title: Maged M. Michael, High performance dynamic lock-free hash tables and list-based sets, SPAA 2002
    locator: whole paper
---

A concurrent hash table is a [hash table](/hash-table/) that many threads use at the same time for put, get and remove, with each operation [linearizable](/linearizability/) as one atomic step on the [dictionary](/dictionary/). Operations on different keys usually touch different buckets, so a good design lets them run in parallel. The classic lock-based design is [lock striping](/lock-striping/): a fixed array of $L$ locks, where lock $i$ guards each bucket whose index is $i$ modulo $L$, and a resize that takes all locks in order. Lock-free designs, such as the [Michael hash table](/michael-hash-table/) and the [split-ordered list](/split-ordered-list/), replace the locks by [compare-and-swap](/compare-and-swap/).

## In plain words

A hash table puts each key in a bucket that its hash picks. If many threads use the table, two of them may change the same bucket at the same moment and spoil it. One lock for the whole table fixes that, but then only one thread works at a time.

Most of the time, two threads work on different buckets and do not need to wait for each other. So give the table several locks, for example sixteen. Each lock guards every sixteenth bucket. A thread takes only the lock of its key's bucket. Threads with keys in different groups work in parallel.

When the table gets too full, it must grow. Growing moves every key, so the thread that grows the table takes all the locks, one after another in a fixed order, and then rebuilds the buckets.

## The abstract type

The table implements the [dictionary](/dictionary/) over keys with a [hash function](/hash-function/) $h$:

- put$(k, v)$ maps $k$ to $v$ and returns the old value of $k$, or MISSING;
- get$(k)$ returns the value of $k$, or MISSING;
- remove$(k)$ deletes $k$ and returns its old value, or MISSING.

The correctness condition is [linearizability](/linearizability/) with respect to this sequential dictionary. A size operation is often only approximate in concurrent tables; this page uses the count of pairs only to decide when to resize.

## Representation

- $T.locks[0 \ldots L-1]$: $L$ mutexes. The number $L$ is fixed.
- $T.buckets[0 \ldots C-1]$: the bucket array, with [separate chaining](/separate-chaining/). The capacity $C$ is always a multiple of $L$. Resize replaces the array by a new one of capacity $2C$.
- $T.count[0 \ldots L-1]$: $T.count[i]$ is the number of pairs whose key has $h(k) \bmod L = i$. Only the holder of lock $i$ writes it.

**Invariant (S).** For each pair $(k, v)$ in the table, $(k, v)$ is in bucket $h(k) \bmod C$, and no key is in two pairs. The pairs, as a map, are the abstract dictionary.

**Stripe fact.** Since $L$ divides $C$, $(h(k) \bmod C) \bmod L = h(k) \bmod L$. So all keys in bucket $b$ have the stripe $b \bmod L$, and a thread can find the lock of a key before it reads $C$: the lock $h(k) \bmod L$ does not depend on the capacity. This is why the capacity grows by doubling and the lock array keeps its size.

## Operations

```pseudo id=main
PUT(T, k, v)
L1  acquire(T.locks[h(k) mod L])
L2  B ← T.buckets; b ← B[h(k) mod |B|]
L3  if b holds a pair (k, w) then
L4      old ← w; replace the pair by (k, v)
L5  else old ← MISSING; append (k, v) to b; T.count[h(k) mod L] += 1
L6  release(T.locks[h(k) mod L])
L7  if Σ T.count > max_load · |B| then
L8      RESIZE(T, |B|)
L9  return old

GET(T, k)
L10 acquire(T.locks[h(k) mod L]); b ← T.buckets[h(k) mod |T.buckets|]
L11 res ← the value of the pair (k, ·) in b, or MISSING
L12 release(T.locks[h(k) mod L]); return res

RESIZE(T, C)                                   ▷ C: the capacity the caller saw
L13 for i ← 0 to L − 1 do acquire(T.locks[i])  ▷ always in index order
L14 if |T.buckets| = C then                    ▷ nobody resized in the meantime
L15     B' ← 2C empty buckets; move each pair (k, v) to B'[h(k) mod 2C]
L16     T.buckets ← B'
L17 for i ← 0 to L − 1 do release(T.locks[i])
```

REMOVE$(T, k)$ is GET with a deletion: under the same lock it finds the pair, deletes it, decrements $T.count[h(k) \bmod L]$ and returns the old value.

**Put, get and remove** hold one lock, the lock of the key's stripe. Line L2 reads the bucket array under this lock. A resize holds all locks, so the array cannot change while the operation holds its lock. The test of line L7 reads the counters without locks; a stale sum only makes a resize a little early or late.

**Resize** takes the locks in increasing index order. Two threads may both see a full table and both call RESIZE with the same old capacity $C$. The first one doubles the table. The second one gets the locks later, finds $|T.buckets| \ne C$ at line L14, and does nothing.

## Example

Take $L = 2$ locks, capacity $C = 2$, max load 1, and $h(k) = k$. The table holds $4 \mapsto a$ in bucket 0 and $7 \mapsto b$ in bucket 1. Thread $A$ calls put$(6, c)$, thread $B$ calls put$(9, d)$ and thread $C$ calls get$(4)$. The keys 4 and 6 are in stripe 0 and the key 9 is in stripe 1. A spin is one failed try to take a lock.

| step | thread | what it does | lock 0 | lock 1 | buckets |
|---|---|---|---|---|---|
| 1 | $A$ | L1, L2: takes lock 0, reads the array | $A$ | | [4] [7] |
| 2 | $B$ | L1, L2: takes lock 1 | $A$ | $B$ | [4] [7] |
| 3 | $C$ | L10: spins on lock 0 | $A$ | $B$ | [4] [7] |
| 4 | $A$ | L5: appends 6 to bucket 0 | $A$ | $B$ | [4 6] [7] |
| 5 | $B$ | L5: appends 9 to bucket 1 | $A$ | $B$ | [4 6] [7 9] |
| 6, 7 | $C$ | spins | $A$ | $B$ | |
| 8 | $A$ | L6: releases lock 0; L7: $4 > 1 \cdot 2$; L13: takes lock 0 again, spins on lock 1 | $A$ | $B$ | |
| 9 to 11 | $A$ | spins on lock 1 | $A$ | $B$ | |
| 12 | $B$ | L6: releases lock 1; L7: $4 > 2$; L13: spins on lock 0 | $A$ | | |
| 13 to 17 | $B$ | spins on lock 0 | $A$ | | |
| 18 | $A$ | L13: takes lock 1; L14: capacity is 2; L15, L16: doubles | $A$ | $A$ | [4] [9] [6] [7] |
| 19, 20 | $B$, $C$ | spin | $A$ | $A$ | |
| 21 | $A$ | L17: releases both; put returns MISSING | | | |
| 22 | $B$ | L13: takes both locks; L14: capacity is 4, not 2, so no resize | $B$ | $B$ | |
| 25 | $B$ | L17: releases both; put returns MISSING | | | |
| 26 to 29 | $C$ | L10 to L12: takes lock 0, reads the new array, finds 4; returns $a$ | | | |

Steps 1 to 5 show the parallelism: $A$ and $B$ change the table at the same time, because their keys are in different stripes, while $C$ waits for $A$ because 4 and 6 share stripe 0. Steps 12 and 22 show why line L14 is needed: without it, $B$ would double the table a second time. After the resize, key 6 is in bucket $6 \bmod 4 = 2$, and $2 \bmod 2 = 0 = 6 \bmod 2$: it is still in stripe 0.

## Correctness

The table is linearizable, with the linearization point of put, get and remove at the moment the operation takes its stripe lock, and it is deadlock-free. The proof rests on three facts. Two operations on the same key take the same lock, by the stripe fact, so their critical sections are ordered. Operations on different keys commute in the sequential dictionary, so their relative order does not change any result. A resize holds all locks and does not change the map, only where pairs are stored, and it keeps (S). Deadlock is not possible because each thread holds at most one lock outside RESIZE and RESIZE takes the locks in one global order, the rule of [lock ordering](/lock-ordering/). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $n$ be the number of pairs, $C$ the capacity, $L$ the number of locks and $\alpha = n / C$ the [load factor](/load-factor/), at most max_load after each resize.

| operation | steps inside the lock | waits for |
|---|---|---|
| put, get, remove | $O(1 + \text{chain length})$, expected $O(1 + \alpha)$ under simple uniform hashing (see [chaining analysis](/chaining-analysis/)) | operations of the same stripe, and resizes |
| resize | $L$ lock acquisitions plus $\Theta(n + C)$ to rehash | all operations |
| space | $\Theta(n + C + L)$ | |

The resize doubles the capacity, so the rehash cost is $O(1)$ amortized per put, as in the sequential [rehashing](/rehashing/) argument. During a resize no other operation runs. With $p$ threads and keys spread evenly over the $L$ stripes, two operations conflict with probability about $1/L$, so the table scales while $p$ is well below $L$. Get takes the lock too; Java's `ConcurrentHashMap` instead makes get read without a lock, which needs care with the memory model.

## Variants

- **Coarse-grained table.** One lock for everything. It is the case $L = 1$.
- **Refinable striping.** Herlihy and Shavit also give a table whose lock array grows with the bucket array, so the number of buckets per lock stays bounded. A resizer marks itself as owner, waits for the threads that hold old locks, and replaces the lock array.
- **Per-bucket locks.** Java 8 `ConcurrentHashMap` locks the first node of a bin and fills an empty bin with one CAS. Earlier versions used 16 segments, each a small hash table with its own lock, the design that Goetz and others use to explain [lock striping](/lock-striping/).
- **[Readers-writer locks](/readers-writer-lock/).** Let gets of one stripe run together. This helps when reads dominate and chains are long.
- **Lock-free chaining.** The [Michael hash table](/michael-hash-table/) keeps a fixed array of lock-free sorted lists, each a [Harris linked list](/harris-linked-list/).
- **Lock-free resizing.** The [split-ordered list](/split-ordered-list/) of Shalev and Shavit stores all keys in one lock-free list in bit-reversed order, so that doubling the table only adds new bucket pointers into the list and moves no key.
- **[Ctrie](/ctrie/).** A lock-free hash trie that grows level by level and supports atomic snapshots.
- **Concurrent open addressing.** Cuckoo and hopscotch tables with striped locks, for example concurrent [cuckoo hashing](/cuckoo-hashing/).

## When to use it

Use a striped table when many threads read and write a shared map and keys are spread over many buckets. Use a lock-free table when threads can be descheduled while they hold a lock, or when resizes must not stop all threads. If one thread writes and many read, a design with lock-free reads, or [read-copy-update](/read-copy-update/), is often faster. If the map is per thread, use a plain [hash table](/hash-table/) and merge at the end.

## Pitfalls

- **A stripe that depends on the capacity.** If the lock index were $h(k) \bmod C$ reduced to $L$ in another way, or if $L$ did not divide $C$, then after a resize a key could move to a bucket whose lock is not the key's lock, and two threads would change one bucket under two different locks. Keep $C$ a multiple of $L$ and grow by doubling.
- **Reading the array before the lock.** If line L2 ran before line L1, a resize could replace the array between the two lines, and the put would change a bucket of the old array, which is lost. Read the array after the lock, as line L2 does.
- **Resizing twice.** Without the test of line L14, two threads that saw the same full table both double it. Pass the capacity that the caller saw.
- **Locks in any order.** A resize that takes the locks in different orders in different threads can deadlock with another resize. Take them in index order, line L13.
- **Size as a promise.** The sum of the counters at line L7 is read without locks. It is only a hint; a size method that must be exact has to take all locks.
- **A bad hash.** With few distinct values of $h(k) \bmod L$, all threads hit the same stripe, and the table is no better than one lock. Mix the hash bits first.

## Implementations

The Python class follows the pseudocode, with remove as a third operation. Each operation is a generator that yields after each shared step and takes locks by repeated tries, so the tests replay the example, check that two stripes run in parallel and that one stripe waits, and run random interleavings with forced resizes against the sequential dictionary with a linearizability search. The plain methods also run under real threads.

## History

Herlihy and Shavit present the coarse, striped and refinable tables in Chapter 13 of their book. Doug Lea's `ConcurrentHashMap`, in Java 5, used segments with one lock each, and Java 8 replaced them by locks on single bins. Michael gave a lock-free hash table with a fixed number of buckets in 2002, and Shalev and Shavit gave the split-ordered list, a lock-free table that can grow, first at PODC 2003 and in the Journal of the ACM in 2006.

## References
