---
title: The MNN correction is a convex combination of the pair vectors, and it removes a small translation exactly
proves: [correctness]
status: full
---

We prove what the steps compute. Cosine normalization removes a scale factor of each cell and turns Euclidean distance into a function of the cosine (Lemma 1). The pairs are symmetric and there are at most $k\min(n_R, n_B)$ of them (Lemma 2). The correction of every cell is a convex combination of the pair vectors, so it removes a batch effect exactly when all pair vectors equal it (Lemma 3). And a translation shorter than half of the smallest distance between reference cells is removed exactly with $k = 1$ (Theorem 4). Haghverdi and co-authors state three assumptions: at least one cell population is present in both batches, the batch effect is almost orthogonal to the biological subspace, and the batch effect varies much less than the biology between cell types. When the batch effect is not constant, the result is a smoothed estimate; how good it is depends on the data, and the tests measure it.

**Setting.** A reference batch $R = (r_1, \dots, r_{n_R})$ and a batch $B = (b_1, \dots, b_{n_B})$ of points in $\mathbb{R}^d$. $N_R(b)$ is the set of the $k$ nearest cells of $R$ to $b$ and $N_B(r)$ the set of the $k$ nearest cells of $B$ to $r$, with ties broken by index. Line L3 keeps the pairs $P = \{(r, b) : r \in N_R(b),\, b \in N_B(r)\}$. Line L4 sets $v_p = r - b$ for $p = (r, b)$, and line L5 sets, for each $x \in B$,
$$c(x) = \sum_{p \in P}\omega_p(x)v_p, \qquad \omega_p(x) = \frac{e^{-\|x - b_p\|^2/\sigma^2}}{\sum_{q \in P}e^{-\|x - b_q\|^2/\sigma^2}},$$
where $b_p$ is the cell of $B$ in pair $p$. Line L6 returns $x + c(x)$.

**Lemma 1 (cosine normalization).** Line L1 maps $x \ne 0$ to $\hat x = x/\|x\|$. Then $\widehat{sx} = \hat x$ for every $s > 0$, and $\|\hat x - \hat y\|^2 = 2 - 2\cos(x, y)$.

*Proof.* $sx/\|sx\| = x/\|x\|$. For unit vectors, $\|\hat x - \hat y\|^2 = \|\hat x\|^2 + \|\hat y\|^2 - 2\hat x \cdot \hat y = 2 - 2\cos(x, y)$. $\square$

So a cell whose counts are all larger by one factor, for example because its batch was sequenced more deeply, lands at the same point, and nearest neighbors after the normalization are nearest by angle.

**Lemma 2 (pairs).** $(r, b) \in P$ if and only if $(b, r)$ is a pair when the roles of $R$ and $B$ are swapped, and $|P| \le k\min(n_R, n_B)$.

*Proof.* The condition $r \in N_R(b)$ and $b \in N_B(r)$ is the same with the roles swapped. Each pair has $r \in N_R(b)$, so for each $b$ there are at most $k$ pairs, and $|P| \le kn_B$; in the same way $|P| \le kn_R$. $\square$

**Lemma 3 (convex combination).** If $P$ is not empty, then for every $x \in B$ the weights $\omega_p(x)$ are positive and sum to 1, so $c(x)$ lies in the convex hull of the pair vectors. In particular, if $v_p = c$ for all $p$, then $c(x) = c$ for every $x$.

*Proof.* Each exponential is positive and they are divided by their sum. The code subtracts the smallest squared distance from all of them before taking the exponential, which multiplies the numerator and the denominator by the same factor and keeps the largest term at 1, so the sum cannot underflow to 0. A weighted mean with positive weights that sum to 1 lies in the convex hull, and it equals $c$ when every term equals $c$. $\square$

So the correction never moves a cell further than the longest pair vector, and a cell type that is found only in $B$ moves by the vectors of the nearest pairs, not onto some cell of $R$. As $\sigma \to \infty$ all weights tend to $1/|P|$ and $c(x)$ tends to the mean of the pair vectors, a single shift. As $\sigma \to 0$ the weight goes to the pairs whose cell $b_p$ is nearest to $x$, so a cell that is in exactly one pair gets that pair's vector.

**Theorem 4 (translation).** Let $B = (r_1 + t, \dots, r_n + t)$ for a vector $t$ with $\|t\| < \delta/2$, where $\delta = \min_{i \ne j}\|r_i - r_j\|$, and let $k = 1$. Then $P = \{(r_i, b_i)\}$ for all $i$, and line L6 returns $b_i - t = r_i$ for every $i$.

*Proof.* For $j \ne i$, $\|b_i - r_j\| = \|r_i - r_j + t\| \ge \delta - \|t\| > \|t\| = \|b_i - r_i\|$, so the nearest cell of $R$ to $b_i$ is $r_i$, with no tie. In the same way $\|r_i - b_j\| = \|r_i - r_j - t\| > \|t\| = \|r_i - b_i\|$, so the nearest cell of $B$ to $r_i$ is $b_i$. So $(r_i, b_i)$ is a pair for every $i$, and no other pair exists because each $b$ has only one nearest cell. Every pair vector is $r_i - b_i = -t$, and by Lemma 3 every cell moves by $-t$. $\square$

The condition is the third assumption of the paper in its simplest form: the batch effect is smaller than the distances that separate cells. With a larger shift, cells of $B$ pair with the wrong cells of $R$. With $k > 1$ and noise, a pair can join cells of two different types; the tests count such pairs.

**What the lines compute.** Line L1 is Lemma 1. Lines L2 and L3 are the pairs of Lemma 2, found with two brute force neighbor searches. Line L4 gives the pair vectors and line L5 the weights of Lemma 3. Line L6 adds the correction. Line L7 adds the corrected batch to the reference, so the next batch is matched against all cells corrected so far; the result depends on the order of the batches.

**Complexity.** The two neighbor searches take $O(n_Rn_Bd)$ time with sorting of $O(n_Rn_B\log n)$, and there are at most $k\min(n_R, n_B)$ pairs. Line L5 takes $O(n_B|P|d)$ time. With $q$ batches of $n$ cells each, the batch $i$ is matched against $(i - 1)n$ cells, and line L5 takes $O(kn^2d)$ for each batch, so the total time is $O(q^2n^2(d + \log n) + qkn^2d)$ by brute force. The space is $O(qnd + |P|d)$ for the cells and the pair vectors.

**What the tests check.** The test file checks the page example, the pairs against the definition with the bound and the symmetry of Lemma 2, Lemma 1, the convex hull of Lemma 3, Theorem 4 on random reference sets, the two limits of $\sigma$, and three batches in a row. Two simulations are measurements, not theorems. With two cell types in different proportions in the two batches, the MNN correction is much closer to the truth than moving the batch by the difference of its mean from the reference mean. A cell type found only in the second batch moves by about the true shift and stays far from the reference cells.
