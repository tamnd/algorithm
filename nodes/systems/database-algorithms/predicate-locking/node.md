---
tag: THBP05
kind: technique
slug: predicate-locking
name: Predicate locking
aliases:
- predicate locks
area: systems/database-algorithms
level: advanced
summary: "Lock the condition of a query instead of the rows it found, so that a write of any row that matches the condition must wait. This is the exact cure for the phantom problem."
prereqs: [phantom-problem, two-phase-locking]
see_also: [phantom-problem, two-phase-locking, strict-two-phase-locking, serializable-snapshot-isolation, isolation-levels, b-tree, read-set-and-write-set, deadlock-detection]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the definition of predicate locks, their conflict test, and the proof that two-phase locking with predicate locks gives consistent (serializable) schedules
  - paper: "H. B. Hunt III and D. J. Rosenkrantz, The complexity of testing predicate locks, Proceedings of the ACM SIGMOD International Conference on Management of Data, 1979"
    locator: the cost of deciding whether two predicate locks conflict, and the classes of predicates for which the test is easy or hard
  - paper: "J. R. Jordan, J. Banerjee and R. B. Batman, Precision locks, Proceedings of the ACM SIGMOD International Conference on Management of Data, 1981"
    locator: precision locking, where read predicates are tested against the rows that writers update
  - paper: "C. Mohan, ARIES/KVL, a key-value locking method for concurrency control of multiaction transactions operating on B-tree indexes, Proceedings of the 16th International Conference on Very Large Data Bases (VLDB), 1990, pages 392 to 405"
    locator: next-key locking on B-tree indexes
  - paper: "David B. Lomet, Key range locking strategies for improved concurrency, Proceedings of the 19th International Conference on Very Large Data Bases (VLDB), 1993"
    locator: key-range lock modes that lock a key and the gap before it separately
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (predicate locks, precision locks and key-range locks)
---

Predicate locking is a way to make [two-phase locking](/two-phase-locking/) correct when transactions read sets of rows given by a condition. A lock on a row protects only a row that exists. It cannot stop another transaction from inserting a new row that matches a query, which is the [phantom problem](/phantom-problem/). A predicate lock protects the condition itself. A query with the condition $P$ takes a shared lock on $P$. A write takes an exclusive lock on the rows it changes, described by their values. Two locks conflict when one of them is exclusive and some row can satisfy both. Eswaran, Gray, Lorie and Traiger proposed predicate locks in 1976 and showed that two-phase locking on predicates gives serializable schedules. The exact test is expensive, so real systems use cheaper forms that lock more than the predicate: locks on ranges of index keys (next-key and key-range locking), on pages, or on whole tables.

## In plain words

A row lock says "nobody may change this row". A predicate lock says "nobody may change any row that is, or would become, an employee of department A". The second lock covers rows that do not exist yet, so a new employee of department A cannot be added until the lock is released.

To decide whether two locks clash, you ask one question: can a single row match both? If one lock is for "department A" and the other is for a new row in department B, no row matches both, and both can go ahead. If the new row is in department A, it matches, and the writer must wait. Index locks give the same protection more cheaply, by locking the place in an index where such a row would go.

## When it applies

- Transactions read rows by a condition (a scan, a range query, a check that no row exists) and write single rows, and the result must be [serializable](/serializability/). With a fixed set of items and no conditions, locks on items are enough.
- The scheduler is [two-phase locking](/two-phase-locking/), usually [strict 2PL](/strict-two-phase-locking/). Predicate locks change what is locked, not the two-phase rule or the release at commit.
- The conditions belong to a class whose conflict test is cheap. Boxes (a range for each attribute) are tested in linear time. Arbitrary conditions with joins or functions are not, and the system must lock a coarser object instead.
- An index on the condition exists if you want the cheap forms: next-key and key-range locks are defined on the keys of an ordered index such as a [B-tree](/b-tree/).

## The template

A predicate here is a box: for some attributes, a closed interval of allowed values. A row with id $r$ and values $v$ is locked as the point box that fixes every attribute, including the id. A point box intersects a box $P$ exactly when the row satisfies $P$.

```pseudo id=main
INTERSECTS(P, Q)
L1  for each attribute a named by P or by Q
L2      if max(lo_P(a), lo_Q(a)) > min(hi_P(a), hi_Q(a)) then return false
L3  return true

REQUEST(T, mode, B)                ▷ mode is S or X, B is a box
L4  for each lock (U, m, C) in the lock table
L5      if U ≠ T and (m = X or mode = X) and INTERSECTS(B, C) then T waits for U
L6  when T waits for nobody, add (T, mode, B) to the lock table
L7  at the commit or abort of T, remove every lock of T
```

An attribute that a box does not name has the interval $(-\infty, \infty)$. Each action asks for these locks:

| action | locks |
|---|---|
| select the rows that satisfy $P$ | S on $P$ |
| insert row $r$ with values $v$ | X on the point $(r, v)$ |
| delete row $r$, whose values are $v$ | X on the point $(r, v)$ |
| update row $r$ from $v$ to $v'$ | X on $(r, v)$ and X on $(r, v')$ |
| update or delete a row $r$ that does not exist | S on the box $\mathit{id} = r$, then nothing |

**Why it works.** Call two actions in conflict when they cannot be swapped without a change in what a transaction sees or in the final state. A select of $P$ and a write conflict exactly when the write adds, removes or changes a row that satisfies $P$, before or after the write. The table makes every such write take an X lock on a point inside $P$: an insert locks the new values, a delete the old values, and an update both. So every conflicting pair of actions asks for conflicting locks, and the usual proof for [two-phase locking](/two-phase-locking/) applies: the order of the lock points of the transactions is a serial order that is equivalent to the run. The last line of the table is needed for the same reason. A write of a missing row is a read of the predicate "row $r$ exists", and it must wait for a transaction that has deleted $r$ and may still abort.

**Cost.** With $L$ locks in the table and $a$ attributes, a request costs $O(L a)$ time, because it is tested against every lock. A real lock manager cannot hash a predicate to a single bucket, which is the main reason why exact predicate locks are rare.

## Classic examples

**The phantom.** The table holds employees 1 and 2 in department 1 and employee 3 in department 2. $T_1$ selects department 1 twice, and $T_2$ inserts employee 4 in department 1 between the two selects.

| scheme | first select | insert of employee 4 | second select |
|---|---|---|---|
| row locks | rows 1, 2; S on rows 1 and 2 | X on row 4, granted | rows 1, 2, 4: a phantom |
| predicate locks | rows 1, 2; S on $\mathit{dept} = 1$ | X on the point (4, dept 1, ...), which is in the box; waits | rows 1, 2; $T_1$ commits, then $T_2$ |

If $T_2$ inserts employee 4 in department 2 instead, its point is outside the box, and the insert runs at once. An update that moves employee 3 from department 2 to department 1 waits as well, because its new point is inside the box. Row locks let that update in, and the second select of $T_1$ then sees employee 3.

**A random test.** The test file runs 1500 random workloads (seed 23) of two to four transactions with selects on boxes over the department and the salary, inserts, updates and deletes. Under predicate locks, every run gave the same select results and the same final table as the serial run in commit order; 181 runs needed a deadlock abort. Under row locks, 379 runs did not match the serial run in commit order, and 281 of them matched no serial order at all.

**Next-key locking.** On an index ordered by key, a scan of the range from $lo$ to $hi$ locks every key in the range and the first key after it. An insert of $k$ locks $k$ and the key just above $k$. This locks the predicate "key between $lo$ and $hi$" plus the gap up to the next key, which is a box that contains the predicate. The conflict test is now an equality test on key names, so the locks fit in an ordinary hashed lock table. The [phantom problem](/phantom-problem/) page runs this scheme.

## Variations

- **Precision locking.** Jordan, Banerjee and Batman (1981) keep read predicates and the rows that writers change, and test each update against the predicates, and each new predicate against the rows already updated. The test is between a predicate and a point, which is the easy case. The template above is close to this, since writes lock points.
- **Next-key locking.** ARIES/KVL (Mohan, 1990) and its successor for whole indexes lock index keys. A range is protected by the keys in it and the next key; the gap below a key is protected by that key.
- **Key-range locking.** Lomet (1993) gives lock modes that separate the key from the gap before it, so that an insert into a gap does not conflict with a reader of the key that bounds it.
- **Granular locks.** A lock on a page or a whole table is a predicate lock on a coarse box. Lock managers with intention locks mix them with row locks.
- **Locks that do not block.** In [serializable snapshot isolation](/serializable-snapshot-isolation/), readers take predicate locks (in practice on index ranges, pages or tables) only to record what they read. A conflicting write does not wait. It marks a read-write dependency, and the system aborts a transaction when two such dependencies form a dangerous structure.
- **Transactional data structures.** In transactional memory, a [read set](/read-set-and-write-set/) holds memory words, and a lookup of a missing key in a map reads no word that a later insert writes. Abstract locks on keys, as in transactional boosting, are predicate locks on the abstract state of the structure.

## Pitfalls

- **The general test is hard.** If predicates may be any Boolean formulas, deciding whether two of them can be true together contains satisfiability. Keep to a class with a fast test, such as boxes, or lock a coarser object.
- **Deletes and updates need the old values.** A delete must lock the row as it was, and an update must lock both the old and the new values. If the update locks only the new values, a row can leave a scanned predicate without a conflict.
- **A missing row is a predicate too.** An update of a row that does not exist reads "row $r$ exists". If it locks nothing, it can act on the uncommitted delete of another transaction that later aborts.
- **More deadlocks.** Predicates overlap more often than rows coincide, so waits and deadlocks are more frequent. The deadlock detector or a timeout must handle them; 181 of the 1500 random runs above had a deadlock.
- **No index, no range lock.** Next-key locking needs an index on the condition. A scan on an attribute without an index must lock the whole table to stay serializable.
- **Index locks are not structure locks.** Key locks protect the logical contents of an index. The pages of the tree still need latches or [lock coupling](/lock-coupling/), which are held for a short time and are not two-phase.
- **Phantoms are about predicates, not locks.** Moving to a lower isolation level, such as REPEATABLE READ in the SQL standard, removes the predicate locks and allows phantoms again. See [isolation levels](/isolation-levels/).

## Exercises

1. Show that the test at lines L1 to L3 is correct: two boxes share a point if and only if their intervals overlap on every attribute.
2. An update locks only the new values of the row. Give a schedule of a select and an update that is not serializable.
3. Give the predicate lock that a transaction needs for "count the employees with a salary above 50 in department 3". Which inserts must wait, and which may run?
4. Show that next-key locking locks a box that contains the predicate of a range scan. Give an insert that next-key locking blocks although it does not satisfy the predicate.
5. Two transactions each check that no booking for room 7 overlaps the hour from 10 to 11, and then insert such a booking. Show that predicate locks lead to a deadlock and not to a double booking.

## References
