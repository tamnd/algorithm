---
tag: 7J4CAH
kind: concept
slug: software-transactional-memory
name: Software transactional memory
aliases:
- STM
area: concurrency/transactional-memory
level: advanced
summary: Transactions on ordinary memory, built in software from reads, writes and atomic primitives such as CAS. Designs differ in concurrency control, version management and conflict detection.
history:
  year: 1995
  people: [Nir Shavit, Dan Touitou]
  note: Shavit and Touitou presented the first STM at PODC 1995 (journal version 1997). DSTM (2003) made transactions dynamic, and TL2, TinySTM, SwissTM and NOrec followed from 2006 to 2010.
prereqs: [transaction, compare-and-swap]
see_also: [hardware-transactional-memory, opacity, contention-management, retry-and-orelse, privatization-safety, tl2, norec, stamp-benchmark-suite]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (basic transactions and the design choices of concurrency control, version management and conflict detection) and Chapter 4 (Software transactional memory)
  - paper: doi:10.1145/224964.224987
    title: Nir Shavit and Dan Touitou, Software transactional memory, PODC 1995
    locator: the first STM and the name of the field
  - paper: doi:10.1007/s004460050028
    title: Nir Shavit and Dan Touitou, Software transactional memory, Distributed Computing 10(2), 1997
    locator: the journal version
  - paper: doi:10.1145/872035.872048
    title: "Maurice Herlihy, Victor Luchangco, Mark Moir and William N. Scherer III, Software transactional memory for dynamic-sized data structures, PODC 2003, pages 92-101"
    locator: dynamic transactions, obstruction-freedom and contention managers
  - paper: doi:10.1145/1065944.1065952
    title: Tim Harris, Simon Marlow, Simon Peyton Jones and Maurice Herlihy, Composable memory transactions, PPoPP 2005
    locator: the STM interface of Concurrent Haskell, with retry and orElse
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapters on transactional programming and software transactional memory
---

Software transactional memory (STM) runs [transactions](/transaction/) on ordinary shared memory, with no special hardware. The programmer marks a block of code as atomic. The STM runs it so that it commits as a whole or aborts with no effect, and so that the committed blocks appear to run one at a time. To do this, the STM puts a small amount of code around every shared read and write of the block. That code keeps logs and per-word metadata, and uses atomic primitives such as [compare-and-swap](/compare-and-swap/) (CAS) to detect conflicts and to commit. Nir Shavit and Dan Touitou built the first STM and named it (PODC 1995; journal version 1997). The many STMs since then differ mainly on three design axes: **concurrency control** (pessimistic or optimistic), **version management** (eager or lazy) and **conflict detection** (eager or lazy). [Hardware transactional memory](/hardware-transactional-memory/) does the same job in the cache of the processor.

## In plain words

Locks make the programmer decide which data each lock protects and in which order to take the locks. An STM lets the programmer write "do these steps atomically" instead. Behind the scenes, the STM watches every shared read and write of the block. It keeps track of what the block read and what it wants to write. If two blocks touch the same data in a way that matters, the STM stops one of them, undoes it, and runs it again. If they do not, both run at the same time. The work of watching every access costs time, often several times the cost of the plain code, but the program is easier to write and blocks that do not touch the same data run in parallel.

## The idea

**Notation and model.** $n$ is the number of processes, $p$ and $q$ are processes, $m$ is the number of data words, and $r$ and $w$ are the numbers of words one transaction reads and writes. The processes are asynchronous and may crash between any two steps. The STM uses atomic read and write and one or more of [compare-and-swap](/compare-and-swap/) (consensus number $\infty$), [load-linked/store-conditional](/load-linked-store-conditional/) (also $\infty$) and [fetch-and-add](/fetch-and-add/) (consensus number 2). The memory is [sequentially consistent](/sequential-consistency/) unless a page says otherwise.

### The interface

An STM offers begin, read$(a)$, write$(a, v)$ and commit, and any of them may abort. A compiler or a library turns `atomic { ... }` into these calls and runs the block again after each abort. A word-based STM works on memory words; an object-based STM works on objects and opens each one for reading or writing before use. The [read set and write set](/read-set-and-write-set/) of a transaction are the words it has read and written so far.

The safety condition is usually [opacity](/opacity/): every transaction, also one that later aborts, sees values that agree with one serial order of transactions that respects real time. Opacity is stronger than [serializability](/serializability/) of the committed transactions. It is needed because a transaction that reads an inconsistent state can loop or crash before the STM aborts it; such a transaction is a [zombie](/zombie-transactions/).

### The three design axes

1. **Concurrency control.** *Pessimistic* control detects a conflict and resolves it at the moment of the access, for example with a write lock taken at the first write. *Optimistic* control lets the conflict happen, and detects and resolves it later, usually at commit. Most STMs are pessimistic for writes and optimistic for reads.
2. **Version management.** With [eager versioning](/eager-versioning/), a write goes to memory at once, and the old value goes to an [undo log](/undo-log/) for the case of an abort. With [lazy versioning](/lazy-versioning/), a write goes to a private [redo log](/redo-log/), and memory changes only at commit.
3. **Conflict detection.** A [transaction conflict](/transaction-conflict/) is a pair of accesses to the same word by two transactions, at least one of them a write. [Eager conflict detection](/eager-conflict-detection/) finds it at the access. [Lazy conflict detection](/lazy-conflict-detection/) finds it at commit. Some STMs mix the two: [SwissTM](/swisstm/) is eager for write-write conflicts and lazy for read-write conflicts.

The choice of when to take the write locks, [encounter-time locking](/encounter-time-locking/) or [commit-time locking](/commit-time-locking/), is close to the conflict detection axis but not the same thing; those pages explain the difference.

### Other choices

- **Metadata.** Most STMs map each word to an ownership record: a versioned lock in a table, hashed by address ([lock striping](/lock-striping/)). [NOrec](/norec/) keeps only one global sequence lock and validates by value.
- **Read visibility.** With *invisible reads*, a reader writes no shared data, and it must [validate](/transaction-validation/) its reads to find conflicts. With *visible reads*, a reader registers itself, so that writers can see it, at the price of a shared write per read.
- **Validation cost.** Checking the whole read set at each read costs $1 + 2 + \dots + r = r(r+1)/2$ checks; a [global version clock](/global-version-clock/) cuts this to $O(r)$.
- **Progress.** Lock-based STMs ([TL2](/tl2/), [TinySTM](/tinystm/)) are blocking and fast. Non-blocking STMs are [lock-free](/lock-freedom/) ([Shavit-Touitou STM](/shavit-touitou-stm/)) or [obstruction-free](/obstruction-freedom/) ([DSTM](/dstm/)) and need a [contention manager](/contention-management/) to avoid [livelock](/livelock/).
- **Multiple versions.** A [multi-version STM](/multi-version-stm/) keeps old values so that read-only transactions never abort.
- **Composition.** Haskell's STM adds `retry` and `orElse` ([retry and orElse](/retry-and-orelse/)). [Nested transactions](/nested-transactions/) and [irrevocable transactions](/transaction-irrevocability/) extend the model further.

### The costs

Each shared access becomes a call with a few more memory accesses. On a single thread, STM code typically runs several times slower than the same code with no synchronization. Aborts waste the work done so far ([transaction abort](/transaction-abort/)). And mixing transactional and non-transactional access to the same data raises the problems of [weak atomicity](/weak-atomicity/) and [privatization safety](/privatization-safety/).

## Examples

**A transfer under several STMs.** Two accounts hold $a_0 = a_1 = 10$. A transaction moves 3 from $a_0$ to $a_1$: two reads and two writes. An audit reads both. The table counts the shared memory steps when each runs alone, in the simulations of this site (each page has its code). These are steps of the simplified code on each page, not times of the real systems.

| STM | Versioning | Locking or ownership | Transfer | Audit of 2 words |
|---|---|---|---|---|
| [Shavit-Touitou](/shavit-touitou-stm/) | static, in place under ownership | ownership in address order, LL/SC | 26 | 20 |
| [DSTM](/dstm/) | new object version per write | locator CAS at open | 16 | 11 |
| [TL2](/tl2/) | lazy (redo log) | commit-time locking | 16 | 7 |
| [TinySTM](/tinystm/), write-back | lazy | encounter-time locking | 16 | 7 |
| [TinySTM](/tinystm/), write-through | eager (undo log) | encounter-time locking | 18 | 7 |
| [SwissTM](/swisstm/) | lazy | eager write locks, commit-time read locks | 28 | 10 |
| [NOrec](/norec/) | lazy | one global sequence lock | 9 | 5 |

NOrec has the fewest steps because it has no per-word metadata. That is also its limit: all commits go through one lock. The audit is cheap in TL2 and TinySTM because a read-only transaction there needs no commit step beyond its reads and lock checks.

**A conflict, two ways.** $T_1$ writes $x$ and then computes for a long time; $T_2$ then reads $x$. With eager conflict detection and encounter-time locks, $T_2$ sees the lock of $x$ at once and waits or aborts. With lazy detection and a redo log, $T_2$ reads the old value of $x$ and continues; if $T_1$ commits first, $T_2$ fails its validation later and aborts with more work wasted, but if $T_2$ commits first, both commit and no work is lost.

**An example that needs opacity.** $T_1$ keeps the invariant $x = y$ and changes both from 0 to 1. A transaction $T_2$ that reads $x = 0$ before $T_1$ commits and $y = 1$ after it, and then runs `while x != y: pass`, loops for ever if the STM checks its reads only at commit. An opaque STM aborts $T_2$ at the read of $y$. See [zombie transactions](/zombie-transactions/).

## Where it is used

- **Haskell.** GHC's `Control.Concurrent.STM` is the best known STM in production use, with `retry` and `orElse` (Harris, Marlow, Peyton Jones and Herlihy 2005). The type system keeps I/O out of transactions.
- **Clojure.** Clojure refs use a multi-version STM.
- **C and C++.** GCC supports `__transaction_atomic` blocks with the `-fgnu-tm` option and its libitm library, which can use STM, hardware TM or a global lock. The C++ Transactional Memory Technical Specification (ISO/IEC TS 19841:2015) defined atomic blocks for C++.
- **Research systems.** DSTM, TL2, TinySTM, SwissTM, NOrec, RSTM and McRT-STM, often compared on the [STAMP benchmark suite](/stamp-benchmark-suite/).
- **Hybrid systems.** [Hybrid transactional memory](/hybrid-transactional-memory/) runs transactions in hardware and falls back to an STM. [Transactional lock elision](/transactional-lock-elision/) runs lock-based critical sections as hardware transactions.

STM has not replaced locks in mainstream languages. Its overhead on a single thread, the problems with I/O inside transactions, and the problems of mixing transactional and plain accesses have kept it mostly in languages that control side effects, such as Haskell and Clojure, and in research.

## References
