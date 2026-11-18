---
tag: TJPXEY
kind: theorem
slug: two-phase-locking-theorem
name: Two-phase locking theorem
aliases:
- 2PL serializability theorem
area: databases/transactions-and-concurrency
level: core
summary: Every schedule produced by transactions that follow two-phase locking is conflict serializable, in the order of their lock points.
prereqs: [two-phase-locking, serializability-theorem]
see_also: [two-phase-locking, serializability-theorem, conservative-two-phase-locking, strict-two-phase-locking, tree-locking-protocol, lock-table, conflict-graph, recoverable-schedule]
sources:
  - paper: doi:10.1145/360363.360369
    title: K. P. Eswaran, J. N. Gray, R. A. Lorie and I. L. Traiger, The notions of consistency and predicate locks in a database system, Communications of the ACM 19(11), 1976, pages 624 to 633
    locator: two-phase transactions, the theorem that they give consistent schedules, and the theorem that a transaction that is not two-phase has a partner that gives an inconsistent schedule
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 3 (the Two Phase Locking Theorem and its proof with the serialization graph)
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 4 (locking schedulers and the correctness of 2PL)
---

The two-phase locking theorem says that if every transaction locks an item before it uses it, and never acquires a lock after it has released one, then the committed work is [conflict serializable](/conflict-serializability/), and the serial order is the order in which the transactions reach their *lock points*. Eswaran, Gray, Lorie and Traiger proved it in 1976, together with a partial converse: a single transaction that breaks the two-phase rule can always be paired with a two-phase partner so that the result is not serializable. The theorem is the correctness argument behind the [two-phase locking](/two-phase-locking/) scheduler and all its variants. It is a statement about serializability only; deadlocks and recoverability are separate questions.

## Statement

**Locked schedules.** Extend the [schedule](/transaction-schedule/) model with lock actions $sl_i(x)$ (shared lock), $xl_i(x)$ (exclusive lock) and $u_i(x)$ (release all locks of $T_i$ on $x$). An $xl_i(x)$ while $T_i$ holds a shared lock on $x$ is an *upgrade*. A locked schedule $L$ is

- *well formed* if each $r_i(x)$ happens while $T_i$ holds a lock on $x$ in some mode, each $w_i(x)$ happens while $T_i$ holds an exclusive lock on $x$, and $T_i$ releases each of its locks at the latest right after its terminal action;
- *legal* if two different transactions never hold locks on the same item at the same time unless both locks are shared;
- *two-phase* if, for each $T_i$, no lock action of $T_i$ follows a release $u_i(\cdot)$ of $T_i$.

The *lock point* $\mathrm{LP}(T_i)$ is the position in $L$ of the last lock action of $T_i$. Let $S$ be $L$ without its lock actions, and $C(S)$ its committed projection.

**Theorem (two-phase locking theorem).** If $L$ is well formed, legal and two-phase, then:

1. every arc $T_i \to T_j$ of the serialization graph of $C(S)$ has $\mathrm{LP}(T_i) < \mathrm{LP}(T_j)$;
2. hence $C(S)$ is conflict serializable, and it is conflict equivalent to the serial schedule of the committed transactions sorted by lock point.

**Partial converse (Eswaran et al. 1976).** Let $T$ be a transaction that is not two-phase: it releases a lock and later performs a lock action. Assume that each lock action of $T$ is a new lock or an upgrade, and covers an access of $T$ that follows it. Then there is a two-phase transaction $T'$ and a well formed, legal locked schedule of $T$ and $T'$, in which both commit, whose schedule is not conflict serializable.

**What the theorem does not give.** It does not say that the converse holds for schedules: some conflict serializable schedules have no two-phase locking. And it says nothing about deadlocks or about [recoverability](/recoverable-schedule/).

## In plain words

When two transactions conflict on an item, the locks make them take turns: the first must let go of the item before the second can take it. A two-phase transaction lets go of anything only after it holds everything it will ever hold, which is its lock point. So the first transaction reached its lock point before it let go, and the second reaches its lock point after it took over. Every conflict therefore runs from the earlier lock point to the later one, and the order of the lock points is a serial order that respects all of them.

## Proof

**Lemma (locks separate conflicts).** Let $p_i(x) <_S q_j(x)$ be conflicting actions of $T_i \ne T_j$. Let $\lambda_i$ be the lock of $T_i$ on $x$ that covers $p_i(x)$ (exclusive if $p$ is a write), and define $\lambda_j$ for $q_j(x)$ in the same way. Then $T_i$ releases $\lambda_i$ before $T_j$ acquires $\lambda_j$.

*Proof.* One of the two actions is a write, so its lock is exclusive, and the two locks conflict. Each lock is held over an interval of $L$ that contains its action. By legality the two intervals are disjoint. If the interval of $\lambda_j$ came first, it would end before the interval of $\lambda_i$ starts, so before $p_i(x)$, and so before $q_j(x)$, which it contains. That is impossible. So the interval of $\lambda_i$ comes first: $\mathrm{rel}(\lambda_i) < \mathrm{acq}(\lambda_j)$. For an upgrade, $\mathrm{acq}$ means the position of the upgrade. $\square$

*Proof of part 1.* Let $T_i \to T_j$ be an arc, from conflicting $p_i(x) <_S q_j(x)$ in $C(S)$. The release of $\lambda_i$ is a release of $T_i$, so by the two-phase rule every lock action of $T_i$ comes before it: $\mathrm{LP}(T_i) < \mathrm{rel}(\lambda_i)$. The lemma gives $\mathrm{rel}(\lambda_i) < \mathrm{acq}(\lambda_j)$. The acquisition of $\lambda_j$ is a lock action of $T_j$, so $\mathrm{acq}(\lambda_j) \le \mathrm{LP}(T_j)$. Together,

$$\mathrm{LP}(T_i) < \mathrm{rel}(\lambda_i) < \mathrm{acq}(\lambda_j) \le \mathrm{LP}(T_j).$$

*Proof of part 2.* The lock points are positions of different actions of $L$, so sorting by lock point gives a linear order of the committed transactions. By part 1, every arc goes forward in that order, so it is a topological order and the graph has no cycle. By the [serializability theorem](/serializability-theorem/), $C(S)$ is conflict equivalent to the serial schedule in that order. $\square$

*Proof of the partial converse.* Let $u(x)$ be the first release of $T$ and let $\ell(y)$ be the first lock action of $T$ after it. Before $u(x)$, $T$ held a lock on $x$ and accessed $x$ under it. Run $T$ up to and including $u(x)$, then all of $T'$, then the rest of $T$. Choose $T'$ by cases.

- *$y = x$, or $y \ne x$ and $T$ holds no lock on $y$ at $u(x)$.* Let $T' = xl'(x)\ xl'(y)\ w'(x)\ w'(y)\ u'(x)\ u'(y)\ c'$, with one lock and one write if $y = x$. Its locks are free: $T$ has released $x$, and holds nothing on $y$. The access of $T$ to $x$ before $u(x)$ conflicts with $w'(x)$, which gives $T \to T'$. The access of $T$ to $y$ that $\ell(y)$ covers comes after $w'(y)$ and conflicts with it, which gives $T' \to T$.
- *$T$ holds a shared lock on $y \ne x$ at $u(x)$, and $\ell(y)$ is an upgrade.* Let $T' = sl'(y)\ r'(y)\ xl'(x)\ w'(x)\ u'(x)\ u'(y)\ c'$. The shared lock is compatible with the one of $T$. Again the access of $T$ to $x$ gives $T \to T'$, and $r'(y)$ before the write of $T$ that the upgrade covers gives $T' \to T$.

$T'$ is two-phase in both cases, and $T$ then commits, so the serialization graph has a cycle. $\square$

**Example.** Let $T_1 = r_1(x)\ w_1(y)\ c_1$ and $T_2 = r_2(z)\ w_2(x)\ r_2(y)\ c_2$. The locked schedule

$$sl_2(z)\ r_2(z)\ sl_1(x)\ r_1(x)\ xl_1(y)\ w_1(y)\ u_1(x)\ xl_2(x)\ w_2(x)\ c_1\ u_1(y)\ sl_2(y)\ r_2(y)\ c_2\ u_2(x)\ u_2(y)\ u_2(z)$$

is well formed, legal and two-phase. $\mathrm{LP}(T_1)$ is $xl_1(y)$ at position 5, and $\mathrm{LP}(T_2)$ is $sl_2(y)$ at position 12. The schedule $S = r_2(z)\ r_1(x)\ w_1(y)\ w_2(x)\ c_1\ r_2(y)\ c_2$ has the arcs $T_1 \to T_2$ on $x$ and on $y$, and it is conflict equivalent to $T_1 T_2$ only. $T_2$ started first, but $T_1$ comes first in the serial order, as its lock point does.

## Consequences

- **Every 2PL variant is serializable.** [Strict two-phase locking](/strict-two-phase-locking/), rigorous 2PL and [conservative two-phase locking](/conservative-two-phase-locking/) produce well formed, legal, two-phase locked schedules, so the theorem applies to them directly. For [multiple granularity locking](/multiple-granularity-locking/) and [key-range locking](/key-range-locking/) the same proof works once one shows that two conflicting accesses are always covered by two conflicting locks.
- **The serialization order is known online.** A transaction that has passed its lock point has a fixed place in the serial order. A scheduler can use that place, for example to number commits, without building the serialization graph.
- **The rule is optimal for item-only knowledge.** By the partial converse, a scheduler that sees only which items each transaction locks, and allows one transaction to break the two-phase rule, cannot guarantee serializability.

## Tightness

- **Not every serializable schedule is a 2PL schedule.** $S = r_1(x)\ w_2(x)\ w_3(y)\ w_1(y)\ c_1\ c_2\ c_3$ is conflict serializable: its arcs are $T_1 \to T_2$ on $x$ and $T_3 \to T_1$ on $y$, and it is equivalent to $T_3 T_1 T_2$. Assume a well formed, legal, two-phase locking of it. $T_1$ holds a lock on $x$ at $r_1(x)$, and $T_2$ an exclusive lock on $x$ at $w_2(x)$, so by the lemma $T_1$ releases $x$ before $w_2(x)$. $T_1$ holds an exclusive lock on $y$ at $w_1(y)$, and $T_3$ one at $w_3(y)$, so by the lemma $T_1$ acquires it after $w_3(y)$. Then $T_1$ acquires a lock after $w_3(y) > w_2(x)$, so after it released $x$. This breaks the two-phase rule.
- **The partial converse needs a free partner.** It builds a partner that locks any items it likes. If all transactions must follow some other rule, transactions that are not two-phase can still be always serializable. The [tree locking protocol](/tree-locking-protocol/) is the standard example: its transactions are not two-phase, and every schedule it allows is serializable.
- **Deadlocks.** The theorem is about the schedules that are produced. Two-phase transactions can wait for each other in a cycle, and then no schedule is produced until a victim aborts; see [deadlock](/deadlock/).
- **Recoverability.** The theorem looks at $C(S)$ only. $xl_1(x)\ w_1(x)\ u_1(x)\ sl_2(x)\ r_2(x)\ c_2\ u_2(x)\ c_1$ is a two-phase locking with the schedule $w_1(x)\ r_2(x)\ c_2\ c_1$, which is conflict serializable and not [recoverable](/recoverable-schedule/).

## History

Eswaran, Gray, Lorie and Traiger, at IBM Research during the System R project, defined two-phase transactions in their 1976 paper and proved both the theorem and the partial converse in a model of entities and lock actions. Bernstein, Hadzilacos and Goodman (1987) gave the proof with the serialization graph and lock points that is used here, and called it the Two Phase Locking Theorem. Later work asked which other locking rules are safe for special data, which led to the [tree protocol](/tree-locking-protocol/) of Silberschatz and Kedem (1980) and to the graph and DAG protocols.

## References
