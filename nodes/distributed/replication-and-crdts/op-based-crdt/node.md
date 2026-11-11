---
tag: G9QCWP
kind: concept
slug: op-based-crdt
name: Operation-based CRDT (CmRDT)
aliases:
- CmRDT
- commutative replicated data type
area: distributed/replication-and-crdts
level: core
summary: CRDT whose replicas broadcast update effects; reliable causal delivery plus commuting concurrent effects makes replicas with the same effects equal.
prereqs: [crdt, causal-broadcast, happened-before]
see_also: [state-based-crdt, delta-state-crdt, crdt-convergence-theorem, or-set, rga, operational-transformation, vector-clocks, strong-eventual-consistency]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2.4 (operation-based objects, prepare and effect, delivery preconditions, Definitions 5 and 6, Theorem 2), Section 3 (Theorems 3 and 4, emulation between the two styles), Section 4 (the counter and set examples)
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA research report RR-7506, 2011
    locator: Section 2 (the op-based specification style), Section 3 (op-based counters, the observed-remove set and the replicated growable array)
  - paper: "Carlos Baquero, Paulo Sérgio Almeida and Ali Shoker, Making operation-based CRDTs operation-based, DAIS 2014, Lecture Notes in Computer Science 8460, Springer"
    title: Carlos Baquero, Paulo Sérgio Almeida and Ali Shoker, Making operation-based CRDTs operation-based, DAIS 2014
    locator: the tagged reliable causal broadcast, causal stability, and pure op-based counters and sets
  - paper: doi:10.1145/3133933
    title: Victor B. F. Gomes, Martin Kleppmann, Dominic P. Mulligan and Alastair R. Beresford, Verifying strong eventual consistency in distributed systems, Proceedings of the ACM on Programming Languages 1 (OOPSLA), 2017
    locator: Sections 3 to 5 (the abstract convergence theorem, the network model with causal delivery, and the verified counter, observed-remove set and RGA)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Handling write conflicts (automatic conflict resolution with CRDTs)
---

An operation-based CRDT, or CmRDT, is a replicated data type in which replicas send each other the updates they perform, not their states. Each update is split into a *prepare* step, which runs once at the replica where the user acts, and an *effect*, which every replica applies. Shapiro, Preguiça, Baquero and Zawirski proved in 2011 that, if the network delivers every effect exactly once in [causal order](/causal-broadcast/) and any two concurrent effects commute, then replicas that have applied the same effects are in the same state. Messages are small, but the delivery layer must do real work: drop duplicates, buffer early messages, and retry lost ones.

## In plain words

Several copies of a shared object change on their own. In the operation-based style, a copy that makes a change tells the others what it did, for example "add 2" or "remove this item". Every copy then repeats the change on its own data.

This works when three things hold. Every message must arrive, and only once, because "add 2" applied twice adds 4. A message must not arrive before an earlier change it depends on, because removing an item that has not arrived yet removes nothing. And two changes made at the same time, without either copy knowing of the other, must give the same result in either order.

When all three hold, copies that have applied the same changes always agree.

## The idea

**Model.** There are $n$ replicas. An op-based object is $(S, s^0, q, t, u, P)$: states, an initial state, queries, prepare functions, effects and delivery preconditions. When a user calls an update at replica $i$:

1. *Prepare* $t$ runs at $i$ only. It has no side effect. It reads the local state and the arguments and returns an effect $u$, a description of the change that carries any information the other replicas need, such as a unique tag.
2. *Effect* $u$ is applied at $i$ at once and broadcast. Every other replica applies $u$ when the delivery layer delivers it and the precondition $P(s, u)$ holds.

The split matters. In an observed-remove set, `remove(e)` reads at the source which tags of $e$ are present, and the effect removes exactly those tags everywhere. An effect that said "remove $e$" would remove at other replicas tags that the source never saw.

**Delivery.** Effects are sent by *reliable causal broadcast*: every effect reaches every correct replica, exactly once, and if an effect $u$ [happened before](/happened-before/) $u'$, every replica applies $u$ first. The usual implementation stamps each effect with a [vector clock](/vector-clocks/), keeps a per-sender counter of applied effects, drops a message whose sequence number it has already seen, and buffers a message from $j$ with clock $V$ until $V[j]$ is one more than the count from $j$ and $V[k]$ is at most the count from $k$ for every other $k$. Lost messages are resent until acknowledged.

**Convergence condition.** Two effects *commute* if, at every reachable state where both are enabled, applying them in either order gives the same state. The [CRDT convergence theorem](/crdt-convergence-theorem/) (Theorem 2) states: if all concurrent effects commute and causal delivery satisfies the preconditions, the object is [strongly eventually consistent](/strong-eventual-consistency/). The proof uses causal delivery to make every replica apply a linear extension of the happened-before order, and commutativity to swap adjacent concurrent effects until two such orders agree.

Effects that are causally ordered need not commute; causal delivery fixes their order. Only concurrent effects need to commute, which is why causal delivery is so useful.

**Comparison with state-based CRDTs.**

| | op-based | [state-based](/state-based-crdt/) |
| --- | --- | --- |
| message | one effect, usually small | the whole state |
| network | exactly once, causal order | any loss, duplication and order, as long as some message gets through |
| condition | concurrent effects commute | states form a semilattice, updates are inflationary, merge is the join |
| membership | the broadcast layer must know all replicas | any replica can merge any state |
| new replica | needs a snapshot plus the later effects | needs one state |

Each style can emulate the other (Shapiro et al., Theorems 3 and 4): a state-based object can keep the set of effects it has seen as its state, and an op-based object can broadcast its whole state as an effect that merges. [Delta-state CRDTs](/delta-state-crdt/) sit in between: they ship small deltas like op-based ones but keep the robust network model of state-based ones.

**Pure op-based CRDTs and causal stability.** Baquero, Almeida and Shoker (2014) noted that many op-based designs send effects that carry state, such as sets of tags, and proposed *pure* op-based CRDTs whose effect is just the operation and its arguments. The delivery layer gives each effect a timestamp, and the object keeps a partially ordered log of effects. An effect is *causally stable* when every replica has delivered it; from then on no concurrent effect can arrive, so the object can fold it into a compact state and drop its metadata.

## Examples

- **Counter.** Prepare for `add(k)` returns $k$; the effect adds $k$. Addition commutes in all cases, so the counter needs exactly-once delivery but not causal order. The implementation shows that 500 random runs with arbitrary reordering all converge to the sum of all effects, and that one duplicated message makes two replicas differ.
- **Observed-remove set.** `add(e)` prepares a fresh tag $(i, k)$; `remove(e)` prepares the set of tags of $e$ that the source holds. Concurrent add and remove commute: the remove cannot name the fresh tag of a concurrent add, so the add wins. A remove and the add it observed do not commute, and causal delivery keeps them in order. The implementation builds a run in which replica 2 receives the remove before the add: without causal order it keeps $x$ while the other two replicas do not, and with causal order the same arrivals are buffered and all three end with the empty set. See [OR-set](/or-set/).
- **Replicated growable array.** The [RGA](/rga/) for shared text inserts each element after a named element, with a unique timestamp, and orders concurrent inserts at the same place by timestamp. Its effects commute when concurrent, and an insert after an element must be delivered after the insert of that element, which causal delivery gives.
- **Non-example: a plain register.** Two concurrent effects `set(1)` and `set(2)` do not commute. A last-writer-wins register makes them commute by attaching a timestamp and keeping the larger one; a multi-value register keeps both. See [LWW register](/lww-register/) and [MV-register](/mv-register/).
- **Non-example: operational transformation.** [Operational transformation](/operational-transformation/) also sends operations, but it rewrites an operation against concurrent ones before applying it, instead of designing operations that commute.

## Where it is used

- **Collaborative editors.** Sequence CRDTs such as RGA, Logoot and Treedoc were designed in the op-based style. Libraries such as Automerge exchange changes that name the changes they depend on, so each replica applies them in causal order.
- **Geo-replicated databases.** AntidoteDB builds transactions with causal consistency on op-based CRDTs, and uses its causally consistent log as the delivery layer.
- **Systems with an existing ordered log.** When updates already flow through a log with causal or total order, such as a message queue per object, op-based CRDTs reuse it and send only small effects.
- **Verification.** Gomes, Kleppmann, Mulligan and Beresford proved the convergence of an op-based counter, observed-remove set and RGA in Isabelle/HOL, on top of a formal model of causal broadcast.

## References
