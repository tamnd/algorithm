---
title: Weak-constraint 4D-Var has the exact adjoint gradient, and for a linear model its minimizer is the Kalman smoother with model error
proves: [correctness, termination]
status: full
---

**Setting.** The window has the time levels $0, \ldots, K$. The model steps $M_k$ are differentiable with Jacobians $M_k'(x)$, and the trajectory of the control $z = (x_0, \eta_1, \ldots, \eta_K)$ is $x_k = M_k(x_{k-1}) + \eta_k$. $B$, all $Q_k$ and all $R_k$ are symmetric positive definite, and $T$ is the set of times with observations $y_k = H_k x_k + \epsilon_k$. The cost is

$$J(z) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k=1}^K \tfrac12 \eta_k^\top Q_k^{-1}\eta_k + \sum_{k \in T} \tfrac12 d_k^\top R_k^{-1} d_k, \qquad d_k = y_k - H_k x_k .$$

**Lemma 1 (gradient).** Let $f_k = -H_k^\top R_k^{-1} d_k$ for $k \in T$ and $f_k = 0$ otherwise, and let $\mu_K = f_K$, $\mu_k = f_k + M_{k+1}'(x_k)^\top \mu_{k+1}$ (the values the backward sweep of line L5 stores after the forcing at each time). Then

$$\nabla_{x_0} J = B^{-1}(x_0 - x^b) + \mu_0, \qquad \nabla_{\eta_k} J = Q_k^{-1}\eta_k + \mu_k \quad (k = 1, \ldots, K).$$

*Proof.* $\mu_k$ is the gradient of the observation term with respect to $x_k$, with all later states seen as functions of $x_k$ and the later $\eta_j$: the term at time $k$ gives $f_k$, and the terms after $k$ act on $x_k$ only through $x_{k+1} = M_{k+1}(x_k) + \eta_{k+1}$, which gives $M_{k+1}'(x_k)^\top \mu_{k+1}$ by the chain rule. A change of $\eta_k$ changes $x_k$ by the same amount and nothing before time $k$, so the observation term has the gradient $\mu_k$ with respect to $\eta_k$. The same holds for $x_0$ with $\mu_0$. The background and model error terms add $B^{-1}(x_0 - x^b)$ and $Q_k^{-1}\eta_k$. $\square$

**Lemma 2 (the inner problem).** Let $G$ be the linear map from an increment $\delta z = (\delta x_0, \delta\eta_1, \ldots, \delta\eta_K)$ to the trajectory increments, $\delta x_k = M_k'(x_{k-1})\delta x_{k-1} + \delta\eta_k$, and let $D = \mathrm{diag}(B^{-1}, Q_1^{-1}, \ldots, Q_K^{-1})$. Line L6 applies

$$A = D + G^\top \Big(\textstyle\bigoplus_{k \in T} H_k^\top R_k^{-1} H_k\Big) G ,$$

which is symmetric positive definite, and line L7 gives the unique minimizer of $J$ with the model linearized along the current trajectory.

*Proof.* The forward loop inside `apply_a` computes $G\,\delta z$, the forcing applies $H_k^\top R_k^{-1} H_k$, and the backward sweep with Lemma 1 applied to these forcings computes $G^\top$ of the result, so `apply_a` is $A$. $v^\top A v \ge v^\top D v > 0$ for $v \ne 0$. With the linearized model the cost is a quadratic in $\delta z$ with Hessian $A$ and gradient $g$ at $\delta z = 0$, where $g = \nabla J(z)$ by Lemma 1, so its minimizer is $-A^{-1} g$. $\square$

So each outer loop is a Gauss-Newton step for $J$ over the control $z$, and $g^\top \delta z = -g^\top A^{-1} g < 0$ when $g \ne 0$.

**Theorem 3 (linear model).** Let $M_k(x) = Mx$. Then the first outer loop, with an exact inner solve, returns the unique minimizer of $J$. If $x_0 \sim N(x^b, B)$, $\eta_k \sim N(0, Q_k)$ and $\epsilon_k \sim N(0, R_k)$ are independent, the trajectory of the minimizer is $x_k^a = E[x_k \mid y]$ for every $k$, the mean of the Rauch-Tung-Striebel smoother with model error covariance $Q_k$, and $x_K^a$ is the Kalman filter mean at time $K$.

*Proof.* For a linear model the linearization is exact, so the first outer loop minimizes $J$ itself, and $J$ is strictly convex by Lemma 2. The map from $z$ to the trajectory is linear and invertible ($\eta_k = x_k - Mx_{k-1}$), and the prior density of $z$ times the likelihood of $y$ is proportional to $\exp(-J(z))$. So the posterior of $z$ is Gaussian with mean $\hat z = \arg\min J$, and since each $x_k$ is a linear function of $z$, $E[x_k \mid y]$ is the trajectory of $\hat z$. The Rauch-Tung-Striebel smoother computes $E[x_k \mid y]$ for this linear Gaussian model, and the Kalman filter computes $E[x_K \mid y_j, j \le K] = E[x_K \mid y]$. $\square$

**Strong-constraint limit.** As every $Q_k \to 0$, the penalty forces $\eta_k \to 0$, and the minimizer tends to the strong-constraint 4D-Var minimizer. In the linear case this is continuity of $E[x_k \mid y]$ in $Q$; the tests check it with $Q = 10^{-9}$ times a positive definite matrix.

**Termination.** The conjugate gradient method of line L7 stops after at most $2n(K+1)$ steps, and the outer loop runs at most `max_outer` times.

**Summary.** The backward sweep gives the exact gradient over the initial state and all model errors. Each outer loop is a Gauss-Newton step with a strictly convex inner problem. For a linear model one outer loop gives the minimizer, whose trajectory is the Kalman smoother mean with model error $Q$. The tests check this to $10^{-8}$ against a separate Kalman filter and smoother, and the gradient against finite differences. $\blacksquare$
