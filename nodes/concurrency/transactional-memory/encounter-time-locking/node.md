---
tag: MKWRVM
kind: concept
slug: encounter-time-locking
name: Encounter-time locking
aliases:
- eager locking
- ETL
- eager acquire
area: concurrency/transactional-memory
level: advanced
summary: An STM takes the write lock of a word at the transaction's first write to it and holds it to the end. Write conflicts show up at once and reads of own writes are cheap; locks are held long.
prereqs: [eager-conflict-detection]
see_also: [commit-time-locking, eager-versioning, tinystm, swisstm, tl2, transaction-conflict, contention-management, deadlock]
sources:
  - paper: doi:10.1145/1345206.1345241
    title: "Pascal Felber, Christof Fetzer and Torvald Riegel, Dynamic performance tuning of word-based software transactional memory, PPoPP 2008, pages 237-246"
    locator: the encounter-time locking design of TinySTM, with write-back and write-through, and the reasons the authors give for it
  - paper: "Dave Dice and Nir Shavit, What really makes transactions faster?, TRANSACT 2006"
    locator: the first Transactional Locking (TL) algorithm and its encounter-time and commit-time locking modes
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: the discussion of encounter-order and commit-time lock acquisition
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 4 (Software transactional memory), the sections on lock-based STM with versioned locks
---

**Encounter-time locking** (ETL) is the rule that a lock-based [software transactional memory](/software-transactional-memory/) takes the write lock of a word (or of its stripe) when the transaction first writes the word, and keeps it until the transaction commits or aborts. Its counterpart is [commit-time locking](/commit-time-locking/) (CTL), which takes all the write locks at the start of the commit. [TinySTM](/tinystm/) uses ETL in both of its modes; [TL2](/tl2/) uses CTL. ETL is a choice about *when locks are held*, which is not the same thing as when conflicts are *detected*. ETL lets a transaction see a write-write conflict at once, and lets a reader see a write in progress; whether the reader then treats it as a conflict is a separate choice, and read-write conflicts with invisible reads are found by validation whatever the locking time. ETL is required for [eager versioning](/eager-versioning/), and it is a common but optional companion of [lazy versioning](/lazy-versioning/).

## In plain words

When a transaction is about to change a word for the first time, it locks the word right away and keeps the lock until the end. Anyone else who wants to change the same word sees the lock at once and knows there is a clash. The transaction can then also find its own changes quickly, because the lock points to them. The cost is that the word stays locked for the rest of the transaction, even if the transaction has much more work to do.

## The idea

**Notation and model.** $n$ is the number of processes, $r$ and $w$ the numbers of words a transaction reads and writes. Each word maps to a versioned lock: one word that holds either a version number or the owner. The STM uses atomic read, write and [compare-and-swap](/compare-and-swap/) (consensus number $\infty$), on a [sequentially consistent](/sequential-consistency/) memory.

A write of $T$ to word $a$ with ETL:

1. Read the lock of $a$. If $T$ owns it, go to step 3.
2. If another transaction owns it, ask the [contention manager](/contention-management/): abort $T$, or wait and try again. If it is free with a version that $T$'s snapshot allows, take it with a CAS from (version, free) to (owner $T$); if the CAS fails, start over.
3. Write the value: into the [redo log](/redo-log/) (write-back) or into memory after logging the old value in the [undo log](/undo-log/) (write-through).

A read of $T$ of word $a$ reads the lock. If $T$ owns it, the value is $T$'s own write: with write-through it is in memory, with write-back the lock can point at the entry in the redo log, so no hash lookup is needed. If another transaction owns it, the reader treats it as a conflict (TinySTM) or ignores it and reads the committed value (SwissTM, see below).

At commit, $T$ already holds all its write locks. It validates its reads, gets a write version, writes back (in write-back mode), and releases each lock with the new version.

### Time of locking and time of detection

ETL and [eager conflict detection](/eager-conflict-detection/) are often named together, but they are two different choices:

| Kind of conflict | What ETL gives | What still decides detection |
|---|---|---|
| write, then write | the second writer sees the lock at its write | the contention manager may still wait instead of abort |
| write, then read | the reader can see the lock at its read | whether readers look at write locks at all |
| read, then write | nothing: the reader left no trace | read validation, at the next read or at commit |

[SwissTM](/swisstm/) shows the difference. Its writers take a write lock at their first write, so write-write conflicts are found at once. But its readers ignore write locks and read the committed value, and a writer takes a second, read-visible lock only at commit; so read-write conflicts are found lazily. In the SwissTM test `test_lazy_read_write_detection`, a reader reads $x = 0$ while a writer holds the write lock of $x$, and the reader commits without an abort. So SwissTM uses ETL for its write locks and still detects read-write conflicts at commit time.

### Why ETL

- Write-write conflicts appear at once, so a doomed writer wastes less work.
- Read after write is cheap: owning the lock tells the transaction that the word is in its write set.
- It is required with eager versioning, since memory holds uncommitted values under the lock.
- The commit is short: the locks are already held.

### Why not

- Locks are held for the rest of the transaction. Others that need the word abort or wait for that whole time.
- Two transactions that lock in opposite orders can wait for each other. With waiting this is a [deadlock](/deadlock/); STMs avoid it by aborting instead of waiting, or by waiting with a timeout.
- It aborts transactions that could both commit, such as two blind writes to one word.

## Examples

**Lock hold time.** A transaction reads $a_0$, writes $a_0 \leftarrow a_0 - 1$, and then reads $k$ more words. The table counts, in a solo run of the simulations, the shared steps between the CAS that takes the lock of $a_0$ and the write that releases it.

| $k$ | [TL2](/tl2/) (CTL) | TinySTM write-back (ETL) | TinySTM write-through (ETL) |
|---|---|---|---|
| 0 | 3 | 3 | 4 |
| 2 | 3 | 9 | 10 |
| 5 | 3 | 18 | 19 |

Each read costs 3 shared steps in both STMs, and under ETL each of them is done while the lock is held: the hold time grows as $3 + 3k$, while under CTL it stays at 3. The total cost of the solo run is the same (9, 15 and 24 steps for TL2 and TinySTM write-back).

**A write-write conflict.** $T_1$ writes $x \leftarrow 1$ and owns the lock of $x$; then $T_2$ writes $x \leftarrow 2$. Under TinySTM's ETL, $T_2$ finds the lock owned at its first write and aborts there, after 2 shared steps; the test `test_encounter_time_locking_finds_a_write_write_conflict_at_the_write` runs this. Under TL2's CTL, $T_2$ takes the lock at its own commit and commits first, and $T_1$ then commits after it: both writes are blind, so the order "$T_2$ then $T_1$" is legal and nothing is lost.

## Where it is used

- [TinySTM](/tinystm/) (2008), in its write-back and write-through modes.
- [SwissTM](/swisstm/) (2009), for its write locks only.
- The McRT STM (2006) and the STM of Adl-Tabatabai et al. (PLDI 2006), which write in place.
- The first Transactional Locking algorithm of Dice and Shavit (TRANSACT 2006) offered both encounter-time and commit-time modes; TL2 kept commit-time locking.
- Most hardware TMs behave like ETL with eager detection: a transactional write gets exclusive ownership of the cache line at once.

## References
