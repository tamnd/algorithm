---
tag: MQEY7J
kind: data-structure
slug: g-counter
name: G-counter
aliases:
- grow-only counter
area: distributed/replication-and-crdts
level: intro
summary: A replicated counter that only increases. Each replica counts its own increments in a vector entry; merge is the pointwise max and the value is the sum.
implements: [crdt]
model: word-ram
complexity:
  vars: {n: the number of replicas}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [state-based-crdt, join-semilattice]
see_also: [pn-counter, crdt, crdt-convergence-theorem, delta-state-crdt, op-based-crdt, vector-clocks, version-vectors, g-set]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, Section 4.1 (integer vectors and counters, the increment-only counter and the counter built from two of them)
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: the section on counters in the catalog of CRDTs (the state-based increment-only counter and the PN-counter)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the δ-counter example (the delta-mutator inc that returns the single entry of the replica)
---

A g-counter is a replicated counter that supports only increments. Each of the $n$ replicas keeps a vector $P$ of $n$ natural numbers, where $P[j]$ is the number of increments made at replica $j$ that this replica knows about. An increment adds 1 to the replica's own entry, the value is the sum of the entries, and two states merge by the pointwise maximum. Because the states form a [join-semilattice](/join-semilattice/) and merge is its join, replicas that exchange states over a network that loses, repeats and reorders messages still end with the same value, which is the total number of increments.

## In plain words

Several servers count the same thing, for example the likes on a post, and each one accepts clicks on its own. A single shared number does not work. If two servers each add one to 5 and then compare, taking the larger number gives 6, but there were two clicks. Adding the numbers fails too, because a copy that arrives twice is counted twice.

The fix is that each server keeps one slot per server. A server writes only in its own slot. To combine two copies, take the larger number in each slot, because a larger number in a slot always means a newer copy of that slot. The count is the total of all slots. Taking the larger number twice gives the same result as taking it once, so repeated, late or out-of-order copies do no harm.

## The abstract type

The g-counter implements a replicated counter with one update, INCREMENT, and one query, VALUE. It is a [state-based CRDT](/state-based-crdt/), and it is the first example of the [CRDT](/crdt/) family.

**Model.** There are $n$ replicas with fixed and known ids $1, \ldots, n$. The system is asynchronous: there is no bound on message delay or on relative speed, and there are no clocks. Channels may lose, duplicate and reorder messages, but a message that is sent infinitely often is received in the end (a fair-lossy channel). Replicas may crash and recover with their state intact, because the state is kept on durable storage; any number $f \le n - 1$ of replicas may be down at a time, and the others keep working. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** Let $I$ be the set of all INCREMENT operations, at all replicas. For a replica $i$, let $C_i \subseteq I$ be the increments in its *causal history*: its own increments and those in the history of each state it has merged.

- *Safety.* VALUE at $i$ returns $|C_i|$. So VALUE never exceeds $|I|$, and it never decreases at a replica. Two replicas with the same causal history have the same state.
- *Liveness.* If increments stop, and every replica keeps sending its state to the others, then every replica reaches $C_i = I$ and returns $|I|$.

So the g-counter has [strong eventual consistency](/strong-eventual-consistency/), not [linearizability](/linearizability/): a read returns a count that may miss recent increments made elsewhere.

## Representation

Replica $i$ stores an array $P[1..n]$ of natural numbers and its own id. The states form the join-semilattice $(\mathbb{N}^n, \le)$, where $P \le Q$ means $P[j] \le Q[j]$ for every $j$, and the join is the pointwise max. The bottom state is the zero vector. The array has the same shape as a [vector clock](/vector-clocks/) or a [version vector](/version-vectors/), but here an entry counts increments, not events.

## Operations

```pseudo id=main
CREATE(n, i)
L1  P ← an array of n natural numbers, all 0
L2  me ← i                                            ▷ the id of this replica

INCREMENT()
L3  P[me] ← P[me] + 1                                 ▷ a replica writes only its own entry

VALUE()
L4  return P[1] + P[2] + ... + P[n]

MERGE(Q)                                              ▷ Q is a state received from a replica
L5  for j ← 1 to n do
L6      P[j] ← max(P[j], Q[j])

COMPARE(Q)
L7  return P[j] ≤ Q[j] for every j                    ▷ the semilattice order
```

**Increment.** Line L3 changes only the entry of the replica that runs it. No other replica writes this entry, so the highest value of $P[i]$ anywhere in the system is the number of increments at $i$, and every copy of $P[i]$ is a past value of it.

**Value.** Line L4 adds the entries. It reads only local state, so it answers at once, also during a network partition.

**Merge.** Lines L5 and L6 compute the join. A larger entry is always a later copy of the same entry, so the max keeps the newer one, and it is the right choice for each entry independently.

**Compare.** Line L7 decides $P \le Q$. If it is true, $Q$ already contains all that $P$ contains, and a replica that has $Q$ does not need $P$.

## Example

Three replicas $A$, $B$ and $C$ start at $(0, 0, 0)$. $A$ increments twice, $B$ once and $C$ once, all at the same time, so there are four increments.

| step | event | $A$ | $B$ | $C$ | values |
| --- | --- | --- | --- | --- | --- |
| 1 | the four increments | $(2, 0, 0)$ | $(0, 1, 0)$ | $(0, 0, 1)$ | 2, 1, 1 |
| 2 | $B$ merges the state of $A$ | $(2, 0, 0)$ | $(2, 1, 0)$ | $(0, 0, 1)$ | 2, 3, 1 |
| 3 | $C$ merges the state of $B$ | $(2, 0, 0)$ | $(2, 1, 0)$ | $(2, 1, 1)$ | 2, 3, 4 |
| 4 | $A$ merges the state of $C$, twice | $(2, 1, 1)$ | $(2, 1, 0)$ | $(2, 1, 1)$ | 4, 3, 4 |
| 5 | $A$ merges a late copy of $B$ from step 2 | $(2, 1, 1)$ | $(2, 1, 0)$ | $(2, 1, 1)$ | 4, 3, 4 |
| 6 | $B$ merges the state of $C$ | $(2, 1, 1)$ | $(2, 1, 1)$ | $(2, 1, 1)$ | 4, 4, 4 |

The duplicate in step 4 and the old state in step 5 change nothing, because $\max(x, x) = x$ and $\max(x, y) = x$ when $y \le x$. In step 3, $C$ learns the increments of $A$ without a message from $A$, through $B$.

Two simpler designs fail on the same run. One integer per replica merged with max ends at $\max(2, 1, 1) = 2$, which loses two increments. One integer merged by addition gives $A$ the value $2 + 4 + 4 = 10$ after step 4, because it counts the duplicate.

## Correctness

The main invariant is that, at every replica $i$ and every time, $P_i[j]$ is the number of increments of replica $j$ in the causal history $C_i$. An increment at $i$ adds one increment of $i$ to $C_i$ and 1 to $P_i[i]$. A merge makes $C_i$ the union of two histories, and the increments of $j$ in each history are the first few increments of $j$, so the union holds as many as the larger of the two, which is what line L6 computes. With the invariant, VALUE returns $|C_i|$, two replicas with the same history have the same vector, and when all histories equal $I$ all values equal $|I|$. The full proof is in [the correctness proof](proofs/correctness.md).

The same result follows from the [CRDT convergence theorem](/crdt-convergence-theorem/): $(\mathbb{N}^n, \max)$ is a join-semilattice, MERGE is its join, and INCREMENT is inflationary, since $P \le P + e_i$.

## Complexity

INCREMENT takes $\Theta(1)$ time. VALUE, MERGE and COMPARE take $\Theta(n)$ time, and the state takes $\Theta(n)$ words. A message carries the whole state, $\Theta(n)$ words, even when only one entry changed. A replica can also keep the sum in a variable and update it in MERGE by the increase of each entry, which makes VALUE $\Theta(1)$.

The space is the cost of tolerating duplication without unique message ids. Each entry is needed: a state that dropped the entry of replica $j$ could not tell a repeated copy of $j$'s increments from new ones.

## Variants

- **[PN-counter](/pn-counter/).** A pair of g-counters, one for increments and one for decrements, with value $\sum P - \sum N$. It supports decrements and is still a join-semilattice, as a product of two.
- **[Op-based counter](/op-based-crdt/).** Each increment is broadcast as the message "+1", and each replica adds 1 per message. Messages are $\Theta(1)$, but the network must deliver each message exactly once, which the state-based form does not need.
- **[Delta-state counter](/delta-state-crdt/).** INCREMENT returns the delta $\{i \mapsto P[i]\}$, a state with a single entry, and replicas send joins of deltas in place of the whole vector. The join of all deltas is the same state, and messages are $O(1)$ words when only one entry changed.
- **Sparse map.** Keep a map from replica ids to counts in place of an array, with a missing id read as 0. This allows replicas to join without a fixed $n$.

## When to use it

Use a g-counter when many replicas must count events that only add, such as page views, likes or retries, and each replica must accept increments while it is cut off from the others. Use a PN-counter if the count can go down. Do not use a g-counter when a read must see every earlier increment (a ticket number, a stock level that must not go below 0); that needs a [linearizable](/linearizability/) counter and [consensus](/consensus-problem/), and is not available during a partition, as the [CAP theorem](/cap-theorem/) shows.

## Pitfalls

- **Merging by addition.** Adding states counts a duplicate or a resent state again. Merge must be idempotent, which the max is and addition is not.
- **One shared integer with max.** Concurrent increments on different replicas collapse into one, as in the example. Each replica needs its own entry.
- **Restarting from zeros.** A replica that loses its state and keeps its old id starts again at $P[i] = 0$. The other replicas still hold a larger $P[i]$, so its next increments are hidden by the max and lost. Keep the state on durable storage, or give a restarted replica a new id.
- **Writing another replica's entry.** If replica $i$ increments $P[j]$ for $j \ne i$, two replicas write the same entry concurrently, and the max loses one of the writes.
- **Unbounded ids.** Each replica id that ever incremented keeps an entry for ever. Systems with many short-lived replicas need a way to retire entries, which the plain g-counter does not have.

## Implementations

The Python class follows the main block, with the `# @line` markers on the lines of L1 to L7. The module also has the op-based counter and the two failing counters of the example.

## History

Shapiro, Preguiça, Baquero and Zawirski described the increment-only counter in 2011, both in the SSS paper that defined CRDTs and in the INRIA report with the catalog of CRDTs. They built it from the vector of integers with pointwise max, and noted that a vector where each process increments only its own entry is a vector clock. The PN-counter, as a pair of two of them, is in the same papers. Almeida, Shoker and Baquero (2015, 2018) gave the delta-state counter, which sends one entry in place of the vector. Counters of this kind are used in production stores, for example the counters of Riak.

## References
