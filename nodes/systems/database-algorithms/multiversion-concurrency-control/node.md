---
tag: 07QKP2
kind: technique
slug: multiversion-concurrency-control
name: Multiversion concurrency control
aliases:
- MVCC
- multiversion timestamp ordering
area: systems/database-algorithms
level: core
summary: "Keep several committed versions of each item, so that a read can be served by an older version instead of waiting or aborting. The schedule must be one-copy serializable."
prereqs: [timestamp-ordering, serializability]
see_also: [snapshot-isolation, serializable-snapshot-isolation, optimistic-concurrency-control, two-phase-locking, isolation-levels, multi-version-stm, global-version-clock, log-structured-merge-tree]
sources:
  - paper: "David P. Reed, Naming and synchronization in a decentralized computer system, PhD thesis, MIT, Technical Report MIT/LCS/TR-205, 1978"
    locator: the chapters on objects as sequences of versions (pseudo-times) and the read and write rules of the timestamp-based scheme, chapter level only
  - paper: doi:10.1145/319996.319998
    title: Philip A. Bernstein and Nathan Goodman, Multiversion concurrency control, theory and algorithms, ACM Transactions on Database Systems 8(4), 1983, pages 465 to 483
    locator: the definitions of multiversion histories and one-copy serializability, the multiversion serialization graph theorem, and the proofs for the multiversion timestamp, multiversion locking and mixed methods
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 5, Multiversion Concurrency Control (1SR, the MVSG, multiversion timestamp ordering, multiversion two-phase locking)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 5, Multiversion Concurrency Control (multiversion schedules, MVSR and the MVTO, MV2PL and ROMV protocols), chapter level only
  - paper: doi:10.14778/3067421.3067427
    title: Yingjun Wu, Joy Arulraj, Jiexi Lin, Ran Xian and Andrew Pavlo, An empirical evaluation of in-memory multi-version concurrency control, Proceedings of the VLDB Endowment 10(7), 2017, pages 781 to 792
    locator: the design space of version storage (append-only, time-travel, delta), garbage collection (tuple-level and transaction-level) and index management
---

*Multiversion concurrency control* (MVCC) keeps, for each data item, a list of versions, one for each committed write, instead of one current value. A read can then be served by an older version, so it never has to wait for a writer and is rarely the cause of an abort. The scheduler decides, for each read, *which* version it returns, and the result must still look like a serial run on one copy of the data: the history must be *one-copy serializable* (1SR). Reed (1978) proposed the first such scheme, based on timestamps; Bernstein and Goodman (1983) gave the theory of 1SR and proved the timestamp, locking and mixed methods correct. The most used form today is [snapshot isolation](/snapshot-isolation/), which is MVCC with a weaker correctness condition. This page uses *multiversion timestamp ordering* (MVTO) as the template.

## In plain words

In a normal database each row has one value. If one transaction is changing a row, another that wants to read it must wait, or the system must undo something.

With MVCC, a change does not replace the old value. It adds a new version next to it, marked with the time of the change. A reader that started earlier reads the version that was current at its own time. So readers and writers do not get in each other's way.

The system must still make the result look as if the transactions ran one after the other, each seeing one copy of the data. The rules about which version a read may use are what make this true. Old versions that no running transaction can still read are deleted later, by a garbage collector.

## When it applies

- The workload has long read-only transactions (reports, backups, analytics) next to short updates, and readers must not block writers or be blocked by them.
- The system can afford the space for old versions and a background process to remove them.
- Weaker levels are acceptable for some transactions: the same version store gives [snapshot isolation](/snapshot-isolation/) and read committed at almost no extra cost, and [serializable snapshot isolation](/serializable-snapshot-isolation/) on top of them.

## The template

**Model.** A transaction $T$ gets a unique timestamp $ts(T)$ when it begins. A version $x_j$ of item $x$ is written by the transaction with timestamp $j$ and carries $wts = j$, a *read timestamp* $rts$ (the largest timestamp of a transaction that read it) and a committed flag. The initial version is $x_0$.

```pseudo id=main
BEGIN(T)
L1  ts(T) ← the next value of a counter
READ(T, x)
L2  v ← the version of x with the largest wts ≤ ts(T)
L3  rts(v) ← max(rts(v), ts(T))
L4  if v is not committed and v.wts ≠ ts(T) then add the writer of v to the commit dependencies of T
    return the value of v
WRITE(T, x, value)
L5  v ← the version of x with the largest wts ≤ ts(T)        ▷ if v.wts = ts(T), overwrite v
L6  if rts(v) > ts(T) then abort T                            ▷ a younger transaction read v and should have read T's version
L7  create the version x_ts(T) with the value, after v
COMMIT(T)
L8  wait until every commit dependency of T has committed; if one aborts, abort T
L9  mark the versions of T committed
ABORT(T)
L10 delete the versions of T; abort every transaction that read one of them
GC()
L11 m ← the smallest timestamp of an active transaction
L12 for each x, delete every version older than the newest version with wts < m
```

**Correctness (1SR).** A multiversion history is *one-copy serializable* if it is equivalent to a serial history on a single copy of each item: every read reads from the same transaction, and the last writer of each item is the same. Bernstein and Goodman prove that MVTO histories are 1SR, equivalent to the serial order of timestamps. The argument: line L2 makes $T$ read the version of the transaction with the largest timestamp below its own that wrote $x$, which is what a serial run in timestamp order would read, *unless* a transaction $U$ with $wts(v) < ts(U) < ts(T)$ writes $x$ later. Line L6 rules this out: when $U$ tries to write, it finds $v$ with $rts(v) \ge ts(T) > ts(U)$ and aborts. So every read reads from the writer it would read from in timestamp order. Line L8 makes the history recoverable: no transaction commits before a transaction it read from.

**Costs.** A read is one search of the version list of $x$ and never blocks; it may create a commit dependency. A write may abort. Space is the number of live versions. The versions that line L12 keeps are the newest version below $m$ and all versions from $m$ on: a present or future transaction has a timestamp at least $m$, so line L2 never selects an older version, and line L6 never inspects one.

## Classic examples

**Readers do not wait.** $x_0 = 0$. $T_1$ and $T_2$ begin, with timestamps 1 and 2. $w_2(x, 2)$ creates $x_2$. Then $r_1(x)$ reads $x_0 = 0$, the version with the largest $wts \le 1$; under single-version timestamp ordering this read would arrive too late and $T_1$ would abort. $r_2(x)$ reads $x_2 = 2$. Both commit, and the history is equivalent to $T_1\, T_2$.

**A late write aborts.** $T_1$ and $T_2$ begin with timestamps 1 and 2. $r_2(x)$ reads $x_0$ and sets $rts(x_0) = 2$. Then $w_1(x)$ finds $x_0$ with $rts = 2 > 1$: in timestamp order $T_2$ should have read $T_1$'s version, but it has already read $x_0$. $T_1$ aborts (line L6). The [Thomas write rule](/thomas-write-rule/) cannot help here, because the overwritten value was read.

**A cascading abort.** $T_1$ writes $x_1$, $T_2$ reads it (line L4 adds a commit dependency) and asks to commit, so it waits (line L8). $T_1$ aborts; line L10 deletes $x_1$ and aborts $T_2$. A variant that lets reads see committed versions only avoids cascades, at the price of making some reads wait.

**Garbage collection.** 50 transactions in a row write $x$ and commit. The list holds 51 versions. With no active transaction, $m$ is the next timestamp, and line L12 keeps only the newest version.

## Variations

- **Multiversion two-phase locking (MV2PL).** Writers take exclusive locks and create versions; readers of read-only transactions read the last committed version as of their start without locks; update transactions lock what they read. A certify step at commit waits for readers. Bernstein and Goodman prove it correct as well.
- **Read-only multiversion (ROMV).** Update transactions use [two-phase locking](/two-phase-locking/) on the newest versions; read-only transactions read a snapshot by timestamp. This is common in practice.
- **Snapshot isolation.** Every transaction reads the snapshot as of its start, and writers follow first-committer-wins. It is cheaper than MVTO but not 1SR; see [snapshot isolation](/snapshot-isolation/) and [serializable snapshot isolation](/serializable-snapshot-isolation/).
- **Optimistic MVCC.** In-memory systems such as Hekaton validate the reads at commit, as in [optimistic concurrency control](/optimistic-concurrency-control/), and use the version store to give readers a stable view.
- **Version storage.** Append-only lists (PostgreSQL keeps all versions in the table), time-travel tables, or deltas in an undo log (Oracle, MySQL InnoDB), which keep the newest version in place and rebuild old ones. Wu and others (2017) compare these designs.
- **Garbage collection.** Tuple-level (vacuum, or cleanup during scans) or transaction-level (by epochs). Long-running transactions hold back $m$ and make version lists grow.
- **Transactional memory.** [Multi-version STM](/multi-version-stm/) applies the same idea to memory words, often with a [global version clock](/global-version-clock/). It keeps versions in memory only, has no durability and no recovery, and asks for opacity, so even transactions that will abort see a consistent snapshot.

## Pitfalls

- **Reading the newest version.** If line L2 returns the newest version rather than the newest at or below $ts(T)$, MVCC is single-version timestamp ordering with extra space, and old readers abort.
- **Forgetting rts.** Without line L3 and the test of line L6, a writer can insert a version under a reader that should have seen it, and the history is not 1SR.
- **Committing before dependencies.** Without line L8, a transaction can commit after reading from a writer that later aborts, and the history is not recoverable.
- **Collecting too much.** Line L12 must keep the newest version below $m$. Deleting it leaves the oldest active transaction with nothing to read.
- **Long transactions.** A transaction that stays active holds $m$ back, so no version newer than its start can be collected. Version chains grow and every read pays to walk them.
- **Calling SI serializable.** The common MVCC protocol is snapshot isolation, which allows write skew. MVCC as such does not imply serializability.

## Exercises

1. Run MVTO on $r_1(x)\, w_2(x)\, r_3(x)\, w_1(x)\, c_1\, c_2\, c_3$ with timestamps 1, 2 and 3. Which versions does each read return, and which transactions abort?
2. Show a history that MVTO accepts and single-version timestamp ordering rejects, and one that both reject.
3. Prove that line L12 never deletes a version that a later call of line L2 would select.
4. Give a multiversion history that is serializable when versions are ignored (conflict equivalent to a serial history on the operations) but not 1SR.
5. Under snapshot isolation, which versions can garbage collection delete, and how does it differ from MVTO?

## References
