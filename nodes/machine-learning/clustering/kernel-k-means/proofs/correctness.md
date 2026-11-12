---
title: Kernel k-means computes feature space distances from K, lowers its objective, and stops
proves: [correctness]
status: full
---

Assume that $K$ is positive semidefinite. Then there are vectors $\varphi_1, \ldots, \varphi_n$ in a real inner product space with $K_{ij} = \langle \varphi_i, \varphi_j \rangle$ (for example the columns of a square root of $K$). The weights $w_i$ are positive. For a non-empty set $P$ of indices let $W_P = \sum_{j \in P} w_j$ and $m_P = \frac{1}{W_P}\sum_{j \in P} w_j \varphi_j$.

**Lemma 1 (the kernel formula).** For each $i$ and each non-empty $P$,
$$\|\varphi_i - m_P\|^2 = K_{ii} - \frac{2}{W_P}\sum_{j \in P} w_j K_{ij} + \frac{1}{W_P^2}\sum_{j, l \in P} w_j w_l K_{jl} .$$

*Proof.* Expand $\langle \varphi_i - m_P, \varphi_i - m_P \rangle = \langle \varphi_i, \varphi_i \rangle - 2\langle \varphi_i, m_P \rangle + \langle m_P, m_P \rangle$ and use the bilinearity of the inner product with $m_P = \frac{1}{W_P}\sum_j w_j \varphi_j$. $\square$

So line L4 computes $D(i, c) = \|\varphi_i - m_{P_c}\|^2$ exactly.

**Lemma 2 (weighted centroid).** For each non-empty $P$ and each vector $z$, $\sum_{i \in P} w_i\|\varphi_i - z\|^2 = \sum_{i \in P} w_i\|\varphi_i - m_P\|^2 + W_P\|m_P - z\|^2$.

*Proof.* Write $\varphi_i - z = (\varphi_i - m_P) + (m_P - z)$ and expand. The cross term is $2\langle \sum_{i \in P} w_i(\varphi_i - m_P), m_P - z \rangle = 0$, because $\sum_{i \in P} w_i \varphi_i = W_P m_P$. $\square$

For labels $a$ let $J(a) = \sum_i w_i \|\varphi_i - m_{P_{a_i}}\|^2$, and for labels $b$ and vectors $z_1, \ldots, z_k$ let $G(b, z) = \sum_i w_i\|\varphi_i - z_{b_i}\|^2$.

**Lemma 3 (one pass).** If a pass of lines L2 to L5 changes at least one label, then the new labels $b$ satisfy $J(b) < J(a)$.

*Proof.* Let $z_c = m_{P_c}$ for the clusters of $a$. Then $J(a) = G(a, z)$. Line L5 gives each point a cluster with the least $D(i, c)$, which by Lemma 1 is the least $\|\varphi_i - z_c\|^2$, and keeps $a_i$ on a tie. So each term of $G(b, z)$ is at most the term of $G(a, z)$, and it is strictly smaller for each $i$ with $b_i \ne a_i$, because $w_i > 0$. Hence $G(b, z) < G(a, z) = J(a)$. By Lemma 2, for each non-empty cluster of $b$ the weighted mean is the best center, so $J(b) \le G(b, z)$. (A cluster of $b$ is non-empty only if it was non-empty in $a$, because line L4 considers only non-empty clusters, so $z_c$ exists for each cluster that $b$ uses.) $\square$

**Theorem.** The loop of lines L1 to L7 stops, and at the end each point is at a nearest weighted mean in feature space.

*Proof.* $J$ depends only on the labels, which take at most $k^n$ values. By Lemma 3, $J$ falls strictly in each pass that changes a label, so no labeling repeats and some pass changes nothing. Then line L6 returns. In that pass each $a_i$ minimized $D(i, c) = \|\varphi_i - m_{P_c}\|^2$ over the non-empty clusters. $\square$

**Theorem (normalized cut).** Let $A$ be a symmetric non-negative matrix with degrees $d_i = \sum_j A_{ij} > 0$, let $w_i = d_i$, $\sigma \ge 0$, and $K = \sigma D^{-1} + D^{-1}AD^{-1}$ with $D = \mathrm{diag}(d)$. Then for each partition into $k$ non-empty clusters,
$$J = n\sigma + \sum_i \frac{A_{ii}}{d_i} - k\sigma - k + \sum_{c} \frac{\mathrm{links}(P_c, V \setminus P_c)}{\mathrm{deg}(P_c)},$$
where $\mathrm{links}(P, Q) = \sum_{i \in P, j \in Q} A_{ij}$ and $\mathrm{deg}(P) = \sum_{i \in P} d_i$.

*Proof.* By Lemma 1 summed with the weights, $J = \sum_i w_i K_{ii} - \sum_c \frac{1}{W_c}\sum_{j, l \in P_c} w_j w_l K_{jl}$. Here $w_i K_{ii} = d_i(\frac{\sigma}{d_i} + \frac{A_{ii}}{d_i^2}) = \sigma + \frac{A_{ii}}{d_i}$, and $\sum_{j, l \in P_c} d_j d_l K_{jl} = \sigma\,\mathrm{deg}(P_c) + \mathrm{links}(P_c, P_c)$, with $W_c = \mathrm{deg}(P_c)$. So $J = n\sigma + \sum_i \frac{A_{ii}}{d_i} - k\sigma - \sum_c \frac{\mathrm{links}(P_c, P_c)}{\mathrm{deg}(P_c)}$. Finally $\mathrm{links}(P_c, P_c) = \mathrm{deg}(P_c) - \mathrm{links}(P_c, V \setminus P_c)$, so the last sum is $k - \mathrm{NCut}$. $\square$

For $\sigma$ large enough $K$ is positive semidefinite, so the first theorem applies, and each pass does not raise the normalized cut as long as no cluster becomes empty.
