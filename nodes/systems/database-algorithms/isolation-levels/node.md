---
tag: VCE808
kind: definition
slug: isolation-levels
name: Isolation levels
aliases:
- ANSI isolation levels
- SQL transaction isolation levels
- ANSI SQL-92 isolation levels
area: systems/database-algorithms
level: core
summary: "Weaker forms of serializability, named read uncommitted, read committed, repeatable read and serializable in SQL-92, and defined by the anomalies each one forbids."
prereqs: [serializability, acid-properties]
see_also: [snapshot-isolation, serializable-snapshot-isolation, phantom-problem, predicate-locking, conflict-graph, two-phase-locking, multiversion-concurrency-control, opacity]
sources:
  - paper: "American National Standards Institute, ANSI X3.135-1992, Database Language SQL, 1992"
    locator: the section on SET TRANSACTION and the table of the four isolation levels with the phenomena P1 (dirty read), P2 (non-repeatable read) and P3 (phantom)
  - paper: doi:10.1145/223784.223785
    title: Hal Berenson, Phil Bernstein, Jim Gray, Jim Melton, Elizabeth O'Neil and Patrick O'Neil, A critique of ANSI SQL isolation levels, Proceedings of ACM SIGMOD 1995, pages 1 to 10
    locator: Section 2 (the phenomena P0 to P3 and the anomalies A1 to A3), Section 3 (cursor stability, lost update P4 and P4C), Section 4 (snapshot isolation, read skew A5A and write skew A5B) and Table 4 (the levels and the phenomena they allow)
  - url: https://pmg.csail.mit.edu/papers/adya-phd.pdf
    title: Atul Adya, Weak consistency, a generalized theory and optimistic implementations for distributed transactions, PhD thesis, MIT, 1999
    locator: Chapters 3 and 4 (histories with versions, the direct serialization graph, the phenomena G0, G1 and G2, and the levels PL-1 to PL-3)
  - paper: doi:10.1109/ICDE.2000.839388
    title: Atul Adya, Barbara Liskov and Patrick O'Neil, Generalized isolation level definitions, Proceedings of the 16th International Conference on Data Engineering (ICDE), 2000, pages 67 to 78
    locator: the definitions of the DSG with ww, wr and rw edges, and of G0, G1a, G1b, G1c, G2-item and G2
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7, Isolation Concepts (degrees of isolation 0 to 3 and their locking protocols), chapter level only
---

An *isolation level* is a property of the histories that a database may produce, weaker than [serializability](/serializability/), that a transaction can choose to get more concurrency. SQL-92 names four: *read uncommitted*, *read committed*, *repeatable read* and *serializable*, and defines each by the *phenomena* that it forbids: dirty read (P1), non-repeatable read (P2) and phantom (P3). Berenson, Bernstein, Gray, Melton, O'Neil and O'Neil (1995) showed that these English definitions are ambiguous and too weak, gave exact forms P0 to P3 that match the locking levels, and added the levels *cursor stability* and *snapshot isolation*. Adya (1999) then defined the levels again by cycles in a graph of the committed transactions, so that the definitions do not forbid optimistic or multiversion implementations.

## Definition

**Histories.** A history is a sequence of operations of transactions $T_1, T_2, \ldots$: $r_i(x)$ (read item $x$), $w_i(x)$ (write $x$; an insert is a write of a new item), $c_i$ (commit) and $a_i$ (abort). A *predicate read* $r_i(P)$ reads the set of items that satisfy a condition $P$, and a write $w_j(y \in P)$ is a write of an item that satisfies $P$ before or after the write. "$\ldots$" stands for any operations, and "before $T_1$ ends" means before $c_1$ or $a_1$.

**Phenomena of Berenson et al.** Each line is a pattern; a history *shows* a phenomenon if it contains the pattern. The P forms are *broad*: they forbid the situation that could lead to an anomaly. The A forms are *strict*: they forbid only the anomaly itself.

| name | pattern | |
|---|---|---|
| P0 dirty write | $w_1(x) \ldots w_2(x) \ldots$ before $T_1$ ends | |
| P1 dirty read | $w_1(x) \ldots r_2(x) \ldots$ before $T_1$ ends | |
| A1 | $w_1(x) \ldots r_2(x) \ldots (a_1$ and $c_2$ in any order$)$ | strict P1 |
| P2 fuzzy read | $r_1(x) \ldots w_2(x) \ldots$ before $T_1$ ends | |
| A2 | $r_1(x) \ldots w_2(x) \ldots c_2 \ldots r_1(x) \ldots c_1$ | strict P2 |
| P3 phantom | $r_1(P) \ldots w_2(y \in P) \ldots$ before $T_1$ ends | |
| A3 | $r_1(P) \ldots w_2(y \in P) \ldots c_2 \ldots r_1(P) \ldots c_1$ | strict P3 |
| P4 lost update | $r_1(x) \ldots w_2(x) \ldots w_1(x) \ldots c_1$ | |
| A5A read skew | $r_1(x) \ldots w_2(x) \ldots w_2(y) \ldots c_2 \ldots r_1(y) \ldots$ ($c_1$ or $a_1$) | |
| A5B write skew | $r_1(x) \ldots r_2(y) \ldots w_1(y) \ldots w_2(x) \ldots$ ($c_1$ and $c_2$ occur) | |

P4C, the lost update with a cursor, is P4 where the read of $T_1$ is through a cursor. In the checker of this page, A5B is matched with the four operations in any order such that $r_1(x)$ comes before $w_2(x)$, $r_2(y)$ before $w_1(y)$, and all four before both commits.

**The levels.** Berenson et al. read the SQL-92 levels with the broad forms, and add that P0 is forbidden at every level:

| level | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| read uncommitted | forbidden | allowed | allowed | allowed |
| read committed | forbidden | forbidden | allowed | allowed |
| repeatable read | forbidden | forbidden | forbidden | allowed |
| serializable | forbidden | forbidden | forbidden | forbidden |

With these forms, the levels are exactly what the locking protocols give: long write locks (held to the end) prevent P0; short read locks add P1; long item read locks add P2; long predicate read locks ([predicate locking](/predicate-locking/)) add P3, which is serializability. The two added levels sit between them. *Cursor stability* forbids P0, P1 and P4C: it keeps the read lock on the row under the cursor until the cursor moves. *[Snapshot isolation](/snapshot-isolation/)* forbids P0, P1, P4, the read skew A5A and the strict A2 and A1, sometimes allows P3, and allows the write skew A5B; it is neither weaker nor stronger than repeatable read.

**The direct serialization graph.** Adya uses histories with versions: each write $w_i(x)$ creates the version $x_i$, each read names the version it reads, and the committed versions of $x$ have a total *version order*. The *direct serialization graph* $DSG(H)$ has a node for each committed transaction and these edges:

- $T_i \xrightarrow{ww} T_j$ (*write dependency*): $T_j$ installs the version of $x$ that comes next after $x_i$;
- $T_i \xrightarrow{wr} T_j$ (*read dependency*): $T_j$ reads $x_i$, or a predicate read of $T_j$ sees a version of $T_i$;
- $T_i \xrightarrow{rw} T_j$ (*anti-dependency*): $T_i$ reads $x_k$ and $T_j$ installs the version next after $x_k$, or $T_j$ installs a version that changes the items that match a predicate read of $T_i$ (a *predicate anti-dependency*).

**Phenomena of Adya.**

- **G0** (write cycle): $DSG(H)$ has a cycle of ww edges only.
- **G1a** (aborted read): a committed $T_j$ reads a version written by an aborted $T_i$.
- **G1b** (intermediate read): a committed $T_j$ reads a version of $x$ by $T_i$ that is not the last one $T_i$ wrote.
- **G1c** (circular information flow): $DSG(H)$ has a cycle of ww and wr edges only.
- **G2-item**: $DSG(H)$ has a cycle with at least one item anti-dependency edge.
- **G2**: $DSG(H)$ has a cycle with at least one anti-dependency edge, item or predicate.

G1 is G1a, G1b or G1c. The *portable levels*: PL-1 forbids G0; PL-2 forbids G1; PL-2.99 forbids G1 and G2-item; PL-3 forbids G1 and G2. They correspond to read uncommitted, read committed, repeatable read and serializable. The difference from the broad forms is that the G phenomena speak only of committed transactions and of cycles, so a system may let a transaction read data before its writer commits, or read old versions, as long as no forbidden cycle appears.

## Examples and non-examples

Each row is a history and what the definitions say about it.

| history | Berenson phenomena | level (broad) | Adya phenomena | PL level |
|---|---|---|---|---|
| $w_1(x)\, w_2(x)\, w_2(y)\, c_2\, w_1(y)\, c_1$ | P0 | none | G0, G1c | none |
| $w_1(x)\, r_2(x)\, c_2\, a_1$ | P1, A1 | read uncommitted | G1a | PL-1 |
| $w_1(x)\, r_2(x)\, w_1(x)\, c_1\, c_2$ | P1, P2 | read uncommitted | G1b | PL-1 |
| H1: $r_1(x)\, w_1(x)\, r_2(x)\, r_2(y)\, c_2\, r_1(y)\, w_1(y)\, c_1$ | P1 | read uncommitted | G2-item | PL-2 |
| H2: $r_1(x)\, r_2(x)\, w_2(x)\, r_2(y)\, w_2(y)\, c_2\, r_1(y)\, c_1$ | P2, A5A | read committed | G2-item | PL-2 |
| $r_1(x)\, w_2(x)\, c_2\, r_1(x)\, c_1$ | P2, A2 | read committed | G2-item | PL-2 |
| H4: $r_1(x)\, r_2(x)\, w_2(x)\, c_2\, w_1(x)\, c_1$ | P2, P4 | read committed | G2-item | PL-2 |
| H5: $r_1(x)\, r_1(y)\, r_2(x)\, r_2(y)\, w_1(y)\, w_2(x)\, c_1\, c_2$ | P2, A5B | read committed | G2-item | PL-2 |
| H3: $r_1(P)\, w_2(y \in P)\, r_2(z)\, w_2(z)\, c_2\, r_1(z)\, c_1$ | P3 | repeatable read | G2 | PL-2.99 |
| $r_1(x)\, w_1(x)\, c_1\, r_2(x)\, w_2(x)\, c_2$ | none | serializable | none | PL-3 |

**H1, H2 and H3 are the cases of Berenson et al.** that defeat the strict forms. In H1 ($x$ and $y$ are accounts with 50 each, and $T_1$ moves 40 from $x$ to $y$), $T_2$ reads $x = 10$ and $y = 50$ and sees a total of 60 instead of 100; $T_1$ commits, so A1 does not occur, but the history is not serializable. P1 rejects it. In H2 the same total is read wrongly by $T_1$ without any re-read, so A2 does not occur; P2 rejects it, and it is the read skew A5A. In H3, $T_1$ reads the employees that satisfy $P$ and then a count $z$ that $T_2$ has updated after inserting an employee; $T_1$ never repeats the predicate read, so A3 does not occur, but P3 rejects it.

**H1 is PL-2.** Adya's read committed level accepts H1, because $T_1$ commits and no cycle of ww and wr edges exists; the cycle $T_1 \xrightarrow{wr} T_2 \xrightarrow{rw} T_1$ has an anti-dependency, so H1 is not PL-3. The broad P1 rejects H1 at read committed already.

**The broad forms forbid serializable histories.** The history $r_1(x)\, w_2(x)\, c_2\, c_1$ is serializable ($T_1$ before $T_2$), but it shows P2, so it is not at the broad repeatable read level. This is the cost of the preventative reading: it describes locking, and it rules out an optimistic scheduler that would allow this history. Adya's PL-3 accepts it.

**Snapshot reads.** If both reads of a transaction come from one snapshot, as in $r_1(x_0)\, w_2(x)\, w_2(y)\, c_2\, r_1(y_0)\, c_1$, the read skew is gone and the history is PL-3, while the same operations read in place give A5A. With versions, H5 is the *write skew* of [snapshot isolation](/snapshot-isolation/): both transactions read the initial versions and write different items, and the DSG has the cycle $T_1 \xrightarrow{rw} T_2 \xrightarrow{rw} T_1$, which is G2-item.

## Related definitions

- [Serializability](/serializability/) is the strongest level; [conflict serializability](/conflict-serializability/) is its testable form, and the [conflict graph](/conflict-graph/) is close to the DSG: on histories where every transaction commits and touches each item at most once (a read, a write, or a read and then a write), the DSG is acyclic exactly when the conflict graph is acyclic.
- The [phantom problem](/phantom-problem/) is P3; [predicate locking](/predicate-locking/) is the locking answer to it.
- [Two-phase locking](/two-phase-locking/) with long locks of all kinds gives serializable; the shorter lock durations give the weaker levels.
- [Snapshot isolation](/snapshot-isolation/) is an isolation level outside the SQL-92 list, and [serializable snapshot isolation](/serializable-snapshot-isolation/) is a way to make it serializable.
- [Multiversion concurrency control](/multiversion-concurrency-control/) is the usual way to build snapshot and read committed levels without read locks.
- [Opacity](/opacity/) is the correctness condition of transactional memory. It asks that even transactions that abort see a consistent state, which no database isolation level demands, and it has no durability part.

## References
