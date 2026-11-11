---
tag: R3QGVQ
kind: concept
slug: open-nested-transactions
name: Open nested transactions
aliases:
- open nesting
area: concurrency/transactional-memory
level: research
summary: An inner transaction that commits for everyone at once; if its parent aborts, a compensating action undoes it, and abstract locks keep the parent's work serializable.
prereqs: [nested-transactions, serializability, linearizability]
see_also: [transactional-boosting, retry-and-orelse, undo-log, transaction-irrevocability, two-phase-locking, read-set-and-write-set, transaction-conflict, logical-deletion]
sources:
  - paper: doi:10.1145/1229428.1229442
    title: "Yang Ni, Vijay S. Menon, Ali-Reza Adl-Tabatabai, Antony L. Hosking, Richard L. Hudson, J. Eliot B. Moss, Bratin Saha and Tatiana Shpeisman, Open nesting in software transactional memory, PPoPP 2007, pp. 68 to 78"
    locator: the open atomic block with commit and abort handlers, abstract locks, and the evaluation on collection classes in a Java STM
  - paper: doi:10.1016/j.scico.2006.05.010
    title: "J. Eliot B. Moss and Antony L. Hosking, Nested transactional memory: model and architecture sketches, Science of Computer Programming 63(2), 2006, pp. 186 to 201"
    locator: the model of open nesting, its read and write set rules, and the discussion of when open nesting is safe
  - book: doi:10.1007/978-3-031-01728-5
    title: Tim Harris, James Larus and Ravi Rajwar, Transactional Memory, second edition, Synthesis Lectures on Computer Architecture, 2010
    locator: Chapter 2 (Basic transactions, the section on nesting, open nesting)
---

An **open nested transaction** is a transaction inside another one that commits for everyone at once: when it ends, its writes become visible to all threads and leave the read and write sets of its parent. This removes conflicts that the parent does not care about, such as conflicts on the size counter of a shared set. The price is that the TM can no longer undo the child from a log if the parent aborts, so the programmer gives a **compensating action** (an inverse at the level of the abstract data type) and holds **abstract locks** to keep other transactions away from the abstract state the child changed. Moss and Hosking described open nesting for TM in 2006, and Ni et al. built it into a Java STM in 2007.

## In plain words

Suppose a long transaction adds an item to a shared set. The set keeps a counter of its size, so every transaction that adds anything to the set writes the counter, and all of them conflict, even when they add different items. The program does not need these conflicts: it only cares that the right items are in the set.

Open nesting lets the "add" finish and publish its result right away, so the counter is free again for others. But now, if the long transaction fails later, the "add" has already happened. The program must say how to take it back: "remove the item, if I added it". And while the long transaction runs, it keeps a lock on that item, so no one else relies on an item that may soon vanish.

## The idea

### Semantics

Let $C$ be an open child of $T$. Moss and Hosking give these rules:

| event | effect |
|---|---|
| $C$ runs | it sees the writes of its ancestors, like a closed child |
| $C$ commits | its writes become visible to every thread; $R(C)$ and $W(C)$ are dropped, not merged into $T$; the handlers that $C$ registers join $T$ |
| $C$ aborts | as for a closed child: only $C$ is undone |
| $T$ commits | the commit handlers run; abstract locks are released |
| $T$ aborts | the closed work of $T$ is undone from its log; the compensating actions of its committed open children run in reverse order, each as a transaction; then abstract locks are released |

Ni et al. write this as an `open atomic` block that can register an `onabort` handler (the compensation) and an `oncommit` handler for its parent, and give abstract locks as a library.

### Two levels of abstraction

Open nesting is correct only if the program is viewed at two levels. At the *low level*, the child reads and writes words; at the *high level*, it performs one operation of an abstract data type, such as `insert(k)` on a set. The parent must use the object only through such operations. Correctness is then *abstract serializability*: the committed top-level transactions, seen as sequences of abstract operations, are equivalent to a serial run. This is the idea of multi-level transactions in databases, and the same argument underlies [transactional boosting](/transactional-boosting/).

Two things are needed for that argument:

1. **Abstract locks.** If $T$ runs `insert(k)` in an open child, no other transaction may run an operation that does not commute with it (another `insert(k)`, `remove(k)` or `contains(k)`) until $T$ commits or has compensated. $T$ takes a lock on the key $k$ before the child and holds it to the end, as in [two-phase locking](/two-phase-locking/). Operations on other keys commute with it and proceed. Without the lock, another transaction can see $k$ in the set, commit, and then see $T$ abort and remove $k$: it observed a state that no serial order of committed transactions contains.
2. **Correct compensation.** The compensation must be an inverse at the high level, given the result of the child: if `insert(k)` returned "added", the inverse is `remove(k)`; if it returned "already there", the inverse is to do nothing. A *physical* undo (write back the old words) is wrong, because other transactions may have changed those words at the low level after the child committed. That is the whole point of open nesting.

### What goes wrong

**Physical undo loses an update.** The set is empty and its size word is 0. $T$ inserts key 1 in an open child and later aborts; process $q$ inserts key 2 with a normal transaction.

| step | parent $T$ | process $q$ | key 1 | key 2 | size |
|---|---|---|---|---|---|
| 1 | open child: insert 1, old size 0; commit | | 1 | 0 | 1 |
| 2 | | insert 2; commit | 1 | 1 | 2 |
| 3 | abort; compensation writes key 1 = 0, size = 0 | | 0 | 1 | 0 |

The set holds key 2 but its size says 0. With the compensation `remove(1)`, step 3 decrements the size and leaves 1.

**A missing abstract lock leaks the child.** $T$ inserts key 1 and later aborts; $q$ runs `contains(1)` and commits. Without the lock on key 1, $q$ can run between steps 1 and 3 and answer "yes", though no committed transaction ever left key 1 in the set. With the lock, $q$ waits until $T$ has compensated and answers "no".

**A compensation that ignores the result.** $q$ inserts key 1 and commits; then $T$ tries to insert key 1 in an open child, which finds it there, and $T$ aborts. A compensation that always runs `remove(1)` deletes the key that $q$ added. The inverse must depend on what the child did.

The implementation for this page runs each of these three programs over all interleavings on a small TL2 model with open children, compensation and abstract locks. The wrong versions (physical undo, no abstract lock, unconditional remove) each reach a bad state, and the correct version never does. Random runs with up to four parents that insert keys and then commit or cancel, plus a writer that makes parents abort and retry, always end with exactly the keys of the committed parents and the right size.

### Other hazards

- If the parent itself reads or writes the words that an open child wrote, the two levels mix and the argument above breaks: the parent's closed log can undo a word that another transaction changed through an operation. The parent must use the object only through its operations.
- A compensation that can fail, block or conflict with the aborting parent needs care; most systems run compensations as ordinary top-level transactions and retry them until they commit.
- Compensations run in the reverse order of the children, so a later child's inverse runs first, as with an [undo log](/undo-log/).

## Examples

**Collection classes.** Ni et al. use open nesting in a hash map and other collections in a Java STM, so that transactions that use different keys do not conflict on the internal size field or bucket structure. The open operation is `put`, its abstract lock is the key, and its compensation is `remove` or a `put` of the old value.

**Unique identifiers.** A transaction that takes a fresh ID from a counter can do so in an open child. Its compensation can be empty: an ID that is never used does no harm. This is a case where no abstract lock is needed, because nothing that another transaction can observe depends on the ID being used.

**Memory allocation.** A transaction that allocates memory can call the allocator in an open child, so that allocations of different transactions do not conflict in the allocator's free lists; the compensation frees the block.

**Logging.** Writing a debug log or statistics from inside a transaction in an open child keeps the log write even if the parent aborts; here the compensation is empty on purpose.

## Where it is used

- Database systems use the same idea as multi-level transactions and as sagas, long transactions built from steps that each commit and have a compensating step.
- Research STMs for Java and C++ (the system of Ni et al., and others that followed it) support open nesting; no mainstream hardware TM supports it. On Intel TSX, for example, an inner transaction is always flattened into the outer one.
- [Transactional boosting](/transactional-boosting/) is a close relative: each operation on a linearizable object is an open child by construction, with abstract locks and inverse operations, but it needs no support from the TM for nesting.

## References
