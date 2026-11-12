---
title: The SVR dual, its KKT conditions, and why the 2n-variable solver returns the optimal fit
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $(x_i, y_i)$, $i = 1, \ldots, n$, be the data with $y_i \in \mathbb{R}$, let $k(x, z) = \varphi(x) \cdot \varphi(z)$ be a positive semidefinite kernel with Gram matrix $K$, and let $\varepsilon \ge 0$ and $C > 0$. Write $f(x) = w \cdot \varphi(x) + b$ and $r_i = y_i - f(x_i)$. The primal problem is

$$(P) \quad \min \; \tfrac12 \lVert w \rVert^2 + C \sum_i (\xi_i + \xi_i^*) \quad \text{s.t. } r_i \le \varepsilon + \xi_i, \; -r_i \le \varepsilon + \xi_i^*, \; \xi_i, \xi_i^* \ge 0.$$

**Lemma 1 (the primal has a solution).** The point $w = 0$, $b = 0$, $\xi_i = \xi_i^* = \lvert y_i \rvert$ is feasible, so the optimal value is finite. For fixed $(w, b)$ the best slacks are $\xi_i = \max(0, r_i - \varepsilon)$ and $\xi_i^* = \max(0, -r_i - \varepsilon)$, so (P) is the minimization of $J(w, b) = \tfrac12 \lVert w \rVert^2 + C \sum_i \lvert r_i \rvert_\varepsilon$. As for the SVM, we may restrict $w$ to the span of the $\varphi(x_i)$. Then $J$ is continuous, convex, and coercive: it grows without bound as $\lVert w \rVert \to \infty$, and as $\lvert b \rvert \to \infty$ with $w$ bounded, because every $\lvert r_i \rvert_\varepsilon$ grows. So a minimizer exists. The term $\tfrac12 \lVert w \rVert^2$ is strictly convex and the rest is convex, so $w$ is the same in every minimizer.

**Lemma 2 (the dual).** With multipliers $\alpha_i, \alpha_i^*, \eta_i, \eta_i^* \ge 0$,

$$L = \tfrac12 \lVert w \rVert^2 + C \sum_i (\xi_i + \xi_i^*) - \sum_i \alpha_i (\varepsilon + \xi_i - r_i) - \sum_i \alpha_i^* (\varepsilon + \xi_i^* + r_i) - \sum_i (\eta_i \xi_i + \eta_i^* \xi_i^*).$$

Since $r_i = y_i - w \cdot \varphi(x_i) - b$, setting the derivatives to zero gives $w = \sum_i (\alpha_i - \alpha_i^*) \varphi(x_i)$ from $w$, $\sum_i (\alpha_i - \alpha_i^*) = 0$ from $b$, and $C - \alpha_i - \eta_i = 0$ and $C - \alpha_i^* - \eta_i^* = 0$ from the slacks, so $0 \le \alpha_i, \alpha_i^* \le C$. Substituting, with $\theta = \alpha - \alpha^*$,

$$D(\alpha, \alpha^*) = -\tfrac12 \theta^\top K \theta - \varepsilon \sum_i (\alpha_i + \alpha_i^*) + y^\top \theta,$$

which is the dual of the page. For $\beta = (\alpha, \alpha^*)$, $z = (+1^n, -1^n)$, $Q_{st} = z_s z_t K_{s \bmod n, t \bmod n}$ and $p = (\varepsilon - y, \varepsilon + y)$ we have $\beta^\top Q \beta = \sum_{s,t} (z_s \beta_s)(z_t \beta_t) K_{s \bmod n, t \bmod n} = \theta^\top K \theta$, because $z_s \beta_s$ summed over the two copies $s = i$ and $s = n + i$ of index $i$ is $\alpha_i - \alpha_i^* = \theta_i$, and $p^\top \beta = \varepsilon \sum_i (\alpha_i + \alpha_i^*) - y^\top \theta$. Also $z^\top \beta = \sum_i \theta_i$. So $\tfrac12 \beta^\top Q \beta + p^\top \beta = -D$, and line L3 maximizes $D$ over the dual feasible set.

**Lemma 3 (weak duality with an explicit gap).** For primal feasible $(w, b, \xi, \xi^*)$ and dual feasible $(\alpha, \alpha^*)$ with $w_\theta = \sum_i \theta_i \varphi(x_i)$,

$$P - D = \tfrac12 \lVert w - w_\theta \rVert^2 + \sum_i \alpha_i (\varepsilon + \xi_i - r_i) + \sum_i \alpha_i^* (\varepsilon + \xi_i^* + r_i) + \sum_i (C - \alpha_i) \xi_i + \sum_i (C - \alpha_i^*) \xi_i^* \ge 0.$$

*Proof.* Expand the right side. The terms in $\xi$ and $\xi^*$ add up to $C \sum_i (\xi_i + \xi_i^*)$. The terms in $\varepsilon$ give $\varepsilon \sum_i (\alpha_i + \alpha_i^*)$. The terms in $r_i$ give $-\sum_i \theta_i r_i = -y^\top \theta + \sum_i \theta_i w \cdot \varphi(x_i) + b \sum_i \theta_i$, and the last sum is 0. Finally $\tfrac12 \lVert w - w_\theta \rVert^2 = \tfrac12 \lVert w \rVert^2 - w \cdot w_\theta + \tfrac12 \theta^\top K \theta$ and $w \cdot w_\theta = \sum_i \theta_i w \cdot \varphi(x_i)$. The total is $\tfrac12 \lVert w \rVert^2 + C \sum_i (\xi_i + \xi_i^*) + \varepsilon \sum_i (\alpha_i + \alpha_i^*) - y^\top \theta + \tfrac12 \theta^\top K \theta = P - D$. Every term is nonnegative by feasibility. $\square$

**Lemma 4 (KKT conditions).** The constraints of (P) are affine and (P) has a solution, so strong duality holds: there is a dual feasible point with $D = P^*$. By Lemma 3, a primal feasible and a dual feasible point are both optimal if and only if every term of the gap is 0. Take the best slacks of Lemma 1. Then the conditions are $w = w_\theta$ and, for each $i$:

- $\alpha_i (\varepsilon + \xi_i - r_i) = 0$ and $(C - \alpha_i) \xi_i = 0$. If $\alpha_i = 0$, then $\xi_i = 0$, so $r_i \le \varepsilon$. If $0 < \alpha_i < C$, then $\xi_i = 0$ and $r_i = \varepsilon$. If $\alpha_i = C$, then $r_i = \varepsilon + \xi_i \ge \varepsilon$.
- In the same way, $\alpha_i^* = 0$ gives $r_i \ge -\varepsilon$, $0 < \alpha_i^* < C$ gives $r_i = -\varepsilon$, and $\alpha_i^* = C$ gives $r_i \le -\varepsilon$.

This is the table of the page. If $\varepsilon > 0$ and both $\alpha_i > 0$ and $\alpha_i^* > 0$, then $r_i \ge \varepsilon$ and $r_i \le -\varepsilon$, which is impossible. So $\alpha_i \alpha_i^* = 0$ at every optimum when $\varepsilon > 0$.

**Lemma 5 (the KKT conditions of the 2n-variable problem).** For $\min \tfrac12 \beta^\top Q \beta + p^\top \beta$ subject to $z^\top \beta = 0$ and $0 \le \beta \le C$, a feasible $\beta$ is optimal if and only if there is a number $b$ with, for each $t$ and $G = Q \beta + p$,

$$G_t + b z_t \ge 0 \text{ if } \beta_t = 0, \qquad G_t + b z_t = 0 \text{ if } 0 < \beta_t < C, \qquad G_t + b z_t \le 0 \text{ if } \beta_t = C.$$

(This is the KKT system of a convex QP with affine constraints, with $b$ the multiplier of $z^\top \beta = 0$.) We show that these are the conditions of Lemma 4. Since $(Q\beta)_i = \sum_j \theta_j K_{ij} = f(x_i) - b$ for $t = i \le n$, we get $G_i + b = f(x_i) + \varepsilon - y_i = \varepsilon - r_i$. So for $\alpha_i$: $\beta_t = 0$ gives $r_i \le \varepsilon$, a free value gives $r_i = \varepsilon$, and $C$ gives $r_i \ge \varepsilon$. For $t = n + i$, $(Q\beta)_t = -(f(x_i) - b)$, and $G_t - b = -f(x_i) + \varepsilon + y_i = \varepsilon + r_i$. So for $\alpha_i^*$: $0$ gives $r_i \ge -\varepsilon$, free gives $r_i = -\varepsilon$, and $C$ gives $r_i \le -\varepsilon$. These are the six cases of Lemma 4, with the multiplier $b$ equal to the bias of $f$.

**Lemma 6 (the gap measure of the solver).** Rewrite the conditions of Lemma 5 with $z_t^2 = 1$. If $t \in I_{up}$, that is $\beta_t < C$ and $z_t = 1$, or $\beta_t > 0$ and $z_t = -1$, the conditions give $b \ge -z_t G_t$. If $t \in I_{low}$, they give $b \le -z_t G_t$. Conversely these inequalities for all $t$ imply the conditions of Lemma 5 (a free $t$ is in both sets, which forces equality). So a feasible $\beta$ is optimal if and only if $m(\beta) = \max_{t \in I_{up}} -z_t G_t \le M(\beta) = \min_{t \in I_{low}} -z_t G_t$, and then every $b \in [m, M]$ is optimal.

**Theorem.** Suppose line L3 stops with $m(\beta) - M(\beta) \le \tau$. Then the $b$ of line L5 lies in $[M, m]$ or $[m, M]$, so every condition of Lemma 6, and hence every entry of the KKT table of the page, holds within $\tau$. If $\tau = 0$, the pair $(\theta, b)$ is optimal: $f$ of line L7 has the unique optimal $w$ of (P) and an optimal $b$.

*Proof.* If some $\beta_t$ is free, it is in both $I_{up}$ and $I_{low}$, so $M \le -z_t G_t \le m$, and the mean of these values is in $[M, m]$. Otherwise line L5 takes $(m + M)/2$. In both cases $b$ is within $\tau$ of every bound of Lemma 6. By Lemma 5 these bounds are the KKT table of the page, with the same $b$. If $\tau = 0$, then $m \le M$ and $b \in [m, M]$, so Lemmas 6, 5 and 4 show that $\beta$ is dual optimal and $(w_\theta, b)$ is primal optimal. Line L4 forms $\theta = \alpha - \alpha^*$, and line L7 drops only the terms with $\theta_i = 0$, so it returns $f(x) = w_\theta \cdot \varphi(x) + b$. That the SMO type method with WSS3 reaches the stopping rule after finitely many steps for every $\tau > 0$ is the convergence result of Fan, Chen and Lin (2005), proved for this general form of the problem. $\square$
