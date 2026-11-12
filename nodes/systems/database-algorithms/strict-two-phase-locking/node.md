---
tag: 4829PV
kind: algorithm
slug: strict-two-phase-locking
name: Strict two-phase locking
aliases:
- strict 2PL
- rigorous 2PL
- strong strict two-phase locking
area: systems/database-algorithms
level: core
summary: "Two-phase locking that keeps exclusive locks until commit or abort. Schedules are strict, so no cascading aborts; the rigorous form keeps all locks and serializes in commit order."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {k: the number of active transactions, d: the number of locked items, w: the number of writes of one transaction}
  time: {per-lock-request: "O(k)", per-deadlock-check: "O(k^2)", per-abort: "O(w)"}
  space: {extra: "O(k d)"}
properties: {deterministic: true, online: true}
prereqs: [two-phase-locking]
see_also: [two-phase-locking, wait-die-and-wound-wait, phantom-problem, isolation-levels, crash-recovery, write-ahead-logging, two-phase-commit, multiversion-concurrency-control]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (strict histories and undo by before images) and Chapter 3 (strict two phase locking)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (strict and strong strict 2PL) and Chapter 11 (schedules with aborts, strictness and recoverability)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (degrees of isolation; degree 3 holds all locks to the end of the transaction)
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: two-phase transactions and the discussion of releasing locks at the end of a transaction so that its updates can be backed out
---

Strict two-phase locking is [two-phase locking](/two-phase-locking/) with one more rule: a transaction keeps every exclusive lock until it commits or aborts. *Rigorous* (or strong strict) 2PL keeps every lock, shared ones too, until the end. Both still produce [conflict serializable](/conflict-serializability/) schedules, and in addition the schedules are *strict*: no transaction reads or overwrites data that an unfinished transaction wrote. So an abort never forces another abort, and recovery can undo a transaction by restoring the old values of what it wrote. This is the form of locking that real database systems use.

## In plain words

Basic two-phase locking lets a transaction hand back a lock early, once it knows it will not need new locks. That is risky. Another transaction can then read a value that the first one wrote, and if the first one later cancels, the second one has used a value that never really existed, so it must be cancelled too.

Strict two-phase locking removes that risk. A transaction keeps the lock on anything it changed until it is finished. Nobody can see its changes before they are final, and if it cancels, the system simply puts the old values back. The rigorous form also keeps read locks to the end. Then the order in which transactions finish is itself a correct serial order, which is handy for logs and for systems with many sites.

## The problem

The input is a stream of actions $r_i(x)$, $w_i(x)$, commit requests and abort requests from concurrent transactions. The scheduler must run, delay or abort actions so that the committed projection of the output is conflict serializable and the whole schedule, with its aborts, is *strict* (see [serializability](/serializability/)): if $w_j(x)$ comes before a read or write of $x$ by another transaction, then $T_j$ has committed or aborted in between. Strictness is what lets [crash recovery](/crash-recovery/) undo a transaction with before images in the [write-ahead log](/write-ahead-logging/). The model is a single site with a lock table in main memory, a word RAM with hashing.

## The algorithm

Locks have the modes S (shared) and X (exclusive), and two locks on the same item by different transactions are compatible only if both are S. Before each write, the scheduler saves the before image of the item, in practice as an undo record of the log.

```pseudo id=main
STRICT-2PL(T_i asks to run p_i(x))              ▷ rigorous: skip L7
L1  m ← S if p is a read, X if p is a write
L2  if T_i holds no lock on x of mode m or X then
L3      while another transaction holds a lock on x that conflicts with m do
            T_i waits; add the edge T_i → holder to the wait-for graph
L4          if the wait-for graph has a cycle then abort the youngest transaction on a cycle
L5      grant the lock (x, m) to T_i
L6  if p is a write then save the before image of x
    run p_i(x)
L7  if T_i holds all its locks then release its S locks on items it will not read again
L8  on commit of T_i: write the commit record, then release all locks of T_i
L9  on abort of T_i: restore its before images in reverse order, then release all its locks
```

Line L8 is the essential change from [basic 2PL](/two-phase-locking/). The order inside it matters: in a system with a log, the commit record must be durable before the X locks are released, or a crash could lose a commit whose results other transactions have already read. Line L4 is deadlock detection with the [wait-for graph](/wait-for-graph/); [wait-die and wound-wait](/wait-die-and-wound-wait/) can replace it.

## Example

**A reader waits for the commit.** Let $T_1 = r_1(x)\, w_1(x)\, w_1(y)$ and $T_2 = r_2(x)\, w_2(z)$, and let $T_1$ start first. Basic 2PL can release $x$ right after $w_1(y)$ and let $T_2$ read it before $c_1$. Strict 2PL keeps the X lock on $x$ until $c_1$:

| step | event | lock table after the step |
|---|---|---|
| 1 | $T_1$ locks $x$ in S, runs $r_1(x)$ | $x$: $T_1$ S |
| 2 | $T_1$ upgrades to X, saves $x$, runs $w_1(x)$ | $x$: $T_1$ X |
| 3 | $T_1$ locks $y$ in X, saves $y$, runs $w_1(y)$ | $x$, $y$: $T_1$ X |
| 4 | $T_2$ asks for S on $x$ and waits for $T_1$ | unchanged |
| 5 | $T_1$ commits and releases $x$ and $y$ | empty |
| 6 | $T_2$ locks $x$ in S, runs $r_2(x)$, then $w_2(z)$, commits | empty at the end |

The schedule is $r_1(x)\, w_1(x)\, w_1(y)\, c_1\, r_2(x)\, w_2(z)\, c_2$, which is strict.

**An abort undone by before images.** Let $T_1 = w_1(x)\, w_1(y)$ and $T_2 = r_2(x)$, with $x = x_0$ at the start. $T_1$ writes $x$ and saves $x_0$. $T_2$ asks for S on $x$ and waits. Then $T_1$ aborts: line L9 sets $x$ back to $x_0$ and releases the lock, and $T_2$ reads $x_0$. Nobody saw the value of the aborted write, so no other transaction has to abort.

**Strict versus rigorous.** Let $T_1 = r_1(x)\, w_1(y)\, r_1(z)$ and $T_2 = w_2(x)$. Under strict 2PL, after $r_1(z)$ the transaction $T_1$ holds all its locks and will not read $x$ again, so it releases its S lock on $x$. $T_2$ now writes $x$ and commits before $c_1$. The schedule is serializable as $T_1 T_2$ (because $r_1(x) < w_2(x)$), but the commit order is $T_2, T_1$. Under rigorous 2PL, $T_2$ waits until $c_1$, and the commit order is a valid serial order.

## Correctness

The proof file has the details.

- **Serializability.** Strict and rigorous 2PL only delay releases, so they still obey the two-phase rule. The lock-point argument of [two-phase locking](/two-phase-locking/) applies: each edge $T_i \to T_j$ of the [conflict graph](/conflict-graph/) of the committed projection has $\mathrm{LP}(T_i) < \mathrm{LP}(T_j)$.
- **Strictness.** If $w_j(x)$ comes before an action of $T_i$ on $x$, the X lock of $T_j$ must be gone before $T_i$ gets its lock, and that happens only at the end of $T_j$.
- **Undo.** From its first write of $x$ to its end, $T_j$ holds X on $x$, so nobody else reads or writes $x$ in that time. Restoring the before images in reverse order gives back the value before $T_j$ and erases nothing that another transaction did.
- **Commit order (rigorous).** For an edge $T_i \to T_j$, the transaction $T_i$ releases its lock on $x$ only at $c_i$, before $T_j$ gets the conflicting lock, so $c_i < c_j$. The commit order is a valid serial order.

## Complexity

- **Per action.** The same as basic 2PL: $O(1)$ expected hash work per request plus a compatibility check against at most $k$ holders. Saving a before image is $O(1)$ per write.
- **Commit and abort.** Releasing all locks of a transaction costs $O(\ell)$ for $\ell$ locks. An abort also restores $w$ before images, $O(w)$.
- **Deadlock detection.** $O(k + e)$, up to $O(k^2)$, per search of the wait-for graph.
- **Concurrency.** Locks are held longer than in basic 2PL, from first use until the commit record is on disk. That is the real cost, and it is why [group commit](/group-commit/) and short transactions matter for throughput.

## Properties

- **Output class.** Conflict serializable and strict, so also avoids cascading aborts and recoverable.
- **Commit order.** Rigorous 2PL produces schedules in which the commit order is a serialization order. This makes it easy to combine with [two-phase commit](/two-phase-commit/) across sites: each site serializes in commit order, and 2PC makes all sites agree on that order. Strict 2PL alone does not guarantee it.
- **Isolation level.** Rigorous 2PL with locks on predicates or key ranges gives the SERIALIZABLE level; the same scheme with short read locks gives READ COMMITTED (see [isolation levels](/isolation-levels/)). Gray's degree 3 consistency is rigorous 2PL.
- **Deadlocks.** As with basic 2PL, deadlocks can happen and must be detected or prevented.
- **Pessimistic and single-version.** Readers block writers and writers block readers. [Multiversion concurrency control](/multiversion-concurrency-control/) removes the reader-writer blocking at the cost of keeping old versions.

## Variants and improvements

- **Strict versus rigorous.** Strict holds X locks to the end; rigorous holds all locks to the end. Rigorous is simpler, since the scheduler never needs to know that a transaction has reached its lock point, and that is what most systems implement.
- **Deadlock handling.** Detection with the wait-for graph (above), prevention with [wait-die or wound-wait](/wait-die-and-wound-wait/), or timeouts. Conservative 2PL with strictness avoids deadlocks but needs the lock set in advance.
- **Granularity and phantoms.** Locks on tables, pages and rows with intention locks; key-range or [predicate locks](/predicate-locking/) against the [phantom problem](/phantom-problem/).
- **Early lock release.** Some systems release locks when the commit record is in the log buffer, before it is on disk, and make dependent transactions wait for that log flush before they commit. This keeps the result recoverable while shortening lock hold times.
- **Short read locks.** Releasing S locks right after each read is not two-phase. It gives the READ COMMITTED level, not serializability.

## When to use it

Use rigorous 2PL as the default locking scheduler of a single-version database that must offer serializable transactions, and whenever recovery undoes transactions with before images. Use the strict but not rigorous form only when the scheduler can tell that a transaction will not lock again, for example with predeclared lock sets. Consider [multiversion concurrency control](/multiversion-concurrency-control/) or [optimistic concurrency control](/optimistic-concurrency-control/) when long read-only transactions or rare conflicts make the blocking cost too high.

## Pitfalls

- **Releasing before the commit is durable.** If X locks go away when the commit is decided but before the log record is on disk, another transaction can read the data and commit, and a crash can then undo the first transaction but not the second.
- **Assuming the commit order is the serial order.** That holds for rigorous 2PL, not for strict 2PL with early release of S locks (third example above).
- **Upgrade deadlocks.** Two transactions that read and then write the same item both hold S and both wait for X. Update locks avoid this.
- **Phantoms.** Holding row locks to commit does not stop inserts of new rows that match a query; see the [phantom problem](/phantom-problem/).
- **Confusing it with two-phase commit.** Strict 2PL is a local locking rule. [Two-phase commit](/two-phase-commit/) is an atomic commitment protocol across sites. A distributed database usually runs both: strict 2PL at each site, and 2PC to decide the outcome before the locks are released.
- **Not the transactional memory rule.** Software [transactional memory](/transaction/) systems such as [TL2](/tl2/) lock the write set only during commit and do not take read locks at all. They give [opacity](/opacity/) by validation, not by holding locks for the whole transaction.

## Implementations

## History

Eswaran, Gray, Lorie and Traiger (1976) already observed that a transaction should keep its locks until its end, so that its updates can be backed out without affecting others; the System R lock manager held write locks to commit. Gray's degrees of consistency (Gray, Lorie, Putzolu and Traiger, 1976) defined degree 3 as holding all locks to the end. Bernstein, Hadzilacos and Goodman (1987) gave the theory of strict histories and the proof that strict 2PL produces them. The name *rigorous* comes from Breitbart, Georgakopoulos, Rusinkiewicz and Silberschatz (1991), who used the commit-order property for multidatabase systems. Weikum and Vossen call the same protocol strong strict 2PL.

## References
