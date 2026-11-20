---
title: The WMMSE iteration never decreases the weighted sum rate, meets the power constraint, and its fixed points are KKT points of the weighted sum rate problem
proves: [correctness]
status: full
---

The model is $y_k = h_k^H x + w_k$ for $k = 1, \ldots, K$, with $h_k \in \mathbb{C}^M$, $w_k \sim \mathcal{CN}(0, N_0)$, $N_0 > 0$, and $x = \sum_k v_k s_k$ with independent unit-energy symbols. Let $T_k(V) = \sum_j |h_k^H v_j|^2 + N_0$ and $\mathrm{SINR}_k(V) = |h_k^H v_k|^2 / (T_k - |h_k^H v_k|^2)$. For weights $a_k > 0$, the problem is

$$\text{maximize } R(V) = \sum_k a_k \log_2(1 + \mathrm{SINR}_k(V)) \quad \text{subject to} \quad \sum_k \|v_k\|^2 \le P.$$

The receiver of user $k$ estimates $s_k$ as $\bar u_k y_k$. Its MSE is $e_k(u_k, V) = E|\bar u_k y_k - s_k|^2 = |u_k|^2 T_k - 2 \mathrm{Re}(\bar u_k h_k^H v_k) + 1$. WMMSE works on

$$G(u, w, V) = \sum_k a_k \bigl(w_k e_k(u_k, V) - \ln w_k\bigr), \qquad w_k > 0.$$

Lines L2, L3 and L4 to L6 minimize $G$ over $u$, over $w$ and over $V$, in turn.

**Lemma 1 (the receive step).** For fixed $V$, $e_k$ is minimized by $u_k = h_k^H v_k / T_k$ (line L2), with the minimum $e_k^\star = 1 - \bar u_k h_k^H v_k = 1 / (1 + \mathrm{SINR}_k)$, which lies in $(0, 1]$.

*Proof.* $e_k$ is a convex quadratic in $u_k$ with the positive coefficient $T_k \ge N_0$, and its gradient with respect to $\bar u_k$ is $T_k u_k - h_k^H v_k$. At the zero, $e_k = |h_k^H v_k|^2 / T_k - 2 |h_k^H v_k|^2 / T_k + 1 = 1 - |h_k^H v_k|^2 / T_k$, which is $1 - \bar u_k h_k^H v_k$ and equals $(T_k - |h_k^H v_k|^2) / T_k = 1 / (1 + \mathrm{SINR}_k)$. It is positive because $T_k - |h_k^H v_k|^2 \ge N_0 > 0$. $\square$

**Lemma 2 (the weight step).** For $e > 0$, $w e - \ln w$ over $w > 0$ has the unique minimizer $w = 1/e$ (line L3), with the value $1 + \ln e$.

*Proof.* The function is strictly convex in $w$, and its derivative $e - 1/w$ is zero only at $w = 1/e$. $\square$

So, with $F(V) = \min_{u, w} G(u, w, V)$, Lemmas 1 and 2 give

$$F(V) = \sum_k a_k \bigl(1 + \ln e_k^\star\bigr) = \sum_k a_k - \ln 2 \cdot R(V).$$

Minimizing $F$ is the same as maximizing $R$.

**Lemma 3 (the precoder step).** For fixed $u$ and $w$, let $A = \sum_j a_j w_j |u_j|^2 h_j h_j^H$ and $b_k = a_k w_k u_k h_k$. Then $G(u, w, V) = \sum_k \bigl(v_k^H A v_k - 2 \mathrm{Re}(b_k^H v_k)\bigr) + c$, where $c$ does not depend on $V$. A minimizer over $\sum_k \|v_k\|^2 \le P$ is $v_k = (A + \mu I)^{-1} b_k$, with $\mu = 0$ if this choice with $\mu = 0$ is defined and meets the power, and otherwise the $\mu > 0$ with $\sum_k \|(A + \mu I)^{-1} b_k\|^2 = P$.

*Proof.* Expand $\sum_k a_k w_k e_k$. The quadratic part is $\sum_k a_k w_k |u_k|^2 \sum_j |h_k^H v_j|^2 = \sum_j v_j^H A v_j$, and the linear part is $-2 \mathrm{Re} \sum_k a_k w_k \bar u_k h_k^H v_k = -2 \mathrm{Re} \sum_k b_k^H v_k$. $A$ is positive semidefinite, so the problem is convex, and $V = 0$ is strictly feasible, so the KKT conditions are necessary and sufficient: $(A + \mu I) v_k = b_k$, $\mu \ge 0$, $\sum_k \|v_k\|^2 \le P$ and $\mu (\sum_k \|v_k\|^2 - P) = 0$. If $A$ is invertible and $f(0) \le P$, where $f(\mu) = \sum_k \|(A + \mu I)^{-1} b_k\|^2$, then $\mu = 0$ satisfies them. Otherwise, in the eigenbasis $A = \sum_i \lambda_i q_i q_i^H$, $f(\mu) = \sum_{i, k} |q_i^H b_k|^2 / (\lambda_i + \mu)^2$, which is continuous and strictly decreasing on $(0, \infty)$ (unless all $b_k = 0$, when $V = 0$ is optimal) and tends to 0. Each $b_k$ is 0 or a multiple of $h_k$ with $u_k \ne 0$, and then $h_k$ is in the range of $A$, so $b_k$ has no component on the eigenvectors with $\lambda_i = 0$. So $f(0^+) = \lim_{\mu \to 0} f(\mu)$ is finite. If $f(0^+) > P$, there is a unique $\mu > 0$ with $f(\mu) = P$, and it satisfies the KKT conditions. If $f(0^+) \le P$, the limit $\mu \to 0^+$ gives the minimum norm solution of $A v_k = b_k$, which satisfies them with $\mu = 0$. $\square$

The implementation finds the root of $f(\mu) = P$ by Newton's method on $f^{-1/2}$, kept inside a bracket $[\mathrm{lo}, \mathrm{hi}]$ with $f(\mathrm{lo}) > P \ge f(\mathrm{hi})$; the start $\mathrm{hi} = \sqrt{\sum_k \|b_k\|^2 / P}$ is valid because $f(\mu) \le \sum_k \|b_k\|^2 / \mu^2$. It stops when $|f - P| \le 10^{-14} P$, or returns the precoder at $\mathrm{hi}$, which meets the power.

**Theorem 1 (monotone rate).** Let $V^t$ be the precoder after iteration $t$, with $V^0$ feasible. Then every $V^t$ is feasible and $R(V^{t+1}) \ge R(V^t)$. The sequence $R(V^t)$ converges.

*Proof.* Let $(u^t, w^t)$ be the outputs of lines L2 and L3 for $V^t$. By Lemmas 1 and 2, $G(u^t, w^t, V^t) = F(V^t)$. By Lemma 3, $V^{t+1}$ minimizes $G(u^t, w^t, \cdot)$ over the feasible set, which contains $V^t$, so $V^{t+1}$ is feasible and $G(u^t, w^t, V^{t+1}) \le G(u^t, w^t, V^t)$. By the definition of $F$ as a minimum, $F(V^{t+1}) \le G(u^t, w^t, V^{t+1})$. So $F(V^{t+1}) \le F(V^t)$, which is $R(V^{t+1}) \ge R(V^t)$. The rate is bounded: $\mathrm{SINR}_k \le |h_k^H v_k|^2 / N_0 \le P \|h_k\|^2 / N_0$. A bounded nondecreasing sequence converges. $\square$

**Theorem 2 (fixed points are KKT points).** If $V$ is a fixed point of one iteration, then $V$ satisfies the KKT conditions of the weighted sum rate problem: $\nabla_{\bar v_k} R(V) = \lambda v_k$ for all $k$ with one $\lambda \ge 0$, and $\lambda (\sum_k \|v_k\|^2 - P) = 0$.

*Proof.* Lemma 1 gives $u(V)$ and Lemma 2 gives $w(V)$ as smooth functions of $V$ (as functions of the real and imaginary parts), because $T_k > 0$ and $e_k^\star > 0$. So $F(V) = G(u(V), w(V), V)$ is smooth, and by the chain rule

$$\nabla_V F = \nabla_V G + (\nabla_u G)\, \frac{\partial u}{\partial V} + (\nabla_w G)\, \frac{\partial w}{\partial V} = \nabla_V G \quad \text{at } (u(V), w(V), V),$$

since $\nabla_u G = 0$ and $\nabla_w G = 0$ at the minimizers $u(V)$ and $w(V)$, which are interior points. At a fixed point, $V$ is the output of Lemma 3 for $(u(V), w(V))$, so $\nabla_{\bar v_k} G + \mu v_k = 0$ with $\mu \ge 0$ and $\mu (\sum_k \|v_k\|^2 - P) = 0$. Hence $\nabla_{\bar v_k} F + \mu v_k = 0$. With $F = \sum_k a_k - \ln 2 \cdot R$, this is $\nabla_{\bar v_k} R = (\mu / \ln 2) v_k$, the KKT condition with $\lambda = \mu / \ln 2$. $\square$

The problem is not convex, so a KKT point can be a local maximum or a saddle point and not the global maximum. The tests include a two-user channel where the default start converges to a worse point than another start.

**Theorem 3 (one user).** For $K = 1$, every precoder step returns a multiple of $h_1$, and the only fixed points are $v_1 = e^{j \phi} \sqrt{P}\, h_1 / \|h_1\|$, the maximum ratio transmission beam with the rate $a_1 \log_2(1 + P \|h_1\|^2 / N_0)$, which is the global maximum.

*Proof.* Here $A = c\, h_1 h_1^H$ with $c = a_1 w_1 |u_1|^2$ and $b_1 = a_1 w_1 u_1 h_1$. $h_1$ is an eigenvector of $A + \mu I$, so $(A + \mu I)^{-1} b_1$ is a multiple of $h_1$ (the minimum norm solution for $\mu \to 0^+$ too). For the fixed points, let $v_1 = \beta h_1$ with $p = |\beta|^2 \|h_1\|^2 \le P$ and $S = |h_1^H v_1|^2 = p \|h_1\|^2$. If $\mu = 0$ at a fixed point, then $v_1 = h_1 / (\bar u_1 \|h_1\|^2)$, so $p = 1 / (|u_1|^2 \|h_1\|^2) = (S + N_0)^2 / (S \|h_1\|^2)$, and with $S = p \|h_1\|^2$ this gives $S^2 = (S + N_0)^2$, which is impossible for $N_0 > 0$. So $\mu > 0$ and $p = P$. The rate $\log_2(1 + |h_1^H v_1|^2 / N_0)$ is at most $\log_2(1 + P \|h_1\|^2 / N_0)$ by the Cauchy-Schwarz inequality, with equality exactly for these beams. $\square$

**Theorem 4 (orthogonal channels).** If $h_k = \sqrt{g_k N_0}\, q_k$ for orthonormal $q_1, \ldots, q_K$, the maximum of $R$ is $\sum_k a_k \log_2(1 + g_k p_k)$ with the weighted water-filling powers $p_k = (a_k / \lambda - 1 / g_k)^+$, where $\lambda > 0$ is set by $\sum_k p_k = P$.

*Proof.* For any feasible $V$, $\mathrm{SINR}_k \le |h_k^H v_k|^2 / N_0 \le g_k \|v_k\|^2$, so $R(V) \le \sum_k a_k \log_2(1 + g_k \|v_k\|^2)$ with $\sum_k \|v_k\|^2 \le P$. The right side is a concave function of the powers $\|v_k\|^2$, and its KKT conditions give $a_k g_k / (1 + g_k p_k) = \lambda$ for $p_k > 0$ and $a_k g_k \le \lambda$ for $p_k = 0$ (the factor $1 / \ln 2$ is put into $\lambda$), which is the formula. The choice $v_k = \sqrt{p_k}\, q_k$ gives no interference and $\mathrm{SINR}_k = g_k p_k$, so it reaches the bound. $\square$

The tests check Theorem 1 (the rate never drops by more than $10^{-12}$ in 15 iterations, for up to 8 users and 8 antennas), the power within $10^{-9}$, Theorem 2 by a finite difference gradient at convergence, Theorem 3, Theorem 4 (WMMSE reaches the weighted water-filling value), a grid search over the beam parameters for two users (the best of six starts matches the grid within $10^{-3}$ and is never below it), and the local optimum mentioned after Theorem 2.
