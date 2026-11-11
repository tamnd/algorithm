---
tag: TFCFZR
kind: data-structure
slug: lww-register
name: LWW-Register
aliases:
- last-writer-wins register
area: distributed/replication-and-crdts
level: intro
summary: A replicated register that stores one value with a stamp (counter, replica id). Merge keeps the value with the larger stamp, so concurrent writes resolve to one winner.
implements: [crdt]
model: word-ram
complexity:
  vars: {v: the size of the stored value}
  time: {worst: Θ(1)}
  space: {extra: Θ(v)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [last-writer-wins, state-based-crdt, lamport-clocks]
see_also: [last-writer-wins, mv-register, lww-element-set, lamport-clocks, hybrid-logical-clocks, crdt, join-semilattice]
sources:
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.2.1, Specification 8 (state-based LWW-Register) and Specification 9 (op-based), timestamps as a local counter with the replica id
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the last-writer-wins register
  - paper: doi:10.1145/359545.359563
    title: Leslie Lamport, Time, clocks, and the ordering of events in a distributed system, Communications of the ACM 21(7), 1978
    locator: pages 558 to 565, logical clocks and the total order by clock value and process id
---

An LWW-Register (last-writer-wins register) is a replicated register that holds one value. Each write tags the value with a stamp $(c, r)$: a counter $c$ one larger than any counter the replica has seen, and the id $r$ of the writing replica. Stamps compare as pairs, so two different writes never tie. Merge keeps the value with the larger stamp. The states form a [join-semilattice](/join-semilattice/), so replicas converge to the value of the write with the largest stamp. This page is about the register as a data structure; the [last-writer-wins](/last-writer-wins/) page covers the general rule and its use in databases.

## In plain words

A register holds one value, like a user's display name. Any server can set a new value at any time. Each server stamps every new value with a number that is one larger than the largest number it has seen, plus its own name to break ties.

To combine two copies, keep the value with the larger stamp. If two servers set different values at the same time, one of them wins on every server, and the other value is gone. The register never shows both; that is the price of a single answer.

## The abstract type

The LWW-Register implements a replicated register with the update WRITE$(v)$ and the query READ. It is a [state-based CRDT](/state-based-crdt/).

**Model.** There are $n$ replicas with unique ids from a totally ordered set. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** Each write gets a stamp, and stamps are unique, totally ordered and consistent with causality: if a write is in the causal history of the replica that makes a second write, the second write has a larger stamp. READ at replica $i$ returns the value of the write with the largest stamp in the causal history $C_i$, or the initial value if $C_i$ has no write. So a write overwrites every write it has seen, and among concurrent writes the one with the larger stamp wins.

## Representation

A replica stores its id $r$ and a pair (stamp, value), where a stamp is a pair $(c, r')$ of a natural number and a replica id, compared in [lexicographic order](/lexicographic-order/). The initial stamp is $(0, \bot)$ with $\bot$ below every id. States are ordered by their stamps. Two states with equal stamps have equal values, because a stamp names one write. The order is total on stamps, so the join of two states is the one with the larger stamp. The counter $c$ of the current stamp is at least every counter the replica has seen, so it plays the part of a [Lamport clock](/lamport-clocks/).

## Operations

```pseudo id=main
CREATE(r, v₀)
L1  stamp ← (0, ⊥);  value ← v₀

READ()
L2  return value

WRITE(v)
L3  c ← stamp.counter + 1                             ▷ larger than every counter seen here
L4  stamp ← (c, r);  value ← v

MERGE(stamp', value')                                 ▷ a state received from a replica
L5  if stamp' > stamp then
L6      stamp ← stamp';  value ← value'

COMPARE(stamp', value')
L7  return stamp ≤ stamp'
```

WRITE (lines L3 and L4) makes a stamp larger than the current one, so it is inflationary. The current stamp is the largest stamp the replica has seen, because MERGE (lines L5 and L6) keeps the larger stamp, so the new counter is larger than the counter of every write in the causal history. MERGE is the join.

## Example

Three replicas $a$, $b$ and $c$ with ids 0, 1 and 2, all starting at $((0, \bot), \text{none})$.

| step | event | $a$ | $b$ | $c$ |
| --- | --- | --- | --- | --- |
| 1 | $a$ writes red | $((1, 0), \text{red})$ | initial | initial |
| 2 | $b$ merges $a$, then writes green | same | $((2, 1), \text{green})$ | initial |
| 3 | $c$ writes blue, concurrently | same | same | $((1, 2), \text{blue})$ |
| 4 | $a$ merges $c$ | $((1, 2), \text{blue})$ | same | same |
| 5 | all merge all | $((2, 1), \text{green})$ | $((2, 1), \text{green})$ | $((2, 1), \text{green})$ |

In step 4, red and blue are concurrent with equal counters, and blue wins on the replica id. In step 5, green wins because $b$ had seen red when it wrote, so its counter is larger. Blue was concurrent with green, and it is lost at every replica. If two writes have the same counter, the larger replica id wins: $((3, 0), x)$ and $((3, 1), y)$ merge to $y$.

## Correctness

The invariant is that the stamp at replica $i$ is the largest stamp among the writes in $C_i$ and the value is the value of that write. It holds at the start, after a write (whose stamp is larger than every stamp in $C_i$), and after a merge (the larger of two maxima is the maximum of the union). This gives the specification. Stamps are unique because two writes at one replica have different counters and writes at different replicas have different ids. The states form a chain under the stamp order, which is a join-semilattice with join "the larger", so the [CRDT convergence theorem](/crdt-convergence-theorem/) gives convergence. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | messages |
| --- | --- | --- |
| READ, WRITE | $\Theta(1)$ | none |
| MERGE, COMPARE | $\Theta(1)$ stamp comparisons | one state: a stamp and a value |

The state is one value and one stamp of $O(\log W + \log n)$ bits after $W$ writes, so the metadata does not grow with the number of replicas. Compare the [MV-Register](/mv-register/), which needs a version vector of $n$ entries per value.

## Variants

- **Op-based LWW-Register.** Broadcast (stamp, value) and apply it with the same rule. The rule is a max, so delivery order does not matter (Specification 9 in the INRIA report).
- **Physical or hybrid timestamps.** Many systems stamp writes with wall-clock time and a replica id. This gives a total order, but it is consistent with causality only if clocks are, which is why [hybrid logical clocks](/hybrid-logical-clocks/) combine both.
- **[MV-Register](/mv-register/).** Keeps all concurrent values instead of picking one.
- **LWW-Map.** A map from keys to LWW-Registers, merged key by key, which is the core of many key-value stores.

## When to use it

Use an LWW-Register for a value where the latest write is what matters and losing a concurrent write is acceptable: a profile field, a configuration value, a cursor position. If users must see conflicts, or if concurrent writes carry information that must not be dropped, use an [MV-Register](/mv-register/) or a richer CRDT.

## Pitfalls

- **Silent loss of concurrent writes.** One of two concurrent writes disappears without any error, as blue does in the example.
- **Stamps that ignore causality.** If a replica writes without first raising its counter above all counters it has seen, a write that follows another can lose to it. Line L3 must use the stamp after merges.
- **Ties without a replica id.** Counters alone tie, and two replicas with equal counters then keep different values for ever. The replica id in the stamp is what makes the order total.
- **Read-modify-write.** "Read, add one, write" on an LWW-Register loses concurrent increments. Use a counter CRDT for counts.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L7, and a pure `join` function gives the semilattice. The tests check the semilattice laws on reachable states, the example run, the tie rule, and seeded random runs with duplicated and reordered states, where every replica must hold the write with the largest stamp in its causal history.

## History

Shapiro, Preguiça, Baquero and Zawirski specified the LWW-Register in Section 3.2.1 of the 2011 INRIA report, in a state-based form (Specification 8) and an op-based form (Specification 9). They build its timestamps from a per-replica counter and the replica id, which is the total order of Lamport (1978), and they credit the last-writer-wins rule to Thomas.

## References
