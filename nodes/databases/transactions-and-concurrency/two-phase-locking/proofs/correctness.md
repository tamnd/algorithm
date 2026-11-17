---
title: Two-phase locking produces conflict serializable schedules in the order of the lock points
proves: [correctness]
status: full
---

**Setting.** A scheduler runs transactions under the rules of the pseudocode. Before $r_i(x)$ the transaction $T_i$ holds a shared (S) or exclusive (X) lock on $x$, and before $w_i(x)$ it holds an X lock on $x$. Two locks on the same item by different transactions *conflict* unless both are S locks, and the lock manager never grants a lock that conflicts with a lock that another transaction holds (line L4). A transaction keeps its lock on $x$ at least until its last action on $x$ (line L8 releases only items that the transaction will not touch again). An upgrade from S to X counts as the acquisition of an X lock. The *two-phase rule* (line L3) says that no transaction acquires a lock after it has released one.

For an attempt of $T_i$ that commits, the *lock point* $\mathrm{LP}(T_i)$ is the time of its last lock acquisition. For an item $x$ and a mode, the *lock interval* of $T_i$ is the time from the acquisition of that lock (or of the upgrade) to its release. Times are positions in the sequence of lock events, reads and writes.

**Lemma 1 (aborted attempts).** An attempt that the deadlock rule aborts (line L5) has released no lock, so no other transaction has read or overwritten an item that the attempt wrote.

*Proof.* The victim is on a cycle of the wait-for graph, so it waits for a lock. Its next action needs a lock that it does not have. If it had released a lock earlier, the two-phase rule would forbid this request (line L3). So it has released nothing. Its writes are on items under its X locks, which no other transaction can lock in any mode, so no other transaction has read or written those items since the writes. $\square$

So the abort is undone by restoring the before images, and the attempt can be removed from the schedule. From now on, $S$ is the committed projection: the actions of the last attempt of each committed transaction, in schedule order.

**Lemma 2 (conflicting actions are separated by locks).** Let $p_i(x) <_S q_j(x)$ be conflicting actions of $T_i$ and $T_j$ in $S$. Then $T_i$ releases its lock on $x$ before $T_j$ acquires the lock that it uses for $q_j(x)$.

*Proof.* At least one of the two actions is a write. Let $L_i$ be the lock of $T_i$ on $x$ that covers $p_i(x)$: the X lock if $p$ is a write, and the S or X lock that $T_i$ holds at $p$ if $p$ is a read. Define $L_j$ for $q_j(x)$ in the same way. If $p$ or $q$ is a write, the matching lock is X, so $L_i$ and $L_j$ conflict. The interval of $L_i$ contains the time of $p$, and the interval of $L_j$ contains the time of $q$, because each transaction keeps its lock until its last action on $x$. Two conflicting locks are never held at the same time, so the two intervals are disjoint. The interval of $L_i$ starts before $p$, and $p$ comes before $q$, which is inside the interval of $L_j$. If the interval of $L_j$ came first, it would end before the interval of $L_i$ starts, so before $p$ and before $q$; this contradicts that it contains $q$. So the interval of $L_i$ comes first, and $T_i$ releases $x$ before $T_j$ acquires $L_j$. $\square$

**Theorem 1 (Eswaran, Gray, Lorie and Traiger 1976).** The conflict graph of $S$ is acyclic. More precisely, every edge $T_i \to T_j$ has $\mathrm{LP}(T_i) < \mathrm{LP}(T_j)$, so $S$ is conflict equivalent to the serial schedule that runs the committed transactions in the order of their lock points.

*Proof.* An edge $T_i \to T_j$ comes from conflicting actions $p_i(x) <_S q_j(x)$. Let $\mathrm{rel}_i(x)$ be the time at which $T_i$ releases the lock $L_i$ of Lemma 2 and let $\mathrm{acq}_j(x)$ be the time at which $T_j$ acquires $L_j$. By the two-phase rule, every acquisition of $T_i$ comes before every release of $T_i$, so $\mathrm{LP}(T_i) < \mathrm{rel}_i(x)$. Lemma 2 gives $\mathrm{rel}_i(x) < \mathrm{acq}_j(x)$. By the definition of the lock point, $\mathrm{acq}_j(x) \le \mathrm{LP}(T_j)$. Together,

$$\mathrm{LP}(T_i) < \mathrm{rel}_i(x) < \mathrm{acq}_j(x) \le \mathrm{LP}(T_j).$$

A cycle $T_1 \to T_2 \to \cdots \to T_1$ would give $\mathrm{LP}(T_1) < \mathrm{LP}(T_1)$, which is false, so the graph is acyclic. Sorting the transactions by lock point gives a topological order of the graph, because every edge goes from a smaller to a larger lock point. By the serializability theorem (an acyclic conflict graph and any of its topological orders give a conflict equivalent serial schedule), $S$ is conflict equivalent to the serial schedule in lock-point order. $\blacksquare$

**Theorem 2 (the rule cannot be weakened).** Let $T_1$ be a transaction that releases a lock on $x$ and later acquires a lock on $y$, and that touches each item it locks while it holds the lock. Then there is a two-phase transaction $T_2$ and a schedule that obeys the lock rules (without the two-phase rule for $T_1$) and is not conflict serializable.

*Proof.* Let $T_2$ lock $x$ and $y$ in X mode, write both, and release both. Run $T_1$ up to and including its release of $x$; it has touched $x$ while it held the lock. Then run all of $T_2$: its X lock on $x$ is free now, and $T_1$ holds no lock on $y$ yet. Then let $T_1$ lock and touch $y$. The action of $T_1$ on $x$ comes before $w_2(x)$ and conflicts with it, so $T_1 \to T_2$. The write $w_2(y)$ comes before the action of $T_1$ on $y$ and conflicts with it, so $T_2 \to T_1$. The conflict graph has a cycle. $\blacksquare$

Theorem 2 is the reason why the two-phase rule is the right rule when the scheduler knows only which items each transaction locks: any transaction that breaks it can be paired with a partner that produces a non-serializable schedule.

**Remark (what the theorem does not say).** Theorem 1 is about the committed projection. It does not say that the schedule is recoverable. A transaction past its lock point may release an X lock before it commits; another transaction may then read the item and commit first. If the writer later aborts for a reason other than a deadlock (a failure or a user abort), the reader has read a value that never existed. [Strict two-phase locking](/strict-two-phase-locking/) closes this gap by holding X locks until commit.
