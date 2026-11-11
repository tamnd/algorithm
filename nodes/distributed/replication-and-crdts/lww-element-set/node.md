---
tag: 3D6HMS
kind: data-structure
slug: lww-element-set
name: LWW-Element-Set
aliases:
- last-writer-wins element set
area: distributed/replication-and-crdts
level: intro
summary: A replicated set that keeps an add timestamp and a remove timestamp per element. The later one decides membership, a bias breaks ties, and clock skew can hide a later write.
implements: [crdt]
model: word-ram
complexity:
  vars: {m: the number of entries in the received state}
  time: {expected: Θ(m)}
  space: {extra: Θ(m)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [last-writer-wins, state-based-crdt, g-set]
see_also: [last-writer-wins, two-phase-set, or-set, lww-register, tombstone, clock-skew, hybrid-logical-clocks, lamport-clocks]
sources:
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.3.3 and Figure 12 (LWW-element-Set, with add and remove timestamps per element and a bias towards add or remove)
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the set designs that order add and remove
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, last write wins and the risks of unsynchronized clocks
---

An LWW-Element-Set (last-writer-wins element set) is a replicated set in which each element carries two timestamps: the largest add timestamp and the largest remove timestamp that the replica has seen. An element is in the set when its add timestamp is larger than its remove timestamp, and a fixed bias decides the case of equal timestamps. Merge takes the larger timestamp of each kind per element, so the states form a [join-semilattice](/join-semilattice/). It applies the [last-writer-wins](/last-writer-wins/) rule per element, and unlike the [2P-Set](/two-phase-set/) it allows an element to be added again after a remove.

## In plain words

For each item, every server writes down two times: the last time someone put the item in, and the last time someone took it out. The item is "in" if the last "put in" time is later than the last "take out" time.

To combine two copies, keep the later time of each kind for each item. Order and repeats do not matter.

The result is only as good as the clocks. If one server's clock is behind, its actions look older than they are. A "put in" that really came last can lose to an earlier "take out" with a larger time, and the item disappears.

## The abstract type

The LWW-Element-Set implements a replicated set with updates ADD$(e, t)$ and REMOVE$(e, t)$ and the query LOOKUP. It is a [state-based CRDT](/state-based-crdt/). The caller supplies the timestamp $t$.

**Model.** There are $n$ replicas. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. Each update gets a timestamp from a totally ordered set. Correct behaviour as users see it needs timestamps that respect causality: an update that follows another in causal order has a larger timestamp. [Lamport clocks](/lamport-clocks/) or [hybrid logical clocks](/hybrid-logical-clocks/) give this; unsynchronized physical clocks do not.

**Specification.** Fix a bias, "add" or "remove". Let $C_i$ be the causal history of replica $i$. For an element $e$, let $a$ be the largest timestamp of an ADD$(e)$ in $C_i$ and $r$ the largest timestamp of a REMOVE$(e)$ in $C_i$, with $-\infty$ for none. LOOKUP$(e)$ at $i$ returns true when $a > r$, false when $a < r$, and the bias when $a = r \ne -\infty$. If updates stop and replicas keep exchanging states, all replicas reach the same set.

## Representation

A replica stores two maps from elements to timestamps, $\mathit{add}$ and $\mathit{rem}$, with a missing key read as $-\infty$. A state is ordered by $s \le s'$ when $s.\mathit{add}[e] \le s'.\mathit{add}[e]$ and $s.\mathit{rem}[e] \le s'.\mathit{rem}[e]$ for every $e$. It is a product of max-semilattices, one per element and kind, so the join is the entrywise maximum. The invariant is that each entry is the largest timestamp of its kind for that element in $C_i$.

## Operations

```pseudo id=main
CREATE(bias)
L1  add ← empty map;  rem ← empty map                ▷ a missing key reads as −∞

ADD(e, t)
L2  add[e] ← max(add[e], t)

REMOVE(e, t)
L3  rem[e] ← max(rem[e], t)

LOOKUP(e)
L4  if add[e] = −∞ then return false
L5  if add[e] ≠ rem[e] then return add[e] > rem[e]
L6  return bias = "add"                               ▷ equal timestamps

MERGE(add', rem')                                     ▷ a state received from a replica
L7  for each e in add' do add[e] ← max(add[e], add'[e])
L8  for each e in rem' do rem[e] ← max(rem[e], rem'[e])
```

ADD and REMOVE (lines L2 and L3) only raise entries, so both are inflationary. LOOKUP (lines L4 to L6) compares the two timestamps and falls back on the bias (line L6). MERGE (lines L7 and L8) is the entrywise maximum.

## Example

Two replicas $a$ and $b$, bias "add". A state for element $x$ is written as (add timestamp, remove timestamp).

| step | event | $a$ | $b$ | $x$ in set at $a$, $b$ |
| --- | --- | --- | --- | --- |
| 1 | $a$ adds $x$ at 1 | $(1, -\infty)$ | $(-\infty, -\infty)$ | yes, no |
| 2 | $b$ merges $a$, then removes $x$ at 3 | same | $(1, 3)$ | yes, no |
| 3 | $a$ adds $x$ at 2, concurrently | $(2, -\infty)$ | same | yes, no |
| 4 | $a$ and $b$ merge each other | $(2, 3)$ | $(2, 3)$ | no, no |
| 5 | $a$ adds $x$ at 4 | $(4, 3)$ | $(2, 3)$ | yes, no |
| 6 | $b$ merges $a$ | same | $(4, 3)$ | yes, yes |

In step 4 the remove at time 3 beats the concurrent add at time 2, only because its timestamp is larger. In step 5 the element comes back, which a 2P-Set does not allow. If an add and a remove both had timestamp 5, the bias decides: with bias "add" the element is in the set, with bias "remove" it is not.

**A clock-skew anomaly.** Let replica $b$'s clock be 10 units behind real time. At real time 100, $a$ adds $x$ with timestamp 100, and $b$ merges it. At real time 105, $a$ removes $x$ with timestamp 105. At real time 108, a user at $b$ adds $x$ again; $b$'s clock says 98. After the replicas merge, the add timestamp is $\max(100, 98) = 100$ and the remove timestamp is 105, so $x$ is not in the set, although the last action in real time was an add. The add at $b$ is lost without any error. A Lamport clock at $b$ would have given the add a timestamp above 100, but not above 105, since $b$ had not seen the remove; with concurrent operations, the timestamp order is the only order there is.

## Correctness

Each entry of each map is a max register, which is a join-semilattice, and the whole state is their product, so MERGE is the join and ADD and REMOVE are inflationary. The invariant "each entry is the largest timestamp of its kind for that element in $C_i$" holds at the start, after an update, and after a merge, because the maximum over a union of histories is the maximum of the two maxima. With it, LOOKUP computes the specification. The [CRDT convergence theorem](/crdt-convergence-theorem/) then gives convergence. Note that the proof does not need the timestamps to be correct; it needs only a total order. Whether the result matches user intent depends on the clocks. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

With hash maps:

| operation | time | messages |
| --- | --- | --- |
| ADD, REMOVE, LOOKUP | $\Theta(1)$ expected | none |
| MERGE of a state with $m$ entries | $\Theta(m)$ expected | one state of $m$ entries |

The state keeps two timestamps for every element ever added or removed, so removed elements stay as [tombstones](/tombstone/). Each timestamp takes $O(\log T)$ bits for a largest timestamp $T$.

## Variants

- **Remove bias or add bias.** The bias only matters on equal timestamps. With unique timestamps such as (counter, replica id) pairs, ties never happen and the bias is not needed.
- **One timestamp per element.** Keep a single (timestamp, present flag) pair per element, which is an [LWW-Register](/lww-register/) of a boolean per element. This is how many key-value stores implement deletes.
- **Op-based form.** Broadcast (element, timestamp, kind) and apply it with the same max rule. Delivery can be in any order since max commutes.
- **[OR-Set](/or-set/).** Replaces timestamps with unique tags, so a concurrent add always wins and clocks do not matter.

## When to use it

Use an LWW-Element-Set when a set must allow re-add and remove, the replicas have reasonable clocks, and losing a write that was concurrent or slightly skewed is acceptable: caches, presence lists, feature flags. When a concurrent add must not be lost, use an [OR-Set](/or-set/).

## Pitfalls

- **Clock skew loses writes.** A replica with a slow clock makes old-looking timestamps, and its later writes can lose to earlier ones, as the example shows. Use [hybrid logical clocks](/hybrid-logical-clocks/) or bound the [clock skew](/clock-skew/).
- **A fast clock wins for too long.** A replica with a clock far ahead writes timestamps that no other replica can beat until real time catches up.
- **Ties with a bias.** With raw physical timestamps, two replicas can write the same timestamp. The bias then decides, which may surprise users; add the replica id to the timestamp to break ties.
- **Tombstones.** Removed elements keep their timestamps for ever, and dropping them early lets an old add come back.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L8 and takes the bias as a parameter. The tests check the semilattice laws on reachable states, the example run, both biases on a tie, the clock-skew run above, and seeded random runs with duplicated and reordered states against the specification.

## History

Shapiro, Preguiça, Baquero and Zawirski described the LWW-element-Set in Section 3.3.3 of the 2011 INRIA report, with a timestamp per add and per remove and a bias towards adds or removes. The last-writer-wins rule itself is older; it goes back to Thomas's write rule for replicated databases.

## References
