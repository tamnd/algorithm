---
title: RootSIFT turns Euclidean distance into the Hellinger kernel
proves: [correctness]
status: full
---

Let $x, y \in \mathbb{R}^D$ have non-negative entries and positive sums $s_x = \sum_i x_i$ and $s_y = \sum_i y_i$. Write $\bar x = x / s_x$ and $\bar y = y / s_y$ for the L1-normalized vectors, and $\sqrt{\cdot}$ entrywise. Lines L1 to L3 compute $R(x) = \sqrt{\bar x}$, and $R(0) = 0$. The Hellinger kernel is $H(x, y) = \sum_i \sqrt{\bar x_i \bar y_i}$.

**Lemma 1 (unit norm).** $\lVert R(x) \rVert_2 = 1$.

*Proof.* $\lVert R(x) \rVert_2^2 = \sum_i \bar x_i = 1$, because $\bar x$ is non-negative with sum 1. $\square$

**Lemma 2 (inner product).** $\langle R(x), R(y) \rangle = H(x, y)$, and $0 \le H(x, y) \le 1$.

*Proof.* $\sqrt{\bar x_i}\sqrt{\bar y_i} = \sqrt{\bar x_i \bar y_i}$ for non-negative entries, so the sums agree. All terms are non-negative, and the Cauchy-Schwarz inequality with Lemma 1 gives $H \le \lVert R(x) \rVert \lVert R(y) \rVert = 1$. $\square$

**Lemma 3 (distance).** $\lVert R(x) - R(y) \rVert_2^2 = 2 - 2 H(x, y)$.

*Proof.* Expand: $\lVert R(x) \rVert^2 + \lVert R(y) \rVert^2 - 2 \langle R(x), R(y) \rangle = 1 + 1 - 2 H(x, y)$ by Lemmas 1 and 2. $\square$

So the Euclidean distance of RootSIFT vectors is $\sqrt{2}$ times the Hellinger distance $h(\bar x, \bar y) = \sqrt{1 - H(x, y)}$ between the normalized histograms.

**Lemma 4 (nearest neighbors).** For a query $q$ and database vectors $p_1, \dots, p_n$, all with positive sums, $\lVert R(q) - R(p_j) \rVert < \lVert R(q) - R(p_k) \rVert$ if and only if $H(q, p_j) > H(q, p_k)$. So the nearest RootSIFT vector is a database vector of largest Hellinger kernel with the query, and every method that ranks by Euclidean distance ranks by the Hellinger kernel.

*Proof.* By Lemma 3, the distance is $\sqrt{2 - 2H}$, a strictly decreasing function of $H$ on $[0, 1]$. $\square$

**Lemma 5 (scale).** $R(c x) = R(x)$ for every $c > 0$.

*Proof.* $c x / (c s_x) = x / s_x$. $\square$

**Theorem.** For non-negative descriptors with positive sums, RootSIFT gives unit vectors whose inner products are the Hellinger kernels and whose squared Euclidean distances are $2 - 2H$. Euclidean nearest neighbor search on RootSIFT vectors returns the descriptor of largest Hellinger kernel, and the result does not change when a descriptor is multiplied by a positive number.

*Proof.* Lemmas 1 to 5. $\blacksquare$
