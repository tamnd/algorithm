---
tag: ZVVV9H
kind: algorithm
slug: multiple-granularity-locking
name: Multiple granularity locking
aliases:
- intention locks
- hierarchical locking
- MGL
area: databases/transactions-and-concurrency
level: core
summary: "Lock the nodes of a hierarchy of database, tables and rows. Intention modes IS, IX and SIX on the ancestors let a coarse lock and a fine lock see each other with one test per node."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {d: the depth of the hierarchy, n: the number of rows under the locked node, k: the number of active transactions}
  time: {per-row-access: "O(d k) expected", per-subtree-lock: "O(d k) expected"}
  space: {extra: "O(d)"}
properties: {deterministic: true, online: true}
prereqs: [two-phase-locking, lock-table, readers-writer-lock]
see_also: [strict-two-phase-locking, key-range-locking, tree-locking-protocol, phantom-problem, predicate-locking, wait-for-graph, deadlock-detection, two-phase-locking-theorem]
sources:
  - paper: doi:10.1145/1282480.1282513
    title: J. N. Gray, R. A. Lorie and G. R. Putzolu, Granularity of locks in a large shared data base, Proceedings of the First International Conference on Very Large Data Bases (VLDB), 1975
    locator: the lock modes IS, IX, S, SIX and X, the compatibility matrix, and the rules for locking a hierarchy of resources from the root down
  - paper: "J. N. Gray, R. A. Lorie, G. R. Putzolu and I. L. Traiger, Granularity of locks and degrees of consistency in a shared data base, in G. M. Nijssen (ed.), Modelling in Data Base Management Systems, North-Holland, 1976"
    locator: the granular lock protocol for hierarchies and for directed acyclic graphs of resources, and its equivalence to locking the leaves
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (multigranularity locking and the intention modes)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (lock granularity and intention lock modes) and Chapter 8 (their implementation in the lock manager)
---

Multiple granularity locking (MGL) lets transactions lock data at different sizes: a whole database, a table, a page or one row. The data items form a tree, and a lock on a node covers every node below it. To make a lock on a table and a lock on one of its rows see each other, a transaction must first put an *intention* lock on every ancestor of the node it locks: IS (intention shared) before a shared lock below, IX (intention exclusive) before an exclusive lock below. With the five modes IS, IX, S, SIX and X and their compatibility matrix, the [lock table](/lock-table/) finds every conflict with one test per node on the path from the root. Gray, Lorie and Putzolu introduced the method in 1975 for System R. With the [two-phase](/two-phase-locking/) rule on top, the schedules are conflict serializable, exactly as if each transaction had locked every row that it covers.

## In plain words

Think of a building with floors and rooms. You can book a single room, or a whole floor at once. If you book a floor for a quiet meeting, nobody else may move furniture in any room of that floor. But the person who books one room does not walk past your floor booking at the desk; the clerk would have to check every room of the floor.

So each person who books a room first puts a small note on the floor and on the building: "someone is working in a room here". A person who wants the whole floor sees the notes and knows at once whether a room is in use. Notes go on from the top down, and come off from the bottom up. Notes do not clash with other notes, only with real bookings.

## The problem

The input is a stream of transactions that read and write rows of tables. Some of them touch a few rows, and some scan or update whole tables. The scheduler must give conflict serializable schedules, as [two-phase locking](/two-phase-locking/) does for single items.

Locks on rows only are correct but expensive: a scan of a table with $n$ rows takes $n$ locks. Locks on tables only are cheap but give little concurrency: two transactions that write different rows of a table wait for each other. MGL allows both sizes at the same time. The hard part is the conflict between a coarse lock and a fine lock on different nodes: S on a table and X on one of its rows. The model is one site with a lock table in main memory, and items form a tree of known shape, with the database at the root.

## The algorithm

The five modes have these meanings:

- **IS**: the transaction will take S locks on some nodes below.
- **IX**: the transaction will take X (or S) locks on some nodes below.
- **S**: the transaction reads the whole subtree.
- **SIX**: S and IX together; the transaction reads the whole subtree and writes some nodes below, which it locks in X.
- **X**: the transaction writes the whole subtree.

Two locks of different transactions on the same node are compatible as in this table:

| held \ requested | IS | IX | S | SIX | X |
|---|---|---|---|---|---|
| IS | yes | yes | yes | yes | no |
| IX | yes | yes | no | no | no |
| S | yes | no | yes | no | no |
| SIX | yes | no | no | no | no |
| X | no | no | no | no | no |

The table follows from the meanings. Two intentions never clash, since the real conflict, if any, shows up on a node lower down. A real access to the subtree (S, the S part of SIX, or X) clashes with a real access of the other side when one of the two is a write. It also clashes with an intention of the other side when one of the two is about writes: S clashes with IX, and X clashes with IS and IX. The modes are ordered IS < IX < SIX < X and IS < S < SIX, and the supremum of IX and S is SIX. A transaction that holds S on a table and now wants to write a row converts its table lock to SIX.

```pseudo id=main
LOCK(T, v, m)                                    ▷ m in IS, IX, S, SIX, X
L1  if v is not the root and the lock of T on parent(v) is weaker than IS (for m in IS, S)
       or weaker than IX (for m in IX, SIX, X) then reject the request
L2  m' ← sup(the mode of T on v, m)
L3  if m' is not compatible with the lock of each other transaction on v then
L4      T waits, with an edge to each holder that blocks m'
L5  else grant m' to T on v

LOCK-SUBTREE(T, v, m)                            ▷ how a transaction uses LOCK
L6  for each proper ancestor u of v, from the root down do
        LOCK(T, u, IX if m in IX, SIX, X, else IS)
L7  LOCK(T, v, m)

UNLOCK(T, v)
L8  reject if T holds a lock on a child of v      ▷ release from the leaves up
L9  at commit or abort (strict 2PL): release all locks of T, deepest nodes first
```

The usual operations become:

| operation | locks |
|---|---|
| read row $r$ of table $t$ | IS on the database, IS on $t$, S on $r$ |
| write row $r$ of table $t$ | IX on the database, IX on $t$, X on $r$ |
| scan table $t$ | IS on the database, S on $t$ |
| scan $t$ and update some rows | IX on the database, SIX on $t$, X on each row it writes |
| rewrite all of $t$ | IX on the database, X on $t$ |

A transaction may hold a lock on a node that a stronger lock above already covers, for example S on a row under its own S on the table. It is redundant and harmless. Line L1 is a little more permissive than the rule of Gray, Lorie and Putzolu, which asks for exactly IS or IX on the parent: here any mode at least IS (or at least IX) is enough, so a transaction that holds S on a table may still lock a row in S.

## Example

Take a database with tables A and B, each with rows 1 and 2.

| step | request | result | why |
|---|---|---|---|
| 1 | $T_1$: IX db, SIX A, X A1 | granted | $T_1$ reads table A and updates row A1 |
| 2 | $T_2$: IS db, IS A, S A2 | granted | IS is compatible with SIX; $T_2$ and $T_1$ both read A2 |
| 3 | $T_3$: IS db, S A | waits for $T_1$ | S is not compatible with SIX: $T_1$ writes a row of A |
| 4 | $T_4$: IX db, IX B, X B1 | granted | IX on db is compatible with IX and IS; table B is free |
| 5 | $T_2$: IX db, IX A | waits for $T_1$ | $T_2$ wants to write A2 too; IX is not compatible with SIX |

After step 5 the [wait-for graph](/wait-for-graph/) has the edges $T_3 \to T_1$ and $T_2 \to T_1$. When $T_1$ commits and releases X on A1, then SIX on A, then IX on db, $T_2$ gets IX on A at once, and $T_3$ still waits: S on A is not compatible with the IX of $T_2$.

At step 3, the conflict between the scan of $T_3$ and the row write of $T_1$ is found on node A, with one test, although the two transactions never name the same row. Without the intention locks, $T_3$ would hold S on A and $T_1$ X on A1, and both would be granted.

**A deadlock.** Let $T_1$ rewrite table A and then table B, and $T_2$ rewrite B and then A. $T_1$ holds X on A and waits for X on B, which $T_2$ holds while it waits for A. MGL does not prevent deadlocks, and the tests find them with the wait-for graph.

## Correctness

The proof is on [the proof page](proofs/correctness.md). Say that $T$ *implicitly* holds S on a leaf $\ell$ when it holds S, SIX or X on $\ell$ or on an ancestor of $\ell$, and implicitly holds X on $\ell$ when it holds X on $\ell$ or on an ancestor.

- **The parent rule holds at all times.** Line L1 checks it when a lock is granted, conversions only make the parent lock stronger, and line L8 keeps a parent lock until the locks below it are gone.
- **Implicit locks never conflict.** Suppose $T$ implicitly holds X on $\ell$ through node $a$, and $U$ implicitly holds S or X on $\ell$ through node $b$. Both nodes are on the path from the root to $\ell$. If $a = b$, the modes on that node conflict. If $a$ is above $b$, then $U$ holds some lock on $a$ by the parent rule, and nothing is compatible with X. If $b$ is above $a$, then $T$ holds at least IX on $b$, and IX, SIX and X are not compatible with S, SIX or X. In each case the lock table would hold two conflicting locks on one node, which it never does.
- **Serializability.** So the implicit locks on the leaves behave as S and X locks of two-phase locking: each read or write of a row runs under an implicit lock of the right mode, and two conflicting implicit locks are never held at the same time. With strict 2PL, every implicit lock is held to the end of the transaction, so by the [two-phase locking theorem](/two-phase-locking-theorem/) the committed projection is conflict serializable, and the schedule is [strict](/strict-schedule/).

## Complexity

- **Locks per access.** A row access takes $d + 1$ lock requests on a hierarchy of depth $d$, one per node on the path. A scan of a subtree with $n$ rows takes $d + 1$ requests instead of the $n$ row locks of flat locking. Requests for the upper nodes are usually conversions that do nothing, because the transaction already holds the intention lock.
- **Time per request.** The test of line L3 compares the new mode with each other holder, $O(k)$ for $k$ holders, or $O(1)$ with a count of each mode in the lock entry. The lookup of the node is $O(1)$ expected with a hash table.
- **Space.** One lock entry per locked node. The upper nodes, the database and the tables, have many holders in IS and IX at a time, which is why their entries need counts per mode.

## Properties

- **Output class.** With strict 2PL, conflict serializable and strict.
- **Same schedules as row locking.** The proof shows that MGL is equivalent to locking every covered leaf, so it gives the serializability of row locking with the lock count of table locking.
- **Deadlocks.** MGL can deadlock, as in the example, and also in new ways: two transactions that hold S on the same table and both convert to SIX wait for each other. A deadlock detector or a timeout is needed.
- **Phantoms at table level.** An insert of a row into table $t$ needs IX on $t$, which is not compatible with S on $t$. So a scan that locks the whole table in S sees no [phantoms](/phantom-problem/) in that table. Row locks alone do not stop phantoms; [key-range locking](/key-range-locking/) does that at row level.

## Variants and improvements

- **Directed acyclic graphs.** Gray, Lorie, Putzolu and Traiger (1976) extend the rules to a DAG of resources, for example a row that is reached both through its table and through an index. To lock a node in S, a transaction needs an intention lock on at least one parent; to lock it in X, on every parent.
- **Lock escalation.** When a transaction holds too many row locks under one table, the lock manager converts its table lock from IS or IX to S or X and drops the row locks. This saves memory, and it can cause waits and deadlocks that the rows alone would not cause.
- **Update mode.** Many systems add a U mode for a read that will probably be followed by a write; see the [lock table](/lock-table/) page.
- **Key ranges in indexes.** In a B+ tree index, the keys and the gaps between them are the leaves under the index node, and [key-range locking](/key-range-locking/) locks them with modes of the same kind.
- **Degrees of consistency.** The 1976 paper also defines degrees of consistency 0 to 3 by how long read and write locks are held. They are the root of the SQL [isolation levels](/isolation-levels/).

## When to use it

Use MGL in any locking system with data at several sizes, which in practice means every relational system that locks: point updates lock rows, and scans, bulk loads and schema changes lock tables. It pays when one workload has both short transactions that touch a few rows and long ones that touch large parts of a table. When all access is by row, flat row locking with an IX on the table is the whole story. When the data is a tree that is always searched from the root, the [tree locking protocol](/tree-locking-protocol/) releases locks earlier.

## Pitfalls

- **A missing intention lock.** Every ancestor needs its intention lock, from the root down. A row lock without IX on its table is invisible to a transaction that locks the table.
- **A release from the top.** If $T$ releases its IX on a table while it holds X on a row, another transaction can lock the table in S and read the row that $T$ writes. Release from the leaves up, or all at once at the end.
- **IS for a write.** A transaction that read a row under IS on the table and now writes it must convert the table lock to IX before it locks the row in X. Line L1 rejects the request otherwise.
- **Conversion deadlocks.** Two transactions that both scan a table in S and then want to update a row both ask for SIX, and each waits for the S of the other. Take SIX at the start if the update is likely.
- **Escalation surprises.** An escalation in the middle of a transaction can make it wait for a table lock that it did not plan for.

## Implementations

## History

Gray, Lorie and Putzolu presented granular locks with the modes IS, IX, S, SIX and X at the first VLDB conference in 1975, from the System R project at IBM San Jose. The longer paper by Gray, Lorie, Putzolu and Traiger (1976) gave the rules for DAGs and argued that the protocol is equivalent to locking the leaves, and it also defined the degrees of consistency. The method has been part of the lock manager of almost every relational system since. Bernstein, Hadzilacos and Goodman (1987) and Gray and Reuter (1993) give the textbook treatment.

## References
