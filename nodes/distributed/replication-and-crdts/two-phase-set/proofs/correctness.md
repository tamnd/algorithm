---
title: A 2P-Set meets the remove-wins set specification and is a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas. Replica $i$ runs the main block with state $(A_i, R_i)$. In one step a replica runs ADD (line L3), runs REMOVE (lines L4 and L5) when its precondition holds, sends a copy of its state, or runs MERGE (lines L6 and L7) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order.

**Histories.** The causal history $C_i$ is a set of events "add $e$" and "remove $e$". An update at $i$ adds its event. A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$. Write $\mathrm{add}(H)$ for the set of elements with an add event in $H$ and $\mathrm{rem}(H)$ for the set of elements with a remove event in $H$.

**Claim 1 (invariant).** At every time and for every $i$: $A_i = \mathrm{add}(C_i)$, $R_i = \mathrm{rem}(C_i)$ and $R_i \subseteq A_i$. A copy in transit satisfies the same equations with its history.

*Proof.* By induction on the steps. At the start all four sets are empty. A copy is the state and history of its sender at one time. Line L3 adds $e$ to $A_i$ and an add of $e$ to $C_i$, so $A_i = \mathrm{add}(C_i)$ still holds, and $R_i$ does not change, so $R_i \subseteq A_i$ still holds. For REMOVE, line L4 makes sure that $e \in A_i$; line L5 adds $e$ to $R_i$ and a remove of $e$ to $C_i$, so $R_i = \mathrm{rem}(C_i)$ and $R_i \subseteq A_i$ hold. For MERGE of a copy $(A', R', H)$, lines L6 and L7 give $A_i \cup A' = \mathrm{add}(C_i) \cup \mathrm{add}(H) = \mathrm{add}(C_i \cup H)$, the same for $R$, and $R_i \cup R' \subseteq A_i \cup A'$ because $R_i \subseteq A_i$ and $R' \subseteq A'$. $\square$

**Theorem 1 (safety).** LOOKUP$(e)$ at $i$ returns true exactly when $C_i$ holds an add of $e$ and no remove of $e$. In particular a remove of $e$ beats every add of $e$, and an add of $e$ after a remove of $e$ in $C_i$ has no visible effect.

*Proof.* Line L2 returns $e \in A_i \wedge e \notin R_i$, and Claim 1 rewrites it as $e \in \mathrm{add}(C_i) \wedge e \notin \mathrm{rem}(C_i)$. Once a remove of $e$ is in $C_i$ it stays there, since histories only grow. $\square$

**Theorem 2 (semilattice).** Order states by $(A, R) \le (A', R')$ when $A \subseteq A'$ and $R \subseteq R'$. This is a join-semilattice with join $(A \cup A', R \cup R')$. MERGE computes the join, and ADD and REMOVE are inflationary.

*Proof.* Each coordinate is the subset lattice, where union is the least upper bound. In a product order a pair is an upper bound of two pairs exactly when each coordinate is, so the least upper bound is the pair of unions. Hence the join is commutative, associative and idempotent. Lines L6 and L7 compute it. Lines L3 and L5 each add an element to one coordinate, which gives a state above the old one. $\square$

**Theorem 3 (convergence).** If updates stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, then there is a time after which all replicas have the same state, and every LOOKUP returns true exactly for the elements that were added and never removed.

*Proof.* Let $U$ be the finite set of all update events. After the last update, each replica $i$ in the end merges a copy from each $j$ sent after the last update, and then $C_i \supseteq C_j$. Each event is in the history of the replica that made it. After finitely many merges $C_i = U$ for all $i$. By Claim 1 all states are $(\mathrm{add}(U), \mathrm{rem}(U))$, and Theorem 1 gives the lookups. The same follows from Theorem 2 and the CRDT convergence theorem. $\square$

**Termination.** ADD, REMOVE and LOOKUP are single steps. MERGE and COMPARE loop once over finite sets.

**Why the precondition matters.** Without line L4, a replica could remove an element $e$ that is not in $A_i$. Then $R_i \not\subseteq A_i$, and a later ADD$(e)$ anywhere, also one that is not concurrent with the remove but follows it in real time, would have no effect. Claim 1 would still hold for $A$ and $R$, but the remove would affect adds that it never observed. The precondition keeps every remove causally after an add of the same element. $\blacksquare$
