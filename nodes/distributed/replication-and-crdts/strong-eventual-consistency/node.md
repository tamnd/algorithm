---
tag: WNCV3P
kind: definition
slug: strong-eventual-consistency
name: Strong eventual consistency
aliases:
- SEC
area: distributed/replication-and-crdts
level: advanced
summary: Eventual delivery plus strong convergence; replicas that have received the same set of updates are in equivalent states at once, with no rollback or consensus.
prereqs: [eventual-consistency, happened-before]
see_also: [crdt, crdt-convergence-theorem, state-based-crdt, op-based-crdt, causal-consistency, consistency-models, cap-theorem, calm-theorem]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2.1 (Definition 1, causal history), Section 2.2 (Definition 2, eventual consistency, and Definition 3, strong eventual consistency), Theorems 1 and 2
  - paper: doi:10.1145/3133933
    title: Victor B. F. Gomes, Martin Kleppmann, Dominic P. Mulligan and Alastair R. Beresford, Verifying strong eventual consistency in distributed systems, Proceedings of the ACM on Programming Languages 1 (OOPSLA), 2017
    locator: the definition of strong eventual consistency used in the paper and its formalization in Isabelle/HOL, with the abstract convergence theorem and the network model
  - paper: doi:10.1145/2578855.2535848
    title: Sebastian Burckhardt, Alexey Gotsman, Hongseok Yang and Marek Zawirski, Replicated data types, specification, verification, optimality, POPL 2014 (ACM SIGPLAN Notices 49(1))
    locator: pages 271 to 284, Section 7 (the axioms EVENTUAL and THINAIR for basic eventual consistency, the comparison with quiescent consistency, and the per-object causal axioms)
  - paper: doi:10.1145/2926965
    title: Paolo Viotti and Marko Vukolić, Consistency in non-transactional distributed storage systems, ACM Computing Surveys 49(1), 2016
    locator: Article 19, the section on eventual consistency and its variants (strong eventual consistency and strong convergence)
---

Strong eventual consistency (SEC) is a guarantee for replicated data that adds a safety property to [eventual consistency](/eventual-consistency/). Eventual consistency only promises that replicas agree some time after updates stop; SEC promises that any two replicas that have received the same set of updates are, at that moment, in states that answer every query in the same way. Shapiro, Preguiça, Baquero and Zawirski defined it in 2011 as the guarantee of [CRDTs](/crdt/). It needs no consensus and no rollback, so every replica can accept updates at any time, even during a partition.

## Definition

**Setting.** A replicated object has replicas $p_1, \ldots, p_n$ in an asynchronous network. Each replica has a state $s_i$ and runs queries and updates locally. Each update is a unique event. The *causal history* $c_i$ of replica $i$ is the set of updates that it has received: its own updates and the updates that reached it through messages. Two states are *equivalent*, $s \equiv s'$, if every query returns the same result on both. A replica is *correct* if it does not crash for ever.

**Eventual consistency (Shapiro et al., Definition 2).** An object is *eventually consistent* (EC) if it has:

- **Eventual delivery.** An update delivered at some correct replica is in the end delivered at every correct replica: for all correct $i, j$, if $f \in c_i$ then, eventually, $f \in c_j$.
- **Convergence.** Correct replicas that have delivered the same updates *eventually* reach equivalent states: if $c_i = c_j$ then, eventually, $s_i \equiv s_j$.
- **Termination.** Every method execution terminates.

**Strong eventual consistency (Definition 3).** An object is *strongly eventually consistent* if it is eventually consistent and has:

- **Strong convergence.** Correct replicas that have delivered the same updates have equivalent states: for all correct $i, j$, at all times, if $c_i = c_j$ then $s_i \equiv s_j$.

Strong convergence replaces "eventually" by "now". It is a safety property: a violation is visible in a finite prefix of an execution. Eventual delivery and termination are liveness properties.

**Remarks.**

- SEC says nothing about *which* state the replicas reach. That is the job of the type's specification, for example "a counter returns the number of increments it has seen". A type that always returns 0 is SEC and useless.
- SEC does not mention order. Two replicas may have received the same updates in different orders, and must still agree.
- SEC needs no bound on time. It holds in an asynchronous system with any number of crashed replicas, and under partitions: each side converges among itself.
- Shapiro et al. motivate the strong form by systems that apply an update at once, later find a conflict and roll back. Rollback wastes work and, in general, needs consensus so that all replicas resolve the conflict in the same way. SEC rules it out.

## Examples and non-examples

- **Example: a state-based g-counter.** Each replica keeps a vector of counts, increments its own entry and merges by pointwise max. Its state is always the join of the states produced by the updates in its history, so equal histories give equal states. See [g-counter](/g-counter/).
- **Example: an op-based counter with exactly-once delivery.** Increments commute, so any two replicas that applied the same increments have the same sum, whatever the order.
- **Example: any CRDT.** Both convergence theorems of the [CRDT convergence theorem](/crdt-convergence-theorem/) give SEC: semilattice states with join as merge, or commuting concurrent effects with causal delivery.
- **Example: a last-writer-wins register with unique timestamps.** Each replica keeps the write with the largest timestamp. Equal sets of writes give the same largest timestamp.
- **Non-example: a register that keeps the last value received.** Two replicas that write and swap their values at the same time have the same history and different values. It does not even reach convergence later, unless new writes arrive.
- **Non-example: eventual consistency with rollback.** Bayou applies writes tentatively and later reorders them according to a primary's commit order, undoing and redoing writes. Two replicas with the same set of writes but different tentative orders differ until the commit order reaches them. This is EC but not SEC.
- **Non-example: a counter whose merge adds.** A duplicated message is counted twice, so two replicas with the same history differ for ever.
- **Non-example: a strongly consistent store under partitions.** A [linearizable](/linearizability/) register built on a primary or on consensus converges, but during a partition some of its operations wait for ever, so it fails the termination condition. By the [CAP theorem](/cap-theorem/), this is unavoidable for a linearizable register.

## Related definitions

- **[Eventual consistency](/eventual-consistency/).** SEC is EC plus strong convergence. Every SEC object is EC; the converse fails, as the Bayou example shows.
- **Quiescent consistency of state.** Vogels's eventual consistency asks only that, if no new updates are made, reads eventually return the last updated value. Neither EC nor SEC needs updates to stop.
- **[Causal consistency](/causal-consistency/).** Causal consistency constrains the order in which a replica may see updates. SEC constrains the state reached once it has seen them. A state-based CRDT gives both for one object; causal+ consistency is causal consistency with convergent conflict handling, which is close to causal delivery combined with SEC.
- **[Session guarantees](/session-guarantees/).** These constrain what one client sees across replicas; they can be added on top of an SEC store.
- **Convergent replicated data types.** The [state-based CRDT](/state-based-crdt/) is the standard way to get SEC with weak network assumptions; the [op-based CRDT](/op-based-crdt/) gets it with causal delivery.
- **[CALM theorem](/calm-theorem/).** Monotone programs have consistent, coordination-free implementations; SEC objects built from join-semilattices are an example of such monotone state.

## References
