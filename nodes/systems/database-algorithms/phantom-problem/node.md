---
tag: J2PGNY
kind: concept
slug: phantom-problem
name: Phantom problem
aliases:
- phantoms
- phantom read
- phantom phenomenon
area: systems/database-algorithms
level: advanced
summary: "A query reads the rows that match a condition, and another transaction then inserts a matching row. Row locks cannot stop this, so two-phase locking on rows is not serializable."
prereqs: [two-phase-locking]
see_also: [predicate-locking, two-phase-locking, strict-two-phase-locking, isolation-levels, snapshot-isolation, serializable-snapshot-isolation, b-tree, conflict-serializability]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the discussion of phantoms (records that are inserted into a set that another transaction has already read) and the predicate locks proposed against them
  - paper: doi:10.1145/223784.223785
    title: Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, SIGMOD 1995, pages 1 to 10
    locator: the phenomenon P3 (phantom) and the anomaly A3, and the isolation levels that allow them
  - paper: "C. Mohan, ARIES/KVL, a key-value locking method for concurrency control of multiaction transactions operating on B-tree indexes, Proceedings of the 16th International Conference on Very Large Data Bases (VLDB), 1990, pages 392 to 405"
    locator: next-key locking on B-tree indexes, which locks the key after a range or after an inserted key
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (phantoms, predicate locks and the locking of key ranges)
---

The phantom problem is the gap between locking *rows* and locking *queries*. A transaction runs a query with a condition, such as all employees of department A, and locks every row that it finds. Another transaction then inserts a new row that matches the condition. The new row did not exist when the locks were taken, so no lock protects it. If the first transaction runs the query again, or uses a total that depends on it, it sees the new row, a *phantom*. Eswaran, Gray, Lorie and Traiger described the problem in 1976 and showed that [two-phase locking](/two-phase-locking/) on single rows is then not enough for serializability. The usual cures are [predicate locking](/predicate-locking/) and its practical forms on indexes, key-range and next-key locks.

## In plain words

Suppose you count the people in a room and lock the door of every person you counted so that nobody leaves. That stops people from leaving, but it does nothing about a new person who walks in. A moment later you count again and get a different number. The new person is the phantom.

The problem is that you locked people, but what you really read was "everyone in this room". To be safe, you must lock the room itself, or at least the door through which new people come in. In a database, the room is a condition on the rows, and the door is a place in an index where a new matching row would go.

## The idea

**Why the item model breaks.** The theory of [conflict serializability](/conflict-serializability/) assumes a fixed set of data items: each action reads or writes one known item, and two actions conflict when they touch the same item. A query with a condition does not touch a fixed item. It reads *the set of rows that satisfy a predicate* $P$, and that set depends on the state. An insert or a delete of a row that satisfies $P$, or an update that makes a row start or stop satisfying $P$, changes the answer, although it touches no row that the query has read.

**A non-serializable execution with row locks.** Let a table hold employees with a department, and let a separate row $\mathit{total}_A$ store the number of employees in department A. Let $T_1$ list the employees of A and then read $\mathit{total}_A$ to print a report, and let $T_2$ hire a new employee $e_3$ in A and increment $\mathit{total}_A$. Both use [strict 2PL](/strict-two-phase-locking/) on rows.

| step | action | locks |
|---|---|---|
| 1 | $T_1$ scans A, finds $e_1$ and $e_2$ | $T_1$: S on $e_1$, $e_2$ |
| 2 | $T_2$ inserts $e_3$ in A | $T_2$: X on $e_3$ (a new row, nobody else can hold a lock on it) |
| 3 | $T_2$ reads and writes $\mathit{total}_A$ from 2 to 3, commits | $T_2$: X on $\mathit{total}_A$, then all released |
| 4 | $T_1$ reads $\mathit{total}_A = 3$ | $T_1$: S on $\mathit{total}_A$ |

$T_1$ prints two employees and a total of three. In the order $T_1 T_2$, it would see two employees and a total of two; in $T_2 T_1$, it would see three and three. No serial order explains what it saw. Yet, viewed as reads and writes of rows, the only conflict is on $\mathit{total}_A$, which gives $T_2 \to T_1$, and the schedule looks conflict serializable. The hidden conflict is between the scan, a read of the predicate "department is A", and the insert of a row that satisfies it.

**The precise condition.** Call an action a *predicate read* $r_i(P)$ when it reads all rows that satisfy $P$, and say that a write *conflicts* with it when the write inserts, deletes or changes a row that satisfies $P$ before or after the write. With these conflicts added, the conflict graph and the serializability theorem work again, and two-phase locking is correct again if it locks predicates instead of rows ([predicate locking](/predicate-locking/)). Without them, 2PL on rows gives serializability only for a fixed set of rows.

**The cures.**

- *Predicate locks.* Lock the predicate $P$ itself. Two predicate locks conflict when some possible row satisfies both and one of them is exclusive. This is exact but expensive to test.
- *Next-key and key-range locks.* When a query uses an index on the condition, lock the index entries in the range and the entry just after it; an insert must lock the entry just above the new key. Every gap between keys is then guarded by the key that ends it. This is the method of ARIES/KVL (Mohan, 1990) and of key-range locking (Lomet, 1993).
- *Coarser locks.* Lock the whole table or the index page that covers the range. Simple and correct, with less concurrency.
- *Serializable snapshot isolation.* [Serializable snapshot isolation](/serializable-snapshot-isolation/) records which index ranges each transaction read, and aborts a transaction when a concurrent write into such a range closes a dangerous cycle.

**Phantoms and isolation levels.** In the ANSI SQL standard the phenomenon P3 is the phantom, and the REPEATABLE READ level allows it while SERIALIZABLE does not. Berenson and others (1995) pointed out that the standard's wording is ambiguous, separated the strict anomaly A3 (the same query gives a different answer in one transaction) from the broad phenomenon P3, and showed that [snapshot isolation](/snapshot-isolation/) rules out A3 but still allows P3-style anomalies such as write skew on a predicate. See [isolation levels](/isolation-levels/).

## Examples

**A repeated scan.** The index holds the keys 5, 10, 20, 30. $T_1$ scans the range from 10 to 20 twice, and $T_2$ inserts 15 between the two scans. The test file runs this with both schemes.

| scheme | first scan of $T_1$ | insert of 15 by $T_2$ | second scan of $T_1$ |
|---|---|---|---|
| row (tuple) locks | 10, 20; S on 10 and 20 | X on 15, granted | 10, 15, 20: a phantom |
| next-key locks | 10, 20; S on 10, 20 and the next key 30 | needs X on 15 and on its next key 20; waits | 10, 20; then $T_1$ commits and $T_2$ goes on |

An insert of 35 is not blocked by the next-key scheme: its next key is the end of the index, which the scan of 10 to 20 did not lock. In 1500 random runs of the test file (seed 17, up to four transactions of scans and inserts), row locks gave a phantom in a repeated scan 173 times, and next-key locks gave none; every next-key run matched the serial run in commit order.

**A constraint check.** A booking system must never give a room to two meetings at the same time. Each booking transaction searches for a booking of the room that overlaps its time, finds none, and inserts its own booking. Under row locks, the search found no rows, so it locked nothing, and two such transactions for the same room and time can both insert. Snapshot isolation allows the same result, because neither transaction sees the insert of the other. The predicate "bookings of this room that overlap this time" was read, and the insert of the other transaction satisfies it.

**Deletes and updates.** A phantom does not need an insert. Deleting a row that a scan has read is stopped by the row lock, but an update that moves a row *into* the scanned range, by changing the department of an employee in B to A, is an insert from the point of view of the predicate.

## Where it is used

- **SERIALIZABLE in locking databases.** Systems that implement SERIALIZABLE with [strict 2PL](/strict-two-phase-locking/) add next-key or key-range locks on indexes, and fall back to table locks when no index covers the condition. Gap locks in some storage engines are a form of next-key locking.
- **Serializable snapshot isolation.** Range locks that do not block, recorded only to detect dangerous read-write dependencies, are how [SSI](/serializable-snapshot-isolation/) handles phantoms.
- **Index concurrency.** The next-key method is defined on [B-trees](/b-tree/), and it must be combined with the latches or [lock coupling](/lock-coupling/) that protect the tree structure itself; those protect the physical pages, while key locks protect the logical contents.
- **Transactional memory.** In software [transactional memory](/transaction/), the read set is a set of memory words, which are fixed, so the phantom problem does not arise for words. It comes back for transactional data structures such as sets and maps, where a lookup of an absent key must conflict with a later insert of that key. Transactional boosting handles this with abstract locks on keys.

## References
