---
tag: MTVENE
kind: data-structure
slug: version-vectors
name: Version vectors
aliases:
- version vector
area: distributed/clocks-and-ordering
level: core
summary: One counter per replica, attached to a copy of the data, incremented on each update and merged on sync, so that two copies conflict exactly when their vectors are incomparable.
model: asynchronous-model
complexity:
  vars: {n: the number of replicas}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1983
  people: [D. Stott Parker Jr.]
  note: Parker et al. introduced version vectors to detect mutual inconsistency between copies of files in a partitioned network.
prereqs: [vector-clocks, happened-before]
see_also: [dotted-version-vectors, vector-clocks, mv-register, dynamo-style-replication, anti-entropy, last-writer-wins, eventual-consistency, multi-master-replication]
sources:
  - paper: doi:10.1109/TSE.1983.236733
    title: D. Stott Parker Jr. et al., Detection of mutual inconsistency in distributed systems, IEEE Transactions on Software Engineering SE-9(3), 1983
    locator: pages 240 to 247
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, Detecting Concurrent Writes (version vectors)
  - url: "https://arxiv.org/abs/1011.5808"
    title: Nuno Preguiça, Carlos Baquero, Paulo Sérgio Almeida, Victor Fonte and Ricardo Gonçalves, Dotted version vectors, logical clocks for optimistic replication, arXiv 1011.5808, 2010
    locator: Section 3.2 (one entry per server) and Section 3.3 (one entry per client)
---

A version vector is an array of $n$ counters, one per replica, that is attached to a copy of a replicated object. A replica adds 1 to its own entry when it updates the copy, and two replicas that synchronize compare their vectors. If one vector dominates, the other copy is simply old. If neither dominates, the copies were updated concurrently and there is a conflict. Parker et al. introduced the method in 1983. It is the same array as a [vector clock](/vector-clocks/), but it timestamps the state of a copy, not each event.

## In plain words

Several computers keep a copy of the same file, and each may change its copy while it cannot reach the others. Later two of them meet and must decide what to keep.

Each copy carries a row of counters, one counter for each computer. When a computer changes its copy, it adds one to its own counter. When two computers compare copies, they compare the rows counter by counter. If one row is at least as large in every counter, that copy has seen every change the other copy has seen, so the older copy can be replaced. If each row is larger somewhere, each copy has a change that the other lacks. That is a conflict, and someone must merge the two versions.

## The abstract type

The setting is the [asynchronous model](/asynchronous-model/) with $n$ replicas $r_1, \ldots, r_n$ of one object, known in advance. Replicas can be cut off from each other for any time, and they synchronize in pairs when they meet, as in [anti-entropy](/anti-entropy/). The operations are:

- UPDATE$(i)$: replica $r_i$ changes its copy.
- MERGE$(V, W)$: the entrywise maximum, used when two concurrent copies are reconciled.
- COMPARE$(V, W)$: one of EQUAL, BEFORE ($W$ dominates), AFTER ($V$ dominates) and CONCURRENT.

The specification uses the causal history $H$ of a copy, the set of updates it contains. COMPARE must give EQUAL, BEFORE, AFTER or CONCURRENT exactly when $H_a = H_b$, $H_a \subsetneq H_b$, $H_b \subsetneq H_a$, or neither set contains the other.

## Representation

A copy at replica $r$ carries an array $V_r[1 \ldots n]$. Entry $V_r[k]$ is the number of updates made at $r_k$ that the copy contains. The order is the entrywise order: $V \le W$ if $V[k] \le W[k]$ for each $k$.

## Operations

```pseudo id=main
VERSION-VECTOR for n replicas
L1  V ← (0, 0, …, 0)

UPDATE(i)                               ▷ replica r_i changes its copy
L2  V[i] ← V[i] + 1

MERGE(V, W)
L3  for k ← 1 to n do
L4      V[k] ← max(V[k], W[k])

COMPARE(V, W)
L5  if V = W then return EQUAL
L6  if V[k] ≤ W[k] for each k then return BEFORE
L7  if V[k] ≥ W[k] for each k then return AFTER
L8  return CONCURRENT

SYNC(a, b)                              ▷ replicas a and b exchange their copies
L9  c ← COMPARE(V_a, V_b)
L10 if c = BEFORE then a takes the copy and the vector of b
L11 if c = AFTER then b takes the copy and the vector of a
L12 if c = CONCURRENT then report a conflict, reconcile the two copies, and give both MERGE(V_a, V_b)
```

A sync does not add 1 to any entry. If the reconciliation of line L12 writes a new value, for example a merge chosen by a user, that write is a new UPDATE.

## Example

Three replicas $A$, $B$ and $C$ hold copies of one file, with vectors in the order $(A, B, C)$.

| step | operation | $V_A$ | $V_B$ | $V_C$ | result |
|---|---|---|---|---|---|
| 1 | $A$ updates | $(1,0,0)$ | $(0,0,0)$ | $(0,0,0)$ | |
| 2 | sync $A$, $B$ | $(1,0,0)$ | $(1,0,0)$ | $(0,0,0)$ | AFTER: $B$ takes the copy of $A$ |
| 3 | $B$ updates | $(1,0,0)$ | $(1,1,0)$ | $(0,0,0)$ | |
| 4 | $A$ updates | $(2,0,0)$ | $(1,1,0)$ | $(0,0,0)$ | |
| 5 | sync $A$, $B$ | $(2,1,0)$ | $(2,1,0)$ | $(0,0,0)$ | CONCURRENT: a conflict |
| 6 | sync $C$, $A$ | $(2,1,0)$ | $(2,1,0)$ | $(2,1,0)$ | BEFORE: $C$ takes the copy of $A$ |

At step 5, $(2,0,0)$ and $(1,1,0)$ are incomparable: $A$ has its second update, which $B$ lacks, and $B$ has its first update, which $A$ lacks. At step 6, $C$ has an old copy with no updates of its own, so it is replaced without a conflict.

## Correctness

The invariant is that $V_r[k]$ equals the number of updates of $r_k$ in the copy of $r$, and that these updates are always the first ones of $r_k$. An update adds the next update of its own replica. A sync either copies a newer state, which contains the old one, or takes a union, and the union of two prefixes of one sequence is the longer prefix, whose size is the maximum. So the entrywise order of two vectors is exactly the inclusion order of the two sets of updates. A reported conflict means that each copy has an update the other lacks, and a sync never discards an update. The full proof is below.

## Complexity

| operation | time |
|---|---|
| UPDATE | $\Theta(1)$ |
| MERGE | $\Theta(n)$ |
| COMPARE | $\Theta(n)$ |
| SYNC | $\Theta(n)$ plus the cost of moving the data |

Each copy carries $n$ integers. If the copies have seen $k$ updates in total, each entry has $O(\log k)$ bits. The vector stays this size however many syncs happen, because a sync does not tick.
## Variants

- **Version vectors against vector clocks.** A [vector clock](/vector-clocks/) ticks at every event, including each send and receive, and orders events. A version vector ticks only when the data changes, and orders states of a copy. Messages that carry no change do not touch it.
- **One entry per server or one per client.** In a store such as Dynamo, servers act for clients. With one entry per server, two clients that write through the same server can make one write look newer than the other, and an update is lost (Section 3.2 of the DVV paper). With one entry per client, the vectors grow with the number of clients (Section 3.3).
- **[Dotted version vectors](/dotted-version-vectors/).** One entry per server plus one isolated event, the dot. They fix the lost update of the per-server scheme without per-client entries.
- **[Multi-value registers](/mv-register/).** Keep all concurrent values, each with its vector, and let a later write that has seen them replace them all.
- **[Interval tree clocks](/interval-tree-clocks/).** A version vector for a set of replicas that grows and shrinks, without global identifiers.

## When to use it

Use version vectors when replicas accept writes independently, as in [multi-master replication](/multi-master-replication/), [Dynamo-style](/dynamo-style-replication/) stores and file synchronizers, and you must find the writes that conflict rather than drop one silently. If losing one of two concurrent writes is acceptable, [last-writer-wins](/last-writer-wins/) with a timestamp is simpler. If the replicas are many and short-lived, use a structure that does not need one entry per replica forever.

## Pitfalls

- **Ticking on sync.** A tick on each sync makes two identical copies look concurrent after they meet, which gives false conflicts.
- **A merge without a union of the data.** Line L12 must reconcile the data as well as the vector. Taking the merged vector with only one of the two copies tells the system that the lost update is present.
- **Entries for clients.** Per-client entries make the vectors grow without bound. Pruning old entries can turn an old write into an apparently concurrent one, or hide a conflict.
- **Reused identifiers.** A replica that loses its state and restarts with the same identifier and a zero counter produces updates that look old. Give it a new identifier, or restore its counter.

## Implementations

## History

D. Stott Parker Jr. and his co-authors published version vectors in 1983 to detect mutual inconsistency between copies of files after a network partition. Dynamo-style stores later used per-object vectors to detect concurrent writes. Preguiça, Baquero, Almeida, Fonte and Gonçalves showed in 2010 that one entry per server loses updates when servers act for many clients, and proposed dotted version vectors.

## References
