---
title: The adjoint sweep gives the gradient of the 4D-Var cost, and for a linear model the minimizer is the Kalman smoother estimate
proves: [correctness]
status: full
---

**Setting.** The window has the time levels $0, 1, \ldots, K$. The model steps are differentiable maps $M_k : \mathbb R^n \to \mathbb R^n$ with Jacobians $M_k'(x)$, and the trajectory from $x_0$ is $x_k = M_k(x_{k-1})$. The set $T \subseteq \{0, \ldots, K\}$ holds the times with observations $y_k \in \mathbb R^{p_k}$, linear operators $H_k$ and symmetric positive definite error covariances $R_k$. $B$ is symmetric positive definite. The cost is

$$J(x_0) = \tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b) + \sum_{k \in T} \tfrac12 d_k^\top R_k^{-1} d_k, \qquad d_k = y_k - H_k x_k .$$

Write $M_{0 \to k} = M_k \circ \cdots \circ M_1$, so $x_k = M_{0 \to k}(x_0)$, and write $M'_{0 \to k} = M_k'(x_{k-1}) \cdots M_1'(x_0)$ for its Jacobian at $x_0$ (chain rule).

**Lemma 1 (gradient).** The vector $g$ of line L9 is $\nabla J(x_0)$.

*Proof.* By the chain rule,

$$\nabla J(x_0) = B^{-1}(x_0 - x^b) - \sum_{k \in T} (M'_{0 \to k})^\top H_k^\top R_k^{-1} d_k .$$

Let $f_k = H_k^\top R_k^{-1} d_k$ for $k \in T$ and $f_k = 0$ otherwise. Let $\lambda^{(k)}$ be the value of $\lambda$ after line L7 at time $k$. We claim

$$\lambda^{(k)} = -\sum_{j \ge k} M_{k+1}'(x_k)^\top \cdots M_j'(x_{j-1})^\top f_j ,$$

where the empty product for $j = k$ is the identity. For $k = K$, line L5 sets $\lambda = 0$ and line L7 gives $\lambda^{(K)} = -f_K$. If the claim holds for $k$, line L8 multiplies by $M_k'(x_{k-1})^\top$ and line L7 at time $k - 1$ subtracts $f_{k-1}$, which gives the claim for $k - 1$. At $k = 0$ the claim reads $\lambda^{(0)} = -\sum_j (M'_{0 \to j})^\top f_j$, because $(M'_{0 \to j})^\top = M_1'(x_0)^\top \cdots M_j'(x_{j-1})^\top$. Line L9 adds $B^{-1}(x_0 - x^b)$. $\square$

So every iterate of line L11 uses the exact gradient. BFGS with the Armijo line search starts from $B$ as the inverse Hessian, keeps the inverse Hessian symmetric positive definite (the update is skipped when $s^\top y \le 0$), and so every search direction is a descent direction: $g^\top p = -g^\top H_{\text{inv}}\, g < 0$ for $g \ne 0$. For a strictly convex quadratic $J$ the iterates converge to the unique minimizer. For a nonconvex $J$ the method stops, by line L10, only near a stationary point.

**Theorem 2 (linear model).** Let $M_k(x) = M x$ for a fixed invertible matrix $M$. Then $J$ is strictly convex and has the unique minimizer

$$x_0^a = \Big(B^{-1} + \sum_{k \in T} (M^k)^\top H_k^\top R_k^{-1} H_k M^k\Big)^{-1}\Big(B^{-1} x^b + \sum_{k \in T} (M^k)^\top H_k^\top R_k^{-1} y_k\Big).$$

Let $x_0 \sim N(x^b, B)$, $x_k = M x_{k-1}$ (no model noise) and $y_k = H_k x_k + \epsilon_k$ with independent $\epsilon_k \sim N(0, R_k)$. Then $x_0^a = E[x_0 \mid y]$, and $M^k x_0^a = E[x_k \mid y]$ for every $k$. In particular $M^K x_0^a$ is the Kalman filter mean at time $K$, and $M^k x_0^a$ is the Rauch-Tung-Striebel smoother mean at time $k$ when that smoother runs with $Q = 0$.

*Proof.* With $x_k = M^k x_0$ the cost is a quadratic in $x_0$ with the Hessian $A = B^{-1} + \sum_{k \in T} (M^k)^\top H_k^\top R_k^{-1} H_k M^k$, and $v^\top A v \ge v^\top B^{-1} v > 0$ for $v \ne 0$. Setting the gradient to zero gives the formula.

By Bayes' theorem the posterior density of $x_0$ is proportional to

$$\exp\big(-\tfrac12 (x_0 - x^b)^\top B^{-1}(x_0 - x^b)\big) \prod_{k \in T} \exp\big(-\tfrac12 (y_k - H_k M^k x_0)^\top R_k^{-1}(y_k - H_k M^k x_0)\big) = \exp(-J(x_0)),$$

so the posterior is Gaussian with mean $x_0^a$ and covariance $A^{-1}$. Each $x_k = M^k x_0$ is a linear function of $x_0$, so $E[x_k \mid y] = M^k E[x_0 \mid y] = M^k x_0^a$.

The Kalman filter mean at time $K$ is $E[x_K \mid y_j, j \le K]$, which is $E[x_K \mid y]$ because the window ends at $K$. The Rauch-Tung-Striebel smoother gives $E[x_k \mid y]$ for the same linear Gaussian model. Both facts are the standard optimality of these recursions for linear Gaussian models (see the pages on the [Kalman filter](/kalman-filter/) and the [Rauch-Tung-Striebel smoother](/rauch-tung-striebel-smoother/)). With $Q = 0$ the smoother needs the predicted covariances $M P M^\top$ to be invertible, which holds because $M$ is invertible. $\square$

The tests check Theorem 2 to $10^{-8}$ against a Kalman filter and smoother written separately with Gaussian elimination, and Lemma 1 against central finite differences for Lorenz-63.

**Summary.** Lines L3 to L9 compute $J$ and its exact gradient with one forward run and one backward adjoint run. The minimizer uses descent directions only. For a linear model the cost is strictly convex, and its minimizer is the posterior mean of the initial state; run forward, it is the smoother mean at every time of the window and the Kalman filter mean at the end. $\blacksquare$
