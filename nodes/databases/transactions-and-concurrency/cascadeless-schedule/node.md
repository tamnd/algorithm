---
tag: E7X2PT
kind: definition
slug: cascadeless-schedule
name: Cascadeless schedule
aliases:
- ACA schedule
- avoiding cascading aborts
area: databases/transactions-and-concurrency
level: core
summary: A schedule in which transactions read only values written by committed transactions, so one abort never forces another.
prereqs: [recoverable-schedule]
see_also: [recoverable-schedule, strict-schedule, strict-two-phase-locking, transaction-schedule, transaction-anomalies, isolation-levels, crash-recovery, two-phase-locking]
sources:
  - paper: doi:10.1145/42267.42272
    title: Vassos Hadzilacos, A theory of reliability in database systems, Journal of the ACM 35(1), 1988, pages 121 to 145
    locator: the class of histories that avoid cascading aborts and its place between the recoverable and strict classes
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (cascading aborts) and Chapter 2 (histories that avoid cascading aborts)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: the chapter on transaction recovery (the classes RC, ACA and ST)
---

A [schedule](/transaction-schedule/) *avoids cascading aborts* (ACA), or is *cascadeless*, if every transaction reads only values that committed transactions wrote, apart from its own writes. Then the abort of one transaction never forces the abort of another. The class lies strictly between the [recoverable](/recoverable-schedule/) and the [strict](/strict-schedule/) schedules of Hadzilacos (1988). In SQL terms, an ACA schedule has no dirty reads; it does not stop dirty writes, which is the extra step that strictness takes.

## Definition

Use the *reads-from* relation of the [schedule page](/transaction-schedule/): $T_i$ reads $x$ from $T_j$ ($i \ne j$) if $w_j(x) <_S r_i(x)$, $T_j$ has not aborted before $r_i(x)$, and every write of $x$ between them belongs to a transaction that aborted before $r_i(x)$.

**Definition (Hadzilacos 1988).** A schedule $S$ *avoids cascading aborts* if for all $i \ne j$ and every item $x$:

$$T_i \text{ reads } x \text{ from } T_j \text{ in } S \implies c_j <_S r_i(x).$$

ACA denotes the class. The condition is on each read at the moment it happens, not on commits: a transaction may not read a value whose writer is still active.

**Cascading aborts.** In a schedule outside ACA, an abort can spread. In

$$S = w_1(x)\ r_2(x)\ w_2(y)\ r_3(y)\ a_1,$$

$T_2$ read $x$ from $T_1$, so after $a_1$ the value that $T_2$ saw does not exist, and $T_2$ must abort. $T_3$ read $y$ from $T_2$, so it must abort as well. $S$ is [recoverable](/recoverable-schedule/), since nothing has committed, so the cascade is legal, but it wastes the work of $T_2$ and $T_3$, and the chain can be as long as the number of active transactions.

**Claim.** If $S$ is in ACA and an active transaction $T_j$ aborts, no other transaction must abort. *Proof.* A transaction must abort only if it read from a transaction that aborts. In ACA, if $T_i$ reads from $T_j$, then $c_j \in S$, so $T_j$ is not active. Therefore no transaction read from $T_j$, and the cascade has no first step. $\square$

**ACA is inside RC, and the inclusion is strict.** *Proof.* Let $S \in$ ACA, and let $T_i$ read $x$ from $T_j$ with $c_i \in S$. Then $c_j <_S r_i(x) <_S c_i$, which is the condition of recoverability. The schedule $w_1(x)\ r_2(x)\ c_1\ c_2$ is recoverable but $T_2$ reads $x$ before $c_1$, so it is not in ACA. $\square$

**Basic facts.**

- *Prefix closed.* Whether a read satisfies the condition depends only on the actions before it, so every prefix of an ACA schedule is in ACA.
- *How a scheduler gets ACA.* It delays every read $r_i(x)$ until the last writer of $x$ that is still active has committed or aborted. [Strict two-phase locking](/strict-two-phase-locking/) does this, and more, by holding exclusive locks until the end of the transaction.
- *Independent of serializability.* An ACA schedule need not be [conflict serializable](/conflict-serializability/), and a serial order of the committed work does not give ACA. The [recoverable schedule](/recoverable-schedule/) page has one example for each combination.

## Examples and non-examples

**Examples.**

- $w_1(x)\ c_1\ r_2(x)\ c_2$ is in ACA: $T_2$ reads $x$ after $c_1$.
- $w_1(x)\ r_1(x)\ c_1$ is in ACA: a transaction may read its own uncommitted write. The definition asks $i \ne j$.
- $w_1(x)\ w_2(x)\ c_1\ c_2$ is in ACA, because nothing is read, but it is not strict: $T_2$ overwrites $x$ while $T_1$ is active. If $T_1$ aborted, restoring the old value of $x$ would also erase the write of $T_2$.
- $r_1(x)\ w_2(x)\ w_1(x)\ c_1\ c_2$ is in ACA but not conflict serializable: the conflict graph has $T_1 \to T_2$ from $r_1(x)$ and $w_2(x)$, and $T_2 \to T_1$ from the two writes.

**Non-examples.**

- $w_1(x)\ r_2(x)\ c_1\ c_2$ is recoverable but not in ACA: $T_2$ reads $x$ while $T_1$ is active, and it would have to abort if $T_1$ did.
- $w_1(x)\ w_2(x)\ a_2\ r_3(x)\ c_1\ c_3$ is not in ACA. After $a_2$, the write of $T_2$ no longer counts, so $T_3$ reads $x$ from $T_1$, which is still active. The abort of $T_2$ does not make the read safe.
- $w_1(x)\ w_2(y)\ r_1(y)\ c_2\ c_1$ is not in ACA, although it is serializable: $r_1(y)$ comes before $c_2$.

**All schedules of two increments.** Let $T_1 = r_1(x)\ w_1(x)\ c_1$ and $T_2 = r_2(x)\ w_2(x)\ c_2$. Of the 20 complete schedules, 14 are in ACA, but only the two serial schedules are in ACA and conflict serializable at the same time. In the other twelve ACA schedules both transactions read $x$ before either writes it, which is the lost update. So ACA protects against aborts, and gives nothing against bad interleavings.

## Related definitions

- **[Recoverable schedules](/recoverable-schedule/)** (RC) only ask that a reader commit after its writer. They allow cascades, but never a committed transaction that must be undone.
- **[Strict schedules](/strict-schedule/)** (ST) also forbid overwriting an item whose last writer is active. Then an abort can be undone by restoring before images. ST is strictly inside ACA.
- **Read committed.** The [isolation level](/isolation-levels/) READ COMMITTED forbids dirty reads, which is the ACA condition. Most systems get it by short read locks or by reading the last committed version.
- **[Transaction anomalies](/transaction-anomalies/).** The dirty read (P1 in the ANSI critique) is the pattern that ACA rules out; the dirty write (P0) is the pattern that ST also rules out.
- **[Crash recovery](/crash-recovery/)** aborts all active transactions after a crash. With ACA, these aborts do not reach any transaction that committed or that survives.

## References
