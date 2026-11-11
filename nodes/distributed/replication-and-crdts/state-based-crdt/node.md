---
tag: D3P23E
kind: concept
slug: state-based-crdt
name: State-based CRDT (CvRDT)
aliases:
- CvRDT
- convergent replicated data type
area: distributed/replication-and-crdts
level: core
summary: CRDT whose replicas ship full states and merge them with a join that is commutative, associative and idempotent, so loss, duplicates and reordering do no harm.
prereqs: [crdt, join-semilattice]
see_also: [op-based-crdt, delta-state-crdt, crdt-convergence-theorem, g-counter, or-set, anti-entropy, tombstone, calm-theorem]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2.3 (state-based objects, Definition 4 of a monotonic semilattice object, Theorem 1), Section 4 (integer vectors and counters, sets)
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA research report RR-7506, 2011
    locator: Section 2 (the state-based specification style with payload, query, update, compare and merge), Section 3 (state-based counters, registers and sets)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the lattice compositions (products, lexicographic products and maps) and the optimized observed-remove set with dots and causal contexts
  - paper: "Neil Conway, William R. Marczak, Peter Alvaro, Joseph M. Hellerstein and David Maier, Logic and lattices for distributed programming, ACM SoCC 2012"
    title: Neil Conway, William R. Marczak, Peter Alvaro, Joseph M. Hellerstein and David Maier, Logic and lattices for distributed programming, SoCC 2012
    locator: the Bloom^L language, in which user-defined lattices with a merge function and monotone functions build state-based replicated programs
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Detecting concurrent writes (merging concurrently written values, version vectors)
---

A state-based CRDT, or CvRDT, is a replicated data type in which each replica updates its own copy of the state and, from time to time, sends the whole state to other replicas, which merge it into theirs. The states form a [join-semilattice](/join-semilattice/), every update moves the state up in its order, and merge is the join. Because the join is commutative, associative and idempotent, a state can be merged in any order and any number of times, so the network may lose, duplicate and reorder messages. Shapiro, Preguiça, Baquero and Zawirski proved in 2011 that such objects are [strongly eventually consistent](/strong-eventual-consistency/): replicas that have seen the same updates are in the same state.

## In plain words

Several copies of some data live on different machines. Each copy accepts changes on its own, with no locks and no waiting. Now and then, a copy sends all its data to another copy, which combines the two.

The combine step is chosen so that it never matters in what order copies are combined, or how many times. Combining a copy with itself gives the same copy. A change can only add information, never take it away, so an old copy that arrives late cannot undo a newer change.

Then any two copies that have heard about the same changes hold the same data, and gossip in any pattern brings all copies into agreement. The price is that each message carries the whole data, and the data often keeps extra records, for example of deleted items.

## The idea

**Specification.** A state-based object has a payload type $S$ with an initial state $s^0$, query methods, update methods, and two special methods: *compare*, a partial order $\le$ on $S$, and *merge*. An update runs at one replica only and changes only that replica's state. Replicas exchange states by any [anti-entropy](/anti-entropy/) or gossip protocol: a replica sends its current state, and the receiver sets $s \leftarrow \text{merge}(s, s')$.

**Conditions (a monotonic semilattice object).**

1. $(S, \le)$ is a join-semilattice: every two states $s, s'$ have a least upper bound $s \sqcup s'$.
2. merge$(s, s') = s \sqcup s'$.
3. Every update is *inflationary*: $s \le u(s)$.

The [CRDT convergence theorem](/crdt-convergence-theorem/) (Theorem 1) shows that these conditions give strong eventual consistency. The heart of the proof is that the state of a replica is always the join of the states that its updates produced, so the state is a function of the set of updates the replica has seen.

**What the network must do.** Only eventual delivery: from each correct replica, some state sent after any given time reaches each other correct replica, directly or through others. Since the state includes everything its sender has seen, there is no need for exactly-once delivery, causal order, acknowledgements or a fixed membership. A new replica starts from the bottom state, or from any replica's state.

**Designing a lattice.** Most state-based CRDTs are built from a few lattices and a few ways to combine them.

- Base lattices: numbers with max, sets with union, booleans with "or".
- *Products*: pairs ordered component by component, joined component by component. A PN-counter is a pair of grow-only counters.
- *Maps* from keys to a lattice, joined key by key, where a missing key counts as bottom. A grow-only counter is a map from replica to number.
- *Lexicographic pairs* $(t, v)$, ordered by $t$ first. A last-writer-wins register is a pair of a timestamp and a value.

An update must only go up. So a deletion cannot remove information; it must add some, for example a *tombstone* that marks an element as deleted, or a causal context that records which additions the deletion has seen. This is the main design difficulty of the style.

**Causal consistency for free.** A merged state reflects everything its sender had seen, so a replica never reflects an update without the updates that its source had seen first. State-based CRDTs therefore give per-object causal consistency without vector clocks in the messages.

**Costs.** Each message carries the whole state, which grows with the data and, for some types, with the number of replicas and deleted elements. [Delta-state CRDTs](/delta-state-crdt/) send small deltas in the same lattice instead. Metadata such as tombstones can be removed only when all replicas have seen it, which needs some coordination or a notion of causal stability.

## Examples

- **[G-counter](/g-counter/).** A vector with one entry per replica; increment adds one to the replica's own entry; merge takes the pointwise max; the value is the sum.
- **PN-counter.** A pair of g-counters for increments and decrements; the value is their difference. See [PN-counter](/pn-counter/).
- **[G-set](/g-set/).** A set that only grows; merge is union.
- **[Two-phase set](/two-phase-set/).** A pair of g-sets, the added and the removed elements; an element removed once can never come back.
- **[LWW register](/lww-register/).** A timestamped value, merged by keeping the larger timestamp; ties are broken by replica id.
- **[MV-register](/mv-register/).** A set of values, each with a version vector; merge keeps the values that no other value dominates, so concurrent writes are all kept.
- **[OR-set](/or-set/).** Each addition gets a unique tag; a removal records the tags it has seen. The optimized form keeps a set of *dots* (replica, sequence number) and a causal context, and needs no tombstones for removed elements.
- **Non-example.** A set whose remove deletes the element, with union as merge, is a semilattice, but remove is not inflationary. After a remove, merging an old copy brings the element back at one replica and not at another, though both have seen the same updates.

## Where it is used

- **Riak** offers counters, sets, maps, flags and registers as state-based CRDTs (the riak_dt library), stored as values in its Dynamo-style store and merged on reads and during anti-entropy.
- **Akka Distributed Data** replicates state-based CRDTs between the nodes of a cluster by gossip, with delta propagation as an optimization.
- **Lattice-based languages.** Bloom^L lets programmers define lattices with a merge function and write programs as monotone functions over them; the [CALM theorem](/calm-theorem/) explains why such programs need no coordination.
- **Version vectors and stores with sibling values**, such as the multi-value registers of Dynamo-style stores, are state-based CRDTs in all but name.

## References
