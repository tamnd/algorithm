---
tag: X5CC3X
kind: data-structure
slug: undo-log
name: Undo log
aliases:
- rollback log
area: concurrency/transactional-memory
level: advanced
summary: Private record of the old values of the words a transaction writes in place. Commit throws it away; abort writes the old values back, in reverse order.
complexity:
  vars: {w: the number of distinct words the transaction writes, t: the number of its writes}
  steps: {write: O(1), commit: O(1), rollback: Θ(w)}
  space: {log: Θ(w), entry_per_write_log: Θ(t)}
prereqs: [read-set-and-write-set]
see_also: [redo-log, eager-versioning, encounter-time-locking, tinystm, transaction-abort, write-ahead-logging, aries-recovery, privatization-safety]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (eager version management with an undo log) and Chapter 4 (Software transactional memory), the part on the logs that an STM keeps
  - paper: doi:10.1145/1345206.1345241
    title: "Pascal Felber, Christof Fetzer and Torvald Riegel, Dynamic performance tuning of word-based software transactional memory, PPoPP 2008, pages 237-246"
    locator: the write-through mode of TinySTM, which writes in place and keeps an undo log
  - paper: "Ali-Reza Adl-Tabatabai, Brian T. Lewis, Vijay Menon, Brian R. Murphy, Bratin Saha and Tatiana Shpeisman, Compiler and runtime support for efficient software transactional memory, PLDI 2006"
    locator: an STM with in-place updates and an undo log, with the compiler support for it
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983
    locator: undo and redo information in database logs, the source of the names
---

An undo log is the private record that a [transaction](/transaction/) keeps when it writes shared memory in place. Before its first write to a word, the transaction saves the old value of the word in the log, and then it writes the new value straight to memory. If the transaction commits, it throws the log away: memory already holds the new values. If it aborts, it *rolls back*: it writes the old values back from the log, in reverse order. The undo log is the data structure of [eager versioning](/eager-versioning/), used in the write-through mode of [TinySTM](/tinystm/) and in the STM of McRT and of Adl-Tabatabai et al. (2006). Its counterpart is the [redo log](/redo-log/) of lazy versioning, which keeps new values aside and writes them at commit. An undo log is only safe if the STM keeps other transactions away from each written word until the transaction ends, usually with a write lock taken at the first write ([encounter-time locking](/encounter-time-locking/)). This page gives the data structure; the versioning page gives the policy.

## In plain words

The transaction writes memory directly. Just before the first time it writes a word, it notes the old value of that word in a private list. If the transaction succeeds, the list is not needed and is dropped, so a commit costs almost nothing. If it fails, the transaction goes through the list from the end to the start and puts each old value back. During the transaction, memory holds values that may still be undone, so no other transaction may read or write those words; the STM locks them.

## The abstract type

An undo log is private to one transaction and works on the shared memory $M$.

| Operation | Effect |
|---|---|
| write$(a, v)$ | if $a$ is not logged, save $(a, M(a))$; then $M(a) \leftarrow v$ |
| commit | drop the log |
| rollback | for each saved $(a, u)$, from the last to the first: $M(a) \leftarrow u$; then drop the log |

A read needs no lookup in the log: memory already holds the transaction's own writes. This is the main gain over a redo log.

## Representation

- A list $E$ of entries $(a, u)$: a word and its old value, in the order of the writes.
- A set *logged* of the words already in $E$, so that each word is saved once. Many STMs skip this set and save at every write, or use the write lock of the word to tell whether the word is already logged: if the transaction already holds the lock, the word is in the log.

## Operations

```pseudo id=main
WRITE(a, v)
L1  if a ∉ logged then                       ▷ first write of this transaction to a
L2      append (a, M[a]) to E; logged ← logged ∪ {a}
L3  M[a] ← v                                 ▷ in place; the STM holds the write lock of a

ROLLBACK()
L4  for each (a, u) in E, from the last to the first: M[a] ← u; then clear E and logged

COMMIT()
L5  clear E and logged
```

In an eager-versioning STM, the write of the transaction is: acquire the write lock of $a$ (or abort), then WRITE$(a, v)$. The commit is: validate the reads, COMMIT, release the locks with new versions. The abort is: ROLLBACK, then release the locks with versions that tell readers the word changed, or with the old versions if no reader can have seen the new values.

## Example

Memory $x = y = z = 0$. A transaction writes $x \leftarrow 1$, $y \leftarrow 2$, $x \leftarrow 3$, and then aborts.

| Step | Operation | Entries $E$ | Memory $(x, y, z)$ |
|---|---|---|---|
| 1 | write$(x, 1)$ | $(x, 0)$ | $(1, 0, 0)$ |
| 2 | write$(y, 2)$ | $(x, 0), (y, 0)$ | $(1, 2, 0)$ |
| 3 | write$(x, 3)$ | same: $x$ is logged | $(3, 2, 0)$ |
| 4 | rollback: $y \leftarrow 0$, then $x \leftarrow 0$ | empty | $(0, 0, 0)$ |

Rollback writes 2 words. If the transaction commits instead of step 4, memory keeps $(3, 2, 0)$ and the commit writes nothing. The test `test_worked_example` runs these steps.

**Why reverse order.** If the log saves an entry at every write, the writes $x: 0 \to 1 \to 2$ give the entries $(x, 0), (x, 1)$. A rollback in reverse order ends with $x = 0$. A rollback in forward order ends with $x = 1$, a value that the transaction wrote and that never committed. The test `test_with_an_entry_per_write_only_the_reverse_order_works` shows both.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). It shows that each word in the log is saved with the value it had just before the transaction first wrote it, and that a rollback in reverse order restores exactly that value for each written word and touches no other word. The proof needs one assumption: from the first write to a word until the end of the rollback, no other transaction writes it. Without this, the tests show two failures: a reader sees a value that is later undone (a dirty read), and a rollback wipes out a write that another transaction committed in the meantime.

## Complexity

Let $w$ be the number of distinct words written and $t$ the number of writes.

- write: $O(1)$ expected time, one shared read and one shared write the first time a word is written, one shared write after that.
- read: no lookup, a plain memory read (plus the checks of the STM).
- commit: $O(1)$ shared steps, since the new values are already in memory.
- rollback: $\Theta(w)$ shared writes, or $\Theta(t)$ with an entry per write.
- Space: $\Theta(w)$ entries, or $\Theta(t)$ with an entry per write.

Compared with the [redo log](/redo-log/), the undo log moves the memory writes from the commit to the write, and moves the cost of an abort from nothing to $\Theta(w)$. It is cheaper when most transactions commit, and dearer when many abort.

## Variants

- **Entry per write.** Save an entry at every write, with no *logged* set. It is simpler and avoids a lookup, at the cost of a longer log, and it needs the reverse order at rollback.
- **Lock as the logged flag.** With encounter-time locking, the transaction already holds the write lock of a word it wrote, so the lock tells whether to log. TinySTM in write-through mode works this way.
- **Object granularity.** An object-based STM can save a copy of the whole object at the first write, and restore it at abort.
- **Database undo logs.** In a database, undo records are written to a durable log before the changed page goes to disk, so that recovery can roll back uncommitted work after a crash ([write-ahead logging](/write-ahead-logging/), [ARIES](/aries-recovery/)). The STM undo log is not durable; it only serves aborts while the process runs.

## When to use it

Use an undo log when most transactions commit and the commit must be short, and when transactions often read words that they wrote, since a read needs no lookup. It fits [eager versioning](/eager-versioning/) with [encounter-time locking](/encounter-time-locking/). Avoid it when aborts are frequent, since each abort writes memory twice (once at the write, once at the rollback); when other code may read the same memory outside transactions, since that code can see values that are later undone; and with an STM whose writes do not take a lock, since the rollback can then destroy other writes.

## Pitfalls

- **No write lock.** An undo log needs exclusive access to each written word from the first write to the end. Without it, a rollback can overwrite a committed value of another transaction, and other transactions can read values that are later undone. The tests show both runs.
- **Forward rollback with an entry per write.** It leaves the value of a middle write. Roll back in reverse order.
- **Logging after the write.** The old value must be saved before memory changes.
- **Readers that do not check the lock.** A reader that ignores the write lock can read a value that the writer later rolls back. An opaque STM must make such a reader wait or abort, or the reader can become a [zombie](/zombie-transactions/).
- **Version numbers on abort.** If a reader may have seen a new value, the lock must get a new version when the writer rolls back, so that the reader's validation fails. Restoring the old version can let a reader that saw the undone value pass validation.
- **Privatization.** A rollback that runs after another thread has privatized the data writes old values into memory that the other thread now owns. See [privatization safety](/privatization-safety/).

## Implementations

## History

Undo logs come from database recovery, where undo records let the system roll back the changes of transactions that did not commit (Haerder and Reuter 1983 describe undo and redo information in their survey of recovery). In software transactional memory, in-place update with an undo log was used by the McRT STM of Saha et al. (2006) and by the compiler-supported STM of Adl-Tabatabai et al. (PLDI 2006). TinySTM (2008) offers it as its write-through mode, next to a write-back mode with a redo log.

## References
