---
tag: QRFZEK
kind: concept
slug: delta-state-crdt
name: Delta-state CRDT
aliases:
- delta CRDT
- delta-state replication
area: distributed/replication-and-crdts
level: advanced
summary: A state-based CRDT whose updates return small deltas in the same lattice; replicas ship joins of deltas, not full states, and still tolerate loss and duplicates.
prereqs: [state-based-crdt, join-semilattice]
see_also: [op-based-crdt, crdt, crdt-convergence-theorem, g-counter, g-set, or-set, anti-entropy, causal-consistency]
sources:
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173; in the arXiv version 1603.01529, Definitions 1 to 3 (delta-mutator, delta-group, delta-CRDT), Section 4.1 (delta-state decomposition), Proposition 1, Algorithm 1, Definitions 4 to 6 (delta-interval, causal delta-merging condition), Proposition 2, Algorithm 2 and Proposition 3
  - paper: "Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Efficient state-based CRDTs by delta-mutation, NETYS 2015, Lecture Notes in Computer Science 9466, Springer"
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Efficient state-based CRDTs by delta-mutation, NETYS 2015
    locator: the first presentation of delta-mutators and the two anti-entropy algorithms
  - paper: "Vitor Enes, Paulo Sérgio Almeida, Carlos Baquero and João Leitão, Efficient synchronization of state-based CRDTs, ICDE 2019"
    title: Vitor Enes, Paulo Sérgio Almeida, Carlos Baquero and João Leitão, Efficient synchronization of state-based CRDTs, IEEE ICDE 2019
    locator: join decompositions and optimal deltas, the two inefficiencies of classic delta-based synchronization (back-propagation of deltas and redundant parts of received deltas), and the experimental comparison with state-based and op-based synchronization
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, Lecture Notes in Computer Science 6976, Springer
    locator: Section 2.3 (state-based objects and Theorem 1, which delta-CRDTs inherit)
---

A delta-state CRDT is a [state-based CRDT](/state-based-crdt/) whose update operations return a *delta*: a small element of the same [join-semilattice](/join-semilattice/) that holds just the change. A replica joins the delta into its own state and later ships joins of deltas, not its whole state, to the other replicas. Almeida, Shoker and Baquero introduced the idea in 2015 to get small messages, as in [op-based CRDTs](/op-based-crdt/), while keeping the weak network assumptions of state-based ones: a delta is a state, so it can be lost, duplicated and reordered and joined again. With an anti-entropy algorithm that sends contiguous runs of deltas and waits for acknowledgements, every reachable state is a state of the full-state CRDT, so the convergence and causal guarantees carry over.

## In plain words

A state-based CRDT keeps copies in agreement by sending whole copies around and merging them. That is safe, because merging the same copy twice or in a different order does no harm, but it is wasteful when the data is large and each change is small.

A delta-state CRDT sends only the changed part. The changed part has the same shape as the data, for example a set with one new item, so the receiver merges it in exactly as it would merge a whole copy. Lost or repeated pieces still do no harm.

There is one catch. If a replica receives a later piece but missed an earlier one, its copy can show a change without the changes that came before it. A careful sending rule, with numbered pieces and acknowledgements, prevents that.

## The idea

**Delta-mutators.** Let $(S, \sqcup)$ be the state lattice of a state-based CRDT with update functions (mutators) $m$. A *delta-mutator* $m^\delta$ returns an element of $S$ such that
$$m(X) = X \sqcup m^\delta(X) \quad \text{for every state } X.$$
This is a *delta-state decomposition* of $m$. Every mutator decomposes trivially, with $m^\delta = m$, since $m$ is inflationary; the point is to find a much smaller delta. A delta-mutator need not be inflationary itself, because the replica always joins its output into the current state.

| type | state | full mutator | delta-mutator |
| --- | --- | --- | --- |
| [g-counter](/g-counter/) | map replica $\to \mathbb{N}$, pointwise max | the whole map with entry $i$ one higher | $\{i \mapsto X(i) + 1\}$ |
| [g-set](/g-set/) | set, union | $X \cup \{e\}$ | $\{e\}$ |
| [OR-set](/or-set/), add | dots and a causal context | the whole new state | the new dot for $e$, and a context with that dot |
| OR-set, remove | as above | the whole new state | no dots, and a context with the removed dots |

A *delta-group* is a join of deltas. A full state is a delta-group, and a join of delta-groups is again one, so a replica can batch deltas, forward deltas it received, or fall back to its full state, all with the same join.

**Convergence (Proposition 1).** Every state is the join of the delta-mutations that reached it. So if each delta-mutation produced anywhere is joined at least once into every replica, directly or inside a delta-group, all replicas end equal. The proof is the ACI laws of the join; delivery order and duplicates do not matter. Algorithm 1 of the paper does this: each replica keeps a delta-group $D$ of recent deltas and periodically sends either $D$ or its full state.

**Causal merging (Definitions 4 to 6, Proposition 2).** Proposition 1 gives eventual convergence only. A full-state CRDT also gives per-object causal consistency: a state that reflects an update reflects every update its source had seen. A delta does not carry that past. If replica $i$ receives the delta of a later update and misses an earlier one, its state reflects the later update without its past, and the state is not one that the full-state CRDT could reach.

The fix numbers the deltas. Replica $j$ joins deltas $d_j^0, d_j^1, \ldots$ in order, so its states are $X_j^{k+1} = X_j^k \sqcup d_j^k$. A *delta-interval* is $\Delta_j^{a,b} = d_j^a \sqcup \cdots \sqcup d_j^{b-1}$. The *causal delta-merging condition* says: replica $i$ joins $\Delta_j^{a,b}$ only when $X_i \sqsupseteq X_j^a$. Then $X_i \sqcup \Delta_j^{a,b} = X_i \sqcup X_j^b$, which is exactly the merge of a full state of $j$. By induction over the run, every state equals a state of an execution of the full-state CRDT, so the [CRDT convergence theorem](/crdt-convergence-theorem/) and causal consistency carry over.

**Algorithm 2 (anti-entropy with acknowledgements).** Each replica $i$ keeps, on durable storage, its state $X_i$ and a counter $c_i$, and, in volatile memory, a map $D_i$ from sequence numbers to deltas and a map $A_i$ of acknowledgements from each neighbour.

1. On a local update, compute $d = m^\delta(X_i)$, set $X_i \leftarrow X_i \sqcup d$, store $D_i[c_i] \leftarrow d$, and increment $c_i$.
2. On receiving $(\textit{delta}, d, n)$ from $j$: if $d \not\sqsubseteq X_i$, join it, store it in $D_i$ under $c_i$, and increment $c_i$. In all cases reply $(\textit{ack}, n)$.
3. On receiving $(\textit{ack}, n)$ from $j$: set $A_i[j] \leftarrow \max(A_i[j], n)$.
4. Periodically pick a neighbour $j$. If $D_i$ is empty or its smallest key exceeds $A_i[j]$, the needed deltas are gone, so send the full state $X_i$. Otherwise send $\bigsqcup \{D_i[l] : A_i[j] \le l < c_i\}$. In both cases send only if $A_i[j] < c_i$, and tag the message with $c_i$.
5. Periodically delete the deltas that every neighbour has acknowledged.

A neighbour acknowledges $n$ only after joining an interval that ends at $n$, so the next interval it receives from $i$ starts at a point it has already reached. After a crash, $D_i$ and $A_i$ are lost, and the next send to each neighbour is the full state; $c_i$ must be durable, or a late acknowledgement from before the crash could make $i$ skip deltas made after it.

**Join decompositions and optimal deltas.** In many lattices every state is the join of *join-irreducible* elements, such as single entries of a map or single elements of a set. Enes, Almeida, Baquero and Leitão (2019) use this to compute, for states $a$ and $b$, the smallest delta $\Delta(a, b)$ with $b \sqcup \Delta(a, b) = a \sqcup b$: the join of the irreducible parts of $a$ that are not below $b$. They also found that classic delta-based synchronization can send about as much as full-state synchronization, for two reasons: a replica sends deltas back to the replica it got them from, and it stores and forwards the parts of a received delta that it already had. Their fixes are to skip deltas that came from the target (avoid back-propagation) and to store only $\Delta(d, X_i)$ for a received $d$ (remove redundant state). Both keep the causal delta-merging condition, because the parts they drop are already below the receiver's state.

## Examples

- **Counter.** The delta of an increment at replica $i$ is the single entry $\{i \mapsto X(i) + 1\}$. Unlike an op-based "add 1", this delta is idempotent: joining it twice changes nothing, because the join is a max.
- **Set.** The delta of `add(e)` is $\{e\}$. A delta-group of ten additions is a set of ten elements.
- **Broken variant.** A sender that ignores acknowledgements and ships only its newest delta violates the causal delta-merging condition. With a g-set, the implementation finds runs in which a replica joins an interval into a state below the start of the interval, so the replica holds a later element without an earlier one that its source had.

**Measured traffic.** The implementation runs Algorithm 2 on a network that loses 20% of messages, duplicates 20% and reorders all of them, with crashes that wipe the delta buffers. In 500 random runs of a g-counter and a g-set, every state at every step equals the join of the full states right after the updates it reflects, every interval is joined only into a state above its start, and all replicas end equal. It also counts the encoded bytes of every delta and acknowledgement, against full-state messages for the same sends:

| setting (5 runs each) | delta bytes | full-state bytes | ratio |
| --- | --- | --- | --- |
| g-set, 3 replicas, no loss, Algorithm 2 | 48505 | 112011 | 0.43 |
| g-set, 3 replicas, no loss, with both optimizations | 16217 | 112011 | 0.14 |
| g-set, 4 replicas, lossy, Algorithm 2 | 152922 | 157340 | 0.97 |
| g-set, 4 replicas, lossy, with both optimizations | 59370 | 157340 | 0.38 |
| g-counter, 4 replicas, lossy, with both optimizations | 17839 | 16071 | 1.11 |

The set gains most, since its full state grows with every update while each delta stays one element. On a lossy network, plain Algorithm 2 gains little, because deltas bounce back to their source and lost acknowledgements make each interval long; this matches the finding of Enes et al. that classic delta-based synchronization can cost as much as full states. A counter with four replicas gains nothing: its full state is four numbers, smaller than the acknowledgements.

## Where it is used

- **Akka Distributed Data** replicates its counters, sets, maps and registers with delta propagation and falls back to full states when needed.
- **Reference implementations.** Baquero's delta-enabled-crdts library gives delta-mutators for counters, sets, maps and registers, including the optimized OR-set with dots and causal contexts.
- **Large maps and sets** in geo-replicated stores, where shipping the full state of a big map for each small change would dominate the traffic, while op-based replication would require exactly-once causal delivery.

## References
