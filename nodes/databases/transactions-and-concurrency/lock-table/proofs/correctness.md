---
title: The lock table grants only compatible locks, loses no wake-up, and its wait-for graph shows every deadlock
proves: [correctness]
status: full
---

The modes come with $\mathit{compat}$ and $\sup$ as on the page, with the property

$$\mathit{compat}(\sup(a, b), m) \iff \mathit{compat}(a, m) \text{ and } \mathit{compat}(b, m). \tag{P}$$

For a set $G$ of modes let $\sup G$ be the supremum of its elements, and say that $\mathit{compat}(\sup \emptyset, m)$ is true. By (P) and induction on $|G|$, $\mathit{compat}(\sup G, m)$ holds exactly when $\mathit{compat}(h, m)$ holds for each $h \in G$. For S and X modes, (P) holds by the table: $\sup(a, b)$ is X unless $a = b = S$, and no mode is compatible with X.

For an item $x$ with entry $e$, write $\mathit{gr}(x)$ for the granted group, a map from transactions to modes, and $Q(x)$ for the queue. For a request $r = (T, m, c)$ in $Q(x)$, its *blockers* are the holders $U \ne T$ in $\mathit{gr}(x)$ with $\neg\mathit{compat}(\mathit{gr}(x)[U], m)$. Say $r$ *fits* when it has no blockers. For a conversion, $T$ itself is in $\mathit{gr}(x)$, and its own mode is not a blocker.

The code tests "fits" with one sup. For a new request ($T \notin \mathit{gr}(x)$), $r$ fits exactly when $\mathit{compat}(\sup \mathit{gr}(x), m)$, by (P). For a conversion, $r$ fits exactly when $\mathit{compat}(\sup(\mathit{gr}(x) \setminus T), m)$. These are the tests of lines L4, L6 and L11.

**Invariants.** Between operations:

- **(I1)** For each $x$ and each two different $T, U$ in $\mathit{gr}(x)$, $\mathit{compat}(\mathit{gr}(x)[T], \mathit{gr}(x)[U])$.
- **(I2)** For each $x$ with $Q(x)$ not empty, the head of $Q(x)$ does not fit.
- **(I3)** Each transaction has at most one request in all the queues together, and $T$ is in the map of waiting transactions with item $x$ exactly when $T$ has a request in $Q(x)$. In each queue, every conversion comes before every new request, and a conversion $(T, m, \mathit{true})$ in $Q(x)$ has $T \in \mathit{gr}(x)$.
- **(I4)** An entry with no holder and no waiter is not in the table.

The compatibility relation is symmetric for S and X and for the matrix of multiple granularity locking. For (I1), we only need that a mode is added to $\mathit{gr}(x)$ when it is compatible with each mode of the other holders, in the order (held, requested) of the matrix.

**Lemma 1 (monotone blocking).** If a request $r$ in $Q(x)$ does not fit, and a step only adds a holder to $\mathit{gr}(x)$ or raises the mode of a holder from $h$ to $\sup(h, m')$, then $r$ still does not fit.

*Proof.* Let $U$ be a blocker of $r = (T, m, c)$, with mode $h$. If the step does not change $U$, then $U$ is still a blocker. If it raises the mode of $U$ to $h' = \sup(h, m')$, then by (P), $\mathit{compat}(h', m)$ would need $\mathit{compat}(h, m)$, which is false. So $U$ is still a blocker. $\square$

**Lemma 2.** Each operation keeps (I1) to (I4).

*Proof.* All operations start in a state where the invariants hold. Look at the operations one at a time.

*REQUEST, line L3.* Nothing changes.

*REQUEST, line L4.* $T$ holds $h$, and the new mode $n = \sup(h, m)$ is compatible with the sup of the other holders, so with each of their modes. This keeps (I1). The step raises one mode, so by Lemma 1 a head that did not fit still does not fit, which keeps (I2). The queues do not change.

*REQUEST, line L5.* The conversion $(T, n, \mathit{true})$ goes after the last conversion in $Q(x)$, so conversions stay first. $T$ did not wait before the call (the code refuses a request from a waiting transaction), and $T \in \mathit{gr}(x)$, so (I3) holds. If $Q(x)$ was not empty and had a conversion or a new request at the head, the new conversion either goes behind the old head (when the old head is a conversion), or becomes the new head (when the queue has no conversion). In the second case, and when $Q(x)$ was empty, the new head is this conversion, and line L4 found that it does not fit, so (I2) holds. In the first case the head does not change. The granted groups do not change, so (I1) holds.

*REQUEST, line L6.* The queue is empty and $m$ is compatible with the group mode, so with each holder. This keeps (I1). No queue changes, and $Q(x)$ stays empty, so (I2) holds for $x$; other items do not change.

*REQUEST, line L7.* The new request goes at the end. If $Q(x)$ was empty, the new head is this request, and it does not fit, since line L6 failed and the queue was empty. Otherwise the head does not change. (I3) holds as in L5.

*RELEASE, lines L8 to L13.* Removing a holder keeps (I1). Then WAKE runs. Each pass of the loop grants the head only if it fits, so (I1) holds after each grant: the new mode is compatible with every other holder. For a conversion, the grant replaces the mode of $T$ by the larger mode, and the other holders do not change. WAKE removes the granted request from the queue and from the map of waiting transactions, so (I3) holds. The loop stops when the queue is empty or the head does not fit, which is (I2) for $x$. Line L13 removes the entry if it is empty, which is (I4). Other items do not change.

*CANCEL.* The request of $T$ leaves $Q(x)$ and the map. The relative order of the other requests does not change, so conversions stay first. Then WAKE runs, as above, and restores (I2) for $x$, also when the removed request was the head.

*RELEASE_ALL.* It is a CANCEL followed by RELEASE calls, each of which keeps the invariants. $\square$

**Theorem 1 (safety).** At every moment, two different transactions that hold locks on the same item hold compatible modes.

*Proof.* This is (I1), by Lemma 2 and induction on the number of operations, from the empty table. $\square$

**Theorem 2 (FIFO).** A new request is granted only when every request that came to $Q(x)$ before it has been granted or cancelled. A conversion is granted only when every conversion that came to $Q(x)$ before it has been granted or cancelled.

*Proof.* Line L6 grants a new request only when $Q(x)$ is empty. WAKE grants only the head of the queue. A new request enters at the end, and later requests go behind it, except conversions, which go behind the conversions already there. So everything ahead of a new request came earlier, and a new request reaches the head only when all of them have left the queue. The same holds for conversions among conversions. $\square$

**The wait-for graph.** The edges are $T \to U$ for each waiting request $r = (T, m, c)$ in $Q(x)$ and each $U$ that is a blocker of $r$ or has a request ahead of $r$ in $Q(x)$. Every $U$ with an edge into it is an active transaction: it holds a lock or waits.

**Theorem 3 (every waiter has an out edge).** If $T$ waits, then $T$ has at least one edge out of it.

*Proof.* Let $r$ be the request of $T$ in $Q(x)$. If $r$ is not the head, the head belongs to another transaction, by (I3), and gives the edge $T \to \mathrm{head}$. If $r$ is the head, by (I2) it does not fit, so it has a blocker $U \ne T$. $\square$

**Theorem 4 (soundness and completeness of the edges).** Let $T$ wait on $x$ with request $r$, and let $N(T)$ be the set of transactions $U$ with an edge $T \to U$.

1. While some $U \in N(T)$ keeps its lock on $x$ in the mode that gives the edge, or keeps its request ahead of $r$ in $Q(x)$, the request $r$ is not granted.
2. If each $U \in N(T)$ releases its lock on $x$ or leaves $Q(x)$, and no other transaction joins $\mathit{gr}(x)$ meanwhile with a mode that blocks $r$, then $r$ is granted.

*Proof.* (1) A request is granted only by WAKE, only as the head, and only if it fits. If $U$ has a request ahead of $r$, then $r$ is not the head. If $U$ is a blocker with the same mode, $r$ does not fit. A blocker that raises its mode is still a blocker by Lemma 1.

(2) After the last $U \in N(T)$ leaves, every request ahead of $r$ in the original queue is gone, and a request that joined later went behind $r$, unless it was a conversion of a holder and $r$ is a new request. Such a conversion belongs to a transaction $V$ that held a lock on $x$ already. If $V$ was a blocker of $r$, it is in $N(T)$ and has left. If not, its conversion goes ahead of $r$, and $T$ gets the new edge $T \to V$, so the hypothesis of (2) applies to the new set $N(T)$ too. So at some point $r$ is the head. It has no blocker then: every blocker at the time of the request was in $N(T)$ and left, and by hypothesis no new blocker came. The last call to RELEASE or CANCEL that removed a member of $N(T)$ ran WAKE, and WAKE grants a head that fits. If $r$ became the head at that call, it was granted then, or WAKE granted the requests ahead of it and then reached $r$. $\square$

**Theorem 5 (deadlock).** Call a nonempty set $D$ of waiting transactions *deadlocked* if no transaction in $D$ can be granted until some transaction in $D$ acts. Since a waiting transaction does nothing until it is granted or aborted, a deadlocked set waits forever unless a transaction of $D$ is aborted.

1. Each cycle of the wait-for graph is a deadlocked set.
2. If every active transaction waits, the wait-for graph has a cycle.

*Proof.* (1) Let $C$ be a cycle. Each $T \in C$ waits, because only a waiting transaction has edges out of it. Each $T \in C$ has an edge to some $U \in C$. By Theorem 4 (1), $T$ is not granted while $U$ keeps its lock or its place, and $U$ waits too, so $U$ does not release anything or leave the queue unless it is granted or aborted. So the first transaction of $C$ to be granted would need an earlier grant in $C$, which is impossible. So no transaction of $C$ is granted, unless one of them is aborted.

(2) Every edge goes to an active transaction, so if all active transactions wait, every node with an edge into it waits, and by Theorem 3 every waiting node has an edge out of it. Start at any waiting transaction and follow out edges. The walk stays among the finitely many waiting transactions, so it repeats a node, and the part between the two visits is a cycle. $\square$

Part (2) is what a scheduler uses when all its transactions wait: it builds the graph, finds a cycle with depth-first search, and aborts one transaction on it. `release_all` of the victim then calls CANCEL, which removes its request and runs WAKE, so by Lemma 2 no waiting request is left behind a head that fits.

**Theorem 6 (use with strict two-phase locking).** Let a scheduler take an S lock through REQUEST before each read and an X lock before each write, let it run an action only after the lock is granted, and let it call `release_all` only at the commit or abort of a transaction. Then the output schedule is strict, and its committed projection is conflict serializable.

*Proof.* Each transaction is two-phase, because it releases no lock before its end, and holds every lock until then. Two conflicting actions $p_i(x)$ and $q_j(x)$ need locks on $x$ in modes that are not compatible (at least one is X). By Theorem 1 these locks are not held at the same time, so if $p_i(x)$ comes first, $T_i$ released its lock before $T_j$ got its lock, which is after the end of $T_i$. So every action that follows a write of another transaction on the same item follows the end of that transaction, which is the definition of a strict schedule. The schedule is a two-phase locked schedule, so by the [two-phase locking theorem](/two-phase-locking-theorem/) its committed projection is conflict serializable. $\square$

The tests check (I1) to (I3) and Theorem 5 (2) on every state of a strict 2PL driver: all interleavings of three sets of two or three short transactions, and 55 random interleavings of four or six. They check Theorem 6 on each output with the brute force classes of the helper `dbsched`, which tries every serial order and does not use a conflict graph.
