---
tag: G0MPST
kind: definition
slug: recoverable-schedule
name: Recoverable schedule
aliases:
- recoverability
area: databases/transactions-and-concurrency
level: core
summary: A schedule in which each transaction commits only after every transaction whose writes it read has committed.
prereqs: [transaction-schedule, serializability]
see_also: [cascadeless-schedule, strict-schedule, strict-two-phase-locking, conflict-serializability, crash-recovery, commitment-ordering, two-phase-locking, acid-properties]
sources:
  - paper: doi:10.1145/42267.42272
    title: Vassos Hadzilacos, A theory of reliability in database systems, Journal of the ACM 35(1), 1988, pages 121 to 145
    locator: the recoverable, cascadeless and strict classes of histories and their inclusions
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (recoverability, cascading aborts, strict executions) and Chapter 2 (recoverable histories)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: the chapter on transaction recovery (the classes RC, ACA, ST and rigorousness)
---

A [schedule](/transaction-schedule/) is *recoverable* (RC) if no transaction commits before every transaction it read from has committed. It is the weakest of the three recovery classes of Hadzilacos (1988), with [cascadeless](/cascadeless-schedule/) and [strict](/strict-schedule/) schedules inside it. Recoverability is about aborts, not about interleaving: [serializability](/serializability/) looks only at the committed projection, so a serializable schedule can still let a committed transaction keep a value that an abort later erases. A recoverable schedule never needs to undo a commit, which the D of the [ACID properties](/acid-properties/) forbids.

## Definition

Let $S$ be a schedule, and use the *reads-from* relation of the [schedule page](/transaction-schedule/): $T_i$ reads $x$ from $T_j$ ($i \ne j$) if $w_j(x) <_S r_i(x)$, $T_j$ has not aborted before $r_i(x)$, and every write of $x$ between them belongs to a transaction that aborted before $r_i(x)$.

**Definition (Hadzilacos 1988).** $S$ is *recoverable* if for all $i \ne j$:

$$T_i \text{ reads some item from } T_j \text{ in } S \text{ and } c_i \in S \implies c_j \in S \text{ and } c_j <_S c_i.$$

RC denotes the class of recoverable schedules.

**Why the condition is the right one.** Assume that $S$ is recoverable and that the active transaction $T_j$ aborts now, so the schedule becomes $S\,a_j$. Every transaction that read from $T_j$ has seen a value that no longer exists, so it must abort too, and so must every transaction that read from one of those, and so on. *Claim:* in a recoverable $S$, none of these transactions is committed. *Proof.* Let $T_j = T_{k_0}, T_{k_1}, \ldots, T_{k_m}$ be a chain in which each $T_{k_t}$ reads from $T_{k_{t-1}}$. We show by induction on $t$ that $T_{k_t}$ is not committed. For $t = 0$, $T_j$ is active. If $T_{k_{t-1}}$ is not committed and $T_{k_t}$ were committed, the definition would need $c_{k_{t-1}} \in S$, a contradiction. $\square$

So in a recoverable schedule every abort can be completed by aborting active transactions only. In a schedule that is not recoverable, some abort would require undoing a commit.

**Basic facts.**

- *Prefix closed.* If $S$ is recoverable, so is every prefix $S'$. The reads-from pairs of $S'$ are those of $S$ whose read lies in $S'$, since they depend only on the actions before the read. If $c_i \in S'$, then $c_j <_S c_i$, so $c_j$ is also in $S'$.
- *A scheduler enforces RC by delaying commits.* Every schedule without commits is recoverable. A scheduler can let $T_i$ read uncommitted data, and then hold back $c_i$ until all the transactions that $T_i$ read from have committed. If one of them aborts, it aborts $T_i$ instead.
- *Inclusions.* ST $\subset$ ACA $\subset$ RC, and both inclusions are strict. The proof of the inclusions is on the [serializability](/serializability/) page; the examples below show that they are strict.
- *Independent of serializability.* RC and the class of schedules whose committed projection is [conflict serializable](/conflict-serializability/) are incomparable. Every serial schedule is in both.

## Examples and non-examples

The table gives one schedule for each region of the diagram of the classes RC, ACA (avoids cascading aborts) and ST (strict), crossed with conflict serializability (CSR) of the committed projection. Each row is in the classes marked "yes" and in no other class of the table.

| schedule | RC | ACA | ST | CSR |
|---|---|---|---|---|
| $w_1(x)\ r_2(x)\ c_2\ c_1$ | no | no | no | yes |
| $w_1(x)\ r_2(x)\ w_2(y)\ r_1(y)\ c_2\ c_1$ | no | no | no | no |
| $w_1(x)\ r_2(x)\ c_1\ c_2$ | yes | no | no | yes |
| $w_1(x)\ r_2(x)\ r_2(y)\ w_1(y)\ c_1\ c_2$ | yes | no | no | no |
| $w_1(x)\ w_2(x)\ c_1\ c_2$ | yes | yes | no | yes |
| $r_1(x)\ w_2(x)\ w_1(x)\ c_1\ c_2$ | yes | yes | no | no |
| $w_1(x)\ c_1\ r_2(x)\ c_2$ | yes | yes | yes | yes |
| $r_1(x)\ r_2(y)\ w_1(y)\ w_2(x)\ c_1\ c_2$ | yes | yes | yes | no |

**The dirty read that commits.** In the first row, $T_2$ reads $x$ from $T_1$ and commits first. If $T_1$ now aborts, the database must erase the value of $T_1$, but $T_2$ is committed and may have shown that value to a user. The schedule is conflict equivalent to the serial schedule $T_1 T_2$, so serializability alone does not catch this.

**Recoverable but with a cascade.** In the third row, $T_2$ waits with its commit until $T_1$ has committed. Had $T_1$ aborted instead of committing, $T_2$ would have had to abort too. That is allowed in RC; the [cascadeless](/cascadeless-schedule/) class forbids it.

**Recoverable but not serializable.** In the fourth row, $T_2$ reads $x$ after $w_1(x)$ and reads $y$ before $w_1(y)$. The [conflict graph](/conflict-graph/) has the cycle $T_1 \to T_2 \to T_1$, but the commit order is correct for the only reads-from pair.

**Reads-from across an abort.** $w_1(x)\ w_2(x)\ r_3(x)\ a_2\ c_1\ c_3$ is not recoverable: $T_3$ reads $x$ from $T_2$, because $a_2$ comes after the read, and $T_3$ commits although $T_2$ never does. The variant $w_1(x)\ w_2(x)\ a_2\ r_3(x)\ c_1\ c_3$ is recoverable: after the abort, $T_3$ reads $x$ from $T_1$, which commits before $T_3$.

**Not a property of the committed projection.** The committed projection of $w_1(x)\ r_2(x)\ a_1\ c_2$ is $r_2(x)\ c_2$, which is recoverable. The schedule itself is not. Recoverability must be checked on the full schedule, with its aborts.

## Related definitions

- **[Cascadeless schedules](/cascadeless-schedule/)** (ACA) ask more: a transaction reads only committed data. Then an abort never forces another abort.
- **[Strict schedules](/strict-schedule/)** (ST) ask more again: no item is read or overwritten while its last writer is still active. Then the abort of a transaction is undone by writing back the before images of its writes. [Strict two-phase locking](/strict-two-phase-locking/) produces strict schedules.
- **[Two-phase locking](/two-phase-locking/)** in its basic form gives conflict serializable schedules that need not be recoverable: a transaction may release an exclusive lock after its lock point and before its commit, and another transaction may read the item and commit first.
- **[Commitment ordering](/commitment-ordering/)** is a different condition on commit order: it orders the commits of conflicting transactions in the order of their conflicts. It is about serializability, not about aborts.
- **[Crash recovery](/crash-recovery/)** handles the aborts of all transactions that were active at a crash. Recoverability of the schedule is what makes that possible without touching committed work.

## References
