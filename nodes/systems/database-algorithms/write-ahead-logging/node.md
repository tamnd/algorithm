---
tag: MBX83W
kind: technique
slug: write-ahead-logging
name: Write-ahead logging
aliases:
- WAL
- write-ahead log protocol
- WAL rule
area: systems/database-algorithms
level: core
summary: "Log each change to stable storage before the page it changes (the WAL rule), and log all of a transaction before its commit returns (the commit rule). Recovery then redoes and undoes."
prereqs: [crash-recovery, steal-and-force-policies]
see_also: [aries-recovery, checkpointing, group-commit, shadow-paging, redo-log, undo-log, log-structured-merge-tree, two-phase-commit]
sources:
  - paper: doi:10.1007/3-540-08755-9_9
    title: Jim Gray, Notes on data base operating systems, in Operating Systems, An Advanced Course, Lecture Notes in Computer Science 60, Springer, 1978, pages 393 to 481
    locator: the section on recovery management, the write-ahead log protocol (log records are written before the changed objects, and the commit record is forced)
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the WAL principle and its relation to the STEAL and FORCE policies
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the LSN and the page_LSN, and the use of the page_LSN to decide whether a change is on the page
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 9, Log Manager, and Chapter 10, Transaction Manager Concepts (chapter level only)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, Crash Recovery (the log, the WAL protocol and the LSNs)
---

Write-ahead logging (WAL) is the technique that lets a database update pages in place and still solve the [crash recovery problem](/crash-recovery/). Each change is first described by a record in an append-only log, and two rules order the writes to stable storage: the *WAL rule* says that the log record of a change reaches stable storage before the changed page does, and the *commit rule* says that all log records of a transaction, with its commit record, reach stable storage before the commit is reported. Under these rules a crash at any moment leaves enough in the log to undo the changes of unfinished transactions and to redo the changes of committed ones. Jim Gray's 1978 notes state the protocol, and it is the base of [ARIES](/aries-recovery/) and of most database and file system recovery today.

## In plain words

Before you change a page of the database, you write a note in a journal that says which page, what was there, and what will be there. The journal only grows at its end, which is fast. The page itself can wait in memory and go to disk much later.

Two rules keep this safe. A changed page may go to disk only after its note is on disk. Then, if the transaction never finishes, the note tells you what to put back. A transaction may be reported as done only after all its notes, and a final "done" note, are on disk. Then, if the changed pages never reach the disk, the notes tell you what to write again.

After a crash, you repeat every noted change that is not on its page, then take back the changes of transactions with no "done" note.

## When it applies

- The data lives in pages that the system changes in place, in a buffer pool, and writes back later. This is the normal case for B-tree and heap files.
- The buffer manager uses *steal* (it may write a page with uncommitted changes) or *no-force* (it does not write all changed pages at commit), or both. See [steal and force](/steal-and-force-policies/). Steal makes undo records necessary, and no-force makes redo records necessary.
- Commits must be cheap. A commit costs one sequential write at the end of the log instead of random writes of every changed page.
- The stable store writes one page atomically and keeps writes to the log in order. If it does not, the design needs extra steps (see the pitfalls).

## The template

Each log record has a *log sequence number* (LSN) that grows along the log; in practice it is the byte offset of the record. Each page stores the LSN of the last record whose change it holds, the *pageLSN*. The log has a stable part on disk and a tail in memory, and FLUSH-LOG$(n)$ writes the tail up to LSN $n$, in order. An update record holds the transaction, the item, the *before image* and the *after image*. The holes of the template are the record format (here, physical images of one item per page) and the recovery passes, which [ARIES](/aries-recovery/) refines.

```pseudo id=main
UPDATE(T, x, v)
L1  p ← FETCH(x)                                ▷ into the buffer pool
L2  r ← APPEND(⟨update, T, x, before = p.value, after = v⟩)
L3  p.value ← v;  p.pageLSN ← r.lsn

FLUSH-PAGE(p)                                   ▷ at any time: steal and no-force
L4  FLUSH-LOG(p.pageLSN)                        ▷ the WAL rule
L5  write p to its place on disk

COMMIT(T)
L6  r ← APPEND(⟨commit, T⟩)
L7  FLUSH-LOG(r.lsn)                            ▷ the commit rule
L8  report the commit to the client

RECOVER()                                       ▷ on restart, from the stable log
L9  for each update record r, in LSN order do               ▷ redo: repeat history
L10     if pageLSN(r.x) < r.lsn then set r.x to r.after, pageLSN(r.x) ← r.lsn
L11 W ← the transactions with an update record and no commit or abort record
L12 for each update record r of a member of W, in reverse LSN order do: set r.x to r.before
L13 write the changed pages to disk; then append ⟨abort, T⟩ for each T ∈ W and flush the log
```

An abort during normal work undoes the transaction's updates, newest first, by calling UPDATE with each before image, so that the undo is logged too, and then appends an abort record. Line L10 is the *pageLSN test*: a record is applied only when the page does not hold it yet. It makes redo idempotent even when a record is not (for example "add 30"), and it lets a page that was written after the record skip it. Line L13 writes the abort records only after the undone pages are on disk: if a crash comes earlier, the next recovery sees the same losers and undoes them again, which gives the same values.

**Why it works.** Take the model of the [crash recovery problem](/crash-recovery/): a strict history, one item per page, and $C$ the transactions whose commit record is in the stable log $R$ at the crash. Then RECOVER ends with each item $x$ equal to $\mathrm{last}_C(x)$.

1. *$R$ is a prefix of the log.* FLUSH-LOG moves the first records of the tail, in order. So if a record is in $R$, every earlier record is in $R$.
2. *Each committed change is in $R$.* The updates of $T \in C$ come before its commit record, which is in $R$, so by step 1 they are in $R$.
3. *The disk is explained by $R$.* By line L4, a page reaches the disk only after the record named by its pageLSN is in $R$. So for each $x$, the disk holds the after image of the record $\mathrm{pageLSN}(x) \in R$, or the initial value when the pageLSN is 0, and later records of $x$ have larger LSNs.
4. *After redo, $x$ holds the after image of the last record of $x$ in $R$.* Lines L9 and L10 apply, in LSN order, every record of $x$ in $R$ with an LSN above the disk's pageLSN, and by step 3 the records below it are already reflected.
5. *Undo gives $\mathrm{last}_C(x)$.* By strictness the records of $x$ in the log form blocks, one transaction per block, and the end record (commit or abort) of each block's transaction comes before the next block. By step 1 every block of $x$ in $R$ but the last belongs to a transaction that ended in $R$. A committed block leaves $x$ at its last write. An aborted block ends with its logged undo, so it leaves $x$ as it was before the block. Only the last block can belong to a loser, and line L12 restores the before image of its first record, the value before that block. So $x$ ends at the last write of a committed transaction, or at its initial value.

The commit rule (line L7) makes each reported commit a member of $C$. A full proof for the refined algorithm, with checkpoints and compensation records, is on the [ARIES](/aries-recovery/) page.

**Cost.** Each update appends one record. Each commit makes one synchronous log write, which [group commit](/group-commit/) can share among many transactions. A page write may wait for a log write. Recovery reads the whole stable log, $O(|R|)$ records, and writes each changed page once; [checkpointing](/checkpointing/) bounds the part of the log that must be read.

**Example.** Start with $A = 100$ and $B = 50$ on disk, pageLSN 0. Run $w_1(A, 70)$, $w_2(B, 80)$, $c_2$, then the buffer steals page $A$, then the system crashes.

| step | log record | stable log after the step | disk after the step |
|---|---|---|---|
| $w_1(A, 70)$ | 1: update $T_1$, $A$, 100 to 70 | empty | $A = 100$, $B = 50$ |
| $w_2(B, 80)$ | 2: update $T_2$, $B$, 50 to 80 | empty | same |
| $c_2$ | 3: commit $T_2$ | 1, 2, 3 (forced by L7) | same |
| flush page $A$ | none | 1, 2, 3 (L4 has nothing to do) | $A = 70$ (pageLSN 1), $B = 50$ |
| crash | | 1, 2, 3 | $A = 70$, $B = 50$ |

Redo: record 1 is skipped, since pageLSN$(A) = 1$; record 2 sets $B = 80$ with pageLSN 2. The losers are $W = \{T_1\}$. Undo sets $A = 100$. The final state is $A = 100$, $B = 80$, and the log gains the record ⟨abort, $T_1$⟩.

## Classic examples

- [ARIES](/aries-recovery/) is write-ahead logging with an analysis pass, redo from the oldest dirty page, and undo that logs compensation records, so that recovery and rollback are restartable with bounded log growth.
- [Checkpointing](/checkpointing/) adds records that tell recovery where it may start reading the log.
- [Group commit](/group-commit/) meets the commit rule for many transactions with one log write.
- [Two-phase commit](/two-phase-commit/) forces a prepare record at each participant before it votes yes, the same rule applied to the vote.
- A [log-structured merge tree](/log-structured-merge-tree/) keeps its newest data in memory and protects it with a write-ahead log that is replayed after a crash.
- Software [transactional memory](/transaction/) uses an in-memory [redo log](/redo-log/) or [undo log](/undo-log/) with the same before and after images, but nothing is on stable storage, so there are no WAL or commit rules and no crash recovery.

## Variations

- **Undo-only log.** With steal and force, records need only before images, and the commit record is written after the forced pages.
- **Redo-only log.** With no-steal and no-force, records need only after images, and there is no undo pass. Main-memory database systems often work this way.
- **Physical, logical and physiological records.** A physical record holds byte images of a page part. A logical record holds an operation, such as "insert key 7 into the index", which is small but cannot be applied twice. ARIES uses physiological records: physical to one page, logical inside the page. The pageLSN test of line L10 is what makes non-idempotent records safe to redo.
- **Full-page images.** The first change of a page after a checkpoint can log the whole page, so that recovery can repair a page that a crash left half written. PostgreSQL does this.
- **Log archiving and media recovery.** Keep old log segments with a backup copy, and redo them over the copy after a disk loss.

## Pitfalls

- **Writing the page before its log record.** Skipping line L4 lets an uncommitted value reach the disk with no before image anywhere. After a crash it stays, and atomicity fails. The fix is to flush the log up to the pageLSN first.
- **Reporting the commit before the log write.** If line L8 runs before line L7 finishes, a crash can lose a transaction that the client was told had committed.
- **Redo without the pageLSN test.** Applying every record in line L10 is correct only for idempotent physical images. For logical records it applies a change twice.
- **Logging the end of recovery too early.** If the abort records of line L13 are durable before the undone pages, a crash in between leaves loser values on disk with nothing to say they must be undone. ARIES avoids the problem by logging each undo step as a compensation record.
- **Gaps in the stable log.** If log blocks are written in parallel and a later block reaches the disk before an earlier one, the stable log is not a prefix, and step 1 of the proof fails. Recovery must stop at the first gap, and the system must not report commits past it.
- **Volatile disk caches.** A drive that reports a write as done while the data is still in its own volatile cache breaks both rules. The log write must use a barrier or a cache flush.

## Exercises

1. Under steal and force, which fields of the update record can be dropped, and where must the commit record go relative to the forced pages? Give a crash that shows the order matters.
2. A system logs "add $d$ to $x$" records and has no pageLSN. Give a crash and a run of RECOVER that leaves $x$ wrong. Then show that the pageLSN test fixes it.
3. Change line L13 to write the abort records before the pages. Give a history and two crashes (one during recovery) that end in a wrong state.
4. Prove that the number of log records read by RECOVER is the length of the stable log, and give a history in which every record must be read by any recovery that uses only the stable log and the disk.

## References
