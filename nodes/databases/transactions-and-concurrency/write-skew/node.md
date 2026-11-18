---
tag: RM83K5
kind: concept
slug: write-skew
name: Write skew
aliases:
- write skew anomaly
- A5B
area: databases/transactions-and-concurrency
level: core
summary: "Two concurrent transactions each read data that the other writes, and write different items. Each is correct alone, but together they break a rule that spans the items. Snapshot isolation allows it."
see_also: [snapshot-isolation, transaction-anomalies, serializable-snapshot-isolation, snapshot-isolation-dangerous-structure, phantom-problem, adya-isolation-levels, robustness-against-weak-isolation, predicate-locking]
sources:
  - paper: doi:10.1145/223784.223785
    title: "Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995"
    locator: "Section 4, the definition of write skew A5B and history H5, and Table 4 (write skew is possible under snapshot isolation and not possible under repeatable read)"
  - paper: doi:10.1145/1071610.1071615
    title: "Alan Fekete, Dimitrios Liarokapis, Elizabeth O'Neil, Patrick O'Neil and Dennis Shasha, Making snapshot isolation serializable, ACM Transactions on Database Systems 30(2), 2005"
    locator: "the dangerous structures of the static dependency graph, and the program changes that remove them by materializing a conflict or by promoting a read to a write, chapter level only"
  - paper: doi:10.1145/1376616.1376690
    title: "Michael J. Cahill, Uwe Röhm and Alan Fekete, Serializable isolation for snapshot databases, Proceedings of ACM SIGMOD 2008"
    locator: "the detection of consecutive rw-antidependencies at run time, chapter level only"
  - book: isbn:9781449373320
    title: "Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017"
    locator: "Chapter 7, the section on write skew and phantoms (meeting rooms and user names; a secondary source)"
---

*Write skew* is the [transaction anomaly](/transaction-anomalies/) in which two concurrent transactions read an overlapping set of data, make decisions from it, and then write *different* items. Each transaction keeps a rule that spans several items when it runs alone, but together they break it. Berenson et al. (1995) named it A5B:

$$r_1(x) \ldots r_2(y) \ldots w_1(y) \ldots w_2(x) \ldots (c_1 \text{ and } c_2 \text{ occur}).$$

It is the anomaly that separates [snapshot isolation](/snapshot-isolation/) from serializability: since the write sets are disjoint, first-committer-wins does not stop it. In the dependency graph of [Adya's isolation levels](/adya-isolation-levels/) it is a cycle of two anti-dependency arcs, and the [dangerous structure theorem](/snapshot-isolation-dangerous-structure/) says that every anomaly of snapshot isolation contains two such arcs in a row. [Serializable snapshot isolation](/serializable-snapshot-isolation/) prevents it at run time. The [snapshot isolation](/snapshot-isolation/) page gives the basic example of doctors on call; this page gives the general shape, the forms with predicates and with more transactions, and the ways to remove it.

## In plain words

Two people look at the same picture and each makes a change that is safe given that picture. But each change assumed that the other part stayed as it was. One person takes money out of account A because the total of A and B is high enough; at the same time another takes money out of B for the same reason. Each check passed, both changes commit, and the total is now too low. No one overwrote anyone else's data, so a database that only checks for two writes to the same row sees no conflict. The problem is a rule that spans several rows, read by both and protected by neither.

## The idea

**The shape.** Write skew needs three things: $T_1$ and $T_2$ are concurrent; $T_1$ reads an item that $T_2$ writes and $T_2$ reads an item that $T_1$ writes; and their write sets do not overlap. In the dependency graph each read of an old version followed by the other's write is an anti-dependency, so the graph has $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_1$. A cycle means no serial order: in $T_1 T_2$ the transaction $T_2$ would have seen the write of $T_1$, and in $T_2 T_1$ the other way round.

**Which levels allow it.** In Table 4 of Berenson et al., write skew is possible under read committed and under snapshot isolation, sometimes possible under cursor stability, and not possible under lock-based repeatable read, where the long read locks make one of the writes wait. In Adya's terms it is G2-item: PL-2.99 and PL-3 forbid it, while PL-2+ and PL-SI allow it, because the cycle has two anti-dependency arcs and not one.

**With predicates.** The items read need not exist. Each transaction checks that *no* row matches a condition and then inserts a matching row: two bookings of the same room for the same hour, two users who take the same name, two shifts that both leave a ward empty. The anti-dependency is then on a predicate, and row locks or row versions cannot catch it, which is the [phantom problem](/phantom-problem/). [Predicate locking](/predicate-locking/) or [key-range locking](/key-range-locking/) under two-phase locking prevent it.

**With more transactions.** The cycle may be longer. $T_1$ reads $x$ and writes $y$, $T_2$ reads $y$ and writes $z$, $T_3$ reads $z$ and writes $x$, all concurrent: the cycle $T_1 \xrightarrow{rw} T_3 \xrightarrow{rw} T_2 \xrightarrow{rw} T_1$ has three anti-dependency arcs. The cycle can also contain ordinary dependencies, as in the read-only anomaly of Fekete, O'Neil and O'Neil (2004), where a read-only transaction closes a cycle between two updaters that are serializable on their own. Under snapshot isolation every non-serializable cycle has two anti-dependency arcs between concurrent transactions that follow each other in the cycle.

## Examples

**Two accounts with a joint limit.** A bank allows either account of a customer to go negative as long as $x + y \ge 0$. Start with $x = y = 50$. $T_1$ withdraws 90 from $y$ and $T_2$ withdraws 90 from $x$; each first reads both balances and checks the rule.

| step | $T_1$ | $T_2$ | committed $x$ | committed $y$ |
|---|---|---|---|---|
| 1 | reads $x = 50$, $y = 50$ | | 50 | 50 |
| 2 | | reads $x = 50$, $y = 50$ | 50 | 50 |
| 3 | $50 + 50 - 90 \ge 0$: writes $y = -40$ | | 50 | 50 |
| 4 | | $50 + 50 - 90 \ge 0$: writes $x = -40$ | 50 | 50 |
| 5 | commits | | 50 | $-40$ |
| 6 | | commits: no concurrent write of $x$ | $-40$ | $-40$ |

The total is $-80$. Under lock-based repeatable read, step 3 waits for the read lock of $T_2$ on $y$ and step 4 for the read lock of $T_1$ on $x$: a deadlock, and one transaction is aborted.

**Meeting rooms.** A booking transaction runs `SELECT count(*) FROM bookings WHERE room = 7 AND hour = 10`, and inserts a booking if the count is 0. Two such transactions under snapshot isolation both see 0, both insert, and both commit, since they insert different rows. A unique index on `(room, hour)` turns the predicate into a key and makes the second insert fail.

**Not write skew.** If $T_1$ and $T_2$ both write the same row, for example a per-customer row that holds the total, the write sets overlap and first-committer-wins aborts one of them. That is the lost update, which snapshot isolation does prevent.

## Where it is used

The term is used to judge whether an application is safe under snapshot isolation, which several database systems offered under the name "serializable" or still offer as their repeatable read level. The fixes fall into four groups:

- **Materialize the conflict.** Fekete et al. (2005) add a write to a row that both transactions touch, such as the customer row in the example, so that the write sets overlap and first-committer-wins applies. For predicates, a row per room and hour plays the same part.
- **Promote a read to a write.** Write the value just read back unchanged, or read it with `SELECT ... FOR UPDATE` in systems that treat this as a write or a lock. The read then conflicts with the other transaction's write.
- **Use a stronger level.** [Serializable snapshot isolation](/serializable-snapshot-isolation/) tracks the anti-dependencies and aborts a transaction that has one coming in and one going out; two-phase locking with predicate or key-range locks prevents the reads from being stale.
- **Prove that it cannot happen.** [Robustness against weak isolation](/robustness-against-weak-isolation/) asks whether any execution of the given programs under snapshot isolation has such a cycle. Fekete et al. found none in TPC-C, so TPC-C runs serializably under snapshot isolation.

## References
