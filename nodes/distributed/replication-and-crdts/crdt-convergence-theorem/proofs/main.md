---
title: Monotonic semilattice objects and commutative op-based objects are strongly eventually consistent
proves: [statement]
status: full
---

This is a full proof of the two convergence theorems of Shapiro, Preguiça, Baquero and Zawirski (2011). The structure follows their Appendices A and B, with the key invariant of the state-based case made explicit.

## Setting

There are $n$ replicas $p_1, \ldots, p_n$ in an asynchronous system. A replica may crash and stay crashed, or recover with its state intact; a replica that does not crash for ever is *correct*. There are no Byzantine faults. Each replica runs a sequence of *method executions*, one at a time, and each method execution terminates.

Each update is a unique event. For a replica $i$, $c_i$ is its *causal history*, defined below for each style; an update is *delivered* at $i$ when it is in $c_i$. States are compared by *equivalence* $s \equiv s'$: all queries return the same results on $s$ and on $s'$.

**Strong eventual consistency (SEC).** An object is SEC if it has:

- *eventual delivery*: an update delivered at some correct replica is in the end delivered at every correct replica;
- *strong convergence*: for all $i, j$, at all times, $c_i = c_j$ implies $s_i \equiv s_j$;
- *termination*: every method execution terminates.

Eventual delivery and termination are liveness properties, strong convergence is a safety property.

## Part 1: state-based objects

**Object.** A state-based object is $(S, \le, s^0, q, u, m)$: a set of states with a partial order, an initial state, queries, updates and a merge. A replica sends its state from time to time, and the receiver runs $m$ on it. The network may lose, duplicate and reorder these messages, and it connects every pair of replicas; every correct replica sends its state to every other replica infinitely often, and a message sent infinitely often over such a channel is received infinitely often.

**Causal history (state-based).** Initially $c_i = \varnothing$. A query does not change $c_i$. An update $e$ at $i$ sets $c_i \leftarrow c_i \cup \{e\}$. A merge at $i$ of a state that $j$ sent when its history was $c$ sets $c_i \leftarrow c_i \cup c$. A message carries the state and, for the analysis only, the history of its sender at the time of sending.

**Monotonic semilattice object.** (i) $(S, \le)$ is a join-semilattice with join $\sqcup$; (ii) a merge computes the join, $s \bullet m(s') = s \sqcup s'$; (iii) each update is inflationary, $s \le s \bullet u$. Assume also that states that are equal are equivalent, which holds trivially, and that $\le$-equivalent states ($x \le y$ and $y \le x$) are equivalent, which holds because $\le$ is antisymmetric.

**Theorem 1 (CvRDT).** Assuming eventual delivery and termination, every monotonic semilattice object is SEC.

**Definition.** For an update $e$, let $v(e)$ be the state of its source replica right after $e$.

**Lemma 1.1 (state as a function of history).** At every time and for every replica $i$,
$$s_i = s^0 \sqcup \bigsqcup_{e \in c_i} v(e).$$
The join of a finite set is well defined by the ACI laws, whatever the order of the terms.

*Proof.* By induction on the method executions in the run, in real-time order. Write $J(c) = s^0 \sqcup \bigsqcup_{e \in c} v(e)$.

- *Start.* $s_i = s^0$ and $c_i = \varnothing$, and $J(\varnothing) = s^0$.
- *Query at $i$.* It changes neither $s_i$ nor $c_i$.
- *Update $e$ at $i$.* Let $s$ be the state before and $s' = s \bullet u$ the state after, so $v(e) = s'$. By induction $s = J(c_i)$. The new history is $c_i \cup \{e\}$, and $e \notin c_i$ because updates are unique. Then $J(c_i \cup \{e\}) = J(c_i) \sqcup v(e) = s \sqcup s' = s'$, where the last step uses $s \le s'$ (property iii) and the fact that $x \le y$ implies $x \sqcup y = y$.
- *Merge at $i$ of a message $(s_j^*, c_j^*)$.* The message was sent by $j$ at an earlier time, so by induction $s_j^* = J(c_j^*)$. The new state is $s_i \sqcup s_j^* = J(c_i) \sqcup J(c_j^*)$. By associativity and commutativity this is the join of $s^0$ twice and of $v(e)$ for every $e$ in $c_i$ or $c_j^*$, with the $e$ in both counted twice. By idempotence the repeats can be dropped, and the result is $J(c_i \cup c_j^*)$, which is the state that the new history gives.

Messages that are lost change nothing, and a duplicate is merged like any other message, so the induction covers every run. $\square$

*Proof of Theorem 1.* **Strong convergence.** By Lemma 1.1, $s_i = J(c_i)$ and $s_j = J(c_j)$ at every time. If $c_i = c_j$ then $s_i = s_j$, so in particular $s_i \equiv s_j$.

**Eventual delivery.** Let $e \in c_i$ at time $t$ with $i$ correct, and let $j$ be correct. Replica $i$ sends its state to $j$ infinitely often after $t$, and each such message carries a history that contains $c_i$ at time $t$, because histories only grow. The channel delivers one of them, and the merge puts $e$ into $c_j$.

**Termination** is assumed for each method. $\square$

**Remark (no delivery order is needed).** The proof uses no property of the network except that some message from $i$ to $j$ sent after any given time arrives. Loss, duplication and reordering all fit in the induction, because a merge of an old state $s_j^*$ is a merge of a smaller history, which the join absorbs.

## Part 2: op-based objects

**Object.** An op-based object is $(S, s^0, q, t, u, P)$. An operation runs a side-effect-free *prepare* $t$ at its source, which returns an *effect* $u$; the source applies $u$ at once and broadcasts it, and every other replica applies $u$ when it is delivered. $P$ is a delivery precondition: $u$ may be applied at a state $s$ only if $P(s, u)$ holds.

**Causal history (op-based).** Initially $c_i = \varnothing$. Queries and prepares do not change it. Applying an effect $u$ at $i$ sets $c_i \leftarrow c_i \cup \{u\}$. An update $u$ *happened before* $u'$, written $u \to u'$, if $u$ was in the history of the source of $u'$ when $u'$ was prepared. Updates are *concurrent*, $u \parallel u'$, if neither happened before the other. The relation $\to$ is a strict partial order on updates.

**Network.** Effects are sent by *reliable causal broadcast*: every effect is delivered exactly once at every correct replica, and if $u \to u'$ then every replica applies $u$ before $u'$.

**Commutativity.** Two updates $u$ and $u'$ *commute* if, for every reachable state $s$ at which both are enabled, $u$ is enabled at $s \bullet u'$, $u'$ is enabled at $s \bullet u$, and $s \bullet u \bullet u' = s \bullet u' \bullet u$. Here we use equality of states; if one uses only query equivalence, one must also assume that applying the same effect to equivalent states gives equivalent states.

**Theorem 2 (CmRDT).** Assuming causal delivery of updates and termination, every op-based object in which all concurrent updates commute, and whose delivery precondition is satisfied by causal delivery, is SEC.

**Lemma 2.1 (what each replica applies).** At every time, the set $c_i$ is *causally closed*: if $u' \in c_i$ and $u \to u'$, then $u \in c_i$. The order in which $i$ applied the elements of $c_i$ is a *linear extension* of $\to$ restricted to $c_i$: a total order that puts $u$ before $u'$ whenever $u \to u'$.

*Proof.* Causal delivery applies $u$ before $u'$ at every replica when $u \to u'$, which gives both claims for effects received from others. For an effect $u'$ prepared at $i$, every $u \to u'$ is in $c_i$ by the definition of $\to$, and $u'$ is applied right after its prepare, after all of them. $\square$

**Lemma 2.2 (adjacent swaps).** Let $\sigma$ and $\tau$ be two linear extensions of a finite partial order $(C, \to)$. If $\sigma \ne \tau$, then some two elements $a, b$ that are adjacent in $\sigma$, with $a$ just before $b$, appear in $\tau$ with $b$ before $a$, and $a \parallel b$.

*Proof.* Let $b$ be the first element of $\tau$ whose position in $\sigma$ differs from its position in $\tau$; the elements before it in $\tau$ are the same as in $\sigma$ and in the same places. So in $\sigma$, $b$ comes later, at position $k$, and the element just before $b$ in $\sigma$, call it $a$, comes after $b$ in $\tau$. If $a \to b$ then $\tau$ would put $a$ before $b$, and if $b \to a$ then $\sigma$ would put $b$ before $a$. Neither holds, so $a \parallel b$. $\square$

**Lemma 2.3 (any two linear extensions give the same state).** Let $C$ be a causally closed set of updates and $\sigma, \tau$ two linear extensions of $\to$ on $C$, each of which is a valid application order (every effect is enabled when it is applied). Then $s^0 \bullet \sigma = s^0 \bullet \tau$.

*Proof.* By induction on the number of *inversions*, the pairs of elements in opposite order in $\sigma$ and $\tau$. With 0 inversions, $\sigma = \tau$. Otherwise take $a, b$ as in Lemma 2.2, and write $\sigma = \rho \, a \, b \, \pi$. Let $s = s^0 \bullet \rho$. The prefix $\rho$ is causally closed, because $\sigma$ is a linear extension of a causally closed set, so $s$ is a state that a replica reaches by applying $\rho$ in this order, and $s$ is reachable. Both $a$ and $b$ are enabled at $s$: $a$ because $\sigma$ applies it there, and $b$ because its precondition is satisfied by causal delivery and all its causal predecessors are in $\rho$ ($a \parallel b$). They are concurrent, so they commute: $s \bullet a \bullet b = s \bullet b \bullet a$, and both orders are valid. Let $\sigma' = \rho \, b \, a \, \pi$. Then $s^0 \bullet \sigma' = s^0 \bullet \sigma$, $\sigma'$ is still a linear extension, and it has one inversion less with $\tau$. By induction $s^0 \bullet \sigma' = s^0 \bullet \tau$. $\square$

*Proof of Theorem 2.* **Strong convergence.** Let $c_i = c_j = C$. By Lemma 2.1, replica $i$ reached $s_i = s^0 \bullet \sigma$ and replica $j$ reached $s_j = s^0 \bullet \tau$ for two linear extensions $\sigma, \tau$ of $\to$ on $C$, both valid application orders. By Lemma 2.3, $s_i = s_j$.

**Eventual delivery.** Reliable causal broadcast delivers every effect at every correct replica. An effect is enabled when delivered, because the precondition is satisfied by causal delivery, so it is applied.

**Termination** is assumed for each method. $\square$

## What each assumption does

- *Idempotence of the join* absorbs duplicate messages and states that were merged before. Without it, as with addition as a merge, a duplicate changes the state, and Lemma 1.1 fails.
- *Commutativity and associativity of the join* make the state independent of the order of merges. A merge that keeps the last state received fails here: two replicas that swap their states have the same history and different states.
- *Inflationary updates* make an update's effect survive a later merge with an older state. A set with an update "remove $x$" that deletes $x$, and a merge by union, fails: a replica that removed $x$ and then merges an older state that contains $x$ gets $x$ back, while a replica with the same history that merged first and removed later has no $x$.
- *Causal delivery* makes each replica apply a linear extension of $\to$. Without it, an effect can be applied before an effect it depends on; for an observed-remove set, a remove applied before the add it observed removes nothing, and the add then wins at that replica only.
- *Commutativity of concurrent effects* is used once, in the swap of Lemma 2.3. Two assignments of different values to a register, applied in different orders at two replicas, leave different values.

The theorems give sufficient conditions. They do not say that every SEC object has a monotonic semilattice or commuting concurrent effects in the given presentation. $\blacksquare$
