---
title: The false positive rate and the cost of a quotient filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: for a key $x \notin S$, the fingerprint $F(x)$ is uniform on $\{0, \ldots, 2^{q+r} - 1\}$ and independent of the fingerprints of the keys of $S$. Let $n$ be the number of distinct fingerprints stored, at most $|S|$, and $\alpha = n/2^q$.

**Theorem 1.** For each $x \notin S$, $\Pr[\text{QUERY}(x) = \text{true}] \le n/2^{q+r} = \alpha 2^{-r}$.

*Proof.* By Theorem 1 of the correctness proof, QUERY$(x)$ is true exactly when $F(x)$ is one of the stored fingerprints. Fix the stored fingerprints; there are at most $n$ distinct values, and $F(x)$ hits each with probability $2^{-(q+r)}$. The [union bound](/union-bound/) gives the claim. $\square$

**Theorem 2 (cost).** Let $C$ be the number of slots of the cluster that contains slot $f_q(x)$, or 1 if that slot is empty. Then QUERY, INSERT and DELETE of $x$ take $O(C)$ time on the word RAM, and the table takes $2^q (r + 3)$ bits.

*Proof.* Line L2 moves left inside the cluster, and lines L4 to L10 move $b$ and $s$ right inside the cluster, so the query reads at most $3C$ slots. Lines L11 to L17 read and write the slots from $b$ to the empty slot after the cluster, at most $C + 1$ of them, and sorting $E$ is not needed when it is read in order, since the runs are already sorted. $\square$

**Cluster length.** The set of non-empty slots after any sequence of operations equals the set of slots used by [linear probing](/linear-probing/) with hash values $f_q$ of the stored fingerprints: in both, the number of used slots in each interval of slots that starts after an empty slot is determined by the quotients in it. So the cluster lengths have the law of linear probing at load $\alpha$, with expected length $O(1/(1 - \alpha)^2)$ for the cluster of a random slot under ideal hashing, which this page takes from the analysis of linear probing. $\blacksquare$
