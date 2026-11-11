---
tag: PZZKRZ
kind: data-structure
slug: g-set
name: G-Set
aliases:
- grow-only set
area: distributed/replication-and-crdts
level: intro
summary: A replicated set that supports add and lookup but no remove. The state is a set and merge is set union, which makes it the simplest state-based CRDT.
implements: [crdt]
model: word-ram
complexity:
  vars: {m: the number of elements in the received state}
  time: {expected: Θ(m)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [state-based-crdt, join-semilattice]
see_also: [two-phase-set, or-set, lww-element-set, g-counter, crdt, crdt-convergence-theorem, hash-table]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the grow-only set among the example CRDTs
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.3.1 and Specification 11 (state-based grow-only set)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the delta form of the grow-only set
---

A G-Set (grow-only set) is a replicated set with two operations, add and lookup, and no remove. Each replica keeps a set $A$. An add puts an element in $A$, and two states merge by set union. Union is the join of the subset order, so the states form a [join-semilattice](/join-semilattice/), and replicas that exchange states over a network that loses, repeats and reorders messages end with the same set: every element that any replica added.

## In plain words

Several servers keep a list of things that were seen, for example the ids of users who opened a page. Each server can add a new item at any time, also when it cannot reach the others. Nobody ever takes an item out.

To combine two copies, put all items of both copies together. If a copy arrives twice, nothing changes. If an old copy arrives late, it has no item that the newer copy lacks, so again nothing changes. In the end every server holds every item that any server added. The price is that an item can never be removed, because a remove would come back on the next combine.

## The abstract type

The G-Set implements a replicated set with the update ADD and the query LOOKUP. It is a [state-based CRDT](/state-based-crdt/).

**Model.** There are $n$ replicas with unique ids. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. Replicas may crash and recover with their state on durable storage. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** Let $C_i$ be the causal history of replica $i$: its own adds and the adds in the history of each state it has merged. LOOKUP$(e)$ at $i$ returns true exactly when some ADD$(e)$ is in $C_i$. If adds stop and replicas keep exchanging states, all replicas reach the same set: all added elements.

## Representation

A replica stores one finite set $A$ of elements, in a [hash table](/hash-table/) or a sorted structure. The states are the finite subsets of the element universe, ordered by inclusion. This order is a join-semilattice: the least upper bound of $A$ and $B$ is $A \cup B$. The invariant is that $A$ is the set of elements added in the causal history of the replica.

## Operations

```pseudo id=main
CREATE()
L1  A ← ∅

ADD(e)
L2  A ← A ∪ {e}

LOOKUP(e)
L3  return e ∈ A

MERGE(B)                                              ▷ a state received from a replica
L4  A ← A ∪ B

COMPARE(B)
L5  return A ⊆ B                                      ▷ the semilattice order
```

ADD (line L2) makes the state larger or keeps it, so it is inflationary. MERGE (line L4) is the join, and COMPARE (line L5) is the order, which a replica can use to skip a state it already covers. LOOKUP (line L3) reads only local state.

## Example

Three replicas $a$, $b$ and $c$ start empty. $a$ adds $x$; $b$ adds $y$ and then $x$; $c$ adds $z$.

| step | event | $a$ | $b$ | $c$ |
| --- | --- | --- | --- | --- |
| 1 | the four adds | $\{x\}$ | $\{x, y\}$ | $\{z\}$ |
| 2 | $b$ merges $a$ | $\{x\}$ | $\{x, y\}$ | $\{z\}$ |
| 3 | $c$ merges $b$ | $\{x\}$ | $\{x, y\}$ | $\{x, y, z\}$ |
| 4 | $a$ merges $c$ twice, then its own old state $\{x\}$ | $\{x, y, z\}$ | $\{x, y\}$ | $\{x, y, z\}$ |
| 5 | $b$ merges $c$ | $\{x, y, z\}$ | $\{x, y, z\}$ | $\{x, y, z\}$ |

In step 2 the merge changes nothing, because $\{x\} \subseteq \{x, y\}$: two replicas added $x$ concurrently and the set holds it once. In step 4 the second copy and the old state change nothing, because union is idempotent and an older state is a subset.

## Correctness

The invariant "$A_i$ is the set of elements added in $C_i$" holds at the start, after ADD (both sides gain $e$), and after MERGE (both sides become a union). With it, LOOKUP meets the specification, and replicas with the same history hold the same set. The semilattice laws hold because $\cup$ is commutative, associative and idempotent, and ADD is inflationary, so the [CRDT convergence theorem](/crdt-convergence-theorem/) also gives convergence. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With a hash set of $|A|$ elements:

| operation | time | messages |
| --- | --- | --- |
| ADD, LOOKUP | $\Theta(1)$ expected | none |
| MERGE of a state with $m$ elements | $\Theta(m)$ expected | one state of $m$ elements |
| COMPARE with a state of $m$ elements | $O(\lvert A \rvert)$ expected | none |

The state takes $\Theta(|A|)$ space, and $|A|$ only grows. A full-state message is large. The [delta-state](/delta-state-crdt/) form sends only the new elements, and the op-based form sends "add $e$", which needs no causal order because adds commute.

## Variants

- **[2P-Set](/two-phase-set/).** A second G-Set of removed elements gives remove, but an element can never be added again.
- **[OR-Set](/or-set/).** Unique tags per add allow remove and re-add, with add winning over a concurrent remove.
- **[LWW-Element-Set](/lww-element-set/).** Timestamps per add and remove; the later one wins.
- **G-Counter.** The [g-counter](/g-counter/) is a G-Set of increment events, compressed into one number per replica by the prefix property.

## When to use it

Use a G-Set when elements are only ever added: seen message ids, users who voted, known peers, the set of all operations in a log. It is also a building block: most set CRDTs are G-Sets of tagged adds and removes. If elements must be removed, use one of the variants.

## Pitfalls

- **Removing from $A$ locally.** A replica that deletes $e$ from its own $A$ gets $e$ back at the next merge with any replica that still has it. A G-Set has no remove; build one with a 2P-Set or an OR-Set.
- **Unbounded growth.** $A$ never shrinks, so a G-Set of events grows for ever. Plan for compaction outside the CRDT, which needs coordination.
- **Mutable elements.** If an element is changed after it is added, two replicas may hold different versions of "the same" element and union keeps both. Store immutable values or ids.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L5. The tests check the semilattice laws on all subsets of a three-element universe and run seeded random runs with duplicated, stale and reordered states.

## History

The G-Set is in the catalog of Shapiro, Preguiça, Baquero and Zawirski (2011) as Specification 11 of the INRIA report, where they also give its op-based form and build the 2P-Set from two of them. Almeida, Shoker and Baquero gave its delta-state form.

## References
