---
title: BIRCH keeps exact summaries within its memory bound, and phase 4 does not raise the sum of squares
proves: [correctness]
status: full
---

We use the pseudocode of the page and the facts about clustering features proved for the [clustering feature tree](/clustering-feature-tree/): a CF $(N, \mathrm{LS}, \mathrm{SS})$ of a set is additive over disjoint unions, and insertion keeps the leaf entries a partition of the inserted points (or inserted CFs) with radius at most $T$. The points are in $\mathbb{R}^d$, and $\mathrm{SSE}(P) = \sum_{x \in P}\|x - \mu_P\|^2 = \mathrm{SS} - \|\mathrm{LS}\|^2/N$. BIRCH is a heuristic for the [k-means problem](/k-means-problem/); the claims below are about its bookkeeping and its last step, not about the optimum.

**Lemma 1 (phase 1 summaries).** After each step of phase 1, the leaf entries of the tree are the CFs of a partition of the points read so far.

*Proof.* Line L2 inserts the CF of one point, which keeps the claim by the CF tree theorem. A rebuild (line L4) inserts the old leaf entries into an empty tree; each old entry is the CF of a part, and a merge of two entries is the CF of the union of their parts by additivity. So the new leaf entries are the CFs of a coarser partition. $\square$

**Lemma 2 (the memory bound and termination).** Let $M \ge 1$. The loop of line L3 stops, and then the tree has at most $M$ leaf entries.

*Proof.* The loop stops only when the bound holds. The new threshold $t'$ of line L4 satisfies $t' > t$ for the old threshold $t = T^2$, and $t' \ge 2t$; if $t = 0$ then $t'$ is the least positive squared radius of a merge of two entries. So after finitely many rebuilds $t' \ge \Delta^2$, where $\Delta$ is the largest distance between two points read so far. For any nonempty set $S$ of these points and any $y \in S$, $R^2(S) = \frac{1}{|S|}\sum_{x \in S}\|x - \mu_S\|^2 \le \frac{1}{|S|}\sum_{x \in S}\|x - y\|^2 \le \Delta^2$, because the centroid minimizes the mean squared distance. So with $t' \ge \Delta^2$ every merge test passes, each leaf has one entry, and the tree has one leaf entry, which is at most $M$. $\square$

**Lemma 3 (Ward increase from CFs).** For disjoint nonempty sets $A$ and $B$ with sizes $a$, $b$ and centroids $\mu_A$, $\mu_B$,
$$\mathrm{SSE}(A \cup B) - \mathrm{SSE}(A) - \mathrm{SSE}(B) = \frac{ab}{a + b}\,\|\mu_A - \mu_B\|^2.$$

*Proof.* The centroid of the union is $\mu = (a\mu_A + b\mu_B)/(a + b)$. For any set $S$ and any point $c$, $\sum_{x \in S}\|x - c\|^2 = \mathrm{SSE}(S) + |S|\,\|\mu_S - c\|^2$. Apply this to $A$ and $B$ with $c = \mu$: the increase is $a\|\mu_A - \mu\|^2 + b\|\mu_B - \mu\|^2$. Here $\mu_A - \mu = \frac{b}{a+b}(\mu_A - \mu_B)$ and $\mu_B - \mu = \frac{a}{a+b}(\mu_B - \mu_A)$, so the increase is $\frac{ab^2 + ba^2}{(a+b)^2}\|\mu_A - \mu_B\|^2 = \frac{ab}{a+b}\|\mu_A - \mu_B\|^2$. $\square$

So line L6 picks the pair of clusters whose union raises the sum of squares least, using only the CFs, and the CF of the union is the sum of the two CFs.

**Lemma 4 (phase 3).** Phase 3 returns $\min(k, m)$ CFs, where $m$ is the number of leaf entries, and they are the CFs of a partition of all points into unions of leaf entries.

*Proof.* Each merge joins two clusters, keeps the sum of their CFs, and lowers the count by one; it starts from the $m$ leaf entries, which partition the points by Lemma 1. $\square$

**Theorem (phase 4).** Let $C_1, \ldots, C_k$ be the partition of phase 3 with centroids $\mu_1, \ldots, \mu_k$. After line L7 assigns each point to the nearest $\mu_j$ and line L8 recomputes the centroids $\mu'_j$ of the new clusters $C'_j$,
$$\sum_j \sum_{x \in C'_j}\|x - \mu'_j\|^2 \;\le\; \sum_j \sum_{x \in C'_j}\|x - \mu_j\|^2 \;\le\; \sum_j \mathrm{SSE}(C_j).$$

*Proof.* The second inequality holds point by point: a point $x \in C_i$ has $\min_j \|x - \mu_j\|^2 \le \|x - \mu_i\|^2$, and the right side summed over all points is $\sum_j \mathrm{SSE}(C_j)$. The first holds cluster by cluster, because the centroid of $C'_j$ minimizes the sum of squared distances to the points of $C'_j$. If a cluster becomes empty, its old centroid is kept and contributes nothing. $\blacksquare$

The right side is $\sum_j (\mathrm{SS}_j - \|\mathrm{LS}_j\|^2/N_j)$ for the phase 3 CFs, so it is known before the second scan. More passes of phase 4 are the iterations of [Lloyd's algorithm](/k-means/), and by the same argument none of them raises the sum of squares.
