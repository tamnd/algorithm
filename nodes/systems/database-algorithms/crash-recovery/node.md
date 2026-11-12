---
tag: 9QT0TX
kind: problem
slug: crash-recovery
name: Crash recovery problem
aliases:
- database recovery
- transaction recovery after a crash
- restart recovery
area: systems/database-algorithms
level: core
summary: "After a crash that loses main memory but keeps the disk, bring the database to the state that holds the effects of exactly the committed transactions."
prereqs: [acid-properties]
see_also: [write-ahead-logging, steal-and-force-policies, aries-recovery, shadow-paging, checkpointing, group-commit, two-phase-commit, log-structured-merge-tree]
sources:
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the failure types (transaction, system and media failure), the recovery actions (transaction undo, global undo, partial redo, global redo) and the taxonomy of logging and propagation strategies
  - paper: doi:10.1007/3-540-08755-9_9
    title: Jim Gray, Notes on data base operating systems, in Operating Systems, An Advanced Course, Lecture Notes in Computer Science 60, Springer, 1978, pages 393 to 481
    locator: the section on recovery management (the model of failures, the log, undo and redo, and the write-ahead log protocol)
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6, Centralized Recovery (the failure model, the requirements of a recovery manager, idempotence of restart)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 12, Crash Recovery, Notion of Correctness
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 16 (atomicity and durability) and Chapter 18, Crash Recovery
---

The crash recovery problem asks how a database system, after a crash that erases its main memory but keeps its disk, can bring the data on disk to a state that holds the effects of exactly the committed transactions. It is the problem behind two of the [ACID properties](/acid-properties/): atomicity (an unfinished transaction leaves no trace) and durability (a committed transaction is not lost). Every solution keeps redundant information on stable storage, almost always a log, and uses two kinds of repair: *undo* removes changes of transactions that did not commit, and *redo* puts back changes of committed transactions that did not reach the disk.

## In plain words

A database keeps its tables on disk, but it changes them in a memory cache, because the disk is slow. It writes changed pages back to the disk later, at times that suit it. Now the power fails. The memory is gone. The disk may hold some changes of a transaction that was still running, and it may miss some changes of a transaction that the system already reported as done.

When the machine starts again, the system must repair the disk before any new work starts. Each change of an unfinished transaction must go away, and each change of a finished transaction must be there. So, before the crash, it must have written enough notes to the disk to do this repair alone. The repair can itself be cut short by a second crash, so it must also be safe to start again.

## Definition

**Storage model.** The database is a set of items (pages or records) $X$. A *state* is a map $D : X \to V$. There are three kinds of storage:

- *Volatile storage* (main memory) holds the buffer pool and other tables. A crash erases it.
- *Stable storage* holds the database state $D_{\text{disk}}$ and, in most designs, a log. A crash does not change it. A write of one page to stable storage is atomic: after a crash the page holds the old or the new contents, never a mix.
- An *archive* (a backup copy and an archived log) survives the loss of the disk. Only media recovery uses it.

**Transactions.** A history is a sequence of actions $w_i(x, v)$ (transaction $T_i$ sets item $x$ to value $v$), $c_i$ (commit) and $a_i$ (abort), plus reads, which do not change the state. We assume the history is *strict*: no transaction reads or overwrites an item that another transaction wrote until that writer commits or aborts. The usual way to get this is [strict two-phase locking](/strict-two-phase-locking/). The system also chooses, at each moment, which buffered pages to write to the disk; this choice is the buffer policy of [steal and force](/steal-and-force-policies/).

**Commit point.** Each transaction that commits does so at one atomic event on stable storage, its *commit point*. In a log-based system the commit point is the moment the commit record reaches the stable log. In [shadow paging](/shadow-paging/) it is the write of the root pointer. The system may report the commit to the client only after the commit point.

**Failure.** A *system crash* is an event at an arbitrary moment that erases volatile storage and keeps stable storage. A *transaction failure* is an abort of one transaction, by the program or by the system (for example to break a [deadlock](/deadlock/)). A *media failure* destroys stable storage, and recovery then starts from the archive.

**The problem.** Let $C$ be the set of transactions whose commit point came before the crash. For each item $x$, let $\mathrm{last}_C(x)$ be the value of the last write of $x$ in the history by a transaction in $C$, or the initial value of $x$ if there is no such write. A *recovery procedure* reads stable storage after a crash and writes it, and it must end with

$$D_{\text{disk}}(x) = \mathrm{last}_C(x) \quad \text{for every } x \in X.$$

Strictness makes $\mathrm{last}_C$ the state of a serial run of the transactions of $C$ in commit order. Two more conditions make a procedure usable:

- **Restartable.** A crash can happen during recovery. If recovery is stopped at any step and run again from the start on the stable state it left, the result must still satisfy the equation. A procedure in which a step has the same effect when it is applied once or many times (it is *idempotent*) is the usual way to get this.
- **Every reported commit is in $C$.** A transaction whose commit the system reported must have its commit point before the crash. A transaction that was not reported may be in $C$ or not, depending on where the crash came.

**Two repairs.** Let $L$ be the set of transactions that started but are not in $C$ (the *losers*). Recovery must

- *undo*: for each $x$ whose disk value was written by a loser, restore the value before the loser's first write of $x$;
- *redo*: for each $x$ whose last write by a member of $C$ is not on the disk, write that value.

Undo needs the *before image* of each write that can reach the disk before its commit point. Redo needs the *after image* of each committed write that can be missing from the disk. The buffer policy decides which of the two can happen.

## Variants

- **Transaction rollback.** One transaction aborts while the system runs. Only undo is needed, and the volatile state is still there to help. Recovery after a crash must also finish the rollbacks that were in progress.
- **System crash recovery.** The problem above. It is the main case, and the cases below build on it.
- **Media recovery.** The disk is lost. Restore the archive copy, then redo the archived log from the point of the copy. An online copy taken while transactions run (a fuzzy dump) needs redo from the start of the copy, so it is close to crash recovery with a very old [checkpoint](/checkpointing/).
- **Distributed transactions.** In [two-phase commit](/two-phase-commit/) a participant can crash after it voted yes and before it hears the decision. Its transaction is then *in doubt*: recovery must keep its locks and its changes, neither undo nor redo them, and ask the coordinator. The problem gains a third state between committed and loser.
- **Main-memory databases.** The whole database is in memory and the disk holds only a log and periodic copies. Recovery loads the last copy and redoes the log; undo is rare because uncommitted data is never written out.
- **Restart time as a goal.** Some systems must also bound the time of recovery. [Checkpointing](/checkpointing/) limits the part of the log that recovery reads.

## Examples

Two items, $A = 100$ and $B = 50$. Transaction $T_1$ moves 30 from $A$ to $B$: $w_1(A, 70)$, $w_1(B, 80)$, $c_1$. The correct state after a crash is $A = 70, B = 80$ if $c_1$ reached the stable log, and $A = 100, B = 50$ if it did not.

| disk after the crash | commit point reached? | repair needed | correct result |
|---|---|---|---|
| $A = 70$, $B = 50$ | no | undo $A$ | $A = 100$, $B = 50$ |
| $A = 70$, $B = 50$ | yes | redo $B$ | $A = 70$, $B = 80$ |
| $A = 100$, $B = 80$ | yes | redo $A$ | $A = 70$, $B = 80$ |
| $A = 70$, $B = 80$ | no | undo $A$ and $B$ | $A = 100$, $B = 50$ |
| $A = 100$, $B = 50$ | no | none | $A = 100$, $B = 50$ |

The first and the second row have the same disk contents and need opposite repairs. The disk alone cannot tell them apart, so the repair needs information that is not in the data pages: the commit record, and the before or after images.

**Idempotence.** A log record that says "set $A$ to 70" can be applied twice with no harm. A record that says "subtract 30 from $A$" cannot: applied to the disk value 70 a second time, it gives 40. Recovery with such logical records must know whether the change is already on the page. Database systems store, in each page, the log sequence number of the last change applied to it (the *pageLSN*), and redo a record only when the pageLSN is smaller than the record's number. This test is the core of [write-ahead logging](/write-ahead-logging/) and of [ARIES](/aries-recovery/).

**A non-solution.** Write every changed page to the disk at commit, and keep no log. A crash in the middle of these writes, after $A = 70$ is on disk and before $B = 80$ is, leaves a state that is neither the old nor the new one, and nothing on disk says which values to restore. Writing many pages at once is not atomic, which is why the problem needs a log or an atomic switch of a root pointer.

## Known algorithms

- [Write-ahead logging](/write-ahead-logging/): log each change before the page it changes, and force the log at commit. Recovery redoes and undoes from the log. Recovery time is linear in the length of the log that it reads.
- [ARIES](/aries-recovery/): write-ahead logging with three passes (analysis, redo that repeats history, undo with compensation log records). It supports the steal and no-force policies, record-level locking and partial rollback, and its recovery is restartable with bounded log growth.
- [Shadow paging](/shadow-paging/): never overwrite a page in place; commit by an atomic switch of the root of the page table. It needs no undo or redo of page contents.
- [Checkpointing](/checkpointing/): not a recovery method on its own, but the way to bound the part of the log that recovery reads.
- [Group commit](/group-commit/): a way to meet the commit rule of write-ahead logging with fewer log writes.
- The choice between them is ruled by the [steal and force](/steal-and-force-policies/) policies: steal needs undo, no-force needs redo.

## Bounds

The costs are counted in log records read and written and in page reads and writes, not in a closed form.

- **Redo work.** With write-ahead logging, recovery reads the log from a redo point to the end. Without checkpoints the redo point is the start of the log, so the work grows without bound as the system runs. A fuzzy checkpoint makes the redo point the oldest first change of a page that was dirty at the checkpoint.
- **Undo work.** Undo reads, for each loser, its log records back to its first one. A long-running transaction that has not committed therefore makes recovery long, whatever the checkpoint policy.
- **Commit cost.** With a no-force policy, each commit needs at least one write to stable storage (its commit record) before it is reported, and a force policy needs a write of each changed page as well. Group commit shares one log write among many commits.
- **Restartable recovery.** In ARIES, each update of a loser is undone at most once over any number of crashes during recovery, because the compensation record of an undo is never undone. So the log that repeated crashes produce grows by at most one record for each update of a loser, plus one end record for each loser.

There are no general lower bounds for the problem in a standard model of computation; the trade-offs between normal-time cost and recovery time are argued from the cost model above.

## Reductions

- Transaction rollback reduces to the undo part of crash recovery for one transaction. ARIES uses the same code for both.
- Media recovery reduces to crash recovery: restore the archive copy as the disk state, then run redo from the log position of the copy.
- [Atomic commit](/atomic-commit/) across sites uses local crash recovery at each participant, with the prepared state added to the log.

## Applications

Every transactional database system solves this problem, and so do journaling file systems, which log changes to their metadata (and in some modes their data) before they write them in place. Storage engines built on a [log-structured merge tree](/log-structured-merge-tree/) keep a write-ahead log for the part of the data that is still in memory. Replicated systems keep a [replicated log](/replicated-log/), but each replica still needs local recovery of its own state. In-memory [transactional memory](/transaction/) gives atomicity and isolation but not durability, so it does not face this problem.

## References
