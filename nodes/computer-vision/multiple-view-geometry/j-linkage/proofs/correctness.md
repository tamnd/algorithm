---
title: J-linkage ends with a partition of the points in which every cluster of two or more points shares a hypothesis and no two clusters share one
proves: [correctness]
status: full
---

We use the notation of the page. The data are $D = \{x_1, \ldots, x_n\}$ with $n \ge 1$, the hypotheses are $H = \{h_1, \ldots, h_M\}$, and the preference set of a point is $P(x) = \{h \in H : r(h, x) < \varepsilon\}$. For finite sets $A$ and $B$ the Jaccard distance is $d_J(A, B) = (|A \cup B| - |A \cap B|)/|A \cup B|$, with $d_J(\emptyset, \emptyset) = 1$. The model of computation is the real RAM.

**Claim.** After line L4, the loop of lines L6 to L9 ends after at most $n - 1$ merges, and the clusters $C$ it returns have these properties. (a) $C$ is a partition of $D$. (b) Each cluster $A$ has the preference set $P(A) = \bigcap_{x \in A} P(x)$. (c) If $|A| \ge 2$, then $P(A) \ne \emptyset$: some hypothesis has residual below $\varepsilon$ at every point of $A$. (d) For two distinct clusters $A$ and $B$, $P(A) \cap P(B) = \emptyset$: no hypothesis is preferred by all points of $A$ and all points of $B$.

**Lemma 1.** For finite sets $A$ and $B$, $d_J(A, B) < 1$ if and only if $A \cap B \ne \emptyset$.

*Proof.* If $A \cup B = \emptyset$, then $d_J = 1$ and $A \cap B = \emptyset$. Otherwise $d_J(A, B) = 1 - |A \cap B|/|A \cup B|$, which is less than 1 exactly when $|A \cap B| > 0$. $\square$

**Lemma 2 (invariant).** At each test of line L8, properties (a), (b) and (c) hold for the current clusters.

*Proof.* Line L5 makes the clusters $\{x\}$ with $P(\{x\}) = P(x)$, so (a) and (b) hold, and (c) is empty. Suppose they hold, and line L9 merges $A$ and $B$. It removes the two clusters and adds $A \cup B$. Since $A$ and $B$ are disjoint and the other clusters are not changed, (a) holds. The new preference set is $P(A) \cap P(B) = \bigcap_{x \in A} P(x) \cap \bigcap_{x \in B} P(x) = \bigcap_{x \in A \cup B} P(x)$, so (b) holds. Line L9 runs only if line L8 did not stop, so $d_J(P(A), P(B)) < 1$, and by Lemma 1, $P(A) \cap P(B) \ne \emptyset$. This is $P(A \cup B)$, so (c) holds for the new cluster. The other clusters keep (b) and (c). $\square$

**Lemma 3 (termination).** The loop makes at most $n - 1$ merges.

*Proof.* There are $n$ clusters at the start, each merge lowers the number by 1, and line L8 stops when fewer than 2 clusters are left. $\square$

**Lemma 4 (stopping condition).** Property (d) holds for the returned clusters.

*Proof.* The loop stops at line L8 in one of two cases. If fewer than 2 clusters are left, (d) holds trivially. Otherwise the least Jaccard distance over all pairs is at least 1, so every pair has distance 1. By Lemma 1, $P(A) \cap P(B) = \emptyset$ for every pair. $\square$

Lemmas 2, 3 and 4 give the claim. Lines L10 and L11 then fit one model to each cluster with at least $m_{\min}$ points. By (c), the points of such a cluster all lie within $\varepsilon$ of at least one common hypothesis, so a model fitted to them explains them all if that hypothesis is close to the true model. By (d), no hypothesis explains all the points of two clusters, so the method does not keep two copies of the same structure as long as a hypothesis close to it is in $H$.

**Remark (what is not proved).** The claim holds for any set of hypotheses. Whether the clusters are the true structures depends on the sampling: a structure is found only if $H$ contains hypotheses that fit it. Toldo and Fusiello support this with experiments, and the locality sampling makes such hypotheses more likely. The merge order is greedy, so the result is a local choice, not the best partition by any global cost.
