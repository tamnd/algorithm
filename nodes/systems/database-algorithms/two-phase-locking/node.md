---
tag: JSBTG5
kind: algorithm
slug: two-phase-locking
name: Two-phase locking
aliases:
- 2PL
- basic two-phase locking
area: systems/database-algorithms
level: core
summary: "Lock each item before use and never lock again after the first unlock. Every schedule it allows is conflict serializable, in the order of the lock points."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {k: the number of active transactions, d: the number of locked items}
  time: {per-lock-request: "O(k)", per-deadlock-check: "O(k^2)"}
  space: {extra: "O(k d)"}
properties: {deterministic: true, online: true}
prereqs: [conflict-serializability, readers-writer-lock, concurrency-control]
see_also: [strict-two-phase-locking, wait-die-and-wound-wait, timestamp-ordering, wait-for-graph, deadlock-detection, phantom-problem, two-phase-commit, lock-coupling]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the definition of two-phase transactions, the theorem that two-phase transactions give consistent (serializable) schedules, and the converse for transactions that are not two-phase
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (two phase locking, the proof by lock points, deadlocks, conservative and strict 2PL)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (locking schedulers, 2PL and its variants, deadlock handling)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (isolation, two-phase locking and degrees of isolation) and Chapter 8 (lock implementation)
---

Two-phase locking (2PL) is the classic locking method for [concurrency control](/concurrency-control/) in databases. Each transaction takes a shared lock on an item before it reads it and an exclusive lock before it writes it, and it obeys one rule: once it has released any lock, it never acquires another. So its life has a growing phase and a shrinking phase. Eswaran, Gray, Lorie and Traiger proved in 1976 that every schedule allowed by these rules is [conflict serializable](/conflict-serializability/), and that the order of the *lock points* (the moment each transaction gets its last lock) is an equivalent serial order. 2PL can deadlock, so it needs deadlock detection or prevention, and the basic form allows cascading aborts, which [strict 2PL](/strict-two-phase-locking/) removes.

## In plain words

Think of a library where you must hold a token for each book you use. Many people can hold a reading token for the same book, but a writing token is for one person only, and nobody else may hold any token for that book at the same time. The rule of two-phase locking is simple: you collect tokens for a while, and from the first time you give a token back, you may not take any new token.

This rule is enough to make the result look as if people had used the library one at a time. Their order is the moment each person collected their last token. The price is that two people can each hold a token the other one needs and wait forever, so the library must notice this and send one of them back to start again.

## The problem

The input is a stream of actions $r_i(x)$ and $w_i(x)$ from concurrent transactions, each followed by a commit. The scheduler must decide, for each action, to run it now, to delay it, or to abort its transaction, so that the committed projection of the output schedule is conflict serializable. Two actions conflict if they are in different transactions, touch the same item, and at least one is a write. The scheduler does not know the programs; it knows only which item each action touches and whether it reads or writes. The model is a single site with a lock table in main memory, a word RAM with hashing.

## The algorithm

The lock table holds, for each item, the transactions that hold a lock on it and the mode, S (shared) or X (exclusive). Two locks on the same item by different transactions are compatible only if both are S. A transaction that reads and then writes the same item upgrades its S lock to X. A transaction that waits for a lock held by another transaction adds an edge to the [wait-for graph](/wait-for-graph/).

```pseudo id=main
TWO-PHASE-LOCKING(T_i asks to run p_i(x))
L1  m ← S if p is a read, X if p is a write
L2  if T_i holds no lock on x of mode m or X then
L3      require that T_i has released no lock          ▷ the two-phase rule
L4      while another transaction holds a lock on x that conflicts with m do
            T_i waits; add the edge T_i → holder to the wait-for graph
L5          if the wait-for graph has a cycle then abort and restart the youngest transaction on a cycle
L6      grant the lock (x, m) to T_i
L7  run p_i(x)
L8  if T_i holds every lock it will need then          ▷ past its lock point
        T_i may release its locks on items it will not touch again
L9  when T_i has no actions left: commit, then release all its locks
```

Line L8 is where 2PL differs from its strict form. In basic 2PL a transaction that knows it is past its lock point may unlock early, which lets others in sooner. A real system usually cannot know that a transaction will ask for no more locks, so practical systems hold locks until commit ([strict 2PL](/strict-two-phase-locking/)). Line L5 shows deadlock *detection*; [wait-die and wound-wait](/wait-die-and-wound-wait/) replace it with deadlock *prevention*.

## Example

**A trace with an early release.** Let $T_1 = r_1(x)\, w_1(x)\, w_1(y)$ and $T_2 = r_2(x)\, w_2(z)$, and let $T_1$ run first.

| step | event | lock table after the step |
|---|---|---|
| 1 | $T_1$ locks $x$ in S, runs $r_1(x)$ | $x$: $T_1$ S |
| 2 | $T_1$ upgrades $x$ to X, runs $w_1(x)$ | $x$: $T_1$ X |
| 3 | $T_1$ locks $y$ in X, runs $w_1(y)$; this is its lock point | $x$, $y$: $T_1$ X |
| 4 | $T_1$ needs no more items and releases $x$ and $y$ | empty |
| 5 | $T_2$ locks $x$ in S, runs $r_2(x)$ | $x$: $T_2$ S |
| 6 | $T_2$ locks $z$ in X, runs $w_2(z)$ | $x$: $T_2$ S, $z$: $T_2$ X |
| 7 | $T_1$ commits, then $T_2$ commits and releases its locks | empty |

The schedule $r_1(x)\, w_1(x)\, w_1(y)\, r_2(x)\, w_2(z)\, c_1\, c_2$ is conflict equivalent to $T_1 T_2$, the order of the lock points (steps 3 and 6). But $T_2$ read $x$ from $T_1$ before $T_1$ committed. If $T_1$ had aborted at step 7, $T_2$ would have to abort too. This is a cascading abort, and it is the reason why systems use strict 2PL.

**A deadlock.** Let $T_1 = r_1(x)\, w_1(y)$ and $T_2 = r_2(y)\, w_2(x)$, and let the actions arrive in the order $r_1(x)$, $r_2(y)$, $w_1(y)$, $w_2(x)$. After the two reads, $T_1$ holds S on $x$ and $T_2$ holds S on $y$. Now $T_1$ waits for $T_2$ (it needs X on $y$) and $T_2$ waits for $T_1$ (it needs X on $x$). The wait-for graph has the cycle $T_1 \to T_2 \to T_1$, and line L5 aborts the younger $T_2$, which has released nothing and whose effects nobody has seen. $T_1$ finishes, then $T_2$ runs again. Without the locks, this interleaving would be the non-serializable schedule $r_1(x)\, r_2(y)\, w_1(y)\, w_2(x)$.

**A serializable schedule that 2PL refuses.** $S = r_1(x)\, w_2(x)\, w_3(y)\, w_1(y)$ is conflict serializable: its edges are $T_1 \to T_2$ (on $x$) and $T_3 \to T_1$ (on $y$), so it is equivalent to $T_3 T_1 T_2$. But no 2PL execution produces it. $T_1$ must release $x$ before $w_2(x)$. $T_1$ cannot hold a lock on $y$ before $w_3(y)$, since it keeps that lock until $w_1(y)$, which comes after $w_3(y)$. So $T_1$ must lock $y$ after $w_3(y)$, which is after it released $x$, and this breaks the two-phase rule.

## Correctness

The full proof is in the proof file; here is the core. Take an edge $T_i \to T_j$ of the [conflict graph](/conflict-graph/) of the committed projection, from conflicting actions $p_i(x)$ before $q_j(x)$. The locks that cover the two actions conflict, each is held from before its action until after it, and two conflicting locks are never held at the same time. So $T_i$ releases $x$ before $T_j$ acquires its lock on $x$. With the two-phase rule this gives

$$\mathrm{LP}(T_i) < \mathrm{release}_i(x) < \mathrm{acquire}_j(x) \le \mathrm{LP}(T_j).$$

Every edge goes forward in lock-point order, so the graph has no cycle, and the schedule is conflict equivalent to the serial schedule in that order. A deadlock victim waits for a lock, so by the two-phase rule it has released nothing yet; no other transaction has seen its writes, and its abort is undone by restoring before images. The converse also holds (Eswaran et al.): for any transaction that unlocks $x$ and later locks $y$, some two-phase partner transaction and some legal interleaving give a cycle.

## Complexity

- **Per action.** With a hash table from items to lock entries, a lock request or release costs $O(1)$ expected time plus a compatibility check against the current holders, $O(k)$ in the worst case for $k$ active transactions. A transaction with $a$ actions makes at most $a$ requests and $a$ releases.
- **Deadlock detection.** The wait-for graph has at most $k$ nodes and, with S locks, up to $k^2$ edges. A depth-first search costs $O(k + e)$, so $O(k^2)$. Systems run it on each wait, periodically, or not at all (and use timeouts).
- **Space.** The lock table holds one entry per locked item and holder, $O(k d)$ for $d$ locked items.
- **Concurrency.** The cost that matters in practice is waiting, not bookkeeping. A transaction holds each lock from first use to (at least) its lock point, so a long transaction that touches a popular item blocks everyone else for that time.

## Properties

- **Output class.** Every committed projection is conflict serializable; with deadlock detection, every transaction that is not chosen as a victim finishes.
- **Not recoverable in general.** Basic 2PL can let a transaction read uncommitted data (the first example), so the schedule may cause cascading aborts. Strict 2PL gives strict schedules.
- **Deadlocks.** 2PL meets the [Coffman conditions](/coffman-conditions/) (mutual exclusion, hold and wait, no preemption, circular wait are all possible), so it can [deadlock](/deadlock/). The scheduler must detect deadlocks with the wait-for graph ([deadlock detection](/deadlock-detection/)), prevent them by ordering ([deadlock prevention](/deadlock-prevention/), [wait-die and wound-wait](/wait-die-and-wound-wait/)), or use timeouts.
- **Pessimistic.** It delays a transaction as soon as a conflict might arise, unlike [optimistic concurrency control](/optimistic-concurrency-control/), which checks at commit.
- **Incomparable with timestamp ordering.** 2PL and [basic timestamp ordering](/timestamp-ordering/) each accept schedules that the other rejects (see the bounds on the [concurrency control](/concurrency-control/) page).

## Variants and improvements

- **Strict and rigorous 2PL.** Hold all X locks (strict) or all locks (rigorous) until commit or abort. Almost every locking database uses one of these. See [strict two-phase locking](/strict-two-phase-locking/).
- **Conservative (static) 2PL.** A transaction declares and acquires all its locks before it starts, all at once or not at all. It never deadlocks (no hold and wait), but it needs the full read and write sets in advance and holds locks longer.
- **Deadlock prevention by timestamps.** [Wait-die and wound-wait](/wait-die-and-wound-wait/) let a transaction wait only in one direction of age, so no cycle can form.
- **Multiple granularity locking.** Gray, Lorie and Putzolu (VLDB 1975) added intention locks on a hierarchy (database, table, page, row), so a transaction can lock a whole table or a single row. The two-phase rule is unchanged.
- **Predicate and key-range locks.** Locks on items do not stop inserts of new rows that match a query. [Predicate locking](/predicate-locking/) and its index-based forms solve the [phantom problem](/phantom-problem/).
- **Lock coupling is not 2PL.** [Lock coupling](/lock-coupling/) in a B-tree releases the parent lock as soon as the child is locked, so it breaks the two-phase rule on purpose. It is safe for one structure because access follows the tree, a fact proved for the tree protocol of Silberschatz and Kedem (1980); it does not serialize general transactions.
- **Distributed 2PL.** Each site runs 2PL on its own items, and the transaction ends with [two-phase commit](/two-phase-commit/). The two protocols do different jobs: 2PL orders conflicting transactions (isolation), and 2PC makes all sites agree to commit or abort (atomicity). Strict 2PL with 2PC keeps locks until the commit decision reaches each site.

## When to use it

Use a two-phase locking scheduler, in its strict form, when conflicts are frequent enough that aborting and retrying would waste much work, and when transactions are short. It is the default serializable method of many relational systems. When reads dominate and long reads must not block writers, a [multiversion](/multiversion-concurrency-control/) scheme is usually better. When conflicts are rare, [optimistic concurrency control](/optimistic-concurrency-control/) avoids the lock table work.

## Pitfalls

- **Release before the lock point.** A transaction that releases a lock and then asks for another one is no longer two-phase, and Theorem 2 of the proof shows that a partner exists that makes the schedule non-serializable. Early release is only safe if the system knows that no more locks will be needed.
- **Cascading aborts.** Basic 2PL releases X locks before commit. Do not use it where a transaction can abort after its lock point; use strict 2PL.
- **Locks on rows are not enough.** A scan that locks the rows it sees does not stop another transaction from inserting a new matching row. This is the [phantom problem](/phantom-problem/).
- **Victim choice and starvation.** If the victim is chosen badly, the same transaction can be aborted again and again ([starvation](/starvation/)). Choosing the youngest transaction on the cycle, and keeping the original age on restart, means the oldest transaction is never chosen.
- **Upgrade deadlocks.** Two transactions that both read and then write the same item both hold S and both wait for X. Update locks (a mode that is compatible with S but not with itself) avoid this common case.
- **Not the same as 2PC.** The names are close, but [two-phase commit](/two-phase-commit/) is a protocol for atomic commitment across sites. It neither takes nor orders locks.
- **Not the same as a readers-writer lock.** The S and X modes are a [readers-writer lock](/readers-writer-lock/) on each item. What makes the method correct is the two-phase rule across many such locks, not the lock itself. In software [transactional memory](/transaction/), [TL2](/tl2/) locks its write set only at commit time and validates its read set with version numbers instead of read locks, so it is not 2PL on reads.

## Implementations

## History

Eswaran, Gray, Lorie and Traiger at IBM Research defined two-phase transactions in the 1976 CACM paper, from the work on System R. They proved that two-phase transactions give consistent schedules and that the rule cannot be weakened if the scheduler knows only the items. The same paper introduced predicate locks for the phantom problem. Gray, Lorie and Putzolu described lock modes and multiple granularity in the same years. Bernstein, Hadzilacos and Goodman (1987) gave the textbook proof with lock points that is used above. Strict 2PL, with locks held to commit, became the standard form in commercial locking systems.

## References
