---
title: An LWW-Element-Set meets the timestamp specification and is a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas. Replica $i$ runs the main block with maps $\mathit{add}_i$ and $\mathit{rem}_i$, where a missing key reads as $-\infty$. In one step a replica runs ADD$(e, t)$ (line L2), REMOVE$(e, t)$ (line L3), sends a copy of its state, or runs MERGE (lines L7 and L8) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order. Timestamps come from a totally ordered set; nothing else about them is assumed.

**Histories.** The causal history $C_i$ is a set of events $(\mathrm{add}, e, t)$ and $(\mathrm{rem}, e, t)$. An update at $i$ adds its event. A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$. For a history $H$ write $\alpha_H(e) = \max\{t : (\mathrm{add}, e, t) \in H\}$ and $\rho_H(e) = \max\{t : (\mathrm{rem}, e, t) \in H\}$, with $\max \varnothing = -\infty$.

**Claim 1 (invariant).** At every time, for every $i$ and every element $e$: $\mathit{add}_i[e] = \alpha_{C_i}(e)$ and $\mathit{rem}_i[e] = \rho_{C_i}(e)$. A copy in transit satisfies the same equations with its history.

*Proof.* By induction on the steps. At the start both sides are $-\infty$. A copy is the state and history of its sender at one time. Line L2 sets $\mathit{add}_i[e]$ to $\max(\alpha_{C_i}(e), t)$, which is $\alpha$ of $C_i$ with the new event; no other entry changes, and no other $\alpha$ or $\rho$ changes. Line L3 is the same for $\mathit{rem}$. For MERGE of a copy with history $H$, line L7 sets each $\mathit{add}_i[e]$ to $\max(\alpha_{C_i}(e), \alpha_H(e))$, and the largest add timestamp of $e$ in $C_i \cup H$ is the larger of the two largest ones. Keys missing from the copy have $\alpha_H(e) = -\infty$ and keep their value. Line L8 is the same for $\mathit{rem}$. $\square$

**Theorem 1 (safety).** LOOKUP$(e)$ at $i$ returns true when $\alpha_{C_i}(e) > \rho_{C_i}(e)$, false when $\alpha_{C_i}(e) < \rho_{C_i}(e)$, false when no add of $e$ is in $C_i$, and the bias when the two are equal and finite.

*Proof.* By Claim 1, line L4 returns false exactly when no add of $e$ is in $C_i$. Otherwise line L5 returns the comparison when the two values differ, and line L6 returns the bias when they are equal. $\square$

**Theorem 2 (semilattice).** Let the state space be the pairs of maps from elements to timestamps extended with $-\infty$, ordered entrywise. Then it is a join-semilattice whose join is the entrywise maximum, MERGE computes the join, and ADD and REMOVE are inflationary.

*Proof.* A totally ordered set with $\max$ is a join-semilattice. A product of join-semilattices under the entrywise order is a join-semilattice with the entrywise join, because a tuple is an upper bound of two tuples exactly when each entry is. Hence the join is commutative, associative and idempotent. Lines L7 and L8 apply $\max$ to each entry of the received state, and entries not in the received state are joined with $-\infty$, which leaves them as they are. Lines L2 and L3 replace one entry by a value at least as large. $\square$

**Theorem 3 (convergence).** If updates stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, then there is a time after which all replicas have the same state and give the same answer to every LOOKUP.

*Proof.* As for the G-Set: after the last update, each replica in the end merges a copy from every other replica sent after the last update, after which all histories equal the set of all events. By Claim 1 the states are equal, and LOOKUP depends only on the state. $\square$

**Termination.** ADD, REMOVE and LOOKUP are a constant number of steps. MERGE loops once over the finite maps of the received state.

**What the proof does not give.** Theorems 1 to 3 hold for any total order of timestamps. They say nothing about whether the winner is the update that happened last in real time. If two updates are causally ordered and the later one has the smaller timestamp, which a slow clock can cause, the earlier update wins at every replica. Only timestamps that respect causality, such as Lamport clocks, make every causally later update win. $\blacksquare$
