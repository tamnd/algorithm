---
title: Conservative 2PL gives conflict serializable schedules in admission order, never deadlocks and never starves
proves: [correctness]
status: full
---

Two lock modes of different transactions *conflict* unless both are S. For a transaction $T$, $L(T)$ is its declared lock set from line L1: X on each item it writes and S on each item it only reads. So the lock of $T$ on $x$ covers every action of $T$ on $x$. A transaction is *admitted* at line L6, and the moment of line L6 is its *lock point* $\mathrm{LP}(T)$. A transaction is *waiting* while it is in the list $W$. The scheduler runs the actions of admitted transactions only, and line L7 rejects an action that its locks do not cover.

**Lemma 1 (safety).** At every moment, two different transactions never hold conflicting locks on the same item.

*Proof.* Locks are granted only at line L6, and only when no lock of $L(T)$ conflicts with a lock held by another transaction. Other steps only release locks. So by induction over the steps, the claim holds after each step. $\square$

**Lemma 2 (two-phase).** Each transaction gets all its locks at its lock point and gets no lock after it. Each lock covers its actions, from before the first action on the item to after the last one.

*Proof.* Line L6 grants all of $L(T)$ in one step, and no other line grants a lock. An action of $T$ runs only after admission. A lock on $x$ is released at line L8 only after the last access of $T$ to $x$, or at line L9 at the end of $T$. $\square$

**Theorem 1 (serializability).** The committed projection of every output schedule is conflict equivalent to the serial schedule of its committed transactions in the order of their lock points.

*Proof.* Let $p_i(x)$ come before $q_j(x)$ in the schedule, $i \ne j$, with at least one of them a write. Their locks on $x$ conflict, because at least one is X, and each lock is held while its action runs (Lemma 2). By Lemma 1 they are not held at the same time, so $T_i$ released its lock on $x$ before $T_j$ got its lock on $x$. By Lemma 2, $\mathrm{LP}(T_i)$ is not later than the moment when $T_i$ got its lock on $x$, which is before the release, and $T_j$ got its lock on $x$ at $\mathrm{LP}(T_j)$. So $\mathrm{LP}(T_i) < \mathrm{LP}(T_j)$. Every pair of conflicting actions of committed transactions is therefore in lock-point order. The serial schedule in lock-point order has the same actions, and it puts every such pair in the same order, so the two are conflict equivalent. This is the argument of the [two-phase locking theorem](/two-phase-locking-theorem/), for a schedule in which every transaction is two-phase. $\square$

**The wait-for graph.** The edges are $T \to U$ for $T \in W$ and either $U$ holds a lock that conflicts with a lock in $L(T)$, or $U$ is before $T$ in $W$ and wants a lock that conflicts with a lock in $L(T)$.

**Lemma 3.** A transaction in $W$ holds no lock.

*Proof.* A transaction joins $W$ at line L2, before it gets any lock, and it gets locks only at line L6, where it leaves $W$. $\square$

**Theorem 2 (no deadlock).** The wait-for graph never has a cycle.

*Proof.* Let $T \to U$ be an edge. If $U$ holds a lock, then by Lemma 3, $U \notin W$, and $U$ has no edge out of it. Otherwise $U$ is before $T$ in $W$. So along any path, the nodes in $W$ come strictly earlier in $W$ at each step, and the path can end at a holder, after which it stops. A cycle would need a node in $W$ to come before itself. $\square$

**Lemma 4.** After each call of ADMIT, if $W$ is not empty, the first transaction in $W$ conflicts with a lock held by another transaction.

*Proof.* In the pass of ADMIT, the set of locks wanted by earlier waiters is empty when the pass reaches the first transaction that it does not admit. That transaction stays in $W$ only because a lock of $L(T)$ conflicts with a held lock. The transactions before it in the pass were admitted, so it is the first in $W$ after the pass. $\square$

**Theorem 3 (progress).** If every admitted transaction runs its remaining actions whenever the arrival order offers them, then every transaction is admitted and ends.

*Proof.* An admitted transaction never waits again: line L7 needs no new lock, and lines L8 and L9 only release. So an admitted transaction ends after its remaining actions are offered, which happens because the arrival order offers each action and the driver runs the first transaction that does not wait.

Now let $T$ be the first transaction in $W$. While $T$ is first, no transaction $U$ that conflicts with $T$ is admitted. Such a $U$ is either already in $W$ behind $T$ or comes later, and in each pass of ADMIT the pass reaches $T$ first and, because $T$ stays in $W$, adds the locks of $T$ to the wanted locks; then $U$ fails the test of line L5. So the set of holders whose locks conflict with $L(T)$ only shrinks while $T$ is first. Each of them is admitted and ends, by the first paragraph. Its release at line L8 or L9 calls ADMIT, and after the last such release, $T$ conflicts with no held lock and has no earlier waiter, so the pass admits it. The next transaction in $W$ is then first, and the same argument applies. By induction along $W$, every transaction is admitted.

In particular, the driver never reaches a state in which every unfinished transaction waits: by Lemma 4, if $W$ is not empty then some transaction holds a lock, and that transaction is admitted and has an action left. $\square$

**Theorem 4 (strictness).** With strict = true, every output schedule is strict: if $w_j(x)$ comes before $o_i(x)$ with $i \ne j$, then $T_j$ ended before $o_i(x)$.

*Proof.* $T_j$ holds X on $x$ from before $w_j(x)$ until line L9 at its end, and $o_i(x)$ needs a lock on $x$ that conflicts with X. By Lemma 1, $T_i$ gets that lock only after the release at the end of $T_j$, so $o_i(x)$ comes after the end of $T_j$. $\square$

With strict = false, Theorem 4 fails: the page gives $w_1(x)\, r_2(x)\, c_2\, r_1(y)\, c_1$, which is not even recoverable. Theorems 1 to 3 do not use the release rule, so they hold for both settings.

The tests check Lemma 1, Lemma 3 and Theorem 2 after every step, and Theorems 1, 3 and 4 on every output, on all interleavings of four sets of two or three short transactions and on 50 random interleavings of four or six. Theorem 1 is checked with the helper `dbsched`, by conflict equivalence of the committed projection with the serial schedule in lock-point order, which is the definition and does not use a conflict graph.
