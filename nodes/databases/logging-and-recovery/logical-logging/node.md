---
tag: 2G2F02
kind: technique
slug: logical-logging
name: Logical logging
aliases:
- operation logging
area: databases/logging-and-recovery
level: core
summary: Log the high-level operation, such as insert this key, instead of the bytes changed, so undo can work on a page that has since changed.
prereqs: [write-ahead-logging, log-sequence-number]
see_also: [physiological-logging, redo-log, undo-log, command-logging, multi-level-recovery, compensation-log-record, state-machine-replication, aries-recovery]
sources:
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 10, physical, logical and physiological logging, chapter level only
  - paper: doi:10.1145/289.291
    title: Theo Haerder and Andreas Reuter, Principles of transaction-oriented database recovery, ACM Computing Surveys 15(4), 1983, pages 287 to 317
    locator: the classification of log data into physical and logical logging, general locator
  - url: https://dev.mysql.com/doc/refman/8.0/en/replication-formats.html
    title: MySQL 8.0 Reference Manual, Replication Formats
    locator: statement-based and row-based binary logging, and row-based logging as the default
---

*Logical logging* is the technique of writing, in each log record, the operation that a transaction performed, such as "insert key 42 with value v into index I", together with what is needed to perform its inverse, instead of the bytes that the operation changed. Recovery then redoes or undoes the operation through the normal access code, so an undo still works after the data has moved, for example after a B-tree split. Unlike [physiological logging](/physiological-logging/), a logical record names no page, so redo cannot work on one page alone; unlike the [redo log](/redo-log/) and the [undo log](/undo-log/) of transactional memory, it holds no new or old word values, which are physical and safe to apply twice. A logical record is short and independent of the storage layout, but applying it twice, or to the wrong state, gives a wrong result.

## In plain words

Instead of writing down "these bytes on that page changed from this to that", the system writes down the action itself, such as "add 30 to the balance of account 7", and how to take it back, such as "subtract 30". These notes are short, and they still make sense after the data has moved to another place on disk. The difficulty is that an action is not safe to repeat. If the system does not know whether "add 30" was already done before the crash, doing it again may add 60. So the system must replay the actions starting from a saved state that it knows exactly, or keep a marker that says which actions each piece of data already has.

## When it applies

- The operations have cheap and well-defined inverses: insert and delete of a key, increment and decrement of a counter, or a set of a field whose old value is logged.
- Undo must work on a structure that other transactions changed in the meantime. A key inserted into a [B+ tree](/b-plus-tree/) leaf may be on another page by the time its transaction aborts. A logical undo finds it again by searching.
- The log must be small, or must be read by another system that has a different storage layout, as in replication: the operations are shipped and the other side runs them.
- Recovery can start from a state that holds the effects of exactly a known prefix of the operations, such as a checkpoint taken while no operation was half done, or a snapshot of an in-memory database.

It does not apply as the only redo log of a page-based system that writes pages at any time, since the pages on disk then hold an arbitrary mix of operations, some half done.

## The template

**Records.** Each record holds an LSN, a transaction id, a prevLSN, the operation with its arguments, and the inverse operation with its arguments. The inverse is computed before the operation runs: for "delete key k" the record must hold the value that is deleted, and for "set field f to 5" it must hold the old value of f.

**Normal processing.** Follow [write-ahead logging](/write-ahead-logging/): append the record, run the operation, and make the record stable before the changes it caused reach disk and before the commit is reported.

**Redo.** Choose a start state $S_c$ that holds the effects of exactly the operations with LSN at most $c$, and no part of any later one. Run the operations with LSN greater than $c$ in log order, each once. Two ways give such a state:

1. An *operation-consistent* checkpoint: the system stops new operations, waits until the running ones are done, writes all dirty pages or a full snapshot, and records $c$. [Shadow paging](/shadow-paging/) gives the same thing by switching to a new consistent copy in one step.
2. An LSN on each object that the operations act on, set by each operation, with redo of a record only if the object's LSN is smaller. If the object is a page, this is physiological logging.

**Undo.** For each loser, run the inverse operations newest first. Each inverse is a new operation on the current state, so it is logged too, as a [compensation log record](/compensation-log-record/), and is not undone again.

**Concurrency.** A logical undo is correct when other transactions changed the same structure only if the inverse commutes with their operations. Two increments of one counter commute, so the counter can be shared; an insert and a search for the same key do not. The usual rule is to hold a lock on the logical item, such as the key, until the transaction ends, while locks on pages are released at the end of each operation.

## Classic examples

**A counter.** The balance of account 7 is 100. $T$ logs "add 30 to account 7, inverse subtract 30" and runs it: the balance is 130. A crash comes after the page with 130 went to disk. If redo starts from that disk state and runs the record again, the balance becomes 160. The physical record "account 7: 100 to 130" is safe to apply twice; the logical one needs a start state without the change, or an LSN check on the page. If $T$ is a loser, the undo "subtract 30" is right whatever other increments committed since, and a physical undo "set 100" would erase them.

**An index insert and a split.** $T$ inserts key 42 into leaf $P$ of a B+ tree. Another transaction then inserts more keys, $P$ splits, and key 42 moves to the new leaf $P'$. $T$ aborts. A physical undo of $T$'s record on $P$ would restore bytes of a page that no longer holds the key. The logical undo "delete key 42 from index I" searches the tree, finds the key in $P'$, deletes it there and logs a CLR for $P'$. The split itself is not undone, since another transaction depends on it.

**Statement-based replication.** In MySQL, with statement-based binary logging the source writes the SQL statements to the binary log, and with row-based logging it writes events that show how each table row changed. The first is logical logging of whole statements, the second is close to physical logging of rows. Row-based logging is the default. A statement whose result depends on more than the data, such as one that uses the current time or a random number, can give different rows on the replica, which is a reason to prefer row events.

**Command logging.** A deterministic in-memory database can log only the transaction requests and rebuild its state by running them again from the last snapshot. The [command logging](/command-logging/) page describes this. It is logical logging at the level of whole transactions, and the snapshot is the operation-consistent start state.

## Variations

- **Physiological redo, logical undo.** The common choice in page-based systems such as [ARIES recovery](/aries-recovery/): redo uses page-local records and the pageLSN test, which puts every page back in its state at the crash, and undo then runs logical inverses on a consistent structure.
- **[Multi-level recovery](/multi-level-recovery/).** Operations at a high level, such as record inserts, are made of page operations at a low level. Each level logs and undoes its own operations, and a completed low-level operation is undone only by the logical inverse at the level above.
- **Operation logging in replication.** [State machine replication](/state-machine-replication/) ships commands, not states, and relies on the same assumption: each replica starts from the same state and applies the same commands in the same order with a deterministic result.
- **Logical records with a value.** A record can hold the operation for redo and the old value for undo, or the reverse, when only one direction must survive layout changes.

## Pitfalls

- **Redo twice.** A logical record is usually not idempotent. Redo must either start from a state that is known to hold exactly a prefix of the log, or check an LSN on the object.
- **Redo on a half-done state.** If the disk holds a B+ tree with a split half written, running "insert key 42" on it can fail or corrupt the tree. Logical redo needs a structurally consistent start state.
- **A missing inverse.** "Delete all rows with price above 10" has no inverse unless the record, or later records, hold the rows that were deleted. Log the data that the inverse needs before the operation runs.
- **Nondeterminism.** An operation that reads the clock, a random source or the order of an unordered scan can give another result when it is run again. Log the value it used, or log the result instead.
- **An undo that cannot run.** A logical undo is a new operation and can need resources: undoing a delete in a full page needs a split and free space. Recovery must reserve what undo needs, or it can get stuck.
- **Undo that does not commute.** If other transactions may act on the same item between an operation and its undo, the inverse must commute with their operations, or the item must stay locked until the transaction ends.

## Exercises

1. Account 7 has balance 100 at a checkpoint taken at LSN 10 with no operation running. The log after it holds LSN 11 "$T_1$ add 30 to account 7", LSN 12 "commit $T_1$" and LSN 13 "$T_2$ add 5 to account 7", and there is no commit of $T_2$. Give the balance after redo from the checkpoint and after the undo of $T_2$. Then say what goes wrong if redo starts from the disk state when the disk already held 135.
2. Write the logical record and its inverse for "update the price of item 9 from 4 to 6", for "delete key 42 with value v from index I" and for "append row r to table R". Which of them need data in the record that the operation itself does not need?
3. Show that two transactions that each add to the same counter can both run, and either can abort with a logical undo, while each holds only a short lock on the page. Then show a pair of operations on one key for which this fails.
4. A system logs physiological records for redo and logical records for undo. Explain why redo must finish on all pages before the first logical undo runs.

## References
