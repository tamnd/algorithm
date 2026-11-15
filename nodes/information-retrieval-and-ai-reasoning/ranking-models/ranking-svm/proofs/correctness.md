---
title: The projected subgradient method for the Ranking SVM converges at rate log T over T, and a small objective orders every pair
proves: [correctness]
status: full
---

The training set gives $P$ pairs. For each query and each two of its documents with $y_i > y_j$, the pair vector is $z = x_i - x_j$. Pairs never mix two queries. For $\lambda > 0$ the objective is

$$J(w) = \frac{\lambda}{2} \lVert w \rVert^2 + \frac{1}{P} \sum_{k=1}^{P} \max(0, 1 - w \cdot z_k).$$

$J$ is $\lambda$-strongly convex, as the sum of $\frac{\lambda}{2}\lVert w \rVert^2$ and a convex function, so it has one minimizer $w^*$. Let $J^* = J(w^*)$.

**Lemma 1 (a ball that holds $w^*$).** $\lVert w^* \rVert \le R = \sqrt{2/\lambda}$.

*Proof.* $\frac{\lambda}{2} \lVert w^* \rVert^2 \le J(w^*) \le J(0) = 1$. $\square$

**Lemma 2 (subgradient).** The vector $g(w) = \lambda w - \frac{1}{P} \sum_{k : w \cdot z_k < 1} z_k$ of line L4 satisfies, for all $u$,

$$J(u) \ge J(w) + g(w) \cdot (u - w) + \frac{\lambda}{2} \lVert u - w \rVert^2.$$

If $\lVert w \rVert \le R$, then $\lVert g(w) \rVert \le G = \lambda R + \max_k \lVert z_k \rVert$.

*Proof.* For the hinge term $h_k(w) = \max(0, 1 - w \cdot z_k)$, the vector $-z_k$ is a subgradient where $w \cdot z_k < 1$ and $0$ is a subgradient elsewhere, so $h_k(u) \ge h_k(w) + (\text{that vector}) \cdot (u - w)$. For the quadratic term, $\frac{\lambda}{2}\lVert u \rVert^2 = \frac{\lambda}{2}\lVert w \rVert^2 + \lambda w \cdot (u - w) + \frac{\lambda}{2}\lVert u - w \rVert^2$. Add the two. The norm bound is the triangle inequality, since the average of at most $P$ vectors $z_k$ divided by $P$ has norm at most $\max_k \lVert z_k \rVert$. $\square$

**Theorem (rate).** Let $w_1 = 0$ and $w_{t+1} = \Pi(w_t - \eta_t g(w_t))$ with $\eta_t = 1/(\lambda t)$, where $\Pi$ is the projection onto the ball of radius $R$ (lines L2 to L6). Then

$$\min_{1 \le t \le T} J(w_t) - J^* \le \frac{G^2 (1 + \ln T)}{2 \lambda T}.$$

*Proof.* Write $d_t = \lVert w_t - w^* \rVert^2$ and $g_t = g(w_t)$. The projection onto a convex set that holds $w^*$ (Lemma 1) does not increase the distance to $w^*$, so $d_{t+1} \le d_t - 2 \eta_t g_t \cdot (w_t - w^*) + \eta_t^2 \lVert g_t \rVert^2$. Hence

$$g_t \cdot (w_t - w^*) \le \frac{d_t - d_{t+1}}{2 \eta_t} + \frac{\eta_t G^2}{2}.$$

Lemma 2 with $u = w^*$ and $w = w_t$ gives $J(w_t) - J^* \le g_t \cdot (w_t - w^*) - \frac{\lambda}{2} d_t$. With $1/\eta_t = \lambda t$,

$$J(w_t) - J^* \le \frac{\lambda (t - 1)}{2} d_t - \frac{\lambda t}{2} d_{t+1} + \frac{G^2}{2 \lambda t}.$$

Summing over $t = 1, \ldots, T$, the first two terms telescope to $0 \cdot d_1 - \frac{\lambda T}{2} d_{T+1} \le 0$, and $\sum_{t \le T} 1/t \le 1 + \ln T$. So $\sum_{t=1}^{T} (J(w_t) - J^*) \le \frac{G^2}{2\lambda}(1 + \ln T)$, and the minimum is at most the mean. $\square$

The code keeps the best iterate seen (line L7), which includes $w_1, \ldots, w_T$, so its value $J_{\text{best}}$ meets the bound. The best values never increase from one step to the next by construction.

**Lemma 3 (weak duality).** For $\alpha \in [0, 1]^P$ let

$$D(\alpha) = \frac{1}{P} \sum_k \alpha_k - \frac{1}{2 \lambda P^2} \Big\lVert \sum_k \alpha_k z_k \Big\rVert^2.$$

Then $D(\alpha) \le J(w)$ for every $w$. The coordinate step $\alpha_k \leftarrow \operatorname{clip}_{[0,1]}\left(\alpha_k + (\lambda P - z_k \cdot v)/\lVert z_k \rVert^2\right)$, with $v = \sum_l \alpha_l z_l$, maximizes $D$ over $\alpha_k$ with the others fixed.

*Proof.* For $\alpha_k \in [0, 1]$, $\max(0, 1 - w \cdot z_k) \ge \alpha_k (1 - w \cdot z_k)$. So $J(w) \ge \frac{\lambda}{2}\lVert w \rVert^2 + \frac{1}{P} \sum_k \alpha_k - \frac{1}{P} w \cdot v$. The right side is a convex quadratic in $w$, minimized at $w = v / (\lambda P)$ with the value $D(\alpha)$. For the coordinate step, $D$ along $\alpha_k + \delta$ is the concave parabola $D(\alpha) + \frac{\delta}{P} - \frac{1}{2\lambda P^2}(2 \delta\, z_k \cdot v + \delta^2 \lVert z_k \rVert^2)$, whose maximum over $\delta$ is at $\delta = (\lambda P - z_k \cdot v)/\lVert z_k \rVert^2$; clipping to the interval keeps the maximum of a concave function over an interval. $\square$

So $J_{\text{best}} - J^* \le J_{\text{best}} - D(\alpha)$ for any $\alpha$, which the tests use to check the theorem without knowing $J^*$.

**Lemma 4 (a small objective orders every pair).** If $J(w) < 1/P$, then $w \cdot x_i > w \cdot x_j$ for every pair with $y_i > y_j$. Also, the number of pairs that $w$ misorders is at most $P\, J(w)$.

*Proof.* A pair with $w \cdot z_k \le 0$ has hinge loss at least 1, so it adds at least $1/P$ to $J(w)$. So $J(w) \ge (\text{number of misordered pairs}) / P$, which gives both claims. $\square$

The number of misordered pairs of one query is the [Kendall tau distance](/kendall-tau-distance/) between the order by $w$ and the order by label, counted over the pairs with different labels. Lemma 4 is the bound of Joachims (2002) that the hinge sum is an upper bound on it.

**Corollary (separable data).** If some $u$ has $u \cdot z_k \ge 1$ for all $k$ and $\frac{\lambda}{2} \lVert u \rVert^2 < 1/P$, then $J^* < 1/P$, and by the theorem the best iterate reaches $J_{\text{best}} < 1/P$ after finitely many steps, after which it orders every pair correctly.

*Proof.* $J^* \le J(u) = \frac{\lambda}{2} \lVert u \rVert^2$. The bound of the theorem tends to 0, so it falls below $1/P - J^*$ for some $T$. Apply Lemma 4. $\square$

**What is not proved.** All statements are about the training pairs. The quality of the ranking on new queries is a matter of measurement, and the margin theory of SVMs bounds it only under assumptions on how the queries are drawn.

The tests in `impl/python/test_ranking_svm.py` check the inequality of Lemma 2 on random points, the theorem against the dual lower bound of Lemma 3 for two values of $\lambda$ and three values of $T$, weak duality, Lemma 4 on random points around a separating vector, the corollary on a planted separable instance, and the worked example of the page.
