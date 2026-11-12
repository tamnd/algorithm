---
tag: T1AQ30
kind: concept
slug: steal-and-force-policies
name: Steal and force buffer policies
aliases:
- STEAL/NO-STEAL
- FORCE/NO-FORCE
- steal/no-force policy
- Haerder-Reuter recovery taxonomy
area: systems/database-algorithms
level: core
summary: "Two buffer manager choices: may a page with uncommitted changes go to disk (steal), and must commit write all changed pages (force). Steal needs undo; no-force needs redo."
prereqs: [crash-recovery]
see_also: [write-ahead-logging, aries-recovery, shadow-paging, checkpointing, write-back, write-through]
sources:
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the classification of propagation strategies (ATOMIC or not), replacement (STEAL or not), end of transaction processing (FORCE or not) and checkpoints, and the table of recovery actions each combination needs
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill, 2003
    locator: Chapter 16, the section on buffer management and recovery (steal and force), and Chapter 18 (ARIES uses steal and no-force)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 10, Transaction Manager Concepts (the interaction of the buffer manager with the log), chapter level only
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 6 (the undo/redo, undo/no-redo, no-undo/redo and no-undo/no-redo recovery algorithms)
---

The *steal* and *force* policies are two independent choices of a database buffer manager that decide what a [crash recovery](/crash-recovery/) method must be able to do. *Steal* lets the buffer manager write a page to disk while a transaction that changed it has not committed; *force* makes every page that a transaction changed reach the disk before its commit is reported. Haerder and Reuter (1983) named the four combinations. A steal policy needs undo information on stable storage, and a no-force policy needs redo information; most systems use steal with no-force, and so need both.

## In plain words

The database changes pages in a memory cache and writes them to disk later. Two questions decide what can be wrong on the disk after a crash.

The first question: may the cache write a page to disk while the change on it belongs to a transaction that has not finished? If yes, the disk can hold a change that must be taken back. So the system must have saved the old value first.

The second question: must every changed page reach the disk before the system says that a transaction is done? If no, a finished transaction can have changes that are only in memory. So the system must have saved the new value first.

Old values allow undo, and new values allow redo. The fastest choice in normal work, yes and then no, needs both.

## The idea

**Definitions.** Let $T$ be a transaction, $p$ a page in the buffer pool, and say that $p$ is *dirty for* $T$ if $p$ holds a change of $T$ that is not yet on the disk.

- **Steal.** The buffer manager may write $p$ to the disk while $p$ is dirty for a transaction that has not reached its commit point. *No-steal* forbids this: a page with uncommitted changes stays in memory (it is *pinned*) until the transaction ends.
- **Force.** Before the commit of $T$ is reported, every page that is dirty for $T$ is written to the disk. *No-force* lets these pages stay in memory after the commit, to be written whenever the replacement policy chooses.

Haerder and Reuter add a third choice, *propagation*: ATOMIC propagation writes a set of pages so that a crash leaves all of them or none of them on disk (for example by [shadow paging](/shadow-paging/)), and NOT ATOMIC propagation updates pages in place, one at a time. Most systems update in place.

**What each choice needs.** With update in place, the four combinations need these recovery actions after a system crash:

| | force | no-force |
|---|---|---|
| **steal** | undo, no redo | undo and redo |
| **no-steal** | no undo, no redo, only if the force at commit is atomic | redo, no undo |

The two rules behind the table:

- *Steal needs undo.* Under steal, an uncommitted value can be on the disk at the crash, so recovery must write back the value that was there before. That before image must be on stable storage before the page is written, which is the WAL rule of [write-ahead logging](/write-ahead-logging/).
- *No-force needs redo.* Under no-force, a committed value can be missing from the disk at the crash, so recovery must write it. That after image must be on stable storage before the commit is reported, which is the commit rule.

The cell "no-steal and force" needs a remark. If the pages of $T$ are forced one at a time and the system crashes after some of them are written, the disk holds part of $T$. $T$ has not committed, because the commit point is after the force. So recovery must undo those pages, or, if the after images were logged before the force, redo the rest. Only an atomic force, such as the root switch of shadow paging, gives a disk that needs neither undo nor redo.

**Costs in normal operation.** The choices that need less recovery cost more while the system runs.

- *Force* writes each changed page at each commit. A page that many transactions change (a hot page, such as a counter) is written once per transaction, and each write is a random I/O, while a log write is sequential and can be shared ([group commit](/group-commit/)). The commit latency includes all these writes.
- *No-steal* pins every page that an active transaction changed. A transaction that changes more pages than the buffer pool holds cannot run, and the replacement policy has fewer pages to choose from.
- *Steal and no-force* let the buffer pool act as a plain [write-back](/write-back/) cache, at the price of a log with both images and a recovery with both passes.

Haerder and Reuter also tie *force* to checkpoints: a force at each commit acts as a checkpoint for that one transaction (they call it transaction-oriented), so redo is never needed.

## Examples

All four examples start with $A = 100$ and $B = 50$ on disk. Transaction $T_1$ writes $w_1(A, 70)$ and has not committed at the crash. Transaction $T_2$ writes $w_2(B, 80)$ and commits, $c_2$. The correct state after recovery is $A = 100$, $B = 80$. Each example shows a crash that loses data when the log that the policy needs is missing.

**Steal and no-force.** The buffer manager steals page $A$ (writes $A = 70$ to disk), $T_2$ commits without a force, and the system crashes before page $B$ is written. Disk: $A = 70$, $B = 50$. Without a before image of $A$, the value 70 of an uncommitted transaction stays: atomicity fails. Without an after image of $B$, the committed value 80 is lost: durability fails. The log must hold both.

**Steal and force.** $A = 70$ is stolen, $T_2$ commits and its page $B = 80$ is forced. Crash. Disk: $A = 70$, $B = 80$. $B$ is right with no redo. Without a before image of $A$, the disk keeps 70: atomicity fails. An undo log is enough.

**No-steal and no-force.** $A = 70$ stays pinned in memory, $T_2$ commits without a force, crash. Disk: $A = 100$, $B = 50$. $A$ is right with no undo. Without an after image of $B$, the committed 80 is lost. A redo log is enough.

**No-steal and force, not atomic.** Change the example so that $T_2$ writes two pages, $w_2(B, 80)$ and $w_2(A, 70)$, with $T_1$ absent. At commit the force writes $B = 80$, then the system crashes before it writes $A$. Disk: $A = 100$, $B = 80$. The commit record was not written, so $T_2$ is a loser and $B$ must return to 50, but the disk does not hold the old value of $B$ any more. With an atomic force (all or nothing), the disk would hold either both old or both new values and no log would be needed.

## Where it is used

- [ARIES](/aries-recovery/) is designed for steal and no-force, and so it logs both images and has a redo and an undo pass.
- [Write-ahead logging](/write-ahead-logging/) is the protocol that makes steal safe (the log before the page) and no-force safe (the log before the commit).
- [Shadow paging](/shadow-paging/) provides atomic propagation, the one way to get the no-undo and no-redo cell.
- [Checkpointing](/checkpointing/) limits redo under no-force by writing out dirty pages, or by recording which pages are dirty.
- Main-memory database systems often never write uncommitted data (no-steal) and never force data pages (no-force), so they keep only a redo log.
- In hardware and operating system caches, [write-back](/write-back/) and [write-through](/write-through/) answer a similar question, but with no transactions: there is no uncommitted data to keep off the disk, and no commit at which to force.

## References
