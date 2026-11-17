---
title: Adaptive voting is exact, and the inliers survive the pruning
proves: [correctness]
status: full
---

We use the notation of the page. There are $m$ correspondences $(a_i, b_i)$ with $b_i = s R a_i + t + o_i + \epsilon_i$, where $o_i = 0$ and $|\epsilon_i| \le \beta$ for an inlier $i$, and $o_i$ is arbitrary for an outlier. We prove two exact parts of the method. The rotation step of the reference code (GNC) is a heuristic, and we claim nothing for it; the semidefinite relaxation and the certificate of TEASER are covered by the theorems of the paper, which this file does not repeat.

## Part 1: adaptive voting solves the scalar TLS problem

Let $v_1, \ldots, v_K$ be real values with bounds $b_k > 0$, and let $\bar c > 0$. The scalar truncated least squares cost is

$$f(x) = \sum_{k=1}^{K} \min\left(\frac{(x - v_k)^2}{b_k^2}, \bar c^2\right).$$

For a set $S \subseteq \{1, \ldots, K\}$ define $g_S(x) = \sum_{k \in S} (x - v_k)^2 / b_k^2 + (K - |S|)\, \bar c^2$, and for $S \ne \emptyset$ let $\bar x_S = \sum_{k \in S} v_k b_k^{-2} / \sum_{k \in S} b_k^{-2}$ be the weighted mean, the unique minimizer of $g_S$.

The interval of $k$ is $I_k = [v_k - \bar c b_k, v_k + \bar c b_k]$, where the $k$-th term of $f$ is below its cap. Sort the $2K$ ends. They cut the line into open pieces. On each piece of positive length, the set $S$ of the intervals that contain the piece is fixed. Adaptive voting computes $g_S(\bar x_S)$ for every piece with $S \ne \emptyset$ and returns the $\bar x_S$ of least value.

**Claim 1.** The returned $\hat x$ is a global minimizer of $f$.

*Proof.* (i) For every $S$ and $x$, $f(x) \le g_S(x)$, because each term of $f$ is at most its quadratic term and at most $\bar c^2$.

(ii) $f$ is continuous and tends to $K \bar c^2$ far from all $v_k$, while $f(v_1) \le (K - 1)\bar c^2 < K \bar c^2$. So $f$ has a global minimizer $x^\star$, and $f(x^\star) < K \bar c^2$. Hence $x^\star$ lies in the interior of some interval: if every $I_k$ had $x^\star$ outside or at an end, every term would equal $\bar c^2$.

(iii) Since $x^\star$ is not the least end of all intervals that contain it, take $\varepsilon > 0$ so small that no end lies in $(x^\star - \varepsilon, x^\star)$. This open set lies in one piece of positive length; let $S$ be its set. For $k \in S$, $I_k$ contains $(x^\star - \varepsilon, x^\star)$, and since $I_k$ is closed, $x^\star \in I_k$, so the $k$-th term of $f(x^\star)$ is $(x^\star - v_k)^2 / b_k^2$. For $k \notin S$, $I_k$ does not meet $(x^\star - \varepsilon, x^\star)$, so either $x^\star \notin I_k$ or $x^\star$ is the left end of $I_k$; in both cases the $k$-th term is $\bar c^2$. So $f(x^\star) = g_S(x^\star)$. The set $S$ is not empty, because $x^\star$ is interior to some interval, and that interval contains a left neighborhood of $x^\star$.

(iv) Then $f(x^\star) = g_S(x^\star) \ge g_S(\bar x_S) \ge \min_{\text{pieces}} g_{S'}(\bar x_{S'}) = g_{\hat S}(\hat x) \ge f(\hat x)$, using (i) last. So $f(\hat x) \le f(x^\star)$, and $\hat x$ is a global minimizer. $\square$

The number of pieces with a nonempty set is at most $2K - 1$, the number of gaps between $2K$ sorted ends. The reference code keeps the running sums $\sum b_k^{-2}$, $\sum v_k b_k^{-2}$ and $\sum v_k^2 b_k^{-2}$ over the current set, so $g_S(\bar x_S) = \sum v_k^2 b_k^{-2} - (\sum v_k b_k^{-2})^2 / \sum b_k^{-2} + (K - |S|)\bar c^2$ costs $O(1)$ per piece, and the whole sweep costs $O(K \log K)$ for the sort.

## Part 2: inlier pairs survive the pruning

For $i < j$ let $\bar a_{ij} = a_j - a_i$ and $\bar b_{ij} = b_j - b_i$, with $\bar a_{ij} \ne 0$, and let $\delta = 2\beta$, $s_{ij} = |\bar b_{ij}| / |\bar a_{ij}|$ and $\alpha_{ij} = \delta / |\bar a_{ij}|$.

**Claim 2.** If $i$ and $j$ are both inliers, then $|s_{ij} - s| \le \alpha_{ij}$, where $s$ is the true scale. So with the known scale and $\bar c \ge 1$, the edge $(i, j)$ passes the test of line L4, and the inliers form a clique of the pruned graph. In particular a maximum clique has at least as many vertices as there are inliers.

*Proof.* For inliers, $\bar b_{ij} = s R \bar a_{ij} + (\epsilon_j - \epsilon_i)$: the translation cancels. By the triangle inequality and since $|R \bar a_{ij}| = |\bar a_{ij}|$,

$$\big|\, |\bar b_{ij}| - s |\bar a_{ij}| \,\big| \le |\bar b_{ij} - s R \bar a_{ij}| = |\epsilon_j - \epsilon_i| \le 2\beta = \delta .$$

Divide by $|\bar a_{ij}|$ to get $|s_{ij} - s| \le \alpha_{ij} \le \bar c\, \alpha_{ij}$. Every pair of inliers is joined, so the inliers form a clique. $\square$

**What the claims do not say.**

- With an unknown scale, the test uses the estimate $\hat s$ of line L3, not $s$. Claim 1 shows that $\hat s$ minimizes the TLS cost of the ratios, but it can differ from $s$, and then an inlier edge can fail the test. The paper bounds the error of $\hat s$ under conditions on the inliers; this file does not.
- A maximum clique can hold outliers, or, in rare cases, be a set of outliers larger than the set of inliers. Line L5 keeps the maximum clique as a strong filter, not as a proof that it is the inlier set. The rotation step must still be robust, which is why it uses the TLS cost.
- The rotation step of the reference code uses graduated non-convexity. It often finds the global TLS minimizer, but it has no guarantee. TEASER instead solves a semidefinite relaxation of the rotation TLS problem and checks a certificate of optimality.
