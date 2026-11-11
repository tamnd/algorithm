---
tag: 0YDBGZ
kind: data-structure
slug: two-phase-set
name: 2P-Set
aliases:
- two-phase set
- 2P-set
area: distributed/replication-and-crdts
level: intro
summary: A replicated set built from two grow-only sets, one of added and one of removed elements. Remove wins over a concurrent add, and a removed element can never be added again.
implements: [crdt]
model: word-ram
complexity:
  vars: {m: the number of elements in the received state}
  time: {expected: Θ(m)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [g-set, state-based-crdt, tombstone]
see_also: [g-set, or-set, lww-element-set, tombstone, crdt, crdt-convergence-theorem, join-semilattice]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the 2P-Set among the example CRDTs
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.3.2 and Specification 12 (state-based 2P-Set, remove with precondition lookup(e), R called the tombstone set)
---

A 2P-Set (two-phase set) is a replicated set with add, remove and lookup. Each replica keeps two [grow-only sets](/g-set/): $A$ holds every element that was added and $R$ holds every element that was removed. An element is in the set when it is in $A$ and not in $R$. Merge is union on both sets. $R$ is a set of [tombstones](/tombstone/): once an element is in $R$ it stays there, so remove wins over a concurrent add and an element can never come back. The name comes from these two phases: an element is first added, then removed, and nothing follows.

## In plain words

Keep two lists on each server. The first list holds everything that was ever put in. The second list holds everything that was ever taken out. An item is "in" if it is on the first list and not on the second.

Both lists only grow, so two copies combine by putting their lists together. The result does not depend on order or on repeated copies.

The cost is in the second list. A server may only take out an item that it can see. After that, the item is gone for good: putting it in again changes nothing, because it is still on the "taken out" list. If one server adds an item while another takes it out, the item ends up out.

## The abstract type

The 2P-Set implements a replicated set with updates ADD and REMOVE and the query LOOKUP. It is a [state-based CRDT](/state-based-crdt/).

**Model.** There are $n$ replicas. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. Replicas may crash and recover with their state on durable storage. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** REMOVE$(e)$ has a precondition at its source: LOOKUP$(e)$ is true there. Let $C_i$ be the causal history of replica $i$. LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ holds an ADD$(e)$ and no REMOVE$(e)$. So a remove beats every add of the same element, earlier or concurrent, and an ADD$(e)$ after a REMOVE$(e)$ has no effect. If updates stop and replicas keep exchanging states, all replicas reach the same set.

## Representation

A replica stores two finite sets $A$ and $R$. A state is a pair $(A, R)$, ordered by $(A, R) \le (A', R')$ when $A \subseteq A'$ and $R \subseteq R'$. This is the product of two G-Set lattices, so it is a join-semilattice with join $(A \cup A', R \cup R')$. The invariants are $R \subseteq A$, $A$ is the set of elements added in $C_i$, and $R$ is the set of elements removed in $C_i$.

## Operations

```pseudo id=main
CREATE()
L1  A ← ∅;  R ← ∅                                     ▷ R is the tombstone set

LOOKUP(e)
L2  return e ∈ A and e ∉ R

ADD(e)
L3  A ← A ∪ {e}

REMOVE(e)
L4  precondition LOOKUP(e)                            ▷ checked at the source only
L5  R ← R ∪ {e}

MERGE(A', R')                                         ▷ a state received from a replica
L6  A ← A ∪ A'
L7  R ← R ∪ R'

COMPARE(A', R')
L8  return A ⊆ A' and R ⊆ R'
```

ADD (line L3) and REMOVE (line L5) only make sets larger, so both are inflationary. The precondition (line L4) runs at the replica that calls REMOVE. It makes sure that $e$ is in $A$ there, so $R \subseteq A$ holds and every remove follows an add in causal order. MERGE (lines L6 and L7) is the join.

## Example

Two replicas $a$ and $b$ start empty. A state is written as $A \mid R$.

| step | event | $a$ | $b$ | elements at $a$, $b$ |
| --- | --- | --- | --- | --- |
| 1 | $a$ adds $x$ and $y$ | $\{x, y\} \mid \varnothing$ | $\varnothing \mid \varnothing$ | $\{x, y\}$, $\varnothing$ |
| 2 | $b$ merges $a$, then removes $x$ | same | $\{x, y\} \mid \{x\}$ | $\{x, y\}$, $\{y\}$ |
| 3 | $a$ adds $z$ | $\{x, y, z\} \mid \varnothing$ | same | $\{x, y, z\}$, $\{y\}$ |
| 4 | $a$ merges $b$ | $\{x, y, z\} \mid \{x\}$ | same | $\{y, z\}$, $\{y\}$ |
| 5 | $a$ adds $x$ again | $\{x, y, z\} \mid \{x\}$ | same | $\{y, z\}$, $\{y\}$ |
| 6 | $b$ merges $a$ | same | $\{x, y, z\} \mid \{x\}$ | $\{y, z\}$, $\{y, z\}$ |

In step 5 the add of $x$ changes nothing: $x$ is already in $A$ and still in $R$. A user who expects $x$ back sees no effect. If in step 3 $a$ had added $x$ instead of $z$, concurrently with the remove at $b$, the result after step 4 would be the same: remove wins.

## Correctness

Each of $A$ and $R$ is a G-Set, so the G-Set invariant holds for each: $A$ is the set of elements added in $C_i$ and $R$ is the set of elements removed in $C_i$. Then line L2 returns true exactly when $C_i$ has an add of $e$ and no remove of $e$, which is the specification. The precondition gives $R \subseteq A$ at the source, and union keeps it. The state order is a product of two semilattices, ADD and REMOVE are inflationary and MERGE is the join, so the [CRDT convergence theorem](/crdt-convergence-theorem/) applies. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With hash sets:

| operation | time | messages |
| --- | --- | --- |
| ADD, REMOVE, LOOKUP | $\Theta(1)$ expected | none |
| MERGE of a state with $m$ entries | $\Theta(m)$ expected | one state of $m$ entries |

The state takes $\Theta(|A| + |R|)$ space. Neither set ever shrinks, so a removed element costs space for ever.

## Variants

- **Op-based 2P-Set.** Broadcast "add $e$" and "remove $e$". A remove must be delivered after the add it removes, which causal delivery gives.
- **U-Set.** If each element is added at most once (for example, elements carry unique ids), $A$ and $R$ can be replaced by one set with a tombstone flag, and an op-based form can drop the tombstone after causal delivery. The INRIA report gives this.
- **PN-Set.** A counter per element, with the element present when the count is positive (Specification 14 in the report). It allows re-adds but does not behave like a set: two concurrent removes push the count below zero.
- **[OR-Set](/or-set/).** Unique tags allow re-add, and add wins instead of remove.
- **[LWW-Element-Set](/lww-element-set/).** Timestamps decide between add and remove, so re-add works.

## When to use it

Use a 2P-Set when an element really should never come back after a remove, for example a set of revoked tokens or of deleted object ids that are never reused. If elements carry fresh unique ids, the no-re-add rule costs nothing. For general sets with re-adds, use an [OR-Set](/or-set/).

## Pitfalls

- **Expecting a re-add to work.** ADD after REMOVE has no effect, without an error. Applications that reuse values (user names, tags) will lose them for good.
- **Removing without the precondition.** A remove of an element that is not in $A$ puts a tombstone for an element that may be added later; that add is then lost before it happens. Check LOOKUP at the source.
- **Tombstones grow without bound.** $R$ keeps every removed element. Garbage collection of $R$ needs all replicas to have seen the remove, which needs coordination.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L8. REMOVE raises an error if its precondition fails. The tests check the semilattice laws on reachable states, the example run, that a concurrent remove wins, and that seeded random runs with duplicated and reordered states converge to the specification computed from the causal history.

## History

Shapiro, Preguiça, Baquero and Zawirski gave the 2P-Set in 2011, in the SSS paper and as Specification 12 of the INRIA report, where $R$ is "colloquially known as the tombstone set". The same report gives the U-Set, the PN-Set and the OR-Set as ways around its limits.

## References
