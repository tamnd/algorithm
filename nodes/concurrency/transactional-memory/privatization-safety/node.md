---
tag: 9NJC6P
kind: concept
slug: privatization-safety
name: Privatization safety
aliases:
- transactional privatization
- privatization problem
- publication safety
area: concurrency/transactional-memory
level: research
summary: A TM is privatization safe if data that a committed transaction made private can then be used with plain loads and stores, with no interference from transactions still in flight.
prereqs: [weak-atomicity, lazy-versioning, eager-versioning]
see_also: [strong-atomicity, opacity, norec, tl2, zombie-transactions, grace-period, quiescent-state, use-after-free]
sources:
  - paper: doi:10.1145/1281100.1281161
    title: "Michael F. Spear, Virendra J. Marathe, Luke Dalessandro and Michael L. Scott, Brief announcement: privatization techniques for software transactional memory, PODC 2007, pp. 338 to 339"
    locator: the delayed cleanup and doomed transaction problems, and the techniques that wait for concurrent transactions
  - paper: doi:10.1145/1378533.1378588
    title: "Vijay Menon, Steven Balensiefer, Tatiana Shpeisman, Ali-Reza Adl-Tabatabai, Richard L. Hudson, Bratin Saha and Adam Welc, Practical weak-atomicity semantics for Java STM, SPAA 2008, pp. 314 to 325"
    locator: the privatization and publication idioms and the semantics that make them safe in a weakly atomic STM
  - paper: doi:10.1145/1837853.1693464
    title: "Luke Dalessandro, Michael F. Spear and Michael L. Scott, NOrec: streamlining STM by abolishing ownership records, PPoPP 2010 (SIGPLAN Notices 45(5), pp. 67 to 78)"
    locator: the single sequence lock and the argument that NOrec is privatization safe
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 2 (Basic transactions, the semantics of mixed transactional and non-transactional accesses) and Chapter 4 (Software transactional memory)
---

**Privatization safety** is the property of a [transactional memory](/software-transactional-memory/) that lets a program make shared data private with one transaction, for example by setting a flag or by unlinking a node, and then use the data with plain loads and stores. Under [weak atomicity](/weak-atomicity/), many STMs are not privatization safe: a transaction that has already committed can still be writing its values back (the delayed cleanup problem), and a doomed transaction can write in place and then roll back (the doomed transaction problem). Spear, Marathe, Dalessandro and Scott named these problems in 2007. The usual fixes are a fence that waits for concurrent transactions, and designs such as [NOrec](/norec/) whose commit order makes the problem impossible.

## In plain words

A program often uses a transaction to say "this data is mine now", and then works on the data without transactions, because plain code is faster. If transactions really ran one at a time, this would be safe: every other transaction either finished before the claim, or starts after it and sees that the data is taken.

A real STM runs transactions at the same time and finishes them in pieces. A transaction that committed before the claim may still be copying its new values into memory after the claim, and so it overwrites the plain writes of the new owner. A transaction that is about to fail may have written into memory directly, and when it undoes its writes, it erases the owner's work. A privatization-safe STM makes sure that, once the claiming transaction is over, no older transaction can still touch the data.

## The idea

### The idiom

Two processes share a flag `priv` and a word `x`, both 0 at the start.

```
privatizer p                         worker q
atomic { priv ← 1 }                  atomic { if priv = 0 then x ← 100 }
r ← x          ▷ plain load
x ← r + 1      ▷ plain store
```

If the two transactions run in some serial order, and the plain accesses come after the transaction of $p$, the final value is $x = 101$ (the worker ran first) or $x = 1$ (the worker saw the flag). Under a single global lock in place of each `atomic`, the program has no data race, so a programmer expects one of these two values. A TM is privatization safe if it gives only these outcomes for this idiom and its variants (the private data can be a node removed from a list, a buffer, or a whole object that is later freed).

The model on this page: two or more asynchronous processes, sequentially consistent memory with atomic read, write and compare-and-swap, and an STM whose transactions are [opaque](/opacity/) among themselves. Plain accesses are not instrumented, which is weak atomicity.

### The delayed cleanup problem

[TL2](/tl2/) and other STMs with [lazy versioning](/lazy-versioning/) commit in phases: lock the write set, take a version from the [global version clock](/global-version-clock/), validate the read set, and then write the redo log back. The transaction is logically committed (serialized) when it takes its version, but its values reach memory later.

| step | worker $q$ | privatizer $p$ | $x$ |
|---|---|---|---|
| 1 | begin, read `priv` $= 0$, buffer $x \leftarrow 100$ | | 0 |
| 2 | lock $x$, take version 1 (serialized here) | | 0 |
| 3 | | atomic { `priv` $\leftarrow 1$ } commits with version 2 | 0 |
| 4 | | plain load $r = x = 0$ | 0 |
| 5 | | plain store $x \leftarrow 1$ | 1 |
| 6 | write back $x \leftarrow 100$, unlock | | 100 |

The serial order is $q$ then $p$, so $p$ should have read 100 and left 101. It read 0, and its store was lost. The transaction of $p$ did not conflict with $q$: it wrote only `priv`, which $q$ read, but $q$ had already passed its validation.

### The doomed transaction problem

An STM with [eager versioning](/eager-versioning/) writes in place under an encounter-time lock and keeps an [undo log](/undo-log/).

| step | worker $q$ | privatizer $p$ | $x$ |
|---|---|---|---|
| 1 | begin, read `priv` $= 0$ | | 0 |
| 2 | lock $x$, log old value 0, write $x \leftarrow 100$ in place | | 100 |
| 3 | | atomic { `priv` $\leftarrow 1$ } commits | 100 |
| 4 | | plain load $r = x = 100$ | 100 |
| 5 | | plain store $x \leftarrow 101$ | 101 |
| 6 | commit: validation sees the new version of `priv`; abort | | 101 |
| 7 | roll back from the undo log: $x \leftarrow 0$ | | 0 |

The worker is doomed from step 3, but it learns this only at step 6. The privatizer read a value that was never committed, and the rollback erased its store. With lazy versioning the same problem appears in a milder form: a doomed transaction with invisible reads can keep reading the private data while $p$ changes it, so it sees a state that opacity does not cover, because opacity speaks only about transactional accesses. In C or C++, if $p$ frees the private node, the doomed transaction can read freed memory, a [use-after-free](/use-after-free/).

### Fixes

- **Quiescence (privatization fence).** After a transaction that may privatize commits, its process waits until every transaction that was active at that moment has ended: committed and written back, or aborted and rolled back. This is the same wait as a [grace period](/grace-period/) in [read-copy-update](/read-copy-update/). In the two runs above, the fence makes $p$ wait for $q$ before step 4: in the first run $q$ finishes its write-back, and $p$ then reads 100; in the second run $q$ aborts and rolls back first, and its retry sees `priv` $= 1$. The cost is a wait proportional to the longest concurrent transaction, paid at each fenced commit. Spear, Marathe, Dalessandro and Scott study fences of this kind and cheaper variants.
- **Ordered commit and write-back.** If a transaction cannot commit until all transactions that serialized before it have finished their write-back, the delayed cleanup problem disappears. [NOrec](/norec/) gets this for free: a writer holds the global sequence lock from its serialization point until the end of its write-back, so the commit of $p$ waits for $q$. NOrec also uses lazy versioning and value-based validation of every read, so a doomed transaction never writes in place and never acts on an inconsistent value. Dalessandro, Spear and Scott list privatization safety as one of the benefits of the design.
- **[Strong atomicity](/strong-atomicity/).** If every plain access is instrumented to behave as a tiny transaction, the plain store of $p$ conflicts with $q$, and the problem is gone, at the cost of slowing all code outside transactions.
- **Single global lock atomicity.** Menon et al. define the semantics that a weakly atomic STM should give to race-free programs as those of one global lock. That definition makes privatization safety (and publication safety, below) a requirement, and their Java STM meets it with commit ordering and waiting.

### Publication

Publication is the dual idiom: a process initializes data with plain stores and then makes it shared with a transaction that sets a flag; other transactions read the flag and then the data. It fails if the plain stores become visible after the flag (a memory model issue: the stores need release order before the publishing commit), or if a reader reads the data early, before the flag, and the STM does not notice that the data changed, because plain stores do not change versions. TL2 aborts such a reader at its read of the flag (the flag has a version newer than the start of the reader); an STM that validates only at commit lets it commit with the new flag and the old data. Menon et al. treat publication and privatization together.

## Examples

**Removing a node and freeing it.** A transaction unlinks a node from a shared linked list, and the process then frees the node or reuses its memory. This is privatization of the node. Without a fence, a doomed transaction that read the old link can still read or write the node; this is the same hazard that [epoch-based reclamation](/epoch-based-reclamation/) and [hazard pointers](/hazard-pointers/) handle for lock-free lists, and the quiescence fence is the epoch method applied to transactions.

**A work queue.** A transaction takes a task object off a shared queue and the process then runs the task with plain code. A worker transaction that was about to update the task (for example, to cancel it) must be finished before the plain code starts, which is what the fence gives.

**The two runs above** are the smallest cases. Each needs only two processes, one shared flag and one data word. With a fence after the privatizing transaction, or with NOrec, every interleaving of these two programs ends with $x = 1$ or $x = 101$.

## Where it is used

- Every STM that supports mixed transactional and plain code with single-global-lock semantics must solve this problem, either with fences after commits or with a commit protocol like NOrec.
- Language-level transactions (in research Java and C++ compilers) present transactions as atomic blocks that behave like one global lock for race-free programs, which is the semantics of Menon et al., and so they rely on privatization safety.
- [Hardware transactional memory](/hardware-transactional-memory/) is privatization safe by construction: a hardware transaction publishes its writes in one step at commit and keeps its writes in the cache until then, so there is no write-back after commit and no rollback in memory. A [hybrid TM](/hybrid-transactional-memory/) must keep this property on its software path.

## References
