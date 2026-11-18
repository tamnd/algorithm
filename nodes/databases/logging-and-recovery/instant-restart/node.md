---
tag: 81XW5M
kind: algorithm
slug: instant-restart
name: Instant restart
aliases:
- instant recovery
- on-demand restart
area: databases/logging-and-recovery
level: research
summary: Admit new transactions right after log analysis and redo or undo each page or transaction on demand when it is first touched.
solves: [crash-recovery]
model: word-ram
complexity:
  vars: {n: the records in the stable log after the last checkpoint, u: the updates of the losers that are not yet compensated, m: the number of losers}
  time: {worst: O(n + u + m)}
  space: {extra: O(n)}
properties: {deterministic: true}
history:
  year: 2015
  people: [Goetz Graefe, Wey Guy, Caetano Sauer, Theo Härder]
  note: Graefe, Guy and Sauer described instant restart in their book on instant recovery with write-ahead logging; Härder, Sauer, Graefe and Guy summarized it in Datenbank-Spektrum in 2015.
prereqs: [aries-recovery, strict-two-phase-locking, log-sequence-number]
see_also: [crash-recovery, media-recovery, fuzzy-checkpoint, compensation-log-record, buffer-pool, physiological-logging, write-behind-logging, checkpointing]
sources:
  - book: isbn:9781627058728
    title: Goetz Graefe, Wey Guy and Caetano Sauer, Instant Recovery with Write-Ahead Logging, second edition, Morgan and Claypool, 2016
    locator: the chapters Single-Page Recovery, Instant Restart after a System Failure, and Applications of Instant Restart, chapter level only
  - paper: doi:10.1007/s13222-015-0204-3
    title: Theo Härder, Caetano Sauer, Goetz Graefe and Wey Guy, Instant recovery with write-ahead logging, Datenbank-Spektrum 15(3), 2015, pages 235 to 239
    locator: the overview of single-page repair, instant restart and instant restore, paper level
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the analysis, redo and undo passes of restart, and new transaction processing during undo, paper level
---

Instant restart, also called on-demand restart, recovers a database after a system crash with the same log and the same log records as [ARIES](/aries-recovery/), but in a different order of work. Restart runs only log analysis, then reacquires the locks of the transactions that were active at the crash, and then opens the system to new transactions. A page is redone when a transaction first needs it, and an unfinished transaction is rolled back when a new transaction needs one of its locks. A background task does the rest. Graefe, Guy and Sauer describe it as one part of *instant recovery*, together with single-page repair and instant restore after a media failure.

## In plain words

A shop closes suddenly. Next morning, the full method is to check every shelf against the order book, and to cancel every half-done order, before the doors open. With a large shop, customers wait for hours.

The quick method first reads the order book once. It writes down which shelves need fixing and puts a "reserved" tag on each item of a half-done order. Then the doors open.

When a customer goes to a shelf that is on the list, a clerk fixes that shelf first, and the customer waits only for that shelf. When a customer wants a reserved item, the clerk first cancels the half-done order and puts its items back. In quiet moments, clerks fix the other shelves and cancel the other orders.

The customer sees the same shop as with the full method. The work is the same. Only the wait at the door is short.

## The problem

The model is the one of the [crash recovery problem](/crash-recovery/) and of ARIES: pages with a pageLSN, a buffer with the steal and no-force policies and the write-ahead rule, a forced commit record, and [strict two-phase locking](/strict-two-phase-locking/) of records. A crash loses the buffer, the lock table and the tail of the log.

After a crash, restart must give every later transaction the same view as a full restart would: the effect of the committed transactions, and none of the effect of the losers. It must stay correct when it crashes during its own run. The goal is to make the time until the first new transaction runs short, and independent of the redo and undo work.

## The algorithm

Analysis is the analysis pass of ARIES. It also builds, for each page, the list of the LSNs of its log records, the *per-page chain*. A real system links these records backward in the log itself, each record with the LSN of the previous record on the same page, as single-page repair does; the code keeps a list in memory.

```pseudo id=main
RESTART()
L1  for each record r of the stable log, from the last checkpoint, in LSN order: find the winners, the losers and undoNext[T] for each loser T
L2      if r is an update or a CLR then append r.lsn to chain[r.page]; add r.page to needRedo
L3  for each loser T, for each update u on the chain of T from undoNext[T]: give T the lock on u.key
L4  write ⟨end, T⟩ for each winner; admit new transactions                    ▷ no redo and no undo has run yet

FIX(P)                                                                        ▷ every access to page P goes through FIX
L5  if P is in needRedo then
L6      for each lsn in chain[P], in LSN order do
L7          if pageLSN(P) < lsn then apply the record lsn to P; pageLSN(P) ← lsn
L8      remove P from needRedo

LOCK(T, x)
L9  if a loser L holds the lock on x then ROLLBACK(L)
L10 take the lock on x for T, or wait if a live transaction holds it

UNDO-STEP(L)
L11 if undoNext[L] ≠ 0 then r ← the record undoNext[L]; undoNext[L] ← r.undoNextLSN if r is a CLR, else r.prevLSN
L12     if r is an update then FIX(r.page); append ⟨CLR, L, r.key, value = r.before, undoNextLSN = r.prevLSN⟩ and apply it
L13 else append ⟨end, L⟩; release the locks of L; L is no longer a loser

BACKGROUND-STEP()
L14 if needRedo is not empty then FIX(a page of needRedo)
L15 else if a loser is left then UNDO-STEP(the loser with the largest undoNext)

ROLLBACK(L)
L16 repeat UNDO-STEP(L) until L has ended
```

**Analysis (lines L1 to L4).** One pass over the log after the last checkpoint finds the losers and the pages that may need redo. Line L3 restores the locks that the losers held at the crash, from their log records. With record locks held to the end of a transaction, a loser held a lock on every record that it changed and did not yet undo. After line L4 the system runs new transactions.

**Redo on demand (lines L5 to L8).** The first fix of a page after the restart applies the records of its chain with the pageLSN test of ARIES. This is single-page redo: it reads one page and the log records of that page, and no other page.

**Undo on demand (lines L9 to L13 and L16).** A new transaction that asks for a lock of a loser rolls the loser back first, with the CLRs of ARIES. A loser that holds no lock that anyone wants waits for the background.

**Background (lines L14 and L15).** Between the actions of new transactions, the system redoes the remaining pages and rolls back the remaining losers. When nothing is left, recovery is complete. A checkpoint can then be taken as usual.

The code that goes with this page is a toy: six records on three pages, physical log records, no checkpoints, no concurrency, and a lock conflict between two live transactions simply fails. It shows the order of the work and the crash cases, not the engineering of a real system.

## Example

Pages: P1 holds a = 10 and b = 20, P2 holds c = 30 and d = 40, P3 holds e = 50 and f = 60. T1 writes a, T2 writes c and e, and T1 commits, which forces the log up to LSN 6. The buffer then writes P2 to disk (a steal: c = 31 with pageLSN 4). Then the system crashes.

| LSN | record |
|---|---|
| 1 | begin T1 |
| 2 | update T1, P1, a: 10 to 11 |
| 3 | begin T2 |
| 4 | update T2, P2, c: 30 to 31 |
| 5 | update T2, P3, e: 50 to 51 |
| 6 | commit T1 |

Analysis finds the winner T1 and the loser T2 with undoNext 5. The chains are P1: [2], P2: [4], P3: [5], so all three pages are in needRedo. Line L3 gives T2 the locks on c and e. Line L4 writes end 7 for T1, and the system opens. No data page has been read yet.

- T3 begins (8) and reads a. FIX(P1) applies LSN 2, so a = 11, the committed value. T3 writes b = 21 (9), commits (10) and ends (11). Only P1 has been redone, and T2 is still a loser.
- T4 begins (12) and wants to write c. T2 holds the lock, so line L9 rolls T2 back. UNDO-STEP finds LSN 5 and fixes P3, which applies LSN 5 (e = 51), then writes CLR 13 with e = 50 and undoNextLSN 4. The next step fixes P2. Its pageLSN is 4, so redo skips LSN 4, and CLR 14 writes c = 30 with undoNextLSN 3. The next step reaches the begin record, and end 15 releases the locks of T2.
- T4 now gets the lock on c and writes c = 32 (16).

The background has nothing left to do. The final values are a = 11, b = 21, c = 32, d = 40, e = 50 and f = 60: the same as after a full ARIES restart followed by T3 and T4.

## Correctness

**Theorem.** Assume the write-ahead rule, a forced commit record, record locks held to the end of each transaction, and that every access to a page goes through FIX and every access to a record through LOCK. Then after any number of crashes, also crashes during the instant phase or the background phase, every read of a new transaction returns the committed value of the record. When the background is done, the database holds exactly the effect of the committed transactions.

The proof has three parts. FIX gives a page that holds the whole history of the stable log on that page, by the pageLSN argument of ARIES applied to one page: before its first fix, nothing has written the page since the restart. The locks of line L3 keep new transactions away from every record that a loser still has to undo, and line L9 releases such a lock only after the loser has ended. Undo of a loser writes before images on records that no one else has changed since, so it restores the values before the loser. The [full proof](proofs/correctness.md) gives the lemmas for the model of the code.

## Complexity

The cost is counted in log records read and pages read and written, for one restart. The log is read from the last [fuzzy checkpoint](/fuzzy-checkpoint/), so a checkpoint bounds $n$.

- **Until the system opens.** Analysis reads the $n$ log records once, and line L3 walks the chains of the losers, at most $n$ records. No data page is read or written. This is the time that ARIES spends in analysis alone; ARIES then reads every dirty page and the log again for redo before undo.
- **First access to a page.** One page read and the records of its chain. A chain that is linked through the log costs one log read per record; with the log records of a page close together in a log archive or a cache, this is a few reads.
- **Total work.** Over the whole restart, each page in needRedo is read once and each record of the log is applied at most once, $O(n)$, as in ARIES. Undo writes one CLR per update of a loser and one end per loser, $O(u + m)$. The total is the same as for ARIES; only the order is different.
- **Log volume per update.** Normal processing is unchanged: one update record per change, with a before and an after image. The per-page backward link adds one LSN to each record.
- **Space.** The table of pages that need redo, the loser table and the lock table. The code also keeps the chains in memory, $O(n)$; a real system keeps them in the log.

**Heuristic.** The time to the first transaction is about the time of analysis, which a checkpoint keeps short. The response time of the first transactions is longer than normal, since each one may pay for the redo of its pages and the rollback of losers in its way. This page gives no measurement.

## Properties

- **Same log, same records.** Normal processing and the log format are those of ARIES, plus the per-page link.
- **Incremental and restartable.** Each page and each loser is recovered on its own. A crash during recovery leaves CLRs and pages that the next analysis uses, so work is not lost.
- **No change in the view.** A new transaction cannot see a page before its redo, or a record of a loser before its undo.
- **Locks reacquired from the log.** The locks of the losers come from their log records alone.

## Variants and improvements

- **Order of the background work.** Redo of the pages that the workload uses often, or rollback of the losers that hold hot locks, first.
- **Redo first, undo later.** ARIES already allows new transactions after the redo pass, while undo runs, when the locks of the losers are reacquired first. The time to open is then that of analysis and redo, which grows with the size of the buffer at the crash.
- **Instant restore.** After a media failure, the same idea restores segments of the lost device on demand from the backup and the log archive, as described in the [media recovery problem](/media-recovery/).
- **Single-page repair.** The per-page chain also repairs one damaged page during normal processing, from an older copy of the page and its log records, without a restart.

## When to use it

Use it when the time until the system accepts work after a crash matters more than the speed of the first transactions, and when the database and the buffer are large, so that a full redo pass takes long. It needs a per-page chain or another fast way to find the records of one page, and locks that can be rebuilt from the log. With a small buffer and a short log after the checkpoint, a plain [ARIES](/aries-recovery/) restart is simpler and almost as fast.

## Pitfalls

- **A page access that bypasses FIX.** A scan or a prefetch that reads a page from disk without the redo check returns an old version. Every path into the buffer must check needRedo.
- **Opening before the loser locks are set.** If a new transaction can read a record before line L3 locks it, it sees an uncommitted value of a loser.
- **Undo with a page that is not redone.** A CLR applied to a page that still needs redo gives the page a high pageLSN, so the later redo skips the older records of the page, and the page never gets them. Line L12 fixes the page first.
- **Locks coarser than records.** With page locks the losers lock whole pages, and many new transactions wait for undo. With predicate or key-range locks, the locks to rebuild must also come from the log.
- **Forgetting needRedo at a second crash.** The state of the instant phase is not in the log. The next analysis rebuilds it from the log, and pages that were redone and written back pass the pageLSN test at no cost.

## Implementations

## History

ARIES (Mohan et al., 1992) recovers in three passes over the log, analysis, redo and undo, and already lets new transactions run during the undo pass. Graefe, Guy and Sauer built instant recovery on the per-page log chains of single-page repair, in their book on instant recovery with write-ahead logging, with a second edition in 2016. Härder, Sauer, Graefe and Guy summarized single-page repair, instant restart and instant restore in Datenbank-Spektrum in 2015.

## References
