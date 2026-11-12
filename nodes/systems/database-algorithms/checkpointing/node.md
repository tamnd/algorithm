---
tag: 3HY3MZ
kind: technique
slug: checkpointing
name: Checkpointing
aliases:
- database checkpoint
- transaction-consistent checkpoint
area: systems/database-algorithms
level: core
summary: "Write a marker and recovery tables to the log, and name it in a master record, so that restart after a crash reads only a bounded tail of the log."
prereqs: [write-ahead-logging]
see_also: [aries-recovery, crash-recovery, steal-and-force-policies, shadow-paging, group-commit, log-compaction, chandy-lamport-snapshot, global-snapshot]
sources:
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the section on checkpoint schemes (transaction-oriented, transaction-consistent, action-consistent and fuzzy checkpoints) and their effect on the redo and undo work at restart
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the section on checkpoints during normal processing (begin_chkpt and end_chkpt records, the master record) and the analysis pass of restart
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, the section on checkpointing (fuzzy checkpoints and the master record)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, the discussion of checkpointing for the undo/redo algorithm (commit-consistent, cache-consistent and fuzzy checkpointing), chapter level only
---

A *checkpoint* is a record in the [write-ahead log](/write-ahead-logging/), together with a pointer to it in a *master record* at a fixed place on disk, that tells [crash recovery](/crash-recovery/) where it can start. Without checkpoints a restart must read the log from its first record, and the log must be kept for ever. A checkpoint bounds both: redo starts at a point the checkpoint gives, and undo needs only the records of transactions that were active at it. The choices differ in what the system must do while the checkpoint is taken. A *consistent* checkpoint stops all transactions and writes all dirty pages. A *fuzzy* checkpoint stops nothing and writes no page: it records the tables that say what is not yet on disk.

## In plain words

A database keeps a journal of every change. After a crash it reads the journal to fix the disk. If it always read from the first page of the journal, a restart would take longer every day.

So the system now and then writes a bookmark. The simple bookmark waits until no work is in progress, saves every changed page, and then writes "all is safe up to here". Restart begins at the bookmark. But all work stops while the pages are saved.

The fuzzy bookmark saves no pages. It only writes two lists: the work in progress, and the pages that are changed in memory but not yet saved, each with the place in the journal where its oldest unsaved change is. Restart begins at the oldest of these places. Work never stops.

## When it applies

- The system recovers with a log ([write-ahead logging](/write-ahead-logging/)), and the log or the restart time must be bounded.
- Under a no-force policy, committed changes can be missing from the disk at the crash, so redo needs a point before which every committed change is on disk. Under steal, undo needs a point before which no active transaction wrote.
- Log space must be reused: records before the redo point of the last checkpoint and before the first record of every active transaction are not needed for crash recovery (they can still be needed for media recovery).

## The template

```pseudo id=main
FUZZY-CHECKPOINT()
L1  b ← APPEND(⟨begin_checkpoint⟩)
L2  att ← a copy of the transaction table (each active T with its lastLSN); dpt ← a copy of the dirty page table (each dirty page with its recLSN)
L3  e ← APPEND(⟨end_checkpoint, att, dpt⟩)
L4  force the log up to e
L5  write b into the master record                         ▷ one atomic block write
CONSISTENT-CHECKPOINT()
L6  stop new transactions and wait until no transaction is active
L7  write every dirty page in the buffer to disk
L8  c ← APPEND(⟨checkpoint⟩); force the log up to c
L9  write c into the master record; let transactions start again
RESTART()
L10 start ← the LSN in the master record; read the log forward from start and rebuild the tables
L11 redo from min(recLSN in the rebuilt dirty page table)      ▷ at or after start for a consistent checkpoint
L12 undo each loser by following its chain back from its lastLSN, past start if it began earlier
```

**Why it bounds redo.** A page that is not in the dirty page table at the end_checkpoint record has every logged change on disk. A page in it has every change before its recLSN on disk. Pages that become dirty after the checkpoint get their first change after the begin record. So every change missing from the disk at a crash is at or after $\min(\text{recLSN}, \text{start})$, and line L11 starts there. For a consistent checkpoint the table is empty at the checkpoint, so redo starts at the checkpoint record.

**Why it bounds undo.** At a consistent checkpoint no transaction is active, so every loser began after it. At a fuzzy checkpoint the copied transaction table names each active transaction with its last LSN, and the prevLSN chain leads back from there to its first record. Undo reads back to the oldest first record of a loser, which a long transaction can push far back.

**Why the master record comes last.** Line L5 is after the force of line L4, so the master record never names a checkpoint whose end record is not on disk. A crash between lines L1 and L5 leaves the master record at the previous checkpoint, which is still correct, only older.

**Costs.** A consistent checkpoint makes the system unavailable for the time to drain the active transactions and to write the whole buffer, which for a large buffer is many seconds. A fuzzy checkpoint costs two log records and one block write, and its redo point depends on how old the oldest dirty page is. Systems therefore write dirty pages in the background, oldest recLSN first, so that the redo point keeps moving; this is a separate process from the checkpoint itself.

## Classic examples

**A redo point before the checkpoint.** Items $a = 10$ and $b = 20$. The log: LSN 1 $w_1(a, 11)$, LSN 2 $c_1$ (forced), LSN 3 begin_checkpoint, LSN 4 end_checkpoint with ATT $= \{\}$ and DPT $= \{a: 1\}$; the master record is set to 3. The page of $a$ is still in memory when the system crashes. Restart reads from LSN 3, finds DPT $= \{a: 1\}$, and redoes from LSN 1: $a = 11$. A restart that began redo at the checkpoint would leave $a = 10$ and lose a committed write.

**A consistent checkpoint.** After 29 committed transactions the system quiesces, writes every dirty page, and writes the checkpoint record. One more transaction writes and commits. Restart reads three records: the checkpoint, the update and the commit. Nothing before the checkpoint is read.

**Checkpoint kinds of Haerder and Reuter (1983).**

| kind | what is on disk at the checkpoint | waits for | restart starts |
|---|---|---|---|
| transaction-oriented | every page of a transaction, at its commit (this is force) | each commit | no redo needed |
| transaction-consistent | all dirty pages, with no transaction active | all active transactions to end | at the checkpoint, no undo before it |
| action-consistent | all dirty pages, with no update in progress | the running actions only | redo at the checkpoint, undo may go back further |
| fuzzy | no pages; the tables of dirty pages and active transactions | nothing | redo at the smallest recLSN |

## Variations

- **Action-consistent (sharp) checkpoint.** Block new updates, write all dirty pages and the list of active transactions, then let updates go on. Redo starts at the checkpoint, but undo still goes back for transactions that were active.
- **Fuzzy checkpoint with gathering.** Real systems copy the tables between the begin and end records while transactions run. Restart then merges the copied tables with the records it reads after the begin record, as in the analysis pass of [ARIES](/aries-recovery/).
- **Two-checkpoint rule.** Some systems write the dirty pages that were already dirty at the previous checkpoint, so that redo never starts before the previous checkpoint. BHG describe a scheme of this kind under the name fuzzy checkpointing.
- **Snapshot checkpoints.** Main-memory databases and many key-value stores write a full copy of the data, made consistent with copy on write or a multiversion read, and then drop the log before it. Redis's RDB file and the [log compaction](/log-compaction/) of a replicated log work in this way.
- **Shadow paging.** [Shadow paging](/shadow-paging/) makes every commit a checkpoint of the whole page table.
- **Distributed snapshots.** The [Chandy-Lamport snapshot](/chandy-lamport-snapshot/) and other [global snapshot](/global-snapshot/) algorithms record a consistent cut of a distributed computation with channel messages. They share the aim of a restart point, but they record process states and messages, not dirty pages and log positions, and they do not stop the processes.

## Pitfalls

- **Starting redo at the checkpoint.** A page that was dirty at a fuzzy checkpoint can hold a committed change from long before it. Redo must start at the smallest recLSN of the dirty page table, which line L11 does.
- **Setting the master record before the force.** If the master record names a begin record whose end record was lost with the log tail, restart has no tables. Force first (line L4), then write the master record (line L5).
- **Truncating the log too early.** Log records before the redo point can be dropped only if no active transaction needs them for undo and media recovery does not need them.
- **A long transaction.** A transaction that stays active across many checkpoints keeps its first record, and all after it, alive. Systems warn about it or abort it.
- **A dirty page that is never written.** A hot page that stays in the buffer keeps its recLSN, and the redo point does not move. Background writing must also write hot pages.

## Exercises

1. In the first classic example, the page of $a$ is written to disk after the end_checkpoint record and before the crash. Which records does redo apply now?
2. Show a log where a transaction-consistent checkpoint and a fuzzy checkpoint at the same position give different redo start points.
3. A system writes the master record before it forces the log. Give a crash that makes restart wrong.
4. With an action-consistent checkpoint, which records before the checkpoint can undo still read? Give an example.
5. A transaction updates the same page every second for an hour, and fuzzy checkpoints are taken every minute. How far back does redo go if the page is never written? If it is written once a minute?

## References
