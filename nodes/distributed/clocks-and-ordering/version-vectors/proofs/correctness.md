---
title: Version vectors compare the sets of updates in two copies
proves: [correctness]
status: full
---

We use the model of the page: $n$ replicas $r_1, \ldots, r_n$ of one object, asynchronous and with no failure assumption. A run is a sequence of operations UPDATE at one replica and SYNC between two replicas. Let $U_k$ be the sequence of updates made by $r_k$, in the order it made them. For a replica $r$ at a point of the run, let $H_r$ be the set of updates that its copy contains: an update adds itself to the copy of the replica that makes it, a copy of a state copies its set, and a reconciliation of two concurrent copies takes the union. So $H_r$ is the causal history of the copy. Write $V_r$ for the version vector of $r$.

**Lemma 1 (invariant).** At every point of the run and for all $r$ and $k$:

1. $H_r$ never loses an element, and $H_{r_k}$ contains all of $U_k$ made so far.
2. $H_r \cap U_k$ is a prefix of $U_k$.
3. $V_r[k] = |H_r \cap U_k|$.

*Proof.* By induction over the operations. At the start all sets are empty and all vectors are zero. Assume the three claims before an operation.

UPDATE at $r_i$ (line L2) adds a new update $u$ to $H_{r_i}$ and 1 to $V_{r_i}[i]$. By claim 1, $H_{r_i}$ already holds all earlier updates of $r_i$, so $H_{r_i} \cap U_i$ is all of $U_i$ before $u$, and with $u$ it is again a prefix of $U_i$, now one longer. Other sets and vectors do not change.

SYNC of $a$ and $b$ (lines L9 to L12). By claims 2 and 3, for each $k$ the sets $H_a \cap U_k$ and $H_b \cap U_k$ are two prefixes of $U_k$ of lengths $V_a[k]$ and $V_b[k]$. So $H_a \cap U_k \subseteq H_b \cap U_k$ if and only if $V_a[k] \le V_b[k]$, and taking this over all $k$:

$$H_a \subseteq H_b \iff V_a \le V_b \text{ in every entry}. \tag{$*$}$$

If line L10 runs, then $V_a \le V_b$, so $H_a \subseteq H_b$ by $(*)$, and $a$ takes the set and the vector of $b$. Line L11 is the same with the roles swapped. If line L12 runs, both get $H_a \cup H_b$ and the entrywise maximum of the vectors. The union of two prefixes of $U_k$ is the longer prefix, so its size is the maximum of the two sizes. In each case the new sets contain the old ones, which gives claim 1, and claims 2 and 3 hold for the new state. $\square$

**Theorem.** At every point of the run, for any two replicas $a$ and $b$, COMPARE$(V_a, V_b)$ returns EQUAL if $H_a = H_b$, BEFORE if $H_a \subsetneq H_b$, AFTER if $H_b \subsetneq H_a$, and CONCURRENT if neither set contains the other. SYNC never discards an update.

*Proof.* By $(*)$ in both directions, $V_a = V_b$ if and only if $H_a = H_b$, and $V_a \le V_b$ if and only if $H_a \subseteq H_b$. Lines L5 to L8 test these conditions in this order, so each answer matches the claim. For the second claim, line L10 replaces $H_a$ by a superset, line L11 replaces $H_b$ by a superset, and line L12 replaces both by their union. $\blacksquare$

So a conflict is reported exactly when each copy holds an update that the other lacks, which is the mutual inconsistency of Parker et al. No conflict is missed, and no false conflict is reported.
