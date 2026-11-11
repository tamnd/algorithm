---
title: A G-Set holds exactly the elements added in its causal history, and union makes it a CRDT
proves: [correctness, invariant, termination]
status: full
---

**Setting.** There are $n$ replicas. Replica $i$ runs the main block with state $A_i$. In one step a replica runs ADD (line L2), sends a copy of its state, or runs MERGE (line L4) on a copy that some replica sent earlier. Copies may be lost, merged more than once and merged in any order. A crash with recovery of the durable state does not change $A_i$.

**Histories.** The causal history $C_i$ is a set of add events. It starts empty. ADD$(e)$ at $i$ adds a new event "add $e$". A MERGE at $i$ of a copy sent when the sender had history $H$ sets $C_i \leftarrow C_i \cup H$. Write $\mathrm{el}(H)$ for the set of elements added by the events in $H$.

**Claim 1 (invariant).** At every time, $A_i = \mathrm{el}(C_i)$ for every $i$, and every copy $(B, H)$ in transit has $B = \mathrm{el}(H)$.

*Proof.* By induction on the steps. At the start $A_i = \varnothing = \mathrm{el}(\varnothing)$. A copy is the state and history of its sender at one time, so it inherits the equation. Line L2 maps $A_i$ to $A_i \cup \{e\}$ and $C_i$ to $C_i \cup \{\text{add } e\}$, and $\mathrm{el}$ of the new history is $\mathrm{el}(C_i) \cup \{e\}$. Line L4 maps $A_i$ to $A_i \cup B$ and $C_i$ to $C_i \cup H$, and $\mathrm{el}(C_i \cup H) = \mathrm{el}(C_i) \cup \mathrm{el}(H) = A_i \cup B$. Other steps do not change $A_i$ or $C_i$. $\square$

**Theorem 1 (safety).** LOOKUP$(e)$ at $i$ returns true exactly when an ADD$(e)$ is in $C_i$, and two replicas with equal histories have equal states.

*Proof.* Line L3 returns $e \in A_i$, and by Claim 1 $A_i = \mathrm{el}(C_i)$. The second part follows because $A_i$ is a function of $C_i$. $\square$

**Theorem 2 (semilattice).** On the finite subsets of the element universe ordered by $\subseteq$, the least upper bound of $A$ and $B$ is $A \cup B$. Hence $\cup$ is commutative, associative and idempotent, MERGE computes the join, and ADD is inflationary.

*Proof.* $A \cup B$ contains $A$ and $B$. Any set that contains both $A$ and $B$ contains every element of $A \cup B$. So $A \cup B$ is the least upper bound. A binary operation that returns least upper bounds is commutative and idempotent, and associative because $(A \cup B) \cup C$ and $A \cup (B \cup C)$ are both the least upper bound of $\{A, B, C\}$. Line L4 computes $A \cup B$, and line L2 maps $A$ to $A \cup \{e\} \supseteq A$. $\square$

**Theorem 3 (convergence).** If adds stop and every replica sends its state to every other replica infinitely often over fair-lossy channels, then there is a time after which every $A_i$ equals the set of all added elements.

*Proof.* Let $E$ be the finite set of all add events. After the last add, for each pair $i, j$, some copy from $j$ is merged at $i$, and then $C_i \supseteq C_j$; histories never shrink. Each event is in the history of the replica that made it. After the latest of these finitely many merges, $C_i = E$ for every $i$, and by Claim 1 $A_i = \mathrm{el}(E)$. $\square$

**Termination.** ADD and LOOKUP are single steps. MERGE and COMPARE loop once over a finite set.

**Remark on remove.** No operation removes an element, and this is needed: an operation that maps $A$ to $A \setminus \{e\}$ is not inflationary, and a later merge with any state that holds $e$ puts $e$ back, so Claim 1 would fail for any specification in which the remove has an effect. $\blacksquare$
