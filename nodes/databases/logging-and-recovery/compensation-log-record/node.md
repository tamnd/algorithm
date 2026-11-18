---
tag: 2XEK6A
kind: definition
slug: compensation-log-record
name: Compensation log record
aliases:
- CLR
area: databases/logging-and-recovery
level: core
summary: A redo-only log record written when an update is undone, which points to the next record to undo so rollback is never repeated.
prereqs: [log-sequence-number, aries-recovery]
see_also: [savepoint, undo-redo-logging, logical-logging, fuzzy-checkpoint, write-ahead-logging, undo-log, crash-recovery]
sources:
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: Section 4.1, Log Records (CLRs hold only redo information, UndoNxtLSN), Section 5.2, Total or Partial Rollbacks (one CLR per undone record, Figure 3), and Section 11 (the log growth of other methods during repeated restart failures)
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 18, Crash Recovery (compensation log records and the undo phase)
---

A *compensation log record* (CLR) is the log record that a database writes when it undoes one update of a transaction. It holds the change that the undo made, as redo information only, and a pointer, the *undoNextLSN*, to the next record of the transaction that is still to be undone, so that a later rollback skips every update that an earlier, interrupted rollback already undid. A CLR is redone after a crash but never undone; it is a part of [ARIES recovery](/aries-recovery/) that the plain [undo/redo logging](/undo-redo-logging/) algorithm does not have, and [savepoints](/savepoint/) use it for partial rollback. Unlike a [checkpoint](/checkpointing/) record, which copies the system's tables to make restart shorter, a CLR belongs to one transaction and describes one change to one page.

## Definition

Let $u$ be an update record of transaction $T$, with page $P$, location $\ell$ in the page, before image $v$ and prevLSN $p$. When $T$ undoes $u$, during an abort, a partial rollback or the undo pass of restart, it appends a CLR $c$ with these fields:

| field | value |
|---|---|
| LSN | the next LSN of the log |
| type | CLR |
| txn id | $T$ |
| prevLSN | the lastLSN of $T$, its newest record before $c$ |
| page id, location | the page and place that the undo changed, usually $P$ and $\ell$ |
| after image | the value that the undo wrote, usually $v$ |
| undoNextLSN | $p$, the prevLSN of $u$ |

It then applies the change to the page and sets the pageLSN of the page to $\text{lsn}(c)$, as for any change. The undo of $u$ and the writing of $c$ follow the WAL rule like an update: the page with the undo goes to disk only after $c$ is stable.

The CLR has no before image, because it is never undone. To roll back $T$, start at its newest record and repeat: if the record is an update, undo it and write a CLR; if it is a CLR, jump to its undoNextLSN; stop at LSN 0 (or, for a partial rollback, at the savepoint's LSN). Since each CLR points past the update it undid, the updates met on this walk are exactly those that no CLR has undone, newest first. The [ARIES](/aries-recovery/) page proves this as its chain lemma.

If the undo is *logical*, the CLR can name a different page than $u$. For example, after a B-tree page split moved the key that $u$ inserted, the undo deletes the key from its new page, and the CLR names that page. This is why a CLR records the undo action itself and not just a reference to $u$.

## Examples and non-examples

**An interrupted rollback.** Transaction $T$ writes updates $u_1$, $u_2$, $u_3$ (LSNs 1, 2, 3, with prevLSNs 0, 1, 2) and then aborts.

| LSN | record | prevLSN | undoNextLSN |
|---|---|---|---|
| 1 | update $u_1$ | 0 | |
| 2 | update $u_2$ | 1 | |
| 3 | update $u_3$ | 2 | |
| 4 | abort | 3 | |
| 5 | CLR for $u_3$ | 4 | 2 |
| 6 | CLR for $u_2$ | 5 | 1 |

The system crashes after LSN 6 is stable. Restart redoes LSNs 1 to 6, which puts the pages in their state at the crash: $u_3$ and $u_2$ undone, $u_1$ in place. The undo pass starts at LSN 6, a CLR, so it jumps to its undoNextLSN, 1, undoes $u_1$, writes CLR 7 with undoNextLSN 0, and ends $T$. Whatever the number of crashes during this rollback, $T$ gets at most three CLRs, one per update.

**The same run without CLRs.** Suppose the undo of $u_3$ and $u_2$ had been logged as ordinary update records $w_3$ and $w_2$ of $T$, with before and after images. After the crash, $T$ is a loser with five updates, $u_1, u_2, u_3, w_3, w_2$, and restart undoes all five, newest first: it first takes back the undo $w_2$, putting back $u_2$'s value, then $w_3$, then $u_3$, $u_2$, $u_1$. The final state is right, but the work and the log grow with every crash during rollback. Section 11 of the ARIES paper reports that in methods where such records are undone, the log written during repeated failures of restart can grow exponentially in the worst case, while in other methods it grows linearly; with CLRs it is bounded by one CLR per update.

**A partial rollback.** A [savepoint](/savepoint/) records the LSN $s$ of the transaction's newest record when the savepoint was set. Rollback to it writes CLRs for the updates after $s$, newest first, and stops when the next record to undo is at or before $s$; the last CLR has undoNextLSN equal to the prevLSN of the oldest undone update, which is at most $s$. The transaction then goes on, and its later records chain back through the CLRs, so a later full rollback skips the undone part.

**Non-example: an undo record.** In an [undo log](/undo-log/) or in undo logging, the record $\langle T, X, v\rangle$ is written *before* the change and holds the old value so that the change can be undone. A CLR is written *after* an undo and describes the undo.

**Non-example: the abort record.** It marks the start of a rollback, changes no page, and carries no undoNextLSN.

**Non-example: a CLR that is undone.** A record that restart undoes like an update is not a CLR, even if it describes an undo. Undoing it puts the original change back for a moment, as the second example shows.

## Related definitions

- The [log sequence number](/log-sequence-number/) page defines prevLSN and undoNextLSN, and the pageLSN that a CLR sets.
- [ARIES recovery](/aries-recovery/) redoes CLRs in its redo pass and follows their undoNextLSN in its undo pass.
- A *dummy CLR* in ARIES ends a nested top action, such as a page split that must survive the rollback of its transaction: its undoNextLSN points before the action, so the undo pass jumps over it.
- A [savepoint](/savepoint/) is the main user of partial rollback with CLRs.
- [Logical logging](/logical-logging/) is the case where the CLR's undo action differs from the inverse of a byte change.
- The [fuzzy checkpoint](/fuzzy-checkpoint/) copies each transaction's undoNext, which a CLR sets.

## References
