---
tag: YQV7PJ
kind: definition
slug: serializability
name: Serializability
aliases:
- serializable schedule
- serializable execution of transactions
area: systems/database-algorithms
level: core
summary: "A concurrent schedule of transactions is serializable if it is equivalent to some serial schedule. Final-state, view and conflict equivalence give three nested classes."
prereqs: [acid-properties]
see_also: [conflict-serializability, view-serializability, conflict-graph, concurrency-control, isolation-levels, two-phase-locking, linearizability, opacity]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: consistency of a schedule as equivalence to a serial schedule, and the proof that serial schedules preserve consistency
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979, pages 631 to 653
    locator: the definition of serializability by equivalence of final states, the NP-completeness of the test, and the subclasses that are easy to test
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 2 (histories, serializable histories, the Serializability Theorem, and recoverable, cascadeless and strict histories)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (final-state, view and conflict serializability and the relations between the classes)
  - book: isbn:9781558601901
    title: Jim Gray and Andreas Reuter, Transaction Processing, Concepts and Techniques, Morgan Kaufmann, 1993
    locator: Chapter 7 (isolation concepts, dependencies between transactions and degrees of isolation)
---

A schedule of concurrent transactions is *serializable* if it is equivalent to some serial schedule, one that runs the same transactions one after the other with no interleaving. It is the meaning of the I in the [ACID properties](/acid-properties/): each transaction can be written as if it ran alone, because the system only allows interleavings that have the same effect as some order of running them alone. The word "equivalent" has three standard meanings (final-state, view and [conflict](/conflict-serializability/) equivalence), which give three nested classes of schedules. Separate conditions (recoverable, avoids cascading aborts, strict) say how commits and aborts may interleave.

## Definition

**Transactions and schedules.** A transaction $T_i$ is a sequence of actions $r_i(x)$ (read item $x$) and $w_i(x)$ (write item $x$), followed by either $c_i$ (commit) or $a_i$ (abort). A *schedule* (or history) $S$ over a set of transactions holds all their actions and keeps the order inside each transaction. We write $p <_S q$ when action $p$ comes before $q$. The schedule is *serial* when, for any two transactions, all actions of one come before all actions of the other. The *committed projection* $C(S)$ keeps the reads and writes of the committed transactions only. Two actions *conflict* if they belong to different transactions, touch the same item, and at least one is a write.

**Interpretation.** To compare schedules without knowing what the programs compute, assume that each write $w_i(x)$ stores an unknown function of all the values that $T_i$ has read before it. This is the Herbrand semantics of Papadimitriou (1979). A schedule then determines the value seen by each read and the final value of each item, as formal terms.

**Three equivalences.** Let $S$ and $S'$ be schedules over the same committed transactions.

- *Final-state equivalence:* $C(S)$ and $C(S')$ leave every item with the same final value under the interpretation above.
- *View equivalence:* in addition, each read sees the same value. Equivalently, each read reads from the same write, and each item has the same last write. See [view serializability](/view-serializability/).
- *Conflict equivalence:* every pair of conflicting actions of $C(S)$ is in the same order in $C(S')$. See [conflict serializability](/conflict-serializability/).

$S$ is *final-state serializable*, *view serializable* or *conflict serializable* if it is equivalent in that sense to some serial schedule. Write FSR, VSR and CSR for the three classes. A plain "serializable" in a database manual means the guarantee that the scheduler gives, which is normally conflict serializability or a property that implies it.

**Theorem 1 (the hierarchy).** $\text{CSR} \subsetneq \text{VSR} \subsetneq \text{FSR}$.

*Proof.* Conflict equivalence fixes the order of each read relative to every write of the same item by another transaction, and the order of any two writes of the same item; inside one transaction the order is fixed anyway. So it fixes which write each read reads from and which write is last, and CSR is contained in VSR (the full argument is Theorem 1 on the view serializability page). View equivalent schedules give each read the same value and each item the same final value, by induction along the schedule, so VSR is contained in FSR. The schedule $r_1(x)\, w_2(x)\, w_1(x)\, w_3(x)$ is in VSR and not in CSR, and the schedule $S_4$ in the examples is in FSR and not in VSR. $\square$

**Theorem 2 (Papadimitriou 1979).** Deciding whether a schedule is serializable in the final-state or the view sense is NP-complete. Conflict serializability can be decided in polynomial time with the [conflict graph](/conflict-graph/).

**Why serializability gives consistency.** Let each transaction, run alone on a database that satisfies the integrity constraints, leave a database that satisfies them. Then a serial schedule preserves the constraints, by induction on the number of transactions. A final-state serializable schedule leaves the same final state as some serial schedule, so it preserves them too. View serializability gives more: each transaction also reads a state that the serial schedule would show it, so it never acts on, or reports, inconsistent data.

**Recoverability.** Serializability looks only at committed transactions. The following conditions control what an abort can do. Say that $T_i$ *reads $x$ from* $T_j$ ($i \ne j$) if $r_i(x)$ comes after $w_j(x)$, $T_j$ has not aborted before $r_i(x)$, and every write of $x$ between them belongs to a transaction that aborted before $r_i(x)$ (an abort restores the value that its transaction overwrote).

- $S$ is *recoverable* (RC) if, whenever $T_i$ reads from $T_j$ and $T_i$ commits, $T_j$ commits before $T_i$ commits. Otherwise a committed transaction can depend on a value that an abort later erases, and the commit cannot be undone.
- $S$ *avoids cascading aborts* (ACA) if, whenever $T_i$ reads $x$ from $T_j$, $T_j$ has committed before that read. Then an abort never forces another abort.
- $S$ is *strict* (ST) if no item written by a transaction $T_j$ is read or written by another transaction before $T_j$ commits or aborts. Then an abort can be undone by restoring the *before image* of each item that the transaction wrote.

**Theorem 3 (Bernstein, Hadzilacos and Goodman, Chapter 2).** $\text{ST} \subsetneq \text{ACA} \subsetneq \text{RC}$.

*Proof.* Let $S$ be strict and let $T_i$ read $x$ from $T_j$ at the read $r_i(x)$. Then $w_j(x) <_S r_i(x)$, and strictness says that $T_j$ committed or aborted before $r_i(x)$. It did not abort before the read, by the definition of reads-from, so it committed before it. Hence $S$ is ACA. Let $S$ be ACA, let $T_i$ read from $T_j$, and let $T_i$ commit. Then $c_j$ comes before the read, which comes before $c_i$, so $S$ is RC. The examples below show that both inclusions are strict. $\square$

Every serial schedule is strict, because each transaction ends before the next one starts. Apart from that, the two families are independent: in the table below, the second row is conflict serializable but does not avoid cascading aborts, and the last row is strict but not conflict serializable. Locking schedulers such as [strict two-phase locking](/strict-two-phase-locking/) are designed to give both conflict serializability and strictness.

## Examples and non-examples

**The lost update is not serializable.** $S_1 = r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)\ c_1\ c_2$. Under the interpretation, the final value of $x$ is $f_2(x_0)$, a function of the initial value only. In $T_1 T_2$ it is $f_2(f_1(x_0))$ and in $T_2 T_1$ it is $f_1(f_2(x_0))$. So $S_1$ is not even final-state serializable. If both transactions add 1, one addition is lost.

**View but not conflict serializable.** $S_2 = r_1(x)\ w_2(x)\ w_1(x)\ w_3(x)\ c_1\ c_2\ c_3$ is view equivalent to $T_1 T_2 T_3$ ($T_1$ reads the initial $x$, $T_3$ writes the final one), but $r_1(x) < w_2(x)$ and $w_2(x) < w_1(x)$ form a conflict cycle.

**An aborted transaction does not count.** $S_3 = r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)\ c_1\ a_2$ is the lost update with $T_2$ aborted. Its committed projection is $r_1(x)\, w_1(x)$, which is serial.

**Final-state but not view serializable.** $S_4 = r_2(x)\ w_1(x)\ r_2(x)\ c_2\ c_1$. The read-only transaction $T_2$ reads two different values of $x$, so no serial order explains what it saw, and $S_4$ is not view serializable. But $T_2$ writes nothing, so its reads do not reach the final state, and $S_4$ leaves the same state as $T_1 T_2$. This is why final-state serializability is too weak for practice: a report printed by $T_2$ shows a state that never existed.

**Recoverability classes.** All four schedules commit both transactions.

| schedule | RC | ACA | ST | why |
|---|---|---|---|---|
| $w_1(x)\ r_2(x)\ c_2\ c_1$ | no | no | no | $T_2$ reads from $T_1$ and commits first |
| $w_1(x)\ r_2(x)\ c_1\ c_2$ | yes | no | no | $T_2$ reads $x$ before $T_1$ commits; if $T_1$ aborted, $T_2$ would have to abort |
| $w_1(x)\ w_2(x)\ c_1\ c_2$ | yes | yes | no | no read of uncommitted data, but $T_2$ overwrites uncommitted data, so the before image of $T_1$ is wrong for $T_2$ |
| $r_1(x)\ r_2(y)\ w_1(y)\ w_2(x)\ c_1\ c_2$ | yes | yes | yes | strict, but the conflict graph has the cycle $T_1 \to T_2 \to T_1$ |

**Reads-from across an abort.** In $w_1(x)\ w_2(x)\ a_2\ r_3(x)\ c_1\ c_3$ the abort of $T_2$ restores the value of $T_1$, so $T_3$ reads $x$ from $T_1$. The schedule is recoverable but does not avoid cascading aborts, since $T_1$ commits after the read.

## Related definitions

- **[Conflict serializability](/conflict-serializability/)** and **[view serializability](/view-serializability/)** are the two classes used in practice and in theory; the [conflict graph](/conflict-graph/) tests the first.
- **[Concurrency control](/concurrency-control/)** is the problem of building a scheduler whose output schedules are serializable and recoverable. [Two-phase locking](/two-phase-locking/), [timestamp ordering](/timestamp-ordering/) and [optimistic concurrency control](/optimistic-concurrency-control/) are the classic solutions.
- **[Isolation levels](/isolation-levels/)** weaken serializability on purpose. [Snapshot isolation](/snapshot-isolation/) is a well-known level that is not serializable.
- **Strict serializability** adds the real-time order: if $T_i$ commits before $T_j$ starts, $T_i$ must come before $T_j$ in the equivalent serial order. Papadimitriou (1979) studied this class. It is what [linearizability](/linearizability/) gives for single operations on objects; linearizability alone says nothing about transactions over many objects, and serializability alone ignores real time.
- **[Opacity](/opacity/)** is the condition used for [transactional memory](/software-transactional-memory/). It asks that committed transactions be strictly serializable and that every transaction, including one that later aborts, read a consistent state. Serializability only constrains committed transactions, because a database transaction that reads inconsistent data is aborted before it can do harm, while an in-memory transaction can loop or crash first.
- **[Two-phase commit](/two-phase-commit/)** is about atomic commitment across sites, not about the order of transactions; a distributed database needs both.

## References
