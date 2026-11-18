---
tag: 7Q7BG3
kind: algorithm
slug: multi-level-recovery
name: Multi-level transaction recovery
aliases:
- multilevel transactions
area: databases/logging-and-recovery
level: advanced
summary: Recover transactions whose operations release low-level locks early by undoing completed subtransactions with logical inverse operations.
solves: [crash-recovery]
model: word-ram
complexity:
  vars: {n: the records in the stable log, u: the completed operations of the losers that are not yet compensated, c: the level 0 updates of one operation, m: the number of losers}
  time: {worst: O(n + u (c + log m) + c m)}
  space: {extra: O(m)}
properties: {deterministic: true}
history:
  year: 1991
  people: [Gerhard Weikum, David Lomet]
  note: Weikum described recovery for transactions built of levels of operations in ACM TODS in 1991; Lomet gave the MLR method at SIGMOD 1992.
prereqs: [aries-recovery, compensation-log-record, logical-logging]
see_also: [nested-transactions, open-nested-transactions, escrow-transactional-method, sagas, savepoint, physiological-logging, crash-recovery, steal-and-force-policies]
sources:
  - paper: doi:10.1145/103140.103145
    title: Gerhard Weikum, Principles and realization strategies of multilevel transaction management, ACM Transactions on Database Systems 16(1), 1991, pages 132 to 180
    locator: the model of transactions as levels of operations, the recovery by inverse operations of completed subtransactions, and the measurements on the UDS system, paper level
  - paper: doi:10.1145/141484.130314
    title: David B. Lomet, MLR, a recovery method for multi-level systems, Proceedings of ACM SIGMOD 1992, ACM SIGMOD Record 21(2), pages 185 to 194
    locator: Section 2.1 (high level compensation), Section 4.3 (undoing completed subtransactions) and Section 5 (MLR rollback), with the level 0 pass and the level 1 pass of restart
  - paper: doi:10.1145/128765.128770
    title: C. Mohan, Don Haderle, Bruce Lindsay, Hamid Pirahesh and Peter Schwarz, ARIES, a transaction recovery method supporting fine-granularity locking and partial rollbacks using write-ahead logging, ACM Transactions on Database Systems 17(1), 1992, pages 94 to 162
    locator: the sections on logical undo and nested top actions, paper level
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: the chapters on transactions with object operations and their crash recovery, chapter level only
---

Multi-level transaction recovery restores a database after a crash when transactions are built from operations at two or more levels, and each high-level operation releases its low-level locks as soon as it ends, long before its transaction commits. Physical undo by before images is then wrong: another transaction may already have changed the same page or record. The method undoes an operation that is still running at the low level, with before images, and undoes an operation that has completed at the high level, by running its logical inverse as a new operation. It extends [ARIES](/aries-recovery/), which has the same pageLSN redo and [compensation log records](/compensation-log-record/), and it is the recovery side of the transaction model whose concurrency side is [open nesting](/open-nested-transactions/).

## In plain words

A bank keeps a counter for each branch and one for the grand total. Adding money to a branch is one small job: change the branch counter, then change the total. While the job runs, it holds those two counters. When the job ends, it lets them go, even though the customer has not yet confirmed.

So two customers can add money to the same branch, one after the other, before either confirms. If the first one now cancels, you cannot put back the old number that the counter had before his deposit. That would also wipe out the second deposit. You must subtract his amount instead.

After a crash, recovery does two repairs. A small job that was cut in half is put back exactly, with the old numbers, because nobody else touched what it held. A small job that ended is taken back with its opposite job.

## The problem

The model is the one of the [crash recovery problem](/crash-recovery/) and of ARIES: pages with a pageLSN, a buffer with the steal and no-force policies and the write-ahead rule, and a commit that forces the log. On top of it, a transaction is a sequence of level 1 operations, and each level 1 operation is a short subtransaction of level 0 page writes.

- *Level 0 locks* are on the records that one operation writes. The operation holds them until it ends, so at level 0 each operation is strict.
- *Level 1 locks* are on the abstract objects that the operations change. Two operations conflict at level 1 only if they do not commute. A transaction holds its level 1 locks to its end.
- Each completed operation has an *inverse*: an operation that removes its effect from any state that later commuting operations may have reached.

The running example is the one of the code: counters, an operation ADD(x, d) that writes x and then the total t, and the inverse ADD(x, -d). Two ADDs always commute, so there are no level 1 locks at all, and two transactions can increase the same counter before either commits.

Recovery must leave every counter with its initial value plus the changes of the committed transactions. It must stay correct when it crashes during its own run.

## The algorithm

The log holds ARIES records plus two record types at level 1. An *op_commit* record ends an operation: it holds the inverse operation and *opPrev*, the lastLSN of the transaction before the operation began. A *comp_commit* record ends a compensation, the run of an inverse: it holds the LSN of the op_commit that it compensates and an undoNextLSN equal to that op_commit's opPrev. Level 0 updates and level 0 CLRs are the ARIES records.

```pseudo id=main
RESTART()
L1  for each record r of the stable log, in LSN order do                          ▷ analysis
L2      if r is commit then mark r.T a winner; if r is end then forget r.T
L3      otherwise lastLSN[r.T] ← r.lsn; undoNext[r.T] ← r.undoNextLSN if r is a CLR or a comp_commit, else r.lsn
L4  write ⟨end, T⟩ for each winner T; the transactions that are left are the losers
L5  for each update or CLR r of the log, in LSN order do                           ▷ redo: repeat history at level 0
L6      if pageLSN(r.page) < r.lsn then write r.after into the page; pageLSN(r.page) ← r.lsn
L7  for each loser T do                                                             ▷ level 0 pass
L8      while the record u named by undoNext[T] is an update or a CLR do
L9          if u is a CLR then undoNext[T] ← u.undoNextLSN
L10         else append ⟨CLR, T, u.page, u.key, value = u.before, undoNextLSN = u.prevLSN⟩; write u.before; undoNext[T] ← u.prevLSN
L11 while a loser is left do                                                        ▷ level 1 pass
L12     T ← the loser with the largest undoNext[T]; r ← the record undoNext[T]
L13     if r is op_commit then run the inverse r.inverse as a new level 0 operation of T
L14         append ⟨comp_commit, T, undone = r.lsn, undoNextLSN = r.opPrev⟩; undoNext[T] ← r.opPrev
L15     else if r is comp_commit then undoNext[T] ← r.undoNextLSN
L16     else if r is abort then undoNext[T] ← r.prevLSN
L17     else append ⟨end, T⟩ and remove T                                           ▷ r is the begin record of T
L18 force the log

ADD(T, x, d)                                                                        ▷ one level 1 operation in normal work
L19 p ← lastLSN[T]; take the level 0 lock on x, then on t, when each write needs it
L20 append ⟨update, T, x, before, before + d⟩ and apply it; then the same for t
L21 append ⟨op_commit, T, inverse = ADD(x, -d), opPrev = p⟩; release the level 0 locks
```

**Analysis and redo (lines L1 to L6)** are those of ARIES without a checkpoint: they find the losers, each with the head of its chain, and repeat history at level 0, losers included. After redo every page holds the effect of the whole stable log.

**The level 0 pass (lines L7 to L10)** finishes level 0. A loser can have at most one operation that did not reach its op_commit: an operation of normal work, or a compensation that a crash cut off. Its level 0 updates sit at the head of the chain. The pass undoes them with before images and CLRs, as ARIES does. This is safe because the operation still held its level 0 locks at the crash, so no other transaction wrote those records after it. The pass stops at the first record that is not a level 0 record: an op_commit, a comp_commit, an abort or a begin. Now every page is *operation consistent*: it holds the effect of completed operations only.

**The level 1 pass (lines L11 to L17)** undoes the completed operations of the losers, newest first. For an op_commit it runs the inverse as a new operation with its own level 0 updates (line L13), and then writes a comp_commit whose undoNextLSN skips the compensated operation (line L14). A comp_commit at the head means that the compensation is already done, so line L15 jumps over it. A later crash during a compensation leaves level 0 updates without a comp_commit: the next restart undoes them in the level 0 pass, finds the op_commit at the head again, and runs the compensation again from the start.

**Normal rollback** of an aborted transaction writes an abort record and runs lines L12 to L17 for that transaction alone, with the same level 0 locks as any operation.

## Example

Pages: P0 holds t = 100, P1 holds a = 10 and b = 20, P2 holds c = 30 and d = 40. T1 runs ADD(a, 5). The buffer writes P1 to disk (a steal), and the write-ahead rule forces the log first. T2 then runs ADD(a, 7) on the same counter and commits. T3 starts ADD(c, 4), writes c, and P2 goes to disk. Then the system crashes.

| LSN | record | note |
|---|---|---|
| 1 | begin T1 | |
| 2 | update T1, P1, a: 10 to 15 | P1 on disk with pageLSN 2 |
| 3 | update T1, P0, t: 100 to 105 | |
| 4 | op_commit T1, inverse ADD(a, -5), opPrev 1 | T1 releases its locks on a and t |
| 5 to 8 | begin T2, a: 15 to 22, t: 105 to 112, op_commit T2 | T2 works on a before T1 ends |
| 9, 10 | commit T2, end T2 | the log is forced to 9 |
| 11 | begin T3 | |
| 12 | update T3, P2, c: 30 to 34 | P2 on disk with pageLSN 12 |

Analysis finds the losers T1 (undoNext 4) and T3 (undoNext 12). Redo applies LSNs 3 and 7 to P0 (pageLSN 0) and LSN 6 to P1 (pageLSN 2), and skips LSNs 2 and 12, which the disk pages already hold. Now a = 22, t = 112 and c = 34.

The level 0 pass meets the update 12 of T3 and writes CLR 13 (c := 30, undoNextLSN 11). The chain of T3 is now at its begin record, and the chain of T1 is at the op_commit 4, so the pass stops. The level 1 pass takes T3 first (undoNext 11 is larger than 4) and writes end 14. For T1 it runs ADD(a, -5): update 15 (a: 22 to 17), update 16 (t: 112 to 107), and comp_commit 17 with undoNextLSN 1. Then end 18.

The result is a = 17, b = 20, c = 30, d = 40 and t = 107: the initial values plus the committed +7 of T2, and t is again the sum of the four counters. Physical undo of T1 would write the before images of LSNs 3 and 2, t = 100 and a = 10, and lose the committed work of T2.

## Correctness

**Theorem.** Assume the write-ahead rule, a forced commit record, level 0 locks held to the end of each operation, level 1 operations of concurrent transactions that commute (or level 1 locks held to commit for those that do not), and inverses that undo an operation from any state that commuting operations reach. Then after any number of crashes, also crashes during restart, a restart that runs to the end leaves each counter at its initial value plus the changes of the transactions whose commit record is in the stable log. No completed operation is compensated twice.

The proof has four steps. Redo repeats history, by the pageLSN argument of ARIES, so the state after redo is the effect of every level 0 record in the stable log. The stable log is a prefix of the log, so each CLR of the level 0 pass comes before any later write of the same record, and its before image is the right value; after the pass, the state is the effect of the completed operations and completed compensations only. The chain of a transaction, read through opPrev and the undoNextLSN of each comp_commit, visits exactly its completed operations that have no comp_commit, newest first. Each compensation then removes the effect of one such operation, because the inverse undoes it in the presence of commuting operations of other transactions. The [full proof](proofs/correctness.md) gives the lemmas for the model of the code.

## Complexity

The cost is counted in log records and page operations for one restart. In the implementation the log has no checkpoint, so analysis and redo read the whole stable log, $n$ records, and redo reads each page at most once. With the [fuzzy checkpoint](/fuzzy-checkpoint/) of ARIES, analysis starts at the last checkpoint and redo at the smallest recLSN, so only the log after those points is read.

- **Level 0 pass.** Each loser has at most one cut-off operation, so the pass writes at most $c$ CLRs per loser, $c m$ in total.
- **Level 1 pass.** Each of the $u$ completed operations costs one compensation: $c$ level 0 updates and one comp_commit, so the pass writes $u(c + 1)$ records and $m$ end records. Choosing the largest undoNext with a heap costs $O(\log m)$ per step.
- **Log volume per update.** In normal work each level 0 write logs a before and an after image, and each operation adds one op_commit that holds its inverse. The inverse is small: a key and a delta.
- **Repeated crashes.** A compensation that a crash cuts off is undone and run again, so each crash during the level 1 pass can add up to $2c$ records. ARIES has a bound on the total growth over all crashes; this method has a bound per crash.

The space is $O(m)$ for the transaction table.

## Properties

- **Early release of low-level locks.** A transaction holds a page or record lock only for the length of one operation, which is the point of the method for hot items such as counters and index pages.
- **Logical undo, physical redo.** Redo stays page-oriented and exact with the pageLSN test; only undo of completed operations is logical.
- **Restartable.** A comp_commit in the stable log removes its operation from the chain, so a crash never makes a completed compensation run again. A compensation without its comp_commit is undone at level 0 and run again.
- **One code path.** Normal rollback and restart use the same level 1 step, as ARIES uses one UNDO-STEP.

## Variants and improvements

- **More levels.** With levels of records, pages and files, each level runs one pass, from the lowest level up, and each pass leaves the state consistent at the next level.
- **Nested top actions of ARIES.** ARIES gets the same effect for structure changes such as B-tree page splits: the split is logged, then closed by a dummy CLR whose undoNextLSN jumps over it, so rollback never undoes the split physically. The undo of the inserted key is a logical inverse.
- **Escrow and counters.** The [escrow transactional method](/escrow-transactional-method/) uses the same commutativity of increments, with checks on bounds.
- **Long-running transactions.** [Sagas](/sagas/) push the idea to whole transactions: each step commits, and a failure runs compensating steps. Sagas give up isolation between steps; level 1 locks keep it here.

## When to use it

Use it when short low-level locks matter, for example on index pages, free-space maps and counters that many transactions update, and when each high-level operation has a cheap inverse. Plain [ARIES](/aries-recovery/) with record locks held to commit is simpler when operations do not need to release their locks early. The method needs a correct inverse for every operation, which is easy for increments and for inserts and deletes of keys, and harder for operations whose inverse depends on data that the operation destroyed.

## Pitfalls

- **Physical undo of a completed operation.** Line L13 must run the inverse. Before images of a completed operation can overwrite later changes of other transactions, as the example shows.
- **Logical undo of a cut-off operation.** The inverse of a whole ADD applied to an operation that wrote x but not yet t would also subtract from t. Cut-off operations must be undone at level 0, in lines L7 to L10, before any level 1 step.
- **The order of the passes.** The level 1 pass must start only after the level 0 pass has ended for every loser. An inverse that runs on a state that still holds half an operation acts on a state that no serial execution reaches.
- **The undoNextLSN of a comp_commit.** It must be the opPrev of the compensated operation, not the prevLSN of the comp_commit. Otherwise the next restart finds the op_commit again and compensates it twice.
- **Inverses that do not commute.** If two operations on the same object do not commute, the transaction must keep its level 1 lock to commit. Without it, the inverse is not correct.

## Implementations

## History

Weikum (ACM TODS 1991) described transactions as levels of operations, with locks per level and recovery by inverse operations of completed subtransactions, and measured an implementation on the Codasyl database system UDS. Lomet (SIGMOD 1992) gave MLR, a method that pairs the commit of each subtransaction with a log record for its parent, logs each compensation as a transaction with its own commit, and recovers with a level 0 pass after ARIES-style redo, then a pass at the next level. The nested top actions of ARIES (Mohan et al. 1992) give the same early release for structure changes inside one system.

## References
