---
tag: EF79FV
kind: algorithm
slug: fuzzy-checkpoint
name: Fuzzy checkpoint
aliases:
- fuzzy checkpointing
area: databases/logging-and-recovery
level: core
summary: A checkpoint that records the dirty pages and active transactions without stopping new updates or forcing pages to disk.
solves: [crash-recovery]
model: word-ram
complexity:
  vars: {m: the entries of the transaction table, d: the entries of the dirty page table, n: the log records from the begin_checkpoint record to the end of the log}
  time: {worst: O(n + m + d)}
  space: {extra: O(m + d)}
properties: {deterministic: true}
history:
  year: 1992
  people: [C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh, Peter Schwarz]
  note: "ARIES gave the form with a transaction table, a dirty page table with recLSNs and a master record; Haerder and Reuter had already named fuzzy checkpoints in their 1983 survey."
prereqs: [checkpointing, log-sequence-number]
see_also: [aries-recovery, undo-redo-logging, compensation-log-record, write-ahead-logging, buffer-pool, steal-and-force-policies, global-snapshot]
sources:
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: Section 4.4, Dirty_Pages Table (the recLSN), Section 5.4, Checkpoints (begin_chkpt and end_chkpt, the dirty pages table gathered a little at a time, no pages forced, the master record), and Section 6.1, Analysis Pass (the merge at end_chkpt, the redo start)
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the section on checkpoint schemes, among them fuzzy checkpoints
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, the section on checkpointing (fuzzy checkpoints and the master record) and the analysis phase
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, the discussion of checkpointing for the undo/redo algorithm (fuzzy checkpointing), chapter level only
---

A fuzzy checkpoint is a [checkpoint](/checkpointing/) that writes the transaction table and the dirty page table to the log without writing any data page and without stopping transactions. Restart then starts its scan at the checkpoint, and starts redo at the oldest recLSN in the dirty page table, which can be older than the checkpoint. The [checkpointing](/checkpointing/) page gives the general technique and compares the kinds of checkpoint, and [ARIES recovery](/aries-recovery/) gives the full restart, with tables copied in one step; this page is about the checkpoint itself when the two tables are copied at different moments while transactions keep running, and about the merge rule that the analysis pass needs then. The nonquiescent checkpoint of [undo/redo logging](/undo-redo-logging/) is a different scheme: it does not stop transactions either, but it writes every dirty item.

## In plain words

A database keeps a journal of changes and a list of the pages in memory that are newer than their disk copies. For each such page it remembers the place in the journal of its oldest change not yet on disk. A checkpoint is a bookmark in the journal that saves this list and the list of running transactions, so that after a crash the system can skip the old part of the journal.

The fuzzy kind writes no pages and does not wait. It writes a "begin" mark, copies the two lists while work goes on, perhaps one now and one a little later, and then writes an "end" mark with the copies. Because the copies were made at different moments, restart reads the journal from the "begin" mark and uses what it reads there to fix the copies.

## The problem

The model is the one of [ARIES](/aries-recovery/). Each page has a pageLSN, the [log sequence number](/log-sequence-number/) of its last change. The buffer manager uses steal and no-force and obeys the WAL rule: before it writes a page, it flushes the log up to the page's pageLSN. A commit is forced. A rollback writes [compensation log records](/compensation-log-record/). Normal processing keeps two tables in memory:

- the transaction table (ATT): for each transaction that has begun and not ended, its status, its lastLSN and its undoNext, the next update to undo;
- the dirty page table (DPT): for each page whose buffer copy differs from the disk, its recLSN, the LSN of the first change since the page was last written.

A checkpoint must let restart rebuild both tables as they were at the crash, after reading only the log from the checkpoint on. It may not write data pages, and it may not stop other transactions. Copying a large table takes time, so the system may copy the ATT and the DPT at different moments, and transactions may begin, change pages, commit and end between the copies.

## The algorithm

```pseudo id=main
FUZZY-CHECKPOINT()                                      ▷ other steps may run between the lines
L1  b ← APPEND(⟨BEGIN_CHECKPOINT⟩)
L2  att ← a copy of the ATT (status, lastLSN, undoNext of each transaction)
L3  dpt ← a copy of the DPT (recLSN of each dirty page)              ▷ before or after L2, but after L1
L4  e ← APPEND(⟨END_CHECKPOINT, att, dpt⟩)
L5  flush the log up to e
L6  master ← b                                                       ▷ one atomic write of a block
ANALYSIS()
L7  start ← master, or 1 if there is none; ATT ← ∅; DPT ← ∅; ended ← ∅
L8  for each record r of the stable log with r.lsn ≥ start, in LSN order do
L9      if r belongs to a transaction T and is not END then ATT[T].lastLSN ← r.lsn; set undoNext and status from r
L10     if r is UPDATE or CLR and r.page ∉ DPT then DPT[r.page] ← r.lsn
L11     if r is END then remove T from the ATT; add T to ended
L12     if r is END_CHECKPOINT then
L13         for each (T, entry) in r.att with T ∉ ATT and T ∉ ended do ATT[T] ← entry
L14         for each (P, recLSN) in r.dpt do DPT[P] ← min(DPT[P], recLSN)         ▷ recLSN if P ∉ DPT
L15 for each committed T in the ATT do append ⟨END, T⟩ and remove T
L16 redoLSN ← the smallest recLSN in the DPT (the end of the log if it is empty)
RECOVER()
L17 ANALYSIS(); redo from redoLSN with the pageLSN test, as in ARIES
L18 undo the transactions left in the ATT, largest undoNext first, writing CLRs
L19 flush the log
```

**The checkpoint (lines L1 to L6).** It costs two log records, one log flush and one write of the master record, plus the time to copy the tables. Both copies come after the begin record. The master record is written only after the end record is on disk, so it never names a checkpoint whose tables were lost.

**The scan (lines L8 to L11).** Analysis reads every record from the begin record on. Each record of a transaction sets the transaction's entry: an update makes itself the head of the chain, a CLR moves the head to its undoNextLSN, an abort leaves the head at its prevLSN, and a commit marks the transaction committed. The first update or CLR of a page puts the page in the DPT with that LSN.

**The merge (lines L12 to L14).** The copies describe the state at two moments between the begin and end records. The scan has already seen every record after the begin record, so it knows more than the copies about every transaction and page that it has met. Line L13 adds from the copy only the transactions that the scan has not met and that have not ended since the begin record. Line L14 adds the copied pages and keeps the smaller recLSN for a page that is in both. A transaction whose records are all before the begin record, and a page whose oldest missing change is before it, come only from the copies.

**Redo and undo (lines L15 to L19).** These are the passes of [ARIES](/aries-recovery/). Redo can start before the checkpoint, at the oldest recLSN. Undo can go back past the checkpoint, along the chain of a transaction that began before it. The flush at the end puts the END records of recovery on disk before new work begins.

## Example

Pages $P = 10$, $Q = 20$, $R = 30$, all with pageLSN 0. Locks are held until END.

| LSN | record | prevLSN | note |
|---|---|---|---|
| 1 | BEGIN $T_1$ | 0 | |
| 2 | UPDATE $T_1$, $P$: 10 to 11 | 1 | DPT: $P$ 2 |
| 3 | BEGIN $T_2$ | 0 | |
| 4 | UPDATE $T_2$, $Q$: 20 to 21 | 3 | DPT: $Q$ 4 |
| 5 | BEGIN_CHECKPOINT | | then the ATT is copied: $T_1$ (active, 2, 2), $T_2$ (active, 4, 4) |
| 6 | COMMIT $T_1$ | 2 | log flushed to 6 |
| 7 | END $T_1$ | 6 | |
| 8 | UPDATE $T_2$, $R$: 30 to 31 | 4 | DPT: $R$ 8; then $P$ is written to disk (11, pageLSN 2) and the DPT is copied: $Q$ 4, $R$ 8 |
| 9 | END_CHECKPOINT with both copies | | log flushed to 9; master $\leftarrow 5$ |
| 10 | BEGIN $T_3$ | 0 | |
| 11 | UPDATE $T_3$, $P$: 11 to 12 | 10 | DPT: $P$ 11 |
| 12 | COMMIT $T_2$ | 8 | log flushed to 12 |

The END record of $T_2$ is still in the log tail when the system crashes. The disk holds $P = 11$ (pageLSN 2), $Q = 20$ and $R = 30$ (pageLSN 0). Analysis starts at LSN 5.

| LSN read | ATT | DPT | note |
|---|---|---|---|
| 5 | | | |
| 6 | $T_1$ committed | | |
| 7 | | | ended $= \{T_1\}$ |
| 8 | $T_2$ (active, 8, 8) | $R$ 8 | |
| 9 | same | $Q$ 4, $R$ 8 | $T_1$ is in the copy but has ended: not added; $T_2$ is known; $Q$ comes from the copy |
| 10, 11 | $T_2$, $T_3$ (active, 11, 11) | $Q$ 4, $R$ 8, $P$ 11 | |
| 12 | $T_2$ committed | same | line L15 then appends END $T_2$ as LSN 13 |

Redo starts at LSN 4, before the checkpoint. It reads 9 records and the 3 pages, and applies LSN 4 ($Q = 21$), LSN 8 ($R = 31$) and LSN 11 ($P = 12$). Undo rolls back $T_3$: CLR at LSN 14 sets $P = 11$ with undoNextLSN 0, and END $T_3$ is LSN 15. The result is $P = 11$, $Q = 21$, $R = 31$, the writes of the committed $T_1$ and $T_2$.

Three wrong choices give wrong results on this run. Without the ended set, line L13 takes $T_1$ back from the copy as an active loser, and undo puts $P = 10$, which removes a committed write. If redo started at the begin record, LSN 4 would be skipped and $Q$ would stay 20. And the DPT copy does not hold $P$, because $P$ was written just before the copy; the scan finds $P$ again at LSN 11. The test file builds this run and the wrong variants.

## Correctness

**Theorem.** Assume the WAL rule, a forced commit, strict page locks held until END, and lines L2 and L3 run after line L1 and before line L4. After a crash at any point, also during recovery, any number of times, the DPT that analysis builds holds every page with a logged change missing from the disk, with a recLSN at most that change's LSN, and the ATT holds exactly the transactions with a record in the stable log and no END record, each with its exact lastLSN, undoNext and status. So recovery with the redo and undo passes of ARIES gives the result of the [crash recovery problem](/crash-recovery/).

The proof has two parts. For the DPT, a missing change at or after the begin record is read by the scan, and the minimum at line L14 never raises a value. A missing change before the begin record was missing at the moment of the DPT copy too, since that copy came after the begin record, so the copy held its page with a recLSN at most that change. For the ATT, a transaction with a record after the begin record gets its entry from its last record, which the scan reads. A transaction with all its records before the begin record and no END was active at the ATT copy, which came after the begin record, so the copy is exact for it. A transaction that ended after the begin record is in the ended set and is not added back. The full proof is in the correctness proof below. It also shows that the ARIES rule, which replaces the recLSN with the copied value instead of taking the minimum, is correct: if a change on the page after the begin record is older than the copied recLSN, the page was written after that change. The tests crash after every step of seeded workloads, and after steps of recovery, and check the final state with both rules.

## Complexity

All bounds are worst case and are proved by counting the steps of the pseudocode.

- **The checkpoint** appends two records, flushes the log once and writes the master record once. Copying the tables takes $O(m + d)$ time and the end record has size $O(m + d)$. It writes no data page.
- **Analysis** reads the $n$ records from the begin record to the end, $O(1)$ each with hash tables, plus $O(m + d)$ for the merge.
- **Redo** reads the log from the smallest recLSN, and it reads each page in the DPT once.
- **Undo** reads the records of the losers, back to the oldest first record of a loser.

So the checkpoint bounds analysis by the log since the checkpoint, but it bounds redo only through the oldest recLSN, and undo only through the oldest loser. In the test with 50 committed transactions, all pages written every 10 transactions, and one transaction still active at the crash, analysis reads 3 records with the checkpoint and 203 without it, and redo reads 4 records with the checkpoint and 202 without it, since without the copied DPT analysis cannot know that the pages were written (a measurement of the implementation).

## Properties

- **No page writes.** The checkpoint never writes a data page, so it does not compete with transactions for the disk.
- **No waiting.** Transactions run during the whole checkpoint. The only short pauses are those needed to copy each table consistently.
- **Restartable.** A crash during the checkpoint leaves the master record at the previous complete checkpoint.
- **Exact tables.** After analysis, the tables are those of a full scan of the log, for the transactions, and cover all missing changes, for the pages.
- **Depends on page writing.** The redo start moves forward only as pages are written. A page that stays dirty keeps an old recLSN and holds back the redo start.

## Variants and improvements

- **Tables copied in one step.** The simplest version copies both tables when it builds the end record. Then the merge does not need the ended set, but the copy must be made while no table changes.
- **ARIES.** ARIES copies the dirty page table a little at a time, and replaces the recLSN with the copied value at the end_checkpoint record. ARIES also notes that a restart without an analysis pass could start redo at the smaller of the begin record and the smallest recLSN in the end record.
- **Background page writing.** Writing the pages with the oldest recLSN, also hot pages, moves the redo start forward. It is separate from the checkpoint but sets the value of each checkpoint.
- **Consistent and two-checkpoint schemes.** The [checkpointing](/checkpointing/) page describes checkpoints that write dirty pages, which make redo start at the checkpoint or at the one before.
- **Snapshots in distributed systems.** A [global snapshot](/global-snapshot/) also records a state without stopping the processes, but it records process states and messages, not log positions.

## When to use it

Use a fuzzy checkpoint in a disk-based system with steal and no-force and a large buffer pool, where writing all dirty pages at once would stall transactions for seconds. It needs pageLSNs and a recovery that can start redo before the checkpoint, as ARIES does. A system without a DPT, such as the plain [undo/redo logging](/undo-redo-logging/) on this site, must write the dirty pages instead. A main-memory system that writes snapshots does not need a DPT at all.

## Pitfalls

- **Re-adding an ended transaction.** If the ATT copy is older than the end record, a transaction can commit and end in between. Without the ended set it comes back as a loser and its committed work is undone.
- **Copying before the begin record.** A page dirtied between the copy and the begin record is in neither the copy nor the scan, and its change is lost if the page was not written. The same holds for a transaction that wrote between the copy and the begin record.
- **Redo from the begin record.** A page in the DPT copy can hold an old missing change. Start at the smallest recLSN.
- **The master record before the flush.** If the end record is lost with the log tail, the master names a checkpoint without tables.
- **Not flushing at the end of recovery.** If the END records written by recovery are lost and a later checkpoint is taken, a loser with all its records before that checkpoint is in neither the copy nor the scan.
- **Hot pages.** A page that is changed all the time is never clean, so its recLSN stays old and every checkpoint keeps the same redo start. ARIES asks that such pages also be written reasonably often.

## Implementations

## History

Haerder and Reuter (1983) listed fuzzy checkpoints among the checkpoint schemes of their survey. Mohan, Haderle, Lindsay, Pirahesh and Schwarz (1992) gave the form used in ARIES and in most later systems: begin and end records, the transaction table and the dirty page table with recLSNs in the end record, the master record written after the end record is on disk, and no pages written by the checkpoint. They allow the dirty page table to be gathered a little at a time, which is the case this page studies. Ramakrishnan and Gehrke present this form in their chapter on crash recovery.

## References
