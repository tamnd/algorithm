---
title: Agglomerative clustering with the Lance-Williams update makes the greedy merges
proves: [correctness]
status: full
---

We write $C_s$ for the cluster that slot $s$ holds, and $\mathcal{L}(A, B)$ for the linkage value of two disjoint clusters. For the weighted and median linkages, $\mathcal{L}$ depends on how each cluster was built: if $A$ was made from $A_1$ and $A_2$, then $\mathcal{L}(A, B) = \frac{1}{2}(\mathcal{L}(A_1, B) + \mathcal{L}(A_2, B))$ for weighted linkage, and $m_A = \frac{1}{2}(m_{A_1} + m_{A_2})$ with $\mathcal{L}(A, B) = \lVert m_A - m_B \rVert^2$ for median linkage, where $m_{\{x\}} = x$. For a single point, all seven linkages give $\mathcal{L}(\{x\}, \{y\}) = d(x, y)$, where $d$ is the squared Euclidean distance for centroid, median and Ward.

The Lance-Williams update is

$$\text{LW} = \alpha_i D_{ki} + \alpha_j D_{kj} + \beta D_{ij} + \gamma \lvert D_{ki} - D_{kj} \rvert,$$

with $D_{ki} = \mathcal{L}(C_k, C_i)$ and so on, $n_i = |C_i|$, and $s = n_i + n_j$.

**Lemma 1 (the rows are exact).** For each of the seven linkages, with the coefficients below, $\text{LW} = \mathcal{L}(C_k, C_i \cup C_j)$.

| linkage | $\alpha_i$ | $\alpha_j$ | $\beta$ | $\gamma$ |
|---|---|---|---|---|
| single | $1/2$ | $1/2$ | $0$ | $-1/2$ |
| complete | $1/2$ | $1/2$ | $0$ | $1/2$ |
| average | $n_i/s$ | $n_j/s$ | $0$ | $0$ |
| weighted | $1/2$ | $1/2$ | $0$ | $0$ |
| centroid | $n_i/s$ | $n_j/s$ | $-n_i n_j/s^2$ | $0$ |
| median | $1/2$ | $1/2$ | $-1/4$ | $0$ |
| Ward | $(n_i + n_k)/(s + n_k)$ | $(n_j + n_k)/(s + n_k)$ | $-n_k/(s + n_k)$ | $0$ |

*Proof.* **Single and complete.** For real numbers $x$ and $y$, $\min(x, y) = \frac{x + y}{2} - \frac{|x - y|}{2}$ and $\max(x, y) = \frac{x + y}{2} + \frac{|x - y|}{2}$. The minimum over the pairs of $C_k \times (C_i \cup C_j)$ is the smaller of the minimum over $C_k \times C_i$ and the minimum over $C_k \times C_j$, and the same holds for the maximum.

**Average.** Let $S(A, B) = \sum_{a \in A, b \in B} d(a, b)$, so $\mathcal{L}(A, B) = S(A, B)/(|A||B|)$. The pairs split, so $S(C_k, C_i \cup C_j) = S(C_k, C_i) + S(C_k, C_j) = n_k n_i D_{ki} + n_k n_j D_{kj}$. Divide by $n_k s$.

**Weighted.** The row is the definition, with $A_1 = C_i$ and $A_2 = C_j$.

**Centroid and median.** For points $u, x, y$ of $\mathbb{R}^p$ and $z = \alpha x + \beta' y$ with $\alpha + \beta' = 1$,

$$\lVert u - z \rVert^2 = \alpha \lVert u - x \rVert^2 + \beta' \lVert u - y \rVert^2 - \alpha \beta' \lVert x - y \rVert^2. \qquad (*)$$

To see this, expand both sides. The terms in $\lVert u \rVert^2$ and $\langle u, \cdot \rangle$ agree because $\alpha + \beta' = 1$. The rest is $\lVert z \rVert^2$ on the left and $\alpha \lVert x \rVert^2 + \beta' \lVert y \rVert^2 - \alpha \beta' \lVert x - y \rVert^2$ on the right, and $\alpha \lVert x \rVert^2 + \beta' \lVert y \rVert^2 - \lVert \alpha x + \beta' y \rVert^2 = \alpha(1 - \alpha)\lVert x \rVert^2 + \beta'(1 - \beta')\lVert y \rVert^2 - 2\alpha\beta' \langle x, y \rangle = \alpha \beta' \lVert x - y \rVert^2$. The centroid of $C_i \cup C_j$ is $\frac{n_i}{s} c_i + \frac{n_j}{s} c_j$, so $(*)$ with $u = c_k$, $\alpha = n_i/s$ and $\beta' = n_j/s$ gives the centroid row. The median point of $C_i \cup C_j$ is $\frac{1}{2}(m_i + m_j)$, so $(*)$ with $\alpha = \beta' = 1/2$ gives the median row.

**Ward.** Here $\mathcal{L}(A, B) = \frac{|A||B|}{|A| + |B|} \lVert c_A - c_B \rVert^2$. Let $t = s + n_k$ and $c$ the centroid of $C_i \cup C_j$. By $(*)$,

$$\mathcal{L}(C_k, C_i \cup C_j) = \frac{n_k s}{t} \lVert c_k - c \rVert^2 = \frac{n_k n_i}{t} \lVert c_k - c_i \rVert^2 + \frac{n_k n_j}{t} \lVert c_k - c_j \rVert^2 - \frac{n_k n_i n_j}{s t} \lVert c_i - c_j \rVert^2.$$

Now $\lVert c_k - c_i \rVert^2 = \frac{n_k + n_i}{n_k n_i} D_{ki}$, $\lVert c_k - c_j \rVert^2 = \frac{n_k + n_j}{n_k n_j} D_{kj}$ and $\lVert c_i - c_j \rVert^2 = \frac{s}{n_i n_j} D_{ij}$. Put these in to get $\frac{n_i + n_k}{t} D_{ki} + \frac{n_j + n_k}{t} D_{kj} - \frac{n_k}{t} D_{ij}$. The formula is linear in the values, so the same row holds for any constant multiple of $\mathcal{L}$, such as twice the increase of the sum of squares. $\square$

**Theorem.** AGGLOMERATIVE$(D, \text{linkage})$ returns $n - 1$ merges. Merge number $t$ joins two clusters $A$ and $B$ of the clustering after $t - 1$ merges, with $\mathcal{L}(A, B)$ minimal over all pairs of that clustering, and records the height $\mathcal{L}(A, B)$.

*Proof.* We show this invariant for the loop of line L3.

> **(A)** The clusters $C_s$ of the active slots are the clusters after the merges made so far, $\text{size}[s] = |C_s|$, and $D[s, r] = \mathcal{L}(C_s, C_r)$ for all active $s \ne r$.

At line L1, each slot holds one point, the sizes are $1$, and $D[s, r] = d(s, r) = \mathcal{L}(\{s\}, \{r\})$. So (A) holds.

Assume (A) at the start of a round. Line L4 picks the active pair with the smallest $D[i, j]$, which by (A) is a pair of current clusters with the smallest $\mathcal{L}$. Line L5 records $h = \mathcal{L}(C_i, C_j)$. In lines L6 and L7, the values $D[k, i]$, $D[k, j]$, $D[i, j]$ and the sizes are still the old ones, because line L7 writes only $D[i, k]$ and $D[k, i]$ for the current $k$, and later values of $k$ read only their own row and column. By Lemma 1, the new $D[i, k]$ is $\mathcal{L}(C_k, C_i \cup C_j)$. Line L9 makes slot $i$ hold $C_i \cup C_j$ with the right size and drops slot $j$. The values between two other slots do not change, and neither do their clusters. So (A) holds again.

Each round drops one slot, so the loop runs $n - 1$ times and ends with one slot that holds all points. $\square$

**Lemma 2 (the priority queue version).** The heap version makes the same merges as the naive version.

*Proof.* Give each slot a version number that grows by one each time the slot takes part in a merge. A heap entry $(v, p, q, a, b)$ is *valid* if $p$ and $q$ are active, $a$ is the version of $p$ and $b$ is the version of $q$. We claim that, before each pop, each pair $p < q$ of active slots has exactly one valid entry, and its value is $D[p, q]$. At the start this holds, with all versions $0$. After a merge into slot $i$, the version of $i$ grows, so each old entry with $i$ stops being valid, and the code pushes one new entry for each pair $i, k$, with the new value. The entries of pairs without $i$ and $j$ keep their version numbers and their values. So the claim holds again. Stale entries are skipped. So the first valid entry that the heap gives is the smallest $(D[p, q], p, q)$ over all active pairs, which is the pair that line L4 picks, with the same rule for ties. $\square$

**Running time.** The round with $m$ active slots scans $m(m - 1)/2$ pairs at line L4 and makes $m - 2$ updates. The sum over $m = n, n - 1, \ldots, 2$ is $\Theta(n^3)$. In the heap version, at most $n(n - 1)/2 + (n - 1)(n - 2)$ entries are ever pushed, and each push and pop takes $O(\log n^2) = O(\log n)$ time, so the time is $O(n^2 \log n)$.
