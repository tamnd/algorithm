---
title: Wait-die and wound-wait never deadlock, never abort the oldest transaction, and keep 2PL serializable
proves: [correctness]
status: full
---

**Setting.** Transactions lock items under rigorous [two-phase locking](/two-phase-locking/): S locks for reads, X locks for writes, and all locks are held until commit or abort. Each transaction $T$ has a timestamp $\mathrm{ts}(T)$, the time of its first start, and the timestamps are distinct. A restarted transaction keeps its timestamp. $T$ is *older* than $U$ if $\mathrm{ts}(T) < \mathrm{ts}(U)$. When the request of $T_i$ conflicts with the locks of the set $H$ of other transactions, the scheduler applies one rule, and it applies the rule again whenever it looks at a waiting transaction:

- *Wait-die:* if $T_i$ is older than every member of $H$, then $T_i$ waits (line L2); otherwise $T_i$ aborts (line L3).
- *Wound-wait:* $T_i$ aborts every member of $H$ that is younger than itself (line L4), and waits for the members that are left, which are all older (line L5).

The *wait-for graph* has an edge $T_i \to T_j$ when $T_i$ waits for a lock that $T_j$ holds.

**Lemma 1 (direction of the edges).** After each application of the rules, every edge $T_i \to T_j$ of the wait-for graph has $\mathrm{ts}(T_i) < \mathrm{ts}(T_j)$ under wait-die and $\mathrm{ts}(T_i) > \mathrm{ts}(T_j)$ under wound-wait.

*Proof.* Under wait-die, a transaction that has an older holder in its set $H$ aborts and has no edges, and a transaction that waits is older than every holder in $H$, so all its edges go to younger transactions. Under wound-wait, a waiting transaction has aborted all younger holders, so its edges go to the older ones only. Between two applications of the rules, the set $H$ of a waiting transaction can only shrink by commits and aborts of holders, because the lock manager does not grant a conflicting lock to a third transaction while the request waits (in the simulator, the rules are applied again before every step, which covers any new holder). $\square$

**Theorem 1 (no deadlock).** The wait-for graph never has a cycle.

*Proof.* Along any path of the graph the timestamps strictly increase (wait-die) or strictly decrease (wound-wait), by Lemma 1. A cycle would return to its first node with a different timestamp, which is impossible. $\square$

So in every state some unfinished transaction does not wait: a finite acyclic graph has a node with no outgoing edge. The scheduler never needs to search the graph or choose a victim after the fact.

**Theorem 2 (the oldest transaction is safe).** The oldest unfinished transaction is never aborted. Under wound-wait it never waits.

*Proof.* Under wait-die, $T_i$ aborts only when some holder in $H$ is older than $T_i$, and no unfinished transaction is older than the oldest one. Under wound-wait, a transaction is aborted only when an older transaction wounds it, and nothing is older than the oldest one. Under wound-wait, the oldest transaction waits only for older holders, and there are none. $\square$

**Corollary (no starvation).** Assume that a finite number of transactions have a smaller timestamp than $T$, and that a transaction that is never aborted eventually finishes. Then $T$ is aborted only finitely often and finishes.

*Proof.* By induction on the number of unfinished transactions older than $T$. If there are none, $T$ is the oldest and Theorem 2 says it is never aborted again, so it finishes by the assumption. Otherwise, the oldest of them is never aborted and finishes, and the claim follows for the rest by the induction hypothesis. Because $T$ keeps its timestamp on restart, new transactions are younger than $T$ and never enter the count. $\square$

The assumption that a transaction that is never aborted finishes is about the lock manager, not about the rules. Under wound-wait it holds whenever the oldest transaction gets steps, since it never waits. Under wait-die, the oldest transaction waits for younger holders; the lock manager must grant a released lock to the oldest waiting request (or keep a first-in, first-out queue) so that younger transactions cannot take the lock again and again. If a transaction got a new timestamp at each restart, it could be the youngest forever and be aborted again and again; keeping the timestamp is what prevents this.

**Theorem 3 (serializability and strictness).** The committed projection of every schedule is conflict serializable, in commit order, and the schedule is strict.

*Proof.* The rules only decide *which* transaction waits or aborts; the locking itself is rigorous two-phase locking, and aborts are undone with before images, which is correct because X locks are held until the end. The theorems of [strict two-phase locking](/strict-two-phase-locking/) apply: the schedule is strict, and every edge $T_i \to T_j$ of the conflict graph of the committed projection has $c_i < c_j$. $\blacksquare$

**The cost of prevention.** Both rules abort some transactions that are not on any cycle. Example: $T_2$ holds X on $x$ and runs; the younger $T_3$ asks for $x$. Under wait-die, $T_3$ dies, although $T_2$ would release $x$ soon and no deadlock exists. Under wound-wait, if the older $T_1$ asks for $x$, it wounds $T_2$, again without a deadlock. Detection with the [wait-for graph](/wait-for-graph/) aborts only on real cycles, at the price of searching the graph.
