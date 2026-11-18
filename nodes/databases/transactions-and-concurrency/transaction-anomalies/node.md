---
tag: 8T9AB6
kind: concept
slug: transaction-anomalies
name: Transaction anomalies
aliases:
- dirty read
- non-repeatable read
- lost update
- read phenomena
- isolation anomalies
area: databases/transactions-and-concurrency
level: core
summary: "The ways concurrent transactions go wrong under weak isolation, from dirty writes to write skew. Each is a pattern of operations or a cycle of dependencies, and levels are named by what they forbid."
see_also: [isolation-levels, write-skew, adya-isolation-levels, phantom-problem, snapshot-isolation, serializability, recoverable-schedule, robustness-against-weak-isolation]
sources:
  - paper: doi:10.1145/223784.223785
    title: "Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995"
    locator: "the phenomena P0 to P4C and the anomalies A1 to A3, A5A and A5B, the histories H1 to H5, Remarks 4 and 5 on the strict and broad readings, and Table 4"
  - url: https://pmg.csail.mit.edu/papers/adya-phd.pdf
    title: "Atul Adya, Weak consistency, a generalized theory and optimistic implementations for distributed transactions, PhD thesis, MIT, 1999"
    locator: "the chapters that define the direct serialization graph and the phenomena G0, G1a, G1b, G1c, G-single, G2-item and G2, chapter level only"
  - paper: "Alan Fekete, Elizabeth O'Neil and Patrick O'Neil, A read-only transaction anomaly under snapshot isolation, ACM SIGMOD Record 33(3), 2004, pages 12 to 14"
    locator: "the read-only anomaly with a checking account, a savings account and a report transaction"
  - url: https://arxiv.org/abs/1609.06670
    title: "Natacha Crooks, Youer Pu, Lorenzo Alvisi and Allen Clement, Seeing is believing, a client-centric specification of database isolation, arXiv 1609.06670"
    locator: "the restatement of the anomalies and levels in terms of the states that clients observe, chapter level only"
  - book: isbn:9781449373320
    title: "Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017"
    locator: "Chapter 7, Transactions, the sections on weak isolation levels (a secondary source for the informal examples)"
---

A *transaction anomaly* is a way in which concurrent transactions produce a result that no serial run could produce, or that uses data that never committed. The best known are the *dirty read*, the *non-repeatable read*, the *phantom* and the *lost update*, but the list that matters is longer: the dirty write, read skew, [write skew](/write-skew/), and the read-only anomaly of [snapshot isolation](/snapshot-isolation/). The [isolation levels](/isolation-levels/) of SQL are named by the anomalies they forbid, so the definitions of the anomalies decide what the levels mean. This page is the catalogue: the anomalies one by one, with an example, the cycle each one makes in the dependency graph of [Adya's isolation levels](/adya-isolation-levels/), and the levels that allow it. A schedule with no anomaly of any kind is [serializable](/serializability/).

## In plain words

When transactions run at the same time, the database may let one see or overwrite the work of another in the middle. Most of the time nothing bad happens. An anomaly is a case where something bad does happen: a transaction reads a value that was later rolled back, reads the same row twice and gets two answers, adds up accounts while money is in transit, or two updates of a counter leave the effect of only one. Each anomaly has a name and a short pattern of reads and writes that shows it. A database that offers a weaker level of isolation tells the programmer which of these patterns can occur. The programmer must then make sure that the application does not depend on their absence.

## The idea

**Three ways to state an anomaly.** The SQL-92 standard described three "phenomena" in English. Berenson et al. (1995) turned them into patterns of operations, and found two readings. The *strict* readings A1, A2 and A3 describe a bad outcome that has already happened, such as a read of data from a transaction that then aborts. The *broad* readings P1, P2 and P3 forbid the first step of such an outcome, such as any read of uncommitted data. Their Remark 4 shows that only the broad readings give the intended levels: histories H1, H2 and H3 are not serializable, yet contain no A1, A2 or A3. Their Remark 5 says that the three phenomena are not enough, and the paper adds the dirty write P0, the lost update P4 and its cursor form P4C, read skew A5A and write skew A5B. Adya (1999) then stated the anomalies as cycles in a graph of committed transactions, so that a multiversion or optimistic system is not blamed for a read that does no harm. Crooks et al. restated them once more in terms of the states that clients observe.

**The catalogue.** Here $T_1$ and $T_2$ are concurrent, items are $x$ and $y$, and $P$ is a predicate.

- *Dirty write* (P0): $w_1(x) \ldots w_2(x) \ldots$ before $T_1$ ends. Two transactions write the same items in different orders, so no serial order explains the final state. It also breaks recovery: if $T_1$ aborts, restoring its before-image of $x$ erases the write of $T_2$. Every level, even read uncommitted, forbids it.
- *Dirty read* (P1): $w_1(x) \ldots r_2(x) \ldots$ before $T_1$ ends. Adya splits it into three committed-only phenomena: the *aborted read* G1a (the writer aborts), the *intermediate read* G1b (the reader sees a version that its writer later overwrote) and *circular information flow* G1c (each of two transactions reads from the other).
- *Non-repeatable read*, or fuzzy read (P2): $r_1(x) \ldots w_2(x) \ldots$ before $T_1$ ends. In the strict form A2, $T_1$ reads $x$ again after $T_2$ commits and gets a new value.
- *Phantom* (P3): $r_1(P) \ldots w_2(y \in P) \ldots$ before $T_1$ ends, where the write inserts, deletes or changes a row that matches $P$. It needs predicate reads, and the [phantom problem](/phantom-problem/) is why row locks alone do not prevent it.
- *Lost update* (P4): $r_1(x) \ldots w_2(x) \ldots w_1(x) \ldots c_1$. $T_1$ writes a value computed from a stale read, and the update of $T_2$ is lost. P4C is the same with the read through a cursor.
- *Read skew* (A5A): $r_1(x) \ldots w_2(x) \ldots w_2(y) \ldots c_2 \ldots r_1(y)$. $T_1$ sees $x$ before and $y$ after the change of $T_2$, so a constraint between them seems broken.
- *Write skew* (A5B): $r_1(x) \ldots r_2(y) \ldots w_1(y) \ldots w_2(x)$, both commit. Each reads what the other writes, and each write is correct alone; the [write skew](/write-skew/) page treats it in detail.
- *Read-only anomaly* (Fekete, O'Neil and O'Neil, 2004). Two updaters are serializable on their own, but a third, read-only transaction sees a state that no serial order of all three contains.

**Anomalies as cycles.** In the direct serialization graph of a history there is an arc for each write dependency (ww), read dependency (wr) and anti-dependency (rw: one transaction reads a version and another installs the next). A history is serializable exactly when the graph has no cycle, so each non-serializable anomaly is a cycle of a certain kind. The kind of cycle, more than the pattern of operations, says how strong a level must be to forbid it.

| anomaly | example | smallest cycle | allowed by read committed | allowed by snapshot isolation |
|---|---|---|---|---|
| dirty write | $w_1(x)\, w_2(x)\, w_2(y)\, c_2\, w_1(y)\, c_1$ | G0: ww, ww | no | no |
| aborted read | $w_1(x)\, r_2(x)\, a_1\, c_2$ | none, G1a | no | no |
| intermediate read | $w_1(x)\, r_2(x)\, w_1(x)\, c_1\, c_2$ | none, G1b | no | no |
| circular information flow | $w_1(x)\, r_2(x)\, w_2(y)\, r_1(y)\, c_1\, c_2$ | G1c: wr, wr | no | no |
| lost update | $r_1(x)\, r_2(x)\, w_2(x)\, c_2\, w_1(x)\, c_1$ | G-single: rw, ww | yes | no |
| non-repeatable read | $r_1(x)\, w_2(x)\, c_2\, r_1(x)\, c_1$ | G-single: rw, wr | yes | no |
| read skew | $r_1(x)\, w_2(x)\, w_2(y)\, c_2\, r_1(y)\, c_1$ | G-single: rw, wr | yes | no |
| phantom | $r_1(P)\, w_2(y \in P)\, c_2\, r_1(P)\, c_1$ | G-single with a predicate rw arc | yes | no, but see below |
| write skew | $r_1(x)\, r_2(y)\, w_1(y)\, w_2(x)\, c_1\, c_2$ | G2-item: rw, rw | yes | yes |
| read-only anomaly | three transactions, see below | G2-item: rw, rw, wr | yes | yes |

Read committed is taken here in the sense of Adya's PL-2 (no G1) and snapshot isolation in the sense of Berenson et al. The first four rows do not need a cycle among committed transactions to be wrong, which is why levels forbid them by rules about writes and aborts. The next four have a cycle with exactly one anti-dependency arc (G-single); a level that forbids G-single, such as Adya's PL-2+ or snapshot isolation, rules them out. The last two have two anti-dependency arcs, and only full serializability rules them out.

**Phantoms under snapshot isolation.** A transaction under snapshot isolation that repeats a predicate read gets the same rows, so the strict phantom A3 cannot occur. The broad P3 can: Berenson et al. mark it "sometimes possible" for snapshot isolation. The bad cases are write skews over a predicate, where two transactions each check that no matching row exists and then each insert one.

## Examples

**A lost increment.** A counter $x = 100$. $T_1$ adds 30 and $T_2$ adds 20; both read 100. $T_2$ writes 120 and commits, then $T_1$ writes 130 and commits. One increment is lost; this is H4 of Berenson et al. Read committed allows it, because every read returns committed data and no write is dirty. Snapshot isolation aborts $T_1$ by first-committer-wins. An atomic `UPDATE ... SET x = x + 30` or a `SELECT ... FOR UPDATE` avoids it at read committed.

**A dirty write breaks recovery.** $x = 0$. $T_1$ writes $x = 1$; $T_2$ writes $x = 2$ and commits; $T_1$ aborts. Undo restores the before-image of $T_1$, $x = 0$, and erases the committed write of $T_2$. Undo by before-images is correct only if no other transaction wrote the item in between, so locking systems hold write locks to the end of the transaction at every level.

**Read skew in a transfer.** Accounts $x = y = 50$. $T_2$ moves 40 from $x$ to $y$. $T_1$ reads $x = 50$ before the transfer and $y = 90$ after it, and reports a total of 140. Neither value was a dirty read, and $T_1$ did not read anything twice, so P1 and the strict A2 miss it. The broad P2 forbids it, and so does snapshot isolation, where $T_1$ reads $y = 50$ from its snapshot.

**The read-only anomaly.** Checking $x = 0$ and savings $y = 0$. $T_2$ withdraws 10 from checking and charges a fee of 1 if $x + y$ would go negative. $T_1$ deposits 20 into savings. $T_3$ only reads. Under snapshot isolation: $T_2$ reads $x = 0, y = 0$; $T_1$ deposits and commits; $T_3$ reads $x = 0, y = 20$ and commits; $T_2$ writes $x = -11$ and commits. The fee says $T_2$ came before $T_1$, and $T_3$ says $T_1$ came before $T_3$ and $T_3$ before $T_2$. Without $T_3$ the history is serializable as $T_2\, T_1$.

## Where it is used

- **Defining isolation levels.** The SQL standard, and the levels of Berenson et al. and of Adya on the [isolation levels](/isolation-levels/) and [Adya's isolation levels](/adya-isolation-levels/) pages, are lists of forbidden anomalies.
- **Checking applications.** [Robustness against weak isolation](/robustness-against-weak-isolation/) asks whether a given set of transaction programs can show any anomaly at a given level. If not, the weak level gives serializable results for that workload.
- **Choosing a fix.** Once the anomaly is known, the fix is local: an atomic update or a lock for a lost update, a snapshot for read skew, a materialized conflict or [serializable snapshot isolation](/serializable-snapshot-isolation/) for write skew, and [predicate locking](/predicate-locking/) or [key-range locking](/key-range-locking/) for phantoms.
- **Testing databases.** Test tools run concurrent transactions against a database and look for the patterns above, or for cycles of the dependency graph, in the observed history. Results of such tests have shown that products with the same level name allow different anomalies.

## References
