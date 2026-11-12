---
tag: 04RT24
kind: algorithm
slug: serializable-snapshot-isolation
name: Serializable snapshot isolation
aliases:
- SSI
area: systems/database-algorithms
level: research
summary: "Snapshot isolation plus SIREAD locks and two flags per transaction, which abort any transaction that could be the pivot of two consecutive rw edges, so that every committed history is serializable."
solves: [concurrency-control]
model: word-ram
complexity:
  vars: {p: the running transactions with a pending write of the item, v: the versions of the item committed after the start of the transaction, s: the SIREAD locks on the item, w: the size of the write set, L: the SIREAD locks kept for transactions that overlap a running one}
  time: {worst: O(p + v + s + w)}
  space: {extra: O(L)}
properties: {deterministic: true}
history:
  year: 2008
  people: [Michael J. Cahill, Uwe Röhm, Alan D. Fekete]
  note: "SIGMOD 2008, on the theory of Fekete et al. (2005); in PostgreSQL 9.1 (2011) by Ports and Grittner."
prereqs: [snapshot-isolation, conflict-graph]
see_also: [isolation-levels, multiversion-concurrency-control, optimistic-concurrency-control, two-phase-locking, predicate-locking, phantom-problem, multi-version-stm, transaction-validation]
sources:
  - paper: doi:10.1145/1376616.1376690
    title: Michael J. Cahill, Uwe Röhm and Alan D. Fekete, Serializable isolation for snapshot databases, Proceedings of ACM SIGMOD 2008, pages 729 to 738
    locator: the description of the new algorithm (the modified begin, read, write and commit operations with SIREAD locks and the inConflict and outConflict flags), its correctness argument, and the discussion of false positives
  - paper: doi:10.1145/1620585.1620587
    title: Michael J. Cahill, Uwe Röhm and Alan D. Fekete, Serializable isolation for snapshot databases, ACM Transactions on Database Systems 34(4), 2009, article 20
    locator: the journal version, with the refinements that check commit order to reduce false positives, chapter level only
  - paper: doi:10.1145/1071610.1071615
    title: Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil and Dennis Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2), 2005, pages 492 to 528
    locator: the theorem that every cycle in the dependency graph of an SI history has two consecutive rw edges between concurrent transactions (the dangerous structure with its pivot)
  - paper: doi:10.14778/2367502.2367523
    title: Dan R. K. Ports and Kevin Grittner, Serializable snapshot isolation in PostgreSQL, Proceedings of the VLDB Endowment 5(12), 2012, pages 1850 to 1861
    locator: the PostgreSQL design (lists of conflicts in place of flags, the commit-order and read-only rules, safe snapshots and deferrable transactions, and the summarization of old transactions to bound memory)
---

*Serializable snapshot isolation* (SSI) is the algorithm of Cahill, Röhm and Fekete (2008) that makes [snapshot isolation](/snapshot-isolation/) serializable. It keeps the cheap parts of SI: reads come from a snapshot and never block, and writers follow first-committer-wins. It adds a test at run time for the only pattern that can make an SI history non-serializable. Fekete and others (2005) showed that every cycle in the [conflict graph](/conflict-graph/) of an SI history contains two consecutive *rw edges* (anti-dependencies) between concurrent transactions, $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$, where $T_1$ may be $T_3$. The middle transaction $T_2$ is the *pivot*. SSI gives each transaction two flags, one for an rw edge in and one for an rw edge out, and aborts a transaction that has both. Every committed history is then serializable, at the cost of some aborts that were not necessary.

## In plain words

Under snapshot isolation, each transaction works on a photo of the database taken when it starts. Two transactions can each read a fact, and each change a different fact that the other one read. Both commit, and the result is one that no order of the two could give. This is write skew.

SSI watches for one sign of danger. "I read something that you later changed" is an arrow from me to you. A bad result always needs one transaction with an arrow coming in and an arrow going out.

So each transaction carries two marks: "an arrow comes in" and "an arrow goes out". If a transaction gets both, SSI aborts it. Sometimes the danger is not real, and the abort was not needed. That is the price of a simple test.

## The problem

The input is a stream of transactions, each a program of reads $r_i(x)$ and writes $w_i(x)$ that ends with $c_i$, run on a multiversion store. The output is, for each read, the version it returns, and for each transaction, commit or abort. The committed transactions must be one-copy serializable: equivalent to some serial run on a single copy of each item. Reads must not wait for writers, as in SI.

**The rw edge.** In an SI history, $T_i \xrightarrow{rw} T_j$ if $T_i$ reads a version of $x$ and $T_j$ writes a later version of $x$. Then $T_j$ commits after $T_i$ starts, and, by first-committer-wins and the snapshot rule, $T_i$ and $T_j$ are concurrent. The other edges of the conflict graph (ww and wr) always go from a transaction that committed before the other started.

**The theorem of Fekete et al. (2005).** If an SI history is not serializable, its dependency graph has a cycle, and every cycle has three consecutive transactions $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ with $T_1, T_2$ concurrent and $T_2, T_3$ concurrent. $T_1 = T_3$ is allowed.

## The algorithm

Each transaction $T$ has a start timestamp $T.start$, a commit timestamp $T.commit$, and two flags $T.in$ and $T.out$. An *SIREAD lock* on $x$ records that $T$ read $x$. It blocks nothing, and it stays after $T$ commits.

```pseudo id=main
BEGIN(T)
L1  T.start ← clock; T.in ← false; T.out ← false
READ(T, x)
L2  take an SIREAD lock on x for T                        ▷ kept after T commits
L3  for each running U ≠ T with a pending write of x do U.in ← true; T.out ← true
L4  N ← the writers of the versions of x committed after T.start
L5  if some U in N has U.out then abort T                  ▷ U is committed and would be a pivot
L6  for each U in N do U.in ← true; T.out ← true
L7  return T's own write of x if any, else the newest version committed at or before T.start
WRITE(T, x, v)
L8  R ← the U ≠ T with an SIREAD lock on x, U running or U.commit > T.start
L9  if some committed U in R has U.in then abort T         ▷ U would be a pivot
L10 for each U in R do U.out ← true; T.in ← true
L11 keep v as a pending write of x by T
COMMIT(T)
L12 if T.in and T.out then abort T                         ▷ T may be a pivot
L13 if some item in T's write set has a version committed after T.start then abort T   ▷ first committer wins
L14 clock ← clock + 1; T.commit ← clock; install T's writes as versions
ABORT(T)
L15 drop T's pending writes and SIREAD locks; the flags that T set on others stay
RELEASE()
L16 drop the SIREAD locks of committed U with U.commit ≤ the smallest start of a running transaction
```

Lines L3 to L6 and L8 to L10 catch every rw edge between concurrent transactions, at the moment of its second operation. If $T$ reads $x$ after a concurrent $U$ wrote it, $U$'s write is still pending (line L3) or already committed after $T.start$ (line L4). If $T$ reads first and $U$ writes later, $U$ finds $T$'s SIREAD lock (line L8). This is why SIREAD locks must outlive their transaction: the writer may come after the reader has committed.

A transaction with both flags is aborted at commit (line L12). If the second edge reaches a pivot that has already committed, the pivot cannot be aborted, so the transaction that performs the operation aborts instead (lines L5 and L9). Cahill and others describe a system where SI uses write locks (first-updater-wins); line L3 then tests for a write lock, and the rest is the same.

## Example

**Write skew.** Two doctors are on call, $a = b = 1$, and the rule is that at least one stays on call. Each transaction reads both and takes one doctor off call.

| step | operation | effect |
|---|---|---|
| 1 | $r_1(a)\, r_1(b)\, r_2(a)\, r_2(b)$ | both see two on call; SIREAD locks on $a$ and $b$ for $T_1$ and $T_2$ |
| 2 | $w_1(a, 0)$ | line L8 finds $T_2$'s lock on $a$: $T_2.out$, $T_1.in$ |
| 3 | $c_1$ | $T_1$ has only $in$: commits |
| 4 | $w_2(b, 0)$ | line L8 finds the lock of the committed $T_1$ on $b$, and $T_1.in$ is set: line L9 aborts $T_2$ |

The database keeps $a = 0, b = 1$. Under plain SI both would commit with $a = b = 0$. If both writes come before both commits, both transactions get both flags and both abort at line L12, although the abort of $T_1$ alone would have been enough.

**A false positive.** $T_1$ reads $x$ and writes $z$, $T_2$ reads $y$ and writes $x$, $T_3$ writes $y$. The schedule $r_1(x)\, r_2(y)\, w_2(x)\, w_3(y)\, w_1(z)\, c_3\, c_2\, c_1$ has $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ and no other edge. It is serializable as $T_1, T_2, T_3$: under plain SI all three commit, and every read returns what it would return in that order. SSI sets $T_1.out$ and $T_2.in$ at $w_2(x)$, $T_2.out$ and $T_3.in$ at $w_3(y)$, and aborts $T_2$ at line L12. The flags record that a structure exists, not whether it closes into a cycle.

## Correctness

**Theorem.** Every history of committed transactions under SSI is one-copy serializable.

*Sketch.* The committed transactions form an SI history, because lines L7, L13 and L14 are those of SI. Assume it is not serializable. By the theorem of Fekete et al., it has committed $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_3$ with both pairs concurrent. Each rw edge between concurrent transactions sets the flags at the time of its later operation, as shown above. Take the later of the two edges. If $T_2$ was running at that time, both $T_2.in$ and $T_2.out$ were set before $T_2$ committed, and line L12 would have aborted it. If $T_2$ had committed, the later operation is $T_1$'s read of $x$ (line L4 finds $T_2$'s version, and $T_2.out$ is set, so line L5 aborts $T_1$) or $T_3$'s write of $y$ (line L8 finds $T_2$'s lock, and $T_2.in$ is set, so line L9 aborts $T_3$). Each case contradicts that all three committed. The full proof is in the correctness proof below.

The test of the implementation runs thousands of random schedules and checks by brute force over all serial orders that every committed history is one-copy serializable, while the same schedules under plain SI are sometimes not.

## Complexity

Let $p$ be the running transactions with a pending write of $x$, $v$ the versions of $x$ committed after $T.start$, $s$ the SIREAD locks on $x$, and $w$ the size of $T$'s write set.

- **Read.** $O(p + v)$ more than an SI read, which already walks the versions.
- **Write.** $O(s)$ to scan the SIREAD locks on $x$.
- **Commit.** $O(1)$ for line L12, plus the $O(w)$ of SI.
- **Space.** Two flags per transaction, and one SIREAD lock per item read. The locks of $T$ must be kept until every transaction concurrent with $T$ has ended (line L16), so one long transaction keeps the locks of all others alive.

So one operation costs at most $O(p + v + s + w)$, and the extra space is $O(L)$, where $L$ is the number of SIREAD locks kept. No operation waits for a lock that SSI adds. The cost is the space and the aborts.

## Properties

- **Readers never block writers, and writers never block readers**, as in SI. SIREAD locks only record.
- **Conservative.** The flags are set by structures that may never close into a cycle, and they stay set when the other transaction aborts. Both cause false positives.
- **No deadlock** is added, since nothing waits.
- **Read-only transactions can abort** (line L5), unless the system knows they run on a safe snapshot.
- **Predicates.** The read set must include the predicates read, as in [predicate locking](/predicate-locking/), or SSI misses rw edges caused by inserts (the [phantom problem](/phantom-problem/)). PostgreSQL takes SIREAD locks on index ranges and pages.

## Variants and improvements

- **Commit order.** In the cycle of Fekete et al., $T_3$ commits first among the three. Cahill's journal version and PostgreSQL check this and do not abort a pivot whose out-neighbor commits after it.
- **Lists in place of flags.** PostgreSQL (Ports and Grittner, 2012) records the actual conflicting transactions, not booleans. When a transaction aborts, its edges vanish, which removes the false positive of the write skew example above.
- **Read-only rules and safe snapshots.** If $T_1$ is read-only, the structure is dangerous only if $T_3$ committed before $T_1$ started. A read-only transaction on a *safe snapshot*, one that no running transaction can make dangerous, needs no SIREAD locks; a *deferrable* transaction waits for such a snapshot and then never aborts.
- **Bounded memory.** PostgreSQL summarizes old committed transactions and coarsens SIREAD locks from rows to pages to relations when memory runs short. Coarser locks add false positives but never miss an edge.
- **Precise cycle testing.** Later work tracks the full graph and aborts only on a real cycle, with more bookkeeping per operation.
- **Static analysis.** Fekete et al. (2005) also show how to make a fixed set of programs serializable under plain SI, by finding the dangerous structures in the static dependency graph and adding conflicts by hand.

## When to use it

Use SSI when the database already runs MVCC with snapshot isolation and the application needs true serializability without rewriting its transactions. Reads stay non-blocking, so read-heavy and mixed workloads keep most of the speed of SI. Prefer plain SI with explicit locks when the dangerous transactions are few and known, and prefer [two-phase locking](/two-phase-locking/) when aborts are very expensive, for example for long transactions that would be restarted. SSI is a database algorithm: transactional memory systems such as [multi-version STM](/multi-version-stm/) use [transaction validation](/transaction-validation/) of read sets at commit, a different test that also forbids write skew but checks every read.

## Pitfalls

- **Releasing SIREAD locks at commit.** A writer that comes after the reader commits must still find the lock (line L8), or the edge is lost.
- **Testing only at commit.** If the pivot has already committed, line L12 can never fire for it. Lines L5 and L9 must abort the transaction that creates the second edge.
- **Ignoring pending writes.** A read must also see writes of running transactions (line L3), or an rw edge to a transaction that commits later is missed.
- **Calling every abort a conflict.** Applications must retry serialization failures, and false positives make retries more frequent than real conflicts.
- **Row locks only.** Without locks on predicates or index ranges, inserts into a range read by another transaction create rw edges that SSI cannot see.
- **Mixing levels.** A transaction that runs at plain SI next to SSI transactions does not take SIREAD locks, and the guarantee holds only among the SSI transactions.

## Implementations

## History

Snapshot isolation was defined by Berenson and others in 1995, and it was known not to be serializable. Fekete, Liarokapis, O'Neil, O'Neil and Shasha (2005) characterized its anomalies by the dangerous structure of two consecutive rw edges and used it to make given applications serializable by static analysis. Michael Cahill, Uwe Röhm and Alan Fekete turned the same theorem into a run-time algorithm in SIGMOD 2008, with prototypes in Berkeley DB and InnoDB, and published the journal version in 2009. Dan Ports and Kevin Grittner implemented SSI in PostgreSQL 9.1 (2011), the first production system to use it, and described the design and its optimizations in PVLDB in 2012.

## References
