---
tag: E549PJ
kind: algorithm
slug: undo-redo-logging
name: Undo/redo logging
aliases:
- undo-redo logging
- undo logging and redo logging
area: databases/logging-and-recovery
level: core
summary: Log before and after images of each update so that recovery redoes committed work and undoes uncommitted work under any buffer policy.
solves: [crash-recovery]
model: word-ram
complexity:
  vars: {n: the log records from the oldest start record of a transaction in the checkpoint list to the end, k: the items that recovery changes, m: the transactions in the candidate set}
  time: {worst: O(n)}
  space: {extra: O(m + k)}
properties: {deterministic: true}
history:
  year: 1978
  people: [Jim Gray]
  note: "Gray's 1978 notes describe a log with undo and redo information written ahead of the data; Haerder and Reuter classified the schemes in 1983, and the record forms here follow Garcia-Molina, Ullman and Widom."
prereqs: [steal-and-force-policies, write-ahead-logging]
see_also: [aries-recovery, checkpointing, fuzzy-checkpoint, log-sequence-number, compensation-log-record, redo-log, undo-log, shadow-paging]
sources:
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson Prentice Hall, 2009
    locator: Chapter 17, Coping with System Failures, Sections 17.2 (Undo Logging), 17.3 (Redo Logging) and 17.4 (Undo/Redo Logging), the rules for each scheme and the recovery with checkpoints
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the classification of logging and buffer schemes (STEAL and FORCE) and the undo and redo actions that each scheme needs
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6 (the undo/redo algorithm and its checkpoints), chapter level only
  - paper: doi:10.1007/3-540-08755-9_9
    title: Jim Gray, Notes on data base operating systems, in Operating Systems, An Advanced Course, Lecture Notes in Computer Science 60, Springer, 1978, pages 393 to 481
    locator: the section on recovery management (the log with undo and redo information, written ahead of the data)
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: Section 4.1, Log Records (the fields of an update record and of a CLR), for the map to the ARIES fields
---

Undo/redo logging is the recovery algorithm that writes, for each update, a log record with both the old value and the new value of the item, so that after a crash it can undo the changes of transactions that did not commit and redo the changes of transactions that did. It sits between two simpler schemes: *undo logging* keeps only old values, so every changed item must reach the disk before the commit record does (the force policy), and *redo logging* keeps only new values, so no changed item may reach the disk before the commit record does (the no-steal policy). Undo/redo logging needs only the [write-ahead rule](/write-ahead-logging/), that the update record reaches the disk before the item does, so the buffer manager is free to use [steal and no-force](/steal-and-force-policies/). [ARIES](/aries-recovery/) is a refined form of the same algorithm, with a [log sequence number](/log-sequence-number/) on each page and [compensation log records](/compensation-log-record/); this page gives the plain form, as taught with the record notation of Garcia-Molina, Ullman and Widom.

## In plain words

Each time a transaction changes an item, the system first notes in a journal the item, the old value and the new value. Memory can hold the change for as long as it likes. The one rule is that a changed item goes to disk only after its note is on disk. When a transaction commits, the system writes a "done" note and waits until it is on disk.

After a crash, the disk can hold changes of unfinished transactions, and it can lack changes of finished ones. Recovery reads the journal backwards and puts back the old value of every change by an unfinished transaction. Then it reads the journal forwards and puts in the new value of every change by a finished one. Now and then the system writes all changed items to disk and marks this in the journal, so recovery can skip the older part.

## The problem

The model is the one of the [crash recovery problem](/crash-recovery/). Each item $X$ is a page with one value. The schedule is strict: a transaction that wrote $X$ holds its write lock until it ends. The buffer manager may write a dirty item to disk at any time, and commit does not write items. A crash keeps the disk and the stable part of the log and loses the buffer and the log tail.

The log holds these records, in the forms of Garcia-Molina, Ullman and Widom:

- $\langle$START $T\rangle$: transaction $T$ begins;
- $\langle T, X, v, w\rangle$: $T$ changed item $X$ from old value $v$ to new value $w$ (undo logging writes only $\langle T, X, v\rangle$, redo logging only $\langle T, X, w\rangle$);
- $\langle$COMMIT $T\rangle$ and $\langle$ABORT $T\rangle$;
- $\langle$START CKPT $(T_1, \dots, T_k)\rangle$, where $T_1, \dots, T_k$ are the active transactions, and $\langle$END CKPT$\rangle$, for a *nonquiescent* checkpoint that does not stop transactions.

Each record has an LSN, its position in the log, starting at 1; real systems often use the byte offset of the record instead. Each item on disk carries the LSN of the last record applied to it, its pageLSN, which the write-ahead rule uses. After recovery, every item must hold the value written by the last committed transaction that wrote it, or its initial value.

The records map to the fields of [ARIES](/aries-recovery/) as follows.

| record here | ARIES record | difference |
|---|---|---|
| $\langle$START $T\rangle$ | BEGIN | ARIES needs none: a prevLSN of 0 marks the first record of $T$ |
| $\langle T, X, v, w\rangle$ | UPDATE | ARIES adds the record's LSN, the prevLSN of $T$ and a location in the page; $v$ and $w$ are the before and after images |
| $\langle$COMMIT $T\rangle$, $\langle$ABORT $T\rangle$ | COMMIT, ABORT | ARIES logs each undo step as a CLR and closes $T$ with END |
| $\langle$START CKPT $(T_1, \dots, T_k)\rangle$ | BEGIN_CHECKPOINT | the list is the set of keys of the ARIES transaction table |
| $\langle$END CKPT$\rangle$ | END_CHECKPOINT | ARIES writes no pages and stores the transaction table and the dirty page table instead |

## The algorithm

Normal processing keeps, for each active transaction, the list of its update records, which it needs for an abort. In this version an abort puts back the old values in the buffer and writes no undo records, so recovery treats an aborted transaction like an unfinished one.

```pseudo id=main
WRITE(T, X, w)
L1  v ← the current value of X (the buffer copy if X is dirty, else the disk copy)
L2  append ⟨T, X, v, w⟩ to the log tail; X ← w in the buffer; pageLSN(X) ← the LSN of the record
OUTPUT(X)                                           ▷ the buffer manager calls it at any time
L3  flush the log up to pageLSN(X)                  ▷ the write-ahead rule (UR1)
L4  write X with its pageLSN to disk; X is clean
COMMIT(T)
L5  append ⟨COMMIT T⟩; flush the log up to it; report the commit
ABORT(T)
L6  for each update ⟨T, X, v, w⟩ of T, newest first, do X ← v in the buffer
L7  append ⟨ABORT T⟩                                ▷ not forced
CHECKPOINT()                                        ▷ other steps may run between L8, L9 and L10
L8  append ⟨START CKPT (T_1, ..., T_k)⟩ for the active T_i; flush the log
L9  OUTPUT every dirty item
L10 append ⟨END CKPT⟩; flush the log
RECOVER()
L11 s, L ← the LSN and the list of the START CKPT that matches the last END CKPT (s ← 0, L ← ∅ if none)
L12 U ← L ∪ {T : ⟨START T⟩ is after s}; C ← ∅; open ← L
L13 for each record r of the stable log, from the end backwards do                 ▷ undo pass
L14     if r.lsn < s and open = ∅ then stop
L15     if r = ⟨COMMIT T⟩ then add T to C
L16     else if r = ⟨START T⟩ then remove T from open
L17     else if r = ⟨T, X, v, w⟩ with T ∈ U and T ∉ C then X ← v; pageLSN(X) ← r.lsn
L18 for each record r after s, forwards do                                          ▷ redo pass
L19     if r = ⟨T, X, v, w⟩ with T ∈ C then X ← w; pageLSN(X) ← r.lsn
L20 OUTPUT every item that lines L17 and L19 changed
L21 append ⟨ABORT T⟩ for each T ∈ U ∖ C; flush the log
```

**Normal processing (lines L1 to L10).** Line L3 is the only ordering rule on the data: the record of a change is on disk before the change is. The commit record is forced so that a reported commit survives a crash; the algorithm stays consistent without the force, but then it can lose a reported commit. The checkpoint writes every item that is dirty at line L9, so every change made before the START CKPT record is on disk once the END CKPT record is.

**Undo pass (lines L11 to L17).** The candidates $U$ are the transactions that were active at the last complete checkpoint and those that started after it. Transactions that ended before the checkpoint need nothing: the checkpoint wrote their final values. The pass goes backwards from the end of the log, so it meets the commit record of a transaction before its updates, and it undoes every update of a candidate without a commit record, newest first. It reads past the checkpoint start until it has seen the start record of each transaction in the list, because those transactions can have updates before the checkpoint. An END CKPT without its START CKPT does not count: line L11 uses the last *complete* checkpoint.

**Redo pass (lines L18 and L19).** The pass goes forwards from the checkpoint start and redoes each update of a committed transaction, oldest first. Updates before the checkpoint are on disk already.

**End (lines L20 and L21).** Recovery writes the items it changed and then records the abort of each unfinished candidate. Recovery appends nothing before line L21, so a crash during recovery leaves the same stable log, and the next run computes the same values.

## Example

Items $A = 10$, $B = 20$, $C = 30$ on disk, all with pageLSN 0. The run before the crash:

| LSN | record | note |
|---|---|---|
| 1 | $\langle$START $T_1\rangle$ | |
| 2 | $\langle T_1, A, 10, 11\rangle$ | |
| 3 | $\langle$START $T_2\rangle$ | |
| 4 | $\langle T_2, B, 20, 21\rangle$ | |
| 5 | $\langle$COMMIT $T_1\rangle$ | log flushed to 5 |
| 6 | $\langle$START CKPT $(T_2)\rangle$ | log flushed to 6 |
| 7 | $\langle T_2, C, 30, 31\rangle$ | |
| 8 | $\langle$START $T_3\rangle$ | |
| 9 | $\langle T_3, A, 11, 12\rangle$ | then line L9 flushes the log to 9 and writes $A = 12$, $B = 21$, $C = 31$ |
| 10 | $\langle$END CKPT$\rangle$ | log flushed to 10 |
| 11 | $\langle$COMMIT $T_2\rangle$ | log flushed to 11 |
| 12 | $\langle T_3, B, 21, 22\rangle$ | the buffer writes $B$: log flushed to 12, $B = 22$ on disk |

Then the system crashes. The disk holds $A = 12$ and $B = 22$, both written by $T_3$, which never committed. Recovery finds the checkpoint at $s = 6$ with list $(T_2)$, so $U = \{T_2, T_3\}$.

| pass | records read | action |
|---|---|---|
| undo | 12 | $T_3$ has no commit seen: $B \leftarrow 21$ |
| undo | 11, 10 | $C = \{T_2\}$ |
| undo | 9, 8 | $T_3$: $A \leftarrow 11$ |
| undo | 7, 6, 5 | $T_2$ committed: skip LSN 7; LSN 5 adds $T_1$ to $C$, which does no harm |
| undo | 4, 3 | $T_2$ committed: skip; LSN 3 closes $T_2$, so open is empty; the pass stops before LSN 2 |
| redo | 7 to 12 | LSN 7: $C \leftarrow 31$ |
| end | | write $A$, $B$, $C$; append $\langle$ABORT $T_3\rangle$ as LSN 13 |

Recovery reads 10 records backwards and 6 forwards and writes 3 items. The result is $A = 11$, $B = 21$, $C = 31$, the values of the committed $T_1$ and $T_2$. The undo of $A$ is needed because the checkpoint itself wrote the uncommitted value 12 to disk. The redo of $C$ is not needed, since the checkpoint wrote 31, but this version has no test that would skip it. The test file builds this run and checks each number.

## Correctness

**Theorem.** Assume a strict schedule, line L3 on every write of an item, and a stable log that only grows at its end. After a crash at any point, also during RECOVER, any number of times, a RECOVER that runs to the end leaves every item with the value of the newest update on it by a transaction whose commit record is in the stable log, or with its initial value.

The proof fixes an item $X$ and splits into three cases. If a committed transaction updated $X$ after the checkpoint start, the redo pass runs last and leaves the newest such value. Otherwise, if an unfinished candidate updated $X$, the undo pass leaves the old value of the oldest such update; by strictness that old value is the last committed one, and no committed update can come later, since its writer would have had to wait for the candidate to end before the checkpoint. Otherwise recovery does not touch $X$, and the checkpoint wrote its last committed value, which nothing changed later. Recovery computes every value from the stable log alone and appends nothing before its last line, which makes a crashed recovery harmless. The full proof is in the correctness proof below.

The order of the passes matters in this version. Take $X = 1$. $T_1$ writes 2 and aborts, which puts back 1 in the buffer without a log record. $T_2$ writes 3 and commits. After a crash, undo then redo gives 3. Redo then undo gives 1: the undo of $T_1$, an unfinished candidate, comes last. The test file checks both.

## Complexity

The cost of one recovery, counted in log records and items, in the worst case:

- **Log records read.** The undo pass reads from the end of the log back to the oldest start record of a transaction in the checkpoint list, or to the checkpoint start if that is older: $n$ records. The redo pass reads the records after the checkpoint start once more, at most $n$. Each record costs $O(1)$ with hash sets, so the time is $O(n)$.
- **Items written.** Each item that recovery changes is written at least once, $k$ writes. In a system with many items per page, recovery reads and writes each touched page once, with enough buffer space.
- **Space.** The sets $U$, $C$ and open take $O(m)$, the changed items $O(k)$.

The checkpoint is what bounds $n$. Without one, both passes read the whole log. With one, the work depends only on the log since the checkpoint start and on the active transactions at the checkpoint, not on the age of the database. In the test with 40 committed transactions of 3 updates each and a checkpoint before the last two transactions, recovery reads 13 records instead of 410 (a measurement of the implementation). A long-running transaction in the list pulls the undo pass back to its start record; this is the main reason to keep transactions short.

## Properties

- **Any buffer policy.** Steal and no-force are both allowed. Undo logging needs force and redo logging needs no-steal.
- **Idempotent.** The records hold values, not operations, so applying a record twice gives the same result, and recovery can run again after a crash without extra bookkeeping.
- **Restartable.** A crash during recovery is followed by a normal recovery.
- **Nonquiescent checkpoints.** Transactions keep running during a checkpoint, but the checkpoint writes every dirty item.
- **Bounded log growth.** Recovery appends one abort record per unfinished candidate, so repeated crashes during recovery add little to the log. ARIES gets the same bound with undo steps that it does log, as compensation log records.

## Variants and improvements

- **The two simpler schemes.** Each keeps only one value per update and pays for it with a buffer rule. Undo logging writes the items of $T$ before $\langle$COMMIT $T\rangle$ and recovers with one backward pass. Redo logging writes $\langle$COMMIT $T\rangle$ before any item of $T$ and recovers with one forward pass over committed transactions.
- **Quiescent checkpoint.** Stop new transactions, wait for the active ones to end, write all dirty items, and write one CKPT record. Recovery then never reads past it, but the system stalls.
- **pageLSN test.** With the pageLSN on disk, redo can skip a record whose LSN is at most the item's pageLSN. This turns the redo of $C$ in the example into a skip, and it is what allows [logical logging](/logical-logging/), where a record cannot be applied twice.
- **ARIES.** [ARIES](/aries-recovery/) adds a prevLSN chain, logs undo steps as [compensation log records](/compensation-log-record/), redoes every update before it undoes (repeating history), and replaces the checkpoint's page writes with a copy of the dirty page table ([fuzzy checkpoint](/fuzzy-checkpoint/)). This supports record-level locking inside a page and [partial rollback](/savepoint/).
- **Group commit.** Several commit records share one log flush; see [group commit](/group-commit/).

## When to use it

Use undo/redo logging when items are updated in place, the buffer manager must be free to write any item, and commit should cost one sequential log write. It is the right model to learn first: it shows why both kinds of information are needed under steal and no-force, and what each buffer rule buys. A real system with many records per page, record locks and operations that are not idempotent uses ARIES. A main-memory system that never writes uncommitted data needs only redo logging. [Shadow paging](/shadow-paging/) avoids the undo information by never writing in place.

## Pitfalls

- **Treat an abort record as the end.** If a stolen value of $T$ reached the disk before $T$ aborted, and the rollback was done only in the buffer, the disk still holds it after a crash. Unless rollbacks are logged, undo aborted transactions in recovery. The test file builds this case.
- **Redo before undo, with unlogged rollbacks.** See the example under Correctness.
- **Stop the undo pass at the checkpoint start.** A transaction in the list can have updates before the checkpoint, and the checkpoint may have written them. Read back to its start record.
- **Use an incomplete checkpoint.** A START CKPT without a matching END CKPT does not promise that the earlier changes are on disk. Use the START CKPT of the last END CKPT.
- **Break the write-ahead rule.** If an item reaches the disk before its update record, a crash can leave a value of an unfinished transaction with no record to undo it. The test file builds this case too.
- **Undo in the wrong order.** Undo newest first. If one transaction wrote $X$ twice, undo oldest first leaves the middle value.

## Implementations

## History

Jim Gray's 1978 notes on data base operating systems describe a log that holds undo and redo information and is written ahead of the data. Haerder and Reuter (1983) classified recovery schemes by their buffer policies (steal or not, force or not) and by the log information each needs, which is where undo/redo logging appears as the scheme for steal and no-force. Bernstein, Hadzilacos and Goodman (1987) gave the undo/redo algorithm with its checkpoints as one of four recovery algorithms. Garcia-Molina, Ullman and Widom present undo logging, redo logging and undo/redo logging in this order, with the record forms used on this page. ARIES (1992) is the refined form that most systems follow.

## References
