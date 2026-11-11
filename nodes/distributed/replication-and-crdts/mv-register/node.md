---
tag: ZMJZQC
kind: data-structure
slug: mv-register
name: Multi-value register (MV-Register)
aliases:
- multi-value register
- MV-Register
area: distributed/replication-and-crdts
level: intro
summary: A replicated register that keeps every concurrent write. Each value carries a version vector, merge keeps the maximal ones, and a read returns a set of siblings.
implements: [crdt]
model: word-ram
complexity:
  vars: {n: the number of replicas}
  time: {worst: Θ(n^3)}
  space: {extra: Θ(n^2)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [version-vectors, state-based-crdt, happened-before]
see_also: [lww-register, version-vectors, dotted-version-vectors, dynamo-style-replication, crdt, join-semilattice, vector-clocks]
sources:
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.2.2, Specification 10 (state-based MV-Register with version vectors) and Figure 10 (the Dynamo shopping cart anomaly)
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the multi-value register
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia et al., Dynamo, Amazon's highly available key-value store, SOSP 2007
    locator: pages 205 to 220, Section 4.4 (data versioning with vector clocks, and siblings reconciled by the client)
---

A Multi-value register (MV-Register) is a replicated register that keeps all writes that are concurrent instead of picking one. Each stored value carries a [version vector](/version-vectors/) of $n$ counters. A write at replica $i$ takes the entrywise maximum of the vectors it holds, adds one to entry $i$, and replaces the state with the new pair. Merge takes the union of two states and keeps only the pairs whose vector no other vector strictly dominates. A read returns the set of values in the state, so after concurrent writes it returns two or more siblings. This is how Dynamo-style stores report conflicts to the application.

## In plain words

A register holds one value. When two servers set it at the same time without seeing each other, an [LWW-Register](/lww-register/) silently keeps one. The MV-Register keeps both and lets the reader decide.

To tell "newer" from "at the same time", each value carries a small table with one counter per server. A write copies the largest counters it has seen and raises its own. If one table is at least as large as another in every slot, its value saw the other one, and the older value is dropped. If neither table is larger, the values were written without seeing each other, and both stay. The next write that has seen both replaces them with one value.

## The abstract type

The MV-Register implements a replicated register with the update WRITE$(x)$ and the query READ, which returns a set. It is a [state-based CRDT](/state-based-crdt/).

**Model.** There are $n$ replicas with fixed ids $1, \ldots, n$. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** Let $C_i$ be the causal history of replica $i$, a set of writes ordered by [happened-before](/happened-before/): $w \prec w'$ when $w$ was in the history of the replica that made $w'$. READ at $i$ returns the values of the maximal writes in $C_i$, the writes in $C_i$ that no other write in $C_i$ follows. So a write overwrites every write it has seen, and concurrent writes are all returned.

**Why a read returns a set.** The register has no rule to choose among concurrent writes, and the specification says so: if two writes are concurrent and both are in $C_i$, both are maximal. Any single answer would have to come from an extra rule, such as timestamps, and that is an LWW-Register. Returning the set leaves the choice to the application, which can merge the values (for example, union of two carts) and write the result.

## Representation

A replica stores its id $i$ and a set $S$ of pairs $(x, V)$, where $V \in \mathbb{N}^n$ is a version vector. Vectors are ordered entrywise. The invariant is that $S$ holds exactly the pairs $(x(w), V(w))$ for the maximal writes $w$ in $C_i$, and that $V(w)[j]$ is the number of writes of replica $j$ in the causal history of $w$, counting $w$. Then $V(w) \le V(w')$ exactly when $w \preceq w'$. The vectors in $S$ form an antichain, and $|S| \le n$ because the writes of one replica are ordered.

States are ordered by $S \le T$ when every vector of $S$ is below some vector of $T$. With the invariant, a state names the down-closed set of writes below its maximal writes, $S \le T$ means that the history of $S$ is contained in that of $T$, and the join is the maximal elements of the union.

## Operations

```pseudo id=main
CREATE(n, i)
L1  S ← ∅

READ()
L2  return {x : (x, V) ∈ S}

WRITE(x)
L3  V ← the zero vector of length n
L4  for each (y, W) ∈ S do V ← max(V, W)              ▷ entrywise
L5  V[i] ← V[i] + 1
L6  S ← {(x, V)}                                      ▷ the new write dominates all of S

MERGE(T)                                              ▷ a state received from a replica
L7  S ← MAXIMAL(S ∪ T)

MAXIMAL(U)
L8  for each (x, V) ∈ U do
L9      keep (x, V) unless some (y, W) ∈ U has V ≤ W and V ≠ W
```

WRITE (lines L3 to L6) makes a vector that is above every vector in $S$, so the new pair dominates the whole state. MERGE (line L7) drops the pairs that the other state has seen and keeps the rest. MAXIMAL (lines L8 and L9) is a direct quadratic scan.

## Example

Three replicas $a$, $b$ and $c$. A pair is written as value with vector $(a, b, c)$.

| step | event | $a$ | $b$ | $c$ | READ at $a$ |
| --- | --- | --- | --- | --- | --- |
| 1 | $a$ writes milk | milk $(1,0,0)$ | $\varnothing$ | $\varnothing$ | $\{$milk$\}$ |
| 2 | $b$ and $c$ merge $a$ | same | milk $(1,0,0)$ | milk $(1,0,0)$ | $\{$milk$\}$ |
| 3 | $b$ writes eggs; $c$ writes tea | same | eggs $(1,1,0)$ | tea $(1,0,1)$ | $\{$milk$\}$ |
| 4 | $a$ merges $b$ and $c$ | eggs $(1,1,0)$, tea $(1,0,1)$ | same | same | $\{$eggs, tea$\}$ |
| 5 | $a$ writes "eggs, tea" | "eggs, tea" $(2,1,1)$ | same | same | $\{$eggs, tea$\}$ as one value |
| 6 | $b$ and $c$ merge $a$ | same | "eggs, tea" $(2,1,1)$ | "eggs, tea" $(2,1,1)$ | same |

In step 4, milk is dropped because $(1,0,0) \le (1,1,0)$. Eggs and tea stay because neither vector is below the other. In step 5, $a$ resolves the conflict by writing a combined value; its vector $(2,1,1)$ dominates both siblings, so step 6 removes them everywhere.

**The Dynamo cart anomaly.** Dynamo keeps siblings with vector clocks, and the shopping cart merges siblings by set union. The INRIA report (Figure 10) shows the cost: if one replica removes an item from the cart while another, concurrent version still has it, the union puts the item back. The MV-Register reports the conflict correctly; the anomaly comes from the application's merge of the values.

## Correctness

The core fact is that $V(w) \le V(w')$ exactly when $w \preceq w'$: a version vector of a write counts the writes of each replica in its history, and these writes form a prefix per replica. Line L4 computes the counts of $C_i$, because every write of $C_i$ is below some maximal write, and line L5 adds the new write. Then MAXIMAL keeps exactly the maximal writes of $C_i \cup H$, since a maximal write of the union is maximal in its own side and is not below anything in the other. States correspond to finite down-closed sets of writes, ordered by inclusion with union as join, so the semilattice laws hold and WRITE is inflationary. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The state has at most $n$ pairs, each with $n$ counters.

| operation | time | messages |
| --- | --- | --- |
| READ | $O(n)$ | none |
| WRITE | $O(n^2)$ | none |
| MERGE (direct scan) | $O(n^3)$ | one state of $O(n^2)$ counters and up to $n$ values |

In practice the number of siblings is small, often one, so a write costs $O(n)$ and a merge $O(n)$ per pair. [Dotted version vectors](/dotted-version-vectors/) make the metadata per sibling one dot plus a shared vector.

## Variants

- **Dynamo siblings with vector clocks.** The client reads the siblings with their context, writes a resolved value with that context, and the server drops the siblings the context covers (DeCandia et al. 2007). Riak does the same with [dotted version vectors](/dotted-version-vectors/), which fix sibling explosion when the server stamps writes for many clients.
- **Op-based MV-Register.** Broadcast (value, vector); with causal delivery, the receiver drops the pairs below the new vector.
- **[LWW-Register](/lww-register/).** Keeps one value by a total order on stamps, with $O(1)$ metadata.

## When to use it

Use an MV-Register when concurrent writes must not be lost silently and the application can merge values: shopping carts, documents with a manual merge, configuration that a person reviews. If an arbitrary winner is fine, an LWW-Register is cheaper. If the value has structure (a set, a counter, a map), a CRDT for that structure merges it without asking the user.

## Pitfalls

- **Treating a read as one value.** A read can return several values. Code that takes "the first" picks at random and loses data.
- **Merging siblings by union.** For sets with removes, union brings removed items back, the Dynamo cart anomaly. Use an [OR-Set](/or-set/) if the value is a set.
- **Writing without the read context.** A write that does not start from the merged vectors of all siblings it resolves leaves them in place, so they come back as siblings.
- **Vectors per client instead of per replica.** If every client gets an entry, vectors grow with the number of clients. Keep entries per replica and use dotted version vectors.

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L9. The tests check the example run, the semilattice laws on reachable states, and seeded random runs with duplicated and reordered states, where READ must equal the values of the maximal writes in the causal history computed by an oracle.

## History

Shapiro, Preguiça, Baquero and Zawirski specified the MV-Register as Specification 10 of the 2011 INRIA report and related it to the shopping cart of Dynamo (DeCandia et al. 2007), which keeps concurrent versions with vector clocks and asks the client to reconcile them. The version vector itself comes from the Locus file system work of Parker et al. (1983).

## References
