---
tag: J2QJTR
kind: definition
slug: causal-consistency
name: Causal consistency
aliases:
- causal consistency model
- causal+ consistency
area: distributed/replication-and-crdts
level: advanced
summary: Each process sees all writes in an order that respects potential causality; concurrent writes may appear in different orders. Causal+ adds convergence.
prereqs: [consistency-models, happened-before]
see_also: [eventual-consistency, strong-eventual-consistency, session-guarantees, causal-broadcast, vector-clocks, crdt, cap-theorem, linearizability]
sources:
  - paper: doi:10.1007/BF01784241
    title: Mustaque Ahamad, Gil Neiger, James E. Burns, Prince Kohli and Phillip W. Hutto, Causal memory, definitions, implementation, and programming, Distributed Computing 9(1), 1995
    locator: pages 37 to 49 (the writes-into and causality orders, the definition of causal memory by one serialization per process, the comparison with sequential consistency and PRAM, and an implementation with vector timestamps)
  - paper: doi:10.1145/2043556.2043593
    title: Wyatt Lloyd, Michael J. Freedman, Michael Kaminsky and David G. Andersen, Don't settle for eventual, scalable causal consistency for wide-area storage with COPS, SOSP 2011
    locator: Section 2 (the ALPS properties, the definition of causal+ consistency as causal consistency with convergent conflict handling, and the comparison with other models), Section 3 (dependency tracking and nearest dependencies)
  - paper: "Prince Mahajan, Lorenzo Alvisi and Mike Dahlin, Consistency, availability, and convergence, University of Texas at Austin technical report UTCS TR-11-22, 2011"
    title: Prince Mahajan, Lorenzo Alvisi and Mike Dahlin, Consistency, availability, and convergence, 2011
    locator: the definition of real-time causal consistency and Theorem 3.1 (no model stronger than real-time causal is always available and one-way convergent)
  - paper: "Matthieu Perrin, Achour Mostéfaoui and Claude Jard, Causal consistency, beyond memory, ACM PPoPP 2016"
    title: Matthieu Perrin, Achour Mostéfaoui and Claude Jard, Causal consistency, beyond memory, PPoPP 2016
    locator: the definitions of weak causal consistency, causal convergence and causal consistency for any abstract data type, and their relations
  - paper: doi:10.1145/2926965
    title: Paolo Viotti and Marko Vukolić, Consistency in non-transactional distributed storage systems, ACM Computing Surveys 49(1), 2016
    locator: Article 19, the section on causal models (causal, causal+, real-time causal and their relation to PRAM and the session guarantees)
---

Causal consistency is a consistency model for shared or replicated data in which every process sees writes in an order that agrees with potential causality. If a process wrote $a$ and then $b$, or read $a$ before it wrote $b$, then no process may see $b$ and then miss $a$. Writes that are not related in this way are *concurrent*, and different processes may see them in different orders. Ahamad, Neiger, Burns, Kohli and Hutto defined it as *causal memory* in 1995. Causal+ consistency, from the COPS system of Lloyd et al. (2011), adds that replicas handle concurrent writes in the same way, so that they converge.

## Definition

**Histories.** A *history* $H$ is a set of operations by processes $p_1, \ldots, p_n$ on registers. Each operation is a write $w(x)v$ or a read $r(x)v$, and each process's operations are totally ordered by *program order* $\to_{po}$. As usual, assume that each value is written at most once, and that every register starts at 0.

**Causality order.** The *writes-into* relation $\to_{wi}$ links a write $w(x)v$ to every read $r(x)v$ of the same value. The *causality order* $\leadsto$ of $H$ is the transitive closure of $\to_{po} \cup \to_{wi}$. Two writes are *concurrent* if neither $w \leadsto w'$ nor $w' \leadsto w$. This is the read/write form of [happened-before](/happened-before/).

**Serializations.** A *serialization* of a set of operations is a total order on them. It is *legal* if each read $r(x)v$ in it returns the value of the last write to $x$ before it, or $v = 0$ if there is none.

**Causal consistency (Ahamad et al. 1995).** For each process $p$, let $H_{p+w}$ be the operations of $p$ together with all writes in $H$. The history $H$ is *causally consistent* if, for each process $p$, there is a legal serialization $S_p$ of $H_{p+w}$ that respects $\leadsto$: if $o \leadsto o'$ and both are in $H_{p+w}$, then $o$ is before $o'$ in $S_p$.

So each process has its own view of the writes. All views agree on the order of causally related writes, and may disagree on the order of concurrent ones.

**Convergent conflict handling (Lloyd et al. 2011).** Two writes *conflict* if they are to the same key and concurrent. A store has convergent conflict handling if all replicas handle all conflicting writes with the same handler function $h$, and $h$ is associative and commutative, so that replicas that have received the same conflicting writes in different orders reach the same value. Last-writer-wins by timestamp and a [CRDT](/crdt/) merge are examples.

**Causal+ consistency.** A store is *causal+ consistent* if it is causally consistent and has convergent conflict handling.

**Remarks.**

- Causal consistency is a safety property. On its own, it allows a replica never to learn of a remote write, because a view that leaves remote writes out until the end is legal. Practical definitions add [eventual](/eventual-consistency/) delivery.
- Causal consistency also allows two processes to settle on different final values for a register for ever. Causal+ forbids this.
- The definition is per process. It contains [read your writes](/read-your-writes/), [monotonic reads](/monotonic-reads/), monotonic writes and writes follow reads, applied to each process as a client.

## Examples and non-examples

Write the operations of each process from left to right in program order.

- **Example: concurrent writes seen in different orders.** $p_1$: $w(x)1$; $p_2$: $w(x)2$; $p_3$: $r(x)1$, $r(x)2$; $p_4$: $r(x)2$, $r(x)1$. The two writes are concurrent. The views $w(x)1, r(x)1, w(x)2, r(x)2$ for $p_3$ and $w(x)2, r(x)2, w(x)1, r(x)1$ for $p_4$ are legal and respect $\leadsto$. The history is causally consistent but not sequentially consistent, because one total order would put $w(x)1$ both before and after $w(x)2$.
- **Example: the store buffer.** $p_1$: $w(x)1$, $r(y)0$; $p_2$: $w(y)1$, $r(x)0$. Each process may see its own write first and the other write later. This is causal and not sequential.
- **Non-example: an effect seen before its cause.** $p_1$: $w(x)1$; $p_2$: $r(x)1$, $w(y)1$; $p_3$: $r(y)1$, $r(x)0$. Here $w(x)1 \to_{wi} r(x)1 \to_{po} w(y)1$, so $w(x)1 \leadsto w(y)1$. Process $p_3$ reads $y = 1$, so its view puts $w(y)1$, and hence $w(x)1$, before $r(y)1$; then $r(x)0$ is not legal. The history is PRAM consistent, since PRAM orders only each writer's own writes, but not causal.
- **Non-example, in application terms.** Alice removes Bob from the list of people who can see her photos, and then uploads a photo. A store that is not causal may show Bob the new photo with the old list. Causal consistency forbids it: the upload depends on the change of list.
- **Causal but not causal+.** In the first example, if no more writes happen, $p_3$ keeps reading 2 and $p_4$ keeps reading 1 for ever. That is causally consistent. Under causal+, all replicas apply the same handler to the two conflicting writes, for example keep the write with the larger timestamp, so both end with the same value.
- **Example: an op-based CRDT on causal broadcast.** Each replica applies each update once, in an order that extends happened-before. Each replica's order is a legal view, so the object is causally consistent; because concurrent effects commute, replicas also converge, which gives causal+. See [op-based CRDT](/op-based-crdt/) and [causal broadcast](/causal-broadcast/).

## Related definitions

- **[Sequential consistency](/consistency-models/) and [linearizability](/linearizability/).** Both are stronger: they ask for one order that all processes agree on. Neither can be implemented by a store that stays available during a partition, by the [CAP theorem](/cap-theorem/).
- **PRAM, or FIFO, consistency.** Weaker: it orders only the writes of each single process, so it allows the non-example above.
- **Real-time causal consistency.** Causal consistency plus the condition that a write that completes before another write starts is ordered first. Mahajan, Alvisi and Dahlin (2011) showed that no consistency model stronger than real-time causal consistency can be implemented by a store that is always available and one-way convergent. In this sense, causal consistency is close to the strongest model that an available store can give.
- **[Session guarantees](/session-guarantees/).** The four guarantees of Terry et al. (1994) constrain what one client session sees. Causal consistency implies all four, and also orders writes across clients, for example when one client reads a value that another client wrote.
- **[Eventual consistency](/eventual-consistency/) and [strong eventual consistency](/strong-eventual-consistency/).** These are about convergence, not order. Causal+ is close to causal delivery combined with strong eventual consistency.
- **Causal consistency for other data types.** Perrin, Mostéfaoui and Jard (2016) extended the definition from memory to any abstract data type, and separated *weak causal consistency*, *causal convergence* and *causal consistency*.
- **Implementation tools.** Replicas track dependencies with [vector clocks](/vector-clocks/) or explicit lists of dependencies, and delay a write until its dependencies are visible. COPS tracks only the *nearest* dependencies of each write, which keeps metadata small.

## References
