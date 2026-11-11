---
tag: 8MX7HQ
kind: abstract-type
slug: crdt
name: Conflict-free replicated data type (CRDT)
aliases:
- conflict-free replicated data type
area: distributed/replication-and-crdts
level: core
summary: A replicated data type whose replicas update locally without coordination and still converge, because concurrent updates merge deterministically.
prereqs: [strong-eventual-consistency, eventual-consistency]
see_also: [state-based-crdt, op-based-crdt, delta-state-crdt, crdt-convergence-theorem, join-semilattice, g-counter, or-set, operational-transformation]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 1 (motivation), Section 2 (system model, strong eventual consistency, state-based and op-based objects, Theorems 1 and 2), Section 3 (Theorems 3 and 4), Section 4 (counters, sets, graphs and the sequence)
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA research report RR-7506, 2011
    locator: Section 3 (the catalogue of counters, registers, sets, maps, graphs and sequences), and the discussion of garbage collection
  - paper: doi:10.1145/2578855.2535848
    title: Sebastian Burckhardt, Alexey Gotsman, Hongseok Yang and Marek Zawirski, Replicated data types, specification, verification, optimality, POPL 2014 (ACM SIGPLAN Notices 49(1))
    locator: pages 271 to 284; Section 3 (specifications by visibility and arbitration), Section 6 (Definition 11 of metadata overhead, Figure 10, Theorem 15 for counters and Theorem 17 for OR-sets)
  - paper: "Nuno Preguiça, Carlos Baquero and Marc Shapiro, Conflict-free replicated data types (CRDTs), Encyclopedia of Big Data Technologies, Springer, 2018"
    title: Nuno Preguiça, Carlos Baquero and Marc Shapiro, Conflict-free replicated data types, Encyclopedia of Big Data Technologies, 2018 (arXiv 1806.10254)
    locator: the overview of the three synchronization models, the main types and their concurrency semantics, and the systems that use CRDTs
  - paper: "Peter Bailis, Alan Fekete, Michael J. Franklin, Ali Ghodsi, Joseph M. Hellerstein and Ion Stoica, Coordination avoidance in database systems, Proceedings of the VLDB Endowment 8(3), 2014"
    title: Peter Bailis et al., Coordination avoidance in database systems, PVLDB 8(3), 2014
    locator: the invariant confluence condition, which says which invariants a coordination-free system can keep
---

A conflict-free replicated data type (CRDT) is a data type, such as a counter, a set, a map or a text sequence, whose copies on different machines can each be read and updated at once, without asking any other copy, and that still come to agree. The rules of the type say exactly how concurrent updates combine, so there are no conflicts for a user or an application to resolve. Shapiro, Preguiça, Baquero and Zawirski named and defined CRDTs in 2011: the guarantee they give is [strong eventual consistency](/strong-eventual-consistency/), which says that replicas that have received the same updates are in the same state. A CRDT stays available during a network partition, at the price of giving up [linearizability](/linearizability/).

## In plain words

Imagine a shopping list shared by several phones. Each phone can add or remove items while offline. Later the phones sync. If two phones changed the list at the same time, someone must decide what the list now says.

A CRDT is a data type that decides this by itself, by a fixed rule that every phone applies in the same way. For example, a counter adds up all the increases, and a set may say that an add made at the same time as a remove wins.

Because every copy uses the same rule, and the rule does not care in what order news arrives, all copies that have heard the same news show the same list. No copy ever waits for another, so each one keeps working when the network is down.

## Operations

A CRDT is a replicated object with $n$ replicas. A client talks to one replica, and each replica has these operations.

| operation | what it does |
| --- | --- |
| `query`$(q)$ | returns a result computed from the local state only; it never waits for other replicas |
| `update`$(u)$ | changes the local state at once and returns; it never waits for other replicas |
| `send` | produces a message for the other replicas: the whole state (state-based), a delta (delta-state), or the effect of an update (op-based) |
| `receive`$(m)$ | incorporates a message: by a merge, or by applying an effect |

The queries and updates are those of an ordinary sequential type, such as `value` and `increment` for a counter, or `lookup`, `add` and `remove` for a set. The type must also say what a query returns after concurrent updates, which a sequential type never has to say. Common policies:

- **Commute.** Concurrent increments both count.
- **Add wins** or **remove wins.** In an [OR-set](/or-set/), an add that is concurrent with a remove of the same element wins.
- **Last writer wins.** Concurrent writes are ordered by a timestamp, and the larger one wins; see [LWW register](/lww-register/).
- **Keep all.** A [multi-value register](/mv-register/) returns all concurrently written values, and the next write replaces them.

Burckhardt, Gotsman, Yang and Zawirski (2014) made this precise: a query result is a function of the set of updates *visible* to it, the *visibility* relation among them, and an *arbitration* order that breaks ties.

## Laws

Each CRDT implementation meets these laws in every execution in which the network meets the assumptions of its style.

1. **Availability.** Every query and update completes using only the local replica.
2. **Eventual delivery.** An update applied at one correct replica is applied, in the end, at every correct replica.
3. **Strong convergence.** Two replicas that have applied the same set of updates are in equivalent states: every query returns the same result at both.
4. **Sequential agreement.** If the updates visible to a query are totally ordered by happened-before, the query returns what the sequential type returns after those updates in that order.
5. **Determinism of concurrency.** The result for concurrent updates depends only on the updates and their causal relation (and on the arbitration order, if the type uses one), not on the order of message arrival.

Laws 2 and 3 are the definition of strong eventual consistency. Two sufficient conditions give them, as the [CRDT convergence theorem](/crdt-convergence-theorem/) shows: states in a join-semilattice with inflationary updates and join as merge, or effects that commute when concurrent, with causal delivery.

## Implementations

**Three styles.**

| style | messages | network assumption | page |
| --- | --- | --- | --- |
| state-based (CvRDT) | the whole state | any loss, duplication and order; some message gets through | [state-based CRDT](/state-based-crdt/) |
| op-based (CmRDT) | one effect per update | exactly once, in causal order | [op-based CRDT](/op-based-crdt/) |
| delta-state | joins of small deltas | as state-based; causal merging needs acknowledgements | [delta-state CRDT](/delta-state-crdt/) |

The names "convergent replicated data type" and "commutative replicated data type" refer to the first two styles; both share the acronym CRDT with the general name. Each style can emulate the others, so they define the same class of types at different costs.

**Common types.**

| type | concurrency policy | page |
| --- | --- | --- |
| grow-only counter | increments commute | [g-counter](/g-counter/) |
| increment and decrement counter | pair of g-counters | [PN-counter](/pn-counter/) |
| grow-only set | union | [g-set](/g-set/) |
| two-phase set | a removed element never returns | [2P-set](/two-phase-set/) |
| last-writer-wins register and set | larger timestamp wins | [LWW register](/lww-register/), [LWW-element-set](/lww-element-set/) |
| multi-value register | keep all concurrent values | [MV-register](/mv-register/) |
| observed-remove set | add wins over a concurrent remove | [OR-set](/or-set/) |
| sequence for text | concurrent inserts ordered by identifiers | [RGA](/rga/), [Logoot](/logoot/), [Treedoc](/treedoc/), [WOOT](/woot/), [YATA](/yata/) |

Maps, records and JSON documents are built by nesting these types, with a map from keys to CRDTs whose merge works key by key.

**Where they are used.** Riak and Akka offer state-based counters, sets, maps and registers. Collaborative editors such as those built on Automerge and Yjs use sequence CRDTs. Geo-replicated databases such as AntidoteDB build causally consistent transactions on op-based CRDTs.

## Lower bounds

- **No linearizability.** A CRDT answers every request at once, so by the [CAP theorem](/cap-theorem/) it cannot be linearizable under partitions, and by [PACELC](/pacelc/) it cannot be sequentially consistent with local reads and writes even without partitions. Strong eventual consistency is the price of availability.
- **Not every invariant survives.** A replica that updates without coordination cannot keep an invariant that two concurrent updates, each safe alone, can break together, such as "the balance is not negative" or "the name is unique". Bailis et al. (2014) call the invariants that are safe *invariant confluent*; others need coordination, for example through reservations or escrow.
- **Metadata (Burckhardt et al. 2014, Section 6).** The *worst-case metadata overhead* of a state-based implementation is the largest ratio between the size of the state and the size of a query result, over executions with $n$ replicas and $m$ updates. Any state-based counter has overhead $\Omega(n)$ (Theorem 15): a replica must remember one number for each other replica, which the g-counter meets. Any state-based OR-set has overhead $\Omega(n \lg m)$ (Theorem 17): a replica must remember removed element instances, and the optimized OR-set with version vectors meets this bound. A multi-value register also needs $\Omega(n \lg m)$ and a last-writer-wins register $\Omega(\lg m)$. The proofs build many executions that must leave pairwise different states and count them.
- **Metadata grows without coordination.** Tombstones and causal contexts that record removals can be discarded only when every replica has seen them. Without that knowledge, which needs some agreement on membership, the metadata of many types only grows.

## References
