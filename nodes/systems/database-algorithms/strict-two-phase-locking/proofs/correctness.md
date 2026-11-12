---
title: Strict 2PL gives strict, conflict serializable schedules, and rigorous 2PL serializes in commit order
proves: [correctness]
status: full
---

**Setting.** The scheduler follows the pseudocode. Before $r_i(x)$ the transaction $T_i$ holds an S or X lock on $x$, and before $w_i(x)$ it holds an X lock on $x$. Conflicting locks (any pair that is not two S locks) are never held by two transactions at the same time. No transaction acquires a lock after it has released one. Under *strict* 2PL, a transaction releases its X locks only at commit (line L8) or after its undo at abort (line L9); it may release an S lock earlier, at line L7, once it holds all its locks and will not touch the item again. Under *rigorous* 2PL, it releases every lock only at commit or abort. Before each write the scheduler saves the *before image*, the value that the write overwrites.

**Theorem 1 (strictness).** Every schedule produced by strict 2PL is strict: if $w_j(x) <_S o_i(x)$ for a read or write $o_i$ of another transaction $T_i$, then $T_j$ has committed or aborted before $o_i(x)$.

*Proof.* At $w_j(x)$ the transaction $T_j$ holds an X lock on $x$, and under strict 2PL it keeps that lock until it commits, or until it aborts and has undone its writes. At $o_i(x)$ the transaction $T_i$ holds a lock on $x$, which conflicts with the X lock of $T_j$. So the X lock of $T_j$ was released before $T_i$ got its lock, and that happens only when $T_j$ commits or aborts. $\square$

By Theorem 3 on the [serializability](/serializability/) page, a strict schedule also avoids cascading aborts and is recoverable.

**Lemma 2 (undo by before images).** When $T_j$ aborts, restoring its before images in reverse order of its writes gives every item the value that it would have if the attempt of $T_j$ had never run.

*Proof.* Let $x$ be an item that $T_j$ wrote. From the first write of $x$ by $T_j$ until the abort, $T_j$ holds an X lock on $x$, so no other transaction reads or writes $x$ in that time. The before image of the first write of $x$ by $T_j$ is the value of $x$ just before $T_j$ touched it. Restoring the before images in reverse order ends with this value for $x$. Items that $T_j$ did not write are not changed. No other transaction read a value written by $T_j$ (by the same X lock), so nothing else depends on the attempt. $\square$

So each aborted attempt can be deleted from the schedule without changing what the other transactions read or the state that they leave. From now on, $C$ is the committed projection: the actions of the committed attempts, in schedule order.

**Theorem 3 (serializability).** $C$ is conflict serializable, and it is conflict equivalent to the serial schedule of the committed transactions in the order of their lock points.

*Proof.* Strict and rigorous 2PL are special cases of two-phase locking: they obey the two-phase rule and the lock compatibility rules, and they only delay releases. The theorem of [two-phase locking](/two-phase-locking/) applies to the committed attempts: for each edge $T_i \to T_j$ of the conflict graph of $C$, $\mathrm{LP}(T_i) < \mathrm{LP}(T_j)$. $\square$

Conflict equivalence fixes which write each read reads from and which write is last on each item (see [view serializability](/view-serializability/), Theorem 1). With Lemma 2, every committed transaction reads the same values and the database ends in the same state as in the serial run in lock-point order. The test file checks exactly this, value by value.

**Theorem 4 (rigorous 2PL serializes in commit order).** Under rigorous 2PL, every edge $T_i \to T_j$ of the conflict graph of $C$ has $c_i <_S c_j$. So $C$ is conflict equivalent to the serial schedule in commit order.

*Proof.* The edge comes from conflicting actions $p_i(x) <_S q_j(x)$. As in the proof for 2PL, $T_i$ releases its lock on $x$ before $T_j$ acquires the lock that covers $q_j(x)$. Under rigorous 2PL, $T_i$ releases its locks only at commit, so $c_i$ comes before that acquisition, which comes before $q_j(x)$, which comes before $c_j$. $\blacksquare$

**Strict 2PL does not always serialize in commit order.** Let $T_1 = r_1(x)\, w_1(y)\, r_1(z)$ and $T_2 = w_2(x)$. Under strict 2PL, $T_1$ reaches its lock point at $r_1(z)$ and may release its S lock on $x$. Then $T_2$ writes $x$ and commits before $T_1$. The conflict $r_1(x) < w_2(x)$ gives $T_1 \to T_2$, but $c_2 < c_1$. The schedule is serializable as $T_1 T_2$, the lock-point order, and not as the commit order. Rigorous 2PL would keep the S lock on $x$ until $c_1$, so $T_2$ would commit second.
