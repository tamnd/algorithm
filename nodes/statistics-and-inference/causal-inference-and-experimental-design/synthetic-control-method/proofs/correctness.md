---
title: The synthetic control solver returns a minimizer over the simplex, with an exact certificate
proves: [correctness]
status: full
---

Let $x_1 \in \mathbb{R}^k$, let $X_0$ be a $k \times J$ matrix, and let $v \in \mathbb{R}^k$ have positive entries, $V = \operatorname{diag}(v)$. The problem is

$$\min_{w \in \Delta} f(w), \qquad f(w) = (x_1 - X_0w)^\top V(x_1 - X_0w), \qquad \Delta = \{w \in \mathbb{R}^J : w \ge 0,\ \textstyle\sum_j w_j = 1\}.$$

The gradient is $g(w) = \nabla f(w) = -2X_0^\top V(x_1 - X_0w)$ and the Hessian is $H = 2X_0^\top VX_0$, which is positive semidefinite. So $f$ is convex. SYNTH starts at the centre of $\Delta$ (line L1), computes $g$ (line L3) and the Frank-Wolfe gap $\gamma(w) = g(w)^\top w - \min_j g_j(w)$ (line L4), stops when the gap is small or the KKT check succeeds (line L5), and otherwise takes the step $w \leftarrow \Pi_\Delta(w - g/L)$ (line L6), where $\Pi_\Delta$ is the Euclidean projection onto $\Delta$. Line L7 solves the KKT system on the support.

**Lemma 1 (existence).** $f$ has a minimizer on $\Delta$. It is unique if $X_0$ has full column rank.

*Proof.* $\Delta$ is compact and $f$ is continuous, so the minimum is attained. If $X_0$ has rank $J$, then $H$ is positive definite and $f$ is strictly convex, and a strictly convex function has at most one minimizer on a convex set. $\square$

When $J > k$, as is usual with many donors and few pre-periods, the minimizer need not be unique. The fitted point $X_0w^*$ is always unique, because it is the point of the convex hull of the donor columns nearest to $x_1$ in the norm of $V$, and by Carathéodory's theorem it is a convex combination of at most $k + 1$ donors. So some minimizer has at most $k + 1$ positive weights. The solver returns one minimizer in every case.

**Lemma 2 (projection onto the simplex).** For $u \in \mathbb{R}^J$ let $u_{(1)} \ge \dots \ge u_{(J)}$ be its sorted entries, $\rho$ the largest $i$ with $u_{(i)} - \frac{1}{i}(\sum_{l \le i}u_{(l)} - 1) > 0$, and $\theta = \frac{1}{\rho}(\sum_{l \le \rho}u_{(l)} - 1)$. Then $\Pi_\Delta(u)_j = \max(u_j - \theta, 0)$.

*Proof.* The projection minimizes $\frac12\lVert p - u\rVert^2$ over $\Delta$. This is strictly convex, so the KKT conditions characterize the unique solution: there are $\theta$ and $\mu \ge 0$ with $p_j - u_j + \theta - \mu_j = 0$ and $\mu_jp_j = 0$. Hence $p_j = \max(u_j - \theta, 0)$, and $\theta$ is fixed by $\sum_j\max(u_j - \theta, 0) = 1$. The left side is continuous and strictly decreasing in $\theta$ where it is positive, so this $\theta$ is unique. If exactly the $\rho'$ largest entries are positive after the shift, then $\theta = \frac{1}{\rho'}(\sum_{l \le \rho'}u_{(l)} - 1)$ and $u_{(\rho')} > \theta \ge u_{(\rho' + 1)}$. Write $t_i = \frac1i(\sum_{l \le i}u_{(l)} - 1)$ and $\varphi(i) = i(u_{(i)} - t_i) = 1 - \sum_{l \le i}(u_{(l)} - u_{(i)})$. The test of the lemma is $\varphi(i) > 0$. The function $\varphi$ is nonincreasing, since $\varphi(i + 1) - \varphi(i) = -i(u_{(i)} - u_{(i + 1)}) \le 0$. At $i = \rho'$ it is positive, because $u_{(\rho')} > \theta$ gives $\sum_{l \le \rho'}(u_{(l)} - u_{(\rho')}) < \sum_{l \le \rho'}(u_{(l)} - \theta) = 1$. At $i = \rho' + 1$ it is not positive, because $u_{(\rho' + 1)} \le \theta$ gives $\sum_{l \le \rho' + 1}(u_{(l)} - u_{(\rho' + 1)}) \ge \sum_{l \le \rho'}(u_{(l)} - \theta) = 1$. So the test holds exactly for $i \le \rho'$, $\rho = \rho'$, and $t_\rho = \theta$. $\square$

This is the algorithm analyzed by Duchi et al. (2008); PROJECT-SIMPLEX in the code keeps the last $t_i$ for which the test holds, which is $t_\rho$.

**Lemma 3 (the gap bounds the error).** For every $w \in \Delta$, $f(w) - \min_\Delta f \le \gamma(w)$, and $\gamma(w) \ge 0$.

*Proof.* Let $w^*$ be a minimizer. Convexity gives $f(w^*) \ge f(w) + g^\top(w^* - w)$, so $f(w) - f(w^*) \le g^\top w - g^\top w^*$. Since $w^* \in \Delta$, $g^\top w^*$ is a weighted mean of the $g_j$ and is at least $\min_jg_j$. So $f(w) - f(w^*) \le g^\top w - \min_jg_j = \gamma(w)$. Also $g^\top w \ge \min_j g_j$ for the same reason, so $\gamma \ge 0$. $\square$

**Theorem 4 (the KKT certificate).** Let $w \in \Delta$, $S = \{j : w_j > 0\}$ and $\nu \in \mathbb{R}$ with $g_j(w) = \nu$ for $j \in S$ and $g_j(w) \ge \nu$ for $j \notin S$. Then $w$ minimizes $f$ on $\Delta$.

*Proof.* $g^\top w = \sum_{j \in S}w_j\nu = \nu$ and $\min_jg_j = \nu$, so $\gamma(w) = 0$, and Lemma 3 gives $f(w) \le \min_\Delta f$. $\square$

Line L7 builds such a $w$. With $A$ the columns of $X_0$ in $S$, the conditions $g_S = \nu\mathbf 1$ and $\mathbf 1^\top w_S = 1$ are the linear system

$$2A^\top VA\,w_S - \nu\mathbf 1 = 2A^\top Vx_1, \qquad \mathbf 1^\top w_S = 1,$$

which the code solves by Gauss-Jordan elimination in the input arithmetic. It accepts the result only if $w_S > 0$ and $g_j \ge \nu - \epsilon(1 + \lvert\nu\rvert)$ off $S$. With fractions the equalities on $S$ hold exactly, and the acceptance test then gives $\gamma(w) \le \epsilon(1 + \lvert\nu\rvert)$ by the computation in the proof, so $f(w) - \min f \le \epsilon(1 + \lvert\nu\rvert)$ with $\epsilon = 10^{-9}$. If every off-support gradient entry is at least $\nu$, which the tests check exactly, $w$ is an exact minimizer. If the system is singular or the test fails, SYNTH returns the gradient iterate, whose error is at most its final gap by Lemma 3.

**Theorem 5 (the step size).** $\nabla f$ is Lipschitz with constant $\lambda_{\max}(H) \le L = 2\sum_{r, j}v_rX_{0, rj}^2$.

*Proof.* $\lVert g(w) - g(w')\rVert = \lVert H(w - w')\rVert \le \lambda_{\max}(H)\lVert w - w'\rVert$, and $\lambda_{\max}(H) \le \operatorname{tr}H = 2\sum_r v_r\sum_jX_{0, rj}^2$ because $H$ is positive semidefinite. $\square$

With a step $1/L$ for an $L$ at least the Lipschitz constant, projected gradient descent satisfies $f(w_t) - \min f \le L\lVert w_0 - w^*\rVert^2/(2t)$ (Beck and Teboulle 2009, for the basic proximal gradient method; cited, not proved here). From the centre of $\Delta$, $\lVert w_0 - w^*\rVert^2 \le 1 - 1/J < 1$, so $t \ge L/(2\varepsilon)$ iterations give error at most $\varepsilon$. When the minimizer is unique and strictly complementary, projected gradient also finds the support after finitely many steps, after which the KKT check of line L5 succeeds. The code relies on this only for speed: correctness rests on Lemma 3 and Theorem 4. The measured counts are on the main page.

**Theorem 6 (the placebo p-value).** Let $R_0, \dots, R_J$ be the statistics of the treated unit and the $J$ donors, each computed by refitting with that unit as treated. If under the null hypothesis the vector $(R_0, \dots, R_J)$ is exchangeable, then $p = \#\{u : R_u \ge R_0\}/(J + 1)$ satisfies $\Pr[p \le m/(J + 1)] \le m/(J + 1)$ for $m = 1, \dots, J + 1$.

*Proof.* $p \le m/(J + 1)$ means at most $m$ of the $R_u$ are at least $R_0$, which places $R_0$ among the $m$ largest values counting ties against it. By exchangeability each position is equally likely to hold the unit called 0, and at most $m$ of the $J + 1$ positions satisfy the condition. $\square$

Exchangeability holds when the treated unit was picked at random, which is rarely true; otherwise the p-value is a description of how unusual the treated unit's gap is among the placebo gaps.

**What is not proved here.** The convergence rate of Theorem 5's step and the finite identification of the support are cited. The statistical properties of the estimate, that the gap after the intervention is close to the effect when the pre-period fit is good, rest on a model for the untreated outcomes. Abadie, Diamond and Hainmueller (2010) bound the bias under a linear factor model with a perfect pre-period fit, the bound shrinking as the number of pre-periods grows. That result is cited, and the simulation on the main page measures the behaviour only for one design.
