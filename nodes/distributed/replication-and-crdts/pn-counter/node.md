---
tag: KN5BQ5
kind: data-structure
slug: pn-counter
name: PN-Counter
aliases:
- positive-negative counter
area: distributed/replication-and-crdts
level: intro
summary: A replicated counter with increment and decrement. It pairs two g-counters, P for increments and N for decrements, and its value is sum(P) minus sum(N).
implements: [crdt]
model: word-ram
complexity:
  vars: {n: the number of replicas}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [g-counter, state-based-crdt, join-semilattice]
see_also: [g-counter, crdt, crdt-convergence-theorem, delta-state-crdt, op-based-crdt, g-set, lww-register]
sources:
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, the counter built from two increment-only counters
  - url: https://inria.hal.science/inria-00555588
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, A comprehensive study of convergent and commutative replicated data types, INRIA RR-7506, 2011
    locator: Section 3.1.3 and Specification 7 (state-based PN-Counter, with the remark that a decrement in a max vector breaks monotonicity), Section 3.1.4 (non-negative counter)
  - paper: doi:10.1109/SRDS.2015.32
    title: Valter Balegas, Diogo Serra, Sérgio Duarte, Carla Ferreira, Marc Shapiro, Rodrigo Rodrigues and Nuno Preguiça, Extending eventually consistent cloud databases for enforcing numeric invariants, SRDS 2015
    locator: pages 31 to 36 (the Bounded Counter, which keeps a lower bound by moving rights between replicas)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the delta form of the positive-negative counter
---

A PN-Counter is a replicated counter that supports increments and decrements. Each of the $n$ replicas keeps two vectors of $n$ natural numbers: $P[j]$ counts the increments made at replica $j$ and $N[j]$ counts the decrements made at replica $j$, as far as this replica knows. The value is $\sum_j P[j] - \sum_j N[j]$, and two states merge by the pointwise maximum of each vector. It is two [g-counters](/g-counter/) side by side, so its states form a [join-semilattice](/join-semilattice/) and replicas converge over a network that loses, repeats and reorders messages.

## In plain words

A g-counter can only go up. To also count down, keep two g-counters. One counts every "plus one" and the other counts every "minus one". Each server writes only in its own slot of each counter. To combine two copies, take the larger number in each slot of each counter. The current count is the total of the plus counter less the total of the minus counter.

The obvious shortcut fails. If a server simply lowers its own slot, then an older copy of that slot still has the higher number. When the copies combine, the larger number wins and the "minus one" disappears. With two counters, every number only grows, so taking the larger number is always safe.

## The abstract type

The PN-Counter implements a replicated integer counter with updates INCREMENT and DECREMENT and the query VALUE. It is a [state-based CRDT](/state-based-crdt/).

**Model.** There are $n$ replicas with fixed, unique ids $1, \ldots, n$. The system is asynchronous. Channels may lose, duplicate and reorder messages, and a message sent infinitely often is received in the end. Replicas may crash and recover with their state on durable storage. A replica sends its whole state from time to time, and the receiver merges it.

**Specification.** Let $C_i$ be the causal history of replica $i$: its own updates and the updates in the history of each state it has merged. VALUE at $i$ returns the number of increments in $C_i$ less the number of decrements in $C_i$. Two replicas with the same causal history have the same state. If updates stop and every replica keeps sending its state to every other, all replicas reach the same history and return the same value. The value can be negative, and no bound on it is kept.

## Representation

Replica $i$ stores two arrays $P[1..n]$ and $N[1..n]$ of natural numbers and its own id. A state is a pair $(P, N)$, and states are ordered by $(P, N) \le (P', N')$ when $P \le P'$ and $N \le N'$ entrywise. This is the product of two copies of the g-counter lattice $(\mathbb{N}^n, \le)$, so it is again a join-semilattice, and its join is the pair of pointwise maxima. The invariant is that $P[j]$ and $N[j]$ are the numbers of increments and decrements of replica $j$ in the causal history.

## Operations

```pseudo id=main
CREATE(n, i)
L1  P ← an array of n natural numbers, all 0          ▷ increments, per replica
L2  N ← an array of n natural numbers, all 0          ▷ decrements, per replica
L3  me ← i

INCREMENT()
L4  P[me] ← P[me] + 1

DECREMENT()
L5  N[me] ← N[me] + 1                                 ▷ a decrement also makes the state larger

VALUE()
L6  return (P[1] + ... + P[n]) − (N[1] + ... + N[n])

MERGE(P', N')                                         ▷ a state received from a replica
L7  for j ← 1 to n do
L8      P[j] ← max(P[j], P'[j])
L9      N[j] ← max(N[j], N'[j])

COMPARE(P', N')
L10 return P[j] ≤ P'[j] and N[j] ≤ N'[j] for every j
```

**Updates.** Lines L4 and L5 each add 1 to an entry that only this replica writes. Both make the state larger in the order, so both are inflationary, which is what the [CRDT convergence theorem](/crdt-convergence-theorem/) asks of an update.

**Value.** Line L6 reads only local state, so it answers at once, also during a partition. It costs $\Theta(n)$, or $\Theta(1)$ if the replica keeps the two sums in variables and updates them in MERGE.

**Merge.** Lines L7 to L9 compute the join. Each entry has a single writer and only grows, so the larger copy of an entry is the newer one.

**Compare.** Line L10 decides the order. If it holds, the other state already holds every update of this one.

## Example

Three replicas $A$, $B$ and $C$ start at zero. $A$ increments twice, $B$ increments once and decrements once, and $C$ decrements once, all at the same time. The true count is $3 - 2 = 1$. A state is written as $P \mid N$.

| step | event | $A$ | $B$ | $C$ | values |
| --- | --- | --- | --- | --- | --- |
| 1 | the five updates | $(2,0,0) \mid (0,0,0)$ | $(0,1,0) \mid (0,1,0)$ | $(0,0,0) \mid (0,0,1)$ | 2, 0, $-1$ |
| 2 | $B$ merges $A$ | same | $(2,1,0) \mid (0,1,0)$ | same | 2, 2, $-1$ |
| 3 | $C$ merges $B$ | same | same | $(2,1,0) \mid (0,1,1)$ | 2, 2, 1 |
| 4 | $A$ merges $C$ twice, then a late copy of its own step 1 state | $(2,1,0) \mid (0,1,1)$ | same | same | 1, 2, 1 |
| 5 | $B$ merges $C$ | same | $(2,1,0) \mid (0,1,1)$ | same | 1, 1, 1 |

**Why one signed vector fails.** Try a single vector $V$ where INCREMENT adds 1 to $V[me]$, DECREMENT subtracts 1, and MERGE takes the pointwise max. With $n = 2$, $A$ increments, so $V_A = (1, 0)$. $B$ merges it and holds $(1, 0)$. Now $A$ decrements: $V_A = (0, 0)$, value 0. Then $A$ merges the copy from $B$: $\max((0,0), (1,0)) = (1, 0)$, value 1. The decrement is lost, although one increment and one decrement were made. The decrement moved the state down in the order, so it is not inflationary, and the join with an older state undoes it. Shapiro et al. make the same point: since merge is a max, a decrement in this vector would have no effect. The PN-Counter on the same run ends at $P = (1, 0)$, $N = (1, 0)$ and value 0.

## Correctness

The invariant is that at every time $P_i[j]$ is the number of increments of replica $j$ in $C_i$ and $N_i[j]$ is the number of decrements of replica $j$ in $C_i$. It is the g-counter invariant twice: the increments of $j$ in any history are the first few increments of $j$, and so are the decrements, so a union of two histories holds as many of each as the larger history, which is what lines L8 and L9 compute. With it, VALUE returns the increments less the decrements in $C_i$, equal histories give equal states, and when all histories are complete all values are equal. Shapiro et al. leave the proof that the PN-Counter is a CRDT to the reader. It is given in full in [the correctness proof](proofs/correctness.md), with the semilattice laws.

## Complexity

| operation | time | messages |
| --- | --- | --- |
| INCREMENT, DECREMENT | $\Theta(1)$ | none |
| VALUE | $\Theta(n)$, or $\Theta(1)$ with kept sums | none |
| MERGE, COMPARE | $\Theta(n)$ | one state of $2n$ numbers |

The state takes $2n$ numbers. A message carries the whole state, even if one entry changed. The [delta-state](/delta-state-crdt/) form sends only the changed entry.

## Variants

- **[Op-based counter](/op-based-crdt/).** Broadcast "+1" or "−1" and add it on delivery. Increments and decrements commute, so causal order is not needed, but each message must arrive exactly once.
- **Delta-state PN-Counter.** An update returns the single changed entry as a delta, and replicas ship joins of deltas (Almeida, Shoker and Baquero).
- **Non-negative and bounded counters.** A PN-Counter can go below zero, and a local check "value > 0 before a decrement" does not stop two replicas from decrementing the last unit at once. Shapiro et al. note that a non-negative counter needs more than local checks. Balegas et al. (2015) give the Bounded Counter: each replica holds rights to decrement, a replica decrements only while it holds rights, and replicas transfer rights to each other, so the bound holds without coordination on each operation.

## When to use it

Use a PN-Counter for counts that go up and down and that each replica must update during a partition, such as the number of items in a shared cart or a vote score, where a short negative or stale value is acceptable. Use a [g-counter](/g-counter/) if the count only grows, since it is half the size. If the value must never pass a bound (stock, account balance), use a bounded counter or a [linearizable](/linearizability/) counter.

## Pitfalls

- **Decrementing in a single vector.** As the example shows, the max of a later merge erases the decrement. Keep decrements in their own vector (line L5), not as a subtraction in $P$.
- **Checking a bound locally.** "Decrement only if the value is positive" is checked against a stale local value. Two replicas can both pass the check and drive the true value below zero.
- **Restarting with an old id and zero state.** As with the g-counter, a replica that lost its state must not reuse its id, or its next updates hide under the larger old entries.
- **Merging by addition.** Adding states counts a duplicate twice. The merge must be the max (lines L8 and L9).

## Implementations

The Python class follows the main block with `# @line` markers for L1 to L10. The module also has the signed single-vector counter of the example, and the tests show how it loses a decrement.

## History

Shapiro, Preguiça, Baquero and Zawirski gave the PN-Counter in 2011, in the SSS paper and as Specification 7 of the INRIA report, as the pair of two increment-only counters. The report also discusses the non-negative counter and why it needs a global invariant. Balegas et al. (2015) gave the Bounded Counter, and Almeida, Shoker and Baquero gave the delta-state form.

## References
