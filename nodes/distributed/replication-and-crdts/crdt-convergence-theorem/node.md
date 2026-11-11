---
tag: TXVMWX
kind: theorem
slug: crdt-convergence-theorem
name: CRDT convergence theorem
aliases:
- Shapiro convergence theorem
- state-based convergence theorem
area: distributed/replication-and-crdts
level: advanced
summary: States in a join-semilattice with inflationary updates and join as merge, or ops whose concurrent pairs commute under causal delivery, give strong eventual consistency.
prereqs: [join-semilattice, strong-eventual-consistency, causal-broadcast]
see_also: [crdt, state-based-crdt, op-based-crdt, delta-state-crdt, g-counter, or-set, calm-theorem, happened-before]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2 (system model, Definitions 2 and 3 of eventual and strong eventual consistency, Definition 4 of a monotonic semilattice object, Theorem 1, Definitions 5 and 6, Theorem 2), Section 3 (Theorems 3 and 4, each style emulates the other), Appendices A and B (the proofs)
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA research report RR-7506, 2011
    locator: Section 2 (the same model and theorems, with the specifications in the style used later for the catalogue of CRDTs)
  - paper: doi:10.1145/3133933
    title: Victor B. F. Gomes, Martin Kleppmann, Dominic P. Mulligan and Alastair R. Beresford, Verifying strong eventual consistency in distributed systems, Proceedings of the ACM on Programming Languages 1 (OOPSLA), 2017
    locator: Sections 3 and 4 (the abstract convergence theorem for operations that commute when concurrent, mechanized in Isabelle/HOL, with an explicit network model)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, Proposition 1 (delta-CRDT convergence) and Proposition 2 (the states reachable under the causal delta-merging condition are those of the standard CRDT), numbered as in the arXiv version
---

The CRDT convergence theorem gives two simple conditions under which replicas that accept updates without any coordination still end in the same state. In the state-based form, the states form a [join-semilattice](/join-semilattice/), every update moves the state up, and replicas merge by taking the join. In the op-based form, replicas send operations by [causal broadcast](/causal-broadcast/) and any two concurrent operations commute. Shapiro, Preguiça, Baquero and Zawirski proved both in 2011, and the two conditions are the definitions of a [state-based CRDT](/state-based-crdt/) and an [op-based CRDT](/op-based-crdt/).

## Statement

**Model (Shapiro et al. 2011, Section 2).** A fixed set of replicas communicate over an asynchronous network that may partition and recover. Replicas do not behave in a Byzantine way. A replica may crash, and may recover with its memory intact. Each update has a unique identity. The *causal history* $c_i$ of replica $i$ is the set of updates it has received: an update at $i$ adds itself, a merge of a state from $j$ adds the history of that state, and the delivery of an operation adds that operation. Two states are *equivalent*, $s \equiv s'$, if every query returns the same result on both.

**Strong eventual consistency (Definitions 2 and 3).** A replicated object is *strongly eventually consistent* ([SEC](/strong-eventual-consistency/)) if it has:

- *eventual delivery*: an update delivered at some correct replica is in the end delivered at every correct replica;
- *strong convergence*: for all replicas $i$ and $j$, if $c_i = c_j$ then $s_i \equiv s_j$;
- *termination*: every method execution terminates.

**Monotonic semilattice object (Definition 4).** A state-based object is a *monotonic semilattice object* if (i) its set of states $S$ with the order $\le$ is a join-semilattice, (ii) merging a state $s'$ into $s$ gives the least upper bound $s \sqcup s'$, and (iii) every update is inflationary: $s \le u(s)$.

**Theorem 1 (CvRDT).** Assuming eventual delivery and termination, every monotonic semilattice object is SEC.

**Commutativity (Definition 6).** Two updates $f$ and $g$ of an op-based object *commute* if, at every reachable state $s$ at which both are enabled, each stays enabled after the other and $s \bullet f \bullet g \equiv s \bullet g \bullet f$.

**Theorem 2 (CmRDT).** Assuming causal delivery of updates and termination, every op-based object whose concurrent updates commute, and whose delivery preconditions are satisfied by causal delivery, is SEC.

Strong convergence is a safety property: it holds at every moment, not only in the limit. Eventual delivery is the liveness part, and the theorem gets it from the network.

## In plain words

Several copies of the same data change on their own and swap news from time to time. The theorem says when the copies always agree once they have heard the same news.

There are two recipes. In the first, copies send their whole state. If merging is like taking the larger of two numbers, so that order and repeats do not matter, and every change only moves the state forward, then any two copies that have heard the same changes are equal. Lost, repeated and late messages do no harm.

In the second, copies send each change once. If the network delivers every change exactly once, never before a change it depends on, and changes made at the same time give the same result in either order, then copies that have applied the same changes are equal.

## Proof

The full proof is in the proof file. Here is its plan.

*Theorem 1.* For an update $e$, let $v(e)$ be the state of its source replica right after $e$. The key invariant is
$$s_i = s^0 \sqcup \bigsqcup_{e \in c_i} v(e),$$
which holds for every replica at every moment. It holds at the start. An update $e$ turns $s$ into $v(e) \ge s$, and $s \sqcup v(e) = v(e)$. A merge joins two states of this form, and by associativity, commutativity and idempotence the result is the join over the union of the two histories. So the state of a replica depends only on its history, which is strong convergence. Eventual delivery follows because each correct replica sends its state to each other one infinitely often, and the network delivers some of these messages.

*Theorem 2.* Causal delivery makes every replica apply its history in an order that extends the happened-before order. Any two such orders of the same set are connected by swaps of adjacent concurrent operations: take the first place where they differ, and the element just before it in one order cannot be causally related to it. The prefix before a swap is causally closed, so its state is reachable, both operations are enabled there, and they commute. So every order gives the same state.

The implementation runs both styles in a seeded simulator. The state-based run loses, duplicates and reorders states and checks the invariant and strong convergence after every step for a g-counter and a g-set, and finds violations for a register that keeps the last state it receives. The op-based run checks a counter and an observed-remove set over a vector-clock causal broadcast with duplicates and reordering.

## Consequences

- **CRDTs are correct by construction.** To show that a new state-based type converges, it is enough to give a join-semilattice of states and show that updates are inflationary; for an op-based type, it is enough to check that concurrent operations commute. This is how the [g-counter](/g-counter/), [PN-counter](/pn-counter/), [g-set](/g-set/), [two-phase set](/two-phase-set/), [OR-set](/or-set/), [LWW register](/lww-register/) and [MV-register](/mv-register/) are proved.
- **The state-based form needs almost nothing from the network.** The proof uses only that some message from each correct replica reaches each other correct replica after any time. Messages may be lost, duplicated and reordered, and any gossip or [anti-entropy](/anti-entropy/) protocol gives eventual delivery.
- **The op-based form moves the burden into the network.** It needs exactly-once causal delivery. Duplicates break counters, and an operation delivered before one it depends on can break a set.
- **The two forms emulate each other (Theorems 3 and 4).** A state-based object can carry the set of operations it has seen as its state, and an op-based object can send its full state as an operation whose effect is a merge. So the two forms define the same class of objects, though at very different cost.
- **Delta-state CRDTs keep the guarantee.** A delta-state CRDT ships joins of small deltas instead of full states. Since a delta is an element of the same lattice and is joined in, the same invariant holds, and with delta-intervals sent in causal order the states equal those of the full-state CRDT; see [delta-state CRDT](/delta-state-crdt/).
- **SEC escapes CAP.** SEC needs no coordination and no waiting, so a CRDT stays available under partitions; it gives up linearizability, not convergence. The [CALM theorem](/calm-theorem/) explains why: monotone programs need no coordination.

## Tightness

Each hypothesis is needed. The implementation runs each counterexample.

- **Idempotence.** Merging by addition is commutative and associative but not idempotent. A duplicated message counts twice, and two replicas with the same history can differ.
- **Commutativity of merge.** A merge that keeps the last state received is associative and idempotent but not commutative. Two replicas that exchange states at the same time swap them and end different, with the same history.
- **Inflationary updates.** A set with a remove that deletes the element and a merge by union is a semilattice with a non-inflationary update. A replica that removes $x$ and then merges an old copy with $x$ gets $x$ back, while a replica that merged first and removed later does not.
- **Causal delivery.** In an op-based observed-remove set, a remove applied before the add it observed removes nothing, and the add then stays at that replica only.
- **Commutativity of concurrent operations.** Two concurrent assignments to a plain register, applied in different orders at two replicas, leave different values.
- **Sufficient, not necessary.** The conditions are about the given presentation of the object. A type can be SEC under some other presentation, and a type whose operations commute in more cases can converge under a delivery guarantee weaker than causal delivery. Gomes et al. separate the two parts: an abstract theorem about any set of operations whose concurrent pairs commute, and a network model that gives the delivery order.

## History

Optimistic replication with commutative operations goes back to the Bayou and Lotus systems of the 1990s and to the WOOT and Treedoc structures for shared text of the mid 2000s. Baquero and Moura described replicated types with a merge in a semilattice in 1997. Shapiro, Preguiça, Baquero and Zawirski named CRDTs and gave the definitions of SEC, the two convergence theorems and the emulation results in 2011, with a long catalogue of types in an INRIA report of the same year. Burckhardt and others gave a more general framework of replicated data types in 2014, Almeida, Shoker and Baquero extended the theory to delta-state CRDTs in 2015 and 2018, and Gomes, Kleppmann, Mulligan and Beresford mechanized the op-based theorem in Isabelle/HOL in 2017.

## References
