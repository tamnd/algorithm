---
title: A PN-Counter returns increments less decrements of its causal history, and it is a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas with ids $1, \ldots, n$. Replica $i$ runs the main block with state $(P_i, N_i)$. A run is a sequence of steps. In one step a replica runs INCREMENT (line L4) or DECREMENT (line L5), or sends a copy of its state, or runs MERGE (lines L7 to L9) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order. A crash with recovery of the durable state does not change the state.

**Names and histories.** Name the $k$-th increment at replica $j$ as $(+, j, k)$ and the $k$-th decrement at $j$ as $(-, j, k)$. The causal history $C_i$ starts empty. An update at $i$ adds its name. A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$. For a set $H$ of names write $H^{+}_j = \{k : (+, j, k) \in H\}$ and $H^{-}_j = \{k : (-, j, k) \in H\}$.

**Claim 1 (prefixes).** At every time, for all $i$ and $j$, $(C_i)^{+}_j$ and $(C_i)^{-}_j$ are prefixes $\{1, \ldots, m\}$ of the naturals, and $(C_i)^{+}_i$ and $(C_i)^{-}_i$ hold all updates made at $i$ so far.

*Proof.* By induction on the steps. At the start all sets are empty. The $k$-th increment at $i$ adds $(+, i, k)$ to a set that is $\{1, \ldots, k-1\}$ by the hypothesis, so it becomes $\{1, \ldots, k\}$; the decrement case is the same. A MERGE replaces each set by its union with the matching set of an older history, which is a prefix by the hypothesis, and the union of two prefixes is the longer prefix. For $j = i$ the older history holds only updates of $i$ made before the copy was sent, which are already in $C_i$. Steps of other replicas do not change $C_i$. $\square$

**Claim 2 (main invariant).** At every time, for all $i$ and $j$, $P_i[j] = |(C_i)^{+}_j|$ and $N_i[j] = |(C_i)^{-}_j|$. A copy carries a state and a history that satisfy the same equations.

*Proof.* By induction on the steps. At the start all values are 0. A copy is the state and history of its sender at one time, so it inherits the equations. Line L4 adds 1 to $P_i[i]$ and adds one name to $(C_i)^{+}_i$, and changes nothing else. Line L5 is the same for $N_i[i]$ and $(C_i)^{-}_i$. In a MERGE of a copy $(P', N', H)$, line L8 sets $P_i[j]$ to $\max(P_i[j], P'[j])$. By the hypothesis and Claim 1 these are the lengths $a$ and $b$ of two prefixes, and the union of the prefixes has length $\max(a, b)$. Line L9 is the same for $N$. Each round of the loop of line L7 handles one $j$, and the rounds do not interact. $\square$

**Theorem 1 (safety).** VALUE at replica $i$ returns $|\{\text{increments in } C_i\}| - |\{\text{decrements in } C_i\}|$. Two replicas with the same causal history have the same state.

*Proof.* Line L6 returns $\sum_j P_i[j] - \sum_j N_i[j]$. By Claim 2 this is $\sum_j |(C_i)^{+}_j| - \sum_j |(C_i)^{-}_j|$, and the sets $(C_i)^{+}_j$ for different $j$ partition the increments of $C_i$, and the same holds for decrements. By Claim 2 the state is a function of the history. $\square$

**Theorem 2 (semilattice).** Let $S = \mathbb{N}^n \times \mathbb{N}^n$ with $(P, N) \le (P', N')$ when $P \le P'$ and $N \le N'$ entrywise, and let $(P, N) \sqcup (P', N') = (\max(P, P'), \max(N, N'))$, with max taken entrywise. Then $(S, \le)$ is a join-semilattice with join $\sqcup$, MERGE computes $\sqcup$, and INCREMENT and DECREMENT are inflationary.

*Proof.* On $\mathbb{N}$, $\max$ is the least upper bound for the usual order. For vectors, $\max(P, P')$ is above both, and every vector above both is above it entry by entry, so it is the least upper bound in $\mathbb{N}^n$. In a product order an upper bound of two pairs is a pair of upper bounds, so the least upper bound is the pair of least upper bounds, which is $\sqcup$. Hence $\sqcup$ is commutative, associative and idempotent. Lines L7 to L9 compute $\sqcup$ entry by entry. Line L4 maps $(P, N)$ to $(P + e_{me}, N) \ge (P, N)$, and line L5 maps it to $(P, N + e_{me}) \ge (P, N)$, where $e_{me}$ is the unit vector. $\square$

**Theorem 3 (convergence).** Suppose that updates stop after some time, and that every replica sends its state to every other replica infinitely often over fair-lossy channels. Then there is a time after which all replicas have the same state, and VALUE returns the total number of increments less the total number of decrements at every replica.

*Proof.* Let $U$ be the finite set of all updates and let $T$ be a time after the last one. For each pair $i, j$, some copy sent by $j$ after $T$ is merged at $i$, and then $C_i$ contains $C_j$, which by Claim 1 holds all updates made at $j$. Histories never shrink. After the latest of these finitely many merges, $C_i = U$ for every $i$. By Theorem 1 all states are equal and the value is the stated difference. The same conclusion follows from Theorem 2 and the [CRDT convergence theorem](/crdt-convergence-theorem/). $\square$

**Termination.** INCREMENT and DECREMENT run one step. VALUE, MERGE and COMPARE run loops of $n$ rounds with a constant number of steps each.

**Where the two vectors matter.** If decrements subtract from $P[me]$, the update maps $P$ to $P - e_{me}$, which is below $P$ in the order, so it is not inflationary, and Claim 2 fails: after $P_i[i]$ goes down, a merge with an older copy of $P_i[i]$ restores the larger number and the decrement is lost. The run in the Example section of the page does this with $n = 2$. Keeping decrements in $N$ makes every update inflationary, which is the property the proof uses in Theorem 2. $\blacksquare$
