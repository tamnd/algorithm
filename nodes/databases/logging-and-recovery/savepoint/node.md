---
tag: 0JQNYQ
kind: definition
slug: savepoint
name: Savepoint
aliases:
- partial rollback
area: databases/logging-and-recovery
level: core
summary: A named point inside a transaction to which it can roll back, undoing later updates while keeping the earlier ones.
prereqs: [log-sequence-number, compensation-log-record]
see_also: [nested-transactions, aries-recovery, compensation-log-record, checkpointing, transaction, strict-two-phase-locking, acid-properties]
sources:
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: Section 5.2, Total or Partial Rollbacks (SaveLSN, a savepoint before each SQL statement in DB2, one CLR per undone record, Figure 3, and the release of locks after a partial rollback)
  - url: https://www.postgresql.org/docs/current/sql-savepoint.html
    title: PostgreSQL documentation, SAVEPOINT
    locator: the description and the compatibility notes on savepoints with the same name
  - url: https://www.postgresql.org/docs/current/sql-rollback-to.html
    title: PostgreSQL documentation, ROLLBACK TO SAVEPOINT
    locator: the description (later savepoints are destroyed, the named one stays)
  - url: https://www.postgresql.org/docs/current/sql-release-savepoint.html
    title: PostgreSQL documentation, RELEASE SAVEPOINT
    locator: the description (the savepoint is removed and the changes after it are kept)
---

A *savepoint* is a named point inside a [transaction](/transaction/) to which the transaction can roll back, undoing the updates made after the savepoint and keeping the ones made before it while the transaction stays active; this is called a *partial rollback*. In a log-based system a savepoint is just the [LSN](/log-sequence-number/) of the transaction's newest log record at the time it is set, and a partial rollback is the usual rollback with [compensation log records](/compensation-log-record/) that stops at that LSN. A savepoint is not a [checkpoint](/checkpointing/): a checkpoint is taken by the system for all transactions to make restart shorter, and [ARIES recovery](/aries-recovery/) after a crash still rolls back every unfinished transaction completely, whatever savepoints it had. A savepoint is also a flat, sequential form of [nested transactions](/nested-transactions/): it can undo a suffix of the work, but the part after it is not a separate transaction with its own commit.

## Definition

Let $T$ be an active transaction, and let $\text{last}(T)$ be the LSN of its newest log record, or 0 if it has none.

**Setting a savepoint.** Setting savepoint $S$ stores $\text{save}(S) = \text{last}(T)$ in the memory of $T$. ARIES calls this value the *SaveLSN*. Nothing is written to the log.

**Rollback to $S$.** Let $n$ be the head of $T$'s undo chain: the next record to undo. Repeat while $n > \text{save}(S)$:

- if record $n$ is an update, undo it, write a CLR with undoNextLSN equal to the update's prevLSN, and set $n$ to that prevLSN;
- if record $n$ is a CLR, set $n$ to its undoNextLSN.

Then $T$ goes on as an active transaction. A total rollback is the case $\text{save}(S) = 0$, followed by an END record.

**What the rollback keeps.** After the rollback, the updates of $T$ that are in effect are exactly the uncompensated updates with LSN at most $\text{save}(S)$, the ones in effect when $S$ was set. The proof is the chain argument of the [CLR](/compensation-log-record/) page: the walk meets the uncompensated updates newest first, and the loop stops before the first one at or before $\text{save}(S)$.

**Several savepoints.** Savepoints of one transaction form a stack ordered by their LSNs. Rolling back to $S$ makes every savepoint set after $S$ invalid, because the work it marked is gone, and keeps $S$ itself, so that the transaction can roll back to $S$ again. Releasing $S$ removes $S$ and the savepoints after it, and keeps all updates. PostgreSQL behaves in this way. In the SQL standard a new savepoint with the name of an old one replaces it; PostgreSQL keeps the old one, and the name then refers to the newer one until it is released.

**Locks.** A partial rollback undoes data changes but does not by itself undo lock requests. ARIES Section 5.2 reports that DB2 keeps all locks after a partial rollback, while System R releases locks after it. Keeping them is always safe under [strict two-phase locking](/strict-two-phase-locking/), since the locks are released at the end of the transaction in any case.

## Examples and non-examples

**A rollback to a savepoint, and a later abort.** $T$ writes $u_1$, sets savepoint $S$, writes $u_2$ and $u_3$, and rolls back to $S$. So $\text{save}(S) = 1$.

| LSN | record | prevLSN | undoNextLSN |
|---|---|---|---|
| 1 | update $u_1$ | 0 | |
| 2 | update $u_2$ | 1 | |
| 3 | update $u_3$ | 2 | |
| 4 | CLR for $u_3$ | 3 | 2 |
| 5 | CLR for $u_2$ | 4 | 1 |
| 6 | update $u_4$ | 5 | |

The rollback starts at $n = 3$, writes CLR 4 and sets $n = 2$, writes CLR 5 and sets $n = 1$, and stops because $1 \le 1$. $T$ then writes $u_4$, whose prevLSN is the CLR 5. If $T$ now aborts, it undoes $u_4$ (CLR 7, undoNextLSN 5), jumps from CLR 5 to LSN 1, undoes $u_1$ (CLR 8, undoNextLSN 0) and ends. It does not undo $u_2$ or $u_3$ a second time.

**Statement atomicity.** An SQL statement that changes many rows must have no effect if it fails half way, for example on a unique-key violation at the 500th row. DB2 sets a savepoint before each SQL statement that changes data, and on an error rolls back to it, so the transaction loses only that statement. ARIES Section 5.2 describes this use.

**A retry in application code.** In PostgreSQL:

```sql
BEGIN;
INSERT INTO orders VALUES (1, 'book');
SAVEPOINT before_stock;
UPDATE stock SET n = n - 1 WHERE item = 'book';
ROLLBACK TO SAVEPOINT before_stock;
UPDATE stock SET n = n - 1 WHERE item = 'pen';
COMMIT;
```

The commit keeps the insert and the second update. The first update has no effect.

**Non-example: a checkpoint.** A [checkpoint](/checkpointing/) writes the system's tables to the log and is not visible to transactions. No transaction can roll back to it.

**Non-example: a crash.** Savepoints are kept in memory. After a crash, restart rolls back each unfinished transaction totally; it does not stop at the transaction's newest savepoint.

**Non-example: a nested subtransaction.** In the [nested transaction](/nested-transactions/) model a child can run in parallel with its siblings, commits to its parent, and can hold its own locks. The work after a savepoint has none of these; it is part of the one transaction, and only the order of the log records separates it.

## Related definitions

- A [compensation log record](/compensation-log-record/) is written for each update that a partial rollback undoes.
- A [log sequence number](/log-sequence-number/) is the value that a savepoint stores.
- [ARIES recovery](/aries-recovery/) was designed with partial rollback as a goal, and its restart treats the CLRs of a partial rollback like any other CLRs.
- [Nested transactions](/nested-transactions/) generalize savepoints to a tree of subtransactions.
- [Atomicity](/acid-properties/) is the property that a total rollback gives, and statement atomicity is the same property for one statement, given by a savepoint.

## References
