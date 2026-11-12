---
tag: 65GB6K
kind: problem
slug: concurrency-control
name: Concurrency control problem
aliases:
- database concurrency control
area: systems/database-algorithms
level: core
summary: "Build a scheduler that interleaves the actions of concurrent transactions, by running, delaying or rejecting each one, so that the output is serializable and recoverable."
prereqs: [serializability, acid-properties]
see_also: [two-phase-locking, timestamp-ordering, optimistic-concurrency-control, multiversion-concurrency-control, conflict-graph, wait-die-and-wound-wait, isolation-levels, software-transactional-memory]
sources:
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 1 (the scheduler model), Chapter 3 (two-phase locking), Chapter 4 (non-locking schedulers, timestamp ordering and serialization graph testing) and Chapter 5 (multiversion concurrency control)
  - paper: doi:10.1145/356842.356846
    title: Philip A. Bernstein and Nathan Goodman, Concurrency control in distributed database systems, ACM Computing Surveys 13(2), 1981, pages 185 to 221
    locator: the decomposition into read-write and write-write synchronization, and the survey of locking and timestamp methods
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: the scheduling problem for consistent transactions, two-phase locking and predicate locks
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (concurrency control algorithms) and Chapter 5 (multiversion concurrency control)
  - paper: doi:10.1145/319566.319567
    title: H. T. Kung and John T. Robinson, On optimistic methods for concurrency control, ACM Transactions on Database Systems 6(2), 1981, pages 213 to 226
    locator: the read, validation and write phases of an optimistic scheduler
---

The concurrency control problem asks for a *scheduler*: a component that receives the reads and writes of many concurrent transactions and decides, for each one, to run it now, to delay it, or to reject it and abort its transaction, so that the result is [serializable](/serializability/) and recoverable while as many interleavings as possible are allowed. It is the problem behind the I of the [ACID properties](/acid-properties/). The classic solutions are [two-phase locking](/two-phase-locking/), [timestamp ordering](/timestamp-ordering/), [optimistic concurrency control](/optimistic-concurrency-control/) and [multiversion concurrency control](/multiversion-concurrency-control/).

## In plain words

Many people use a bank's database at the same time. If the database ran their requests one at a time, everyone would wait. If it mixed the steps of all requests freely, two people could change the same balance at once and one change could be lost.

A scheduler sits between the requests and the data. Each time a request wants to read or change a record, the scheduler decides: go ahead, wait, or give up and start again. A good scheduler lets many requests run side by side, and still makes the final result look as if the requests ran one after another in some order. It must also make sure that a cancelled request leaves no trace that others have used.

## Definition

**Input.** A set of transactions $T_1, T_2, \ldots$ arrives over time. Each transaction issues one action at a time: $r_i(x)$, $w_i(x)$, and finally $c_i$ (commit request) or $a_i$ (abort). The scheduler sees an action only when its transaction issues it. It does not know the future actions, unless the variant says that transactions declare their read and write sets at the start.

**Decisions.** For each action the scheduler may

1. *execute* it, which appends it to the output schedule;
2. *delay* it, which blocks its transaction until a later decision; or
3. *reject* it, which aborts its transaction. The transaction may restart later as a new attempt.

**Output.** The output is the schedule $S$ of executed actions, with commits and aborts.

**Requirements.**

- *Safety.* The committed projection of every output schedule is in a target class, normally [conflict serializable](/conflict-serializability/) schedules. The output must also be recoverable, and normally strict, so that aborts can be undone by restoring before images (the classes are defined on the [serializability](/serializability/) page). Every prefix of the output must meet the same demand, because a crash can stop the system at any point.
- *Liveness.* The scheduler never blocks forever: a [deadlock](/deadlock/) must be prevented or detected and broken. Ideally every transaction that keeps restarting eventually commits, so no transaction starves.
- *Concurrency.* Among safe schedulers, prefer one that executes more interleavings without delay and rejects fewer actions. Bernstein, Hadzilacos and Goodman describe a scheduler as a filter: the set of input interleavings that it passes through unchanged measures how much concurrency it allows.

## Variants

- **Pessimistic or optimistic.** A pessimistic scheduler prevents a conflict before it happens, by locks or timestamps, and delays or rejects at access time. An optimistic scheduler lets transactions run on private copies and checks for conflicts at commit time (Kung and Robinson 1981). The first pays with waiting and deadlocks, the second with wasted work when validation fails.
- **What the scheduler uses to order transactions.** Locks ([two-phase locking](/two-phase-locking/), [strict two-phase locking](/strict-two-phase-locking/)), timestamps fixed at start ([timestamp ordering](/timestamp-ordering/), the [Thomas write rule](/thomas-write-rule/)), the conflict graph itself (serialization graph testing), or the commit order (optimistic validation).
- **Single version or multiversion.** With several versions of each item, a read can be served from an older version instead of waiting or aborting. [Multiversion concurrency control](/multiversion-concurrency-control/) and [snapshot isolation](/snapshot-isolation/) use this; snapshot isolation is not serializable, and [serializable snapshot isolation](/serializable-snapshot-isolation/) repairs it.
- **Weaker targets.** The target class can be one of the weaker [isolation levels](/isolation-levels/) instead of serializability.
- **Predicates and phantoms.** When transactions read sets of rows given by a condition, locks on single rows are not enough; see the [phantom problem](/phantom-problem/) and [predicate locking](/predicate-locking/).
- **Distributed data.** With data on several sites, each site runs a local scheduler, and an atomic commit protocol such as [two-phase commit](/two-phase-commit/) makes all sites agree on commit or abort. Bernstein and Goodman (1981) split the problem into read-write and write-write synchronization and combine a method for each.
- **Transactional memory.** The same problem on memory words, with [software transactional memory](/software-transactional-memory/), adds the demand of [opacity](/opacity/) for transactions that will abort, and drops durability.

## Examples

Take the input interleaving of the lost update, where $T_1$ starts before $T_2$:

$$r_1(x)\ r_2(x)\ w_1(x)\ w_2(x)\ c_1\ c_2.$$

Its conflict graph has the cycle $T_1 \to T_2 \to T_1$, so a correct scheduler must change it.

| scheduler | what happens |
|---|---|
| strict two-phase locking | $T_1$ and $T_2$ get shared locks on $x$. $w_1(x)$ waits for $T_2$, then $w_2(x)$ waits for $T_1$: a deadlock. The detector aborts one of them, say $T_2$, and $T_1$ writes and commits. |
| wound-wait | At $w_1(x)$ the older $T_1$ wounds the younger $T_2$, which aborts at once; $T_1$ writes and commits. |
| basic timestamp ordering, $ts(T_1) = 1$, $ts(T_2) = 2$ | After $r_2(x)$ the read timestamp of $x$ is 2. $w_1(x)$ has timestamp $1 < 2$, so it is rejected and $T_1$ aborts; $w_2(x)$ and $c_2$ are executed. |
| optimistic, backward validation | Both run on private copies. $T_1$ validates first and commits. $T_2$ read $x$, which $T_1$ wrote after $T_2$ started, so $T_2$ fails validation and restarts. |
| serialization graph testing | $w_1(x)$ adds the edge $T_2 \to T_1$ and is executed. $w_2(x)$ would add $T_1 \to T_2$ and close a cycle, so it is rejected and $T_2$ aborts. |

Every scheduler aborts one transaction here, because the input cannot be made serializable by delays that keep both reads before both writes. The difference lies in which one it aborts, when, and how much work is lost.

A friendlier input such as $r_1(x)\ w_1(x)\ r_2(y)\ w_2(y)\ c_1\ c_2$, where the transactions touch different items, passes through all of these schedulers unchanged.

## Known algorithms

| method | type | target | deadlock possible | page |
|---|---|---|---|---|
| two-phase locking | pessimistic, locks | conflict serializable | yes | [two-phase locking](/two-phase-locking/) |
| strict and rigorous 2PL | pessimistic, locks | conflict serializable and strict | yes | [strict two-phase locking](/strict-two-phase-locking/) |
| 2PL with wait-die or wound-wait | pessimistic, locks and timestamps | as above | no | [wait-die and wound-wait](/wait-die-and-wound-wait/) |
| conservative 2PL (all locks at start) | pessimistic, predeclared sets | conflict serializable | no | [two-phase locking](/two-phase-locking/) |
| basic timestamp ordering | pessimistic, timestamps | conflict serializable in timestamp order | no (no waiting) | [timestamp ordering](/timestamp-ordering/) |
| Thomas write rule | timestamps | view serializable | no | [Thomas write rule](/thomas-write-rule/) |
| serialization graph testing | conflict graph | all conflict serializable schedules | no (no waiting) | [conflict graph](/conflict-graph/) |
| optimistic (Kung and Robinson) | validation at commit | conflict serializable | no | [optimistic concurrency control](/optimistic-concurrency-control/) |
| multiversion schemes | versions | serializable or snapshot isolation | depends | [multiversion concurrency control](/multiversion-concurrency-control/) |

## Bounds

The problem has no single cost measure. The facts below are exact statements about the classes of schedules and the cost of the decisions.

- **Testing the target.** Conflict serializability of a finished schedule is decided in polynomial time by the [conflict graph](/conflict-graph/), and every prefix of a conflict serializable schedule is conflict serializable. View serializability is NP-complete to test (Papadimitriou 1979) and is not closed under prefixes, so no practical online scheduler targets it exactly.
- **Serialization graph testing passes exactly the conflict serializable inputs.** It executes an action unless that action closes a cycle, so it passes an input unchanged exactly when the input is conflict serializable. Its cost is a cycle check per new edge, and the graph must keep committed transactions until they have no incoming edges.
- **Two-phase locking and timestamp ordering pass incomparable sets.** Both pass only conflict serializable inputs, and each passes some that the other does not. With timestamps given in the order of the first actions, the input $r_2(z)\ w_1(x)\ c_1\ r_2(x)\ c_2$ passes two-phase locking ($T_1$ locks, writes and commits before $T_2$ asks for $x$), but timestamp ordering rejects $r_2(x)$ because the older $T_2$ would read a value of the younger $T_1$. The input $r_3(z)\ r_1(x)\ w_2(x)\ w_3(y)\ w_1(y)$ passes timestamp ordering, with timestamps 1, 2 and 3 for $T_3$, $T_1$ and $T_2$, but no two-phase locking execution produces it without delays: $T_1$ must give up its lock on $x$ before $w_2(x)$, so it must already hold its lock on $y$, and then $w_3(y)$ could not run.
- **Deadlock and starvation.** Two-phase locking with waiting can deadlock: the example above shows it with two transactions. Wait-die and wound-wait prevent deadlock and, because a restarted transaction keeps its timestamp, also prevent starvation. Basic timestamp ordering never waits, so it never deadlocks, but a transaction that restarts with a new timestamp can in principle be rejected again and again.
- **Cost per action.** A lock manager with a hash table on item names handles a lock request in $O(1)$ expected time plus the time to queue it. Timestamp ordering keeps two timestamps per item and decides in $O(1)$ time. Deadlock detection costs a cycle search in the [wait-for graph](/wait-for-graph/), in time linear in its size.

## Reductions

- **To graph acyclicity.** The safety demand for conflict serializability is the absence of cycles in the conflict graph. Every scheduler above is proved correct by showing that the conflict graph of its output agrees with a fixed order: lock points for two-phase locking, timestamps for timestamp ordering, validation order for optimistic methods. A [topological order](/topological-sort/) of the graph is the equivalent serial order.
- **Deadlock handling to cycle detection or prevention.** A locking scheduler needs [deadlock detection](/deadlock-detection/) on the wait-for graph, or a [prevention](/deadlock-prevention/) rule such as a global lock order or the timestamp rules of wait-die and wound-wait.
- **Read-write and write-write synchronization.** Bernstein and Goodman (1981) show that a scheduler is correct when it orders read-write conflicts and write-write conflicts by compatible orders, which lets one combine a locking method for one kind with a timestamp method for the other.

## Applications

Every relational database and many key-value stores run a scheduler of this kind. Lock-based systems use strict two-phase locking with a deadlock detector or a timeout, and add key-range locks against phantoms. Multiversion systems serve reads from snapshots and use locks or validation only for writes. In-memory transactional systems use optimistic validation, because their transactions are short and the cost of a lock table is high compared to the work. The same ideas appear in [software transactional memory](/software-transactional-memory/), where [contention management](/contention-management/) plays the role of the deadlock and starvation policy.

## References
