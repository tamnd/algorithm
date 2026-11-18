---
tag: 4T8VBW
kind: definition
slug: strict-schedule
name: Strict schedule
aliases:
- strictness of schedules
area: databases/transactions-and-concurrency
level: core
summary: A schedule in which no item is read or overwritten until the last transaction that wrote it has committed or aborted.
prereqs: [cascadeless-schedule]
see_also: [recoverable-schedule, cascadeless-schedule, strict-two-phase-locking, commitment-ordering, undo-log, write-ahead-logging, external-consistency, linearizability]
sources:
  - paper: doi:10.1145/42267.42272
    title: Vassos Hadzilacos, A theory of reliability in database systems, Journal of the ACM 35(1), 1988, pages 121 to 145
    locator: strict histories, their place inside the cascadeless class, and recovery by before images
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (strict executions and before images) and Chapter 2 (strict histories)
  - paper: doi:10.1109/32.92915
    title: Yuri Breitbart, Dimitrios Georgakopoulos, Marek Rusinkiewicz and Abraham Silberschatz, On rigorous transaction scheduling, IEEE Transactions on Software Engineering 17(9), 1991, pages 954 to 960
    locator: the definition of rigorous schedules and their properties
---

A [schedule](/transaction-schedule/) is *strict* (ST) if no transaction reads or writes an item while another transaction that wrote the item earlier is still active. It is the smallest of the three recovery classes of Hadzilacos (1988): every strict schedule [avoids cascading aborts](/cascadeless-schedule/) and is [recoverable](/recoverable-schedule/). Its practical value is that an abort can be done physically, by writing back the old value of every item that the transaction wrote. Most lock based systems produce strict schedules, because [strict two-phase locking](/strict-two-phase-locking/) does.

The word "strict" here is about aborts. It is not the same as *strict serializability*, which is serializability plus the real-time order of transactions that do not overlap; see [external consistency](/external-consistency/) and [linearizability](/linearizability/).

## Definition

**Definition (Hadzilacos 1988).** A schedule $S$ is *strict* if for all $i \ne j$, every item $x$ and every action $o_i(x) \in \{r_i(x), w_i(x)\}$:

$$w_j(x) <_S o_i(x) \implies a_j <_S o_i(x) \text{ or } c_j <_S o_i(x).$$

ST denotes the class.

**The last writer is enough.** The summary speaks of the *last* writer of $x$. The two forms are the same. *Proof.* The definition implies the last-writer form at once. For the other direction, assume the last-writer form. We show the definition for $o_i(x)$ by induction on its position in $S$. Let $w_j(x) <_S o_i(x)$ with $i \ne j$, and let $w_k(x)$ be the last write of $x$ before $o_i(x)$. If $k = j$, the last-writer form says that $T_j$ ended before $o_i(x)$. If $k \ne j$, then $w_j(x) <_S w_k(x) <_S o_i(x)$, and $w_k(x)$ is an earlier action of a transaction other than $T_j$. By the induction hypothesis for $w_k(x)$, $T_j$ ended before $w_k(x)$, so also before $o_i(x)$. $\square$

**ST is inside ACA, and the inclusion is strict.** *Proof.* If $T_i$ reads $x$ from $T_j$, then $w_j(x) <_S r_i(x)$ and $T_j$ has not aborted before $r_i(x)$. Strictness gives $c_j <_S r_i(x)$, which is the ACA condition. The schedule $w_1(x)\ w_2(x)\ c_1\ c_2$ reads nothing, so it is in ACA, and it is not strict. $\square$

**Recovery by before images.** The *before image* of $w_j(x)$ is the value of $x$ just before that write. Undo $a_j$ by writing back the before images of the writes of $T_j$, last write first. *Claim:* if $S\,a_j$ is strict, this gives every item the value of its last write by a transaction that did not abort, or its initial value if there is none. *Proof sketch.* Fix $x$ and the first write $w_j(x)$ of $T_j$. By strictness, every earlier writer of $x$ ended before $w_j(x)$, so (by induction on the number of aborts) the value just before $w_j(x)$ is the last write of $x$ by a committed transaction, or the initial value. By strictness again, no other transaction writes $x$ between $w_j(x)$ and $a_j$. So restoring the before image of the first write of $T_j$, which the reverse order does last, gives the right value. $\square$

Without strictness this fails. Take $x = 1$ and $w_1(x{=}2)\ w_2(x{=}3)\ a_1\ a_2$. The undo of $T_1$ writes back $1$, and the undo of $T_2$ then writes back $2$, the value of an aborted transaction. The right final value is $1$.

**Basic facts.**

- *Prefix closed.* The condition on an action depends only on the actions before it.
- *How a scheduler gets ST.* Hold every exclusive lock until commit or abort, as [strict two-phase locking](/strict-two-phase-locking/) does. Then any $o_i(x)$ after $w_j(x)$ needs a lock that conflicts with the exclusive lock of $T_j$, and it gets that lock only after $T_j$ has ended. Read locks may be released earlier.
- *Not a serializability condition.* A strict schedule need not be [conflict serializable](/conflict-serializability/). Strict two-phase locking gives both, because the two-phase rule gives serializability and the long exclusive locks give strictness.

## Examples and non-examples

**Examples.**

- $w_1(x)\ c_1\ r_2(x)\ w_2(x)\ c_2$ is strict.
- $r_1(x)\ w_2(x)\ c_1\ c_2$ is strict: a write after a read of an active transaction is allowed. The condition only looks at earlier writes.
- $r_1(x)\ r_2(x)\ w_1(x)\ c_1\ w_2(x)\ c_2$ is strict and is a lost update. With $T_1 = r_1(x)\ w_1(x)\ c_1$ and $T_2 = r_2(x)\ w_2(x)\ c_2$, six of the 20 complete schedules are strict, and four of them are not conflict serializable.
- $r_1(x)\ r_2(y)\ w_1(y)\ w_2(x)\ c_1\ c_2$ is strict but not conflict serializable: $T_1 \to T_2$ on $x$ and $T_2 \to T_1$ on $y$.

**Non-examples.**

- $w_1(x)\ w_2(x)\ c_1\ c_2$ is in ACA but not strict: $T_2$ overwrites $x$ while $T_1$ is active. This is the *dirty write*.
- $w_1(x)\ r_2(x)\ c_1\ c_2$ is recoverable, not in ACA and so not strict.
- $w_1(x)\ w_1(y)\ w_2(y)\ c_1\ c_2$ is not strict, although no transaction reads anything and the schedule is serializable.

## Related definitions

- **[Cascadeless schedules](/cascadeless-schedule/)** (ACA) forbid only the dirty read. **[Recoverable schedules](/recoverable-schedule/)** (RC) only order the commits. ST $\subset$ ACA $\subset$ RC.
- **Rigorous schedules** (Breitbart, Georgakopoulos, Rusinkiewicz and Silberschatz 1991) add the mirror rule for reads: if $r_j(x) <_S w_i(x)$ with $i \ne j$, then $T_j$ ended before $w_i(x)$. So no two conflicting actions of active transactions ever overlap. A rigorous schedule is strict, and its committed projection is conflict serializable in commit order. *Proof.* For committed $T_i, T_j$ and conflicting actions $p_j <_S q_i$, rigor gives $c_j <_S q_i <_S c_i$. So every arc of the [conflict graph](/conflict-graph/) goes from the earlier to the later commit, and the commit order is a topological order. $\square$ Strong strict two-phase locking, which holds all locks until the end, produces rigorous schedules. The same argument shows that rigorous schedules satisfy [commitment ordering](/commitment-ordering/): conflicting committed transactions commit in the order of their conflicts.
- **Strict serializability** has nothing to do with this class. It is serializability in an order that respects real time, the database analogue of [linearizability](/linearizability/).
- **[Undo logs](/undo-log/) and [write-ahead logging](/write-ahead-logging/)** store before images. Strictness is what makes those before images enough to undo an aborted transaction at the item level.

## References
