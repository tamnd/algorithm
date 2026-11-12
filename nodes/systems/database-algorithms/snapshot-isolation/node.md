---
tag: ZZY45M
kind: definition
slug: snapshot-isolation
name: Snapshot isolation
aliases:
- SI
- snapshot isolation level
- first-committer-wins isolation
area: systems/database-algorithms
level: core
summary: "Each transaction reads the committed state as of its start and commits only if no concurrent committed transaction wrote an item it wrote. It allows write skew, so it is not serializable."
prereqs: [multiversion-concurrency-control, isolation-levels]
see_also: [serializable-snapshot-isolation, conflict-graph, phantom-problem, two-phase-locking, multi-version-stm, global-snapshot, chandy-lamport-snapshot]
sources:
  - paper: doi:10.1145/223784.223785
    title: Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995, pages 1 to 10
    locator: Section 4.2 (the definition of snapshot isolation with start and commit timestamps and first-committer-wins, the write skew A5B and the constraint example, and Table 4)
  - paper: doi:10.1145/1071610.1071615
    title: Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil and Dennis Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2), 2005, pages 492 to 528
    locator: Section 2 (snapshot isolation as implemented in Oracle and PostgreSQL, with first-updater-wins) and the definition of the dependency graph with vulnerable rw edges
  - paper: "Alan Fekete, Elizabeth O'Neil and Patrick O'Neil, A read-only transaction anomaly under snapshot isolation, ACM SIGMOD Record 33(3), 2004, pages 12 to 14"
    locator: the example with a checking account, a savings account and a read-only report transaction
  - url: https://pmg.csail.mit.edu/papers/adya-phd.pdf
    title: Atul Adya, Weak consistency, a generalized theory and optimistic implementations for distributed transactions, PhD thesis, MIT, 1999
    locator: the chapter on PL-SI (start dependencies and the phenomena G-SIa and G-SIb), chapter level only
---

*Snapshot isolation* (SI) is an [isolation level](/isolation-levels/), defined by Berenson, Bernstein, Gray, Melton, O'Neil and O'Neil (1995), that [multiversion concurrency control](/multiversion-concurrency-control/) provides without read locks. A transaction reads from a *snapshot*: the committed data as of the moment it started, plus its own writes. When it commits, it succeeds only if no transaction that committed after it started wrote an item that it also wrote; this rule is *first-committer-wins*. Readers never wait for writers and never block them. SI prevents dirty reads, non-repeatable reads, lost updates and read skew, but it allows *write skew*, so it is not [serializable](/serializability/). Several systems have offered it under the name "serializable".

## Definition

**Timestamps.** Each transaction $T_i$ gets a *start timestamp* $s_i$ when it begins and, if it reaches commit, a *commit timestamp* $c_i$ that is larger than every timestamp given out before. Each committed write of $T_i$ creates a version of the item stamped $c_i$. Two transactions are *concurrent* if their intervals $[s_i, c_i]$ and $[s_j, c_j]$ overlap.

**Snapshot isolation.** A history of $r_i(x)$, $w_i(x)$, $c_i$ and $a_i$, in which every read names the version it returns, is a *snapshot isolation history* if:

1. **Snapshot read.** A read $r_i(x)$ returns the value of the last write of $x$ by $T_i$ if there is one, and otherwise the version of $x$ with the largest commit timestamp at most $s_i$.
2. **First committer wins.** If $T_i$ and $T_j$ both commit, are concurrent, and both write some item $x$, the history is not allowed. In an implementation, the second of the two to commit is aborted.

Writes stay private until commit, and a transaction that only reads always commits.

**Phenomena.** In the terms of [isolation levels](/isolation-levels/), Berenson et al. show that SI forbids the dirty write P0, the dirty read P1, the lost update P4 (and P4C), the read skew A5A, and the strict anomalies A1, A2 and A3. It sometimes allows the phantom P3 (a predicate read is stable, but a constraint between a predicate and an insert is not), and it allows the write skew:

> **A5B write skew:** $r_1(x) \ldots r_2(y) \ldots w_1(y) \ldots w_2(x) \ldots$ ($c_1$ and $c_2$ occur).

So SI is incomparable with repeatable read: SI allows A5B, which repeatable read forbids, and repeatable read allows phantom anomalies that SI forbids. Adya's level PL-SI states SI with the dependency graph, extended by *start dependency* edges (from $T_i$ to $T_j$ when $T_i$ commits before $T_j$ starts), and the phenomena G-SIa and G-SIb defined on it.

**Why it is not serializable.** In the dependency graph of an SI history, an rw edge (an anti-dependency, $T_i$ reads a version that $T_j$ overwrites) can go between concurrent transactions; ww and wr edges cannot, by the two rules. A cycle needs rw edges between concurrent transactions. Fekete, Liarokapis, O'Neil, O'Neil and Shasha (2005) showed that every cycle has two such rw edges in a row; this is the basis of [serializable snapshot isolation](/serializable-snapshot-isolation/).

## Examples and non-examples

**Write skew: doctors on call.** A hospital requires that at least one doctor is on call. Alice and Bob are both on call ($a = 1$, $b = 1$). Each wants to leave, and each runs a transaction that reads both rows, checks that at least two doctors are on call, and takes itself off call.

| step | $T_1$ (Alice) | $T_2$ (Bob) | committed state |
|---|---|---|---|
| 1 | $r_1(a) = 1$ | | $a = 1, b = 1$ |
| 2 | $r_1(b) = 1$ | | |
| 3 | | $r_2(a) = 1$ | |
| 4 | | $r_2(b) = 1$ | |
| 5 | $w_1(a, 0)$ | | |
| 6 | | $w_2(b, 0)$ | |
| 7 | $c_1$ | | $a = 0, b = 1$ |
| 8 | | $c_2$ | $a = 0, b = 0$ |

Both transactions read the snapshot with two doctors on call. The write sets $\{a\}$ and $\{b\}$ are disjoint, so first-committer-wins lets both commit, and no one is on call. In either serial order the second transaction would see one doctor and stay. The dependency graph has $T_1 \xrightarrow{rw} T_2$ ($T_1$ read $b$, $T_2$ wrote it) and $T_2 \xrightarrow{rw} T_1$, a cycle. Under [two-phase locking](/two-phase-locking/) the reads would take shared locks, and the writes would deadlock instead.

**Lost update prevented.** $r_1(x) = 100$, $r_2(x) = 100$, $w_1(x, 120)$, $w_2(x, 130)$, $c_1$, $c_2$. $T_1$ and $T_2$ are concurrent and both write $x$, so $c_2$ fails and $T_2$ aborts. The final value is 120, and $T_2$ can retry and read it.

**Read skew prevented.** Accounts $x = y = 50$. $r_1(x) = 50$, then $T_2$ moves 40, $w_2(x, 10)$, $w_2(y, 90)$, $c_2$, then $r_1(y)$. $T_1$ reads $y = 50$ from its snapshot, so it sees the total 100. Read in place, the same schedule gives the read skew A5A with a total of 140.

**A read-only anomaly.** Fekete, O'Neil and O'Neil (2004) showed that even a read-only transaction can see a state that no serial order explains. Checking $x = 0$ and savings $y = 0$. $T_2$ withdraws 10 from checking and charges a fee of 1 if $x + y$ would be negative; $T_1$ deposits 20 into savings; $T_3$ reads both. The schedule: $r_2(x_0)$, $r_2(y_0)$, $r_1(y_0)$, $w_1(y, 20)$, $c_1$, $r_3(x_0) = 0$, $r_3(y_1) = 20$, $c_3$, $w_2(x, -11)$, $c_2$. $T_2$ charged the fee, so it acted as if it came before $T_1$; $T_3$ saw the deposit but not the withdrawal, so $T_1$ came before $T_3$ and $T_3$ before $T_2$. Without $T_3$ the history is serializable.

**Non-example: concurrent writers of one item.** Any history where two concurrent transactions both write $x$ and both commit is not an SI history, whatever the reads.

**Non-example: other snapshots.** A [global snapshot](/global-snapshot/) of a distributed system, such as the [Chandy-Lamport snapshot](/chandy-lamport-snapshot/), records a consistent cut of process states and channel messages for checkpointing or debugging. It has no transactions, no commit rule and no write conflict, and the word means only "a consistent picture at one logical time".

## Related definitions

- [Isolation levels](/isolation-levels/): SI is one of the two levels that Berenson et al. added to the SQL-92 list, with cursor stability.
- [Multiversion concurrency control](/multiversion-concurrency-control/) keeps the versions that snapshot reads need, and its garbage collection removes versions older than the oldest active snapshot.
- [Serializable snapshot isolation](/serializable-snapshot-isolation/) adds a test for two consecutive rw edges between concurrent transactions and aborts one of them, which makes SI serializable.
- [Conflict graph](/conflict-graph/): the dependency graph of an SI history adds rw edges from a read to the next version, which can point backwards in time.
- [Phantom problem](/phantom-problem/): snapshot reads make a repeated predicate read return the same rows, but a constraint over a predicate can still be broken by two inserts.
- [Multi-version STM](/multi-version-stm/) gives read-only transactions a snapshot of memory in the same way. Transactional memory has no durability and usually asks for opacity, so an updating transaction also validates its reads at commit, which rules out write skew.

## References
