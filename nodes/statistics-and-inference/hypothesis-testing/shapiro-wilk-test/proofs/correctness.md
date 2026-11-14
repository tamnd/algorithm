---
title: The Shapiro-Wilk statistic is a squared correlation in its proven range, it is invariant, and its p-value is exact for three observations
proves: [correctness, termination]
status: full
---

We prove that SHAPIRO-WILK returns $W = (\sum_i a_iy_i)^2/\sum_i(y_i - \bar y)^2$, that $W$ is the squared correlation of the sorted sample with the weights, that $W$ is location and scale invariant, that $na_n^2/(n - 1) \le W \le 1$, and that for $n = 3$ line L6 returns the exact p-value, so the test has size exactly $\alpha$. Two things are not proved, and the page reports them as measured: that Royston's weights in line L2 are close to the exact $V^{-1}m/\lVert V^{-1}m\rVert$, and that the normalizing transform in lines L7 to L9 gives a p-value close to the true one for $n \ge 4$. The lower bound uses one inequality on the weights, which we check by computation and do not prove.

Throughout, $a = (a_1, \dots, a_n)$ is the output of line L2. By construction it satisfies $a_i = -a_{n+1-i}$, so $\sum_i a_i = 0$ and $a_{(n+1)/2} = 0$ when $n$ is odd, and $\sum_i a_i^2 = 1$, because the middle weights are scaled by $\phi$ for exactly this. It is also increasing, $a_1 < a_2 < \dots < a_n$. The middle weights are increasing because $\Phi^{-1}$ is increasing; that the end weights are larger than their neighbors is a property of the fitted polynomials, which the tests check for ten values of $n$ from 3 to 500, and Lemma 4 only uses the signs $a_i < 0$ for $i \le n/2$.

**Lemma 1 (line L4).** $b = \sum_{i=1}^n a_iy_i$.

*Proof.* Group the terms $i$ and $n + 1 - i$ for $i \le \lfloor n/2\rfloor$: $a_iy_i + a_{n+1-i}y_{n+1-i} = a_{n+1-i}(y_{n+1-i} - y_i)$, because $a_i = -a_{n+1-i}$. When $n$ is odd, the middle term is $a_{(n+1)/2}y_{(n+1)/2} = 0$. $\square$

**Lemma 2 (squared correlation and the upper bound).** If $SS > 0$, then $b^2/SS = r^2$, where $r$ is the sample correlation of $(y_i)$ and $(a_i)$, and $0 \le b^2/SS \le 1$, with $b^2/SS = 1$ if and only if $y - \bar y\mathbf 1$ is a multiple of $a$.

*Proof.* Since $\sum_i a_i = 0$, $\sum_i a_i(y_i - \bar y) = \sum_i a_iy_i = b$ and $\sum_i (a_i - \bar a)^2 = \sum_i a_i^2 = 1$. So $r^2 = b^2/(1 \cdot SS)$. By the Cauchy-Schwarz inequality, $b^2 = \left(\sum_i a_i(y_i - \bar y)\right)^2 \le \sum_i a_i^2 \sum_i (y_i - \bar y)^2 = SS$, with equality if and only if the two vectors are proportional. $\square$

So line L5 returns $b^2/SS$ in exact arithmetic, and the minimum with 1 only removes rounding.

**Lemma 3 (invariance).** Let $x_i' = c + dx_i$ with $d \ne 0$. Then $W(x') = W(x)$.

*Proof.* If $d > 0$, the sorted sample is $y_i' = c + dy_i$. Then $b' = \sum_i a_i(c + dy_i) = db$, because $\sum_i a_i = 0$, and $SS' = d^2SS$. If $d < 0$, the order reverses: $y_i' = c + dy_{n+1-i}$, so $b' = \sum_i a_i(c + dy_{n+1-i}) = d\sum_i a_iy_{n+1-i}$. With $j = n + 1 - i$, $\sum_i a_iy_{n+1-i} = \sum_j a_{n+1-j}y_j = -\sum_j a_jy_j = -b$, so $b' = -db$, and again $b'^2 = d^2b^2$. In both cases $W' = d^2b^2/(d^2SS) = W$. $\square$

So under $H_0$ the law of $W$ is the same for every $\mu$ and $\sigma > 0$, and the p-value may be computed for standard normal data.

**Lemma 4 (lower bound).** Let $c_k = \sum_{i > k} a_i$ for $1 \le k \le n - 1$. Assume
$$(n - 1)c_k^2 \ge k(n - k)a_n^2 \quad \text{for } 1 \le k \le n - 1. \tag{C}$$
Then $W \ge na_n^2/(n - 1)$ for every sample with $SS > 0$, with equality for $y = (0, \dots, 0, 1)$.

*Proof.* First, $c_k > 0$. If $k \ge n/2$, every $a_i$ with $i > k$ is $\ge 0$ and $a_n > 0$ is among them. If $k < n/2$, $c_k = -\sum_{i \le k} a_i$, and every $a_i$ with $i \le k$ is $< 0$.

Write $d_k = y_{k+1} - y_k \ge 0$ and $s_k$ for the vector with $s_{k,i} = 1$ for $i > k$ and $0$ otherwise. Then $y = y_1\mathbf 1 + \sum_{k=1}^{n-1} d_ks_k$. Since $a^\top\mathbf 1 = 0$, $b = \sum_k d_kc_k$. Let $t_k = s_k - \frac{n - k}{n}\mathbf 1$, the centered $s_k$; then $y - \bar y\mathbf 1 = \sum_k d_kt_k$ and $\lVert t_k\rVert^2 = (n - k) - (n - k)^2/n = k(n - k)/n$. By the triangle inequality, $\sqrt{SS} \le \sum_k d_k\lVert t_k\rVert$. Not all $d_k$ are 0 because $SS > 0$, so
$$\sqrt W = \frac{\sum_k d_kc_k}{\sqrt{SS}} \ge \frac{\sum_k d_kc_k}{\sum_k d_k\lVert t_k\rVert} \ge \min_k \frac{c_k}{\lVert t_k\rVert},$$
where the last step holds because a ratio of sums with nonnegative weights is at least the smallest ratio of the terms. By (C), $c_k^2/\lVert t_k\rVert^2 = nc_k^2/(k(n - k)) \ge na_n^2/(n - 1)$ for every $k$. So $W \ge na_n^2/(n - 1)$.

For $y = (0, \dots, 0, 1)$, $b = a_n$ and $SS = 1 - 1/n = (n - 1)/n$, so $W = na_n^2/(n - 1)$. $\square$

Condition (C) holds with equality for $k = 1$ and $k = n - 1$, since $c_1 = -a_1 = a_n$ and $c_{n-1} = a_n$. For $n = 3$ these are all the $k$. For the weights of line L2, a computation over every $n$ from 3 to 5000 and every $k$ found the smallest value of $(n - 1)c_k^2/(k(n - k)a_n^2)$ to be $1 - 4 \times 10^{-13}$, which is 1 up to rounding. So (C) holds for the weights used, as a checked computation and not as a proof for a general $n$.

**Lemma 5 (the exact law for $n = 3$).** If $x_1, x_2, x_3$ are iid $N(\mu, \sigma^2)$, then $P(W \le w) = \frac6\pi\left(\arcsin\sqrt w - \frac\pi3\right)$ for $\frac34 \le w \le 1$.

*Proof.* For $n = 3$, line L2 gives $a = (-1/\sqrt2, 0, 1/\sqrt2)$, so $W = (y_3 - y_1)^2/(2SS)$: half the squared range over $SS$. The centered vector $x - \bar x\mathbf 1$ is the orthogonal projection of $x$ onto the plane $\mathbf 1^\perp$. Since $x \sim N(\mu\mathbf 1, \sigma^2I)$, the projection has the law $N(0, \sigma^2)$ in each of two orthonormal coordinates of the plane, independently, so it is $R(\cos\Theta\,e + \sin\Theta\,f)$ for an orthonormal basis $e, f$ of the plane, with $\Theta$ uniform on $[0, 2\pi)$ and independent of $R$. The projections of the three unit vectors onto the plane have length $\sqrt{2/3}$ and are $2\pi/3$ apart, so the three centered values are $\sqrt{2/3}\,R\cos(\Theta - \varphi_j)$ for $\varphi_j = \varphi_1 + 2\pi(j - 1)/3$, and $SS = R^2$.

So $W = g(\Theta)$, where $g(\theta) = \frac13\left(\max_j\cos(\theta - \varphi_j) - \min_j\cos(\theta - \varphi_j)\right)^2$. The function $g$ has period $2\pi/3$, because adding $2\pi/3$ to $\theta$ permutes the three values, and it is even about $\varphi_1$, because $\theta \mapsto 2\varphi_1 - \theta$ replaces each $\theta - \varphi_j$ by its negative up to the same permutation. Hence $g$ is also even about $\varphi_1 + \pi/3$, and the law of $g(\Theta)$ is the law of $g(\varphi_1 + U)$ with $U$ uniform on $[0, \pi/3]$. For $0 \le u \le \pi/3$, the largest of $\cos u, \cos(u - 2\pi/3), \cos(u + 2\pi/3)$ is $\cos u$ and the smallest is $\cos(u + 2\pi/3)$, because $u + 2\pi/3 \in [2\pi/3, \pi]$. Their difference is $2\sin(u + \pi/3)\sin(\pi/3) = \sqrt3\sin(u + \pi/3)$, so $g(\varphi_1 + u) = \sin^2(u + \pi/3)$.

Let $v = U + \pi/3$, uniform on $[\pi/3, 2\pi/3]$. For $\frac34 \le w \le 1$, $\sin^2 v \le w$ if and only if $v \le \arcsin\sqrt w$ or $v \ge \pi - \arcsin\sqrt w$, a set of length $2(\arcsin\sqrt w - \pi/3)$ in an interval of length $\pi/3$. This gives the stated distribution function. $\square$

**Lemma 6 (size for $n = 3$).** For $n = 3$ the p-value of line L6 is uniform on $[0, 1]$ under $H_0$, and rejecting when $p \le \alpha$ has size exactly $\alpha$.

*Proof.* Line L6 returns $G(W)$, where $G$ is the distribution function of Lemma 5, clipped to $[0, 1]$ only against rounding. $G$ is continuous and strictly increasing on $[\frac34, 1]$ and $W$ has this law, so $G(W)$ is uniform, by the probability integral transform. Hence $P(G(W) \le \alpha) = \alpha$. Small $W$ gives small $p$, as the test requires. $\square$

**What is measured and not proved.** For $n \ge 4$ the weights of line L2 and the transform in lines L7 to L9 are Royston's fitted approximations. The tests compute the exact weights for $n = 4, 5, 6$ from the integrals that define the means and covariances of normal order statistics and find the approximations within $1.5 \times 10^{-3}$. Seeded simulations give a size of the nominal 5% test between 0.046 and 0.054 for $n$ from 4 to 200. Lemmas 1 to 4 hold for the weights of line L2 whatever their accuracy, because they use only the antisymmetry, the unit norm, the order and condition (C).

**Termination.** Line L1 sorts $n$ values. Line L2 makes $n$ calls of $\Phi^{-1}$, each a fixed number of operations, and a fixed number of polynomial evaluations. Lines L3 to L5 are three passes over $n$ values. Lines L6 to L9 are a fixed number of operations and one call of $\Phi$. Every step is a bounded loop, so the algorithm stops.

**Theorem.** For $3 \le n \le 5000$ and data that are not all equal, SHAPIRO-WILK returns $W = (\sum_i a_iy_i)^2/SS$, which is the squared correlation of the sorted sample with the weights, is invariant under $x \mapsto c + dx$ with $d \ne 0$, and lies in $[na_n^2/(n - 1), 1]$. For $n = 3$ the returned p-value is exact and the test has size exactly $\alpha$.

*Proof.* Lemmas 1 to 6, with condition (C) checked by computation for the weights used. $\blacksquare$
