---
tag: M5J251
kind: definition
slug: transaction-conflict
name: Transaction conflict
aliases:
- data conflict
- read-write conflict
- write-write conflict
area: concurrency/transactional-memory
level: intro
summary: Two concurrent transactions access the same location and at least one of them writes it. There are read-write, write-read and write-write conflicts; striped metadata adds false ones.
prereqs: [read-set-and-write-set]
see_also: [transaction-abort, contention-management, eager-conflict-detection, lazy-conflict-detection, transaction-validation, lock-striping, serializability, tl2]
sources:
  - book: isbn:9781608452354
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Morgan and Claypool, 2010
    locator: Chapter 2 (conflict detection, and the kinds of conflict between read and write sets)
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979
    locator: conflicting steps and conflict serializability
  - paper: doi:10.1007/11864219_14
    title: "Dave Dice, Ori Shalev and Nir Shavit, Transactional Locking II, DISC 2006, LNCS 4167, pages 194-208"
    locator: Section 2 (the stripe table of versioned locks, which maps many words to one lock)
  - paper: doi:10.1007/11864219_13
    title: "Michael F. Spear, Virendra J. Marathe, William N. Scherer III and Michael L. Scott, Conflict detection and validation strategies for software transactional memory, DISC 2006, LNCS 4167, pages 179-193"
    locator: the kinds of conflict and the times at which an STM can detect them
---

A **transaction conflict** happens when two [transactions](/transaction/) that run at the same time access the same memory location and at least one of the accesses is a write. Two reads never conflict. A conflict does not always mean that something went wrong: often one of the two transactions can still be placed before the other in a serial order. But a transactional memory that does not handle a conflict can break isolation, so every TM detects conflicts and resolves them, usually by making one transaction wait or [abort](/transaction-abort/). This page defines the three kinds of conflict (read-write, write-read and write-write) and the *false* conflict that comes from metadata that covers more than one word.

## Definition

**Notation and model.** $n$ is the number of processes. A transaction $T$ has a [read set](/read-set-and-write-set/) $RS(T)$ and a write set $WS(T)$, which grow as it runs. $T$ is *live* from its begin until its commit or abort. Two transactions are *concurrent* if each begins before the other ends.

**Definition.** Let $T$ and $U$ be concurrent transactions and $a$ a location. $T$ and $U$ **conflict on $a$** if at least one of them writes $a$ and the other reads or writes $a$:

$$a \in \big(WS(T) \cap (RS(U) \cup WS(U))\big) \cup \big(WS(U) \cap RS(T)\big).$$

The kind of conflict is named by the order of the two accesses. If $T$ accesses $a$ first and $U$ second:

| Kind | First access | Second access | The danger if nothing is done |
|---|---|---|---|
| read-write (RW) | $T$ reads $a$ | $U$ writes $a$ | if $U$ commits first, $T$ has read a value that is no longer current: $T$ must be ordered before $U$, or abort |
| write-read (WR) | $T$ writes $a$ | $U$ reads $a$ | $U$ may read a value that $T$ later aborts or overwrites (a dirty read) |
| write-write (WW) | $T$ writes $a$ | $U$ writes $a$ | the two commits may interleave, or one write may be lost |

Many authors do not separate RW from WR and speak of read-write conflicts for both. The order matters for an STM, because it decides who sees the conflict first: in an RW conflict the writer comes second and, with [invisible reads](/software-transactional-memory/), cannot see the reader at all.

**Where the definition comes from.** In database theory, two steps of different transactions *conflict* if they access the same item and one is a write. A schedule is *conflict serializable* if the graph with an edge from $T$ to $U$ for each conflict in which $T$ goes first has no cycle (Papadimitriou 1979; see [serializability](/serializability/)). A conflict in a TM is the same relation, looked at while the transactions still run.

**Conflict and detection are different.** The definition is about the accesses of the program. What the STM detects depends on its metadata. An STM that keeps one versioned lock for a group of words, a *stripe*, sees all words of the stripe as one location. Two transactions that access different words of the same stripe, one of them writing, have no conflict by the definition, but the STM detects one. This is a **false conflict**. In the other direction, an STM must never miss a true conflict that could break its safety condition.

## Examples and non-examples

The examples start from $x = y = 0$.

**Example (RW, and why it can be harmless).** $T$ reads $x = 0$. $U$ writes $x \leftarrow 1$ and commits. If $T$ then commits without having read anything else, the order "$T$ then $U$" explains all values, and the run is fine. If $T$ then reads $y$, which $U$ also wrote, $T$ sees $x$ from before $U$ and $y$ from after $U$; no order explains it, so $T$ must abort. The [TL2](/tl2/) page shows this run with an audit and a transfer.

**Example (WR).** $T$ writes $x \leftarrow 1$ in place (eager versioning) and has not committed. If $U$ reads $x = 1$ and $T$ then aborts, $U$ has read a value that never existed in any committed state. An STM with an [undo log](/undo-log/) prevents this with a write lock that readers check. The undo-log test `test_without_a_write_lock_another_reader_sees_a_value_that_is_undone` shows the run.

**Example (WW, a lost update).** $T$ and $U$ both read $x = 0$ and both write $x \leftarrow x + 1$. The two writes conflict, and so do each read and the other write. If both commit, $x = 1$, while any serial order gives $x = 2$. The TL2 test `test_without_write_locks_an_update_is_lost` removes the write locks from TL2 and finds this run: both transactions commit and $x$ ends at 1.

**Example (false conflict from striping).** TL2 maps each word to a lock by a hash. A reader reads $x$; a writer writes $y$ and commits. With one lock per word, nothing happens: the reader commits. With the hash that sends every word to stripe 0, the writer's commit gives the stripe a new version, and the reader, which then reads $x$, sees a version newer than its start time and aborts. The TL2 test `test_lock_striping_gives_a_false_conflict` counts 0 aborts in the first case and 1 in the second. With a table of $s$ stripes and a good hash, two given different words share a stripe with probability about $1/s$.

**Non-example (two reads).** $T$ and $U$ both read $x$. They do not conflict, and every STM lets them run in parallel. With *visible reads*, the two readers both write to shared reader metadata; the STM must take care that this traffic does not create a detected conflict.

**Non-example (not concurrent).** $T$ writes $x$ and commits; then $U$ begins and reads $x$. The accesses touch the same location, but the transactions are not concurrent, so there is no conflict: $U$ simply comes after $T$.

**Non-example (a write that only looks like a conflict).** $T$ reads $x$ and $U$ writes the same value back into $x$. By the definition, they conflict. An STM that validates by value, such as [NOrec](/norec/), does not see it, and that is safe, because $T$'s read is still correct. A detected conflict is a property of the STM, not of the program.

## Related definitions

- [Read set and write set](/read-set-and-write-set/): the sets the definition uses.
- [Eager conflict detection](/eager-conflict-detection/) finds a conflict at the second access; [lazy conflict detection](/lazy-conflict-detection/) finds it at commit.
- [Transaction validation](/transaction-validation/) finds RW conflicts with invisible reads.
- [Contention management](/contention-management/) decides which of two conflicting transactions waits or aborts; [transaction abort](/transaction-abort/) is the usual result.
- A [data race](/race-condition/) is the same pattern for plain accesses outside transactions; under [weak atomicity](/weak-atomicity/), a conflict between a transaction and a plain access is not detected.
- [Lock striping](/lock-striping/) is the source of false conflicts.

## References
