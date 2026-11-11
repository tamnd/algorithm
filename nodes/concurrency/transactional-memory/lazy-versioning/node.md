---
tag: 2GSNPW
kind: concept
slug: lazy-versioning
name: Lazy versioning
aliases:
- deferred update
- buffered writes
- lazy version management
area: concurrency/transactional-memory
level: advanced
summary: Writes are buffered in a private redo log and reach memory only at commit. Abort is free and memory holds only committed values; every read must look in the log first.
prereqs: [redo-log, software-transactional-memory]
see_also: [eager-versioning, commit-time-locking, lazy-conflict-detection, tl2, norec, transaction-abort, privatization-safety, hardware-transactional-memory]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (version management, eager and lazy) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2.1 (the write set kept as a redo log and written back at commit)
  - paper: doi:10.1145/1693453.1693464
    title: Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec, streamlining STM by abolishing ownership records, PPoPP 2010
    locator: the redo log written back under the global sequence lock
  - paper: doi:10.1145/165123.165164
    title: Maurice Herlihy and J. Eliot B. Moss, Transactional memory, architectural support for lock-free data structures, ISCA 1993
    locator: the transactional cache, which holds tentative values until commit
---

**Lazy versioning** is the version management policy in which a transaction keeps its writes in a private buffer, the [redo log](/redo-log/), and copies them to shared memory only when it commits. Until then, memory holds only committed values. If the transaction aborts, it drops the buffer and nothing in memory has to change. It is one of the three design axes of [software transactional memory](/software-transactional-memory/); the other choice is [eager versioning](/eager-versioning/), which writes in place and keeps an undo log. Lazy versioning makes abort free and keeps other transactions from ever seeing uncommitted values, at the price of a lookup in the log at every read and of a write-back at commit. It is the policy of [TL2](/tl2/), [NOrec](/norec/), [SwissTM](/swisstm/), the write-back mode of [TinySTM](/tinystm/), and of most hardware TMs. This page gives the policy; the redo log page gives the data structure.

## In plain words

The transaction does not touch the real data while it works. It writes its changes on a private list. When it reads something, it first checks its own list, so that it sees its own changes. At the end, if all is well, it copies the list into the real data in one step that nobody can see half done. If it has to give up, it throws the list away, and the real data never changed.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. The STM uses atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$), on a [sequentially consistent](/sequential-consistency/) memory.

A write by transaction $T$ to word $a$ puts $(a, v)$ in $T$'s redo log, or changes the value if $a$ is already there. It takes no shared step (unless the STM also takes a lock at that time, see below).

A read by $T$ of word $a$ first looks up $a$ in the redo log. If $a$ is there, the read returns the logged value: this is *read after write*. Otherwise it reads memory, with the checks of the STM.

At commit, $T$ must make its whole log visible at once. It gets exclusive access to the words in its log (write locks in TL2, one global lock in NOrec), validates its reads, copies each logged value to memory, and releases. At abort, $T$ drops the log and releases any locks; memory needs no repair.

### Locks and lazy versioning

Lazy versioning does not decide when to lock. Two combinations are common:

- **Lazy versioning with [commit-time locking](/commit-time-locking/).** The write locks are taken at commit, just before the write-back. Locks are held for a short time. [TL2](/tl2/) works this way.
- **Lazy versioning with [encounter-time locking](/encounter-time-locking/).** The write lock is taken at the first write, but the value still goes to the log. Another writer finds the conflict at once, and readers still see the old committed value. TinySTM in write-back mode and [SwissTM](/swisstm/) work this way.

With eager versioning, by contrast, the lock must be taken at the first write; see the [eager versioning](/eager-versioning/) page.

### What it costs

- A read pays a lookup in the log. Since most reads are of words the transaction did not write, the lookup must answer "not there" fast: a hash index and a small [Bloom filter](/bloom-filter/) do this.
- A commit pays $w$ memory writes, plus the locking.
- An abort pays nothing in shared memory.
- Memory holds only committed values, so a reader can never see a value that is later undone. This makes [opacity](/opacity/) easier to get and helps with [privatization](/privatization-safety/), though a slow write-back can still race with a thread that has privatized the data.

## Examples

**A transfer in TL2.** Two accounts hold $a_0 = a_1 = 10$, and $T$ moves 3 from $a_0$ to $a_1$. $T$ reads both, logs $[a_0, 7]$ and $[a_1, 13]$, and memory still shows 10 and 10. At commit it locks both stripes, takes a write version from the clock, validates its reads, writes 7 and 13, and releases the locks with the new version. Alone, this costs 16 shared steps in the simulation of the [TL2](/tl2/) page. If $T$ aborts before commit, it has written nothing to memory.

**Read after write.** $T$ writes $a_0 \leftarrow 7$ and then reads $a_0$ to check the balance. The lookup finds $[a_0, 7]$ and returns 7. Without the lookup, $T$ would read the 10 in memory, and a check like "if $a_0 < 0$ abort" would test the wrong value.

**A long reader and a writer.** An audit $U$ reads $a_0 = 10$. $T$ then logs $[a_0, 7]$ and $[a_1, 13]$, but has not committed. $U$ reads $a_1$ and finds 10 in memory, the committed value; with encounter-time locking it also sees $T$'s lock and must decide whether to wait or abort, but with commit-time locking it sees nothing and reads 10. Both reads are of committed values, so $U$ sees a consistent state and can commit before $T$. Under eager versioning, $U$ would instead find 13 in memory (under $T$'s lock) and could not use it.

**Hardware.** Most hardware TMs keep tentative values in the cache and make them visible at commit, which is lazy versioning in hardware: [Herlihy and Moss](/herlihy-moss-htm/) (1993) used a transactional cache, and [Intel TSX](/intel-tsx/) keeps the write set in the L1 cache. A write set that does not fit in the cache makes the transaction abort.

## Where it is used

- Word-based STMs: [TL2](/tl2/), [NOrec](/norec/), [SwissTM](/swisstm/), and [TinySTM](/tinystm/) in write-back mode.
- Object-based STMs such as [DSTM](/dstm/), where a transaction writes to a private copy of the object and the commit makes the copy current.
- Haskell's STM, where each transaction keeps a log of its reads and writes and the commit applies the writes.
- Hardware TMs ([hardware transactional memory](/hardware-transactional-memory/)), where the cache is the buffer.
- In databases, deferred update is a classic choice for optimistic schemes such as [optimistic concurrency control](/optimistic-concurrency-control/), where a transaction writes into a private workspace and its writes are installed after validation.

## References
